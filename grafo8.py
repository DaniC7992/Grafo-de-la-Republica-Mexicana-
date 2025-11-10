import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from itertools import permutations
import math

# -------------------------------
# Coordenadas reales (aprox. centro del estado)
# -------------------------------
estados = {
    "Jalisco": (20.6597, -103.3496),
    "Guanajuato": (21.0190, -101.2574),
    "Michoacán": (19.5665, -101.7068),
    "Edo. de México": (19.3564, -99.7560),
    "Puebla": (19.0379, -98.2035),
    "Veracruz": (19.1738, -96.1342),
    "Oaxaca": (17.0732, -96.7266)
}

# -------------------------------
# Conexiones entre estados y costos (km)
# -------------------------------
conexiones = [
    ("Jalisco", "Guanajuato", 220),
    ("Jalisco", "Michoacán", 330),
    ("Guanajuato", "Michoacán", 160),
    ("Guanajuato", "Edo. de México", 320),
    ("Michoacán", "Edo. de México", 210),
    ("Edo. de México", "Puebla", 140),
    ("Puebla", "Veracruz", 250),
    ("Veracruz", "Oaxaca", 480),
    ("Puebla", "Oaxaca", 380),
    ("Michoacán", "Puebla", 290),
    ("Guanajuato", "Puebla", 420),
    ("Jalisco", "Edo. de México", 520)
]

# Crear grafo
G = nx.Graph()
for a, b, c in conexiones:
    G.add_edge(a, b, weight=c)

# -------------------------------
# Función: calcular costo del recorrido
# -------------------------------
def costo_recorrido(grafo, camino):
    total = 0
    for a, b in zip(camino, camino[1:]):
        if grafo.has_edge(a, b):
            total += grafo[a][b]['weight']
        else:
            return math.inf
    return total

# -------------------------------
# a) Recorrido sin repetir
# -------------------------------
mejor_camino_a, mejor_costo_a = None, math.inf
for perm in permutations(estados.keys()):
    costo = costo_recorrido(G, perm)
    if costo < mejor_costo_a:
        mejor_camino_a, mejor_costo_a = perm, costo

# -------------------------------
# b) Recorrido repitiendo un estado
# -------------------------------
mejor_camino_b, mejor_costo_b = None, math.inf
for repetido in estados.keys():
    lista = list(estados.keys()) + [repetido]
    for perm in permutations(lista, 8):
        if len(set(perm)) == 7:
            costo = costo_recorrido(G, perm)
            if costo < mejor_costo_b:
                mejor_camino_b, mejor_costo_b = perm, costo

# -------------------------------
# Mostrar resultados
# -------------------------------
print("=== (a) Recorrido sin repetir ===")
print(" → ".join(mejor_camino_a))
print(f"Costo total: {mejor_costo_a} km")

print("\n=== (b) Recorrido repitiendo un estado ===")
print(" → ".join(mejor_camino_b))
print(f"Costo total: {mejor_costo_b} km")

# -------------------------------
# MAPA con etiquetas legibles y líneas guía
# -------------------------------
plt.figure(figsize=(13, 11))
m = Basemap(projection='merc',
            llcrnrlat=14, urcrnrlat=33,
            llcrnrlon=-118, urcrnrlon=-86,
            resolution='i')

m.drawmapboundary(fill_color='lightblue')
m.fillcontinents(color='cornsilk', lake_color='lightblue')
m.drawcountries(color='black', linewidth=1)
m.drawstates(color='gray', linewidth=0.5)

# Dibujar conexiones
for a, b, w in conexiones:
    lat_a, lon_a = estados[a]
    lat_b, lon_b = estados[b]
    x1, y1 = m(lon_a, lat_a)
    x2, y2 = m(lon_b, lat_b)
    plt.plot([x1, x2], [y1, y2], color='gray', linewidth=1.3, alpha=0.7)
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    plt.text(mid_x, mid_y, f"{w}", fontsize=8, color='blue', ha='center')

# Desplazamientos para etiquetas (para no encimar)
offsets = {
    "Jalisco": (80000, 70000),
    "Guanajuato": (60000, 100000),
    "Michoacán": (80000, -30000),
    "Edo. de México": (80000, -20000),
    "Puebla": (70000, -20000),
    "Veracruz": (90000, -40000),
    "Oaxaca": (80000, -50000)
}

# Dibujar estados, etiquetas y líneas guía
for estado, (lat, lon) in estados.items():
    x, y = m(lon, lat)
    dx, dy = offsets[estado]
    plt.plot(x, y, 'ro', markersize=9)  # Punto rojo del estado
    plt.plot([x, x + dx * 0.6], [y, y + dy * 0.6], color='black', linestyle='--', linewidth=0.8)  # Línea guía
    plt.text(x + dx, y + dy, estado, fontsize=12, fontweight='bold',
             color='darkred', bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.4'))

# Resaltar recorridos
# Verde: sin repetir
for a, b in zip(mejor_camino_a, mejor_camino_a[1:]):
    lat_a, lon_a = estados[a]
    lat_b, lon_b = estados[b]
    x1, y1 = m(lon_a, lat_a)
    x2, y2 = m(lon_b, lat_b)
    plt.plot([x1, x2], [y1, y2], color='green', linewidth=3, label="Recorrido sin repetir" if a == mejor_camino_a[0] else "")

# Rojo: con repetición
for a, b in zip(mejor_camino_b, mejor_camino_b[1:]):
    lat_a, lon_a = estados[a]
    lat_b, lon_b = estados[b]
    x1, y1 = m(lon_a, lat_a)
    x2, y2 = m(lon_b, lat_b)
    plt.plot([x1, x2], [y1, y2], color='red', linewidth=2.5, linestyle='--', label="Recorrido con repetición" if a == mejor_camino_b[0] else "")

plt.title("Mapa de México: 7 Estados con Rutas, Costos y Nombres Claros", fontsize=15, fontweight='bold')
plt.legend()
plt.show()
