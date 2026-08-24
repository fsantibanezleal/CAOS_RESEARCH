@echo off
rem Self-healing launcher: exits if any shard is already running.
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "python.exe" >NUL
if %ERRORLEVEL%==0 exit /b 0
cd /d E:\_Temp\caos-research-tau\problems\computation-complexity\tau-conjecture\experiments\EXP-013-additive-residual
start "tau_add_00" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 0 --nshards 20 >> shard_00.log 2>&1"
start "tau_add_01" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 1 --nshards 20 >> shard_01.log 2>&1"
start "tau_add_02" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 2 --nshards 20 >> shard_02.log 2>&1"
start "tau_add_03" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 3 --nshards 20 >> shard_03.log 2>&1"
start "tau_add_04" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 4 --nshards 20 >> shard_04.log 2>&1"
start "tau_add_05" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 5 --nshards 20 >> shard_05.log 2>&1"
start "tau_add_06" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 6 --nshards 20 >> shard_06.log 2>&1"
start "tau_add_07" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 7 --nshards 20 >> shard_07.log 2>&1"
start "tau_add_08" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 8 --nshards 20 >> shard_08.log 2>&1"
start "tau_add_09" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 9 --nshards 20 >> shard_09.log 2>&1"
start "tau_add_10" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 10 --nshards 20 >> shard_10.log 2>&1"
start "tau_add_11" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 11 --nshards 20 >> shard_11.log 2>&1"
start "tau_add_12" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 12 --nshards 20 >> shard_12.log 2>&1"
start "tau_add_13" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 13 --nshards 20 >> shard_13.log 2>&1"
start "tau_add_14" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 14 --nshards 20 >> shard_14.log 2>&1"
start "tau_add_15" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 15 --nshards 20 >> shard_15.log 2>&1"
start "tau_add_16" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 16 --nshards 20 >> shard_16.log 2>&1"
start "tau_add_17" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 17 --nshards 20 >> shard_17.log 2>&1"
start "tau_add_18" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 18 --nshards 20 >> shard_18.log 2>&1"
start "tau_add_19" /min cmd /c ""D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 19 --nshards 20 >> shard_19.log 2>&1"
