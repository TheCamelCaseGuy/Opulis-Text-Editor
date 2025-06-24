@echo off
setlocal

:: Config
set "REPO=TheCamelCaseGuy/Opulis-Text-Editor"
set "INSTALL_DIR=%LOCALAPPDATA%\Opulis"
set "EXECUTABLE=Opulis.exe"
set "DOWNLOAD_URL=https://github.com/%REPO%/releases/latest/download/%EXECUTABLE%"
set "TARGET_PATH=%INSTALL_DIR%\%EXECUTABLE%"
set "SHORTCUT_NAME=Opulis.lnk"

:: Create install directory if needed
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

:: Download the EXE release
echo Downloading latest Opulis.exe from GitHub releases...
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%TARGET_PATH%'"

:: Add to PATH if not already present
for /f "tokens=2* delims=    " %%A in ('reg query HKCU\Environment /v PATH 2^>nul') do (
    set "current_path=%%B"
)

setlocal enabledelayedexpansion
echo !current_path! | find /i "%INSTALL_DIR%" >nul
if errorlevel 1 (
    set "new_path=!current_path!;%INSTALL_DIR%"
    reg add "HKCU\Environment" /v PATH /d "!new_path!" /f >nul
    echo PATH updated successfully.
) else (
    echo PATH already contains Opulis.
)
endlocal

:: Create desktop shortcut
powershell -Command ^
  "$s=(New-Object -COM WScript.Shell).CreateShortcut('%USERPROFILE%\Desktop\%SHORTCUT_NAME%');" ^
  "$s.TargetPath='%TARGET_PATH%';" ^
  "$s.WorkingDirectory='%INSTALL_DIR%';" ^
  "$s.IconLocation='%TARGET_PATH%';" ^
  "$s.Save()"

:: Create Start Menu shortcut
set "STARTMENU_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Opulis.lnk"

powershell -Command ^
  "$s=(New-Object -COM WScript.Shell).CreateShortcut('%STARTMENU_PATH%');" ^
  "$s.TargetPath='%TARGET_PATH%';" ^
  "$s.WorkingDirectory='%INSTALL_DIR%';" ^
  "$s.IconLocation='%TARGET_PATH%';" ^
  "$s.Save()"

echo Opulis added to Start Menu.

echo Opulis installed! Restart CMD or PowerShell to launch via 'Opulis'.
pause
