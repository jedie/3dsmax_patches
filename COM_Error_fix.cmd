@echo off

REM Written 2016 by Jens Diemer
REM Open Source licenced under GPL v3+
REM more info:
REM http://forums.autodesk.com/t5/3ds-max-3ds-max-design-general/2016-sp2-bug-com-error/m-p/5957698#M109841

title %~0
cd /d c:\

whoami /groups | find "S-1-16-12288" > nul
if errorlevel 1 (
    echo.
    echo WARNING:
    echo You should start this batch with admin rights!!!
    echo.
)

echo on
cd /d "%ProgramFiles%\Autodesk\3ds Max 2016"
regsvr32 /u MAXComponents.dll
regsvr32 MAXComponents.dll

@echo.
@pause