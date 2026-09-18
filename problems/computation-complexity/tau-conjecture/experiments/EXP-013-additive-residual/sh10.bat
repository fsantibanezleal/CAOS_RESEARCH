@echo off
cd /d "%~dp0"
"%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 10 --nshards 20 >> shard_10.log 2>&1
