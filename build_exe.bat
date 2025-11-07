@echo off
echo Instalando PyInstaller desde PyPI publico...
pip install --index-url https://pypi.org/simple/ pyinstaller

echo Creando ejecutable...
pyinstaller --onefile --windowed --name "Convertidor_AFND_AFD" main.py

echo Ejecutable creado en dist/Convertidor_AFND_AFD.exe
pause