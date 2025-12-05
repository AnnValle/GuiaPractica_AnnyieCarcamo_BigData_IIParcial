import pandas as pd
import numpy as np
import io


# 1. Cargar el archivo
try:
    df = pd.read_csv("ventas.csv")
except FileNotFoundError:
    print("ERROR: El archivo 'ventas.csv' no se encuentra.")
    # Usar un DataFrame vacío para evitar errores si no se encuentra el archivo
    df = pd.DataFrame()

if not df.empty:
    # 2. Limpieza básica (Ej. 1): Eliminar nulos y duplicados
    df_limpio = df.dropna().drop_duplicates().copy()

    # 3. Normalización de texto (Ej. 2): Cliente y Producto a formato Título
    df_limpio['Cliente'] = df_limpio['Cliente'].str.title()
    df_limpio['Producto'] = df_limpio['Producto'].str.title()

    # 4. Corrección de tipos (Ej. 4): Convertir a numérico y reemplazar inválidos por la media
    columnas_a_validar = ['Cantidad', 'PrecioUnitario', 'Total']
    for col in columnas_a_validar:
        col_corr = col + '_Corregido'
        # Convertir a numérico, forzando errores a NaN
        df_limpio[col_corr] = pd.to_numeric(df_limpio[col], errors='coerce')
        # Calcular la media de los valores válidos
        media_col = df_limpio[col_corr].mean()
        # Reemplazar NaN con la media
        df_limpio[col_corr].fillna(media_col, inplace=True)
        # Actualizar la columna original con los valores corregidos
        df_limpio[col] = df_limpio[col_corr]

    # 5. Cálculo de campos dependientes (Ej. 3 y 5)
    UMBRAL_DESCUENTO = 1500
    TASA_DESCUENTO = 0.10
    TASA_IMPUESTO = 0.15 

    # Descuento
    df_limpio['Descuento'] = np.where(df_limpio['Total'] > UMBRAL_DESCUENTO, df_limpio['Total'] * TASA_DESCUENTO, 0).round(2)
    df_limpio['Total_con_descuento'] = (df_limpio['Total'] - df_limpio['Descuento']).round(2)
    # Impuesto y Total Final
    df_limpio['Impuesto'] = (df_limpio['Total_con_descuento'] * TASA_IMPUESTO).round(2)
    df_limpio['Total_Final'] = (df_limpio['Total_con_descuento'] + df_limpio['Impuesto']).round(2)


    df_limpio['Fecha'] = pd.to_datetime(df_limpio['Fecha'])




    texto_busqueda = input("Ingrese el texto a buscar en el nombre del cliente (e.g., 'lu' para 'Lucía' o 'Perez'): ")

    # Usar un valor por defecto si el usuario no ingresa nada
    if not texto_busqueda:
        texto_busqueda = "María"
        print(f"No se ingresó texto. Usando valor por defecto: '{texto_busqueda}'")
        
    # 2. Convertir el texto de búsqueda a minúsculas
    texto_busqueda_lower = texto_busqueda.lower()

    # 3. Filtrar usando .str.lower() en la columna Cliente y .str.contains()
    df_busqueda = df_limpio[
        df_limpio['Cliente'].str.lower().str.contains(texto_busqueda_lower, na=False)
    ].copy()

    # 4. Mostrar los resultados
    print("\n" + "=" * 60)
    print(f"Resultados de la Búsqueda Dinámica para: '{texto_busqueda}'")
    print("=" * 60)
    print(f"Se encontraron **{len(df_busqueda)}** transacciones que coinciden con el nombre.")
    
    columnas_mostrar = ['Fecha', 'Cliente', 'Producto', 'Total_Final']
    if len(df_busqueda) > 0:
        print("\n--- Muestra de los primeros 10 resultados ---")
        print(df_busqueda[columnas_mostrar].head(10))
    else:
        print("\nNo se encontró ninguna coincidencia.")
    print("=" * 60)