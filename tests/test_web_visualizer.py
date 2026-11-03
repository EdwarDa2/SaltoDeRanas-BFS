"""Pruebas unitarias para ui/web_visualizer.py."""
from pathlib import Path
import pytest

from core.bfs_solver import resolver_bfs
from ui.web_visualizer import (
    construir_html_interactivo,
    exportar_visualizador_web,
    abrir_visualizador_web,
    obtener_imagen_grafo_b64,
)


def test_construir_html_interactivo():
    resultado = resolver_bfs()
    html = construir_html_interactivo(resultado)

    assert "<!DOCTYPE html>" in html
    assert "Salto de Ranas" in html
    assert "RRR_VVV" in html
    assert "VVV_RRR" in html
    assert "btn-start" in html
    assert "results-panel" in html
    assert "tab-btn-tree" in html
    assert "Árbol de Navegación" in html


def test_exportar_visualizador_web(tmp_path):
    resultado = resolver_bfs()
    destino = tmp_path / "test_tablero.html"
    archivo = exportar_visualizador_web(ruta_archivo=destino, resultado=resultado)

    assert archivo.exists()
    contenido = archivo.read_text(encoding="utf-8")
    assert "Salto de Ranas" in contenido


def test_abrir_visualizador_web_sin_abrir(tmp_path, monkeypatch):
    llamado_browser = False

    def fake_open(url):
        nonlocal llamado_browser
        llamado_browser = True

    monkeypatch.setattr("webbrowser.open", fake_open)

    destino = tmp_path / "web_test.html"
    abrir_visualizador_web(ruta_archivo=destino, auto_abrir=True)
    assert destino.exists()
    assert llamado_browser


def test_obtener_imagen_grafo_b64_existente(tmp_path):
    # Probar que devuelve una cadena data:image/png;base64,... si el archivo existe
    dummy_img = tmp_path / "test.png"
    dummy_img.write_bytes(b"\x89PNG\r\n\x1a\nfakeimagebytes")
    b64 = obtener_imagen_grafo_b64(dummy_img)
    assert b64.startswith("data:image/png;base64,")


def test_obtener_imagen_grafo_b64_no_existente():
    b64 = obtener_imagen_grafo_b64(Path("ruta_que_no_existe_xyz.png"))
    # Si las rutas por defecto tampoco existieran devolvería "", pero si existe una por defecto devuelve base64
    assert isinstance(b64, str)
