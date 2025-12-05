import pandas as pd
import io

# Definimos el tamaño del bloque
CHUNK_SIZE = 100 
numero_chunk = 0

# Lista para almacenar los resultados parciales (Series de subtotales por producto)
all_chunks_groups = []

print(f"Agrupación Distribuida de Ventas por Producto (Bloque: {CHUNK_SIZE})")
print("-" * 70)

# 1. Leer el archivo usando chunksize
# Usamos usecols para cargar solo las columnas que necesitamos: 'Producto' y 'Total'
try:
    chunk_iterator = pd.read_csv(
        "ventas.csv", 
        chunksize=CHUNK_SIZE, 
        usecols=['Producto', 'Total']
    )
except FileNotFoundError:
    print("ERROR: El archivo 'ventas.csv' no se encuentra.")
    chunk_iterator = []

# 2. Iterar sobre los bloques, corregir tipos y agrupar
for chunk in chunk_iterator:
    numero_chunk += 1
    
    # A. Corrección de tipos (replicando la lógica del Ej. 4 para el 'Total')
    # Convertir a numérico y reemplazar valores inválidos (NaNs) con la media del chunk
    chunk['Total'] = pd.to_numeric(chunk['Total'], errors='coerce')
    chunk['Total'].fillna(chunk['Total'].mean(), inplace=True)
    
    # B. Agrupar y sumar el subtotal por producto en este bloque
    subtotal_por_producto = chunk.groupby('Producto')['Total'].sum()
    
    # C. Almacenar el resultado parcial
    all_chunks_groups.append(subtotal_por_producto)
    
    # Muestra de progreso
    print(f"Bloque {numero_chunk} procesado. Subtotales parciales calculados.")

# 3. Consolidar los resultados
print("-" * 70)
print("Consolidando resultados de los bloques...")

# Concatenar todas las Series de subtotales parciales en una sola Serie
serie_consolidada = pd.concat(all_chunks_groups)

# 4. Calcular la suma final por producto
# Aplicar el último groupby.sum() suma los subtotales parciales de los productos iguales
ventas_finales_por_producto = serie_consolidada.groupby(serie_consolidada.index).sum().sort_values(ascending=False)


# 5. Mostrar el resultado final
print("Resultado Final: Venta Total Global por Producto**")
print("-" * 40)
print(ventas_finales_por_producto.apply(lambda x: f'L{x:,.2f}')) # Aplicar formato de moneda

print("-" * 70)

ventas_finales_por_producto = serie_consolidada.groupby(serie_consolidada.index).sum()