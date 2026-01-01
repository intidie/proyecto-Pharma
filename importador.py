import pandas as pd
import io
from datetime import datetime

class ImportadorDatos:
    """Clase para importar datos desde diferentes formatos"""
    
    def __init__(self, database_manager):
        self.db = database_manager
    
    def procesar_excel(self, archivo, categoria):
        """Importar datos desde archivo Excel"""
        try:
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
            content = archivo.read().decode('utf-8')
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
            df.columns = df.columns.str.lower().str.strip()
            
            required_cols = ['fecha', 'punto', 'parametro', 'dato']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                return {
                    'success': False,
                    'message': f'Faltan columnas: {", ".join(missing_cols)}'
                }
            
            datos_validos = []
            errores = []
            
            for idx, row in df.iterrows():
                try:
                    fecha = pd.to_datetime(row['fecha']).date()
                    dato = float(str(row['dato']).replace(',', '.'))
                    punto = str(row['punto']).strip()
                    parametro = str(row['parametro']).strip().upper()
                    tipo = row.get('tipo', 'agua')
                    nota = str(row['nota']) if 'nota' in row and pd.notna(row['nota']) else None
                    
                    datos_validos.append({
                        'tipo': tipo,
                        'punto': punto,
                        'parametro': parametro,
                        'fecha': fecha,
                        'dato': dato,
                        'nota': nota
                    })
                    
                except Exception as e:
                    errores.append(f"Fila {idx + 2}: {str(e)}")
                    continue
            
            if not datos_validos:
                return {
                    'success': False,
                    'message': 'No se encontraron datos válidos',
                    'errores': errores
                }
            
            insertados = 0
            for dato in datos_validos:
                resultado = self.db.insertar_medicion(
                    categoria=categoria,
                    **dato
                )
                if resultado['success']:
                    insertados += 1
            
            mensaje = f"✓ {insertados} registros importados"
            if errores:
                mensaje += f" ({len(errores)} errores)"
            
            return {
                'success': True,
                'message': mensaje,
                'insertados': insertados,
                'errores': errores[:10]
            }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al procesar: {str(e)}'
            }
