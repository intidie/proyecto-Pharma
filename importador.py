import pandas as pd
import io
from datetime import datetime

class ImportadorDatos:
    """Clase para importar datos desde diferentes formatos"""
    
    def __init__(self, database_manager):
        self.db = database_manager
    
    def validar_pu(self, pu):
        """Validar que Pu esté entre 001 y 007"""
        try:
            pu_str = str(pu).zfill(3)
            pu_num = int(pu_str)
            return 1 <= pu_num <= 7, pu_str
        except:
            return False, None
    
    def procesar_excel(self, archivo, categoria):
        """Importar datos desde archivo Excel"""
        try:
            # Leer el archivo Excel
            df = pd.read_excel(archivo)
            return self._procesar_dataframe(df, categoria)
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al leer Excel: {str(e)}'
            }
    
    def procesar_txt(self, archivo, categoria, separador=','):
        """Importar datos desde archivo TXT/CSV"""
        try:
            # Leer el contenido del archivo
            content = archivo.read().decode('utf-8')
            
            # Crear DataFrame desde el contenido
            df = pd.read_csv(io.StringIO(content), sep=separador)
            return self._procesar_dataframe(df, categoria)
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al leer TXT: {str(e)}'
            }
    
    def _procesar_dataframe(self, df, categoria):
        """Procesar un DataFrame y guardarlo en la base de datos"""
        try:
            # Normalizar nombres de columnas
            df.columns = df.columns.str.lower().str.strip()
            
            # Verificar columnas requeridas
            required_cols = ['fecha', 'dato', 'pu']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                return {
                    'success': False,
                    'message': f'Faltan columnas: {", ".join(missing_cols)}. Columnas requeridas: fecha, dato, pu'
                }
            
            # Preparar datos para inserción
            datos_validos = []
            errores = []
            
            for idx, row in df.iterrows():
                try:
                    # Procesar fecha
                    fecha = pd.to_datetime(row['fecha']).date()
                    
                    # Procesar dato
                    dato = float(row['dato'])
                    
                    # Procesar y validar Pu
                    es_valido, pu = self.validar_pu(row['pu'])
                    if not es_valido:
                        errores.append(f"Fila {idx + 2}: Pu inválido ({row['pu']})")
                        continue
                    
                    # Procesar notas (opcional)
                    notas = str(row['notas']) if 'notas' in row and pd.notna(row['notas']) else None
                    
                    datos_validos.append({
                        'fecha': fecha,
                        'dato': dato,
                        'pu': pu,
                        'notas': notas
                    })
                    
                except Exception as e:
                    errores.append(f"Fila {idx + 2}: {str(e)}")
                    continue
            
            if not datos_validos:
                return {
                    'success': False,
                    'message': 'No se encontraron datos válidos para importar',
                    'errores': errores
                }
            
            # Insertar en la base de datos
            resultado = self.db.insertar_lote(categoria, datos_validos)
            
            if resultado['success']:
                mensaje = f"✓ {resultado['insertados']} registros importados"
                if errores:
                    mensaje += f" ({len(errores)} filas con errores)"
                
                return {
                    'success': True,
                    'message': mensaje,
                    'insertados': resultado['insertados'],
                    'errores': errores[:10]  # Mostrar solo los primeros 10 errores
                }
            else:
                return resultado
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al procesar datos: {str(e)}'
            }
    
    def generar_plantilla_excel(self, archivo_salida):
        """Generar una plantilla Excel de ejemplo"""
        try:
            datos_ejemplo = {
                'fecha': ['2025-12-22', '2025-12-21', '2025-12-20'],
                'dato': [150.5, 145.2, 148.9],
                'pu': ['001', '002', '003'],
                'notas': ['Medición normal', 'Revisado', '']
            }
            
            df = pd.DataFrame(datos_ejemplo)
            df.to_excel(archivo_salida, index=False)
            
            return {
                'success': True,
                'message': f'Plantilla creada: {archivo_salida}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def generar_plantilla_txt(self, archivo_salida):
        """Generar una plantilla TXT de ejemplo"""
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write("fecha,dato,pu,notas\n")
                f.write("2025-12-22,150.5,001,Medición normal\n")
                f.write("2025-12-21,145.2,002,Revisado\n")
                f.write("2025-12-20,148.9,003,\n")
            
            return {
                'success': True,
                'message': f'Plantilla creada: {archivo_salida}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def importar_desde_sql(self, archivo_sql, categoria):
        """Importar datos desde un archivo SQL"""
        try:
            with open(archivo_sql, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Extraer los valores INSERT
            import re
            pattern = r"INSERT INTO .* VALUES \('([^']+)', ([0-9.]+), '([^']+)'(?:, (?:'([^']*)'|NULL))?\)"
            matches = re.findall(pattern, contenido)
            
            if not matches:
                return {
                    'success': False,
                    'message': 'No se encontraron datos válidos en el archivo SQL'
                }
            
            datos_validos = []
            for match in matches:
                fecha_str, dato_str, pu, notas = match
                
                es_valido, pu_validado = self.validar_pu(pu)
                if not es_valido:
                    continue
                
                datos_validos.append({
                    'fecha': datetime.strptime(fecha_str, '%Y-%m-%d').date(),
                    'dato': float(dato_str),
                    'pu': pu_validado,
                    'notas': notas if notas else None
                })
            
            if not datos_validos:
                return {
                    'success': False,
                    'message': 'No se encontraron datos válidos'
                }
            
            resultado = self.db.insertar_lote(categoria, datos_validos)
            return resultado
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al importar SQL: {str(e)}'
            }