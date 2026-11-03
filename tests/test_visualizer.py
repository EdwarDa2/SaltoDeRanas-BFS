"""Pruebas unitarias para el módulo ui/visualizer.py."""
import io
import pytest
from rich.console import Console

from core.bfs_solver import resolver_bfs
from core.state import Movimiento, ESTADO_INICIAL, ESTADO_META
from ui.visualizer import (
    crear_tablero_renderable,
    formatear_movimiento,
    mostrar_paso,
    mostrar_resumen,
    animar_solucion,
    recorrer_paso_a_paso,
)


def test_crear_tablero_renderable():
    tabla = crear_tablero_renderable(ESTADO_INICIAL)
    assert len(tabla.columns) == 7
    assert tabla.row_count == 1


def test_formatear_movimiento():
    mov_avanzar = Movimiento(ficha="R", origen=2, destino=3)
    texto = formatear_movimiento(mov_avanzar, paso_actual=1, total_pasos=15)
    plain = texto.plain
    assert "Paso 1/15" in plain
    assert "Rana R" in plain
    assert "AVANZAR" in plain
    assert "[2]" in plain
    assert "[3]" in plain

    mov_saltar = Movimiento(ficha="V", origen=4, destino=2)
    texto_salto = formatear_movimiento(mov_saltar, paso_actual=2, total_pasos=15)
    assert "SALTAR" in texto_salto.plain


def test_mostrar_paso_sin_movimiento():
    buffer = io.StringIO()
    consola = Console(file=buffer, force_terminal=False, width=80)
    mostrar_paso(ESTADO_INICIAL, mov=None, paso_actual=0, total_pasos=15, console=consola)
    salida = buffer.getvalue()
    assert "Paso 0/15" in salida
    assert "Estado Inicial" in salida


def test_mostrar_paso_con_movimiento():
    buffer = io.StringIO()
    consola = Console(file=buffer, force_terminal=False, width=80)
    mov = Movimiento(ficha="R", origen=2, destino=3)
    mostrar_paso("RR_RVVV", mov=mov, paso_actual=1, total_pasos=15, console=consola)
    salida = buffer.getvalue()
    assert "Paso 1/15" in salida
    assert "Rana R" in salida


def test_mostrar_resumen():
    buffer = io.StringIO()
    consola = Console(file=buffer, force_terminal=False, width=80)
    resultado = resolver_bfs()
    mostrar_resumen(resultado, console=consola)
    salida = buffer.getvalue()
    assert "Solución Óptima Encontrada" in salida
    assert "15" in salida
    assert "72" in salida


def test_animar_solucion_ejecucion():
    buffer = io.StringIO()
    consola = Console(file=buffer, force_terminal=False, width=80)
    resultado = resolver_bfs()
    # Con retraso 0 para pruebas rápidas
    animar_solucion(resultado, retraso_segundos=0.0, console=consola)
    salida = buffer.getvalue()
    assert "Solución Óptima Encontrada" in salida


def test_recorrer_paso_a_paso_simulado(monkeypatch):
    buffer = io.StringIO()
    consola = Console(file=buffer, force_terminal=False, width=80)
    resultado = resolver_bfs()
    # Simular que el usuario presiona Enter 15 veces
    monkeypatch.setattr("builtins.input", lambda _: "")
    recorrer_paso_a_paso(resultado, console=consola)
    salida = buffer.getvalue()
    assert "Modo Interactivo" in salida
    assert "Solución Óptima Encontrada" in salida

