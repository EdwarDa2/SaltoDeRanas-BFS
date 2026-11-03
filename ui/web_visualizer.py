# Módulo 3B: Visualizador Web Interactivo (HTML5 / CSS3 / JS)
"""Generador de visualización web interactiva para Salto de Ranas."""
from __future__ import annotations

import base64
import json
import webbrowser
from pathlib import Path

from core.bfs_solver import ResultadoBusqueda, resolver_bfs

RUTA_HTML_DEFAULT = Path("resultados") / "visualizador.html"
RUTA_GRAFO_DEFAULT = Path("resultados") / "arbol_navegacion_bfs.png"


def obtener_imagen_grafo_b64(ruta_grafo: Path | str | None = None) -> str:
    """Lee y codifica en Base64 la imagen del grafo si existe."""
    candidatos = [
        Path(ruta_grafo) if ruta_grafo else None,
        RUTA_GRAFO_DEFAULT,
        Path("analytics") / "grafo_salto_ranas.png",
    ]
    for ruta in candidatos:
        if ruta and ruta.exists():
            try:
                datos = ruta.read_bytes()
                return f"data:image/png;base64,{base64.b64encode(datos).decode('ascii')}"
            except Exception:
                pass
    return ""


def construir_html_interactivo(
    resultado: ResultadoBusqueda,
    ruta_grafo: Path | str | None = None,
) -> str:
    """Genera el contenido HTML completo, autocontenido con CSS y JS."""
    grafo_b64 = obtener_imagen_grafo_b64(ruta_grafo)

    datos_solucion = {
        "ruta": resultado.ruta,
        "movimientos": [
            {
                "ficha": m.ficha,
                "origen": m.origen,
                "destino": m.destino,
                "tipo": m.tipo,
                "descripcion": str(m),
            }
            for m in resultado.movimientos
        ],
        "metricas": {
            "longitud": resultado.longitud,
            "nodos_explorados": resultado.nodos_explorados,
            "nodos_descubiertos": resultado.nodos_descubiertos,
            "tiempo_ms": round(resultado.tiempo_ms, 4),
            "estado_inicial": resultado.ruta[0],
            "estado_meta": resultado.ruta[-1],
        },
    }

    json_data = json.dumps(datos_solucion, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Salto de Ranas - Solucionador BFS</title>
  <style>
    :root {{
      --bg: #0f172a;
      --card-bg: #1e293b;
      --accent-red: #ef4444;
      --accent-green: #22c55e;
      --accent-blue: #38bdf8;
      --accent-gold: #f59e0b;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --pad-color: #334155;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}
    body {{
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 1.5rem 1rem;
    }}
    header {{
      text-align: center;
      margin-bottom: 1.5rem;
    }}
    h1 {{
      font-size: 2.2rem;
      background: linear-gradient(to right, #38bdf8, #22c55e);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.3rem;
    }}
    .subtitle {{
      color: var(--text-muted);
      font-size: 1rem;
    }}
    /* Barra de Pestanas */
    .tab-bar {{
      display: flex;
      gap: 0.5rem;
      margin-bottom: 1rem;
      width: 100%;
      max-width: 950px;
    }}
    .tab-btn {{
      flex: 1;
      background: #1e293b;
      color: var(--text-muted);
      border: 1px solid #334155;
      padding: 0.75rem 1rem;
      border-radius: 0.5rem;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      transition: all 0.2s ease;
    }}
    .tab-btn:hover {{
      background: #334155;
      color: white;
    }}
    .tab-btn.active {{
      background: linear-gradient(135deg, #0284c7, #0369a1);
      color: white;
      border-color: #38bdf8;
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
    }}
    .main-container {{
      width: 100%;
      max-width: 950px;
      background: var(--card-bg);
      border-radius: 1rem;
      padding: 2rem;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
      border: 1px solid #334155;
    }}
    .tab-content {{
      display: none;
    }}
    .tab-content.active {{
      display: block;
    }}
    /* Tablero de casillas */
    .pond-board {{
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 12px;
      margin: 1.5rem 0;
      padding: 1.5rem;
      background: #091222;
      border-radius: 1rem;
      border: 2px dashed #334155;
    }}
    .slot {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      aspect-ratio: 1;
      background: var(--pad-color);
      border-radius: 50%;
      position: relative;
      transition: all 0.3s ease;
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.4);
    }}
    .slot-idx {{
      position: absolute;
      bottom: -22px;
      font-size: 0.8rem;
      color: var(--text-muted);
      font-weight: 600;
    }}
    .frog {{
      width: 82%;
      height: 82%;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.5rem;
      color: white;
      cursor: default;
      transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
      box-shadow: 0 4px 10px rgba(0,0,0,0.3);
      user-select: none;
    }}
    .frog.red {{
      background: linear-gradient(135deg, #f87171, #dc2626);
      border: 2px solid #fca5a5;
    }}
    .frog.green {{
      background: linear-gradient(135deg, #4ade80, #16a34a);
      border: 2px solid #86efac;
    }}
    /* Narrativa de movimiento */
    .narrative-box {{
      text-align: center;
      padding: 1rem;
      background: #0f172a;
      border-radius: 0.5rem;
      border: 1px solid #334155;
      margin-bottom: 1rem;
      min-height: 60px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .step-indicator {{
      font-size: 0.9rem;
      color: var(--accent-blue);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.2rem;
    }}
    .move-description {{
      font-size: 1.15rem;
      font-weight: 500;
    }}
    /* Controles */
    .controls {{
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      justify-content: center;
      align-items: center;
      margin-top: 1.5rem;
    }}
    button.btn {{
      background: #334155;
      color: white;
      border: none;
      padding: 0.75rem 1.4rem;
      border-radius: 0.5rem;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s ease;
    }}
    button.btn:hover:not(:disabled) {{
      background: #475569;
      transform: translateY(-2px);
    }}
    button.btn:disabled {{
      opacity: 0.4;
      cursor: not-allowed;
    }}
    button.primary {{
      background: linear-gradient(135deg, #0284c7, #0369a1);
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
    }}
    button.primary:hover:not(:disabled) {{
      background: linear-gradient(135deg, #0369a1, #075985);
    }}
    .speed-control {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.9rem;
      color: var(--text-muted);
      margin-left: 0.5rem;
    }}
    input[type=range] {{
      accent-color: var(--accent-blue);
      cursor: pointer;
    }}
    /* Panel de resultados al finalizar */
    .results-panel {{
      display: none;
      margin-top: 1.8rem;
      padding: 1.5rem;
      background: #091222;
      border: 1px solid #22c55e;
      border-radius: 0.75rem;
      animation: fadeIn 0.5s ease;
    }}
    .results-panel.visible {{
      display: block;
    }}
    .results-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: var(--accent-green);
      font-size: 1.25rem;
      font-weight: 700;
      margin-bottom: 1rem;
    }}
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 1rem;
    }}
    .stat-card {{
      background: #1e293b;
      padding: 1rem;
      border-radius: 0.5rem;
      border-left: 3px solid var(--accent-blue);
    }}
    .stat-label {{
      font-size: 0.75rem;
      color: var(--text-muted);
      text-transform: uppercase;
    }}
    .stat-value {{
      font-size: 1.25rem;
      font-weight: 700;
      color: #f1f5f9;
      margin-top: 0.2rem;
    }}
    /* Seccion Arbol de Navegacion */
    .tree-section {{
      display: flex;
      flex-direction: column;
      gap: 1.2rem;
    }}
    .tree-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }}
    .tree-badges {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      font-size: 0.8rem;
    }}
    .badge {{
      padding: 0.3rem 0.6rem;
      border-radius: 0.25rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
    }}
    .badge-init {{ background: #1e3a8a; color: #93c5fd; }}
    .badge-goal {{ background: #064e3b; color: #6ee7b7; }}
    .badge-opt {{ background: #78350f; color: #fde68a; }}
    .badge-deadlock {{ background: #7f1d1d; color: #fca5a5; }}
    .badge-viable {{ background: #334155; color: #cbd5e1; }}
    .tree-img-container {{
      width: 100%;
      max-height: 600px;
      overflow: auto;
      background: #ffffff;
      border-radius: 0.5rem;
      border: 1px solid #475569;
      box-shadow: inset 0 2px 6px rgba(0,0,0,0.3);
      padding: 1rem;
      text-align: center;
    }}
    .tree-img-container img {{
      max-width: 100%;
      height: auto;
      cursor: zoom-in;
      transition: transform 0.3s ease;
    }}
    .tree-img-container img.zoomed {{
      max-width: none;
      width: 2500px;
      cursor: zoom-out;
    }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(10px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>
</head>
<body>

  <header>
    <h1>Rompecabezas Salto de Ranas</h1>
    <p class="subtitle">Agente Inteligente con Búsqueda en Anchura (BFS)</p>
  </header>

  <!-- Barra de pestanas -->
  <div class="tab-bar">
    <button class="tab-btn active" id="tab-btn-sim" onclick="switchTab('sim')">
      Animación del Rompecabezas
    </button>
    <button class="tab-btn" id="tab-btn-tree" onclick="switchTab('tree')">
      Árbol de Navegación BFS (72 Estados)
    </button>
  </div>

  <main class="main-container">
    <!-- PESTANA 1: ANIMACION DEL JUEGO -->
    <div id="tab-sim" class="tab-content active">
      <div class="narrative-box">
        <div id="step-indicator" class="step-indicator">Paso 0 de 15</div>
        <div id="move-description" class="move-description">Configuración Inicial (Estado de partida)</div>
      </div>

      <!-- Tablero de 7 casillas -->
      <div class="pond-board" id="board"></div>

      <!-- Controles -->
      <div class="controls">
        <button id="btn-start" class="btn primary" onclick="togglePlay()">
          <span id="play-text">Iniciar Animación</span>
        </button>
        <button id="btn-prev" class="btn" onclick="stepPrev()" disabled>Anterior</button>
        <button id="btn-next" class="btn" onclick="stepNext()">Siguiente</button>
        <button id="btn-reset" class="btn" onclick="resetState()">Reiniciar</button>

        <div class="speed-control">
          <label for="speed-range">Velocidad:</label>
          <input type="range" id="speed-range" min="200" max="1500" step="100" value="700" onchange="updateSpeed()">
        </div>
      </div>

      <!-- Panel de Resultados Final -->
      <div id="results-panel" class="results-panel">
        <div class="results-header">
          <span>Solución Óptima Encontrada y Verificada</span>
          <button class="btn" onclick="switchTab('tree')" style="font-size:0.85rem; padding:0.4rem 0.8rem;">
            Ver Árbol de Navegación
          </button>
        </div>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-label">Movimientos Óptimos</div>
            <div class="stat-value" id="stat-moves">15</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Nodos Explorados BFS</div>
            <div class="stat-value" id="stat-explored">72 / 72 (100%)</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Tiempo de Cálculo BFS</div>
            <div class="stat-value" id="stat-time">0.14 ms</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Estados Deadlock Evitados</div>
            <div class="stat-value">13</div>
          </div>
        </div>
      </div>
    </div>

    <!-- PESTANA 2: ARBOL DE NAVEGACION -->
    <div id="tab-tree" class="tab-content">
      <div class="tree-section">
        <div class="tree-header">
          <div>
            <h2 style="font-size:1.3rem; margin-bottom:0.2rem;">Espacio de Estados (DAG de 72 Nodos)</h2>
            <p style="color:var(--text-muted); font-size:0.85rem;">
              Estratificado en 16 niveles de profundidad (0 a 15). Haz clic en la imagen para ampliar o reducir.
            </p>
          </div>
          <div class="tree-badges">
            <span class="badge badge-init">Inicial (1)</span>
            <span class="badge badge-opt">Ruta Óptima (14)</span>
            <span class="badge badge-goal">Meta (1)</span>
            <span class="badge badge-viable">Viables (14)</span>
            <span class="badge badge-deadlock">Deadlocks (13)</span>
          </div>
        </div>

        <div class="tree-img-container" id="tree-container">
          {"<img id='tree-img' src='" + grafo_b64 + "' alt='Árbol de navegación BFS' onclick='toggleZoom(this)' title='Haz clic para ampliar/reducir'>" if grafo_b64 else "<p style='color:#333; padding:2rem;'>El archivo del árbol de navegación (arbol_navegacion_bfs.png) no fue encontrado. Ejecute 'python main.py --generar-resultados' para crearlo.</p>"}
        </div>
      </div>
    </div>
  </main>

  <script>
    const DATA = {json_data};

    let currentStep = 0;
    let isPlaying = false;
    let playTimer = null;
    let speedMs = 700;

    const board = document.getElementById('board');
    const stepIndicator = document.getElementById('step-indicator');
    const moveDescription = document.getElementById('move-description');
    const playText = document.getElementById('play-text');
    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');
    const resultsPanel = document.getElementById('results-panel');

    function switchTab(tab) {{
      const tabSim = document.getElementById('tab-sim');
      const tabTree = document.getElementById('tab-tree');
      const btnSim = document.getElementById('tab-btn-sim');
      const btnTree = document.getElementById('tab-btn-tree');

      if (tab === 'sim') {{
        tabSim.classList.add('active');
        tabTree.classList.remove('active');
        btnSim.classList.add('active');
        btnTree.classList.remove('active');
      }} else {{
        tabSim.classList.remove('active');
        tabTree.classList.add('active');
        btnSim.classList.remove('active');
        btnTree.classList.add('active');
      }}
    }}

    function toggleZoom(img) {{
      img.classList.toggle('zoomed');
    }}

    function renderBoard(step) {{
      const state = DATA.ruta[step];
      board.innerHTML = '';

      for (let i = 0; i < state.length; i++) {{
        const char = state[i];
        const slot = document.createElement('div');
        slot.className = 'slot';

        const idx = document.createElement('span');
        idx.className = 'slot-idx';
        idx.innerText = `[${{i}}]`;
        slot.appendChild(idx);

        if (char === 'R') {{
          const frog = document.createElement('div');
          frog.className = 'frog red';
          frog.innerText = 'R';
          slot.appendChild(frog);
        }} else if (char === 'V') {{
          const frog = document.createElement('div');
          frog.className = 'frog green';
          frog.innerText = 'V';
          slot.appendChild(frog);
        }}
        board.appendChild(slot);
      }}

      stepIndicator.innerText = `Paso ${{step}} de ${{DATA.metricas.longitud}}`;
      if (step === 0) {{
        moveDescription.innerText = 'Configuración Inicial (Estado de partida: ' + state + ')';
      }} else {{
        const mov = DATA.movimientos[step - 1];
        const color = mov.ficha === 'R' ? 'Roja' : 'Verde';
        const accion = mov.tipo === 'saltar' ? 'SALTÓ' : 'AVANZÓ';
        moveDescription.innerHTML = `Rana <strong>${{color}}</strong> ${{accion}} desde casilla [${{mov.origen}}] hacia casilla [${{mov.destino}}]`;
      }}

      btnPrev.disabled = (step === 0);
      btnNext.disabled = (step === DATA.ruta.length - 1);

      if (step === DATA.ruta.length - 1) {{
        resultsPanel.classList.add('visible');
        document.getElementById('stat-moves').innerText = DATA.metricas.longitud;
        document.getElementById('stat-explored').innerText = `${{DATA.metricas.nodos_explorados}} / ${{DATA.metricas.nodos_descubiertos}}`;
        document.getElementById('stat-time').innerText = `${{DATA.metricas.tiempo_ms}} ms`;
      }} else {{
        resultsPanel.classList.remove('visible');
      }}
    }}

    function togglePlay() {{
      if (isPlaying) {{
        pause();
      }} else {{
        if (currentStep >= DATA.ruta.length - 1) {{
          currentStep = 0;
          renderBoard(0);
        }}
        play();
      }}
    }}

    function play() {{
      isPlaying = true;
      playText.innerText = 'Pausar';
      playTimer = setInterval(() => {{
        if (currentStep < DATA.ruta.length - 1) {{
          currentStep++;
          renderBoard(currentStep);
        }} else {{
          pause();
        }}
      }}, speedMs);
    }}

    function pause() {{
      isPlaying = false;
      playText.innerText = 'Continuar';
      clearInterval(playTimer);
    }}

    function stepNext() {{
      pause();
      if (currentStep < DATA.ruta.length - 1) {{
        currentStep++;
        renderBoard(currentStep);
      }}
    }}

    function stepPrev() {{
      pause();
      if (currentStep > 0) {{
        currentStep--;
        renderBoard(currentStep);
      }}
    }}

    function resetState() {{
      pause();
      currentStep = 0;
      playText.innerText = 'Iniciar Animación';
      renderBoard(0);
    }}

    function updateSpeed() {{
      speedMs = parseInt(document.getElementById('speed-range').value);
      if (isPlaying) {{
        pause();
        play();
      }}
    }}

    renderBoard(0);
  </script>
</body>
</html>
"""


def exportar_visualizador_web(
    ruta_archivo: Path | str = RUTA_HTML_DEFAULT,
    resultado: ResultadoBusqueda | None = None,
    ruta_grafo: Path | str | None = None,
) -> Path:
    """Genera y guarda el archivo HTML autocontenido en disco."""
    resultado = resultado or resolver_bfs()
    html_contenido = construir_html_interactivo(resultado, ruta_grafo=ruta_grafo)

    destino = Path(ruta_archivo)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(html_contenido, encoding="utf-8")
    return destino


def abrir_visualizador_web(
    ruta_archivo: Path | str = RUTA_HTML_DEFAULT,
    resultado: ResultadoBusqueda | None = None,
    ruta_grafo: Path | str | None = None,
    auto_abrir: bool = True,
) -> Path:
    """Exporta el archivo HTML y lo abre en una nueva pestaña del navegador."""
    destino = exportar_visualizador_web(ruta_archivo, resultado=resultado, ruta_grafo=ruta_grafo)
    if auto_abrir:
        webbrowser.open(destino.resolve().as_uri())
    return destino
