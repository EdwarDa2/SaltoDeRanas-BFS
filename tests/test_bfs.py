# Pruebas unitarias
from functools import lru_cache

import pytest

from core.bfs_solver import ResultadoBusqueda, reconstruir_ruta, resolver_bfs
from core.state import ESTADO_INICIAL, ESTADO_META, obtener_sucesores, es_meta


@pytest.fixture(scope="module")
def solucion() -> ResultadoBusqueda:
    resultado = resolver_bfs()
    assert resultado is not None
    return resultado


def test_la_solucion_tiene_15_movimientos(solucion):
    assert solucion.longitud == 15
    assert len(solucion.ruta) == 16


def test_la_ruta_empieza_en_inicio_y_termina_en_meta(solucion):
    assert solucion.ruta[0] == ESTADO_INICIAL
    assert solucion.ruta[-1] == ESTADO_META


def test_cada_paso_es_un_sucesor_valido_con_su_movimiento(solucion):
    for i, mov in enumerate(solucion.movimientos):
        permitidos = dict(obtener_sucesores(solucion.ruta[i]))
        assert solucion.ruta[i + 1] in permitidos
        assert permitidos[solucion.ruta[i + 1]] == mov


def test_la_ruta_no_repite_estados(solucion):
    assert len(set(solucion.ruta)) == len(solucion.ruta)


def test_bfs_coincide_con_la_distancia_minima_calculada_por_recursion():
    @lru_cache(maxsize=None)
    def minimo(estado):
        if es_meta(estado):
            return 0
        opciones = [minimo(s) for s, _ in obtener_sucesores(estado)]
        return 1 + min(opciones) if opciones else float("inf")

    assert minimo(ESTADO_INICIAL) == resolver_bfs().longitud == 15


def test_bfs_explora_los_72_estados(solucion):
    assert solucion.nodos_explorados == 72
    assert solucion.nodos_descubiertos == 72


def test_tiempo_es_no_negativo(solucion):
    assert solucion.tiempo_ms >= 0


def test_inicio_igual_a_meta_da_ruta_vacia():
    r = resolver_bfs(ESTADO_META, ESTADO_META)
    assert r.ruta == [ESTADO_META]
    assert r.movimientos == []
    assert r.longitud == 0
    assert r.nodos_explorados == 1


def test_meta_inalcanzable_devuelve_None_y_no_una_ruta_falsa():
    assert resolver_bfs("RRRVVV_", ESTADO_META) is None
    assert resolver_bfs(ESTADO_META, ESTADO_INICIAL) is None


def test_funciona_desde_un_estado_intermedio():
    r = resolver_bfs("RR_RVVV", ESTADO_META)
    assert r is not None
    assert r.longitud == 14
    assert r.ruta[0] == "RR_RVVV"


@pytest.mark.parametrize("malo", ["RRR_VV", "xxxxxxx"])
def test_estados_invalidos_lanzan_error(malo):
    with pytest.raises(ValueError):
        resolver_bfs(malo, ESTADO_META)
    with pytest.raises(ValueError):
        resolver_bfs(ESTADO_INICIAL, malo)


def test_reconstruir_ruta_con_padres_manuales():
    from core.state import Movimiento
    m = Movimiento("R", 2, 3)
    padres = {"A": None, "B": ("A", m), "C": ("B", m)}
    ruta, movs = reconstruir_ruta(padres, "C")
    assert ruta == ["A", "B", "C"]
    assert movs == [m, m]