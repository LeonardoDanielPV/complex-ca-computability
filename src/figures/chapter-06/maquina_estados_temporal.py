import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as mpath
import os

# Configuración
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['text.color'] = '#2C3E50'

COLOR_BG = "#EFEFEF"
COLOR_NODE_BG = "#D4E6F1"
COLOR_NODE_EDGE = "#2C3E50"
COLOR_ARROW = "#7B241C"

fig, ax = plt.subplots(figsize=(8, 6), facecolor=COLOR_BG)
ax.set_facecolor(COLOR_BG)
ax.axis('off')

# Establecer límites para mantener aspecto
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')

# Coordenadas de los nodos
nodes = {
    'Paused': (0.3, 0.7),
    'Running': (0.7, 0.7),
    'Step': (0.5, 0.3)
}

node_w = 0.22
node_h = 0.12

def add_node(name, center):
    x, y = center
    box = patches.FancyBboxPatch(
        (x - node_w/2, y - node_h/2),
        node_w, node_h,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        edgecolor=COLOR_NODE_EDGE,
        facecolor=COLOR_NODE_BG,
        linewidth=2,
        zorder=3
    )
    ax.add_patch(box)
    ax.text(x, y, name, ha='center', va='center', fontsize=14, zorder=4, weight='bold')

for name, pos in nodes.items():
    add_node(name, pos)

# Estado inicial
init_x, init_y = 0.05, 0.7
circle = patches.Circle((init_x, init_y), radius=0.015, color=COLOR_NODE_EDGE, zorder=3)
ax.add_patch(circle)

# Flecha estado inicial
arrow_init = patches.FancyArrowPatch(
    (init_x, init_y), (nodes['Paused'][0] - node_w/2, nodes['Paused'][1]),
    connectionstyle="arc3,rad=0",
    color=COLOR_NODE_EDGE,
    arrowstyle="-|>,head_length=8,head_width=4",
    linewidth=2,
    zorder=2
)
ax.add_patch(arrow_init)

def add_edge(start, end, text, rad, text_pos):
    pA = nodes[start]
    pB = nodes[end]
    
    arrow = patches.FancyArrowPatch(
        pA, pB,
        connectionstyle=f"arc3,rad={rad}",
        color=COLOR_ARROW,
        arrowstyle="-|>,head_length=8,head_width=4",
        linewidth=1.5,
        zorder=2,
        shrinkA=35,
        shrinkB=35
    )
    ax.add_patch(arrow)
    
    bbox_props = dict(boxstyle="round,pad=0.2", fc=COLOR_BG, ec="none")
    ax.text(text_pos[0], text_pos[1], text,
            ha='center', va='center', fontsize=10, family='monospace', style='italic',
            bbox=bbox_props, zorder=5)

# Transiciones
add_edge('Paused', 'Running', 'play() / start_loop()', -0.2, (0.5, 0.81))
add_edge('Running', 'Paused', 'pause() / halt_loop()', -0.2, (0.5, 0.59))

add_edge('Paused', 'Step', 'advance() / tick++', -0.2, (0.33, 0.48))
add_edge('Step', 'Paused', '[tick_completed]', -0.2, (0.47, 0.52))

# Auto-transición en Running
pC = nodes['Running']
x0, y0 = pC[0] + node_w/2 - 0.01, pC[1]
path_data = [
    (mpath.Path.MOVETO, (x0, y0 + 0.02)),
    (mpath.Path.CURVE4, (x0 + 0.15, y0 + 0.1)),
    (mpath.Path.CURVE4, (x0 + 0.15, y0 - 0.1)),
    (mpath.Path.CURVE4, (x0, y0 - 0.02))
]
codes, verts = zip(*path_data)
path = mpath.Path(verts, codes)
patch = patches.FancyArrowPatch(path=path,
                                color=COLOR_ARROW,
                                arrowstyle="-|>,head_length=8,head_width=4",
                                linewidth=1.5,
                                zorder=2)
ax.add_patch(patch)
bbox_props = dict(boxstyle="round,pad=0.2", fc=COLOR_BG, ec="none")
ax.text(x0 + 0.08, y0, 'compute_next_generation()',
        ha='left', va='center', fontsize=10, family='monospace', style='italic',
        bbox=bbox_props, zorder=5)

plt.tight_layout()
output_path = os.path.join(os.path.dirname(__file__), 'maquina_estados_temporal.pdf')
plt.savefig(output_path, format='pdf', bbox_inches='tight', facecolor="#FFFFFF")
print(f"Generado exitosamente en: {output_path}")
