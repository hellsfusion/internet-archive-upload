@echo off
python main.py

if %errorlevel% neq 0 (
    echo.
    echo ADVERTENCIA: El script terminó con errores
    echo Revisa el archivo ia_upload_detailed.log para más detalles
) else (
    echo.
    echo Script ejecutado exitosamente
)

echo.
pause