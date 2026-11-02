# Módulo 4: Generación de Grafos (NetworkX/Matplotlib)
"""Construcción y exportación del grafo completo de estados de Salto de Ranas."""
from __future__ import annotations

from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D

from core.bfs_solver import ResultadoBusqueda, resolver_bfs
from core.state import ESTADO_INICIAL, ESTADO_META, obtener_sucesores


INICIO = "inicio"
META = "meta"
RUTA = "ruta"             
DEADLOCK = "deadlock"     
CONDENADO = "condenado"   
VIABLE = "viable"         

ESTILO = {  
    INICIO: ("#4C8BF5", "Estado inicial"),
    META: ("#2E9E5B", "Estado meta"),
    RUTA: ("#F5B400", "Ruta óptima"),
    VIABLE: ("#D9DEE5", "Viable (llega a la meta)"),
    CONDENADO: ("#F4B6B6", "Condenado (no llega a la meta)"),
    DEADLOCK: ("#D64545", "Deadlock (sin movimientos)"),
}


def construir_grafo(inicio: str = ESTADO_INICIAL) -> nx.DiGraph:
    """Grafo dirigido con todos los estados alcanzables desde `inicio`.

    Atributos de nodo: `nivel` (distancia mínima desde el inicio).
    Atributos de arista: `movimiento` (el Movimiento que une los dos estados).
    """
    G = nx.DiGraph()
    G.add_node(inicio)
    pendientes = [inicio]
    for estado in pendientes:  
        for sucesor, movimiento in obtener_sucesores(estado):
            if sucesor not in G:
                pendientes.append(sucesor)
            G.add_edge(estado, sucesor, movimiento=movimiento)

    niveles = nx.single_source_shortest_path_length(G, inicio)
    nx.set_node_attributes(G, niveles, "nivel")
    return G


def clasificar_nodos(
    G: nx.DiGraph, resultado: ResultadoBusqueda, inicio: str = ESTADO_INICIAL
) -> dict[str, str]:
    """Asigna a cada estado una categoría (ver constantes de arriba)."""
    en_ruta = set(resultado.ruta)
    categorias: dict[str, str] = {}
    for nodo in G:
        if nodo == inicio:
            categorias[nodo] = INICIO
        elif nodo == ESTADO_META:
            categorias[nodo] = META
        elif nodo in en_ruta:
            categorias[nodo] = RUTA
        elif G.out_degree(nodo) == 0:
            categorias[nodo] = DEADLOCK
        elif not nx.has_path(G, nodo, ESTADO_META):
            categorias[nodo] = CONDENADO
        else:
            categorias[nodo] = VIABLE
    return categorias


def calcular_posiciones(G: nx.DiGraph, resultado: ResultadoBusqueda) -> dict[str, tuple[float, float]]:
    """Layout por niveles: x = nivel, y reparte los nodos; la ruta óptima queda en y = 0."""
    en_ruta = set(resultado.ruta)
    por_nivel: dict[int, list[str]] = {}
    for nodo, nivel in G.nodes(data="nivel"):
        por_nivel.setdefault(nivel, []).append(nodo)

    posiciones: dict[str, tuple[float, float]] = {}
    for nivel, nodos in por_nivel.items():
        nodos.sort(key=lambda n: (n not in en_ruta, n))  
        for i, nodo in enumerate(nodos):
            y = 0 if i == 0 else (i + 1) // 2 * (1 if i % 2 else -1)
            posiciones[nodo] = (float(nivel), float(y))
    return posiciones


def exportar_grafo(
    ruta_archivo: str | Path, resultado: ResultadoBusqueda | None = None
) -> Path:
    """Dibuja el grafo completo y lo guarda como imagen (PNG, SVG, PDF...)."""
    resultado = resultado or resolver_bfs()
    G = construir_grafo()
    categorias = clasificar_nodos(G, resultado)
    pos = calcular_posiciones(G, resultado)
    conteo = Counter(categorias.values())

    aristas_ruta = set(zip(resultado.ruta, resultado.ruta[1:]))
    otras = [e for e in G.edges if e not in aristas_ruta]

    fig, ax = plt.subplots(figsize=(30, 11))
    ax.set_axis_off()
    TAM = 1500

    nx.draw_networkx_edges(G, pos, edgelist=otras, ax=ax, edge_color="#9AA3AF",
                           width=0.9, alpha=0.8, arrows=True, arrowsize=9,
                           node_size=TAM, node_shape="s")
    nx.draw_networkx_edges(G, pos, edgelist=sorted(aristas_ruta), ax=ax, edge_color="#E08A00",
                           width=3.2, arrows=True, arrowsize=16,
                           node_size=TAM, node_shape="s")
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=TAM, node_shape="s",
                           node_color=[ESTILO[categorias[n]][0] for n in G],
                           edgecolors="#374151", linewidths=0.8)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_family="monospace",
                            font_weight="bold")

    for nivel in range(max(n for _, n in G.nodes(data="nivel")) + 1):
        ax.text(nivel, max(y for _, y in pos.values()) + 1.0, f"Nivel {nivel}",
                ha="center", fontsize=10, color="#4B5563")

    leyenda = [
        Line2D([0], [0], marker="s", linestyle="", markersize=11, markerfacecolor=color,
               markeredgecolor="#374151", label=f"{texto}: {conteo.get(cat, 0)}")
        for cat, (color, texto) in ESTILO.items()
    ]
    ax.legend(handles=leyenda, loc="lower center", ncol=3, frameon=False, fontsize=10,
              bbox_to_anchor=(0.5, -0.02))
    ax.set_title(
        f"Grafo de estados de Salto de Ranas: {G.number_of_nodes()} estados, "
        f"{G.number_of_edges()} movimientos, solución óptima de {resultado.longitud} pasos",
        fontsize=18, pad=40)

    destino = Path(ruta_archivo)
    destino.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destino, dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return destino