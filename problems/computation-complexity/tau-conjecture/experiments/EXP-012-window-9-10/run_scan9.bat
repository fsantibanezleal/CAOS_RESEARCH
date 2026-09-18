@echo off
cd /d "%~dp0"
"%~dp0..\..\..\..\..\.venv\Scripts\python.exe" scan9.py --nproc 20 >> scan9.log 2>&1
