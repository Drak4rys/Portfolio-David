@echo off
cd /d "%~dp0"

echo Generation de gallery.json...
py generate_gallery_json.py

echo.
echo Lancement du serveur local...
start http://localhost:8000
py -m http.server 8000

pause