from flask import Flask

app = Flask(__name__)

# Página HTML con SVG, estilo y JavaScript interactivo
html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grafo Interactivo y Matriz de Adyacencia</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f4f8;
            color: #333;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0;
            padding: 20px;
        }
        h1 {
            margin-bottom: 10px;
        }
        .container {
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 20px;
            max-width: 900px;
            width: 100%;
            margin-bottom: 20px;
        }
        svg {
            width: 100%;
            height: auto;
            max-height: 400px;
            display: block;
            margin: 0 auto 20px;
        }
        table {
            width: 60%;
            border-collapse: collapse;
            margin: 0 auto;
        }
        th, td {
            border: 1px solid #aaa;
            padding: 8px;
            text-align: center;
        }
        th {
            background: #e2e8f0;
        }
        button {
            margin: 5px;
            padding: 10px 20px;
            font-size: 14px;
            background: #3182ce;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:disabled {
            background: #a0aec0;
            cursor: default;
        }
        .controls {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 15px;
        }
        .controls input, .controls select {
            margin: 5px;
            padding: 5px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>Grafo y Matriz de Adyacencia</h1>
    <div class="container">
        <!-- SVG del grafo -->
        <svg id="graph" viewBox="0 0 300 200">
            <!-- Nodos -->
            <circle id="node-A" cx="60" cy="140" r="20" fill="#f56565" />
            <text x="60" y="140" text-anchor="middle" dy=".3em" fill="#fff">A</text>

            <circle id="node-B" cx="60" cy="40" r="20" fill="#48bb78" />
            <text x="60" y="40" text-anchor="middle" dy=".3em" fill="#fff">B</text>

            <circle id="node-C" cx="240" cy="40" r="20" fill="#4299e1" />
            <text x="240" y="40" text-anchor="middle" dy=".3em" fill="#fff">C</text>

            <circle id="node-D" cx="240" cy="140" r="20" fill="#ed8936" />
            <text x="240" y="140" text-anchor="middle" dy=".3em" fill="#fff">D</text>
        </svg>

        <!-- Matriz de adyacencia -->
        <table id="matrix"></table>
        
        <div class="controls">
            <button id="nextBtn" onclick="nextStep()">Siguiente</button>
            <button onclick="resetMatrix()">Reiniciar</button>
        </div>

        <!-- Controles dinámicos -->
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
        const steps = [
            {r:0, c:0, w:0}, {r:0, c:1, w:1}, {r:0, c:2, w:-4}, {r:0, c:3, w:2},
            {r:1, c:0, w:1}, {r:1, c:1, w:0}, {r:1, c:2, w:3}, {r:1, c:3, w:0},
            {r:2, c:0, w:-4}, {r:2, c:1, w:3}, {r:2, c:2, w:0}, {r:2, c:3, w:0},
            {r:3, c:0, w:2}, {r:3, c:1, w:0}, {r:3, c:2, w:0}, {r:3, c:3, w:0}
        ];
        let current = 0;
        const edgeElements = {};

        window.onload = () => {
            initMatrix();
            initNodeSelectors();
            renderStaticEdges();
        };

        function initMatrix() {
            const table = document.getElementById('matrix');
            table.innerHTML = '';
            const header = table.insertRow();
            header.insertCell().innerHTML = '';
            nodes.forEach(n => {
                const th = document.createElement('th');
                th.textContent = n;
                header.appendChild(th);
            });
            nodes.forEach((n,i) => {
                const row = table.insertRow();
                const th = document.createElement('th');
                th.textContent = n;
                row.appendChild(th);
                nodes.forEach((_, j) => {
                    const cell = row.insertCell();
                    cell.id = `cell-${i}-${j}`;
                    cell.textContent = '';
                });
            });
        }

        function initNodeSelectors() {
            const from = document.getElementById('fromNode');
            const to = document.getElementById('toNode');
            nodes.forEach(n => {
                const o1 = document.createElement('option'); o1.value = n; o1.text = n;
                const o2 = document.createElement('option'); o2.value = n; o2.text = n;
                from.appendChild(o1);
                to.appendChild(o2);
            });
        }

        function renderStaticEdges() {
            // Aristas iniciales
            steps.slice(1).filter(s=>s.w!==0).forEach(({r,c,w})=>{
                const key = nodes[r]+nodes[c];
                drawEdge(nodes[r], nodes[c], w);
            });
        }

        function drawEdge(a, b, w) {
            const svg = document.getElementById('graph');
            const nodeA = document.getElementById(`node-${a}`);
            const nodeB = document.getElementById(`node-${b}`);
            const x1 = +nodeA.getAttribute('cx'), y1=+nodeA.getAttribute('cy');
            const x2 = +nodeB.getAttribute('cx'), y2=+nodeB.getAttribute('cy');
            const line = document.createElementNS('http://www.w3.org/2000/svg','line');
            line.setAttribute('x1',x1); line.setAttribute('y1',y1);
            line.setAttribute('x2',x2); line.setAttribute('y2',y2);
            line.setAttribute('stroke','#333'); line.setAttribute('stroke-width','2');
            line.id = `edge-${a}${b}`;
            svg.appendChild(line);
            const txt = document.createElementNS('http://www.w3.org/2000/svg','text');
            txt.setAttribute('x',(x1+x2)/2);
            txt.setAttribute('y',(y1+y2)/2 - 5);
            txt.setAttribute('text-anchor','middle');
            txt.textContent = w;
            txt.id = `label-${a}${b}`;
            svg.appendChild(txt);
            edgeElements[a+b] = {line, txt};
            // Matriz:
            const i = nodes.indexOf(a), j = nodes.indexOf(b);
            document.getElementById(`cell-${i}-${j}`).textContent = w;
            document.getElementById(`cell-${j}-${i}`).textContent = w;
        }

        function nextStep() {
            if (current < steps.length) {
                const {r, c, w} = steps[current];
                document.getElementById(`cell-${r}-${c}`).textContent = w;
                current++;
                if (current === steps.length) {
                    const btn = document.getElementById('nextBtn');
                    btn.textContent = 'Completado'; btn.disabled=true;
                }
            }
        }

        function resetMatrix() {
            current = 0;
            document.getElementById('nextBtn').textContent='Siguiente';
            document.getElementById('nextBtn').disabled=false;
            // Limpiar matriz y SVG dinámico
            initMatrix();
            // Remover aristas dinámicas
            Object.values(edgeElements).forEach(({line,txt})=>{
                line.remove(); txt.remove();
            });
            for (let k in edgeElements) delete edgeElements[k];
        }

        function addEdge() {
            const a = document.getElementById('fromNode').value;
            const b = document.getElementById('toNode').value;
            const w = document.getElementById('edgeWeight').value;
            if (!w || a===b) return;
            // Si existe, actualiza peso
            if (edgeElements[a+b]) {
                edgeElements[a+b].txt.textContent = w;
                document.getElementById(`cell-${nodes.indexOf(a)}-${nodes.indexOf(b)}`).textContent = w;
                document.getElementById(`cell-${nodes.indexOf(b)}-${nodes.indexOf(a)}`).textContent = w;
            } else {
                drawEdge(a,b,w);
            }
        }

        function removeEdge() {
            const a = document.getElementById('fromNode').value;
            const b = document.getElementById('toNode').value;
            const key = a+b;
            if (edgeElements[key]) {
                edgeElements[key].line.remove();
                edgeElements[key].txt.remove();
                delete edgeElements[key];
                document.getElementById(`cell-${nodes.indexOf(a)}-${nodes.indexOf(b)}`).textContent = '';
                document.getElementById(`cell-${nodes.indexOf(b)}-${nodes.indexOf(a)}`).textContent = '';
            }
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
