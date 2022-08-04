# Default columns
AOI_ID_COLUMN_NAME = "aoi_id"
LAT_PRIMARY_COL_NAME = "lat"
LON_PRIMARY_COL_NAME = "lon"
SINCE_COL_NAME = "since"
UNTIL_COL_NAME = "until"
SURVEY_RESOURCE_ID_COL_NAME = "survey_resource_id"


MAX_RETRIES = 300

# Projections
LAT_LONG_CRS = "WGS 84"
AREA_CRS = {
    "au": "epsg:3577",
    "ca": "esri:102001",
    "nz": "epsg:3577",
    "us": "esri:102003",
}
API_CRS = "epsg:4326"

IMPERIAL_COUNTRIES = ["us"]


class MeasurementUnits:
    def __init__(self, country):
        self.country = country

    def area_units(self):
        if self.country in IMPERIAL_COUNTRIES:
            area_units = "sqft"
        else:
            area_units = "sqm"
        return area_units


# Error Codes
AOI_EXCEEDS_MAX_SIZE = "AOI_EXCEEDS_MAX_SIZE"

# Units
METERS_TO_FEET = 3.28084
SQUARED_METERS_TO_SQUARED_FEET = METERS_TO_FEET * METERS_TO_FEET

# The address fields expected by the address endpoint. state should be statecode (2 digit) but these
# are the API fields
ADDRESS_FIELDS = ("streetAddress", "city", "state", "zip")

# Class IDs
BUILDING_ID = "a2e4ae39-8a61-5515-9d18-8900aa6e6072"
ROOF_ID = "c08255a4-ba9f-562b-932c-ff76f2faeeeb"

TRAMPOLINE_ID = "753621ee-0b9f-515e-9bcf-ea40b96612ab"
POOL_ID = "0339726f-081e-5a6e-b9a9-42d95c1b5c8a"
CONSTRUCTION_ID = "a2a81381-13c6-57dc-a967-af696e45f6c7"
SOLAR_ID = "3680e1b8-8ae1-5a15-8ec7-820078ef3298"

VEG_VERYLOW_ID = "a7d921b7-393c-4121-b317-e9cda3e4c19b"
VEG_LOW_ID = "2780fa70-7713-437c-ad98-656b8a5cc4f2"
VEG_MEDHIGH_ID = "dfd8181b-80c9-4234-9d05-0eef927e3aca"
VEG_IDS = [VEG_VERYLOW_ID, VEG_LOW_ID, VEG_MEDHIGH_ID]

DIRT_GRAVEL_SAND_ID = "0ad1355f-5dfd-403b-8b8b-b7d8ed95731f"
WATER_BODY_ID = "2e0bd9e3-3b67-4990-84dc-1b4812fdd02b"
CONCRETE_ID = "290897be-078b-4948-97aa-755289a67a29"
ASPHALT_ID = "97a1f8a8-7cf2-4e81-82b4-753ee225d9ed"
LAWN_GRASS_ID = "68dc5061-5842-4a17-8073-e278a91b607d"
SURFACES_IDS = [
    WATER_BODY_ID,
    CONCRETE_ID,
    ASPHALT_ID,
    LAWN_GRASS_ID,
    DIRT_GRAVEL_SAND_ID,
]

METAL_ROOF_ID = "4424186a-0b42-5608-a5a0-d4432695c260"
TILE_ROOF_ID = "516fdfd5-0be9-59fe-b849-92faef8ef26e"
SHINGLE_ROOF_ID = "4bbf8dbd-cc81-5773-961f-0121101422be"

FLAT_ROOF_ID = "224f98d3-b853-542a-8b18-e1e46e3a8200"
HIP_ROOF_ID = "ac0a5f75-d8aa-554c-8a43-cee9684ef9e9"
GABLE_ROOF_ID = "59c6e27e-6ef2-5b5c-90e7-31cfca78c0c2"
DUTCH_GABLE_ROOF_ID = "3719eb40-d6d1-5071-bbe6-379a551bb65f"
TURRET_ROOF_ID = "89582082-e5b8-5853-bc94-3a0392cab98a"

TREE_OVERHANG_ID = "8e9448bd-4669-5f46-b8f0-840fee25c34c"

STRUCTURALLY_DAMAGED_ROOF = "f907e625-26b3-59db-a806-d41f62ce1f1b"
TEMPORARY_REPAIR = "abb1f304-ce01-527b-b799-cbfd07551b2c"
ROOF_PONDING = "f41e02b0-adc0-5b46-ac95-8c59aa9fe317"
ROOF_RUSTING = "526496bf-7344-5024-82d7-77ceb671feb4"
TILE_SHINGLE_DISCOLOURATION = "cfa8951a-4c29-54de-ae98-e5f804c305e3"

LEAF_OFF_VEG_ID = "cd47dfd1-2c24-543c-89fd-7677b2cc100b"
DRIVEABLE_ID = "372fb6c1-a3ab-5019-ba0f-489ed12079de"

ROOF_CHAR_IDS = [
    METAL_ROOF_ID,
    TILE_ROOF_ID,
    SHINGLE_ROOF_ID,
    FLAT_ROOF_ID,
    HIP_ROOF_ID,
    GABLE_ROOF_ID,
    DUTCH_GABLE_ROOF_ID,
    TURRET_ROOF_ID,
    TREE_OVERHANG_ID,
]
CLASSES_WITH_NO_PRIMARY_FEATURE = VEG_IDS + SURFACES_IDS + [TREE_OVERHANG_ID]

CONNECTED_CLASS_IDS = (
    SURFACES_IDS
    + VEG_IDS
    + [
        DRIVEABLE_ID,
        LEAF_OFF_VEG_ID,
    ]
)
