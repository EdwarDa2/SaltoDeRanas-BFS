@echo off
cd /d "%~dp0"
title Salto de Ranas - BFS
cls
echo ============================================================
echo      ROMPECABEZAS SALTO DE RANAS - SOLUCIONADOR BFS
echo ============================================================
echo.
echo Iniciando el agente inteligente y preparando visualizador web...
echo.

python main.py --web
if errorlevel 1 (
    echo.
    echo ============================================================
    echo [AVISO] No se pudo iniciar automaticamente.
    echo Verifique que Python este instalado y sus dependencias listas:
    echo     pip install -r requirements.txt
    echo ============================================================
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  [OK] El visualizador interactivo esta abierto en su navegador.
echo       - Podra presionar 'Iniciar Animacion' (Start).
echo       - Podra explorar la pestana 'Arbol de Navegacion'.
echo.
echo  Si tambien desea ver el menu de consola, presione 'M'.
echo  De lo contrario, presione Enter para cerrar esta ventana.
echo ============================================================
set /p "opc=Seleccione una opcion [M / Enter para salir]: "
if /i "%opc%"=="M" (
    cls
    python main.py
)

