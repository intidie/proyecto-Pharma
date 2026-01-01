from flask import Flask, request, jsonify
from flask_cors import CORS
from database import DatabaseManager
from importador import ImportadorDatos
import os

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
    <title>APP HTTP - Laboratorio</title>
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
        }
    </style>
</head>
<body>
    <div id="root"></div>
    <script>
        // Aquí iría el código React compilado
        // Por ahora, usaremos una interfaz HTML simple
        window.location.href = '/dashboard';
    </script>
</body>
</html>'''
    return html_content

@app.route('/dashboard')
def dashboard():
    """Dashboard principal con interfaz completa"""
    return '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APP HTTP - Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .sidebar-transition { transition: width 0.3s ease; }
        .slide-button {
            position: fixed;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            z-index: 1000;
        }
    </style>
</head>
<body class="bg-gray-50">
    <div id="app" class="flex h-screen">
        <!-- Sidebar -->
        <div id="sidebar" class="sidebar-transition w-80 bg-white border-r border-gray-200 overflow-hidden">
            <div class="p-6 border-b border-gray-200">
                <div class="flex items-center justify-between">
                    <h1 class="text-xl font-semibold text-gray-800">APP HTTP</h1>
                    <button onclick="toggleSidebar()" class="p-2 hover:bg-gray-100 rounded-lg">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
            
            <div class="p-4 overflow-y-auto" style="height: calc(100vh - 80px);">
                <!-- Menú principal -->
                <div class="space-y-1 mb-6">
                    <button onclick="showView('home')" class="w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-gray-700 hover:bg-gray-100">
                        <i class="fas fa-home"></i>
                        <span class="font-medium">Inicio</span>
                    </button>
                    <button onclick="showView('import')" class="w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-gray-700 hover:bg-gray-100">
                        <i class="fas fa-upload"></i>
                        <span class="font-medium">Importar Datos</span>
                    </button>
                    <button onclick="showView('export')" class="w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-gray-700 hover:bg-gray-100">
                        <i class="fas fa-download"></i>
                        <span class="font-medium">Exportar Datos</span>
                    </button>
                    <button onclick="showView('database')" class="w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-gray-700 hover:bg-gray-100">
                        <i class="fas fa-database"></i>
                        <span class="font-medium">Base de Datos</span>
                    </button>
                </div>

                <div class="border-t border-gray-200 pt-4">
                    <h3 class="text-xs font-semibold text-gray-500 uppercase mb-3 px-2">Puntos de Muestreo</h3>
                    
                    <!-- Fisicoquímica -->
                    <div class="mb-2">
                        <button onclick="toggleSection('fisicoquimica')" class="w-full flex items-center justify-between px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg">
                            <div class="flex items-center gap-2">
                                <i class="fas fa-flask text-blue-600"></i>
                                <span>Fisicoquímica</span>
                            </div>
                            <i class="fas fa-chevron-down" id="icon-fisicoquimica"></i>
                        </button>
                        <div id="section-fisicoquimica" class="hidden ml-4 mt-1 space-y-1">
                            <!-- Vapor -->
                            <div class="mb-2">
                                <button onclick="toggleSection('vapor')" class="w-full flex items-center justify-between px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg">
                                    <div class="flex items-center gap-2">
                                        <i class="fas fa-wind text-orange-500" style="font-size: 0.875rem;"></i>
                                        <span>Vapor</span>
                                    </div>
                                    <i class="fas fa-chevron-right text-sm" id="icon-vapor"></i>
                                </button>
                                <div id="section-vapor" class="hidden ml-6 mt-1 space-y-1">
                                    <!-- Puntos PMV -->
                                </div>
                            </div>
                            
                            <!-- Agua -->
                            <div class="mb-2">
                                <button onclick="toggleSection('agua')" class="w-full flex items-center justify-between px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg">
                                    <div class="flex items-center gap-2">
                                        <i class="fas fa-droplet text-blue-500" style="font-size: 0.875rem;"></i>
                                        <span>Agua</span>
                                    </div>
                                    <i class="fas fa-chevron-right text-sm" id="icon-agua"></i>
                                </button>
                                <div id="section-agua" class="hidden ml-6 mt-1 space-y-1">
                                    <!-- Puntos PA -->
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Microbiología -->
                    <div class="mb-2">
                        <button onclick="toggleSection('microbiologia')" class="w-full flex items-center justify-between px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg">
                            <div class="flex items-center gap-2">
                                <i class="fas fa-bacteria text-green-600"></i>
                                <span>Microbiología</span>
                            </div>
                            <i class="fas fa-chevron-down" id="icon-microbiologia"></i>
                        </button>
                        <div id="section-microbiologia" class="hidden ml-6 mt-1 space-y-1">
                            <button onclick="showCategoryForm('nitrogeno', 'microbiologia')" class="w-full px-3 py-2 text-xs text-gray-600 hover:bg-gray-50 rounded-lg text-left">
                                Nitrógeno
                            </button>
                            <button onclick="showCategoryForm('aire_comprimido', 'microbiologia')" class="w-full px-3 py-2 text-xs text-gray-600 hover:bg-gray-50 rounded-lg text-left">
                                Aire comprimido
                            </button>
                            <button onclick="showCategoryForm('vapor_micro', 'microbiologia')" class="w-full px-3 py-2 text-xs text-gray-600 hover:bg-gray-50 rounded-lg text-left">
                                Vapor
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Botón slide -->
        <button id="slideButton" onclick="toggleSidebar()" class="slide-button hidden bg-blue-600 text-white p-3 rounded-r-lg shadow-lg hover:bg-blue-700">
            <i class="fas fa-bars"></i>
        </button>

        <!-- Contenido principal -->
        <div class="flex-1 flex flex-col overflow-hidden">
            <header class="bg-white border-b border-gray-200 px-6 py-4">
                <div class="flex items-center justify-between">
                    <h2 id="pageTitle" class="text-xl font-semibold text-gray-800">Panel Principal</h2>
                    <div class="flex items-center gap-2">
                        <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                        <span class="text-sm text-gray-600">Conectado</span>
                    </div>
                </div>
            </header>

            <main id="mainContent" class="flex-1 overflow-y-auto p-6">
                <!-- Contenido dinámico -->
                <div id="homeView">
                    <div class="max-w-6xl mx-auto">
                        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                            <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                                <div class="flex items-center justify-between mb-4">
                                    <h3 class="text-sm font-semibold text-gray-800">Vapor</h3>
                                    <i class="fas fa-wind text-orange-500"></i>
                                </div>
                                <p class="text-2xl font-bold text-gray-900">8</p>
                                <p class="text-xs text-gray-600 mt-1">Puntos PMV</p>
                            </div>
                            <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                                <div class="flex items-center justify-between mb-4">
                                    <h3 class="text-sm font-semibold text-gray-800">Agua</h3>
                                    <i class="fas fa-droplet text-blue-500"></i>
                                </div>
                                <p class="text-2xl font-bold text-gray-900">18</p>
                                <p class="text-xs text-gray-600 mt-1">Puntos PA</p>
                            </div>
                            <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                                <div class="flex items-center justify-between mb-4">
                                    <h3 class="text-sm font-semibold text-gray-800">Microbiología</h3>
                                    <i class="fas fa-bacteria text-green-600"></i>
                                </div>
                                <p class="text-2xl font-bold text-gray-900">3</p>
                                <p class="text-xs text-gray-600 mt-1">Categorías</p>
                            </div>
                            <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                                <div class="flex items-center justify-between mb-4">
                                    <h3 class="text-sm font-semibold text-gray-800">Total</h3>
                                    <i class="fas fa-database text-purple-600"></i>
                                </div>
                                <p class="text-2xl font-bold text-gray-900">26</p>
                                <p class="text-xs text-gray-600 mt-1">Puntos totales</p>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>

    <script>
        let sidebarOpen = true;
        
        const estructuraData = {
            vapor: {
                PMV001: ['PH', 'CONDUCTIVIDAD', 'CLORO', 'DUREZA', 'COLOR', 'TURBIDEZ', 'HIERRO', 'SOLIDOS', 'SULFATOS'],
                PMV002: ['PH', 'CONDUCTIVIDAD', 'CLORO', 'DUREZA', 'COLOR', 'TURBIDEZ', 'HIERRO', 'SOLIDOS', 'SULFATOS'],
                PMV003: ['DUREZA', 'HIERRO', 'SULFATOS'],
                PMV004: ['CONDUCTIVIDAD', 'CLORO'],
                PMV005: ['PH', 'CONDUCTIVIDAD'],
                PMV006: ['PH', 'CONDUCTIVIDAD'],
                PMV007: ['CONDUCTIVIDAD', 'TOC'],
                PMV008: ['CONDUCTIVIDAD', 'TOC']
            },
            agua: {
                PA001: ['TOC', 'PH', 'CONDUCTIVIDAD'],
                PA002: ['PH', 'CONDUCTIVIDAD', 'TOC'],
                PA003: ['CONDUCTIVIDAD', 'PH', 'TOC'],
                PA004: ['COLOR', 'TURBIDEZ', 'TOC', 'PH', 'CONDUCTIVIDAD'],
                PA005: ['DUREZA', 'HIERRO', 'SULFATOS', 'TOC', 'PH', 'CONDUCTIVIDAD'],
                PA006: ['PH', 'CONDUCTIVIDAD', 'CLORO', 'DUREZA', 'COLOR', 'TURBIDEZ', 'HIERRO', 'SOLIDOS TOTALES', 'SULFATOS', 'TOC'],
                PA007: ['PH', 'CONDUCTIVIDAD', 'TOC'],
                PA008: ['PH', 'CONDUCTIVIDAD', 'CLORO', 'TOC'],
                PA009: ['PH', 'CONDUCTIVIDAD', 'TOC'],
                PA010: ['PH', 'CONDUCTIVIDAD', 'TOC'],
                PA011: ['PH', 'CONDUCTIVIDAD', 'TOC'],
                PA012: ['TOC', 'PH', 'CONDUCTIVIDAD'],
                PA013: ['PH', 'CONDUCTIVIDAD', 'TOC'],
                PA014: ['PH', 'CONDUCTIVIDAD', 'TOC'],
                PA015: ['PH', 'CONDUCTIVIDAD', 'TOC'],
                PA016: ['PH', 'CONDUCTIVIDAD', 'TOC'],
                PA017: ['PH', 'CONDUCTIVIDAD', 'TOC'],
                PA018: ['PH', 'CONDUCTIVIDAD', 'TOC']
            }
        };

        function toggleSidebar() {
            sidebarOpen = !sidebarOpen;
            const sidebar = document.getElementById('sidebar');
            const slideButton = document.getElementById('slideButton');
            
            if (sidebarOpen) {
                sidebar.classList.remove('w-0');
                sidebar.classList.add('w-80');
                slideButton.classList.add('hidden');
            } else {
                sidebar.classList.remove('w-80');
                sidebar.classList.add('w-0');
                slideButton.classList.remove('hidden');
            }
        }

        function toggleSection(section) {
            const sectionEl = document.getElementById('section-' + section);
            const icon = document.getElementById('icon-' + section);
            
            if (sectionEl.classList.contains('hidden')) {
                sectionEl.classList.remove('hidden');
                icon.classList.remove('fa-chevron-right');
                icon.classList.add('fa-chevron-down');
            } else {
                sectionEl.classList.add('hidden');
                icon.classList.remove('fa-chevron-down');
                icon.classList.add('fa-chevron-right');
            }
        }

        function showParameterForm(punto, parametro, tipo) {
            document.getElementById('pageTitle').textContent = parametro + ' - ' + punto;
            document.getElementById('mainContent').innerHTML = `
                <div class="max-w-2xl mx-auto">
                    <div class="bg-white rounded-xl border border-gray-200 p-8">
                        <div class="mb-6">
                            <div class="flex items-center gap-3 mb-2">
                                <span class="px-3 py-1 rounded-full text-sm font-medium ${
                                    tipo === 'vapor' ? 'bg-orange-100 text-orange-700' :
                                    tipo === 'agua' ? 'bg-blue-100 text-blue-700' :
                                    'bg-green-100 text-green-700'
                                }">${punto}</span>
                                <i class="fas fa-chevron-right text-gray-400"></i>
                                <span class="text-lg font-semibold text-gray-800">${parametro}</span>
                            </div>
                        </div>

                        <form onsubmit="submitForm(event, '${punto}', '${parametro}', '${tipo}')" class="space-y-6">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Fecha de medición</label>
                                <input type="date" id="fecha" required 
                                    value="${new Date().toISOString().split('T')[0]}"
                                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Valor (${parametro})</label>
                                <input type="text" id="dato" required placeholder="Ej: 150.5"
                                    oninput="validateNumber(this)"
                                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                                <p class="mt-1 text-xs text-gray-500">Use punto (.) para decimales. No se permiten comas.</p>
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Notas (opcional)</label>
                                <textarea id="nota" rows="3" placeholder="Agregar observaciones..."
                                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"></textarea>
                            </div>

                            <div class="flex gap-3">
                                <button type="button" onclick="showView('home')"
                                    class="flex-1 px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium">
                                    Cancelar
                                </button>
                                <button type="submit"
                                    class="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium">
                                    Guardar Datos
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            `;
        }

        function validateNumber(input) {
            let value = input.value;
            value = value.replace(/,/g, '.');
            value = value.replace(/[^0-9.]/g, '');
            const parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }
            input.value = value;
        }

        async function submitForm(event, punto, parametro, tipo) {
            event.preventDefault();
            
            const fecha = document.getElementById('fecha').value;
            const dato = document.getElementById('dato').value;
            const nota = document.getElementById('nota').value;

            const data = {
                punto: punto,
                parametro: parametro,
                tipo: tipo,
                fecha: fecha,
                dato: parseFloat(dato),
                nota: nota
            };

            try {
                const response = await fetch('/api/guardar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                
                if (result.success) {
                    alert('✓ Datos guardados correctamente');
                    showView('home');
                } else {
                    alert('Error: ' + result.message);
                }
            } catch (error) {
                alert('Error de conexión: ' + error.message);
            }
        }

        function showView(view) {
            document.getElementById('pageTitle').textContent = 
                view === 'home' ? 'Panel Principal' :
                view === 'import' ? 'Importar Datos' :
                view === 'export' ? 'Exportar Datos' :
                'Base de Datos';
            
            // Implementar otras vistas aquí
        }

        // Cargar puntos al iniciar
        window.onload = function() {
            // Cargar vapor
            const vaporSection = document.getElementById('section-vapor');
            Object.keys(estructuraData.vapor).forEach(punto => {
                const div = document.createElement('div');
                div.innerHTML = `
                    <button onclick="toggleSection('${punto}')" class="w-full flex items-center justify-between px-3 py-2 text-sm rounded-lg text-gray-600 hover:bg-gray-50">
                        <span class="font-mono text-xs">${punto}</span>
                        <i class="fas fa-chevron-right text-xs" id="icon-${punto}"></i>
                    </button>
                    <div id="section-${punto}" class="hidden ml-4 mt-1 space-y-1 border-l-2 border-orange-200 pl-3">
                        ${estructuraData.vapor[punto].map(param => `
                            <button onclick="showParameterForm('${punto}', '${param}', 'vapor')"
                                class="w-full text-left text-xs text-gray-600 py-1.5 px-2 hover:bg-orange-50 hover:text-orange-600 rounded flex items-center justify-between group">
                                <span>${param}</span>
                                <i class="fas fa-plus text-xs opacity-0 group-hover:opacity-100"></i>
                            </button>
                        `).join('')}
                    </div>
                `;
                vaporSection.appendChild(div);
            });

            // Cargar agua
            const aguaSection = document.getElementById('section-agua');
            Object.keys(estructuraData.agua).forEach(punto => {
                const div = document.createElement('div');
                div.innerHTML = `
                    <button onclick="toggleSection('${punto}')" class="w-full flex items-center justify-between px-3 py-2 text-sm rounded-lg text-gray-600 hover:bg-gray-50">
                        <span class="font-mono text-xs">${punto}</span>
                        <i class="fas fa-chevron-right text-xs" id="icon-${punto}"></i>
                    </button>
                    <div id="section-${punto}" class="hidden ml-4 mt-1 space-y-1 border-l-2 border-blue-200 pl-3">
                        ${estructuraData.agua[punto].map(param => `
                            <button onclick="showParameterForm('${punto}', '${param}', 'agua')"
                                class="w-full text-left text-xs text-gray-600 py-1.5 px-2 hover:bg-blue-50 hover:text-blue-600 rounded flex items-center justify-between group">
                                <span>${param}</span>
                                <i class="fas fa-plus text-xs opacity-0 group-hover:opacity-100"></i>
                            </button>
                        `).join('')}
                    </div>
                `;
                aguaSection.appendChild(div);
            });
        };
    </script>
</body>
</html>'''

@app.route('/api/guardar', methods=['POST'])
def guardar_medicion():
    """Endpoint para guardar una nueva medición"""
    try:
        datos = request.json
        punto = datos.get('punto')
        parametro = datos.get('parametro')
        tipo = datos.get('tipo')
        fecha = datos.get('fecha')
        dato = datos.get('dato')
        nota = datos.get('nota')
        
        # Determinar la tabla según el tipo
        if tipo in ['vapor', 'agua']:
            categoria = 'fisicoquimica'
        else:
            categoria = 'microbiologia'
        
        resultado = db.insertar_medicion(
            categoria=categoria,
            tipo=tipo,
            punto=punto,
            parametro=parametro,
            fecha=fecha,
            dato=dato,
            nota=nota
        )
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/importar', methods=['POST'])
def importar_datos():
    """Endpoint para importar datos desde Excel o TXT"""
    try:
        file = request.files.get('file')
        categoria = request.form.get('categoria')
        tipo = request.form.get('tipo')
        
        if not file or not categoria:
            return jsonify({'success': False, 'message': 'Archivo o categoría no proporcionados'}), 400
        
        if tipo == 'excel':
            resultado = importador.procesar_excel(file, categoria)
        else:
            resultado = importador.procesar_txt(file, categoria)
        
        if resultado['success']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 400
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/obtener/<categoria>', methods=['GET'])
def obtener_mediciones(categoria):
    """Obtener todas las mediciones de una categoría"""
    try:
        resultado = db.obtener_mediciones(categoria)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/estadisticas/<categoria>', methods=['GET'])
def obtener_estadisticas(categoria):
    """Obtener estadísticas de una categoría"""
    try:
        resultado = db.obtener_estadisticas(categoria)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Verificar estado del servidor"""
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
    port = int(os.environ.get('PORT', 5000))
    
    print("=" * 60)
    print("🚀 SERVIDOR INICIADO")
    print(f"📍 Puerto: {port}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=False)