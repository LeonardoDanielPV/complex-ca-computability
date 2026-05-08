import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch

# =============================================================================
# Configuración Académica de Estilo (Nivel Ingeniería / Estilo Cormen)
# =============================================================================
plt.rcParams.update({
    "text.usetex": False,           # Utiliza mathtext interno para compilar nativamente
    "mathtext.fontset": "cm",       # Computer Modern para tipografía matemática
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman", "Times New Roman"],
})

# ==============================================================================
# Configuración del estilo académico (Paleta de colores rigurosa)
# ==============================================================================
COLOR_CENTER   = "#7B241C"  # Rojo vino tenue (acento)
COLOR_NEIGHBOR = "#EFEFEF"  # Gris claro
COLOR_EDGE     = "#2C3E50"  # Azul pizarra oscuro
COLOR_TEXT     = "#2C3E50"  # Azul pizarra oscuro
COLOR_LIGHT_BG = "#FFFFFF"

# Crear la figura con 1 fila y 2 columnas
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# ==============================================================================
# SUBGRÁFICO 1: Espacio de cuadrícula Z^2 (Vecindad de Moore)
# ==============================================================================
ax1.set_title(r"Espacio de cuadrícula $\mathbb{Z}^2$ (Vecindad de Moore)", 
              fontsize=16, pad=5)
ax1.set_aspect('equal', adjustable='box')
ax1.axis('off')

# Generar la cuadrícula de 3x3
for i in [-1, 0, 1]:
    for j in [-1, 0, 1]:
        facecolor = COLOR_CENTER if (i == 0 and j == 0) else COLOR_NEIGHBOR
        # Coordenadas ajustadas para que (0,0) sea el centroide geométrico de la célula central
        rect = Rectangle((i - 0.5, j - 0.5), 1, 1, 
                         facecolor=facecolor, edgecolor=COLOR_EDGE, linewidth=1.5, zorder=1)
        ax1.add_patch(rect)

# Trazar vectores direccionales de la célula central hacia sus 8 vecinos
for i in [-1, 0, 1]:
    for j in [-1, 0, 1]:
        if i == 0 and j == 0:
            continue
        arrow = FancyArrowPatch((0, 0), (i, j), 
                                color=COLOR_EDGE, arrowstyle='-|>', mutation_scale=15, 
                                lw=1.8, zorder=2)
        ax1.add_patch(arrow)

# Anotaciones geométricas evidenciando la asimetría de distancias
bbox_props = dict(boxstyle="round,pad=0.3", fc=COLOR_LIGHT_BG, ec=COLOR_EDGE, lw=1)
ax1.text(0, 0.5, r"$d = 1$", color=COLOR_TEXT, fontsize=12, ha='center', va='center', 
         bbox=bbox_props, zorder=3)
ax1.text(0.5, 0.5, r"$d = \sqrt{2}$", color=COLOR_TEXT, fontsize=12, ha='center', va='center', 
         rotation=45, bbox=bbox_props, zorder=3)

# Acotar los límites de la gráfica para centrar la cuadrícula
ax1.set_xlim(-2, 2)
ax1.set_ylim(-2, 2)

# ==============================================================================
# SUBGRÁFICO 2: Teselación Hexagonal Isótropa (Espacio L_hex)
# ==============================================================================
ax2.set_title(r"Teselación Hexagonal (Espacio $\mathcal{L}_{hex}$)", 
              fontsize=16, pad=5)
ax2.set_aspect('equal', adjustable='box')
ax2.axis('off')

# Constante algebraica exacta para la altura del hexágono
h = np.sqrt(3) / 2  

# Función generadora de hexágonos Flat-Topped basados en coordenadas centrales
def build_hexagon(cx, cy, color):
    vertices = [
        (cx + 1, cy),               # Derecha
        (cx + 0.5, cy + h),         # Superior derecha
        (cx - 0.5, cy + h),         # Superior izquierda
        (cx - 1, cy),               # Izquierda
        (cx - 0.5, cy - h),         # Inferior izquierda
        (cx + 0.5, cy - h)          # Inferior derecha
    ]
    return Polygon(vertices, facecolor=color, edgecolor=COLOR_EDGE, linewidth=1.5, zorder=1)

# Mapeo de la vecindad canónica N_hex (centro y los 6 vecinos colindantes)
# Estructura: (coordenada_x, coordenada_y, color, etiqueta_axial)
hex_neighborhood = [
    (0, 0, COLOR_CENTER, ""),                  # Origen (Célula central)
    (1.5, h, COLOR_NEIGHBOR, r"$(1,0)$"),      # Vecino Noreste
    (0, 2*h, COLOR_NEIGHBOR, r"$(0,1)$"),      # Vecino Norte
    (-1.5, h, COLOR_NEIGHBOR, r"$(-1,1)$"),    # Vecino Noroeste
    (-1.5, -h, COLOR_NEIGHBOR, r"$(-1,0)$"),   # Vecino Suroeste
    (0, -2*h, COLOR_NEIGHBOR, r"$(0,-1)$"),    # Vecino Sur
    (1.5, -h, COLOR_NEIGHBOR, r"$(1,-1)$")     # Vecino Sureste
]

# Dibujar hexágonos, vectores y sus etiquetas
for cx, cy, color, label in hex_neighborhood:
    ax2.add_patch(build_hexagon(cx, cy, color))
    
    if label != "": # Es un vecino (no el centro)
        # Vector direccional
        arrow = FancyArrowPatch((0, 0), (cx, cy), 
                                color=COLOR_EDGE, arrowstyle='-|>', mutation_scale=15, 
                                lw=1.8, zorder=2)
        ax2.add_patch(arrow)
        
        # Posicionamiento de la etiqueta matemática para evitar superposición
        ax2.text(cx * 1.25, cy * 1.25, label, fontsize=12, 
                 ha='center', va='center', fontweight='bold', zorder=3,
                 bbox=dict(boxstyle="round,pad=0.1", fc=COLOR_NEIGHBOR, ec='none', alpha=0.8))

# Demostración geométrica de isotropía: Círculo con radio constante
# La distancia euclidiana a cualquier centro vecino es matemáticamente sqrt(3)
radius = np.sqrt(1.5**2 + h**2) 
circle = Circle((0, 0), radius=radius, edgecolor=COLOR_EDGE, facecolor='none', 
                linestyle='--', linewidth=1.2, alpha=0.6, zorder=4)
ax2.add_patch(circle)

# Acotación matemática enfatizando la uniformidad radial
ax2.text(0, -3.2, r"$\forall v \in \mathcal{N}_{hex}, \ ||v|| = c$", 
         color=COLOR_EDGE, fontsize=14, ha='center', fontweight='bold')

# Acotar los límites para mantener simetría
ax2.set_xlim(-3.5, 3.5)
ax2.set_ylim(-3.5, 3.5)

# ==============================================================================
# Exportación del documento y renderizado
# ==============================================================================
plt.tight_layout()
plt.savefig("comparativa_reticulas.pdf", format='pdf', bbox_inches='tight', dpi=300)
print("Figura generada exitosamente y guardada como 'comparativa_reticulas.pdf'.")
plt.show()