@echo off
echo Instalando dependencias saltando credenciales corporativas...
echo.

REM Usar PyPI oficial directamente
pip install --index-url https://pypi.org/simple/ --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org matplotlib>=3.5.0

pip install --index-url https://pypi.org/simple/ --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org networkx>=2.8.0

pip install --index-url https://pypi.org/simple/ --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org numpy>=1.21.0

echo.
echo Instalacion completada!
pause