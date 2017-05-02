#!/bin/bash

pip install -r requirements.txt

# run pipe line
cd news_pipeline
python monitor.py &
python fetcher.py &
python deduper.py &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
