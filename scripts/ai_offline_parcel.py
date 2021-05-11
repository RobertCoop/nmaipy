import argparse
import concurrent.futures
import os
import random
from pathlib import Path
from typing import Optional

import geopandas as gpd
import numpy as np
import pandas as pd
from tqdm import tqdm

from nearmap_ai import parcels
from nearmap_ai.constants import AREA_CRS, BUILDING_ID, POOL_ID
from nearmap_ai.feature_api import FeatureApi

# TODO: This script is currently set up to run with buildings and pools, it should be generalized to take packs as an
#       argument and run with any set of features and attributes.

CHUNK_SIZE = 1000
PROCESSES = 20
THREADS = 4

PACKS = ["pool", "building"]
PARCEL_PROPERTIES = [
    "aoi_id",
    "address",
    "address_id",
    "geom_id",
    "jurisdiction_id",
    "lga_pid",
    "loc_pid",
    "locality",
    "lot_number",
    "parcl_stts",
    "plan_number",
    "latitude",
    "longitude",
    "parcel_area_sqm",
]

FINAL_COLUMNS = PARCEL_PROPERTIES + [
    "date",
    "building_present",
    "building_count",
    "building_total_area_sqm",
    "building_total_clipped_area_sqm",
    "building_confidence",
    "primary_building_area_sqm",
    "primary_building_clipped_area_sqm",
    "primary_building_confidence",
    "swimming_pool_present",
    "swimming_pool_count",
    "swimming_pool_total_area_sqm",
    "swimming_pool_total_clipped_area_sqm",
    "swimming_pool_confidence",
    "primary_swimming_pool_area_sqm",
    "primary_swimming_pool_clipped_area_sqm",
    "primary_swimming_pool_confidence",
    "system_version",
    "link",
]


def parse_arguments():
    """
    Get command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--parcel-dir", help="Directory with parcel files", type=str, required=True)
    parser.add_argument("--output-dir", help="Directory to store results", type=str, required=True)
    parser.add_argument("--key-file", help="Path to file with API keys", type=str, required=False, default=None)
    parser.add_argument("--workers", help="Number of processes", type=int, required=False, default=PROCESSES)
    return parser.parse_args()


def api_key(key_file: Optional[str] = None) -> str:
    """
    Get an API key. If a key file is specified a random key from the file will be returned.
    """
    if key_file is None:
        return os.environ["API_KEY"]
    with open(key_file, "r") as f:
        keys = [line.rstrip() for line in f]
    return keys[random.randint(0, len(keys) - 1)]


def process_chunk(
    chunk_id: str, parcel_gdf: gpd.GeoDataFrame, classes_df: pd.DataFrame, output_dir: str, key_file: str
):
    """
    Create a parcel rollup for a chuck of parcels.

    Args:
        chunk_id: Used to save data for the chunk
        parcel_gdf: Parcel set
        classes_df: Classes in output
        output_dir: Directory to save data to
        key_file: Path to API key file
    """
    cache_path = Path(output_dir) / "cache"
    chunk_path = Path(output_dir) / "chunks"
    outfile = chunk_path / f"rollup_{chunk_id}.parquet"
    outfile_errors = chunk_path / f"errors_{chunk_id}.parquet"
    if outfile.exists():
        return

    # Get additional parcel attributes from parcel geometry
    parcel_gdf["latitude"] = parcel_gdf.geometry.apply(lambda g: g.centroid.coords[0][1])
    parcel_gdf["longitude"] = parcel_gdf.geometry.apply(lambda g: g.centroid.coords[0][0])
    parcel_temp_gdf = parcel_gdf.to_crs(AREA_CRS["au"])
    parcel_gdf["parcel_area_sqm"] = parcel_temp_gdf.area.round(1)
    del parcel_temp_gdf

    # Get features
    feature_api = FeatureApi(api_key=api_key(key_file), cache_dir=cache_path, workers=THREADS)
    features_gdf, metadata_df, errors_df = feature_api.get_features_gdf_bulk(parcel_gdf, packs=PACKS)
    if len(errors_df) == len(parcel_gdf):
        errors_df.to_parquet(outfile_errors)
        return

    # Filter features
    features_gdf = parcels.filter_features_in_parcels(parcel_gdf, features_gdf, country="au")

    # Create rollup
    rollup_df = parcels.parcel_rollup(parcel_gdf, features_gdf, classes_df)

    # Put it all together and save
    final_df = metadata_df.merge(rollup_df, on="aoi_id").merge(parcel_gdf[PARCEL_PROPERTIES], on="aoi_id")
    final_df = final_df[FINAL_COLUMNS]
    errors_df.to_parquet(outfile_errors)
    final_df.to_parquet(outfile)


def main():
    args = parse_arguments()
    # Path setup
    parcel_paths = list(Path(args.parcel_dir).glob("*.parquet"))
    cache_path = Path(args.output_dir) / "cache"
    chunk_path = Path(args.output_dir) / "chunks"
    final_path = Path(args.output_dir) / "final"
    cache_path.mkdir(parents=True, exist_ok=True)
    chunk_path.mkdir(parents=True, exist_ok=True)
    final_path.mkdir(parents=True, exist_ok=True)

    # Get classes
    classes_df = FeatureApi(api_key=api_key(args.key_file)).get_feature_classes()
    classes_df = classes_df.loc[[BUILDING_ID, POOL_ID]]

    # Loop over parcel files
    for f in parcel_paths:
        print(f)
        # If output exists, skip
        outpath = final_path / f"{f.stem}.csv"
        if outpath.exists():
            continue
        # Read parcel data
        parcels_gdf = parcels.read_from_file(f)
        # Some parcel properties only exist for certain batches, so if they do not appear we fill them with Nones
        for parcel_prop in PARCEL_PROPERTIES:
            if parcel_prop not in parcels_gdf.columns:
                parcels_gdf[parcel_prop] = None
        jobs = []
        if args.workers > 1:
            with concurrent.futures.ProcessPoolExecutor(PROCESSES) as executor:
                # Chunk parcels and send chunks to process pool
                for i, batch in enumerate(np.array_split(parcels_gdf, len(parcels_gdf) // CHUNK_SIZE)):
                    chunk_id = f"{f.stem}_{str(i).zfill(4)}"
                    jobs.append(
                        executor.submit(process_chunk, chunk_id, batch, classes_df, args.output_dir, args.key_file)
                    )
                [j.result() for j in tqdm(jobs)]
        else:
            # If we only have one worker, run in main process
            for i, batch in tqdm(enumerate(np.array_split(parcels_gdf, len(parcels_gdf) // CHUNK_SIZE))):
                chunk_id = f"{f.stem}_{str(i).zfill(4)}"
                process_chunk(chunk_id, batch, classes_df, args.output_dir, args.key_file)

        # Combine chunks and save
        data = []
        errors = []
        for cp in chunk_path.glob(f"rollup_{f.stem}_*.parquet"):
            data.append(pd.read_parquet(cp))
        pd.concat(data).to_csv(outpath, index=False)
        for cp in chunk_path.glob(f"errors_{f.stem}_*.parquet"):
            errors.append(pd.read_parquet(cp))
        pd.concat(errors).to_csv(final_path / f"{f.stem}_errors.csv", index=False)


if __name__ == "__main__":
    main()