import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import os

def generar_figura_espiral(output_filename="evolucion_spiral.pdf"):
    """
    Genera la figura teórica de la evolución de una espiral en un autómata celular
    hexagonal (3 subgráficas para t, t+1, t+2).
    """
    # 1. Definición de la Paleta de Colores
    c_0 = "#EFEFEF"  # Estado 0: Sustrato/Reposo
    c_1 = "#2C3E50"  # Estado 1: Frente de Activación
    c_2 = "#7B241C"  # Estado 2: Decaimiento Temprano
    c_3 = "#D4E6F1"  # Estado 3: Decaimiento Tardío

    # 2. Configuración del Sustrato Celular (Radio de la retícula)
    radius = 5

    # 3. Mapeo de Estados para la Secuencia Evolutiva
    # --- t ---
    # Semilla inicial asimétrica en el centro
    st_t0 = {
        (0, 0): 1, (1, 0): 1, (0, 1): 1
    }
    
    # --- t+1 ---
    # Semilla transiciona a Estado 2.
    # Anillo exterior asimétrico se enciende en Estado 1.
    st_t1 = {
        (0, 0): 2, (1, 0): 2, (0, 1): 2
    }
    s1_t1 = [(2, 0), (1, 1), (0, 2), (-1, 2), (-1, 1), (-1, 0), (0, -1)]
    for c in s1_t1:
        st_t1[c] = 1

    # --- t+2 ---
    # El epicentro regresa a 0. Las demás decaen.
    # El frente expansivo avanza y envuelve el núcleo.
    st_t2 = {
        (0, 0): 0, 
        (1, 0): 3, (0, 1): 3
    }
    for c in s1_t1:
        st_t2[c] = 2
        
    s1_t2 = [
        (3, 0), (3, -1), (2, -1), (2, 1), (1, 2), (0, 3), (-1, 3),
        (-2, 3), (-2, 2), (-2, 1), (-2, 0), (-1, -1), (0, -2), (1, -2), (1, -1)
    ]
    for c in s1_t2:
        st_t2[c] = 1

    # 4. Configuración del Renderizado de Matplotlib
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 22
    })

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    pasos = [
        (st_t0, "$t$"),
        (st_t1, "$t+1$"),
        (st_t2, "$t+2$")
    ]

    # 5. Dibujo de la Retícula Hexagonal
    for ax, (estados, etiqueta) in zip(axes, pasos):
        ax.set_aspect('equal')
        ax.axis('off')  # Apagar ejes cartesianos
        
        # Generar polígonos
        for q in range(-radius, radius + 1):
            for r in range(-radius, radius + 1):
                # Restricción para formar un hexágono grande (distancia axial)
                if -q - r >= -radius and -q - r <= radius:
                    # Transformación a coordenadas cartesianas (Orientación Pointy-Top)
                    x = np.sqrt(3) * (q + r / 2)
                    y = 1.5 * r
                    
                    # Obtener estado y color
                    estado = estados.get((q, r), 0)
                    color = {0: c_0, 1: c_1, 2: c_2, 3: c_3}[estado]
                    
                    # Crear hexágono contiguo
                    hex_patch = RegularPolygon(
                        (x, y),
                        numVertices=6,
                        radius=1.0,
                        orientation=0,
                        facecolor=color,
                        edgecolor="white",  # Líneas divisorias sutiles y elegantes
                        linewidth=0.7
                    )
                    ax.add_patch(hex_patch)
                    
        # Configurar límites para evitar deformación y garantizar misma escala
        ax.set_xlim(-10, 10)
        ax.set_ylim(-11, 9)
        
        # Etiqueta de tiempo centrada abajo de cada figura
        ax.text(0, -9.5, etiqueta, ha='center', va='center', fontsize=26)

    # 6. Exportar Figura
    plt.tight_layout()
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base_dir = os.getcwd()
        
    output_path = os.path.join(base_dir, output_filename)
    plt.savefig(output_path, format='pdf', bbox_inches='tight', dpi=300)
    print(f"Figura guardada exitosamente en: {output_path}")

if __name__ == '__main__':
    generar_figura_espiral()
