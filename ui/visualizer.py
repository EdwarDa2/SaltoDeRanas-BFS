# Módulo 3: Visualización en Consola (Rich)
"""Visualizador en consola para la resolución del rompecabezas Salto de Ranas."""
from __future__ import annotations

import time
from typing import Optional

from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.bfs_solver import ResultadoBusqueda
from core.state import Movimiento, ROJA, VERDE, VACIO

# Colores y etiquetas de visualización
ESTILO_FICHAS = {
    ROJA: {"estilo": "bold white on red", "simbolo": " R "},
    VERDE: {"estilo": "bold white on green", "simbolo": " V "},
    VACIO: {"estilo": "dim white on grey23", "simbolo": " _ "},
}


def crear_tablero_renderable(estado: str) -> Table:
    """Crea una tabla Rich estilizada representando las 7 casillas del tablero."""
    tabla = Table(show_header=True, header_style="bold cyan", expand=False)
    
    # 7 columnas para las posiciones 0 a 6
    for i in range(len(estado)):
        tabla.add_column(f"[{i}]", justify="center", width=7)

    celdas = []
    for char in estado:
        info = ESTILO_FICHAS.get(char, {"estilo": "white", "simbolo": f" {char} "})
        celdas.append(Text(info["simbolo"], style=info["estilo"], justify="center"))

    tabla.add_row(*celdas)
    return tabla


def formatear_movimiento(mov: Movimiento, paso_actual: int, total_pasos: int) -> Text:
    """Genera una descripción textual estilizada de la acción realizada."""
    color_ficha = "red" if mov.ficha == ROJA else "green"
    texto = Text()
    texto.append(f"Paso {paso_actual}/{total_pasos}: ", style="bold yellow")
    texto.append(f"Rana {mov.ficha} ", style=f"bold {color_ficha}")
    texto.append(f"realizó un ", style="white")
    texto.append(f"{mov.tipo.upper()} ", style="bold magenta")
    texto.append(f"desde casilla ", style="white")
    texto.append(f"[{mov.origen}] ", style="bold cyan")
    texto.append(f"hacia casilla ", style="white")
    texto.append(f"[{mov.destino}]", style="bold cyan")
    return texto


def mostrar_paso(
    estado: str,
    mov: Optional[Movimiento] = None,
    paso_actual: int = 0,
    total_pasos: int = 0,
    console: Optional[Console] = None,
) -> None:
    """Muestra un paso individual con su tablero y narración dentro de un Panel."""
    console = console or Console()
    tablero = crear_tablero_renderable(estado)

    if mov is not None:
        descripcion = formatear_movimiento(mov, paso_actual, total_pasos)
    else:
        descripcion = Text("Estado Inicial (Configuración de partida)", style="bold italic cyan")

    contenido = Group(
        Align.center(tablero),
        Text(""),
        Align.center(descripcion),
    )

    titulo = f"[bold green]Salto de Ranas - Paso {paso_actual}/{total_pasos}[/]"
    panel = Panel(contenido, title=titulo, border_style="blue", expand=False)
    console.print(panel)


def mostrar_resumen(resultado: ResultadoBusqueda, console: Optional[Console] = None) -> None:
    """Imprime un panel estilizado con las métricas finales de la búsqueda BFS."""
    console = console or Console()

    tabla_metricas = Table(show_header=False, box=None, padding=(0, 2))
    tabla_metricas.add_column("Métrica", style="bold white")
    tabla_metricas.add_column("Valor", style="bold cyan")

    tabla_metricas.add_row("Estado inicial:", resultado.ruta[0])
    tabla_metricas.add_row("Estado meta:", resultado.ruta[-1])
    tabla_metricas.add_row("Movimientos óptimos:", str(resultado.longitud))
    tabla_metricas.add_row("Nodos explorados:", str(resultado.nodos_explorados))
    tabla_metricas.add_row("Nodos descubiertos:", str(resultado.nodos_descubiertos))
    tabla_metricas.add_row("Tiempo de cálculo BFS:", f"{resultado.tiempo_ms:.4f} ms")

    panel = Panel(
        Align.center(tabla_metricas),
        title="[bold green]Solución Óptima Encontrada[/]",
        border_style="green",
        expand=False,
    )
    console.print(panel)


def animar_solucion(
    resultado: ResultadoBusqueda,
    retraso_segundos: float = 0.5,
    console: Optional[Console] = None,
) -> None:
    """Reproduce automáticamente la secuencia de movimientos de la solución."""
    console = console or Console()
    total_pasos = resultado.longitud

    console.clear()
    console.print("[bold yellow]Iniciando animación de la solución óptima...[/]\n")
    time.sleep(retraso_segundos)

    # Mostrar estado inicial
    console.clear()
    mostrar_paso(resultado.ruta[0], mov=None, paso_actual=0, total_pasos=total_pasos, console=console)
    time.sleep(retraso_segundos)

    for i, mov in enumerate(resultado.movimientos, start=1):
        console.clear()
        estado = resultado.ruta[i]
        mostrar_paso(estado, mov=mov, paso_actual=i, total_pasos=total_pasos, console=console)
        time.sleep(retraso_segundos)

    console.print("\n")
    mostrar_resumen(resultado, console=console)


def recorrer_paso_a_paso(
    resultado: ResultadoBusqueda,
    console: Optional[Console] = None,
) -> None:
    """Permite al usuario avanzar paso a paso presionando [Enter]."""
    console = console or Console()
    total_pasos = resultado.longitud

    console.clear()
    console.print("[bold cyan]Modo Interactivo: Presione [ENTER] para avanzar en cada movimiento.[/]\n")

    mostrar_paso(resultado.ruta[0], mov=None, paso_actual=0, total_pasos=total_pasos, console=console)

    for i, mov in enumerate(resultado.movimientos, start=1):
        input("\nPresione [Enter] para el siguiente paso...")
        console.clear()
        estado = resultado.ruta[i]
        mostrar_paso(estado, mov=mov, paso_actual=i, total_pasos=total_pasos, console=console)

    console.print("\n")
    mostrar_resumen(resultado, console=console)
