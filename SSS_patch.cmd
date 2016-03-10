@echo off

REM Written 2016 by Jens Diemer
REM Open Source licenced under GPL v3+
REM more info:
REM http://forums.autodesk.com/t5/3ds-max-3ds-max-design-general/max-2016-backburner-renders-slower-update/m-p/6206899#M111981

title %~0
cd /d c:\

whoami /groups | find "S-1-16-12288" > nul
if errorlevel 1 (
    echo.
    echo WARNING:
    echo You should start this batch with admin rights!!!
    echo.
)

set python=%ProgramW6432%\Autodesk\3ds Max 2016\python\python.exe
set py_file=%~dp0SSS_patch.py

call:test_exist "%python%" "python.exe not found here:"
echo on
"%python%" --version
@echo off

call:test_exist "%py_file%" "Patch script not found here:"

title %py_file%
echo on
"%python%" "%py_file%"
@echo off
pause
exit

:test_exist
    if NOT exist "%~1" (
        echo.
        echo ERROR: %~2
        echo.
        echo "%~1"
        echo.
        pause
        exit 1
    )
goto:eof