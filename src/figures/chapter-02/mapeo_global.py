import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch

# Configuración de estilo LaTeX y paleta de colores académica
plt.rcParams.update({
    "text.usetex": False, # Se usa False para evitar dependencias locales de LaTeX, pero se emula perfectamente
    "mathtext.fontset": "cm", # Computer Modern para las matemáticas
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman", "Times New Roman", "serif"],
    "font.size": 12
})

# Paleta de colores estricta
COLOR_BG = "#EFEFEF"      # Gris claro (Células inactivas)
COLOR_TEXT = "#2C3E50"    # Azul oscuro (Ejes, textos, líneas principales)
COLOR_NEIGHBOR = "#D4E6F1" # Azul claro (Vecindad de Moore)
COLOR_CENTER = "#7B241C"  # Rojo oscuro (Célula central / Estado futuro)

def draw_grid(ax, cx, cy, rows, cols, cell_size=0.5, facecolors=None, edgecolor=COLOR_TEXT, alpha=1.0):
    """
    Dibuja una retícula bidimensional centrada en (cx, cy).
    Retorna un diccionario con las coordenadas de los centros de cada célula.
    """
    start_x = cx - (cols * cell_size) / 2
    start_y = cy - (rows * cell_size) / 2
    centers = {}
    
    for r in range(rows):
        for c in range(cols):
            x = start_x + c * cell_size
            # Construcción Top-down
            y = start_y + (rows - 1 - r) * cell_size 
            color = facecolors.get((r, c), COLOR_BG) if facecolors else COLOR_BG
            rect = patches.Rectangle((x, y), cell_size, cell_size,
                                     linewidth=1.2, edgecolor=edgecolor, 
                                     facecolor=color, alpha=alpha, zorder=2)
            ax.add_patch(rect)
            centers[(r, c)] = (x + cell_size/2, y + cell_size/2)
            
    return centers

def draw_fancy_arrow(ax, posA, posB, text="", rad=0.0, color=COLOR_TEXT, lw=2.0, mutation_scale=15):
    """ Dibuja una flecha direccional con soporte para curvatura (rad). """
    arrow = FancyArrowPatch(posA, posB, connectionstyle=f"arc3,rad={rad}",
                            arrowstyle="-|>", mutation_scale=mutation_scale, 
                            color=color, lw=lw, zorder=3)
    ax.add_patch(arrow)
    if text:
        mx, my = (posA[0] + posB[0]) / 2, (posA[1] + posB[1]) / 2
        ax.text(mx, my + 0.3, text, ha='center', va='center', 
                color=color, fontsize=14, zorder=4)

def main():
    # 1. Configuración del lienzo (Sin ejes para un look de diagrama puro)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Límites del lienzo conceptual
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # =========================================================================
    # PARTE MACROSCÓPICA: Mapeo Global (G)
    # =========================================================================
    
    # Lógica de colores para la Configuración Global C_t
    fc_global_ct = {}
    for r in range(5):
        for c in range(5):
            if r == 2 and c == 2:
                fc_global_ct[(r, c)] = COLOR_CENTER
            elif 1 <= r <= 3 and 1 <= c <= 3:
                fc_global_ct[(r, c)] = COLOR_NEIGHBOR
                
    # Lógica de colores para la Configuración Global C_t+1
    fc_global_ct1 = {(2, 2): COLOR_CENTER}
    
    # Dibujo de las retículas globales completas
    draw_grid(ax, cx=2.5, cy=7.5, rows=5, cols=5, cell_size=0.5, facecolors=fc_global_ct)
    draw_grid(ax, cx=7.5, cy=7.5, rows=5, cols=5, cell_size=0.5, facecolors=fc_global_ct1)
    
    # Etiquetas de la sección Macroscópica
    ax.text(2.5, 9.1, r"Configuración global $\mathcal{C}_t$", ha='center', fontsize=14, color=COLOR_TEXT)
    ax.text(7.5, 9.1, r"Configuración global $\mathcal{C}_{t+1}$", ha='center', fontsize=14, color=COLOR_TEXT)
    
    # Flecha del mapeo global G
    draw_fancy_arrow(ax, (3.9, 7.5), (6.1, 7.5), text=r"Mapeo Global $G$", rad=0)

    # Cajas demarcadoras (Zooming context)
    ax.add_patch(patches.Rectangle((1.75, 6.75), 1.5, 1.5, fill=False, edgecolor=COLOR_CENTER, lw=2, ls='--', zorder=4))
    ax.add_patch(patches.Rectangle((7.25, 7.25), 0.5, 0.5, fill=False, edgecolor=COLOR_CENTER, lw=2, ls='--', zorder=4))

    # =========================================================================
    # PARTE MICROSCÓPICA: Función de Transición Local (\delta)
    # =========================================================================
    
    # Retícula ampliada de la vecindad de Moore (3x3)
    fc_local_ct = {}
    for r in range(3):
        for c in range(3):
            fc_local_ct[(r, c)] = COLOR_CENTER if (r == 1 and c == 1) else COLOR_NEIGHBOR
            
    draw_grid(ax, cx=2.5, cy=3.0, rows=3, cols=3, cell_size=0.7, facecolors=fc_local_ct)
    
    # Célula individual ampliada en t+1
    draw_grid(ax, cx=7.5, cy=3.0, rows=1, cols=1, cell_size=0.7, facecolors={(0,0): COLOR_CENTER})
    
    # Operador central \delta
    circle_delta = patches.Circle((5.0, 3.0), radius=0.45, facecolor=COLOR_BG, edgecolor=COLOR_TEXT, lw=2, zorder=5)
    ax.add_patch(circle_delta)
    ax.text(5.0, 3.0, r"$\delta$", ha='center', va='center', fontsize=18, color=COLOR_TEXT, zorder=6)
    
    # Flechas convergentes desde la vecindad hacia \delta
    # Simulamos el flujo de información local curvando las flechas desde el borde de la vecindad
    draw_fancy_arrow(ax, (3.6, 3.7), (4.6, 3.3), rad=-0.2, lw=1.5, mutation_scale=12)
    draw_fancy_arrow(ax, (3.6, 3.0), (4.5, 3.0), rad=0.0, lw=1.5, mutation_scale=12)
    draw_fancy_arrow(ax, (3.6, 2.3), (4.6, 2.7), rad=0.2, lw=1.5, mutation_scale=12)
    
    # Flecha divergente desde \delta hacia el nuevo estado
    draw_fancy_arrow(ax, (5.5, 3.0), (7.0, 3.0), rad=0.0, lw=2, mutation_scale=15)
    
    # Etiquetas de la sección Microscópica
    ax.text(2.5, 1.6, r"Vecindad local $N(c)$", ha='center', fontsize=13, color=COLOR_TEXT)
    ax.text(5.0, 2.2, r"Función local", ha='center', fontsize=12, color=COLOR_TEXT)
    ax.text(7.5, 1.6, r"Estado futuro $\sigma_c^{t+1}$", ha='center', fontsize=13, color=COLOR_TEXT)

    # =========================================================================
    # INTEGRACIÓN VISUAL: Líneas de proyección (Topológico -> Algebraico)
    # =========================================================================
    
    # Conexiones punteadas para la extracción de la vecindad (C_t)
    ax.plot([1.75, 1.45], [6.75, 4.05], ls=':', color=COLOR_TEXT, alpha=0.6, lw=1.5)
    ax.plot([3.25, 3.55], [6.75, 4.05], ls=':', color=COLOR_TEXT, alpha=0.6, lw=1.5)
    
    # Conexiones punteadas para la extracción del estado futuro (C_t+1)
    ax.plot([7.25, 7.15], [7.25, 3.35], ls=':', color=COLOR_TEXT, alpha=0.6, lw=1.5)
    ax.plot([7.75, 7.85], [7.25, 3.35], ls=':', color=COLOR_TEXT, alpha=0.6, lw=1.5)

    # 2. Renderizado y Guardado
    plt.tight_layout()
    output_filename = "mapeo_global.pdf"
    plt.savefig(output_filename, format="pdf", bbox_inches="tight", dpi=300)
    print(f"Figura teórica generada exitosamente y guardada como: {output_filename}")

if __name__ == "__main__":
    main()