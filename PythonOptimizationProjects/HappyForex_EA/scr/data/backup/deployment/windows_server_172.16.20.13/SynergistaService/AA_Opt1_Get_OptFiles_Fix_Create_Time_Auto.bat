Start /min cmd.exe /c EURUSD_1y.bat
Goto :1
:1

Start /min cmd.exe /c EURUSD_3y.bat
Goto :2
:2

Start /min cmd.exe /c EURUSD_5y.bat
Goto :3
:3

Start /min cmd.exe /c GBPUSD_1y.bat
Goto :4
:4

Start /min cmd.exe /c GBPUSD_3y.bat
Goto :5
:5

Start /min cmd.exe /c GBPUSD_5y.bat
Goto :6
:6

Start /min cmd.exe /c USDJPY_1y.bat
Goto :7
:7

Start /min cmd.exe /c USDJPY_3y.bat
Goto :8
:8

Start /min cmd.exe /c USDJPY_5y.bat
Goto :9
:9

cd D:/SynergistaService/Fix_CREATE_TIME_Auto/
Start /min cmd.exe /c fix_CREATE_TIME.exe 4
Goto :10
:10
exit
