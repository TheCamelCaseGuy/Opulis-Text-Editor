@echo off
setlocal

:: Config
set "INSTALL_DIR=%LOCALAPPDATA%\Opulis"
set "EXECUTABLE=Opulis.exe"
set "TARGET_PATH=%INSTALL_DIR%\%EXECUTABLE%"
set "DESKTOP_SHORTCUT=%USERPROFILE%\Desktop\Opulis.lnk"
set "STARTMENU_SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Opulis.lnk"

echo Uninstalling Opulis...

:: Delete desktop shortcut
if exist "%DESKTOP_SHORTCUT%" (
    echo Removing desktop shortcut...
    del "%DESKTOP_SHORTCUT%"
)

:: Delete Start Menu shortcut
if exist "%STARTMENU_SHORTCUT%" (
    echo Removing Start Menu shortcut...
    del "%STARTMENU_SHORTCUT%"
)

:: Remove from PATH if present
for /f "tokens=2* delims=    " %%A in ('reg query HKCU\Environment /v PATH 2^>nul') do (
    set "current_path=%%B"
)

setlocal enabledelayedexpansion
set "clean_path=!current_path:%INSTALL_DIR%=!"
reg add "HKCU\Environment" /v PATH /d "!clean_path!" /f >nul
endlocal

:: Delete install directory
if exist "%INSTALL_DIR%" (
    echo Deleting Opulis install folder...
    rmdir /s /q "%INSTALL_DIR%"
)

echo ✅ Opulis has been uninstalled. Restart your terminal to refresh PATH.
pause
