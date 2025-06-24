@echo off
echo Repairing Opulis installation...

:: Step 1: Uninstall existing version
echo Uninstalling current installation...
powershell -Command "iwr -useb https://raw.githubusercontent.com/TheCamelCaseGuy/Opulis-Text-Editor/main/installer/uninstaller.bat -OutFile $env:TEMP\opulis_uninstaller.bat"
call %TEMP%\opulis_uninstaller.bat

:: Step 2: Install latest version
echo Reinstalling Opulis...
powershell -Command "iwr -useb https://raw.githubusercontent.com/TheCamelCaseGuy/Opulis-Text-Editor/main/installer/installer.bat -OutFile $env:TEMP\opulis_installer.bat"
call %TEMP%\opulis_installer.bat

:: Step 3: Wait briefly and relaunch
timeout /t 2 >nul
echo Launching Opulis...
start "" "%ProgramFiles%\Opulis\Opulis.exe"

echo Repair complete.
exit
