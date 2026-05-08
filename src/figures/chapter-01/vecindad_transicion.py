import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# =============================================================================
# Configuración Académica de Estilo (Nivel Ingeniería / Estilo Cormen)
# =============================================================================
plt.rcParams.update({
    "text.usetex": False,           # Utiliza mathtext interno para compilar nativamente
    "mathtext.fontset": "cm",       # Computer Modern para tipografía matemática
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman", "Times New Roman"],
})

# Creación del lienzo sin ejes cartesianos para mantener limpieza vectorial
fig, ax = plt.subplots(figsize=(11, 5))
ax.set_aspect('equal')
ax.axis('off')

# =============================================================================
# Parámetros Topológicos y Geométricos
# =============================================================================
R = 1.0                           # Radio de la tesela
H = np.sqrt(3) * R                # Distancia euclidiana entre centros de hexágonos
orientacion_hex = np.pi / 6       # Rotación de 30 grados para mapeo submatricial ortogonal

# Paleta de colores sobria
color_vecindad  = "#EFEFEF"       # Gris tenue para la periferia de interacción
color_bordes    = "#2C3E50"       # Gris asfalto elegante para delimitaciones
color_centro_t  = "#D4E6F1"       # Azul tenue para estado transitorio t
color_centro_t1 = "#7B241C"       # Vino oscuro para el estado evaluado en t+1

# =============================================================================
# PARTE IZQUIERDA: Configuración en el Tiempo t
# =============================================================================

# 1. Dibujo de la célula central en t
hex_center = patches.RegularPolygon(
    (0, 0), numVertices=6, radius=R, orientation=orientacion_hex, 
    facecolor=color_centro_t, edgecolor=color_bordes, linewidth=1.5, zorder=2
)
ax.add_patch(hex_center)
ax.text(0, 0, r"$s_c^t$", ha='center', va='center', fontsize=16, color='black', zorder=4)

# 2. Dibujo de la vecindad perimetral y el flujo de información
# Desfase de pi/6 asegura que los centros coincidan con las caras del hexágono central
angles = np.linspace(0, 2 * np.pi, 6, endpoint=False) + np.pi / 6

for i, angle in enumerate(angles):
    cx = H * np.cos(angle)
    cy = H * np.sin(angle)
    
    # Renderizado del vecino
    hex_vecino = patches.RegularPolygon(
        (cx, cy), numVertices=6, radius=R, orientation=orientacion_hex, 
        facecolor=color_vecindad, edgecolor=color_bordes, linewidth=1.5, zorder=1
    )
    ax.add_patch(hex_vecino)
    
    # Etiqueta del estado de la célula adyacente
    ax.text(cx, cy, rf"$s_{i+1}^t$", ha='center', va='center', fontsize=14, color='black', zorder=4)
    
    # 3. Flujo determinista (Flechas):
    # Vector unitario que apunta desde el vecino hacia el centro (0,0)
    unit_x = -cx / H
    unit_y = -cy / H
    
    # Cálculo algebraico de los límites visuales de la flecha
    # Inicia al 60% del radio desde el centro del vecino, culmina al 25% de la célula central
    start_x = cx + unit_x * (0.6 * R)
    start_y = cy + unit_y * (0.6 * R)
    end_x = -unit_x * (0.25 * R)
    end_y = -unit_y * (0.25 * R)
    
    arrow = patches.FancyArrowPatch(
        (start_x, start_y), (end_x, end_y),
        mutation_scale=18, color='#555555', arrowstyle='-|>', lw=1.5, zorder=3
    )
    ax.add_patch(arrow)

# Etiqueta temporal estática
ax.text(0, -3.2, r"Tiempo $t$", ha='center', va='center', fontsize=14)

# =============================================================================
# PARTE CENTRAL: Mapeo de la Función de Transición
# =============================================================================

# Flecha gruesa que denota el mapeo topológico y computacional
ax.annotate(
    "", xy=(4.5, 0), xytext=(2.2, 0),
    arrowprops=dict(arrowstyle="simple", lw=1.5, color=color_bordes, alpha=0.8)
)
ax.text(3.35, 0.4, r"$\Phi(N)$", ha='center', va='center', fontsize=18, fontweight='bold')

# =============================================================================
# PARTE DERECHA: Configuración en el Tiempo t+1
# =============================================================================

# Desplazamiento en el eje X para la representación de aislamiento temporal
cx_right = 7.0

hex_right = patches.RegularPolygon(
    (cx_right, 0), numVertices=6, radius=R, orientation=orientacion_hex, 
    facecolor=color_centro_t1, edgecolor=color_bordes, linewidth=1.5, zorder=2
)
ax.add_patch(hex_right)

# Texto invertido para contrastar con el fondo oscuro (Rigor de visualización)
ax.text(cx_right, 0, r"$s_c^{t+1}$", ha='center', va='center', fontsize=16, color='white', zorder=4)

ax.text(cx_right, -3.2, r"Tiempo $t+1$", ha='center', va='center', fontsize=14)

# =============================================================================
# Ajuste de Encamisado y Exportación a PDF Vectorial
# =============================================================================
ax.set_xlim(-2.5, 9.5)
ax.set_ylim(-3.8, 3)

plt.tight_layout()
plt.savefig("vecindad_transicion.pdf", format='pdf', bbox_inches='tight', transparent=True)