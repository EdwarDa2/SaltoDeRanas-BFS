# Salto de Ranas - Solucionador BFS

Agente inteligente basado en metas para resolver de forma óptima el rompecabezas clásico lineal **Salto de Ranas** (*Frogs Jumping Puzzle*) mediante **Búsqueda en Anchura (BFS)**.

> 💡 **Guía Rápida para el Evaluador:** Consulte el archivo **[`INSTRUCCIONES_EVALUADOR.md`](INSTRUCCIONES_EVALUADOR.md)** o ejecute directamente **`ejecutar.bat`** (Windows) para iniciar la visualización interactiva con un solo clic.

---

## 📋 Descripción del Problema

El rompecabezas se compone de un tablero unidimensional de 7 casillas con 3 fichas rojas (`R`), 3 fichas verdes (`V`) y 1 espacio vacío (`_`):

*   **Estado Inicial:** `RRR_VVV`
*   **Estado Meta:** `VVV_RRR`

### Reglas de Movimiento
*   Las ranas **R** únicamente se mueven hacia la **derecha**.
*   Las ranas **V** únicamente se mueven hacia la **izquierda**.
*   **Avanzar (costo 1):** Moverse a una casilla adyacente vacía.
*   **Saltar (costo 1):** Saltar sobre una rana de distinto color hacia una casilla vacía contigua.

### Espacio de Estados y Grafo
*   **Combinaciones teóricas:** $\frac{7!}{3! \cdot 3! \cdot 1!} = 140$ estados posibles.
*   **Estados alcanzables reales:** **72 estados**.
*   **Estructura del grafo:** Grafo Dirigido Acíclico (**DAG**) sin ciclos.
*   **Estados sin salida (*deadlocks*):** **13 estados** donde no hay movimientos legales posibles.
*   **Longitud de solución óptima:** **15 movimientos** ($n^2 + 2n$ para $n=3$).

---

## 🏗️ Arquitectura del Proyecto

```text
SaltoDeRanas-BFS/
├── core/                       # Lógica de dominio y motor de búsqueda
│   ├── state.py                # Modelo de estado, validación y transiciones
│   └── bfs_solver.py           # Algoritmo BFS y reconstrucción de ruta
├── ui/                         # Interfaces de visualización
│   ├── visualizer.py           # Animación en consola con Rich
│   ├── web_visualizer.py       # Generador de interfaz web interactiva
│   └── visualizador_web.html   # Interfaz web generada con botón Start
├── analytics/                  # Análisis y exportación de grafos
│   ├── graph_exporter.py       # Construcción del DAG con NetworkX y Matplotlib
│   └── grafo_salto_ranas.png   # Imagen exportada del espacio de estados
├── tests/                      # Suite de pruebas automatizadas con pytest
│   ├── test_state.py
│   ├── test_bfs.py
│   ├── test_visualizer.py
│   ├── test_web_visualizer.py
│   ├── test_graph_exporter.py
│   └── test_main.py
├── main.py                     # Punto de entrada y orquestador CLI
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Documentación técnica
```

---

## 🚀 Instalación y Requisitos

Requiere **Python 3.10+**.

1. Clonar el repositorio o situarse en el directorio raíz del proyecto.
2. Instalar las dependencias requeridas:

```bash
pip install -r requirements.txt
```

Dependencias principales:
*   `rich`: Animación e interfaces estéticas en terminal.
*   `networkx`: Modelado de grafos y análisis de estados.
*   `matplotlib`: Renderizado y exportación visual del DAG.
*   `pytest`: Ejecución de pruebas unitarias.

---

## 💻 Uso y Ejecución

### 🌐 Modo Web (Interfaz en Navegador con Botón Start)
Abre automáticamente una pestaña en tu navegador predeterminado con el tablero interactivo, botón de Iniciar, Pausa, Reinicio, selector de velocidad y panel de métricas final:

```bash
python main.py --web
```

### 🖥️ Modo Menú Interactivo en Consola
```bash
python main.py
```

Opciones disponibles en el menú:
1. **Ver animación automática en consola** (reproduce los 15 movimientos).
2. **Recorrer la solución paso a paso** (presionando `[Enter]`).
3. **Abrir visualizador interactivo en el navegador web** (con botón Start).
4. **Exportar grafo de estados a imagen PNG**.
5. **Ejecutar todo** (animación en consola + exportación de grafo).
6. **Salir**.

### ⚙️ Banderas Directas por Línea de Comandos
```bash
# Abrir visualizador web en navegador
python main.py --web

# Animación en consola
python main.py --animar

# Cambiar la velocidad de la animación en consola (ej. 0.3 segundos por paso)
python main.py --animar --velocidad 0.3

# Recorrer paso a paso en consola
python main.py --pasos

# Exportar grafo de estados a PNG
python main.py --grafo

# Ejecutar todo
python main.py --todo
```

---

## 🧪 Ejecución de Pruebas Unitarias

Para correr la suite completa de 60 pruebas unitarias:

```bash
python -m pytest
```

---

## 📊 Visualización del Grafo

La exportación en `analytics/grafo_salto_ranas.png` clasifica visualmente cada nodo del DAG:
*   **Azul:** Estado inicial (`RRR_VVV`).
*   **Verde:** Estado meta (`VVV_RRR`).
*   **Amarillo / Dorado:** Ruta óptima de 15 pasos.
*   **Gris:** Estados viables (que pueden alcanzar la meta).
*   **Rojo Claro:** Estados condenados (no pueden alcanzar la meta).
*   **Rojo Intenso:** Estados *deadlock* (bloqueo total sin movimientos legales).
