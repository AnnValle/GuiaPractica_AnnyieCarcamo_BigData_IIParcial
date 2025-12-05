import pandas as pd
import numpy as np
import os
import re # Usado para sanitizar nombres de archivo
import time

# --- PARTE A: Exportación de Resúmenes Agregados ---

# Carga y limpieza inicial
df = pd.read_csv("ventas.csv")
df_limpio = df.dropna().drop_duplicates().copy()

# Normalización de texto
df_limpio['Cliente'] = df_limpio['Cliente'].str.title()
df_limpio['Producto'] = df_limpio['Producto'].str.title()

# Corrección de tipos
columnas_a_validar = ['Cantidad', 'PrecioUnitario', 'Total']
for col in columnas_a_validar:
    col_corr = col + '_Corregido'
    df_limpio[col_corr] = pd.to_numeric(df_limpio[col], errors='coerce')
    media_col = df_limpio[col_corr].mean()
    df_limpio[col_corr].fillna(media_col, inplace=True)
    df_limpio[col] = df_limpio[col_corr]

# Cálculo de Totales
UMBRAL_DESCUENTO = 1500
TASA_DESCUENTO = 0.10
TASA_IMPUESTO = 0.15 
df_limpio['Descuento'] = np.where(df_limpio['Total'] > UMBRAL_DESCUENTO, df_limpio['Total'] * TASA_DESCUENTO, 0).round(2)
df_limpio['Total_con_descuento'] = (df_limpio['Total'] - df_limpio['Descuento']).round(2)
df_limpio['Impuesto'] = (df_limpio['Total_con_descuento'] * TASA_IMPUESTO).round(2)
df_limpio['Total_Final'] = (df_limpio['Total_con_descuento'] + df_limpio['Impuesto']).round(2)
df_limpio['Fecha'] = pd.to_datetime(df_limpio['Fecha'])




print("Exportando Resúmenes Agregados...")

# 1. Resumen por Producto
resumen_producto = df_limpio.groupby('Producto')['Total_Final'].sum().sort_values(ascending=False)
resumen_producto_df = resumen_producto.reset_index(name='Venta_Total_Final')

# Exportar Resumen por Producto
nombre_prod = "resumen_ventas_por_producto.csv"
resumen_producto_df.to_csv(nombre_prod, index=False)
print(f"Archivo de resumen de productos creado: {nombre_prod}")


# 2. Resumen por Cliente
resumen_cliente = df_limpio.groupby('Cliente')['Total_Final'].sum().sort_values(ascending=False)
resumen_cliente_df = resumen_cliente.reset_index(name='Gasto_Total_Final')

# Exportar Resumen por Cliente
nombre_cliente = "resumen_ventas_por_cliente.csv"
resumen_cliente_df.to_csv(nombre_cliente, index=False)
print(f"Archivo de resumen de clientes creado: {nombre_cliente}")
print("-" * 60)


# --- PARTE B: Exportación Segmentada (Particionamiento) ---

# Función para asegurar nombres de archivo válidos para Windows
def sanitizar_nombre_archivo(nombre):
    """Convierte el nombre del producto a un nombre de archivo seguro."""
    # 1. Reemplazar espacios y guiones
    nombre_limpio = nombre.lower().replace(' ', '_').replace('-', '_')
    # 2. Eliminar caracteres inválidos en Windows (\/:*?"<>|)
    # Usamos re.sub para buscar y reemplazar los caracteres inválidos
    nombre_seguro = re.sub(r'[\\/:*?"<>|]', '', nombre_limpio)
    return nombre_seguro

# Crear un directorio para las particiones
partition_dir = "ventas_por_producto_segmentadas"
os.makedirs(partition_dir, exist_ok=True)
print(f"Exportando archivos segmentados a: '{partition_dir}/'")

total_archivos = 0
# 3. Iterar y exportar archivos por partición de producto
for producto in df_limpio['Producto'].unique():
    # Filtrar el DataFrame para obtener solo las transacciones de este producto
    df_particion = df_limpio[df_limpio['Producto'] == producto].copy()
    
    # Crear nombre de archivo válido
    nombre_archivo_base = sanitizar_nombre_archivo(producto)
    nombre_archivo = f"{nombre_archivo_base}.csv"
    ruta_archivo = os.path.join(partition_dir, nombre_archivo)
    
    # Exportar el archivo
    df_particion.to_csv(ruta_archivo, index=False)
    
    # print(f"  - Exportado: {nombre_archivo}")
    total_archivos += 1

print(f"\nProceso de Particionamiento finalizado.")
print(f"Total de archivos creados: {total_archivos}")
print("-" * 60)