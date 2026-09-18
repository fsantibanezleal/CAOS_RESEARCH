@echo off
cd /d "%~dp0"
"%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 4 --nshards 20 >> shard_04.log 2>&1
