import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Configurar fuente Times New Roman y matemáticas
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'cm'

fig, ax = plt.subplots(figsize=(14, 7))
ax.set_aspect('equal')
ax.axis('off')

# Paleta de colores solicitada
color_line = '#2C3E50'
color_fill_even = '#EFEFEF'
color_fill_odd = '#D4E6F1'
color_dashed = '#7B241C'

# --- 1. Lado Izquierdo: Matriz de Memoria ---
grid_size = 4
cell_w = 1.0
start_x_left = 0.0
start_y_left = 0.0

# Dibujamos la matriz de arriba hacia abajo (j=0 arriba, j=3 abajo)
for j in range(grid_size):
    for i in range(grid_size):
        # Resaltamos las filas impares
        fill_color = color_fill_odd if j % 2 != 0 else color_fill_even
        
        # x aumenta hacia la derecha, y disminuye hacia abajo
        x_rect = start_x_left + i * cell_w
        y_rect = start_y_left + (grid_size - 1 - j) * cell_w
        
        rect = patches.Rectangle((x_rect, y_rect), cell_w, cell_w, 
                                 linewidth=1.5, edgecolor=color_line, 
                                 facecolor=fill_color, zorder=2)
        ax.add_patch(rect)
        
        # Etiqueta (i, j) en la esquina superior izquierda
        ax.text(x_rect + 0.08, y_rect + cell_w - 0.08, f'$({i},{j})$', 
                ha='left', va='top', fontsize=12, color=color_line)

# --- 2. Flecha de Transformación Isomórfica ---
arrow_x_start = start_x_left + grid_size * cell_w + 0.5
arrow_x_end = arrow_x_start + 2.5
arrow_y = start_y_left + (grid_size * cell_w) / 2.0

ax.annotate('', xy=(arrow_x_end, arrow_y), xytext=(arrow_x_start, arrow_y),
            arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", 
                            color=color_line, lw=2))

# Etiqueta de la transformación
ax.text((arrow_x_start + arrow_x_end) / 2, arrow_y + 0.3, r'$\Phi: \mathbb{Z}^2 \to \mathbb{H}$', 
        ha='center', va='bottom', fontsize=18, color=color_line)

# --- 3. Lado Derecho: Mapeo Hexagonal odd-r ---
hex_w = 1.2
hex_size = hex_w / np.sqrt(3)  # Lado del hexágono
hex_v_dist = 1.5 * hex_size    # Distancia vertical entre filas
start_x_right = arrow_x_end + 1.0

# Alinear la fila superior (j=0) con la de la matriz ortogonal
center_y_top = start_y_left + grid_size * cell_w - cell_w / 2.0

centers_x_even = []
centers_x_odd = []

for j in range(grid_size):
    for i in range(grid_size):
        fill_color = color_fill_odd if j % 2 != 0 else color_fill_even
        
        # Lógica de desplazamiento odd-r
        offset_x = (hex_w / 2.0) if j % 2 != 0 else 0.0
        cx = start_x_right + i * hex_w + offset_x
        cy = center_y_top - j * hex_v_dist
        
        # Guardar centros de j=0 y j=1 para las líneas de desalineamiento
        if j == 0:
            centers_x_even.append(cx)
        elif j == 1:
            centers_x_odd.append(cx)
            
        # Vértices del hexágono 'pointy-topped'
        angles_deg = [60 * k - 30 for k in range(6)]
        angles_rad = np.deg2rad(angles_deg)
        vertices = np.column_stack((cx + hex_size * np.cos(angles_rad), 
                                    cy + hex_size * np.sin(angles_rad)))
        
        hex_patch = patches.Polygon(vertices, closed=True, linewidth=1.5, 
                                    edgecolor=color_line, facecolor=fill_color, zorder=2)
        ax.add_patch(hex_patch)
        
        # Etiqueta central (i, j)
        ax.text(cx, cy, f'$({i},{j})$', ha='center', va='center', 
                fontsize=12, color=color_line)

# --- 4. Anotaciones y Formalismo ---
y_min_line = center_y_top - (grid_size - 1) * hex_v_dist - hex_size * 1.5
y_max_line = center_y_top + hex_size * 1.5

# Líneas punteadas verticales
for cx in centers_x_even:
    ax.plot([cx, cx], [y_min_line, y_max_line], linestyle='--', 
            color=color_dashed, linewidth=1.2, alpha=0.8, zorder=1)
for cx in centers_x_odd:
    ax.plot([cx, cx], [y_min_line, y_max_line], linestyle='--', 
            color=color_dashed, linewidth=1.2, alpha=0.8, zorder=1)

# Anotación matemática en la parte inferior
eq_x = start_x_right + (grid_size * hex_w) / 2.0 - hex_w / 4.0
eq_y = y_min_line - 0.2
ax.text(eq_x, eq_y, r'$\Delta x = (j\ \text{mod}\ 2) \cdot \frac{w}{2}$', 
        ha='center', va='top', fontsize=16, color=color_line)

# Configurar los límites del lienzo
ax.set_xlim(start_x_left - 0.5, start_x_right + grid_size * hex_w + 0.5)
ax.set_ylim(eq_y - 1.5, center_y_top + hex_size * 1.5)

plt.tight_layout()

# Guardar la figura
output_filename = "mapeo_compensado_oddr.pdf"
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_filename)
plt.savefig(output_path, format='pdf', bbox_inches='tight', dpi=300)
print(f"Figura teórica generada y guardada en: {output_path}")
