import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

def generar_diagrama():
    # Configuración de fuente y estilo
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
    plt.rcParams['mathtext.fontset'] = 'stix'

    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 9))
    
    # Apagar los ejes como solicitado
    plt.axis('off')

    # Coordenadas X
    X_L = 0.2
    X_C = 0.5
    X_R = 0.8

    # Coordenadas Y
    Y_1 = 0.75  # Arriba
    Y_2 = 0.50  # Centro
    Y_3 = 0.25  # Abajo

    # Definición de Nodos
    nodes_data = {
        'C1': {'pos': (X_C, Y_1), 'text': 'Inicialización Topológica', 'bg': '#EFEFEF', 'edge': '#2C3E50', 'lw': 2.5, 'tc': '#2C3E50', 'fw': 'bold'},
        'C2': {'pos': (X_C, Y_2), 'text': 'Evaluación Algebraica\n(Motor de Transición)', 'bg': '#EFEFEF', 'edge': '#2C3E50', 'lw': 2.5, 'tc': '#2C3E50', 'fw': 'bold'},
        'C3': {'pos': (X_C, Y_3), 'text': 'Mapeo Geométrico\n(Viewport / Render)', 'bg': '#EFEFEF', 'edge': '#2C3E50', 'lw': 2.5, 'tc': '#2C3E50', 'fw': 'bold'},
        
        'L1': {'pos': (X_L, Y_1), 'text': 'Determinismo Espacial', 'bg': '#D4E6F1', 'edge': '#2C3E50', 'lw': 1.5, 'tc': '#2C3E50', 'fw': 'normal'},
        'L2': {'pos': (X_L, Y_2), 'text': 'Sincronización\nTemporal Estricta', 'bg': '#D4E6F1', 'edge': '#2C3E50', 'lw': 1.5, 'tc': '#2C3E50', 'fw': 'normal'},
        'L3': {'pos': (X_L, Y_3), 'text': 'Invarianza Topológica', 'bg': '#D4E6F1', 'edge': '#2C3E50', 'lw': 1.5, 'tc': '#2C3E50', 'fw': 'normal'},
        
        'R1': {'pos': (X_R, Y_1), 'text': 'Memoria de Doble\nBúfer ($\\mathcal{O}(n)$)', 'bg': '#FFFFFF', 'edge': '#7B241C', 'lw': 1.5, 'tc': '#2C3E50', 'fw': 'normal'},
        'R2': {'pos': (X_R, Y_2), 'text': 'Orquestación en Paralelo\n(SIMD / ECS)', 'bg': '#FFFFFF', 'edge': '#7B241C', 'lw': 1.5, 'tc': '#2C3E50', 'fw': 'normal'},
        'R3': {'pos': (X_R, Y_3), 'text': 'Desacoplamiento\nLógico-Visual', 'bg': '#FFFFFF', 'edge': '#7B241C', 'lw': 1.5, 'tc': '#2C3E50', 'fw': 'normal'},
    }

    box_w = 0.24
    box_h = 0.12

    # Diccionario para guardar los objetos patch creados
    patches_dict = {}

    # Dibujar Nodos
    for key, data in nodes_data.items():
        px, py = data['pos']
        # Rectángulo con bordes redondeados
        rect = patches.FancyBboxPatch(
            (px - box_w/2, py - box_h/2), box_w, box_h,
            boxstyle="round,pad=0.01,rounding_size=0.03",
            linewidth=data['lw'],
            edgecolor=data['edge'],
            facecolor=data['bg'],
            zorder=3
        )
        ax.add_patch(rect)
        patches_dict[key] = rect
        # Agregar el texto en el centro del nodo
        ax.text(px, py, data['text'], ha='center', va='center', fontsize=11, color=data['tc'], weight=data['fw'], zorder=4)

    # Títulos de las columnas
    ax.text(X_L, Y_1 + box_h/2 + 0.04, "Requerimientos\nFuncionales", ha='center', va='bottom', fontsize=12, color='#2C3E50', weight='bold')
    ax.text(X_C, Y_1 + box_h/2 + 0.04, "Ciclo de Vida de\nla Simulación", ha='center', va='bottom', fontsize=12, color='#2C3E50', weight='bold')
    ax.text(X_R, Y_1 + box_h/2 + 0.04, "Restricciones\nArquitectónicas", ha='center', va='bottom', fontsize=12, color='#7B241C', weight='bold')

    # Función auxiliar para dibujar conexiones entre nodos
    def draw_connection(start, end, style="arc3,rad=0.0", color='#2C3E50', lw=1.5, arrowstyle='-|>', linestyle='solid', z=2):
        xA, yA = nodes_data[start]['pos']
        xB, yB = nodes_data[end]['pos']
        
        arrow = patches.FancyArrowPatch(
            posA=(xA, yA), posB=(xB, yB),
            patchA=patches_dict[start], patchB=patches_dict[end],
            shrinkA=2, shrinkB=2,
            connectionstyle=style,
            arrowstyle=arrowstyle,
            color=color,
            linewidth=lw,
            linestyle=linestyle,
            mutation_scale=15,
            zorder=z
        )
        ax.add_patch(arrow)

    # Flujo central (Gruesas)
    draw_connection('C1', 'C2', lw=3.0)
    draw_connection('C2', 'C3', lw=3.0)

    # Izquierda a Centro
    draw_connection('L1', 'C1', style="arc3,rad=0.05")
    draw_connection('L2', 'C2', style="arc3,rad=0.05")
    draw_connection('L3', 'C3', style="arc3,rad=0.05")

    # Centro a Derecha
    draw_connection('C2', 'R1', style="arc3,rad=-0.1")  # La evaluación requiere doble búfer
    draw_connection('C2', 'R2', style="arc3,rad=0.0")   # La evaluación aprovecha paralelismo
    draw_connection('C3', 'R3', style="arc3,rad=0.0")   # El mapeo obedece al desacoplamiento

    # Transversales
    # L2 <-> R1: La sincronización fuerza el doble búfer
    draw_connection('L2', 'R1', style="arc3,rad=-0.25", color='#7F8C8D', linestyle='dashed', arrowstyle='<|-|>', lw=1.5, z=1)
    
    # L3 <-> R3: La invarianza exige desacoplar el modelo analítico del gráfico
    # Al estar en la misma línea (Y_3), rad=-0.25 lo curvará por debajo de C3
    draw_connection('L3', 'R3', style="arc3,rad=-0.25", color='#7F8C8D', linestyle='dashed', arrowstyle='<|-|>', lw=1.5, z=1)

    # Ajuste de los límites para asegurar que no se corte y mantener la proporción
    ax.set_xlim(0.05, 0.95)
    ax.set_ylim(0.05, 0.95)
    ax.set_aspect('equal')

    # Guardar en archivo PDF
    output_path = os.path.join(os.path.dirname(__file__), 'jerarquia_req.pdf')
    plt.savefig(output_path, format='pdf', bbox_inches='tight', pad_inches=0.1)
    print(f"Figura guardada exitosamente en: {output_path}")

if __name__ == "__main__":
    generar_diagrama()
