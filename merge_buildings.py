import geopandas as gpd
import pandas as pd
import os

# --- Configuración ---

# 1. Directorio donde están los archivos
DATA_DIR = os.path.join("static", "data")

# 2. Lista de archivos que quieres unir
files_to_merge = [
    "hospitalet_buildings.geojson",
    "edificis.geojson",
    "santjust_buildings.geojson",
    "santjoan_buildings.geojson",
    "esplugues_buildings.geojson",
    "santfeliu_buildings.geojson",
    "cornella_buildings.geojson"
]

# 3. Nombre del archivo de salida
OUTPUT_FILE = os.path.join(DATA_DIR, "buildings.geojson")

# ---------------------

def merge_geojson_files():
    """
    Lee múltiples archivos GeoJSON, los combina en uno solo
    y guarda el resultado.
    """
    
    # Lista para guardar cada GeoDataFrame individual
    gdfs_list = []
    
    print("Iniciando la unión de archivos GeoJSON...")
    
    target_crs = None # Almacenará el CRS (Sistema de Coordenadas) del primer archivo

    for filename in files_to_merge:
        filepath = os.path.join(DATA_DIR, filename)
        
        try:
            # 1. Leer el archivo
            print(f"Leyendo: {filepath}")
            current_gdf = gpd.read_file(filepath)
            print(f" -> Encontrados {len(current_gdf)} edificios.")
            
            # 2. Comprobar el Sistema de Coordenadas (CRS)
            if target_crs is None:
                target_crs = current_gdf.crs # Establece el CRS objetivo
                print(f" -> CRS objetivo establecido a: {target_crs.to_string()}")

            # 3. Si un archivo tiene un CRS diferente, se reproyecta
            if current_gdf.crs != target_crs:
                print(f"   ¡Aviso! CRS de '{filename}' no coincide. Reproyectando...")
                current_gdf = current_gdf.to_crs(target_crs)
                
            gdfs_list.append(current_gdf)

        except Exception as e:
            print(f"ERROR: No se pudo leer el archivo {filepath}. Error: {e}")
            print(" -> Saltando este archivo.")
    
    if not gdfs_list:
        print("No se ha podido leer ningún archivo. Saliendo.")
        return

    # 4. Combinar todos los GeoDataFrames en uno solo
    print("\nCombinando todos los archivos...")
    # pd.concat es la función de pandas para apilar los datos
    combined_gdf = pd.concat(gdfs_list, ignore_index=True)

    # 5. Guardar el archivo combinado
    try:
        print(f"Guardando el archivo combinado en: {OUTPUT_FILE}")
        combined_gdf.to_file(OUTPUT_FILE, driver="GeoJSON")
        print("\n--- ¡Éxito! ---")
        print(f"Total de edificios combinados: {len(combined_gdf)}")
        print(f"Archivo guardado en: {OUTPUT_FILE}")
    
    except Exception as e:
        print(f"ERROR: No se pudo guardar el archivo combinado. Error: {e}")

# --- Ejecutar el script ---
if __name__ == "__main__":
    merge_geojson_files()