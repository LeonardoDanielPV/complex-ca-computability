import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generar_diagrama_isomorfismo():
    # Configuración de tipografía matemática para emular el estilo LaTeX (Times/STIX)
    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.size'] = 12

    # Creación del lienzo con dimensiones calibradas (relación 16:10)
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off') # Se apagan los ejes para un estilo de diagrama puramente teórico

    # Paleta de colores académica
    C_FILL = "#EFEFEF"
    C_EDGE = "#2C3E50"
    C_HIGHLIGHT = "#D4E6F1"
    C_ACCENT = "#7B241C"

    # =========================================================================
    # 1. PANEL SUPERIOR: MODELO DE LA MÁQUINA DE TURING (MT)
    # =========================================================================
    mt_cell_w = 1.2
    mt_cell_h = 1.0
    mt_start_x = 2.0
    mt_start_y = 8.5
    num_cells = 7

    labels = ["...", r"$s_{i-2}$", r"$s_{i-1}$", r"$s_i$", r"$s_{i+1}$", r"$s_{i+2}$", "..."]

    # Renderizado de la Cinta Infinita
    for i in range(num_cells):
        x = mt_start_x + i * mt_cell_w
        rect = patches.Rectangle((x, mt_start_y), mt_cell_w, mt_cell_h, 
                                 facecolor=C_FILL, edgecolor=C_EDGE, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + mt_cell_w/2, mt_start_y + mt_cell_h/2, labels[i], 
                ha='center', va='center', fontsize=14)

    # Renderizado del Cabezal de Lectura/Escritura
    head_x = mt_start_x + 3 * mt_cell_w + mt_cell_w/2 # Centro de la celda i
    head_top_y = mt_start_y - 0.1
    head_bot_y = mt_start_y - 0.9
    head_w = 0.8
    
    triangle = patches.Polygon([[head_x, head_top_y], 
                                [head_x - head_w/2, head_bot_y], 
                                [head_x + head_w/2, head_bot_y]], 
                               closed=True, facecolor=C_ACCENT, edgecolor=C_EDGE)
    ax.add_patch(triangle)
    
    # Etiqueta de estado del cabezal
    ax.text(head_x, head_bot_y - 0.2, r"$q \in Q$", 
            ha='center', va='top', fontsize=14, color=C_ACCENT)

    # Ecuación y Título de la MT
    eq_mt_x = 13.5
    ax.text(eq_mt_x, mt_start_y + mt_cell_h, "Máquina de Turing (MT)", 
            ha='center', va='center', fontsize=14)
    ax.text(eq_mt_x, mt_start_y + mt_cell_h/2, 
            r"$\delta: Q \times \Gamma \rightarrow Q \times \Gamma \times \{L, R\}$", 
            ha='center', va='center', fontsize=16)


    # =========================================================================
    # 2. PANEL INFERIOR: AUTÓMATA CELULAR BIDIMENSIONAL (AC)
    # =========================================================================
    ca_cell_w = 0.6
    ca_rows = 7
    ca_cols = 11
    # Se ajusta ca_start_x para que el centro de la retícula se alinee con head_x
    center_col = 5
    center_row = 3
    ca_start_x = head_x - (center_col * ca_cell_w + ca_cell_w/2)
    ca_start_y = 0.5

    # Renderizado de la Retícula y la Vecindad de Moore
    for r in range(ca_rows):
        for c in range(ca_cols):
            x = ca_start_x + c * ca_cell_w
            y = ca_start_y + r * ca_cell_w
            
            # Subrayado topológico de la vecindad de Moore (3x3)
            if (center_row - 1 <= r <= center_row + 1) and (center_col - 1 <= c <= center_col + 1):
                facecolor = C_HIGHLIGHT
            else:
                facecolor = C_FILL
                
            rect = patches.Rectangle((x, y), ca_cell_w, ca_cell_w, 
                                     facecolor=facecolor, edgecolor=C_EDGE, 
                                     linewidth=0.5, alpha=0.8)
            ax.add_patch(rect)
            
            # Destacado del Locus Central
            if r == center_row and c == center_col:
                rect_center = patches.Rectangle((x, y), ca_cell_w, ca_cell_w, 
                                                fill=False, edgecolor=C_ACCENT, linewidth=2.5)
                ax.add_patch(rect_center)
                circle = patches.Circle((x + ca_cell_w/2, y + ca_cell_w/2), 
                                        radius=ca_cell_w/6, color=C_ACCENT)
                ax.add_patch(circle)

    # Ecuación y Título del AC
    eq_ca_y = ca_start_y + (ca_rows * ca_cell_w) / 2
    ax.text(eq_mt_x, ca_start_y + (ca_rows * ca_cell_w) - 1.5, "Autómata Celular (AC)", 
            ha='center', va='center', fontsize=14)
    ax.text(eq_mt_x, eq_ca_y, r"$\Phi: \Sigma^{|N|} \rightarrow \Sigma$", 
            ha='center', va='center', fontsize=16)


    # =========================================================================
    # 3. CONEXIONES DE ISOMORFISMO (MAPEO TOPOLÓGICO)
    # =========================================================================
    arrow_props = dict(arrowstyle="-|>", color=C_EDGE, ls="dashed", lw=1.8, mutation_scale=20)
    bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.9)

    # a) Isomorfismo Espacial (Memoria): Cinta -> Retícula
    start_1 = (mt_start_x + 1.5 * mt_cell_w, mt_start_y - 0.2)
    end_1 = (ca_start_x + 2 * ca_cell_w, ca_start_y + ca_rows * ca_cell_w + 0.2)
    ax.annotate("", xy=end_1, xytext=start_1, 
                arrowprops=dict(connectionstyle="arc3,rad=-0.15", **arrow_props))
    ax.text((start_1[0]+end_1[0])/2 - 0.4, (start_1[1]+end_1[1])/2, 
            "Isomorfismo Espacial\n(Memoria)", ha='right', va='center', fontsize=12)

    # b) Locus de Procesamiento: Cabezal -> Vecindad activa
    start_2 = (head_x, head_bot_y - 0.8)
    end_2 = (head_x, ca_start_y + ca_rows * ca_cell_w + 0.2)
    ax.annotate("", xy=end_2, xytext=start_2, 
                arrowprops=dict(connectionstyle="arc3,rad=0", **arrow_props))
    ax.text(head_x + 0.3, (start_2[1]+end_2[1])/2, 
            "Locus de\nProcesamiento", ha='left', va='center', fontsize=12, bbox=bbox_props)

    # c) Equivalencia de Transición Algorítmica: delta -> Phi
    start_3 = (eq_mt_x, mt_start_y - 0.6)
    end_3 = (eq_mt_x, eq_ca_y + 1.2)
    ax.annotate("", xy=end_3, xytext=start_3, 
                arrowprops=dict(connectionstyle="arc3,rad=0", **arrow_props))
    ax.text(eq_mt_x + 0.3, (start_3[1]+end_3[1])/2, 
            "Equivalencia de Transición\nAlgorítmica", ha='left', va='center', fontsize=12)

    # Guardar en vector (PDF) asegurando la limpieza de los bordes
    plt.savefig("equivalencia_turing.pdf", format="pdf", bbox_inches="tight")
    print("El archivo 'equivalencia_turing.pdf' se ha generado exitosamente.")

if __name__ == "__main__":
    generar_diagrama_isomorfismo()