@echo off

REM Written 2016 by Jens Diemer
REM Open Source licenced under GPL v3+
REM more info:
REM http://forums.autodesk.com/t5/3ds-max-3ds-max-design-general/max-2017-mr-drb-satellite-doesn-t-start/m-p/6281098

title %~0
cd /d c:\

whoami /groups | find "S-1-16-12288" > nul
if errorlevel 1 (
    echo.
    echo WARNING:
    echo You should start this batch with admin rights!!!
    echo.
)

set python=%ProgramW6432%\Autodesk\3ds Max 2017\3dsmaxpy.exe
set py_file=%~dpn0.py

call:test_exist "%python%" "Python not found here:"
echo on
"%python%" --version
@echo off

call:test_exist "%py_file%" "Patch script not found here:"

title %py_file%
echo on
"%python%" "%py_file%"
@echo off

call:verbose_do net start mi-raysat_3dsmax2017_64
call:verbose_do sc config mi-raysat_3dsmax2017_64 start= auto

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


:verbose_do
	echo.
	echo %*
	%*
	echo.
goto:eof