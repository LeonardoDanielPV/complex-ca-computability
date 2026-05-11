import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Configuración para que el texto luzca como LaTeX usando la fuente Times New Roman
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['mathtext.fontset'] = 'cm'  # Fuente Computer Modern para matemáticas

def generar_figura():
    fig, ax = plt.subplots(figsize=(10, 10))

    # 1. Geometría y Estructura Base (5x5 macro-bloques)
    n_blocks = 5
    ax.set_xlim(-1, n_blocks + 1)
    ax.set_ylim(-1, n_blocks + 2)
    ax.set_aspect('equal')
    ax.axis('off')

    # Paleta de colores
    color_border = "#2C3E50"
    color_inactive_bg = "#EFEFEF"
    color_active_bg = "#FFFFFF"
    color_microgrid = "#D4E6F1"
    color_active_cell = "#7B241C"

    # Bloques activos (5 macro-bloques contiguos en la zona inferior derecha/centro)
    # Seleccionamos: (3,1), (4,1), (3,2), (4,2), (4,3)
    active_blocks = [(3, 1), (4, 1), (3, 2), (4, 2), (4, 3)]

    # Posiciones para las etiquetas H(R_i) = 0
    h_r_i_positions = [(1, 4), (0, 1), (2, 3), (1, 0)]
    # Posiciones para las etiquetas H(R_j) > 0
    h_r_j_positions = [(3, 1), (4, 2)]

    # Dibujar la cuadrícula
    for x in range(n_blocks):
        for y in range(n_blocks):
            is_active = (x, y) in active_blocks
            
            # Fondo del bloque
            bg_color = color_active_bg if is_active else color_inactive_bg
            
            # 1. Rectángulo de fondo
            rect_bg = patches.Rectangle((x, y), 1, 1, facecolor=bg_color, edgecolor='none')
            ax.add_patch(rect_bg)
            
            # 2. Patrón de rayado para inactivos
            if not is_active:
                rect_hatch = patches.Rectangle((x, y), 1, 1, facecolor='none', edgecolor='#D0D0D0', hatch='///', linewidth=0)
                ax.add_patch(rect_hatch)
                
            # 3. Micro-cuadrícula para activos
            if is_active:
                micro_steps = 5
                step = 1.0 / micro_steps
                for mx in range(1, micro_steps):
                    # Líneas verticales de micro-celdas
                    ax.plot([x + mx*step, x + mx*step], [y, y + 1], color=color_microgrid, linestyle=':', linewidth=1)
                    # Líneas horizontales de micro-celdas
                    ax.plot([x, x + 1], [y + mx*step, y + mx*step], color=color_microgrid, linestyle=':', linewidth=1)
                    
            # 4. Borde del macro-bloque (siempre encima)
            rect_border = patches.Rectangle((x, y), 1, 1, facecolor='none', edgecolor=color_border, linewidth=1.5)
            ax.add_patch(rect_border)

    # 2. Etiquetas H(R_i) = 0
    for px, py in h_r_i_positions:
        ax.text(px + 0.5, py + 0.5, r'$H(R_i) = 0$', color=color_border, 
                ha='center', va='center', fontsize=14, 
                bbox=dict(facecolor='#EFEFEF', edgecolor='none', alpha=0.9, pad=2))

    # 3. Etiquetas H(R_j) > 0
    for px, py in h_r_j_positions:
        ax.text(px + 0.5, py + 0.5, r'$H(R_j) > 0$', color=color_active_cell, 
                ha='center', va='center', fontsize=14, fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=2))

    # Función para iluminar micro-celdas
    def draw_micro_cell(mx, my, color):
        macro_x = int(mx // 5)
        macro_y = int(my // 5)
        if (macro_x, macro_y) in active_blocks:
            x_pos = mx * 0.2
            y_pos = my * 0.2
            rect = patches.Rectangle((x_pos, y_pos), 0.2, 0.2, facecolor=color, edgecolor=color_microgrid, linewidth=0.5)
            ax.add_patch(rect)

    # Coordenadas de micro-celdas para patrón Beehive alrededor del bloque (3, 1) -> (15-19, 5-9)
    beehive_cells = [
        (17, 7), (18, 7),
        (16, 6), (19, 6),
        (17, 5), (18, 5)
    ]

    for cx, cy in beehive_cells:
        draw_micro_cell(cx, cy, color_active_cell)
        
    # Patrón extra (glider en fase de evolución) en el bloque (4, 3) -> (20-24, 15-19)
    glider_cells = [
        (22, 17),
        (23, 16),
        (21, 15), (22, 15), (23, 15)
    ]
    for cx, cy in glider_cells:
        draw_micro_cell(cx, cy, color_active_cell)

    # 4. Anotaciones Lógicas y Flechas de Flujo
    
    # Flecha de Omisión (Bypass)
    # Origen: arriba a la izquierda, apunta a un bloque gris en (1, 4)
    ax.annotate(r'Bypass de Memoria: $\mathcal{O}(1)$ R/W', 
                xy=(1.5, 4.5), xycoords='data',
                xytext=(1.0, 6.0), textcoords='data',
                arrowprops=dict(arrowstyle="->", color=color_border, lw=2,
                                connectionstyle="arc3,rad=-0.2"),
                ha='center', va='center', fontsize=12,
                bbox=dict(boxstyle="round,pad=0.5", facecolor='white', edgecolor=color_border, lw=1, alpha=0.9))

    # Flecha de Procesamiento (Evaluación Activa)
    # Origen: arriba a la derecha, apunta al clúster Beehive en (3.5, 1.5)
    ax.annotate(r'Evaluación Activa del Motor:' + '\n' + r'Actualización en $\mathcal{O}(k)$', 
                xy=(3.5, 1.8), xycoords='data',
                xytext=(4.5, 6.0), textcoords='data',
                arrowprops=dict(arrowstyle="->", color=color_active_cell, lw=2,
                                connectionstyle="arc3,rad=0.15"),
                ha='center', va='center', fontsize=12,
                bbox=dict(boxstyle="round,pad=0.5", facecolor='white', edgecolor=color_active_cell, lw=1, alpha=0.9))

    # Guardar figura
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "particionamiento_espacial.pdf")
    plt.tight_layout()
    plt.savefig(output_path, format='pdf', dpi=300, bbox_inches='tight', transparent=True)
    plt.close(fig)
    print(f"Figura generada con éxito en: {output_path}")

if __name__ == "__main__":
    generar_figura()
