import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

def main():
    # Configuración de estilo y fuente para publicación científica
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
    plt.rcParams['text.color'] = '#2C3E50'
    plt.rcParams['axes.edgecolor'] = '#2C3E50'

    # Crear figura y eje con proporción 1:1
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.axis('off')

    # Establecer límites del área de dibujo
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Paleta de colores estricta requerida
    color_bg = "#EFEFEF"      # Fondo contenedor
    color_border = "#2C3E50"  # Bordes principales
    color_fill = "#D4E6F1"    # Relleno de componentes
    color_accent = "#7B241C"  # Acentos y flechas importantes
    color_white = "#FFFFFF"

    def draw_box(ax, x, y, w, h, title, subtitle="", facecolor=color_fill, edgecolor=color_border, textcolor=color_border):
        """Dibuja una caja con sombra para representar un componente interno."""
        # Sombra sutil
        shadow = patches.FancyBboxPatch(
            (x + 0.08, y - 0.08), w, h, 
            boxstyle="round,pad=0.1,rounding_size=0.2", 
            facecolor='black', alpha=0.1, edgecolor='none'
        )
        ax.add_patch(shadow)
        
        # Caja principal
        box = patches.FancyBboxPatch(
            (x, y), w, h, 
            boxstyle="round,pad=0.1,rounding_size=0.2", 
            linewidth=1.8, edgecolor=edgecolor, facecolor=facecolor, zorder=2
        )
        ax.add_patch(box)
        
        # Textos
        center_y = y + h/2
        if subtitle:
            ax.text(x + w/2, center_y + 0.35, title, ha='center', va='center', 
                    fontsize=14, fontweight='bold', color=textcolor, zorder=3)
            ax.text(x + w/2, center_y - 0.25, subtitle, ha='center', va='center', 
                    fontsize=11, color=textcolor, fontstyle='italic', zorder=3)
        else:
            ax.text(x + w/2, center_y, title, ha='center', va='center', 
                    fontsize=14, fontweight='bold', color=textcolor, zorder=3)

    # 1. Contenedor Global: Fondo del diagrama
    # Añadimos un pequeño margen invisible para asegurar un recorte perfecto
    ax.scatter([0, 10], [0, 10], alpha=0)

    outer_shadow = patches.FancyBboxPatch(
        (0.35, 0.35), 9.3, 9.3, 
        boxstyle="round,pad=0.2,rounding_size=0.4", 
        facecolor='black', alpha=0.05, edgecolor='none'
    )
    ax.add_patch(outer_shadow)

    outer_box = patches.FancyBboxPatch(
        (0.3, 0.3), 9.4, 9.4, 
        boxstyle="round,pad=0.2,rounding_size=0.4", 
        linewidth=2, edgecolor=color_border, facecolor=color_white, zorder=1
    )
    ax.add_patch(outer_box)
    ax.text(5.0, 9.4, "Sistema Multi-Viewport", ha='center', va='center', 
            fontsize=18, fontweight='bold', color=color_border, zorder=3)

    # 2. Contenedor Interno: Viewport (Instancia)
    vp_box = patches.FancyBboxPatch(
        (0.8, 0.8), 8.4, 7.8, 
        boxstyle="round,pad=0.15,rounding_size=0.3", 
        linewidth=2, edgecolor=color_accent, facecolor=color_bg, linestyle='--', zorder=1.5
    )
    ax.add_patch(vp_box)

    # Etiqueta del contenedor interno
    bbox_props = dict(boxstyle="round,pad=0.3", fc=color_bg, ec=color_accent, lw=1.5)
    ax.text(5.0, 8.6, "Instancia Viewport", ha='center', va='center', 
            fontsize=15, fontweight='bold', color=color_accent, bbox=bbox_props, zorder=3)

    # 3. Dibujar Componentes Internos
    # Capa Lógica y Operacional (Arriba)
    draw_box(ax, 1.5, 5.5, 3.0, 2.0, "Automaton", "Motor Lógico\ny Espacio Celular", facecolor=color_fill)
    draw_box(ax, 5.5, 5.5, 3.0, 2.0, "Simulation", "Motor Operacional\ny Reglas", facecolor=color_fill)

    # Capa de Interfaz y Representación (Abajo)
    draw_box(ax, 1.5, 2.0, 3.0, 2.0, "Cámara", "Contexto de\nRepresentación Visual", facecolor=color_fill)
    draw_box(ax, 5.5, 2.0, 3.0, 2.0, "Input Handlers", "Manejadores de Input\ne Interacción", facecolor=color_fill)

    # 4. Conexiones y Flujo de Datos
    # Automaton <-> Simulation
    ax.annotate("", xy=(5.5, 6.5), xytext=(4.5, 6.5), 
                arrowprops=dict(arrowstyle="<|-|>", color=color_accent, lw=2.5, shrinkA=0, shrinkB=0), zorder=2)
    ax.text(5.0, 6.7, "Actualización\nde Estado", ha='center', va='bottom', fontsize=11, color=color_border, fontweight='bold')

    # Automaton -> Cámara
    ax.annotate("", xy=(3.0, 4.0), xytext=(3.0, 5.5), 
                arrowprops=dict(arrowstyle="-|>", color=color_accent, lw=2.5, shrinkA=0, shrinkB=0), zorder=2)
    ax.text(2.8, 4.75, "Lectura\nde Estado", ha='right', va='center', fontsize=11, color=color_border, fontweight='bold')

    # Input -> Simulation
    ax.annotate("", xy=(7.0, 5.5), xytext=(7.0, 4.0), 
                arrowprops=dict(arrowstyle="-|>", color=color_accent, lw=2.5, shrinkA=0, shrinkB=0), zorder=2)
    ax.text(7.2, 4.75, "Control\n(Play, Step)", ha='left', va='center', fontsize=11, color=color_border, fontweight='bold')

    # Input -> Cámara
    ax.annotate("", xy=(4.5, 3.0), xytext=(5.5, 3.0), 
                arrowprops=dict(arrowstyle="-|>", color=color_accent, lw=2.5, shrinkA=0, shrinkB=0), zorder=2)
    ax.text(5.0, 3.2, "Manipulación\n(Pan, Zoom)", ha='center', va='bottom', fontsize=11, color=color_border, fontweight='bold')

    # Ajustes finales y guardado
    plt.tight_layout()

    # Ruta de salida (en el mismo directorio que el script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "composicion_viewport.pdf")

    plt.savefig(output_file, format='pdf', bbox_inches='tight', dpi=300)
    print(f"Figura generada con éxito: {output_file}")

if __name__ == '__main__':
    main()
