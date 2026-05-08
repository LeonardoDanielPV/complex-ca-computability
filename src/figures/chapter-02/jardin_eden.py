#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_jardin_eden.py
=======================
Genera la figura teórica 'fig:jardin_eden' del Capítulo 2:
Diagrama de transición de estados que ilustra la irreversibilidad espacial,
la no inyectividad del mapeo global Φ y los estados Jardín del Edén.

Salida: figures/chapter-02/jardin_eden.pdf
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # Backend no interactivo
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import matplotlib.patheffects as pe

# =============================================================================
# Configuración global de estilo
# =============================================================================
plt.rcParams.update({
    "text.usetex": False,
    "mathtext.fontset": "cm",          # Computer Modern para matemáticas
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
    "font.size": 11,
    "axes.linewidth": 0,
    "figure.dpi": 300,
})

# Paleta académica
COLOR_BG       = "#FFFFFF"       # Fondo blanco limpio
COLOR_NODE_FILL = "#D4E6F1"      # Azul pálido académico
COLOR_NODE_EDGE = "#2C3E50"      # Gris-azul oscuro (bordes y texto)
COLOR_GE_FILL   = "#F2D7D5"      # Rojo pálido para el nodo GE
COLOR_GE_EDGE   = "#7B241C"      # Rojo oscuro académico
COLOR_ARROW     = "#2C3E50"      # Color de las flechas
COLOR_ANNOT_BG  = "#F8F9F9"      # Fondo de anotaciones
COLOR_TIME_BAND = "#EFEFEF"      # Bandas temporales

# =============================================================================
# Posiciones de los nodos (coordenadas lógicas)
# =============================================================================
# Columna izquierda: Tiempo t       |  Columna derecha: Tiempo t+1
# C1 arriba-izq, C2 medio-izq      |  C3 derecha-centro
# C_GE abajo-izq                    |  C4 abajo-derecha

NODE_RADIUS = 0.38

positions = {
    "C1":  (1.5,  3.8),
    "C2":  (1.5,  2.2),
    "CGE": (1.5,  0.5),
    "C3":  (5.0,  3.0),
    "C4":  (5.0,  0.5),
}

labels = {
    "C1":  r"$C_1$",
    "C2":  r"$C_2$",
    "CGE": r"$C_{GE}$",
    "C3":  r"$C_3$",
    "C4":  r"$C_4$",
}

# =============================================================================
# Funciones auxiliares
# =============================================================================

def draw_node(ax, center, label, radius=NODE_RADIUS,
              fill_color=COLOR_NODE_FILL, edge_color=COLOR_NODE_EDGE,
              text_color=COLOR_NODE_EDGE, linewidth=1.8, fontsize=14):
    """Dibuja un nodo circular con etiqueta centrada."""
    circle = plt.Circle(center, radius,
                        facecolor=fill_color,
                        edgecolor=edge_color,
                        linewidth=linewidth,
                        zorder=3)
    ax.add_patch(circle)
    ax.text(center[0], center[1], label,
            ha="center", va="center",
            fontsize=fontsize, color=text_color,
            fontweight="bold", zorder=4)


def draw_arrow(ax, start, end, node_radius=NODE_RADIUS,
               color=COLOR_ARROW, linewidth=1.6, style="->",
               connectionstyle="arc3,rad=0.0", shrink_extra=0.02):
    """Dibuja una flecha dirigida entre dos nodos, acortada para no solapar."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dist = np.hypot(dx, dy)
    if dist == 0:
        return

    # Acortar flecha para que empiece/termine en el borde del nodo
    shrink = node_radius + shrink_extra
    ux, uy = dx / dist, dy / dist
    x_start = start[0] + ux * shrink
    y_start = start[1] + uy * shrink
    x_end   = end[0]   - ux * shrink
    y_end   = end[1]   - uy * shrink

    arrow = FancyArrowPatch(
        (x_start, y_start), (x_end, y_end),
        arrowstyle="-|>",
        mutation_scale=16,
        linewidth=linewidth,
        color=color,
        connectionstyle=connectionstyle,
        zorder=2,
    )
    ax.add_patch(arrow)


def draw_annotation_box(ax, text, xy_target, xy_text, box_color,
                         edge_color, text_color=COLOR_NODE_EDGE,
                         fontsize=8.5, arrowprops_override=None):
    """Dibuja una anotación con caja y flecha apuntando al objetivo."""
    default_arrowprops = dict(
        arrowstyle="-|>",
        color=edge_color,
        linewidth=1.2,
        connectionstyle="arc3,rad=-0.15",
    )
    if arrowprops_override:
        default_arrowprops.update(arrowprops_override)

    ax.annotate(
        text,
        xy=xy_target,
        xytext=xy_text,
        fontsize=fontsize,
        color=text_color,
        ha="center", va="center",
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor=box_color,
            edgecolor=edge_color,
            linewidth=1.2,
            alpha=0.95,
        ),
        arrowprops=default_arrowprops,
        zorder=5,
    )


# =============================================================================
# Construcción de la figura
# =============================================================================

fig, ax = plt.subplots(1, 1, figsize=(9.5, 5.8))
fig.patch.set_facecolor(COLOR_BG)
ax.set_facecolor(COLOR_BG)
ax.set_xlim(-0.5, 8.5)
ax.set_ylim(-0.8, 5.2)
ax.set_aspect("equal")
ax.axis("off")

# ── Bandas temporales de fondo ───────────────────────────────────────────────
band_left = FancyBboxPatch(
    (-0.2, -0.5), 3.4, 5.2,
    boxstyle="round,pad=0.15",
    facecolor=COLOR_TIME_BAND, edgecolor="none", alpha=0.5, zorder=0
)
ax.add_patch(band_left)

band_right = FancyBboxPatch(
    (3.6, -0.5), 3.0, 5.2,
    boxstyle="round,pad=0.15",
    facecolor=COLOR_TIME_BAND, edgecolor="none", alpha=0.5, zorder=0
)
ax.add_patch(band_right)

# Etiquetas temporales
ax.text(1.5, 4.85, r"Tiempo $t$",
        ha="center", va="center", fontsize=12,
        color="#566573", fontstyle="italic", zorder=1)
ax.text(5.0, 4.85, r"Tiempo $t\!+\!1$",
        ha="center", va="center", fontsize=12,
        color="#566573", fontstyle="italic", zorder=1)

# ── Nodos ────────────────────────────────────────────────────────────────────
# Nodos estándar (azul)
for node_id in ["C1", "C2", "C3", "C4"]:
    draw_node(ax, positions[node_id], labels[node_id],
              fill_color=COLOR_NODE_FILL, edge_color=COLOR_NODE_EDGE)

# Nodo Jardín del Edén (rojo, destacado)
draw_node(ax, positions["CGE"], labels["CGE"],
          fill_color=COLOR_GE_FILL, edge_color=COLOR_GE_EDGE,
          text_color=COLOR_GE_EDGE, linewidth=2.2, fontsize=13)

# ── Aristas (flechas de transición Φ) ────────────────────────────────────────
# C1 → C3  (convergencia, ligeramente curvada arriba)
draw_arrow(ax, positions["C1"], positions["C3"],
           connectionstyle="arc3,rad=-0.08", linewidth=1.8)

# C2 → C3  (convergencia, ligeramente curvada abajo)
draw_arrow(ax, positions["C2"], positions["C3"],
           connectionstyle="arc3,rad=0.08", linewidth=1.8)

# CGE → C4  (transición normal hacia adelante)
draw_arrow(ax, positions["CGE"], positions["C4"],
           color=COLOR_GE_EDGE, linewidth=1.8)

# ── Etiquetas Φ sobre las flechas ────────────────────────────────────────────
# Flecha C1→C3
mid_c1_c3 = (
    (positions["C1"][0] + positions["C3"][0]) / 2,
    (positions["C1"][1] + positions["C3"][1]) / 2 + 0.30,
)
ax.text(mid_c1_c3[0], mid_c1_c3[1], r"$\Phi$",
        ha="center", va="center", fontsize=11,
        color=COLOR_ARROW, fontstyle="italic", zorder=5)

# Flecha C2→C3
mid_c2_c3 = (
    (positions["C2"][0] + positions["C3"][0]) / 2,
    (positions["C2"][1] + positions["C3"][1]) / 2 - 0.28,
)
ax.text(mid_c2_c3[0], mid_c2_c3[1], r"$\Phi$",
        ha="center", va="center", fontsize=11,
        color=COLOR_ARROW, fontstyle="italic", zorder=5)

# Flecha CGE→C4
mid_ge_c4 = (
    (positions["CGE"][0] + positions["C4"][0]) / 2,
    (positions["CGE"][1] + positions["C4"][1]) / 2 + 0.25,
)
ax.text(mid_ge_c4[0], mid_ge_c4[1], r"$\Phi$",
        ha="center", va="center", fontsize=11,
        color=COLOR_GE_EDGE, fontstyle="italic", zorder=5)

# ── Anotación: No inyectividad (cerca de C3) ────────────────────────────────
annot_noninjective_text = (
    "No inyectividad:\n"
    "Convergencia de trayectorias\n"
    r"(Pérdida de información)"
)
draw_annotation_box(
    ax,
    text=annot_noninjective_text,
    xy_target=(positions["C3"][0] + NODE_RADIUS + 0.05, positions["C3"][1]),
    xy_text=(7.2, 3.8),
    box_color="#EBF5FB",
    edge_color=COLOR_NODE_EDGE,
    fontsize=8.5,
    arrowprops_override=dict(
        arrowstyle="-|>",
        color=COLOR_NODE_EDGE,
        linewidth=1.2,
        connectionstyle="arc3,rad=-0.2",
    ),
)

# ── Anotación: Jardín del Edén (apuntando a CGE) ────────────────────────────
annot_ge_text = (
    "Estado Jardín del Edén:\n"
    "Sin preimágenes\n"
    r"($\Phi^{-1}(C_{GE}) = \emptyset$)"
)
draw_annotation_box(
    ax,
    text=annot_ge_text,
    xy_target=(positions["CGE"][0], positions["CGE"][1] - NODE_RADIUS - 0.05),
    xy_text=(3.3, -0.55),
    box_color="#FDEDEC",
    edge_color=COLOR_GE_EDGE,
    text_color=COLOR_GE_EDGE,
    fontsize=8.5,
    arrowprops_override=dict(
        arrowstyle="-|>",
        color=COLOR_GE_EDGE,
        linewidth=1.2,
        connectionstyle="arc3,rad=0.25",
    ),
)

# ── Símbolo visual de "sin entrada" sobre CGE ───────────────────────────────
# Pequeña "X" estilizada o indicador de ausencia de flechas entrantes
# Dibujamos un pequeño ícono de "prohibido" (ø) sobre el nodo
ax.text(positions["CGE"][0] + NODE_RADIUS + 0.15,
        positions["CGE"][1] + NODE_RADIUS + 0.15,
        r"$\nexists$", fontsize=14, color=COLOR_GE_EDGE,
        ha="center", va="center", zorder=5,
        path_effects=[pe.withStroke(linewidth=2, foreground=COLOR_BG)])

# ── Línea punteada separadora entre columnas temporales ──────────────────────
ax.plot([3.25, 3.25], [-0.3, 4.6], linestyle="--",
        color="#ABB2B9", linewidth=0.9, zorder=1, alpha=0.7)

# ── Leyenda inferior: significado del mapeo ──────────────────────────────────
ax.text(3.25, -1,
        r"$\Phi : \Sigma^{\mathbb{Z}^d} \to \Sigma^{\mathbb{Z}^d}$"
        r" — Función de transición global",
        ha="center", va="center", fontsize=9,
        color="#7F8C8D", zorder=5)

# =============================================================================
# Guardar la figura
# =============================================================================
plt.tight_layout(pad=0.3)
output_path = "jardin_eden.pdf"
fig.savefig(output_path, format="pdf", bbox_inches="tight",
            facecolor=COLOR_BG, dpi=300)
plt.close(fig)

print(f"[OK] Figura generada exitosamente: {output_path}")
