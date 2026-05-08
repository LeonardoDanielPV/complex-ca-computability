import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_figure():
    """
    Genera la figura teórica de la intersección de planos para el dominio hexagonal.
    El hexágono resultante, dadas las ecuaciones explícitas (y = ±(sqrt(3)/2)R y
    ±(sqrt(3)/2)x ± (1/2)y = (sqrt(3)/2)R), es un hexágono flat-topped (con bordes 
    horizontales). El script respeta estrictamente estas fronteras algebraicas.
    """
    # Configuración académica de fuentes (estilo LaTeX)
    plt.rcParams.update({
        "text.usetex": False,
        "mathtext.fontset": "cm", # Computer Modern, similar a LaTeX
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "serif"],
        "axes.labelsize": 12,
        "font.size": 14,
    })

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('#EFEFEF') # Fondo sobrio
    
    R = 1.0
    a = (np.sqrt(3) / 2) * R
    
    # Vértices del hexágono flat-topped (orientación dictada por las ecuaciones)
    angles = np.radians(np.arange(0, 360, 60))
    vertices = np.column_stack((R * np.cos(angles), R * np.sin(angles)))
    
    # Ángulos normales para las 6 rectas (30, 90, 150, 210, 270, 330 grados)
    normal_angles = np.radians(np.arange(30, 390, 60))
    normals = np.column_stack((np.cos(normal_angles), np.sin(normal_angles)))
    
    plot_limit = 1.6
    
    # 1. Dibujar regiones sombreadas y rectas divisorias
    for i in range(6):
        n = normals[i]
        midpoint = a * n
        t = np.array([-n[1], n[0]]) # Vector tangente a la frontera
        
        # Puntos para la línea infinita de la frontera
        p1 = midpoint + 5 * t
        p2 = midpoint - 5 * t
        
        # Línea punteada que representa el semiplano
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#2C3E50', linestyle='--', linewidth=1.2, zorder=1)
        
        # Polígono de sombreado que se extiende hacia el origen (-n)
        p3 = p2 - 10 * n
        p4 = p1 - 10 * n
        poly = patches.Polygon([p1, p2, p3, p4], closed=True, facecolor='#2C3E50', alpha=0.08, zorder=0)
        ax.add_patch(poly)

    # 2. Dibujar el hexágono central H
    hex_polygon = patches.Polygon(vertices, closed=True, facecolor='#D4E6F1', edgecolor='#2C3E50', linewidth=2.5, zorder=3)
    ax.add_patch(hex_polygon)
    
    # 3. Vectores normales unitarios pequeños saliendo de las caras
    for i in range(6):
        n = normals[i]
        midpoint = a * n
        ax.arrow(midpoint[0], midpoint[1], 0.15 * n[0], 0.15 * n[1], 
                 head_width=0.04, head_length=0.06, fc='#2C3E50', ec='#2C3E50', 
                 length_includes_head=True, zorder=4)

    # 4. Anotaciones matemáticas
    # Símbolo del dominio central
    ax.text(0, 0, r'$\mathcal{H}$', fontsize=32, ha='center', va='center', color='#2C3E50', zorder=5)
    
    # Circunradio R (desde origen al vértice superior izquierdo)
    top_left_vertex = vertices[2] # 120 grados
    ax.plot([0, top_left_vertex[0]], [0, top_left_vertex[1]], color='#7B241C', linestyle=':', linewidth=2, zorder=4)
    mid_R = top_left_vertex / 2.0
    offset_R = np.array([np.cos(np.radians(30)), np.sin(np.radians(30))]) * 0.08 # Offset ortogonal
    ax.text(mid_R[0] + offset_R[0], mid_R[1] + offset_R[1], r'$R$', fontsize=18, color='#7B241C', ha='center', va='center', zorder=5)
    
    # Apotema a (desde origen al punto medio de la arista lateral inferior derecha)
    mid_a = a * normals[5] # 330 grados (-30 grados)
    ax.plot([0, mid_a[0]], [0, mid_a[1]], color='#7B241C', linestyle=':', linewidth=2, zorder=4)
    mid_mid_a = mid_a / 2.0
    offset_a = np.array([np.cos(np.radians(60)), np.sin(np.radians(60))]) * 0.08 # Offset ortogonal
    ax.text(mid_mid_a[0] + offset_a[0], mid_mid_a[1] + offset_a[1], r'$a$', fontsize=18, color='#7B241C', ha='center', va='center', zorder=5)
    
    # Ecuaciones de las inecuaciones
    # Borde horizontal superior (normal a 90 grados, index 1)
    top_mid = a * normals[1]
    ax.text(top_mid[0], top_mid[1] + 0.25, r'$|y| \leq \frac{\sqrt{3}}{2}R$', 
            fontsize=20, color='#2C3E50', ha='center', va='center', zorder=5)
    
    # Borde diagonal superior derecho (normal a 30 grados, index 0)
    tr_mid = a * normals[0]
    pos_tr = tr_mid + 0.3 * normals[0]
    ax.text(pos_tr[0], pos_tr[1], r'$\frac{\sqrt{3}}{2}|x| + \frac{1}{2}|y| \leq \frac{\sqrt{3}}{2}R$', 
            fontsize=20, color='#2C3E50', ha='center', va='center', rotation=-60, zorder=5)
    
    # 5. Configuración final del lienzo
    ax.set_aspect('equal') # Proporciones exactas
    ax.set_xlim(-plot_limit, plot_limit)
    ax.set_ylim(-plot_limit, plot_limit)
    ax.axis('off') # Apagar ejes cartesianos para apariencia teórica
    
    # 6. Guardar la figura
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()
        
    output_path = os.path.join(script_dir, 'interseccion_planos.pdf')
    plt.savefig(output_path, format='pdf', bbox_inches='tight', pad_inches=0.05, facecolor=fig.get_facecolor())
    print(f"Figura teórica generada y guardada exitosamente en:\n{output_path}")

if __name__ == "__main__":
    create_figure()
