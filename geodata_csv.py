import os
os.environ["GDAL_DATA"] = r"C:\Users\joanm\anaconda3\envs\webservices\Library\share\gdal"
import geopandas as gpd

# 1. Llegeix el GeoJSON original
gdf = gpd.read_file("static/data/estacions.geojson")  # ajusta el path si cal

# 2. Extreu coordenades de la geometria (assegura que és geometry de veritat)
#    Si per algun motiu la columna ja fos text, això petaria, cosa que ens protegeix d'usar el fitxer equivocat.
gdf["lon"] = gdf.geometry.x
gdf["lat"] = gdf.geometry.y

# 3. Converteix la geometria a WKT de forma segura
gdf["geometry_wkt"] = gdf.geometry.to_wkt()

# 4. Escull l'ordre i les columnes que vols al CSV
cols = [
    "FID",
    "ID_ESTACIO",
    "CODI_GRUP_ESTACIO",
    "NOM_ESTACIO",
    "PICTO",
    "DATA",
    "PERSONA",
    "lon",
    "lat",
    "geometry_wkt",
]

gdf[cols].to_csv("static/data/estacions.csv", index=False, encoding="utf-8")
print("Exportat estacions.csv correctament.")
