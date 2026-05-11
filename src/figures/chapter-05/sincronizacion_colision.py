import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

# Configuración académica global
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.size'] = 11

def generar_figura_sincronizacion():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Parámetros del espacio y tiempo
    x_min, x_max = 0, 10
    y_min, y_max = 0, 10
    t_min, t_max = 0, 10

    # Coordenadas del evento
    ic, jc, tc = 5, 5, 8  # Punto de colisión / sincronización
    i1, j1 = 2, 2         # Origen del glider 1
    i2, j2 = 8, 2         # Origen del glider 2

    # Paleta de colores solicitada
    color_grid = "#EFEFEF"
    color_dark = "#2C3E50"
    color_cone = "#D4E6F1"
    color_red = "#7B241C"

    # 1. Ejes y Planos Base
    X_base, Y_base = np.meshgrid(np.linspace(x_min, x_max, 11), np.linspace(y_min, y_max, 11))
    
    # Líneas de cuadrícula sutiles en t=0
    for i in range(x_min, x_max + 1):
        ax.plot([i, i], [y_min, y_max], [0, 0], color=color_grid, lw=1, zorder=1)
    for j in range(y_min, y_max + 1):
        ax.plot([x_min, x_max], [j, j], [0, 0], color=color_grid, lw=1, zorder=1)

    # Etiqueta plano t=0
    ax.text(x_max, y_max, 0, "Plano de configuración inicial $t=0$", 
            color=color_dark, fontsize=11, ha='right', va='bottom')

    # Plano t=tc
    Z_tc = np.full_like(X_base, tc)
    ax.plot_surface(X_base, Y_base, Z_tc, color='white', alpha=0.1, edgecolor='lightgray', linewidth=0.5, linestyle=':', zorder=2)
    ax.text(x_max, y_max, tc, "Plano de sincronización $t=t_c$", 
            color=color_dark, fontsize=11, ha='right', va='bottom')

    # 2. Cono de Luz (Causal Cone)
    # Proyectamos un cono invertido (pirámide de base cuadrada) desde tc hacia t=0
    r = tc  # Radio causal asumiendo c=1 (vecindad de Moore)
    v1 = [ic - r, jc - r, 0]
    v2 = [ic + r, jc - r, 0]
    v3 = [ic + r, jc + r, 0]
    v4 = [ic - r, jc + r, 0]
    apex = [ic, jc, tc]

    faces = [
        [apex, v1, v2],
        [apex, v2, v3],
        [apex, v3, v4],
        [apex, v4, v1]
    ]

    pyramid = Poly3DCollection(faces, facecolors=color_cone, alpha=0.2, edgecolors=color_cone, linewidths=1)
    ax.add_collection3d(pyramid)
    # Base del cono en t=0
    base_face = Poly3DCollection([[v1, v2, v3, v4]], facecolors=color_cone, alpha=0.1, edgecolors=color_cone, linewidths=1)
    ax.add_collection3d(base_face)

    # 3. Punto de Intersección (Colisión)
    ax.scatter(ic, jc, tc, color=color_red, s=80, depthshade=False, zorder=10)
    ax.text(ic, jc, tc + 0.6, "$(i_c, j_c)$", color=color_red, fontsize=12, ha='center', weight='bold')

    # 4. Retroceso Cinemático y Vectores
    # Trayectorias en retroceso
    ax.plot([ic, i1], [jc, j1], [tc, 0], color=color_dark, linestyle='--', linewidth=2.5, zorder=5)
    ax.plot([ic, i2], [jc, j2], [tc, 0], color=color_dark, linestyle='--', linewidth=2.5, zorder=5)

    # Vector u1
    m1x, m1y, m1z = (ic + i1)/2, (jc + j1)/2, tc/2
    d1x, d1y, d1z = i1 - ic, j1 - jc, -tc
    ax.quiver(m1x, m1y, m1z, d1x, d1y, d1z, color=color_dark, length=0.4, normalize=True, arrow_length_ratio=0.3, zorder=6)
    ax.text(m1x - 0.5, m1y, m1z, "$\\vec{u}_1$", color=color_dark, fontsize=14, zorder=7)

    # Vector u2
    m2x, m2y, m2z = (ic + i2)/2, (jc + j2)/2, tc/2
    d2x, d2y, d2z = i2 - ic, j2 - jc, -tc
    ax.quiver(m2x, m2y, m2z, d2x, d2y, d2z, color=color_dark, length=0.4, normalize=True, arrow_length_ratio=0.3, zorder=6)
    ax.text(m2x + 0.5, m2y, m2z, "$\\vec{u}_2$", color=color_dark, fontsize=14, zorder=7)

    # 5. Semillas Iniciales (Bounding Boxes en t=0)
    def draw_seed(x, y, label):
        d = 0.5
        # Parche cuadrado 3x3 representativo
        seed_faces = [[[x-d, y-d, 0], [x+d, y-d, 0], [x+d, y+d, 0], [x-d, y+d, 0]]]
        seed_poly = Poly3DCollection(seed_faces, facecolors=color_dark, alpha=0.6, edgecolors='black', linewidths=1)
        ax.add_collection3d(seed_poly)
        ax.text(x, y - 1.5, 0, label, color=color_dark, fontsize=12, ha='center')

    draw_seed(i1, j1, "$(i_1, j_1)$")
    draw_seed(i2, j2, "$(i_2, j_2)$")

    # 6. Formato Académico
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 0.8])  # Proporciones isométricas relativas

    # Ajuste de límites para evitar recortes
    ax.set_xlim(x_min -3, x_max + 3)
    ax.set_ylim(y_min - 3, y_max + 3)
    ax.set_zlim(0, tc + 1)
    
    # Orientación de la cámara para mejor visualización de 3D
    ax.view_init(elev=25, azim=-45)

    # Guardar archivo PDF en el mismo directorio que el script
    script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    output_path = os.path.join(script_dir, "sincronizacion_colision.pdf")
    
    plt.tight_layout()
    plt.savefig(output_path, format='pdf', bbox_inches='tight', dpi=300)
    print(f"Figura teórica generada y guardada exitosamente en:\n{output_path}")

if __name__ == '__main__':
    generar_figura_sincronizacion()
