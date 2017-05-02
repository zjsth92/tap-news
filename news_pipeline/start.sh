#!/bin/bash
python monitor.py &
python fetcher.py &
python deduper.py