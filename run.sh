export PYTHONPATH=.
python /home/jovyan/datascience/nearmap-ai-user-guides/scripts/ai_offline_parcel.py \
    --parcel-dir "" \
    --output-dir "" \
    --country us \
    --include-parcel-geometry \
    --packs building vegetation \
    --workers 2 \
    --compress-cache \
    --log-level INFO