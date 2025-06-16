from flask import Flask

app = Flask(__name__)

# Página HTML con SVG, estilo y JavaScript interactivo.
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
            max-width: 800px;
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
            margin-top: 20px;
            padding: 10px 20px;
            font-size: 16px;
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
    </style>
</head>
<body>
    <h1>Grafo y Matriz de Adyacencia</h1>
    <div class="container">
        <!-- Dibujo del grafo con SVG -->
        <svg viewBox="0 0 300 200">
            <!-- Nodos -->
            <circle cx="60" cy="140" r="20" fill="#f56565" />
            <text x="60" y="140" text-anchor="middle" dy=".3em" fill="#fff">A</text>

            <circle cx="60" cy="40" r="20" fill="#48bb78" />
            <text x="60" y="40" text-anchor="middle" dy=".3em" fill="#fff">B</text>

            <circle cx="240" cy="40" r="20" fill="#4299e1" />
            <text x="240" y="40" text-anchor="middle" dy=".3em" fill="#fff">C</text>

            <circle cx="240" cy="140" r="20" fill="#ed8936" />
            <text x="240" y="140" text-anchor="middle" dy=".3em" fill="#fff">D</text>

            <!-- Aristas y etiquetas de peso -->
            <line x1="60" y1="140" x2="60" y2="40" stroke="#333" stroke-width="2" />
            <text x="55" y="90" text-anchor="end" dy=".3em">1</text>

            <line x1="60" y1="140" x2="240" y2="140" stroke="#333" stroke-width="2" />
            <text x="150" y="130" text-anchor="middle" dy=".3em">2</text>

            <line x1="60" y1="40" x2="240" y2="40" stroke="#333" stroke-width="2" />
            <text x="150" y="30" text-anchor="middle" dy=".3em">3</text>

            <line x1="60" y1="140" x2="240" y2="40" stroke="#333" stroke-width="2" />
            <text x="150" y="100" text-anchor="middle" dy=".3em">-4</text>
        </svg>

        <!-- Matriz de adyacencia -->
        <table id="matrix"></table>
        <button id="nextBtn" onclick="nextStep()">Siguiente</button>
    </div>

    <script>
        // Definición de nodos y secuencia de llenado
        const nodes = ['A','B','C','D'];
        const steps = [
            /* fila A */ {r:0, c:0, w:0}, {r:0, c:1, w:1}, {r:0, c:2, w:-4}, {r:0, c:3, w:2},
            /* fila B */ {r:1, c:0, w:1}, {r:1, c:1, w:0}, {r:1, c:2, w:3}, {r:1, c:3, w:0},
            /* fila C */ {r:2, c:0, w:-4}, {r:2, c:1, w:3}, {r:2, c:2, w:0}, {r:2, c:3, w:0},
            /* fila D */ {r:3, c:0, w:2}, {r:3, c:1, w:0}, {r:3, c:2, w:0}, {r:3, c:3, w:0}
        ];
        let current = 0;
        
        // Construir la tabla al cargar
        window.onload = () => {
            const table = document.getElementById('matrix');
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
        };

        // Función para avanzar un paso
        function nextStep() {
            if (current < steps.length) {
                const {r, c, w} = steps[current];
                document.getElementById(`cell-${r}-${c}`).textContent = w;
                current++;
                if (current === steps.length) {
                    const btn = document.getElementById('nextBtn');
                    btn.textContent = 'Completado';
                    btn.disabled = true;
                }
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
    # Ejecuta el servidor en http://localhost:5000
    app.run(debug=True)
