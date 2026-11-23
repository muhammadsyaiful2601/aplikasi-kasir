@echo off
title Firdaus Servis - Kasir & POS
cd /d "%~dp0"

if exist "FirdausServis.exe" (
    start "" "FirdausServis.exe"
    exit /b
)

echo Membuka Firdaus Servis...
start "" "app\index.html"
exit /b
