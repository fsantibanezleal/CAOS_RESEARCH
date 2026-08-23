@echo off
cd /d E:\_Temp\caos-research-tau\problems\computation-complexity\tau-conjecture\experiments\EXP-013-additive-residual
"D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe" scan9add_fast.py --shard 2 --nshards 20 >> shard_02.log 2>&1
