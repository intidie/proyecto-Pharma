import psycopg2
from psycopg2.extras import RealDictCursor
import os
from urllib.parse import urlparse
from datetime import datetime

class DatabaseManager:
    """Clase para gestionar todas las operaciones de la base de datos"""
    
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
    
    def get_connection(self):
        """Crear conexión a la base de datos"""
        try:
            if self.database_url:
                result = urlparse(self.database_url)
                conn = psycopg2.connect(
                    database=result.path[1:],
                    user=result.username,
                    password=result.password,
                    host=result.hostname,
                    port=result.port
                )
            else:
                # Conexión local para desarrollo
                conn = psycopg2.connect(
                    database="laboratorio",
                    user="postgres",
                    password="postgres",
                    host="localhost",
                    port="5432"
                )
            return conn
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None
    
 








    def init_database(self):
        """Inicializar las tablas de la base de datos"""
        conn = self.get_connection()
        if not conn:
            print("No se pudo conectar a la base de datos")
            return False
        
        try:
            cur = conn.cursor()
            
            # --- AGREGA ESTA LÍNEA AQUÍ PARA BORRAR LAS TABLAS VIEJAS ---
            cur.execute('DROP TABLE IF EXISTS mediciones_toc, mediciones_ph, mediciones_conductividad, mediciones_microbiologia CASCADE;')
            # -----------------------------------------------------------

   



            # Crear tabla TOC
            cur.execute('''
                CREATE TABLE IF NOT EXISTS mediciones_toc (
                    id SERIAL PRIMARY KEY,
                    fecha DATE NOT NULL,
                    dato DECIMAL(10, 2) NOT NULL,
                    pu VARCHAR(3) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notas TEXT
                )
            ''')
            
            # Crear tabla pH
            cur.execute('''
                CREATE TABLE IF NOT EXISTS mediciones_ph (
                    id SERIAL PRIMARY KEY,
                    fecha DATE NOT NULL,
                    dato DECIMAL(10, 2) NOT NULL,
                    pu VARCHAR(3) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notas TEXT
                )
            ''')
            
            # Crear tabla Conductividad
            cur.execute('''
                CREATE TABLE IF NOT EXISTS mediciones_conductividad (
                    id SERIAL PRIMARY KEY,
                    fecha DATE NOT NULL,
                    dato DECIMAL(10, 2) NOT NULL,
                    pu VARCHAR(3) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notas TEXT
                )
            ''')
            
            # Crear tabla Microbiología
            cur.execute('''
                CREATE TABLE IF NOT EXISTS mediciones_microbiologia (
                    id SERIAL PRIMARY KEY,
                    fecha DATE NOT NULL,
                    tipo VARCHAR(50) NOT NULL,
                    dato DECIMAL(10, 2) NOT NULL,
                    pu VARCHAR(3) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notas TEXT
                )
            ''')
            
            conn.commit()
            cur.close()
            conn.close()
            print("✓ Base de datos inicializada correctamente")
            return True
            
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")
            if conn:
                conn.close()
            return False
    
    def insertar_medicion(self, categoria, fecha, dato, pu, notas=None):
        """Insertar una nueva medición"""
        conn = self.get_connection()
        if not conn:
            return {'success': False, 'message': 'Error de conexión'}
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            tabla = f'mediciones_{categoria}'
            
            cur.execute(f'''
                INSERT INTO {tabla} (fecha, dato, pu, notas)
                VALUES (%s, %s, %s, %s)
                RETURNING id, fecha, dato, pu, timestamp, notas
            ''', (fecha, float(dato), pu, notas))
            
            nuevo_registro = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            
            return {
                'success': True,
                'message': '✓ Datos guardados correctamente',
                'data': dict(nuevo_registro)
            }
        except Exception as e:
            if conn:
                conn.close()
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def obtener_mediciones(self, categoria, limite=None):
        """Obtener mediciones de una categoría"""
        conn = self.get_connection()
        if not conn:
            return {'success': False, 'message': 'Error de conexión'}
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            tabla = f'mediciones_{categoria}'
            
            if limite:
                query = f'SELECT * FROM {tabla} ORDER BY fecha DESC, timestamp DESC LIMIT %s'
                cur.execute(query, (limite,))
            else:
                query = f'SELECT * FROM {tabla} ORDER BY fecha DESC, timestamp DESC'
                cur.execute(query)
            
            mediciones = cur.fetchall()
            cur.close()
            conn.close()
            
            return {
                'success': True,
                'data': [dict(m) for m in mediciones]
            }
        except Exception as e:
            if conn:
                conn.close()
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def obtener_estadisticas(self, categoria):
        """Obtener estadísticas de una categoría"""
        conn = self.get_connection()
        if not conn:
            return {'success': False, 'message': 'Error de conexión'}
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            tabla = f'mediciones_{categoria}'
            
            cur.execute(f'''
                SELECT 
                    COUNT(*) as total,
                    AVG(dato) as promedio,
                    MAX(dato) as maximo,
                    MIN(dato) as minimo,
                    STDDEV(dato) as desviacion_estandar
                FROM {tabla}
            ''')
            
            stats = cur.fetchone()
            cur.close()
            conn.close()
            
            return {
                'success': True,
                'data': dict(stats)
            }
        except Exception as e:
            if conn:
                conn.close()
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def eliminar_medicion(self, categoria, id):
        """Eliminar una medición por ID"""
        conn = self.get_connection()
        if not conn:
            return {'success': False, 'message': 'Error de conexión'}
        
        try:
            cur = conn.cursor()
            tabla = f'mediciones_{categoria}'
            
            cur.execute(f'DELETE FROM {tabla} WHERE id = %s', (id,))
            conn.commit()
            
            eliminados = cur.rowcount
            cur.close()
            conn.close()
            
            if eliminados > 0:
                return {'success': True, 'message': 'Registro eliminado'}
            else:
                return {'success': False, 'message': 'Registro no encontrado'}
        except Exception as e:
            if conn:
                conn.close()
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def limpiar_tabla(self, categoria):
        """Eliminar todos los registros de una tabla"""
        conn = self.get_connection()
        if not conn:
            return {'success': False, 'message': 'Error de conexión'}
        
        try:
            cur = conn.cursor()
            tabla = f'mediciones_{categoria}'
            
            cur.execute(f'DELETE FROM {tabla}')
            conn.commit()
            
            eliminados = cur.rowcount
            cur.close()
            conn.close()
            
            return {
                'success': True,
                'message': f'{eliminados} registros eliminados'
            }
        except Exception as e:
            if conn:
                conn.close()
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def insertar_lote(self, categoria, datos):
        """Insertar múltiples mediciones de una vez"""
        conn = self.get_connection()
        if not conn:
            return {'success': False, 'message': 'Error de conexión'}
        
        try:
            cur = conn.cursor()
            tabla = f'mediciones_{categoria}'
            registros_insertados = 0
            errores = []
            
            for dato in datos:
                try:
                    cur.execute(f'''
                        INSERT INTO {tabla} (fecha, dato, pu, notas)
                        VALUES (%s, %s, %s, %s)
                    ''', (dato['fecha'], float(dato['dato']), dato['pu'], dato.get('notas')))
                    registros_insertados += 1
                except Exception as e:
                    errores.append(f"Error en registro: {str(e)}")
                    continue
            
            conn.commit()
            cur.close()
            conn.close()
            
            mensaje = f'✓ {registros_insertados} registros insertados'
            if errores:
                mensaje += f' ({len(errores)} errores)'
            
            return {
                'success': True,
                'message': mensaje,
                'insertados': registros_insertados,
                'errores': len(errores)
            }
        except Exception as e:
            if conn:
                conn.close()
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def exportar_a_sql(self, categoria, archivo_salida):
        """Exportar datos a un archivo SQL"""
        conn = self.get_connection()
        if not conn:
            return {'success': False, 'message': 'Error de conexión'}
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            tabla = f'mediciones_{categoria}'
            
            cur.execute(f'SELECT * FROM {tabla} ORDER BY fecha, timestamp')
            mediciones = cur.fetchall()
            
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write(f"-- Exportación de {tabla}\n")
                f.write(f"-- Fecha: {datetime.now()}\n\n")
                
                for med in mediciones:
                    notas = f"'{med['notas']}'" if med.get('notas') else 'NULL'
                    f.write(f"INSERT INTO {tabla} (fecha, dato, pu, notas) VALUES ")
                    f.write(f"('{med['fecha']}', {med['dato']}, '{med['pu']}', {notas});\n")
            
            cur.close()
            conn.close()
            
            return {
                'success': True,
                'message': f'Datos exportados a {archivo_salida}',
                'registros': len(mediciones)
            }
        except Exception as e:
            if conn:
                conn.close()
            return {'success': False, 'message': f'Error: {str(e)}'}