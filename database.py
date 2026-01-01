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
            
            # Tabla principal para fisicoquímica
            cur.execute('''
                CREATE TABLE IF NOT EXISTS mediciones_fisicoquimica (
                    id SERIAL PRIMARY KEY,
                        tipo VARCHAR(20) NOT NULL,
                punto VARCHAR(20) NOT NULL,
                parametro VARCHAR(50) NOT NULL,
                fecha DATE NOT NULL,
                dato DECIMAL(10, 4) NOT NULL,
                nota TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla para microbiología
        cur.execute('''
            CREATE TABLE IF NOT EXISTS mediciones_microbiologia (
                id SERIAL PRIMARY KEY,
                tipo VARCHAR(50) NOT NULL,
                punto VARCHAR(50) NOT NULL,
                parametro VARCHAR(50) NOT NULL,
                fecha DATE NOT NULL,
                dato DECIMAL(10, 4) NOT NULL,
                nota TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Índices para mejorar rendimiento
        cur.execute('CREATE INDEX IF NOT EXISTS idx_fisico_fecha ON mediciones_fisicoquimica(fecha)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_fisico_punto ON mediciones_fisicoquimica(punto)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_fisico_parametro ON mediciones_fisicoquimica(parametro)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_micro_fecha ON mediciones_microbiologia(fecha)')
        
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

def insertar_medicion(self, categoria, tipo, punto, parametro, fecha, dato, nota=None):
    """Insertar una nueva medición"""
    conn = self.get_connection()
    if not conn:
        return {'success': False, 'message': 'Error de conexión'}
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        tabla = f'mediciones_{categoria}'
        
        cur.execute(f'''
            INSERT INTO {tabla} (tipo, punto, parametro, fecha, dato, nota)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, tipo, punto, parametro, fecha, dato, nota, timestamp
        ''', (tipo, punto, parametro, fecha, float(dato), nota))
        
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

def obtener_mediciones(self, categoria, filtros=None):
    """Obtener mediciones con filtros opcionales"""
    conn = self.get_connection()
    if not conn:
        return {'success': False, 'message': 'Error de conexión'}
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        tabla = f'mediciones_{categoria}'
        
        query = f'SELECT * FROM {tabla}'
        params = []
        
        if filtros:
            conditions = []
            if 'punto' in filtros:
                conditions.append('punto = %s')
                params.append(filtros['punto'])
            if 'parametro' in filtros:
                conditions.append('parametro = %s')
                params.append(filtros['parametro'])
            if 'fecha_inicio' in filtros:
                conditions.append('fecha >= %s')
                params.append(filtros['fecha_inicio'])
            if 'fecha_fin' in filtros:
                conditions.append('fecha <= %s')
                params.append(filtros['fecha_fin'])
            
            if conditions:
                query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' ORDER BY fecha DESC, timestamp DESC'
        
        cur.execute(query, params)
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

def obtener_estadisticas(self, categoria, punto=None, parametro=None):
    """Obtener estadísticas"""
    conn = self.get_connection()
    if not conn:
        return {'success': False, 'message': 'Error de conexión'}
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        tabla = f'mediciones_{categoria}'
        
        query = f'''
            SELECT 
                COUNT(*) as total,
                AVG(dato) as promedio,
                MAX(dato) as maximo,
                MIN(dato) as minimo,
                STDDEV(dato) as desviacion_estandar
            FROM {tabla}
            WHERE 1=1
        '''
        params = []
        
        if punto:
            query += ' AND punto = %s'
            params.append(punto)
        if parametro:
            query += ' AND parametro = %s'
            params.append(parametro)
        
        cur.execute(query, params)
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