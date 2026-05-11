import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def main():
    # Configurar fuente para estilo académico
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Bitstream Vera Serif', 'Computer Modern Roman', 'serif']

    # Paleta de colores rigurosa y académica
    C_BG = "#EFEFEF"      # Fondos de paquetes (sobrio)
    C_TEXT = "#2C3E50"    # Texto, bordes oscuros (elegancia)
    C_FILL = "#D4E6F1"    # Relleno de clases (distinción sutil)
    C_ACCENT = "#7B241C"  # Acentos, dependencias (énfasis)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('off')
    ax.set_aspect('equal')
    ax.set_xlim(-2, 102)
    ax.set_ylim(-2, 84)

    # --- FUNCIONES AUXILIARES DE DIBUJO ---

    def draw_package(ax, x, y, w, h, title):
        shadow_offset = 1.0
        tab_w = 34 if len(title) > 15 else 22
        tab_h = 5
        
        # Sombras
        shadow_tab = patches.Rectangle((x + shadow_offset, y+h - shadow_offset), tab_w, tab_h, linewidth=0, facecolor='#D0D0D0', zorder=0)
        ax.add_patch(shadow_tab)
        shadow_rect = patches.Rectangle((x + shadow_offset, y - shadow_offset), w, h, linewidth=0, facecolor='#D0D0D0', zorder=0)
        ax.add_patch(shadow_rect)

        # Pestaña
        tab = patches.Rectangle((x, y+h), tab_w, tab_h, linewidth=1.5, edgecolor=C_TEXT, facecolor=C_BG, zorder=1)
        ax.add_patch(tab)
        ax.text(x + 2, y+h + tab_h/2.0, title, ha='left', va='center', fontsize=11, color=C_TEXT, fontweight='bold', zorder=2)
        
        # Caja principal
        rect = patches.Rectangle((x, y), w, h, linewidth=1.5, edgecolor=C_TEXT, facecolor=C_BG, zorder=1)
        ax.add_patch(rect)

    def draw_class(ax, x, y, w, h, title, methods=[], is_abstract_class=False):
        shadow_offset = 1.0
        shadow = patches.Rectangle((x + shadow_offset, y - shadow_offset), w, h, linewidth=0, facecolor='#D0D0D0', zorder=2)
        ax.add_patch(shadow)

        rect = patches.Rectangle((x, y), w, h, linewidth=1.5, edgecolor=C_TEXT, facecolor=C_FILL, zorder=3)
        ax.add_patch(rect)
        
        if is_abstract_class:
            title_y = y + h - 2.5
            ax.text(x + w/2.0, title_y, "<<abstract>>", ha='center', va='center', fontsize=10, color=C_TEXT, fontstyle='italic', zorder=4)
            ax.text(x + w/2.0, title_y - 3.5, title, ha='center', va='center', fontsize=11, color=C_TEXT, fontweight='bold', fontstyle='italic', zorder=4)
            line_y = y + h - 7.5
        else:
            title_y = y + h - 3.0
            ax.text(x + w/2.0, title_y, title, ha='center', va='center', fontsize=11, color=C_TEXT, fontweight='bold', zorder=4)
            line_y = y + h - 6.0
        
        ax.plot([x, x+w], [line_y, line_y], color=C_TEXT, linewidth=1.5, zorder=4)
        
        for i, (method, is_abstract_method) in enumerate(methods):
            fstyle = 'italic' if is_abstract_method else 'normal'
            ax.text(x + 1.5, line_y - 3 - i*3.5, method, ha='left', va='center', fontsize=9.5, color=C_TEXT, fontstyle=fstyle, zorder=4)

    def draw_inheritance_tree(ax, children_coords, parent_coords, mid_y):
        parent_x, parent_y = parent_coords
        triangle_h = 3.5
        triangle_w = 4.5
        
        # Triángulo herencia UML
        triangle = patches.Polygon(
            [[parent_x, parent_y], [parent_x - triangle_w/2.0, parent_y - triangle_h], [parent_x + triangle_w/2.0, parent_y - triangle_h]], 
            closed=True, edgecolor=C_TEXT, facecolor='white', linewidth=1.5, zorder=3
        )
        ax.add_patch(triangle)
        
        # Línea vertical del padre
        ax.plot([parent_x, parent_x], [parent_y - triangle_h, mid_y], color=C_TEXT, linewidth=1.5, zorder=2)
        
        # Línea horizontal
        min_x = min([c[0] for c in children_coords])
        max_x = max([c[0] for c in children_coords])
        ax.plot([min_x, max_x], [mid_y, mid_y], color=C_TEXT, linewidth=1.5, zorder=2)
        
        # Líneas verticales a los hijos
        for cx, cy in children_coords:
            ax.plot([cx, cx], [mid_y, cy], color=C_TEXT, linewidth=1.5, zorder=2)

    def draw_dependency(ax, start_x, start_y, end_x, end_y, text=""):
        ax.plot([start_x, end_x], [start_y, end_y], color=C_ACCENT, linewidth=1.8, linestyle='--', zorder=2)
        
        # Punta de flecha abierta UML
        arrow_len = 3.0
        arrow_w = 2.5
        ax.plot([end_x - arrow_len, end_x], [end_y + arrow_w/2.0, end_y], color=C_ACCENT, linewidth=1.8, zorder=2)
        ax.plot([end_x - arrow_len, end_x], [end_y - arrow_w/2.0, end_y], color=C_ACCENT, linewidth=1.8, zorder=2)
        
        if text:
            ax.text((start_x + end_x)/2.0, start_y + 1.0, text, ha='center', va='bottom', 
                    fontsize=10, color=C_ACCENT, fontstyle='italic', zorder=3,
                    bbox=dict(facecolor='white', edgecolor='none', pad=2, alpha=0.8))

    def draw_note(ax, x, y, w, h, text):
        fc = 4.0 # Folded corner size
        pts = [
            [x, y], [x+w, y], [x+w, y+h-fc], [x+w-fc, y+h], [x, y+h]
        ]
        poly = patches.Polygon(pts, closed=True, edgecolor=C_TEXT, facecolor="#FFFFFF", linewidth=1.2, zorder=4)
        ax.add_patch(poly)
        
        ax.plot([x+w-fc, x+w-fc], [y+h, y+h-fc], color=C_TEXT, linewidth=1.2, zorder=5)
        ax.plot([x+w-fc, x+w], [y+h-fc, y+h-fc], color=C_TEXT, linewidth=1.2, zorder=5)
        
        ax.text(x + w/2.0, y + h/2.0, text, ha='center', va='center', fontsize=9.5, color=C_TEXT, zorder=5, fontstyle='italic')

    def draw_dashed_link(ax, x1, y1, x2, y2):
        ax.plot([x1, x2], [y1, y2], color=C_TEXT, linewidth=1.0, linestyle=':', zorder=1)


    # --- CONSTRUCCIÓN DEL DIAGRAMA ---

    # 1. Paquetes
    draw_package(ax, 2, 5, 32, 70, "Simulation Core")
    draw_package(ax, 38, 5, 60, 70, "Visualization Subsystem")

    # 2. Clases
    # CellularAutomaton
    draw_class(ax, 5, 51.5, 26, 16, "CellularAutomaton", 
               [("+ get_state(): GridState", False), ("+ step(): void", False)])

    # AutomatonRenderer
    draw_class(ax, 53, 50, 30, 20, "AutomatonRenderer", 
               [("+ render(state: GridState)", False), ("+ transform_geometry()", True)], is_abstract_class=True)

    # SquareRenderer
    draw_class(ax, 41, 20, 26, 14, "SquareRenderer", 
               [("+ transform_geometry()", False)])

    # HexRenderer
    draw_class(ax, 69, 20, 26, 14, "HexRenderer", 
               [("+ transform_geometry()", False)])

    # 3. Relaciones
    # Dependencia (Núcleo -> Visualización)
    draw_dependency(ax, 31, 59.5, 53, 59.5, "<<observes>>\nstate data")

    # Herencia
    children_coords = [(54, 34), (82, 34)] # X centros: 41+13=54; 69+13=82. Y top: 20+14=34
    parent_coords = (68, 50)               # X centro: 53+15=68. Y bottom: 50
    draw_inheritance_tree(ax, children_coords, parent_coords, mid_y=42)

    # 4. Notas Arquitectónicas
    # Nota sobre encapsulación
    note1_x, note1_y, note1_w, note1_h = 55, 6, 26, 11
    draw_note(ax, note1_x, note1_y, note1_w, note1_h, "Encapsula la lógica\nde transformación\ngeométrica")
    # Enlaces a las clases de renderizado
    draw_dashed_link(ax, 68, 17, 54, 20)
    draw_dashed_link(ax, 68, 17, 82, 20)

    # Nota sobre independencia del núcleo
    note2_x, note2_y, note2_w, note2_h = 5, 20, 26, 14
    draw_note(ax, note2_x, note2_y, note2_w, note2_h, "Núcleo agnóstico\na la topología\nvisual y rendering")
    draw_dashed_link(ax, 18, 34, 18, 51.5)

    # 5. Guardar Figura
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jerarquia_renderizado.pdf')
    plt.savefig(output_path, format='pdf', bbox_inches='tight', dpi=300, transparent=True)
    print(f"Diagrama generado exitosamente en: {output_path}")

if __name__ == "__main__":
    main()
