import pandas as pd
import io

# Definimos el tamaño del bloque (chunk)
CHUNK_SIZE = 100 
total_global_ventas = 0.0
numero_chunk = 0

print(f"Calculando Total Global de Ventas por Chunks (Bloque: {CHUNK_SIZE})")
print("-" * 60)

# 1. Leer el archivo usando chunksize
try:
    # Seleccionamos solo las columnas necesarias para ahorrar memoria
    chunk_iterator = pd.read_csv(
        "ventas.csv", 
        chunksize=CHUNK_SIZE, 
        usecols=['Total'] # Solo necesitamos la columna 'Total'
    )
except FileNotFoundError:
    print("ERROR: El archivo 'ventas.csv' no se encuentra.")
    chunk_iterator = []

# 2. Iterar sobre los bloques y calcular el subtotal
for chunk in chunk_iterator:
    numero_chunk += 1
    

    chunk['Total'] = pd.to_numeric(chunk['Total'], errors='coerce')
    chunk['Total'].fillna(chunk['Total'].mean(), inplace=True)
    
    # Calcular el subtotal de ventas para el chunk actual
    subtotal_chunk = chunk['Total'].sum()
    total_global_ventas += subtotal_chunk
    
    print(f"Bloque {numero_chunk}: Subtotal = L.{subtotal_chunk:,.2f}")

# 3. Mostrar el total final acumulado
print("-" * 60)
print(f"Total Global de Ventas (Acumulado): L. {total_global_ventas:,.2f}")