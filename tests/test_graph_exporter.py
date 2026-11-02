from collections import Counter

import networkx as nx
import pytest

from analytics.graph_exporter import (
    CONDENADO, DEADLOCK, INICIO, META, RUTA, VIABLE,
    calcular_posiciones, clasificar_nodos, construir_grafo, exportar_grafo,
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


def test_ninguna_arista_salta_niveles(grafo):
    for u, v in grafo.edges:
        assert grafo.nodes[v]["nivel"] - grafo.nodes[u]["nivel"] == 1


def test_conteo_por_categoria(categorias):
    assert Counter(categorias.values()) == {
        INICIO: 1, META: 1, RUTA: 14, VIABLE: 14, CONDENADO: 29, DEADLOCK: 13,
    }


def test_deadlocks_no_tienen_salida_y_no_son_la_meta(grafo, categorias):
    for nodo, cat in categorias.items():
        if cat == DEADLOCK:
            assert grafo.out_degree(nodo) == 0
            assert nodo != ESTADO_META


def test_condenados_no_alcanzan_la_meta_pero_si_tienen_movimientos(grafo, categorias):
    for nodo, cat in categorias.items():
        if cat == CONDENADO:
            assert grafo.out_degree(nodo) > 0
            assert not nx.has_path(grafo, nodo, ESTADO_META)


def test_viables_y_ruta_si_alcanzan_la_meta(grafo, categorias):
    for nodo, cat in categorias.items():
        if cat in (VIABLE, RUTA, INICIO):
            assert nx.has_path(grafo, nodo, ESTADO_META)


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