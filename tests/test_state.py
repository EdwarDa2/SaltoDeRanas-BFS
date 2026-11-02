from collections import deque

import pytest

from core.state import (
    ESTADO_INICIAL, ESTADO_META, Movimiento,
    es_meta, obtener_sucesores, validar_estado,
)


def sucesores(estado):
    return dict(obtener_sucesores(estado))  


@pytest.mark.parametrize("malo", ["RRR_VV", "RRRRVVV", "RRR__VV", "rrr_vvv", ""])
def test_estado_invalido_lanza_error(malo):
    with pytest.raises(ValueError):
        validar_estado(malo)


def test_inicial_y_meta_son_validos():
    validar_estado(ESTADO_INICIAL)
    validar_estado(ESTADO_META)


def test_obtener_sucesores_rechaza_estado_invalido():
    with pytest.raises(ValueError):
        obtener_sucesores("XXXXXXX")


def test_es_meta():
    assert es_meta("VVV_RRR")
    assert not es_meta(ESTADO_INICIAL)


def test_desde_inicio_solo_hay_dos_avances():
    s = sucesores(ESTADO_INICIAL)
    assert set(s) == {"RR_RVVV", "RRRV_VV"}
    assert s["RR_RVVV"] == Movimiento("R", 2, 3)
    assert s["RRRV_VV"] == Movimiento("V", 4, 3)


def test_roja_salta_sobre_verde():
    s = sucesores("RRV_VVR")
    assert set(s) == {"R_VRVVR", "RRVV_VR"}
    assert s["R_VRVVR"] == Movimiento("R", 1, 3)
    assert s["RRVV_VR"] == Movimiento("V", 4, 3)


def test_verde_salta_sobre_roja():
    s = sucesores("RVV_RVR")
    assert s == {"RVVVR_R": Movimiento("V", 5, 3)}


def test_no_salta_sobre_mismo_color():
    assert all(m.tipo == "avanzar" for m in sucesores(ESTADO_INICIAL).values())


def test_bordes_no_provocan_error_de_indice():
    assert obtener_sucesores("_RRRVVV") == []   
    assert obtener_sucesores("RRRVVV_") == []   


def test_movimiento_describe_la_accion():
    assert Movimiento("R", 1, 3).tipo == "saltar"
    assert Movimiento("V", 4, 3).tipo == "avanzar"
    assert str(Movimiento("R", 2, 3)) == "R avanzar de 2 a 3"


def explorar_todo():
    vistos, cola, transiciones = {ESTADO_INICIAL}, deque([ESTADO_INICIAL]), []
    while cola:
        actual = cola.popleft()
        for nuevo, mov in obtener_sucesores(actual):
            transiciones.append((actual, nuevo, mov))
            if nuevo not in vistos:
                vistos.add(nuevo)
                cola.append(nuevo)
    return vistos, transiciones


def test_hay_72_estados_alcanzables_y_la_meta_es_uno_de_ellos():
    vistos, _ = explorar_todo()
    assert len(vistos) == 72
    assert ESTADO_META in vistos


def test_hay_13_deadlocks():
    vistos, _ = explorar_todo()
    sin_salida = [e for e in vistos if not obtener_sucesores(e) and not es_meta(e)]
    assert len(sin_salida) == 13


def test_las_fichas_nunca_retroceden():
    _, transiciones = explorar_todo()
    for _, _, mov in transiciones:
        if mov.ficha == "R":
            assert mov.destino > mov.origen
        else:
            assert mov.destino < mov.origen


def test_cada_sucesor_es_valido_y_conserva_las_fichas():
    _, transiciones = explorar_todo()
    for origen, nuevo, _ in transiciones:
        validar_estado(nuevo)
        assert sorted(nuevo) == sorted(origen)
        assert nuevo != origen