@ECHO off

Echo '%date% %time%';'Inizio esecuzione file batch' >> ..\\log\\batch_log.log

py --version >NUL
if errorlevel 0 goto YesPython
Echo '%date% %time%';'Python Error: Python not installed' >> ..\\log\\batch_log.log
goto PostPython

:YesPython
python.exe agent.py
if errorlevel 0 goto PythonSuccess
Echo '%date% %time%';'PythonFile:Error' >> ..\\log\\batch_log.log
goto PostPython
:PythonSuccess
Echo '%date% %time%';'PythonFile:OK' >> ..\\log\\batch_log.log
:PostPython

Echo '%date% %time%';'Fine esecuzione file batch' >> ..\\log\\batch_log.log