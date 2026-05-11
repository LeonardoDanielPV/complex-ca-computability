import matplotlib.pyplot as plt
import matplotlib.patches as patches

def crear_diagrama():
    # Lienzo con proporciones ajustadas para evitar deformación
    fig, ax = plt.subplots(figsize=(11, 12))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Configuración tipográfica para estándar académico (ej. IEEE/ACM/Springer)
    plt.rcParams["font.family"] = "serif"
    font_main = {'fontname': 'Times New Roman', 'fontsize': 13, 'fontweight': 'bold'}
    font_sub = {'fontname': 'Times New Roman', 'fontsize': 11}
    font_annot = {'fontname': 'Times New Roman', 'fontsize': 12, 'fontstyle': 'italic'}
    font_iso = {'fontname': 'Times New Roman', 'fontsize': 11, 'fontweight': 'bold'}

    # Dimensiones maestras de las cajas jerárquicas
    boxes_x = 2.5
    boxes_w = 6.0

    # Coordenadas Y (De abajo hacia arriba: Capa 1 -> Capa 4)
    y1 = 1.0; h1 = 2.5
    y2 = 3.8; h2 = 2.0
    y_iso = 6.2
    y3 = 6.6; h3 = 2.0
    y4 = 8.9; h4 = 2.0

    # =========================================================
    # Capa 1: Núcleo Algebraico de Simulación
    # =========================================================
    ax.add_patch(patches.Rectangle((boxes_x, y1), boxes_w, h1, facecolor="#D4E6F1", edgecolor="#1C2833", lw=1.5))
    ax.text(boxes_x + boxes_w/2, y1 + h1 - 0.35, "Capa 1: Núcleo Algebraico de Simulación", ha='center', va='center', color='black', **font_main)
    
    sb_y = y1 + 0.25
    sb_h = h1 - 0.8
    sb_w = 1.7
    spacing = (boxes_w - 3*sb_w) / 4
    for i, txt in enumerate(["Estructura Matrical\n(GridStorage)", "Funciones de Transición\nDiscreta", "Memoria\n(Double Buffering)"]):
        sb_x = boxes_x + spacing + i*(sb_w + spacing)
        ax.add_patch(patches.Rectangle((sb_x, sb_y), sb_w, sb_h, facecolor="white", edgecolor="#1C2833", lw=1.0))
        ax.text(sb_x + sb_w/2, sb_y + sb_h/2, txt, ha='center', va='center', color='black', **font_sub)

    # =========================================================
    # Capa 2: Controlador de Flujo y Sincronización
    # =========================================================
    ax.add_patch(patches.Rectangle((boxes_x, y2), boxes_w, h2, facecolor="#EFEFEF", edgecolor="#1C2833", lw=1.5))
    ax.text(boxes_x + boxes_w/2, y2 + h2 - 0.35, "Capa 2: Controlador de Flujo y Sincronización", ha='center', va='center', color='black', **font_main)
    
    sb_y2 = y2 + 0.25
    sb_h2 = h2 - 0.8
    sb_w2 = 2.6
    spacing2 = (boxes_w - 2*sb_w2) / 3
    for i, txt in enumerate(["Bucle de Actualización\n(Ticks)", "Gestión de Instancias\nde Simulación"]):
        sb_x = boxes_x + spacing2 + i*(sb_w2 + spacing2)
        ax.add_patch(patches.Rectangle((sb_x, sb_y2), sb_w2, sb_h2, facecolor="white", edgecolor="#1C2833", lw=1.0))
        ax.text(sb_x + sb_w2/2, sb_y2 + sb_h2/2, txt, ha='center', va='center', color='black', **font_sub)

    # =========================================================
    # Línea de Aislamiento Estructural
    # =========================================================
    # Usamos linestyle con patrón (0, (2, 4)) y capstyle round para dar efecto de punteado avanzado
    ax.plot([boxes_x - 0.5, boxes_x + boxes_w + 0.5], [y_iso, y_iso], color="#7B241C", lw=3.0, linestyle=(0, (2, 4)), dash_capstyle='round')
    ax.text(boxes_x + boxes_w/2, y_iso + 0.15, "Frontera de Desacoplamiento (Aislamiento del Núcleo)", ha='center', va='bottom', color="#7B241C", **font_iso)

    # =========================================================
    # Capa 3: Mapeo Geométrico y Visualización Continua
    # =========================================================
    ax.add_patch(patches.Rectangle((boxes_x, y3), boxes_w, h3, facecolor="#2C3E50", edgecolor="#1C2833", lw=1.5))
    ax.text(boxes_x + boxes_w/2, y3 + h3 - 0.35, "Capa 3: Mapeo Geométrico y Visualización Continua", ha='center', va='center', color='white', **font_main)
    
    sb_y3 = y3 + 0.25
    sb_h3 = h3 - 0.8
    for i, txt in enumerate(["Motor de Renderizado\n(Viewport)", "Proyección Topológica"]):
        sb_x = boxes_x + spacing2 + i*(sb_w2 + spacing2)
        ax.add_patch(patches.Rectangle((sb_x, sb_y3), sb_w2, sb_h3, facecolor="none", edgecolor="white", lw=1.2))
        ax.text(sb_x + sb_w2/2, sb_y3 + sb_h3/2, txt, ha='center', va='center', color='white', **font_sub)

    # =========================================================
    # Capa 4: Administrador Global e Interfaz de Eventos
    # =========================================================
    ax.add_patch(patches.Rectangle((boxes_x, y4), boxes_w, h4, facecolor="#7B241C", edgecolor="#1C2833", lw=1.5))
    ax.text(boxes_x + boxes_w/2, y4 + h4 - 0.35, "Capa 4: Administrador Global e Interfaz de Eventos", ha='center', va='center', color='white', **font_main)
    
    sb_y4 = y4 + 0.25
    sb_h4 = h4 - 0.8
    for i, txt in enumerate(["Application Manager", "Entrada de Usuario\n(ImGui)"]):
        sb_x = boxes_x + spacing2 + i*(sb_w2 + spacing2)
        ax.add_patch(patches.Rectangle((sb_x, sb_y4), sb_w2, sb_h4, facecolor="none", edgecolor="white", lw=1.2))
        ax.text(sb_x + sb_w2/2, sb_y4 + sb_h4/2, txt, ha='center', va='center', color='white', **font_sub)

    # =========================================================
    # Flechas Relacionales Periféricas
    # =========================================================
    # Izquierda: Grafo de dependencias (Apunta hacia abajo)
    ax.annotate('', xy=(1.2, 1.0), xytext=(1.2, 10.9), arrowprops=dict(arrowstyle='-|>', lw=2.5, color='black', mutation_scale=20))
    ax.text(0.8, 5.95, "Grafo de Dependencias / Jerarquía de Control", rotation=90, ha='center', va='center', color='black', **font_annot)

    # Derecha: Flujo de datos (Apunta hacia arriba)
    ax.annotate('', xy=(9.8, 10.9), xytext=(9.8, 1.0), arrowprops=dict(arrowstyle='-|>', lw=2.5, color='black', mutation_scale=20))
    ax.text(10.2, 5.95, "Flujo de Datos (Lectura del Estado Matrical)", rotation=-90, ha='center', va='center', color='black', **font_annot)

    # Exportación con rigor académico (Se usa bbox_inches por defecto o omitido para respetar proporciones)
    plt.savefig("diagrama_arquitectura.pdf", format="pdf")
    print("Figura teórica guardada exitosamente como 'diagrama_arquitectura.pdf'")

if __name__ == "__main__":
    try:
        crear_diagrama()
    except Exception as e:
        print(f"Error generando el diagrama: {e}")
