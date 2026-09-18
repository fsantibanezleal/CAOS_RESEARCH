@echo off
cd /d "%~dp0"
"%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 15 --nshards 20 >> shard_15.log 2>&1
