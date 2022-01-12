@ECHO off

Echo '%date% %time%';'Inizio esecuzione file batch' >> ..\\log\\batch_log.log

USBDview.exe /stab usb_devices
if errorlevel 0 goto USBSuccess
Echo '%date% %time%';'USBDeviceList:Error' >> ..\\log\\batch_log.log
goto PostUSB
:USBSuccess
Echo '%date% %time%';'USBDeviceList:OK' >> ..\\log\\batch_log.log
:PostUSB

PowerShell.exe -ExecutionPolicy Bypass -Command "& '%~dpn0.ps1'" > updatepending.txt
if errorlevel 0 goto PowershellSuccess
Echo '%date% %time%';'UpdatePendingList:Powershell Error' >> ..\\log\\batch_log.log
goto PostPowershell
:PowershellSuccess
Echo '%date% %time%';'UpdatePendingList:OK' >> ..\\log\\batch_log.log
:PostPowershell

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

del "updatepending.txt"
del "usb_devices"
del "USBDview.cfg"
Echo '%date% %time%';'CancellazioneFileInutili:OK' >> ..\\log\\batch_log.log

Echo '%date% %time%';'Fine esecuzione file batch' >> ..\\log\\batch_log.log