# Guia de Evaluacion Rapida: Rompecabezas Salto de Ranas (BFS)

Estimado evaluador, este proyecto implementa un **agente inteligente** para la resolucion optima del clasico rompecabezas lineal **Salto de Ranas** (*Frogs Jumping Puzzle*) mediante **Busqueda en Anchura (BFS)**.

---

## Como evaluar el proyecto (3 Formas Rapidas)

Puede evaluar el sistema eligiendo la opcion que le resulte mas comoda:

### Opcion 1: Arranque Rapido con 1 Clic (Recomendado en Windows)
En la carpeta raiz del proyecto desde el Explorador de Archivos de Windows, simplemente haga **doble clic sobre el archivo**:
`INICIAR_SISTEMA.bat`

> Esto resolvera el problema con BFS y **abrira de inmediato una pestana interactiva en su navegador web predeterminado**, con el boton **Iniciar Animacion** para ver la solucion paso a paso y la pestana para inspeccionar el arbol de navegacion completo.

---

### Opcion 2: Ejecucion desde Terminal
Abra una terminal en la carpeta del proyecto y elija cualquiera de los siguientes comandos:

```bash
# 1. Abrir la interfaz web interactiva en el navegador
python main.py --web

# 2. Ver la animacion directamente en la consola (Rich)
python main.py --animar

# 3. Recorrer la solucion paso a paso en consola (presionando Enter)
python main.py --pasos

# 4. Desplegar el menu interactivo completo con todas las opciones
python main.py
```

*Nota: Si aun no tiene instaladas las dependencias, puede instalarlas con: `pip install -r requirements.txt`.*

---

### Opcion 3: Inspeccion Directa de Resultados (Sin escribir comandos)
Si prefiere revisar de inmediato los resultados sin ejecutar terminales, abra la carpeta **[`resultados/`](resultados/)**:

1. **`resultados/visualizador.html`**:
   * Haga **doble clic** para abrirlo en cualquier navegador web.
   * Cuenta con el boton **Iniciar Animacion**, controles de pausa/velocidad, narrador de cada salto y una pestana superior para ver el **Arbol de Navegacion**.
2. **`resultados/arbol_navegacion_bfs.png`**:
   * Imagen en alta resolucion del grafo completo (DAG) con los 72 estados organizados por niveles (0 a 15), identificando la ruta optima de 15 pasos y los 13 *deadlocks*.
3. **`resultados/metricas.json`**:
   * Datos cuantitativos de la ejecucion (longitud optima, nodos explorados, tiempo en milisegundos y secuencia formal de movimientos).

---

## Validacion de Pruebas Automatizadas

El codigo fue desarrollado bajo estandares de desarrollo guiado por pruebas (TDD). Para comprobar la suite completa de **61 pruebas unitarias**:

```bash
python -m pytest
```

---

## Mapeo de Componentes para la Evaluacion

| Criterio a Evaluar | Ubicacion en el Codigo | Descripcion |
|---|---|---|
| **Modelo y Reglas del Dominio** | `core/state.py` | Definicion de estados, validacion inmutable y generador de sucesores legales (avances y saltos). |
| **Algoritmo de Busqueda (BFS)** | `core/bfs_solver.py` | Implementacion formal de BFS con cola FIFO, control de visitados, recoleccion de metricas y reconstruccion de ruta. |
| **Arbol / Grafo de Navegacion** | `analytics/graph_exporter.py` y `resultados/arbol_navegacion_bfs.png` | Modelado del DAG con NetworkX, layout por niveles, deteccion de 13 deadlocks y exportacion grafica. |
| **Visualizacion Web Interactiva** | `ui/web_visualizer.py` y `resultados/visualizador.html` | Interfaz en navegador con boton Iniciar Animacion, reproduccion y pestanas integradas. |
| **Visualizacion en Consola** | `ui/visualizer.py` | Animacion paso a paso formateada con la libreria `Rich`. |
| **Punto de Entrada / CLI** | `main.py` | Orquestacion general mediante argumentos CLI y menu interactivo. |
| **Pruebas Automatizadas** | `tests/` | 61 tests unitarios con `pytest` que verifican consistencia matematica y algoritmica. |

---

## Resumen de Resultados Verificados

* **Estado Inicial:** `RRR_VVV` | **Estado Meta:** `VVV_RRR`
* **Solucion Optima:** **15 movimientos** (coincide exactamente con la cota teorica n^2 + 2n = 15).
* **Espacio de Estados Alcanzables:** **72 estados** (de 140 permutaciones teoricas posibles).
* **Estados sin salida (*deadlocks*):** **13 estados** evitados exitosamente por el algoritmo.
* **Nodos explorados por BFS:** **72** (exploracion exhaustiva de los alcanzables).
* **Tiempo de resolucion:** **~0.14 ms**.
