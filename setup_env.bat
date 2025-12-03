@echo off
REM Script to set up virtual environment and install requirements
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing requirements (excluding Polygon3 which requires Visual C++ Build Tools)...
pip install numpy pillow opencv-python
pip install pycocotools
pip install -r requirements.txt --no-deps Polygon3 2>nul || echo Polygon3 skipped (requires Visual C++ Build Tools)

echo.
echo ========================================
echo Virtual environment setup complete!
echo ========================================
echo.
echo To activate the environment, run:
echo   venv\Scripts\activate.bat
echo.
echo Note: Polygon3 was skipped as it requires Microsoft Visual C++ Build Tools.
echo If you need it, install from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
pause

