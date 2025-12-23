from flask import Flask, request, jsonify
from flask_cors import CORS
from database import DatabaseManager
from importador import ImportadorDatos

app = Flask(__name__)
CORS(app)

# Inicializar gestores
db = DatabaseManager()
importador = ImportadorDatos(db)

# Inicializar la base de datos al inicio
db.init_database()

@app.route('/')
def index():
    """Ruta principal que sirve el HTML"""
    html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard de Laboratorio</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        h1 {
            text-align: center;
            color: white;
            margin-bottom: 40px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            animation: fadeInDown 0.8s ease;
        }

        .import-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        .import-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid #667eea;
        }

        .import-title {
            font-size: 1.5em;
            color: #333;
            font-weight: 600;
        }

        .upload-area {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .upload-box {
            border: 2px dashed #667eea;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            background: #f5f7fa;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .upload-box:hover {
            border-color: #764ba2;
            background: #e8ebf5;
        }

        .upload-box input[type="file"] {
            display: none;
        }

        .upload-icon {
            font-size: 3em;
            margin-bottom: 10px;
        }

        .upload-text {
            color: #555;
            margin-bottom: 10px;
        }

        .select-categoria {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
            margin-top: 10px;
        }

        .main-sections {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }

        .section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            animation: fadeInUp 0.8s ease;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .section:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }

        .section-header {
            display: flex;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid #667eea;
        }

        .section-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            font-size: 24px;
        }

        .section-title {
            font-size: 1.8em;
            color: #333;
            font-weight: 600;
        }

        .subsections {
            display: grid;
            gap: 20px;
        }

        .subsection {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            padding: 25px;
            animation: slideIn 0.6s ease;
            transition: all 0.3s ease;
        }

        .subsection:hover {
            transform: scale(1.02);
        }

        .subsection-title {
            font-size: 1.3em;
            color: #764ba2;
            margin-bottom: 20px;
            font-weight: 600;
            display: flex;
            align-items: center;
        }

        .subsection-title::before {
            content: "▸";
            margin-right: 10px;
            font-size: 1.2em;
        }

        .form-group {
            margin-bottom: 15px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
            font-size: 0.95em;
        }

        input[type="date"],
        input[type="number"],
        input[type="text"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
            transition: all 0.3s ease;
            background: white;
        }

        input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .tooltip {
            position: relative;
            display: inline-block;
            margin-left: 8px;
            cursor: help;
        }

        .tooltip-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 20px;
            height: 20px;
            background: #667eea;
            color: white;
            border-radius: 50%;
            font-size: 12px;
            font-weight: bold;
        }

        .tooltip-text {
            visibility: hidden;
            width: 200px;
            background-color: #333;
            color: white;
            text-align: center;
            border-radius: 6px;
            padding: 8px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 0.85em;
        }

        .tooltip-text::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #333 transparent transparent transparent;
        }

        .tooltip:hover .tooltip-text {
            visibility: visible;
            opacity: 1;
        }

        .submit-btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .empty-section {
            text-align: center;
            padding: 40px;
            color: #999;
            font-style: italic;
        }

        .alert {
            padding: 15px;
            margin-top: 15px;
            border-radius: 8px;
            display: none;
        }

        .alert.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .alert.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        @media (max-width: 768px) {
            .main-sections { grid-template-columns: 1fr; }
            h1 { font-size: 1.8em; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔬 Dashboard de Laboratorio</h1>
        
        <!-- Sección de importación -->
        <div class="import-section">
            <div class="import-header">
                <h2 class="import-title">📤 Importar Datos desde Archivo</h2>
            </div>
            <div class="upload-area">
                <div class="upload-box" onclick="document.getElementById('file-excel').click()">
                    <div class="upload-icon">📊</div>
                    <div class="upload-text"><strong>Subir Excel (.xlsx, .xls)</strong></div>
                    <input type="file" id="file-excel" accept=".xlsx,.xls" onchange="handleFileUpload(this, 'excel')">
                    <select id="categoria-excel" class="select-categoria">
                        <option value="">Seleccionar categoría</option>
                        <option value="toc">TOC</option>
                        <option value="ph">pH</option>
                        <option value="conductividad">Conductividad</option>
                    </select>
                    <p style="font-size: 0.85em; color: #666; margin-top: 10px;">
                        Formato: fecha | dato | pu
                    </p>
                </div>
                
                <div class="upload-box" onclick="document.getElementById('file-txt').click()">
                    <div class="upload-icon">📄</div>
                    <div class="upload-text"><strong>Subir TXT (.txt, .csv)</strong></div>
                    <input type="file" id="file-txt" accept=".txt,.csv" onchange="handleFileUpload(this, 'txt')">
                    <select id="categoria-txt" class="select-categoria">
                        <option value="">Seleccionar categoría</option>
                        <option value="toc">TOC</option>
                        <option value="ph">pH</option>
                        <option value="conductividad">Conductividad</option>
                    </select>
                    <p style="font-size: 0.85em; color: #666; margin-top: 10px;">
                        Formato: fecha,dato,pu (separado por comas)
                    </p>
                </div>
            </div>
            <div id="alert-import" class="alert"></div>
        </div>
        
        <div class="main-sections">
            <div class="section">
                <div class="section-header">
                    <div class="section-icon">⚗️</div>
                    <h2 class="section-title">Fisicoquímica</h2>
                </div>
                
                <div class="subsections">
                    <div class="subsection">
                        <h3 class="subsection-title">TOC (Carbono Orgánico Total)</h3>
                        <form id="form-toc">
                            <div class="form-group">
                                <label for="toc-fecha">Fecha:</label>
                                <input type="date" id="toc-fecha" name="fecha" required>
                            </div>
                            <div class="form-group">
                                <label for="toc-dato">Dato:</label>
                                <input type="number" id="toc-dato" name="dato" step="0.01" placeholder="Ingrese el valor" required>
                            </div>
                            <div class="form-group">
                                <label for="toc-pu">
                                    Pu:
                                    <span class="tooltip">
                                        <span class="tooltip-icon">?</span>
                                        <span class="tooltip-text">Seleccione del 001 al 007</span>
                                    </span>
                                </label>
                                <input type="text" id="toc-pu" name="pu" placeholder="001-007" maxlength="3" required>
                            </div>
                            <button type="submit" class="submit-btn">Guardar Datos TOC</button>
                            <div id="alert-toc" class="alert"></div>
                        </form>
                    </div>

                    <div class="subsection">
                        <h3 class="subsection-title">pH</h3>
                        <form id="form-ph">
                            <div class="form-group">
                                <label for="ph-fecha">Fecha:</label>
                                <input type="date" id="ph-fecha" name="fecha" required>
                            </div>
                            <div class="form-group">
                                <label for="ph-dato">Dato:</label>
                                <input type="number" id="ph-dato" name="dato" step="0.01" placeholder="Ingrese el valor" required>
                            </div>
                            <div class="form-group">
                                <label for="ph-pu">
                                    Pu:
                                    <span class="tooltip">
                                        <span class="tooltip-icon">?</span>
                                        <span class="tooltip-text">Seleccione del 001 al 007</span>
                                    </span>
                                </label>
                                <input type="text" id="ph-pu" name="pu" placeholder="001-007" maxlength="3" required>
                            </div>
                            <button type="submit" class="submit-btn">Guardar Datos pH</button>
                            <div id="alert-ph" class="alert"></div>
                        </form>
                    </div>

                    <div class="subsection">
                        <h3 class="subsection-title">Conductividad</h3>
                        <form id="form-cond">
                            <div class="form-group">
                                <label for="cond-fecha">Fecha:</label>
                                <input type="date" id="cond-fecha" name="fecha" required>
                            </div>
                            <div class="form-group">
                                <label for="cond-dato">Dato:</label>
                                <input type="number" id="cond-dato" name="dato" step="0.01" placeholder="Ingrese el valor" required>
                            </div>
                            <div class="form-group">
                                <label for="cond-pu">
                                    Pu:
                                    <span class="tooltip">
                                        <span class="tooltip-icon">?</span>
                                        <span class="tooltip-text">Seleccione del 001 al 007</span>
                                    </span>
                                </label>
                                <input type="text" id="cond-pu" name="pu" placeholder="001-007" maxlength="3" required>
                            </div>
                            <button type="submit" class="submit-btn">Guardar Datos Conductividad</button>
                            <div id="alert-cond" class="alert"></div>
                        </form>
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="section-header">
                    <div class="section-icon">🦠</div>
                    <h2 class="section-title">Microbiología</h2>
                </div>
                <div class="empty-section">
                    <p>Esta sección estará disponible próximamente...</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        function validarPu(valor) {
            const num = parseInt(valor);
            return valor.length === 3 && !isNaN(num) && num >= 1 && num <= 7;
        }

        function mostrarAlerta(id, mensaje, tipo) {
            const alert = document.getElementById(id);
            alert.textContent = mensaje;
            alert.className = `alert ${tipo}`;
            alert.style.display = 'block';
            setTimeout(() => { alert.style.display = 'none'; }, 5000);
        }

        async function handleFileUpload(input, tipo) {
            const file = input.files[0];
            if (!file) return;

            const categoriaId = tipo === 'excel' ? 'categoria-excel' : 'categoria-txt';
            const categoria = document.getElementById(categoriaId).value;

            if (!categoria) {
                mostrarAlerta('alert-import', 'Por favor selecciona una categoría', 'error');
                input.value = '';
                return;
            }

            const formData = new FormData();
            formData.append('file', file);
            formData.append('categoria', categoria);
            formData.append('tipo', tipo);

            mostrarAlerta('alert-import', '⏳ Procesando archivo...', 'success');

            try {
                const response = await fetch('/api/importar', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                
                if (result.success) {
                    mostrarAlerta('alert-import', `✓ ${result.message}`, 'success');
                } else {
                    mostrarAlerta('alert-import', result.message, 'error');
                }
            } catch (error) {
                mostrarAlerta('alert-import', 'Error al importar archivo', 'error');
            }

            input.value = '';
        }

        async function enviarDatos(categoria, formData) {
            try {
                const response = await fetch('/api/guardar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        categoria: categoria,
                        fecha: formData.get('fecha'),
                        dato: formData.get('dato'),
                        pu: formData.get('pu')
                    })
                });
                return await response.json();
            } catch (error) {
                return { success: false, message: 'Error de conexión' };
            }
        }

        document.getElementById('form-toc').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            if (!validarPu(formData.get('pu'))) {
                mostrarAlerta('alert-toc', 'El Pu debe ser entre 001 y 007', 'error');
                return;
            }
            const result = await enviarDatos('toc', formData);
            mostrarAlerta('alert-toc', result.message, result.success ? 'success' : 'error');
            if (result.success) {
                this.reset();
                document.getElementById('toc-fecha').value = new Date().toISOString().split('T')[0];
            }
        });

        document.getElementById('form-ph').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            if (!validarPu(formData.get('pu'))) {
                mostrarAlerta('alert-ph', 'El Pu debe ser entre 001 y 007', 'error');
                return;
            }
            const result = await enviarDatos('ph', formData);
            mostrarAlerta('alert-ph', result.message, result.success ? 'success' : 'error');
            if (result.success) {
                this.reset();
                document.getElementById('ph-fecha').value = new Date().toISOString().split('T')[0];
            }
        });

        document.getElementById('form-cond').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            if (!validarPu(formData.get('pu'))) {
                mostrarAlerta('alert-cond', 'El Pu debe ser entre 001 y 007', 'error');
                return;
            }
            const result = await enviarDatos('conductividad', formData);
            mostrarAlerta('alert-cond', result.message, result.success ? 'success' : 'error');
            if (result.success) {
                this.reset();
                document.getElementById('cond-fecha').value = new Date().toISOString().split('T')[0];
            }
        });

        const hoy = new Date().toISOString().split('T')[0];
        document.getElementById('toc-fecha').value = hoy;
        document.getElementById('ph-fecha').value = hoy;
        document.getElementById('cond-fecha').value = hoy;
    </script>
</body>
</html>'''
    return html_content

@app.route('/api/importar', methods=['POST'])
def importar_datos():
    """Endpoint para importar datos desde Excel o TXT"""
    try:
        file = request.files.get('file')
        categoria = request.form.get('categoria')
        tipo = request.form.get('tipo')
        
        if not file or not categoria:
            return jsonify({'success': False, 'message': 'Archivo o categoría no proporcionados'}), 400
        
        categorias_validas = ['toc', 'ph', 'conductividad']
        if categoria not in categorias_validas:
            return jsonify({'success': False, 'message': 'Categoría no válida'}), 400
        
        # Procesar según el tipo de archivo
        if tipo == 'excel':
            resultado = importador.procesar_excel(file, categoria)
        else:  # txt o csv
            resultado = importador.procesar_txt(file, categoria)
        
        if resultado['success']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 400
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al importar: {str(e)}'}), 500

@app.route('/api/guardar', methods=['POST'])
def guardar_medicion():
    """Endpoint para guardar una nueva medición"""
    try:
        datos_request = request.json
        categoria = datos_request.get('categoria', '').lower()
        fecha = datos_request.get('fecha')
        dato = datos_request.get('dato')
        pu = datos_request.get('pu')
        
        categorias_validas = ['toc', 'ph', 'conductividad']
        if categoria not in categorias_validas:
            return jsonify({'success': False, 'message': 'Categoría no válida'}), 400
        
        try:
            pu_num = int(pu)
            if not (1 <= pu_num <= 7) or len(pu) != 3:
                raise ValueError()
        except:
            return jsonify({'success': False, 'message': 'El Pu debe estar entre 001 y 007'}), 400
        
        resultado = db.insertar_medicion(categoria, fecha, dato, pu)
        
        if resultado['success']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/obtener/<categoria>', methods=['GET'])
def obtener_mediciones(categoria):
    """Obtener todas las mediciones de una categoría"""
    try:
        categoria = categoria.lower()
        if categoria not in ['toc', 'ph', 'conductividad']:
            return jsonify({'success': False, 'message': 'Categoría no válida'}), 400
        
        resultado = db.obtener_mediciones(categoria)
        
        if resultado['success']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/estadisticas/<categoria>', methods=['GET'])
def obtener_estadisticas(categoria):
    """Obtener estadísticas de una categoría"""
    try:
        categoria = categoria.lower()
        if categoria not in ['toc', 'ph', 'conductividad']:
            return jsonify({'success': False, 'message': 'Categoría no válida'}), 400
        
        resultado = db.obtener_estadisticas(categoria)
        
        if resultado['success']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Verificar estado del servidor y conexión a BD"""
    try:
        conn = db.get_connection()
        if conn:
            conn.close()
            db_status = "conectada"
        else:
            db_status = "desconectada"
        
        return jsonify({
            'status': 'OK',
            'message': 'Servidor funcionando',
            'database': db_status
        })
    except:
        return jsonify({'status': 'OK', 'database': 'error'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    
    print("=" * 60)
    print("🚀 SERVIDOR INICIADO")
    print(f"📍 Puerto: {port}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=False)