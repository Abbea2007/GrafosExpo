from flask import Flask

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grafo Interactivo con Lista de Adyacencia</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f4f8; color: #333; display: flex; flex-direction: column; align-items: center; margin: 0; padding: 20px; }
        h1 { margin-bottom: 10px; }
        .container { background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 20px; max-width: 900px; width: 100%; margin-bottom: 20px; }
        svg { width: 100%; height: auto; max-height: 400px; display: block; margin: 0 auto 20px; }
        .controls { display: flex; justify-content: center; flex-wrap: wrap; margin-top: 15px; }
        .controls input, .controls select { margin: 5px; padding: 5px; font-size: 14px; }
        button { margin: 5px; padding: 10px 20px; font-size: 14px; background: #3182ce; color: #fff; border: none; border-radius: 4px; cursor: pointer; }
        button:disabled { background: #a0aec0; cursor: default; }
        #adjList { width: 60%; margin: 0 auto; }
        .node-list { margin-bottom: 10px; }
        .node-list strong { margin-right: 10px; }
    </style>
</head>
<body>
    <h1>Grafo y Lista de Adyacencia</h1>
    <div class="container">
        <svg id="graph" viewBox="0 0 300 200">
            <circle id="node-A" cx="60" cy="140" r="20" fill="#f56565" />
            <text x="60" y="140" text-anchor="middle" dy=".3em" fill="#fff">A</text>
            <circle id="node-B" cx="60" cy="40" r="20" fill="#48bb78" />
            <text x="60" y="40" text-anchor="middle" dy=".3em" fill="#fff">B</text>
            <circle id="node-C" cx="240" cy="40" r="20" fill="#4299e1" />
            <text x="240" y="40" text-anchor="middle" dy=".3em" fill="#fff">C</text>
            <circle id="node-D" cx="240" cy="140" r="20" fill="#ed8936" />
            <text x="240" y="140" text-anchor="middle" dy=".3em" fill="#fff">D</text>
        </svg>
        <div id="adjList"></div>
        <div class="controls">
            <button onclick="resetGraph()">Reiniciar</button>
        </div>
        <div class="controls">
            <select id="fromNode"></select>
            <select id="toNode"></select>
            <input type="number" id="edgeWeight" placeholder="Peso" />
            <button onclick="addEdge()">Añadir Arista</button>
            <button onclick="removeEdge()">Remover Arista</button>
        </div>
    </div>
    <script>
        const nodes = ['A','B','C','D'];
        let adjacencyList = {};
        const svg = document.getElementById('graph');
        const edgeElements = {};

        window.onload = () => {
            initControls();
            initGraph();
        };

        function initControls() {
            const from = document.getElementById('fromNode');
            const to = document.getElementById('toNode');
            nodes.forEach(n => {
                from.add(new Option(n, n));
                to.add(new Option(n, n));
            });
        }

        function initGraph() {
            // Inicializar lista vacía
            nodes.forEach(n => adjacencyList[n] = []);
            // Aristas iniciales
            const initial = [ ['A','B',1], ['A','C',-4], ['A','D',2], ['B','C',3] ];
            initial.forEach(([a,b,w]) => {
                addEdgeToData(a,b,w);
                drawEdge(a, b, w);
            });
            renderAdjList();
        }

        function renderAdjList() {
            const container = document.getElementById('adjList');
            container.innerHTML = '';
            nodes.forEach(n => {
                const div = document.createElement('div');
                div.className = 'node-list';
                const title = document.createElement('strong');
                title.textContent = n + ' →';
                div.appendChild(title);
                const list = document.createElement('span');
                const items = adjacencyList[n].map(([dest,w]) => `(${dest}, ${w})`).join(', ');
                list.textContent = '[' + items + ']';
                div.appendChild(list);
                container.appendChild(div);
            });
        }

        function addEdgeToData(a, b, w) {
            adjacencyList[a].push([b, Number(w)]);
            adjacencyList[b].push([a, Number(w)]);
        }
# Dibuja una arista entre dos nodos en el SVG y actualiza la matriz de adyacencia.
# Si la arista ya existe, se actualiza; si no, se crea una nueva línea y su etiqueta con el peso.

        function drawEdge(a, b, w) {
            const nodeA = document.getElementById(`node-${a}`);
            const nodeB = document.getElementById(`node-${b}`);
            const x1 = +nodeA.getAttribute('cx'), y1 = +nodeA.getAttribute('cy');
            const x2 = +nodeB.getAttribute('cx'), y2 = +nodeB.getAttribute('cy');
            const idLine = `edge-${a}${b}`;
            const idLabel = `label-${a}${b}`;
            if (edgeElements[idLine]) return; // ya existe
            const line = document.createElementNS('http://www.w3.org/2000/svg','line');
            line.setAttribute('x1',x1);
            line.setAttribute('y1',y1);
            line.setAttribute('x2',x2);
            line.setAttribute('y2',y2);
            line.setAttribute('stroke','#333');
            line.setAttribute('stroke-width','2');
            line.id = idLine;
            svg.appendChild(line);
            const txt = document.createElementNS('http://www.w3.org/2000/svg','text');
            txt.setAttribute('x',(x1+x2)/2);
            txt.setAttribute('y',(y1+y2)/2 - 5);
            txt.setAttribute('text-anchor','middle');
            txt.textContent = w;
            txt.id = idLabel;
            svg.appendChild(txt);
            edgeElements[idLine] = { line, txt };
        }

        function addEdge() {
            const a = document.getElementById('fromNode').value;
            const b = document.getElementById('toNode').value;
            const w = document.getElementById('edgeWeight').value;
            if (!w || a === b) return;
            addEdgeToData(a, b, w);
            drawEdge(a, b, w);
            renderAdjList();
        }

        function removeEdge() {
            const a = document.getElementById('fromNode').value;
            const b = document.getElementById('toNode').value;
            // Filtrar datos
            adjacencyList[a] = adjacencyList[a].filter(item => item[0] !== b);
            adjacencyList[b] = adjacencyList[b].filter(item => item[0] !== a);
            // Remover SVG
            const idLine = `edge-${a}${b}`;
            const idLine2 = `edge-${b}${a}`;
            [idLine, idLine2].forEach(id => {
                if (edgeElements[id]) {
                    edgeElements[id].line.remove();
                    edgeElements[id].txt.remove();
                    delete edgeElements[id];
                }
            });
            renderAdjList();
        }

        function resetGraph() {
            // Limpiar SVG de aristas
            Object.values(edgeElements).forEach(e => { e.line.remove(); e.txt.remove(); });
            for (let k in edgeElements) delete edgeElements[k];
            initGraph();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return html

if __name__ == '__main__':
    app.run(debug=True)
