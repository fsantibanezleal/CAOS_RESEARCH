@echo off
cd /d "%~dp0"
start "tau_add_0" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 0 --nshards 20 >> shard_00.log 2>&1
start "tau_add_1" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 1 --nshards 20 >> shard_01.log 2>&1
start "tau_add_2" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 2 --nshards 20 >> shard_02.log 2>&1
start "tau_add_3" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 3 --nshards 20 >> shard_03.log 2>&1
start "tau_add_4" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 4 --nshards 20 >> shard_04.log 2>&1
start "tau_add_5" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 5 --nshards 20 >> shard_05.log 2>&1
start "tau_add_6" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 6 --nshards 20 >> shard_06.log 2>&1
start "tau_add_7" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 7 --nshards 20 >> shard_07.log 2>&1
start "tau_add_8" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 8 --nshards 20 >> shard_08.log 2>&1
start "tau_add_9" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 9 --nshards 20 >> shard_09.log 2>&1
start "tau_add_10" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 10 --nshards 20 >> shard_10.log 2>&1
start "tau_add_11" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 11 --nshards 20 >> shard_11.log 2>&1
start "tau_add_12" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 12 --nshards 20 >> shard_12.log 2>&1
start "tau_add_13" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 13 --nshards 20 >> shard_13.log 2>&1
start "tau_add_14" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 14 --nshards 20 >> shard_14.log 2>&1
start "tau_add_15" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 15 --nshards 20 >> shard_15.log 2>&1
start "tau_add_16" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 16 --nshards 20 >> shard_16.log 2>&1
start "tau_add_17" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 17 --nshards 20 >> shard_17.log 2>&1
start "tau_add_18" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 18 --nshards 20 >> shard_18.log 2>&1
start "tau_add_19" /min "%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9add_fast.py --shard 19 --nshards 20 >> shard_19.log 2>&1
