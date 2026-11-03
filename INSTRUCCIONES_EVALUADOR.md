# 📋 Guía de Evaluación Rápida: Rompecabezas Salto de Ranas (BFS)

Estimado evaluador, este proyecto implementa un **agente inteligente** para la resolución óptima del clásico rompecabezas lineal **Salto de Ranas** (*Frogs Jumping Puzzle*) mediante **Búsqueda en Anchura (BFS)**.

---

## ⚡ ¿Cómo evaluar el proyecto? (3 Formas Rápidas)

Puede evaluar el sistema eligiendo la opción que le resulte más cómoda:

### Opción 1: Arranque Rápido con 1 Clic (Recomendado en Windows)
En la carpeta raíz del proyecto, simplemente haga **doble clic sobre el archivo**:
👉 `ejecutar.bat`

> Esto resolverá el problema con BFS y **abrirá de inmediato una pestaña interactiva en su navegador web**, con el botón **Start** para ver la animación y la pestaña para inspeccionar el árbol de navegación completo.

---

### Opción 2: Ejecución desde Terminal
Abra una terminal en la carpeta del proyecto y elija cualquiera de los siguientes comandos:

```bash
# 1. Abrir la interfaz web interactiva en el navegador
python main.py --web

# 2. Ver la animación directamente en la consola (Rich)
python main.py --animar

# 3. Recorrer la solución paso a paso en consola (presionando Enter)
python main.py --pasos

# 4. Desplegar el menú interactivo completo con todas las opciones
python main.py
```

*Nota: Si aún no tiene instaladas las dependencias, puede ejecutarlas con: `pip install -r requirements.txt`.*

---

### Opción 3: Inspección Directa (Sin escribir código ni comandos)
Si prefiere revisar de inmediato los resultados sin ejecutar terminales, abra la carpeta **[`resultados/`](resultados/)**:

1. **`resultados/visualizador.html`**:
   * Haga **doble clic** para abrirlo en su navegador.
   * Cuenta con el botón **"Iniciar Animación" (Start)**, controles de pausa/velocidad, narrador de cada salto y una pestaña superior con el **Árbol de Navegación**.
2. **`resultados/arbol_navegacion_bfs.png`**:
   * Imagen en alta resolución del grafo completo (DAG) con los 72 estados organizados por niveles (0 a 15), identificando la ruta óptima de 15 pasos y los 13 *deadlocks*.
3. **`resultados/metricas.json`**:
   * Datos cuantitativos de la ejecución (longitud óptima, nodos explorados, tiempo en milisegundos y secuencia formal de movimientos).

---

## 🧪 Validación de Pruebas Automatizadas

El código fue desarrollado bajo estándares de desarrollo guiado por pruebas (TDD). Para comprobar la suite completa de **61 pruebas unitarias**:

```bash
python -m pytest
```

---

## 🗺️ Mapeo de Componentes para la Evaluación

| Criterio a Evaluar | Ubicación en el Código | Descripción |
|---|---|---|
| **Modelo y Reglas del Dominio** | `core/state.py` | Definición de estados, validación inmutable y generador de sucesores legales (avances y saltos). |
| **Algoritmo de Búsqueda (BFS)** | `core/bfs_solver.py` | Implementación formal de BFS con cola FIFO, control de visitados, recolección de métricas y reconstrucción de ruta. |
| **Árbol / Grafo de Navegación** | `analytics/graph_exporter.py` y `resultados/arbol_navegacion_bfs.png` | Modelado del DAG con NetworkX, layout por niveles, detección de 13 deadlocks y exportación gráfica. |
| **Visualización Web Interactiva** | `ui/web_visualizer.py` y `resultados/visualizador.html` | Interfaz en navegador con botón Start, animación y pestañas integradas. |
| **Visualización en Consola** | `ui/visualizer.py` | Animación paso a paso formateada con la librería `Rich`. |
| **Punto de Entrada / CLI** | `main.py` | Orquestación general mediante argumentos CLI y menú interactivo. |
| **Pruebas Automatizadas** | `tests/` | 61 tests unitarios con `pytest` que verifican consistencia matemática y algorítmica. |

---

## 📊 Resumen de Resultados Verificados

* **Estado Inicial:** `RRR_VVV` | **Estado Meta:** `VVV_RRR`
* **Solución Óptima:** **15 movimientos** (coincide exactamente con la cota teórica $n^2 + 2n = 15$).
* **Espacio de Estados Alcanzables:** **72 estados** (de 140 permutaciones teóricas posibles).
* **Estados sin salida (*deadlocks*):** **13 estados** evitados exitosamente por el algoritmo.
* **Nodos explorados por BFS:** **72** (exploración exhaustiva de los alcanzables).
* **Tiempo de resolución:** **~0.14 ms**.

