import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_uml_diagram():
    # Configurar fuente a serif para un estilo académico
    plt.rcParams['font.family'] = 'serif'
    
    # Crear la figura sin ejes, garantizando la proporción geométrica
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal')
    ax.axis('off')
    
    # -------------------------------------------------------------------------
    # 1. Contenedor Principal (Automaton)
    # -------------------------------------------------------------------------
    # Coordenadas: x=1, y=1, ancho=8, alto=6
    automaton = patches.Rectangle((1, 1), 8, 6, linewidth=2.5, 
                                  edgecolor='#2C3E50', facecolor='#EFEFEF', zorder=1)
    ax.add_patch(automaton)
    
    # Título principal del contenedor
    ax.text(5, 6.6, "Clase Automaton (Núcleo Analítico y de Simulación)", 
            fontsize=13, fontweight='bold', ha='center', va='center', color='#2C3E50')
    
    # Línea horizontal separadora del título y los métodos del contenedor general
    ax.plot([1.2, 8.8], [6.3, 6.3], color='#2C3E50', linewidth=1.5, zorder=2)
    
    # Métodos principales de Automaton
    ax.text(1.5, 6.1, "+ iterarGeneracion()\n+ aplicarRegla()", 
            fontsize=11, ha='left', va='top', color='#2C3E50', family='monospace')
    
    # -------------------------------------------------------------------------
    # 2. Lógica de Reglas de Transición (Izquierda)
    # -------------------------------------------------------------------------
    # Coordenadas: x=1.5, y=1.5, ancho=3.3, alto=3.8
    logica = patches.Rectangle((1.5, 1.5), 3.3, 3.8, linewidth=1.5, 
                               edgecolor='#2C3E50', facecolor='#D4E6F1', zorder=2)
    ax.add_patch(logica)
    
    # Título Lógica
    ax.text(3.15, 5.0, "<<Interface>>\nLógica de Reglas de Transición", 
            fontsize=11, fontweight='bold', ha='center', va='center', color='#2C3E50')
    ax.plot([1.6, 4.7], [4.6, 4.6], color='#2C3E50', linewidth=1.0, zorder=3)
    
    # Métodos de la interfaz
    ax.text(1.7, 4.4, "+ evaluarVecindad()", 
            fontsize=11, ha='left', va='top', color='#2C3E50', family='monospace')
    ax.plot([1.6, 4.7], [3.8, 3.8], color='#2C3E50', linewidth=1.0, zorder=3)
    
    # Implementaciones concretas
    ax.text(1.7, 3.6, "Implementaciones:\n  - Spiral\n  - Beehive\n  - Moore", 
            fontsize=11, ha='left', va='top', color='#2C3E50', style='italic')

    # -------------------------------------------------------------------------
    # 3. GridStorage (Derecha Arriba)
    # -------------------------------------------------------------------------
    # Coordenadas: x=5.2, y=3.5, ancho=3.4, alto=1.8
    grid = patches.Rectangle((5.2, 3.5), 3.4, 1.8, linewidth=1.5, 
                             edgecolor='#2C3E50', facecolor='#D4E6F1', zorder=2)
    ax.add_patch(grid)
    
    # Título GridStorage
    ax.text(6.9, 5.0, "Clase GridStorage\n(Mapeo Topológico)", 
            fontsize=11, fontweight='bold', ha='center', va='center', color='#2C3E50')
    ax.plot([5.3, 8.5], [4.6, 4.6], color='#2C3E50', linewidth=1.0, zorder=3)
    
    # Métodos GridStorage
    ax.text(5.4, 4.4, "+ getVecindad(x, y)\n+ swapBuffers()", 
            fontsize=11, ha='left', va='top', color='#2C3E50', family='monospace')

    # -------------------------------------------------------------------------
    # 4. BitArray (Derecha Abajo)
    # -------------------------------------------------------------------------
    # Coordenadas: x=5.6, y=1.5, ancho=2.6, alto=1.4
    bitarray = patches.Rectangle((5.6, 1.5), 2.6, 1.4, linewidth=1.5, 
                                 edgecolor='#2C3E50', facecolor='#EAEDED', 
                                 linestyle='--', zorder=2)
    ax.add_patch(bitarray)
    
    # Título BitArray
    ax.text(6.9, 2.6, "BitArray\n(Double Buffering)", 
            fontsize=11, fontweight='bold', ha='center', va='center', color='#2C3E50')
    ax.plot([5.7, 8.1], [2.2, 2.2], color='#2C3E50', linewidth=1.0, zorder=3)
    
    # Métodos y complejidad
    ax.text(5.8, 2.0, "+ getBit(index)\n+ setBit(index)", 
            fontsize=11, ha='left', va='top', color='#2C3E50', family='monospace')
    ax.text(8.0, 1.75, "O(1)", 
            fontsize=10, ha='right', va='center', color='#7B241C', fontweight='bold')

    # -------------------------------------------------------------------------
    # 5. Relaciones Topológicas UML (Agregación / Composición)
    # -------------------------------------------------------------------------
    def add_diamond(ax, x, y, direction='left', color='#7B241C'):
        """Dibuja un rombo de composición UML en la coordenada (x,y)."""
        dw, dh = 0.3, 0.2
        if direction == 'left':
            pts = [(x, y), (x+dw/2, y+dh/2), (x+dw, y), (x+dw/2, y-dh/2)]
        elif direction == 'right':
            pts = [(x, y), (x-dw/2, y+dh/2), (x-dw, y), (x-dw/2, y-dh/2)]
        elif direction == 'bottom':
            pts = [(x, y), (x+dh/2, y-dw/2), (x, y-dw), (x-dh/2, y-dw/2)]
        poly = patches.Polygon(pts, closed=True, facecolor=color, edgecolor=color, zorder=4)
        ax.add_patch(poly)

    # Conexión: Automaton (Borde Izquierdo) -> Lógica de Reglas
    add_diamond(ax, 1.0, 3.4, direction='left')
    ax.plot([1.3, 1.5], [3.4, 3.4], color='#7B241C', linewidth=1.5, zorder=3)
    ax.text(1.15, 3.55, "1", fontsize=10, color='#7B241C', ha='center')

    # Conexión: Automaton (Borde Derecho) -> GridStorage
    add_diamond(ax, 9.0, 4.4, direction='right')
    ax.plot([8.7, 8.6], [4.4, 4.4], color='#7B241C', linewidth=1.5, zorder=3)
    ax.text(8.85, 4.55, "1", fontsize=10, color='#7B241C', ha='center')

    # Conexión: GridStorage (Base) -> BitArray (Top)
    add_diamond(ax, 6.9, 3.5, direction='bottom')
    ax.plot([6.9, 6.9], [3.2, 2.9], color='#7B241C', linewidth=1.5, zorder=3)
    ax.text(7.05, 3.3, "1", fontsize=10, color='#7B241C', ha='left')
    ax.text(7.05, 3.0, "2", fontsize=10, color='#7B241C', ha='left')

    # Limitar y ajustar visualmente
    plt.xlim(0.5, 9.5)
    plt.ylim(0.5, 7.5)
    plt.tight_layout()
    
    # Guardar como PDF
    plt.savefig('diagrama_clases_nucleo.pdf', format='pdf', bbox_inches='tight', dpi=300)
    print("Figura 'diagrama_clases_nucleo.pdf' generada exitosamente.")

if __name__ == '__main__':
    draw_uml_diagram()
