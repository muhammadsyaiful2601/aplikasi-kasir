@echo off
title Aplikasi Kasir - PREVIEW (dev server)
cd /d "%~dp0.."

echo.
echo  ============================================================
echo   PREVIEW MODE - tidak perlu build
echo  ------------------------------------------------------------
echo   Alamat : http://localhost:5180
echo   Sumber : folder app\
echo   Cara   : edit file di app\ lalu REFRESH browser (Ctrl+F5)
echo  ------------------------------------------------------------
echo   Buka Chrome/Edge, lalu klik panel "Database" di sisi kiri
echo   untuk memilih lokasi file database.
echo  ============================================================
echo.

start "" "http://localhost:5180"
node "%~dp0server.js"
pause
