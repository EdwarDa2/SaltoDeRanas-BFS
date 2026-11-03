# Punto de entrada y orquestación del CLI
"""Sistema de Resolución del Rompecabezas Salto de Ranas mediante BFS."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from analytics.graph_exporter import exportar_grafo, exportar_metricas_json
from core.bfs_solver import resolver_bfs
from ui.visualizer import animar_solucion, recorrer_paso_a_paso, mostrar_resumen
from ui.web_visualizer import abrir_visualizador_web, exportar_visualizador_web

console = Console()

DIR_RESULTADOS = Path("resultados")
RUTA_GRAFO_DEFAULT = DIR_RESULTADOS / "arbol_navegacion_bfs.png"
RUTA_HTML_DEFAULT = DIR_RESULTADOS / "visualizador.html"
RUTA_METRICAS_DEFAULT = DIR_RESULTADOS / "metricas.json"


def mostrar_banner() -> None:
    """Muestra el encabezado del sistema en consola."""
    banner_texto = (
        "[bold cyan]Rompecabezas Salto de Ranas (Frogs Jumping Puzzle)[/]\n"
        "[dim]Agente Inteligente con Búsqueda en Anchura (BFS)[/]"
    )
    console.print(
        Panel(
            banner_texto,
            title="[bold green]Inteligencia Artificial[/]",
            border_style="cyan",
            expand=False,
        )
    )


def generar_entregables_resultados(dir_salida: Path = DIR_RESULTADOS) -> dict[str, Path]:
    """Genera los artefactos entregables en la carpeta de resultados."""
    dir_salida.mkdir(parents=True, exist_ok=True)
    console.print(f"[yellow]Generando entregables en:[/] [cyan]{dir_salida.resolve()}[/]")
    
    resultado = resolver_bfs()
    
    ruta_grafo = dir_salida / "arbol_navegacion_bfs.png"
    exportar_grafo(ruta_grafo, resultado=resultado)
    
    ruta_metricas = dir_salida / "metricas.json"
    exportar_metricas_json(ruta_metricas, resultado=resultado)
    
    ruta_html = dir_salida / "visualizador.html"
    exportar_visualizador_web(ruta_html, resultado=resultado)
    
    console.print(f"  [bold green][OK][/] Árbol de navegación: [cyan]{ruta_grafo.name}[/]")
    console.print(f"  [bold green][OK][/] Métricas estructuradas: [cyan]{ruta_metricas.name}[/]")
    console.print(f"  [bold green][OK][/] Visualizador web: [cyan]{ruta_html.name}[/]")
    
    return {"grafo": ruta_grafo, "metricas": ruta_metricas, "html": ruta_html}


def ejecutar_animacion(retraso: float = 0.5) -> None:
    """Calcula la solución BFS y reproduce la animación en consola."""
    console.print("[yellow]Calculando solución con BFS...[/]")
    resultado = resolver_bfs()
    animar_solucion(resultado, retraso_segundos=retraso, console=console)


def ejecutar_paso_a_paso() -> None:
    """Calcula la solución BFS y permite explorarla interactivamente."""
    console.print("[yellow]Calculando solución con BFS...[/]")
    resultado = resolver_bfs()
    recorrer_paso_a_paso(resultado, console=console)


def ejecutar_web(ruta_destino: Path = RUTA_HTML_DEFAULT, auto_abrir: bool = True) -> Path:
    """Calcula la solución BFS y abre la interfaz web interactiva en el navegador."""
    console.print("[yellow]Calculando solución BFS y preparando visualizador web...[/]")
    resultado = resolver_bfs()
    archivo = abrir_visualizador_web(ruta_archivo=ruta_destino, resultado=resultado, auto_abrir=auto_abrir)
    console.print(f"[bold green]Visualizador web listo en:[/] [cyan]{archivo.resolve()}[/]")
    if auto_abrir:
        console.print("[green]Se ha abierto una nueva pestaña en tu navegador web predeterminado.[/]")
    return archivo


def ejecutar_exportacion_grafo(ruta_destino: Path = RUTA_GRAFO_DEFAULT) -> Path:
    """Genera y guarda el grafo de estados con NetworkX y Matplotlib."""
    console.print(f"[yellow]Construyendo espacio de estados y exportando grafo...[/]")
    resultado = resolver_bfs()
    archivo = exportar_grafo(ruta_destino, resultado=resultado)
    console.print(f"[bold green]Grafo exportado exitosamente en:[/] [cyan]{archivo.resolve()}[/]")
    return archivo


def ejecutar_todo(retraso: float = 0.5, dir_salida: Path = DIR_RESULTADOS) -> None:
    """Ejecuta la animación y genera todos los entregables en la carpeta de resultados."""
    resultado = resolver_bfs()
    animar_solucion(resultado, retraso_segundos=retraso, console=console)
    console.print("\n")
    generar_entregables_resultados(dir_salida)


def menu_interactivo() -> None:
    """Despliega un menú interactivo en terminal para el usuario."""
    while True:
        console.clear()
        mostrar_banner()
        console.print("\n[bold yellow]Menú Principal:[/]")
        console.print("  [bold cyan]1.[/] Abrir visualizador interactivo en el navegador web (Recomendado)")
        console.print("  [bold cyan]2.[/] Ver animación automática en consola")
        console.print("  [bold cyan]3.[/] Recorrer la solución paso a paso (manual en consola)")
        console.print("  [bold cyan]4.[/] Generar todos los entregables en carpeta 'resultados/'")
        console.print("  [bold cyan]5.[/] Exportar solo grafo de navegación a imagen PNG")
        console.print("  [bold cyan]6.[/] Ejecutar todo (animación en consola + entregables)")
        console.print("  [bold cyan]7.[/] Salir\n")

        opcion = Prompt.ask(
            "[bold white]Seleccione una opción[/]",
            choices=["1", "2", "3", "4", "5", "6", "7"],
            default="1",
        )

        if opcion == "1":
            ejecutar_web()
            Prompt.ask("\nPresione [Enter] para volver al menú")
        elif opcion == "2":
            ejecutar_animacion()
            Prompt.ask("\nPresione [Enter] para volver al menú")
        elif opcion == "3":
            ejecutar_paso_a_paso()
            Prompt.ask("\nPresione [Enter] para volver al menú")
        elif opcion == "4":
            generar_entregables_resultados()
            Prompt.ask("\nPresione [Enter] para volver al menú")
        elif opcion == "5":
            ejecutar_exportacion_grafo()
            Prompt.ask("\nPresione [Enter] para volver al menú")
        elif opcion == "6":
            ejecutar_todo()
            Prompt.ask("\nPresione [Enter] para volver al menú")
        elif opcion == "7":
            console.print("[bold green]¡Hasta luego![/]")
            break


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Configura los argumentos por línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Solucionador del Rompecabezas Salto de Ranas mediante BFS."
    )
    parser.add_argument(
        "--web", "-w",
        action="store_true",
        help="Abre el visualizador interactivo en una pestaña del navegador web.",
    )
    parser.add_argument(
        "--animar", "-a",
        action="store_true",
        help="Reproduce la animación automática de la solución en consola.",
    )
    parser.add_argument(
        "--pasos", "-p",
        action="store_true",
        help="Recorre la solución paso a paso de forma manual.",
    )
    parser.add_argument(
        "--generar-resultados", "-r",
        action="store_true",
        help="Genera todos los archivos entregables en la carpeta 'resultados/'.",
    )
    parser.add_argument(
        "--grafo", "-g",
        action="store_true",
        help="Genera y exporta la imagen del grafo de estados en formato PNG.",
    )
    parser.add_argument(
        "--todo", "-t",
        action="store_true",
        help="Ejecuta la animación y genera todos los entregables.",
    )
    parser.add_argument(
        "--velocidad", "-s",
        type=float,
        default=0.5,
        help="Segundos de pausa entre cada paso en la animación (por defecto: 0.5).",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=RUTA_GRAFO_DEFAULT,
        help=f"Ruta del archivo de salida para el grafo (por defecto: {RUTA_GRAFO_DEFAULT}).",
    )
    return parser.parse_args(args)


def main(argv: list[str] | None = None) -> None:
    """Punto de entrada principal."""
    args = parse_args(argv)

    # Si no se pasó ninguna bandera, abrir el menú interactivo
    if not (args.web or args.animar or args.pasos or args.generar_resultados or args.grafo or args.todo):
        menu_interactivo()
        return

    try:
        if args.todo:
            ejecutar_todo(retraso=args.velocidad)
        elif args.generar_resultados:
            generar_entregables_resultados()
        elif args.web:
            ejecutar_web()
        elif args.animar:
            ejecutar_animacion(retraso=args.velocidad)
        elif args.pasos:
            ejecutar_paso_a_paso()
        elif args.grafo:
            ejecutar_exportacion_grafo(ruta_destino=args.output)
    except KeyboardInterrupt:
        console.print("\n[bold red]Ejecución interrumpida por el usuario.[/]")
        sys.exit(0)


if __name__ == "__main__":
    main()
