#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_mapeo_inverso.py
========================
Genera la figura teórica 'fig:mapeo_inverso' para el Capítulo 3 del
Trabajo Terminal "Computabilidad en autómatas celulares complejos".

La figura ilustra el isomorfismo inverso Φ⁻¹ : ℝ² → ℤ² mediante tres
secciones horizontales:
  1. Dominio Continuo (teselación hexagonal con punto P(x,y))
  2. Transición algebraica (flecha con la función de mapeo)
  3. Dominio Discreto (cuadrícula ortogonal con celda destino (i,j))

Salida: report/figures/chapter-03/mapeo_inverso.pdf

Autor: Generado automáticamente para el documento técnico.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.path import Path
import matplotlib.patheffects as pe
import os

# ============================================================================
# 0. CONFIGURACIÓN GLOBAL DE ESTILO
# ============================================================================

# Paleta académica sobria
COLOR_BG        = "#EFEFEF"
COLOR_DARK      = "#2C3E50"
COLOR_HIGHLIGHT = "#D4E6F1"
COLOR_ACCENT    = "#7B241C"
COLOR_WHITE     = "#FFFFFF"
COLOR_GRID_BG   = "#F8F8F8"

# Tipografía
plt.rcParams.update({
    "font.family":       "serif",
    "font.serif":        ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset":  "cm",          # Computer Modern para LaTeX math
    "font.size":         10,
    "axes.unicode_minus": False,
    "text.usetex":       False,         # No requiere instalación de LaTeX
    "pdf.fonttype":      42,            # TrueType para compatibilidad
})


# ============================================================================
# 1. FUNCIONES AUXILIARES DE GEOMETRÍA
# ============================================================================

def hexagon_vertices(cx, cy, R, orientation="pointy"):
    """
    Calcula los 6 vértices de un hexágono regular.
    
    Parámetros
    ----------
    cx, cy : float
        Centro del hexágono.
    R : float
        Circunradio.
    orientation : str
        'pointy' para punta superior (pointy-top).
    
    Retorna
    -------
    verts : ndarray (6, 2)
        Coordenadas de los vértices en orden antihorario.
    """
    if orientation == "pointy":
        angles = [np.pi / 6 + k * np.pi / 3 for k in range(6)]
    else:
        angles = [k * np.pi / 3 for k in range(6)]
    verts = np.array([(cx + R * np.cos(a), cy + R * np.sin(a)) for a in angles])
    return verts


def draw_hexagon(ax, cx, cy, R, facecolor="none", edgecolor=COLOR_DARK,
                 linewidth=1.2, zorder=2, orientation="pointy"):
    """Dibuja un hexágono regular como un Polygon patch."""
    verts = hexagon_vertices(cx, cy, R, orientation)
    hex_patch = mpatches.Polygon(
        verts, closed=True,
        facecolor=facecolor, edgecolor=edgecolor,
        linewidth=linewidth, zorder=zorder,
        joinstyle="round"
    )
    ax.add_patch(hex_patch)
    return hex_patch


def hex_center_oddr(col, row, R):
    """
    Calcula el centro (x, y) de un hexágono en coordenadas offset odd-r.
    Hexágonos pointy-top con filas desplazadas.
    """
    sqrt3 = np.sqrt(3)
    x = (col + 0.5 * (row % 2)) * sqrt3 * R
    y = row * 1.5 * R
    return x, y


# ============================================================================
# 2. SECCIÓN IZQUIERDA: DOMINIO CONTINUO (TESELACIÓN HEXAGONAL)
# ============================================================================

def draw_continuous_domain(ax, origin_x, origin_y):
    """
    Dibuja un parche de teselación hexagonal 3×3 con el hexágono central
    resaltado, un punto P(x,y) y ejes locales de referencia.
    """
    R = 0.38   # Circunradio de cada hexágono
    rows, cols = 3, 3

    # --- Dibujar todos los hexágonos ---
    centers = []
    for row in range(rows):
        for col in range(cols):
            lx, ly = hex_center_oddr(col, row, R)
            cx = origin_x + lx
            cy = origin_y - ly  # Invertir eje Y para visual natural

            is_center = (row == 1 and col == 1)
            fc = COLOR_HIGHLIGHT if is_center else COLOR_BG
            lw = 1.8 if is_center else 1.0

            draw_hexagon(ax, cx, cy, R, facecolor=fc, linewidth=lw)
            centers.append((cx, cy, is_center))

    # --- Punto P(x,y) dentro del hexágono central ---
    center_hex = [(cx, cy) for cx, cy, ic in centers if ic][0]
    px = center_hex[0] + 0.06
    py = center_hex[1] + 0.04

    # Punto con efecto de sombra
    ax.plot(px, py, 'o', color=COLOR_ACCENT, markersize=7, zorder=10,
            markeredgecolor=COLOR_DARK, markeredgewidth=0.8)

    # Etiqueta del punto
    ax.annotate(
        r"$P(x,y) \in \mathbb{R}^2$",
        xy=(px, py),
        xytext=(px + 0.25, py + 0.32),
        fontsize=9.5,
        color=COLOR_DARK,
        fontweight="bold",
        arrowprops=dict(
            arrowstyle="-|>",
            color=COLOR_DARK,
            lw=1.0,
            connectionstyle="arc3,rad=-0.2"
        ),
        zorder=12
    )

    # --- Ejes locales de referencia (X, Y) ---
    ax_origin_x = origin_x - 0.15
    ax_origin_y = origin_y - rows * 1.5 * R + 0.15
    arrow_len = 0.40

    # Eje X
    ax.annotate(
        "", xy=(ax_origin_x + arrow_len, ax_origin_y),
        xytext=(ax_origin_x, ax_origin_y),
        arrowprops=dict(arrowstyle="-|>", color=COLOR_DARK, lw=1.3),
        zorder=8
    )
    ax.text(ax_origin_x + arrow_len + 0.06, ax_origin_y - 0.02,
            r"$x$", fontsize=9, color=COLOR_DARK, va="center")

    # Eje Y
    ax.annotate(
        "", xy=(ax_origin_x, ax_origin_y + arrow_len),
        xytext=(ax_origin_x, ax_origin_y),
        arrowprops=dict(arrowstyle="-|>", color=COLOR_DARK, lw=1.3),
        zorder=8
    )
    ax.text(ax_origin_x - 0.06, ax_origin_y + arrow_len + 0.04,
            r"$y$", fontsize=9, color=COLOR_DARK, ha="center")

    # Punto de origen de ejes
    ax.plot(ax_origin_x, ax_origin_y, 'o', color=COLOR_DARK,
            markersize=3, zorder=9)

    # --- Etiqueta inferior del dominio ---
    label_y = origin_y - rows * 1.5 * R - 0.30
    label_x = origin_x + cols * np.sqrt(3) * R / 2 - 0.10
    ax.text(
        label_x, label_y,
        "Espacio Continuo Euclidiano",
        fontsize=9, fontweight="bold", color=COLOR_DARK,
        ha="center", va="top",
        bbox=dict(boxstyle="round,pad=0.25", facecolor=COLOR_WHITE,
                  edgecolor=COLOR_DARK, linewidth=0.8, alpha=0.9)
    )

    return center_hex


# ============================================================================
# 3. SECCIÓN CENTRAL: TRANSICIÓN ALGEBRAICA (FLECHA DE MAPEO)
# ============================================================================

def draw_transition_arrow(ax, x_start, x_end, y_center):
    """
    Dibuja una flecha elegante de transición con las etiquetas matemáticas
    del isomorfismo inverso Φ⁻¹.
    """
    # --- Flecha principal (gruesa, elegante) ---
    arrow = FancyArrowPatch(
        (x_start, y_center), (x_end, y_center),
        arrowstyle="-|>",
        mutation_scale=22,
        color=COLOR_DARK,
        linewidth=2.8,
        connectionstyle="arc3,rad=0",
        zorder=5,
        path_effects=[
            pe.Stroke(linewidth=4.5, foreground=COLOR_WHITE),
            pe.Normal()
        ]
    )
    ax.add_patch(arrow)

    # --- Etiqueta superior: función de mapeo ---
    mid_x = (x_start + x_end) / 2
    ax.text(
        mid_x, y_center + 0.30,
        r"$\Phi^{-1} : \mathbb{R}^2 \to \mathbb{Z}^2$",
        fontsize=12, fontweight="bold", color=COLOR_DARK,
        ha="center", va="bottom",
        bbox=dict(boxstyle="round,pad=0.3", facecolor=COLOR_WHITE,
                  edgecolor=COLOR_DARK, linewidth=0.6, alpha=0.95)
    )

    # --- Etiqueta inferior: fórmula indicativa ---
    ax.text(
        mid_x, y_center - 0.28,
        r"$q = \lfloor q_f \rceil,\ r = \lfloor r_f \rceil$",
        fontsize=8.5, color=COLOR_DARK, style="italic",
        ha="center", va="top",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="#F5F5F5",
                  edgecolor="#CCCCCC", linewidth=0.5, alpha=0.9)
    )


# ============================================================================
# 4. SECCIÓN DERECHA: DOMINIO DISCRETO (CUADRÍCULA DE MEMORIA)
# ============================================================================

def draw_discrete_domain(ax, origin_x, origin_y):
    """
    Dibuja una cuadrícula ortogonal 4×4 que representa el arreglo de memoria,
    con una celda específica resaltada como destino del mapeo.
    """
    n_rows, n_cols = 4, 4
    cell_size = 0.42

    # --- Dibujar la cuadrícula ---
    for row in range(n_rows):
        for col in range(n_cols):
            x = origin_x + col * cell_size
            y = origin_y - row * cell_size

            # Celda destino resaltada: posición (1, 2) en la cuadrícula
            is_target = (row == 1 and col == 2)

            if is_target:
                fc = COLOR_HIGHLIGHT
                ec = COLOR_ACCENT
                lw = 2.5
            else:
                fc = COLOR_GRID_BG
                ec = COLOR_DARK
                lw = 0.8

            rect = FancyBboxPatch(
                (x, y), cell_size, cell_size,
                boxstyle="square,pad=0",
                facecolor=fc, edgecolor=ec,
                linewidth=lw, zorder=3
            )
            ax.add_patch(rect)

            # Texto de índice tenue en cada celda (opcional para densidad visual)
            if not is_target:
                ax.text(
                    x + cell_size / 2, y + cell_size / 2,
                    f"{row},{col}",
                    fontsize=5.5, color="#AAAAAA",
                    ha="center", va="center", zorder=4
                )

    # --- Etiqueta de la celda destino ---
    target_x = origin_x + 2 * cell_size + cell_size / 2
    target_y = origin_y - 1 * cell_size + cell_size / 2

    ax.annotate(
        r"$(i,j) \in \mathbb{Z}^2$",
        xy=(target_x, target_y),
        xytext=(target_x + 0.55, target_y + 0.50),
        fontsize=9.5,
        fontweight="bold",
        color=COLOR_ACCENT,
        arrowprops=dict(
            arrowstyle="-|>",
            color=COLOR_ACCENT,
            lw=1.2,
            connectionstyle="arc3,rad=-0.25"
        ),
        zorder=12,
        bbox=dict(boxstyle="round,pad=0.2", facecolor=COLOR_WHITE,
                  edgecolor=COLOR_ACCENT, linewidth=0.6)
    )

    # --- Marca visual dentro de la celda destino ---
    ax.plot(target_x, target_y, 's', color=COLOR_ACCENT,
            markersize=8, zorder=10, markeredgecolor=COLOR_DARK,
            markeredgewidth=0.6)

    # --- Etiquetas de filas y columnas ---
    for col in range(n_cols):
        ax.text(
            origin_x + col * cell_size + cell_size / 2,
            origin_y + cell_size + 0.08,
            f"{col}",
            fontsize=7, color=COLOR_DARK,
            ha="center", va="bottom", fontweight="bold"
        )
    for row in range(n_rows):
        ax.text(
            origin_x - 0.12,
            origin_y - row * cell_size + cell_size / 2,
            f"{row}",
            fontsize=7, color=COLOR_DARK,
            ha="right", va="center", fontweight="bold"
        )

    # --- Etiqueta inferior del dominio ---
    label_x = origin_x + n_cols * cell_size / 2
    label_y = origin_y - n_rows * cell_size - 0.18
    ax.text(
        label_x, label_y,
        "Espacio de Memoria Discreto",
        fontsize=9, fontweight="bold", color=COLOR_DARK,
        ha="center", va="top",
        bbox=dict(boxstyle="round,pad=0.25", facecolor=COLOR_WHITE,
                  edgecolor=COLOR_DARK, linewidth=0.8, alpha=0.9)
    )

    # --- Borde exterior del arreglo (marco de memoria) ---
    outer_rect = FancyBboxPatch(
        (origin_x - 0.02, origin_y - (n_rows - 1) * cell_size - 0.02),
        n_cols * cell_size + 0.04,
        n_rows * cell_size + 0.04,
        boxstyle="round,pad=0.03",
        facecolor="none", edgecolor=COLOR_DARK,
        linewidth=1.8, zorder=2, linestyle="--"
    )
    ax.add_patch(outer_rect)

    return target_x, target_y


# ============================================================================
# 5. COMPOSICIÓN PRINCIPAL
# ============================================================================

def main():
    """Genera y guarda la figura completa del mapeo inverso."""

    # --- Crear la figura ---
    fig, ax = plt.subplots(1, 1, figsize=(12, 4.5))
    fig.patch.set_facecolor(COLOR_WHITE)
    ax.set_facecolor(COLOR_WHITE)
    ax.set_aspect("equal")
    ax.axis("off")

    # ---- Coordenadas de layout ----
    # Sección izquierda: dominio continuo
    hex_origin_x = 0.2
    hex_origin_y = 1.8

    # Sección derecha: dominio discreto
    grid_origin_x = 5.5
    grid_origin_y = 1.95

    # --- 1. Dibujar dominio continuo ---
    center_hex = draw_continuous_domain(ax, hex_origin_x, hex_origin_y)

    # --- 2. Dibujar dominio discreto ---
    target_pos = draw_discrete_domain(ax, grid_origin_x, grid_origin_y)

    # --- 3. Dibujar flecha de transición ---
    arrow_start_x = 2.5
    arrow_end_x = 5.2
    arrow_y = 1.05
    draw_transition_arrow(ax, arrow_start_x, arrow_end_x, arrow_y)

    # --- Títulos de sección (encabezados superiores) ---
    header_y = 2.55
    header_style = dict(
        fontsize=9, color=COLOR_DARK, ha="center", va="bottom",
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor=COLOR_HIGHLIGHT,
                  edgecolor=COLOR_DARK, linewidth=0.6, alpha=0.7)
    )

    ax.text(1.2, header_y, "Dominio Continuo", **header_style)
    ax.text(3.85, header_y, "Transición Algebraica", **header_style)
    ax.text(6.4, header_y, "Dominio Discreto", **header_style)

    # --- Líneas separadoras verticales sutiles ---
    for sep_x in [2.85, 5.05]:
        ax.axvline(
            x=sep_x, ymin=0.08, ymax=0.92,
            color="#D5D8DC", linewidth=0.8, linestyle=":",
            zorder=1
        )

    # --- Ajustar límites ---
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(-0.6, 2.9)

    # --- Guardar ---
    output_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "report", "figures", "chapter-03"
    )
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "mapeo_inverso.pdf")

    fig.savefig(
        output_path,
        format="pdf",
        bbox_inches="tight",
        dpi=300,
        pad_inches=0.15,
        facecolor=COLOR_WHITE
    )
    print(f"✓ Figura guardada exitosamente en:\n  {output_path}")

    # También guardar PNG para previsualización rápida
    png_path = os.path.join(output_dir, "mapeo_inverso.png")
    fig.savefig(
        png_path,
        format="png",
        bbox_inches="tight",
        dpi=200,
        pad_inches=0.15,
        facecolor=COLOR_WHITE
    )
    print(f"✓ Vista previa PNG guardada en:\n  {png_path}")

    plt.close(fig)


if __name__ == "__main__":
    main()
