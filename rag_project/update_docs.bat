@echo off
echo ========================================
echo Documentation Generator
echo ========================================
echo.

echo Generating documentation...
python scripts\generate_docs.py

echo.
echo ========================================
echo Documentation updated successfully!
echo ========================================
echo.
echo Check docs/ folder for updated files:
echo - MODULE_INDEX.md
echo - FUNCTION_REFERENCE.md
echo - CLASS_REFERENCE.md
echo.
pause
