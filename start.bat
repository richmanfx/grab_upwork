@echo off

set /a count=0
rem ������� �᫮ ��ࠬ��஢
for %%a in (%*) do set /a count+=1

if %count% neq 1 (
	echo ��᫮ ��ࠬ��஢: %count%
    echo �ॡ���� ���� ��ࠬ���.
) else (
    C:\Python27\python.exe grab_upwork.py %~1
)




