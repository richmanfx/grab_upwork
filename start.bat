@echo off

set /a count=0
rem Посчитать число параметров
for %%a in (%*) do set /a count+=1

if %count% neq 1 (
	echo Число параметров: %count%
    echo Требуется один параметр.
) else (
    C:\Python27\python.exe grab_upwork.py %~1
)




