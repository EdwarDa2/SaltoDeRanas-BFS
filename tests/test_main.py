"""Pruebas unitarias para main.py."""
from pathlib import Path
import pytest

from main import parse_args, main, RUTA_GRAFO_DEFAULT


def test_parse_args_defaults():
    args = parse_args([])
    assert not args.animar
    assert not args.pasos
    assert not args.web
    assert not args.generar_resultados
    assert not args.grafo
    assert not args.todo
    assert args.velocidad == 0.5
    assert args.output == RUTA_GRAFO_DEFAULT


def test_parse_args_flags():
    args = parse_args(["--animar", "-s", "0.2"])
    assert args.animar
    assert args.velocidad == 0.2

    args = parse_args(["--web"])
    assert args.web

    args = parse_args(["--generar-resultados"])
    assert args.generar_resultados

    args = parse_args(["--grafo", "-o", "custom.png"])
    assert args.grafo
    assert args.output == Path("custom.png")


def test_main_cli_animar(monkeypatch):
    llamado = False

    def fake_animar(retraso=0.5):
        nonlocal llamado
        llamado = True

    monkeypatch.setattr("main.ejecutar_animacion", fake_animar)
    main(["--animar"])
    assert llamado


def test_main_cli_web(monkeypatch):
    llamado = False

    def fake_web(ruta_destino=None, auto_abrir=True):
        nonlocal llamado
        llamado = True
        return Path("fake.html")

    monkeypatch.setattr("main.ejecutar_web", fake_web)
    main(["--web"])
    assert llamado


def test_main_cli_generar_resultados(monkeypatch):
    llamado = False

    def fake_gen(dir_salida=None):
        nonlocal llamado
        llamado = True
        return {}

    monkeypatch.setattr("main.generar_entregables_resultados", fake_gen)
    main(["--generar-resultados"])
    assert llamado


def test_main_cli_grafo(tmp_path, monkeypatch):
    llamado = False

    def fake_grafo(ruta_destino):
        nonlocal llamado
        llamado = True
        return ruta_destino

    monkeypatch.setattr("main.ejecutar_exportacion_grafo", fake_grafo)
    destino = tmp_path / "grafo_test.png"
    main(["--grafo", "-o", str(destino)])
    assert llamado


def test_main_menu_salir(monkeypatch):
    # Simular que el usuario presiona "7" (Salir) en el menú
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: "7")
    main([])  # No levanta excepciones y termina limpio
