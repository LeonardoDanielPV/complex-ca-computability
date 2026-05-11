import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import rcParams

# Configuración de tipografía académica
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']
# Se usa 'stix' para renderizar matemáticas con aspecto similar a Times New Roman/LaTeX 
# sin depender de una instalación externa completa de TeX.
rcParams['mathtext.fontset'] = 'stix'

# Crear figura con proporciones cuadradas
fig, ax = plt.subplots(figsize=(6, 6))

# 1. Definición de Nodos (Posiciones)
nodes = {
    'CH_t': (0.25, 0.75),
    'CH_t1': (0.75, 0.75),
    'CQ_t': (0.25, 0.25),
    'CQ_t1': (0.75, 0.25)
}

# Etiquetas de los Nodos
labels = {
    'CH_t': r'$\mathcal{C}_{\mathcal{H}}(t)$',
    'CH_t1': r'$\mathcal{C}_{\mathcal{H}}(t+1)$',
    'CQ_t': r'$\mathcal{C}_{\mathcal{Q}}(t)$',
    'CQ_t1': r'$\mathcal{C}_{\mathcal{Q}}(t+1)$'
}

# Paleta de colores rigurosa/académica
colors = {
    'node_bg': '#EFEFEF',      # Fondo del nodo
    'node_edge': '#2C3E50',    # Borde del nodo
    'node_text': '#2C3E50',    # Texto del nodo
    'arrow': '#2C3E50',        # Flechas de flujo
    'func_label': '#7B241C'    # Funciones de transición (destacadas)
}

# Dimensiones base para las cajas contenedoras
box_width = 0.18
box_height = 0.12

# Dibujar Nodos (Cajas con esquinas redondeadas)
for key, (x, y) in nodes.items():
    # Caja contenedora
    bbox = patches.FancyBboxPatch(
        (x - box_width/2, y - box_height/2),
        box_width, box_height,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        ec=colors['node_edge'], fc=colors['node_bg'], lw=1.5, zorder=3
    )
    ax.add_patch(bbox)
    
    # Texto matemático del nodo
    ax.text(x, y, labels[key], ha='center', va='center', fontsize=20, 
            color=colors['node_text'], zorder=4)

# 2. Vectores (Flechas de flujo)
def add_arrow(start, end, label, offset_x=0, offset_y=0):
    """Función para dibujar flechas que conectan los bordes de los nodos."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    
    # Margen para que las flechas no atraviesen las cajas
    gap_x = (box_width / 2 + 0.03) if dx != 0 else 0
    gap_y = (box_height / 2 + 0.03) if dy != 0 else 0
    
    start_adj = (start[0] + gap_x * (1 if dx > 0 else -1 if dx < 0 else 0), 
                 start[1] + gap_y * (1 if dy > 0 else -1 if dy < 0 else 0))
    end_adj = (end[0] - gap_x * (1 if dx > 0 else -1 if dx < 0 else 0), 
               end[1] - gap_y * (1 if dy > 0 else -1 if dy < 0 else 0))
               
    # Dibujar la flecha
    arrow = patches.FancyArrowPatch(
        start_adj, end_adj,
        arrowstyle='-|>', mutation_scale=20, lw=1.5, color=colors['arrow'], zorder=2
    )
    ax.add_patch(arrow)
    
    # Posicionar la etiqueta de la flecha
    mid_x = (start_adj[0] + end_adj[0]) / 2 + offset_x
    mid_y = (start_adj[1] + end_adj[1]) / 2 + offset_y
    ax.text(mid_x, mid_y, label, ha='center', va='center', fontsize=20, 
            color=colors['func_label'])

# Horizontal Superior
add_arrow(nodes['CH_t'], nodes['CH_t1'], r'$\Phi_H$', offset_y=0.06)

# Horizontal Inferior
add_arrow(nodes['CQ_t'], nodes['CQ_t1'], r'$\Phi_Q$', offset_y=-0.06)

# Vertical Izquierda
add_arrow(nodes['CH_t'], nodes['CQ_t'], r'$\Psi$', offset_x=-0.06)

# Vertical Derecha
add_arrow(nodes['CH_t1'], nodes['CQ_t1'], r'$\Psi$', offset_x=0.06)

# 3. Detalles Simbólicos y Estética Central
center_x = (nodes['CH_t'][0] + nodes['CH_t1'][0]) / 2
center_y = (nodes['CH_t'][1] + nodes['CQ_t'][1]) / 2

# Símbolo de congruencia
ax.text(center_x, center_y + 0.05, r'$\cong$', ha='center', va='center', 
        fontsize=32, color=colors['node_edge'])
# Ecuación del diagrama conmutativo
ax.text(center_x, center_y - 0.06, r'$\Psi \circ \Phi_H = \Phi_Q \circ \Psi$', 
        ha='center', va='center', fontsize=16, color=colors['node_edge'])

# 4. Composición
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')  # Mantener proporciones geométricas
ax.axis('off')          # Apagar cuadrículas y ejes

plt.tight_layout()

# Guardar la figura en la misma ruta que el script
output_filename = 'diagrama_conmutativo.pdf'
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_filename)

plt.savefig(output_path, format='pdf', bbox_inches='tight', pad_inches=0.0)
print(f"El diagrama se ha generado y guardado exitosamente en:\n{output_path}")
