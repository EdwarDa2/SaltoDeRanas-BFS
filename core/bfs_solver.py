# Módulo 2: Motor de Búsqueda BFS
"""Motor de Búsqueda en Anchura (BFS) para Salto de Ranas."""
from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass

from core.state import (
    ESTADO_INICIAL,
    ESTADO_META,
    Movimiento,
    obtener_sucesores,
    validar_estado,
)


@dataclass(frozen=True)
class ResultadoBusqueda:
    """Resultado de una búsqueda exitosa."""

    ruta: list[str]                 
    movimientos: list[Movimiento]   
    nodos_explorados: int           
    nodos_descubiertos: int         
    tiempo_ms: float

    @property
    def longitud(self) -> int:
        return len(self.movimientos)


# padres[hijo] = (padre, movimiento)  |  padres[inicio] = None
Padres = dict[str, "tuple[str, Movimiento] | None"]


def reconstruir_ruta(padres: Padres, meta: str) -> tuple[list[str], list[Movimiento]]:
    """Recorre los punteros de padre desde la meta hasta el inicio y los invierte."""
    ruta = [meta]
    movimientos: list[Movimiento] = []
    actual = meta
    while padres[actual] is not None:
        padre, movimiento = padres[actual]
        ruta.append(padre)
        movimientos.append(movimiento)
        actual = padre
    ruta.reverse()
    movimientos.reverse()
    return ruta, movimientos


def resolver_bfs(
    inicio: str = ESTADO_INICIAL, meta: str = ESTADO_META
) -> ResultadoBusqueda | None:
    """Busca la ruta más corta de `inicio` a `meta`.

    Devuelve None si la meta no es alcanzable desde `inicio`.
    """
    validar_estado(inicio)
    validar_estado(meta)

    t0 = time.perf_counter()
    frontera: deque[str] = deque([inicio])     
    padres: Padres = {inicio: None}             
    explorados = 0

    while frontera:
        actual = frontera.popleft()
        explorados += 1

        if actual == meta:
            ruta, movimientos = reconstruir_ruta(padres, meta)
            return ResultadoBusqueda(
                ruta=ruta,
                movimientos=movimientos,
                nodos_explorados=explorados,
                nodos_descubiertos=len(padres),
                tiempo_ms=(time.perf_counter() - t0) * 1000,
            )

        for sucesor, movimiento in obtener_sucesores(actual):
            if sucesor not in padres:           
                padres[sucesor] = (actual, movimiento)
                frontera.append(sucesor)

    return None  