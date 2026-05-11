import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# Configuración tipográfica para estilo académico (LaTeX-like)
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "mathtext.fontset": "stix",
    "axes.unicode_minus": False
})

def main():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.axis('off')

    # Parámetros geométricos de los hexágonos
    R = 1.0
    orientation = 0

    # Paleta de colores
    color_center = "#D4E6F1"
    color_neighbor = "#EFEFEF"
    color_edge = "#2C3E50"
    color_text = "#2C3E50"
    color_dotted = "#7B241C"

    # Función para mapear coordenadas cúbicas (x, y, z) a cartesianas (X, Y)
    # en una topología hexagonal pointy-topped.
    def hex_center(x, y, z):
        X = (np.sqrt(3) / 2) * (x - z)
        Y = -1.5 * y
        return X, Y

    # Definición de la vecindad de radio 1: (x, y, z, is_center)
    # El orden corresponde a: Centro, y luego los 6 vecinos en sentido antihorario
    # comenzando desde la posición superior derecha.
    hexagons = [
        (0, 0, 0, True),     # Centro
        (1, -1, 0, False),   # Superior Derecha
        (0, -1, 1, False),   # Superior Izquierda
        (-1, 0, 1, False),   # Izquierda
        (-1, 1, 0, False),   # Inferior Izquierda
        (0, 1, -1, False),   # Inferior Derecha
        (1, 0, -1, False)    # Derecha
    ]

    # Renderizado de los hexágonos y sus etiquetas
    for x, y, z, is_center in hexagons:
        X, Y = hex_center(x, y, z)
        color = color_center if is_center else color_neighbor
        
        # Crear el polígono hexagonal
        hexagon = mpatches.RegularPolygon(
            (X, Y),
            numVertices=6,
            radius=R,
            orientation=orientation,
            facecolor=color,
            edgecolor=color_edge,
            linewidth=1.5,
            zorder=1
        )
        ax.add_patch(hexagon)
        
        # Añadir la etiqueta de la coordenada cúbica
        label = rf'$({x}, {y}, {z})$'
        ax.text(X, Y, label, ha='center', va='center', 
                color=color_text, fontsize=12, zorder=3)

    # --- Representación de Ejes Cúbicos y Axiales ---
    
    # Vectores directores para los ejes cúbicos +x, +y, +z
    # Estos vectores apuntan exactamente a través de los vértices del hexágono central
    # (que corresponden a las fronteras entre los hexágonos vecinos).
    v_x = (np.sqrt(3)/2, 0.5)   # 30 grados
    v_y = (0, -1.0)             # 270 grados
    v_z = (-np.sqrt(3)/2, 0.5)  # 150 grados

    L_arrow = 2.4   # Longitud de la flecha sólida (ejes cúbicos)
    L_dotted = 3.6  # Longitud total con la extensión punteada (ejes axiales)

    def add_axis(v_dir, label, is_qr=False, qr_label=''):
        vx, vy = v_dir
        
        # Flecha sólida para el eje cúbico
        ax.annotate('', xy=(vx * L_arrow, vy * L_arrow), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='-|>', color=color_edge, lw=2, mutation_scale=15),
                    zorder=2)
        
        # Etiqueta del eje cúbico
        ax.text(vx * (L_arrow + 0.35), vy * (L_arrow + 0.35), label, 
                color=color_edge, fontsize=15, ha='center', va='center', zorder=4)
        
        if is_qr:
            # Línea punteada que extiende el eje para ilustrar la proyección axial
            ax.plot([vx * L_arrow, vx * L_dotted], [vy * L_arrow, vy * L_dotted], 
                    color=color_dotted, linestyle='--', lw=1.5, zorder=1)
            
            # Calcular posición para la etiqueta del eje axial (offset perpendicular)
            mid_x = vx * (L_arrow + L_dotted) / 2
            mid_y = vy * (L_arrow + L_dotted) / 2
            
            # Offset perpendicular para no sobreescribir la línea
            if label == r'$+z$':
                off_x, off_y = vy, -vx  # Offset hacia arriba-derecha
            else:
                off_x, off_y = -vy, vx  # Offset hacia arriba-izquierda
                
            offset_dist = 0.3
            ax.text(mid_x + off_x * offset_dist, mid_y + off_y * offset_dist, qr_label, 
                    color=color_dotted, fontsize=15, ha='center', va='center', zorder=4)

    # Dibujar los tres ejes principales
    add_axis(v_x, r'$+x$', is_qr=True, qr_label=r'$+q$')
    add_axis(v_y, r'$+y$')
    add_axis(v_z, r'$+z$', is_qr=True, qr_label=r'$+r$')

    # Ajustar límites de la ventana para que no se corte ningún elemento
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-4.5, 4.5)

    # Guardar la figura en PDF
    output_filename = "vecindad_hexagonal.pdf"
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_filename)
    plt.savefig(output_path, bbox_inches='tight', format='pdf', transparent=True)
    print(f"Figura guardada exitosamente en: {output_path}")

if __name__ == '__main__':
    main()
