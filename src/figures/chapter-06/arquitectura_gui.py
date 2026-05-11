import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def generate_architecture_diagram():
    # Estilo académico y tipografía
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
    plt.rcParams['text.color'] = '#2C3E50'
    
    # Paleta de colores estricta solicitada
    c_bg = "#EFEFEF"
    c_text = "#2C3E50"
    c_blue = "#D4E6F1"
    c_red = "#7B241C"
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_aspect('equal') # Proporciones geométricas exactas
    
    def draw_box(x, y, w, h, text, facecolor, edgecolor, textcolor, 
                 fontsize=11, fontweight='normal', shadow=True, title=False, 
                 title_y_offset=0.3):
        # Sombra paralela para estética rigurosa
        if shadow:
            shadow_box = patches.FancyBboxPatch(
                (x + 0.08, y - 0.08), w, h, 
                boxstyle='round,pad=0,rounding_size=0.15', 
                linewidth=0, facecolor='black', alpha=0.15)
            ax.add_patch(shadow_box)
            
        # Caja principal
        box = patches.FancyBboxPatch(
            (x, y), w, h, 
            boxstyle='round,pad=0,rounding_size=0.15', 
            linewidth=1.5, edgecolor=edgecolor, facecolor=facecolor)
        ax.add_patch(box)
        
        # Inserción de texto
        if text:
            if title:
                ax.text(x + w / 2, y + h - title_y_offset, text, 
                        ha='center', va='center', fontsize=fontsize, 
                        color=textcolor, fontweight=fontweight)
            else:
                ax.text(x + w / 2, y + h / 2, text, 
                        ha='center', va='center', fontsize=fontsize, 
                        color=textcolor, fontweight=fontweight)
        return box

    # 1. Clase Application (Base)
    draw_box(0.5, 0.5, 11, 7, "Clase Application (Arquitectura Base)", 
             facecolor=c_bg, edgecolor=c_text, textcolor=c_text, 
             fontsize=14, fontweight='bold', shadow=False, title=True, 
             title_y_offset=0.4)

    # 2. Ciclo de Simulación (Izquierda)
    draw_box(1.0, 1.0, 4.5, 5.2, "Ciclo Central de Simulación", 
             facecolor='white', edgecolor=c_red, textcolor=c_red, 
             fontsize=12, fontweight='bold', shadow=True, title=True, 
             title_y_offset=0.3)
             
    # Componentes Internos de Simulación
    draw_box(1.5, 4.0, 3.5, 0.9, "Motor de Estados\n(Autómata Celular)", 
             facecolor=c_bg, edgecolor=c_red, textcolor=c_text)
    draw_box(1.5, 2.5, 3.5, 0.9, "Evaluador de Reglas y\nResolución de Vecindad", 
             facecolor=c_bg, edgecolor=c_red, textcolor=c_text)
    draw_box(1.5, 1.2, 3.5, 0.9, "Búfer de Memoria y\nDatos de Cuadrícula", 
             facecolor=c_bg, edgecolor=c_red, textcolor=c_text)

    # Flechas de flujo en Simulación (Ciclo Cíclico)
    ax.annotate('', xy=(3.25, 3.9), xytext=(3.25, 3.4), 
                arrowprops=dict(arrowstyle='->', color=c_red, lw=1.5))
    ax.annotate('', xy=(3.25, 2.4), xytext=(3.25, 2.1), 
                arrowprops=dict(arrowstyle='->', color=c_red, lw=1.5))
                
    # Flecha de retorno
    c1 = patches.ConnectionPatch((1.5, 1.65), (1.5, 4.45), "data", "data",
                                 connectionstyle="bar,fraction=-0.15", 
                                 arrowstyle="->", color=c_red, lw=1.5)
    ax.add_patch(c1)

    # 3. Sistema de Docking (Derecha)
    draw_box(6.5, 1.0, 4.5, 5.2, "Sistema de Docking (UI)", 
             facecolor=c_blue, edgecolor=c_text, textcolor=c_text, 
             fontsize=12, fontweight='bold', shadow=True, title=True, 
             title_y_offset=0.3)

    # Paneles de Herramientas y Analíticos
    draw_box(7.0, 4.0, 3.5, 0.9, "Panel de Herramientas\n(Controles de Ejecución)", 
             facecolor='white', edgecolor=c_text, textcolor=c_text)
    draw_box(7.0, 2.5, 3.5, 0.9, "Panel Analítico\n(Espacio Fase / Dinámica)", 
             facecolor='white', edgecolor=c_text, textcolor=c_text)
    draw_box(7.0, 1.2, 3.5, 0.9, "Panel Analítico\n(Entropía y Métricas)", 
             facecolor='white', edgecolor=c_text, textcolor=c_text)

    # 4. Representación de la Independencia (Frontera)
    ax.plot([6.0, 6.0], [1.5, 5.5], color=c_text, linestyle='dashdot', lw=1.5, alpha=0.6)
    
    # Etiqueta de la Frontera
    ax.text(6.0, 1.2, "Frontera de Desacoplamiento\n(Independencia Estructural)", 
            ha='center', va='center', fontsize=9, color=c_text, fontweight='bold')

    # Flechas de comunicación cruzada (desacoplada)
    ax.annotate('', xy=(6.5, 4.2), xytext=(5.5, 4.2), 
                arrowprops=dict(arrowstyle='-|>,head_width=0.3,head_length=0.5', 
                                color=c_text, lw=1.5, ls='--'))
    ax.annotate('', xy=(5.5, 3.5), xytext=(6.5, 3.5), 
                arrowprops=dict(arrowstyle='-|>,head_width=0.3,head_length=0.5', 
                                color=c_text, lw=1.5, ls='--'))
                
    # Etiquetas de comunicación
    ax.text(6.0, 4.3, "Eventos Asíncronos", ha='center', va='bottom', 
            fontsize=9, color=c_text, style='italic')
    ax.text(6.0, 3.4, "Lectura de Estado (Solo-Lectura)", ha='center', va='top', 
            fontsize=9, color=c_text, style='italic')

    # Guardar en el directorio actual (que será el del reporte técnico)
    try:
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'arquitectura_gui.pdf')
    except NameError:
        output_path = 'arquitectura_gui.pdf'
        
    plt.tight_layout()
    plt.savefig(output_path, format='pdf', bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Diagrama guardado exitosamente en: {output_path}")

if __name__ == '__main__':
    generate_architecture_diagram()
