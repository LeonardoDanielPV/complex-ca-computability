"""
Generador de figura: Tensor de Vecindad 2x2
Capítulo 4 - Computabilidad en autómatas celulares complejos
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# Asegurar que se guarde en el mismo directorio del script
output_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(output_dir, "tensor_vecindad_2x2.pdf")

# Configuración de estilo académico
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "cm",
    "font.size": 14,
    "axes.linewidth": 1.5
})

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
ax.axis('off')

# Paleta de colores rigurosa
color_fill = "#EFEFEF"
color_border = "#2C3E50"
color_inactive = "#7B241C"
color_highlight = "#D4E6F1"

# Geometría Principal (Bloque 2x2 centrado en 0,0)
# Las celdas van de -1 a 1, cada una de tamaño 1x1.
cells = [
    (-1, 0),  # Top-Left
    (0, 0),   # Top-Right
    (-1, -1), # Bottom-Left
    (0, -1)   # Bottom-Right
]

# Dibujar la cuadrícula 2x2
for x, y in cells:
    rect = patches.Rectangle((x, y), 1, 1, facecolor=color_fill, edgecolor=color_border, linewidth=2, zorder=2)
    ax.add_patch(rect)

# Etiqueta central matemática para la subred funcional
# Usamos un bbox con el mismo color de fondo para que oculte la intersección de líneas
ax.text(0, 0, r'$\mathcal{T}_B$', ha='center', va='center', fontsize=26, color=color_border,
        bbox=dict(facecolor=color_fill, edgecolor='none', pad=4), zorder=5)

# Perímetro Expuesto: 8 aristas perimetrales
# Definidas por su punto medio (mx, my) y vector normal saliente (nx, ny)
edges = {
    "top_left": (-0.5, 1.0, 0, 1),
    "top_right": (0.5, 1.0, 0, 1),
    "bottom_left": (-0.5, -1.0, 0, -1),
    "bottom_right": (0.5, -1.0, 0, -1),
    "left_top": (-1.0, 0.5, -1, 0),
    "left_bottom": (-1.0, -0.5, -1, 0),
    "right_top": (1.0, 0.5, 1, 0),
    "right_bottom": (1.0, -0.5, 1, 0)
}

# Ejes Direccionales Activos: 6 aristas
# Asignación congruente con un mapeo de vecindad hexagonal a cuadrícula cuadrada
active_edges = {
    "left_top": ("NW", r"$\mathit{NW}$"),
    "left_bottom": ("W", r"$\mathit{W}$"),
    "right_top": ("NE", r"$\mathit{NE}$"),
    "right_bottom": ("E", r"$\mathit{E}$"),
    "bottom_left": ("SW", r"$\mathit{SW}$"),
    "bottom_right": ("SE", r"$\mathit{SE}$")
}

# Aristas Inactivas (Degeneradas): 2 aristas
inactive_edges = ["top_left", "top_right"]

# Dibujar vectores y etiquetas para las aristas activas
arrow_length = 0.65
for edge_name, (dir_name, label) in active_edges.items():
    mx, my, nx, ny = edges[edge_name]
    
    # Origen (borde) y destino (punta de flecha)
    ex = mx + nx * arrow_length
    ey = my + ny * arrow_length
    
    # Dibujar la flecha perpendicular saliente
    ax.annotate("",
                xy=(ex, ey), xycoords='data',
                xytext=(mx, my), textcoords='data',
                arrowprops=dict(arrowstyle="-|>", color=color_border, lw=2.5,
                                shrinkA=0, shrinkB=0,
                                mutation_scale=18),
                zorder=3)
    
    # Ubicar la etiqueta matemática de la dirección
    lx = mx + nx * (arrow_length + 0.25)
    ly = my + ny * (arrow_length + 0.25)
    ax.text(lx, ly, label, ha='center', va='center', fontsize=18, color=color_border)

# Resaltar visualmente las aristas inactivas
for edge_name in inactive_edges:
    mx, my, nx, ny = edges[edge_name]
    
    # Superponer línea gruesa y punteada sobre la arista
    if nx == 0: # Horizontal
        x_start, x_end = mx - 0.5, mx + 0.5
        y_start, y_end = my, my
    else: # Vertical
        x_start, x_end = mx, mx
        y_start, y_end = my - 0.5, my + 0.5
        
    ax.plot([x_start, x_end], [y_start, y_end], color=color_inactive, lw=3.5, ls="--", zorder=4)
    
    # Agregar un símbolo sutil de "bloqueo" (una pequeña cruz roja) cerca del borde
    bx = mx + nx * 0.15
    by = my + ny * 0.15
    size = 0.08
    ax.plot([bx - size, bx + size], [by - size, by + size], color=color_inactive, lw=2.5, zorder=5)
    ax.plot([bx - size, bx + size], [by + size, by - size], color=color_inactive, lw=2.5, zorder=5)

# Ajuste de encuadre para asegurar proporciones y espaciado
ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-2.2, 2.2)

plt.tight_layout()
plt.savefig(output_file, format="pdf", bbox_inches='tight')
print(f"Figura guardada exitosamente en: {output_file}")
