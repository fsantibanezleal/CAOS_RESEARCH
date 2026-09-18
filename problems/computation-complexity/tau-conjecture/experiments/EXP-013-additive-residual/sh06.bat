@echo off
cd /d "%~dp0"
"%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 6 --nshards 20 >> shard_06.log 2>&1
