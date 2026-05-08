import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuración global para emular tipografía rigurosa de LaTeX
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'stix',
    'axes.linewidth': 1.5
})

def generar_espacio_fases():
    # Inicialización del lienzo: aspect ratio estricto y sin ejes
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_aspect('equal')
    ax.axis('off')

    # Paleta de colores académica solicitada
    c_bg = "#EFEFEF"         # Fondo genérico de nodos transitorios
    c_border = "#2C3E50"     # Bordes y flechas deterministas
    c_attractor = "#D4E6F1"  # Fondo distintivo para estados atractor
    c_accent = "#7B241C"     # Acento sobrio para el punto fijo

    r = 0.35  # Radio uniforme de los nodos

    # Definición estructurada de los nodos en el plano coordenado
    # Formato: id: (x, y, etiqueta_matemática, es_atractor, color_borde)
    nodes = {
        # --- Dinámica 1: Punto Fijo y su cuenca de atracción ---
        'Cf': (-3.5, 0, r'$\mathcal{C}_f$', True, c_accent),
        'C1': (-6, 1.5, r'$\mathcal{C}_1$', False, c_border),
        'C2': (-4.8, 0.9, r'$\mathcal{C}_2$', False, c_border),
        'C3': (-6, -1.5, r'$\mathcal{C}_3$', False, c_border),
        'C4': (-4.8, -0.9, r'$\mathcal{C}_4$', False, c_border),
        'C5': (-6.5, 0, r'$\mathcal{C}_5$', False, c_border),
        'C6': (-5.0, 0, r'$\mathcal{C}_6$', False, c_border),

        # --- Dinámica 2: Ciclo Límite (p=4) y su cuenca ---
        'L1': (3.5, 1.3, r'$\mathcal{C}_{L1}$', True, c_border),
        'L2': (4.8, 0, r'$\mathcal{C}_{L2}$', True, c_border),
        'L3': (3.5, -1.3, r'$\mathcal{C}_{L3}$', True, c_border),
        'L4': (2.2, 0, r'$\mathcal{C}_{L4}$', True, c_border),
        
        # Ramas transitorias convergiendo al ciclo límite
        'T1': (3.5, 2.8, r'$\mathcal{C}_{7}$', False, c_border),
        'T2': (6.3, 0, r'$\mathcal{C}_{8}$', False, c_border),
        'T3': (3.5, -2.8, r'$\mathcal{C}_{9}$', False, c_border),
        'T4': (0.7, 0, r'$\mathcal{C}_{10}$', False, c_border),
        'T5': (5.2, 1.6, r'$\mathcal{C}_{11}$', False, c_border),
        'T6': (5.2, -1.6, r'$\mathcal{C}_{12}$', False, c_border)
    }

    circle_patches = {}

    # 1. Trazar Nodos (Soporte Finito del Espacio de Fases)
    for key, (x, y, label, is_att, b_color) in nodes.items():
        face_color = c_attractor if is_att else c_bg
        lw = 2.0 if is_att else 1.5
        
        # Circunferencia del nodo
        circle = patches.Circle((x, y), r, facecolor=face_color, edgecolor=b_color, lw=lw, zorder=3)
        ax.add_patch(circle)
        circle_patches[key] = circle
        
        # Etiqueta de la Configuración en LaTeX
        ax.text(x, y, label, ha='center', va='center', fontsize=12, color=b_color, zorder=4)

    # 2. Trazar Transiciones Dinámicas Globales G (Aristas)
    # Formato: (origen, destino, curvatura_radial)
    edges = [
        # Cuenca del Punto Fijo
        ('C1', 'C2', 0.1), ('C2', 'Cf', 0.1),
        ('C3', 'C4', -0.1), ('C4', 'Cf', -0.1),
        ('C5', 'C6', 0.0), ('C6', 'Cf', 0.0),
        
        # Flujo Secuencial del Ciclo Límite (curvatura positiva = abombado exterior)
        ('L1', 'L2', 0.25), ('L2', 'L3', 0.25),
        ('L3', 'L4', 0.25), ('L4', 'L1', 0.25),
        
        # Cuenca del Ciclo Límite
        ('T1', 'L1', 0.0), ('T2', 'L2', 0.0),
        ('T3', 'L3', 0.0), ('T4', 'L4', 0.0),
        ('T5', 'L1', -0.15), ('T6', 'L3', 0.15)
    ]

    for src, dst, rad in edges:
        p1 = circle_patches[src]
        p2 = circle_patches[dst]
        
        # Uso avanzado de FancyArrowPatch conectando exactamente las fronteras de los nodos
        arrow = patches.FancyArrowPatch(
            p1.center, p2.center,
            connectionstyle=f"arc3,rad={rad}",
            patchA=p1, patchB=p2,
            shrinkA=1, shrinkB=1,  # Padding milimétrico respecto al borde
            arrowstyle='-|>', mutation_scale=16,
            color=c_border, lw=1.5, zorder=2
        )
        ax.add_patch(arrow)

    # 3. Dibujar Self-Loop Determinista para el Punto Fijo
    x_c, y_c = nodes['Cf'][0], nodes['Cf'][1]
    start_x, start_y = x_c - r*0.6, y_c + r*0.7
    end_x, end_y = x_c + r*0.6, y_c + r*0.7
    
    ax.annotate('', xy=(end_x, end_y), xycoords='data',
                xytext=(start_x, start_y), textcoords='data',
                arrowprops=dict(arrowstyle="-|>", color=c_accent, lw=1.8,
                                connectionstyle="arc3,rad=1.6",
                                shrinkA=0, shrinkB=0, mutation_scale=16),
                zorder=2)
    
    # Ecuación del operador global G para asintotas
    ax.text(x_c, y_c + r + 0.65, r'$G(\mathcal{C}_f) = \mathcal{C}_f$', 
            ha='center', va='center', color=c_accent, fontsize=13, fontweight='bold')

    # 4. Anotaciones Académicas (Etiquetas y Estructuras)
    # Identificador: Punto Fijo
    ax.text(-3.5, -3.5, "Punto Fijo\n" + r"($p=1$)", ha='center', va='top', fontsize=14)
    ax.text(-3.5, -4.3, r"Cuenca de atracción $\mathcal{B}(\mathcal{C}_f)$", ha='center', va='top', fontsize=13, color='#5D6D7E', fontstyle='italic')

    # Identificador: Ciclo Límite
    ax.text(3.5, -3.5, "Ciclo Límite\n" + r"($p=4$)", ha='center', va='top', fontsize=14)
    ax.text(3.5, -4.3, r"Cuenca de atracción $\mathcal{B}(\mathcal{C}_{L})$", ha='center', va='top', fontsize=13, color='#5D6D7E', fontstyle='italic')

    # Limites del lienzo
    ax.set_xlim(-7.5, 7.5)
    ax.set_ylim(-4, 4)

    # 5. Exportar el diagrama vectorizado nativo para LaTeX
    plt.savefig("espacio_fases.pdf", format='pdf', bbox_inches='tight')
    print("Gráfica generada con éxito: espacio_fases.pdf")

if __name__ == '__main__':
    generar_espacio_fases()