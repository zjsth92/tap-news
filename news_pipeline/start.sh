#!/bin/bash
echo "##### start news pipeline #####"
python -u monitor.py &
monitor_pid=$!
echo "monitor running on pid:$monitor_pid"
python -u fetcher.py &
fetcher_pid=$!
echo "fetcher running on pid:$fetcher_pid"
python -u deduper.py