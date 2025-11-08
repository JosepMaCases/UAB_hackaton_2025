import geopandas as gpd
import sys
import os

# --- Nombres de los archivos ---
gml_file = "static/data/hospitalet_buildings.gml"
geojson_file = "static/data/hospitalet_buildings.geojson"
# ------------------------------

print(f"Iniciando la conversión de '{gml_file}' a '{geojson_file}'...")

# 1. Comprobar si el archivo de entrada existe
if not os.path.exists(gml_file):
    print(f"Error: No se encontró el archivo '{gml_file}' en esta carpeta.")
    print("Por favor, asegúrate de que el archivo GML está en el mismo directorio que este script.")
    sys.exit(1)

try:
    # 2. Leer el archivo GML con geopandas
    # Geopandas (fiona/gdal) detectará el CRS (Sistema de Coordenadas)
    # y analizará la estructura compleja de INSPIRE.
    print(f"Leyendo '{gml_file}'... (Esto puede tardar un momento si el archivo es grande)")
    gdf = gpd.read_file(gml_file)

    print(f"Archivo GML leído con éxito. Contiene {len(gdf)} edificios.")
    print(f"El CRS (Sistema de Coordenadas) original es: {gdf.crs}")

    # 3. Reproyectar a EPSG:4326 (WGS 84)
    # Es el estándar obligatorio para GeoJSON.
    print("Reproyectando coordenadas a EPSG:4326 (WGS 84)...")
    gdf_wgs84 = gdf.to_crs("EPSG:4326")

    # 4. Guardar el resultado como GeoJSON
    print(f"Guardando el archivo GeoJSON como '{geojson_file}'...")
    gdf_wgs84.to_file(geojson_file, driver="GeoJSON")

    print("\n--- ¡Éxito! ---")
    print(f"El archivo '{geojson_file}' ha sido creado correctamente.")

except Exception as e:
    print(f"\n--- ¡Error durante la conversión! ---")
    print(f"Detalle del error: {e}")
    print("\nPosibles causas:")
    print("1. ¿Está 'geopandas' y sus dependencias (GDAL) instalados correctamente?")
    print("   (Recuerda: 'conda install -c conda-forge geopandas' es la forma más fácil)")
    print("2. El archivo GML podría estar dañado o tener una estructura inesperada.")