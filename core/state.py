# Módulo 1: Modelo del Estado y Transiciones

"""Dominio del problema Salto de Ranas.

El estado del tablero es una cadena inmutable de 7 caracteres:
'R' (ficha roja), 'V' (ficha verde) y '_' (casilla vacía).
"""
from __future__ import annotations

from typing import NamedTuple

ROJA = "R"
VERDE = "V"
VACIO = "_"

ESTADO_INICIAL = "RRR_VVV"
ESTADO_META = "VVV_RRR"


class Movimiento(NamedTuple):
    """Describe una acción: qué ficha se movió, desde dónde y hacia dónde."""

    ficha: str
    origen: int
    destino: int

    @property
    def tipo(self) -> str:
        return "saltar" if abs(self.destino - self.origen) == 2 else "avanzar"

    def __str__(self) -> str:
        return f"{self.ficha} {self.tipo} de {self.origen} a {self.destino}"


def validar_estado(estado: str) -> None:
    """Lanza ValueError si la cadena no es un tablero válido."""
    if len(estado) != len(ESTADO_INICIAL):
        raise ValueError(f"El estado debe tener {len(ESTADO_INICIAL)} casillas: {estado!r}")
    if sorted(estado) != sorted(ESTADO_INICIAL):
        raise ValueError(f"El estado debe tener 3 'R', 3 'V' y 1 '_': {estado!r}")


def es_meta(estado: str) -> bool:
    return estado == ESTADO_META


def _mover(estado: str, origen: int, destino: int) -> str:
    """Devuelve un NUEVO estado intercambiando dos casillas."""
    casillas = list(estado)
    casillas[origen], casillas[destino] = casillas[destino], casillas[origen]
    return "".join(casillas)


def obtener_sucesores(estado: str) -> list[tuple[str, Movimiento]]:
    """Genera todos los estados alcanzables con un movimiento válido.

    Se razona desde el hueco: solo las fichas a distancia 1 o 2 del hueco
    pueden moverse, así que basta revisar como máximo 4 candidatas.
    """
    validar_estado(estado)
    hueco = estado.index(VACIO)
    n = len(estado)
    sucesores: list[tuple[str, Movimiento]] = []

    # Rojas: están a la izquierda del hueco y se mueven hacia la derecha.
    if hueco - 1 >= 0 and estado[hueco - 1] == ROJA:  # avanzar
        sucesores.append((_mover(estado, hueco - 1, hueco), Movimiento(ROJA, hueco - 1, hueco)))
    if hueco - 2 >= 0 and estado[hueco - 2] == ROJA and estado[hueco - 1] == VERDE:  # saltar
        sucesores.append((_mover(estado, hueco - 2, hueco), Movimiento(ROJA, hueco - 2, hueco)))

    # Verdes: están a la derecha del hueco y se mueven hacia la izquierda.
    if hueco + 1 < n and estado[hueco + 1] == VERDE:  # avanzar
        sucesores.append((_mover(estado, hueco + 1, hueco), Movimiento(VERDE, hueco + 1, hueco)))
    if hueco + 2 < n and estado[hueco + 2] == VERDE and estado[hueco + 1] == ROJA:  # saltar
        sucesores.append((_mover(estado, hueco + 2, hueco), Movimiento(VERDE, hueco + 2, hueco)))

    return sucesores