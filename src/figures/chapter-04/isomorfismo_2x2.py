import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Configuración de estilo
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'cm'

# Colores definidos
c_bg = "#EFEFEF"
c_active = "#2C3E50"
c_fill = "#D4E6F1"
c_inactive = "#7B241C"

fig, ax = plt.subplots(figsize=(16, 7))
fig.patch.set_facecolor('white') 
ax.set_aspect('equal')
ax.axis('off')

# Centros geométricos
center_hex = np.array([0, 0])
center_grid = np.array([10, 0])

# --- 1. HEXÁGONO REGULAR ---
R = 2.2
angles_v = np.deg2rad([30, 90, 150, 210, 270, 330])
hx = center_hex[0] + R * np.cos(angles_v)
hy = center_hex[1] + R * np.sin(angles_v)
hex_poly = patches.Polygon(np.column_stack((hx, hy)), closed=True, 
                           facecolor=c_fill, edgecolor=c_active, lw=2.5, zorder=2)
ax.add_patch(hex_poly)

# Vectores del Hexágono
vec_labels = [r"$E$", r"$NE$", r"$NW$", r"$W$", r"$SW$", r"$SE$"]
vec_angles = np.deg2rad([0, 60, 120, 180, 240, 300])
apothem = R * np.cos(np.deg2rad(30))

for angle, label in zip(vec_angles, vec_labels):
    dx = (apothem + 0.6) * np.cos(angle)
    dy = (apothem + 0.6) * np.sin(angle)
    ax.arrow(center_hex[0], center_hex[1], dx, dy, head_width=0.2, head_length=0.25, 
             fc=c_active, ec=c_active, zorder=3, length_includes_head=True)
    
    tx = center_hex[0] + (apothem + 1.1) * np.cos(angle)
    ty = center_hex[1] + (apothem + 1.1) * np.sin(angle)
    ax.text(tx, ty, label, fontsize=16, color=c_active, ha='center', va='center', zorder=4)

# --- 2. FLECHA DE TRANSFORMACIÓN (\Phi) ---
ax.arrow(3.2, 0, 3.6, 0, head_width=0.5, head_length=0.4, width=0.15, 
         fc=c_active, ec=c_active, zorder=3, length_includes_head=True)
ax.text(5.0, 0.7, r"$\Phi$", fontsize=24, color=c_active, ha='center', va='center')

# --- 3. BLOQUE ORTOGONAL 2x2 (TENSOR) ---
L = 1.7
rects = [
    (-L, 0, L, L, r"$\mathcal{T}_B[0,0]$"), 
    (0, 0, L, L, r"$\mathcal{T}_B[0,1]$"),  
    (-L, -L, L, L, r"$\mathcal{T}_B[1,0]$"), 
    (0, -L, L, L, r"$\mathcal{T}_B[1,1]$")   
]

for x, y, w, h, label in rects:
    rect = patches.Rectangle((center_grid[0] + x, center_grid[1] + y), w, h,
                             facecolor=c_fill, edgecolor=c_active, lw=2.5, zorder=2)
    ax.add_patch(rect)
    ax.text(center_grid[0] + x + w/2, center_grid[1] + y + h/2, label, 
            fontsize=15, color=c_active, ha='center', va='center', zorder=4)

ax.text(center_grid[0], center_grid[1] + L + 1.0, r"$\mathcal{T}_B$", 
        fontsize=24, color=c_active, ha='center', va='center', weight='bold')

# --- 4. ARISTAS INACTIVAS (DEGENERADAS) ---
ax.plot([center_grid[0] - L, center_grid[0]], [center_grid[1] + L, center_grid[1] + L], 
        color=c_inactive, lw=5, ls=':', dash_capstyle='round', zorder=5)

ax.plot([center_grid[0], center_grid[0] + L], [center_grid[1] - L, center_grid[1] - L], 
        color=c_inactive, lw=5, ls=':', dash_capstyle='round', zorder=5)

# --- 5. VECTORES DEL BLOQUE 2x2 ---
grid_vecs = [
    (L/2, L, r"$NE$"),
    (L, L/2, r"$E$"),
    (L, -L/2, r"$SE$"),
    (-L/2, -L, r"$SW$"),
    (-L, -L/2, r"$W$"),
    (-L, L/2, r"$NW$")
]

for vx, vy, label in grid_vecs:
    start_x, start_y = center_grid[0], center_grid[1]
    end_x = start_x + vx * 1.5 
    end_y = start_y + vy * 1.5
    
    ax.arrow(start_x, start_y, end_x - start_x, end_y - start_y, 
             head_width=0.2, head_length=0.25, 
             fc=c_active, ec=c_active, zorder=3, length_includes_head=True)
    
    tx = start_x + vx * 1.85
    ty = start_y + vy * 1.85
    ax.text(tx, ty, label, fontsize=16, color=c_active, ha='center', va='center', zorder=4)

# --- 6. ANOTACIÓN DE ARISTAS INACTIVAS ---
text_x, text_y = center_grid[0] - 3.2, -3.2
ax.text(text_x, text_y, "Aristas inactivas\n(conservación de simetría)", 
        fontsize=14, color=c_inactive, ha='center', va='center', 
        bbox=dict(facecolor=c_bg, edgecolor=c_inactive, boxstyle='round,pad=0.6', lw=1.5),
        zorder=5)

y_edge_top = center_grid[1] + L + 0.15 
ax.plot([text_x, text_x], [text_y + 0.6, y_edge_top], color=c_inactive, lw=2, zorder=4)
x_edge_top = center_grid[0] - L/2 
ax.annotate('', xy=(x_edge_top - 0.1, y_edge_top), xytext=(text_x, y_edge_top),
            arrowprops=dict(arrowstyle="->", color=c_inactive, lw=2))

x_edge_bottom = center_grid[0] + L/2 
ax.plot([text_x + 1.9, x_edge_bottom], [text_y, text_y], color=c_inactive, lw=2, zorder=4)
y_edge_bottom = center_grid[1] - L - 0.1 
ax.annotate('', xy=(x_edge_bottom, y_edge_bottom), xytext=(x_edge_bottom, text_y),
            arrowprops=dict(arrowstyle="->", color=c_inactive, lw=2))

# Ajuste fino de la vista
plt.xlim(-3.5, 14.5)
plt.ylim(-4.5, 4.5)

# Guardar figura
output_filename = "isomorfismo_2x2.pdf"
plt.savefig(output_filename, format='pdf', bbox_inches='tight')
print(f"Figura guardada exitosamente en: {output_filename}")
