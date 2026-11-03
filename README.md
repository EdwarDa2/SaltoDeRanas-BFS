# Salto de Ranas - Solucionador BFS

Agente inteligente basado en metas para resolver de forma óptima el rompecabezas clásico lineal **Salto de Ranas** (*Frogs Jumping Puzzle*) mediante **Búsqueda en Anchura (BFS)**.

> **Guía Rápida para el Evaluador:** Consulte el archivo **[`INSTRUCCIONES_EVALUADOR.md`](INSTRUCCIONES_EVALUADOR.md)** o ejecute directamente **`INICIAR_SISTEMA.bat`** (Windows) para iniciar la visualización interactiva con un solo clic.

---

## Descripción del Problema

El rompecabezas se compone de un tablero unidimensional de 7 casillas con 3 fichas rojas (`R`), 3 fichas verdes (`V`) y 1 espacio vacío (`_`):

*   **Estado Inicial:** `RRR_VVV`
*   **Estado Meta:** `VVV_RRR`

### Reglas de Movimiento
*   Las ranas **R** únicamente se mueven hacia la **derecha**.
*   Las ranas **V** únicamente se mueven hacia la **izquierda**.
*   **Avanzar (costo 1):** Moverse a una casilla adyacente vacía.
*   **Saltar (costo 1):** Saltar sobre una rana de distinto color hacia una casilla vacía contigua.

### Espacio de Estados y Grafo
*   **Combinaciones teóricas:** 7! / (3! * 3! * 1!) = 140 estados posibles.
*   **Estados alcanzables reales:** **72 estados**.
*   **Estructura del grafo:** Grafo Dirigido Acíclico (**DAG**) sin ciclos.
*   **Estados sin salida (*deadlocks*):** **13 estados** donde no hay movimientos legales posibles.
*   **Longitud de solución óptima:** **15 movimientos** (coincide con n^2 + 2n para n=3).

---

## Arquitectura del Proyecto

```text
SaltoDeRanas-BFS/
├── INICIAR_SISTEMA.bat          # Lanzador directo con doble clic para Windows
├── INSTRUCCIONES_EVALUADOR.md   # Guía rápida de evaluación
├── README.md                    # Documentación técnica general
├── main.py                      # Punto de entrada y orquestador CLI
├── requirements.txt             # Dependencias del proyecto
│
├── core/                        # Dominio y motor de búsqueda
│   ├── state.py                 # Modelo de estado, validación y transiciones
│   └── bfs_solver.py            # Algoritmo BFS y reconstrucción de ruta
│
├── ui/                          # Interfaces de visualización
│   ├── visualizer.py            # Animación en consola con Rich
│   └── web_visualizer.py        # Generador de interfaz web interactiva
│
├── analytics/                   # Análisis y exportación de grafos
│   └── graph_exporter.py        # Construcción del DAG con NetworkX y Matplotlib
│
├── resultados/                  # Entregables pre-generados
│   ├── visualizador.html        # Interfaz web con animación y árbol de navegación
│   ├── arbol_navegacion_bfs.png # Imagen de alta resolución del DAG
│   └── metricas.json            # Reporte numérico estructurado
│
└── tests/                       # Suite de pruebas automatizadas con pytest
    ├── test_state.py
    ├── test_bfs.py
    ├── test_visualizer.py
    ├── test_web_visualizer.py
    ├── test_graph_exporter.py
    └── test_main.py
```

---

## Instalación y Requisitos

Requiere **Python 3.10+**.

1. Situarse en el directorio raíz del proyecto.
2. Instalar las dependencias requeridas:

```bash
pip install -r requirements.txt
```

Dependencias principales:
*   `rich`: Animación e interfaces en terminal.
*   `networkx`: Modelado de grafos y análisis de estados.
*   `matplotlib`: Renderizado y exportación visual del DAG.
*   `pytest`: Ejecución de pruebas unitarias.

---

## Uso y Ejecución

### Modo 1: Doble Clic en Windows (Recomendado)
Haga doble clic en el archivo:
`INICIAR_SISTEMA.bat`

### Modo 2: Interfaz Web en Navegador
Abre automáticamente una pestaña en su navegador predeterminado con el tablero interactivo, botón Iniciar Animación, controles de pausa y la pestaña del árbol de navegación:

```bash
python main.py --web
```

### Modo 3: Menú Interactivo en Consola
```bash
python main.py
```

### Modo 4: Banderas Directas por Línea de Comandos
```bash
# Ver animación en consola
python main.py --animar

# Cambiar la velocidad de la animación en consola (ej. 0.3 segundos por paso)
python main.py --animar --velocidad 0.3

# Recorrer paso a paso en consola
python main.py --pasos

# Generar todos los entregables en resultados/
python main.py --generar-resultados

# Exportar grafo de estados a PNG
python main.py --grafo

# Ejecutar todo
python main.py --todo
```

---

## Ejecución de Pruebas Unitarias

Para correr la suite completa de 61 pruebas unitarias:

```bash
python -m pytest
```

---

## Visualización del Grafo

La exportación en `resultados/arbol_navegacion_bfs.png` clasifica visualmente cada nodo del DAG:
*   **Azul:** Estado inicial (`RRR_VVV`).
*   **Verde:** Estado meta (`VVV_RRR`).
*   **Amarillo / Dorado:** Ruta óptima de 15 pasos.
*   **Gris:** Estados viables (que pueden alcanzar la meta).
*   **Rojo Claro:** Estados condenados (no pueden alcanzar la meta).
*   **Rojo Intenso:** Estados *deadlock* (bloqueo total sin movimientos legales).
