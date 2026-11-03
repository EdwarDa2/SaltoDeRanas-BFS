from collections import Counter
import json
from pathlib import Path

import networkx as nx
import pytest

from analytics.graph_exporter import (
    CONDENADO, DEADLOCK, INICIO, META, RUTA, VIABLE,
    calcular_posiciones, clasificar_nodos, construir_grafo, exportar_grafo,
    exportar_metricas_json,
)
from core.bfs_solver import resolver_bfs
from core.state import ESTADO_INICIAL, ESTADO_META, obtener_sucesores


@pytest.fixture(scope="module")
def grafo():
    return construir_grafo()


@pytest.fixture(scope="module")
def resultado():
    return resolver_bfs()


@pytest.fixture(scope="module")
def categorias(grafo, resultado):
    return clasificar_nodos(grafo, resultado)


def test_el_grafo_tiene_72_nodos_y_82_aristas(grafo):
    assert grafo.number_of_nodes() == 72
    assert grafo.number_of_edges() == 82


def test_el_grafo_es_aciclico(grafo):
    assert nx.is_directed_acyclic_graph(grafo)


def test_las_aristas_coinciden_con_los_sucesores_del_dominio(grafo):
    for origen in grafo:
        esperados = dict(obtener_sucesores(origen))
        reales = {v: grafo.edges[origen, v]["movimiento"] for v in grafo.successors(origen)}
        assert reales == esperados


def test_niveles_van_de_0_a_15(grafo):
    assert grafo.nodes[ESTADO_INICIAL]["nivel"] == 0
    assert grafo.nodes[ESTADO_META]["nivel"] == 15
    assert set(nx.get_node_attributes(grafo, "nivel").values()) == set(range(16))


def test_clasificacion_de_nodos_es_exhaustiva_y_disjunta(grafo, categorias):
    assert set(categorias.keys()) == set(grafo.nodes)
    conteo = Counter(categorias.values())
    assert conteo[INICIO] == 1
    assert conteo[META] == 1
    assert conteo[RUTA] == 14  
    assert conteo[DEADLOCK] == 13
    assert conteo[INICIO] + conteo[META] + conteo[RUTA] + conteo[DEADLOCK] + conteo[CONDENADO] + conteo[VIABLE] == 72


def test_deadlocks_coinciden_con_los_grados_de_salida_cero(grafo, categorias):
    deadlocks_reales = {n for n, grado in grafo.out_degree() if grado == 0 and n != ESTADO_META}
    deadlocks_clasificados = {n for n, cat in categorias.items() if cat == DEADLOCK}
    assert deadlocks_clasificados == deadlocks_reales
    assert ESTADO_META not in deadlocks_clasificados  


def test_la_ruta_optima_no_pasa_por_estados_perdidos(resultado, categorias):
    for estado in resultado.ruta:
        assert categorias[estado] in (INICIO, RUTA, META)


def test_posiciones_unicas_y_ruta_en_el_eje_central(grafo, resultado):
    pos = calcular_posiciones(grafo, resultado)
    assert len(pos) == 72
    assert len(set(pos.values())) == 72  
    for estado in resultado.ruta:
        assert pos[estado][1] == 0
    for nodo, (x, _) in pos.items():
        assert x == grafo.nodes[nodo]["nivel"]


def test_exportar_crea_un_png_valido(tmp_path):
    destino = exportar_grafo(tmp_path / "salida" / "grafo.png")  
    assert destino.exists()
    contenido = destino.read_bytes()
    assert contenido[:8] == b"\x89PNG\r\n\x1a\n"
    assert len(contenido) > 10_000


def test_exportar_acepta_otros_formatos(tmp_path):
    destino = exportar_grafo(tmp_path / "grafo.svg")
    assert destino.read_text(encoding="utf-8").lstrip().startswith(("<?xml", "<svg"))


def test_exportar_metricas_json(tmp_path):
    destino = tmp_path / "metricas.json"
    res = exportar_metricas_json(destino)
    assert res.exists()
    data = json.loads(res.read_text(encoding="utf-8"))
    assert data["metricas_clave"]["longitud_solucion_optima"] == 15
    assert data["metricas_clave"]["estados_alcanzables"] == 72
    assert data["metricas_clave"]["estados_deadlock"] == 13
