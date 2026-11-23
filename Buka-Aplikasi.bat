@echo off
title Aplikasi Kasir - Kasir & POS
cd /d "%~dp0"

if exist "AplikasiKasir.exe" (
    start "" "AplikasiKasir.exe"
    exit /b
)

echo Membuka Aplikasi Kasir...
start "" "app\index.html"
exit /b
