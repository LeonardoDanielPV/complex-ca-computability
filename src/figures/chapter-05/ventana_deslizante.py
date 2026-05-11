#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_diagrama_conmutativo.py
===========================
Genera la figura teórica "fig:diagrama_conmutativo" (ventana deslizante)
para el Capítulo 5 del Trabajo Terminal:
"Computabilidad en autómatas celulares complejos".

Salida: diagrama_conmutativo.pdf
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # backend sin ventana
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Rectangle

# ──────────────────────────────────────────────
#  Configuración global de estilo
# ──────────────────────────────────────────────
plt.rcParams.update({
    "font.family":    "serif",
    "font.serif":     ["Times New Roman", "CMU Serif", "DejaVu Serif"],
    "mathtext.fontset": "cm",          # Computer Modern para fórmulas
    "text.usetex":    False,           # no requiere instalación LaTeX
    "axes.unicode_minus": False,
})

# ──────────────────────────────────────────────
#  Paleta de colores académica
# ──────────────────────────────────────────────
COL_BG_INACTIVE  = "#EFEFEF"   # fondo de celdas inactivas
COL_BORDER       = "#2C3E50"   # bordes de la retícula y marco de P
COL_WINDOW_BG    = "#D4E6F1"   # fondo de la ventana deslizante
COL_MATCH        = "#7B241C"   # celdas coincidentes (glider Spiral)
COL_ARROW        = "#2C3E50"   # flechas indicadoras de barrido
COL_LABEL        = "#2C3E50"   # texto principal

# ──────────────────────────────────────────────
#  Dimensiones de la retícula y la ventana
# ──────────────────────────────────────────────
GRID_ROWS = 12
GRID_COLS = 12
CELL_SIZE = 1.0               # tamaño de cada celda (unidades arbitrarias)

# Origen de la ventana deslizante P (esquina superior-izquierda, 0-indexed)
WIN_ROW = 4
WIN_COL = 4
WIN_SIZE = 4                   # ventana 4×4

# Celdas coincidentes dentro de P (coords relativas a la ventana)
# Patrón asimétrico conexo simulando un fragmento del glider Spiral
MATCH_CELLS = [
    (0, 1),
    (1, 0),
    (1, 1),
    (2, 1),
    (2, 2),
]


def draw_grid(ax):
    """Dibuja la retícula global de 12×12 con celdas inactivas."""
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            x = c * CELL_SIZE
            # Invertimos eje-y para que fila 0 quede arriba
            y = (GRID_ROWS - 1 - r) * CELL_SIZE
            rect = Rectangle(
                (x, y), CELL_SIZE, CELL_SIZE,
                linewidth=0.4,
                edgecolor=COL_BORDER,
                facecolor=COL_BG_INACTIVE,
                zorder=1,
            )
            ax.add_patch(rect)


def draw_window(ax):
    """
    Dibuja la ventana deslizante P sobre la retícula.
    Las celdas de la ventana que NO son coincidentes se rellenan con azul tenue;
    las celdas coincidentes se rellenan con el acento rojo.
    """
    match_set = set(MATCH_CELLS)

    for dr in range(WIN_SIZE):
        for dc in range(WIN_SIZE):
            r = WIN_ROW + dr
            c = WIN_COL + dc
            x = c * CELL_SIZE
            y = (GRID_ROWS - 1 - r) * CELL_SIZE

            is_match = (dr, dc) in match_set
            face = COL_MATCH if is_match else COL_WINDOW_BG

            rect = Rectangle(
                (x, y), CELL_SIZE, CELL_SIZE,
                linewidth=0.4,
                edgecolor=COL_BORDER,
                facecolor=face,
                zorder=2,
            )
            ax.add_patch(rect)

    # Marco grueso alrededor de toda la ventana P
    x0 = WIN_COL * CELL_SIZE
    y0 = (GRID_ROWS - 1 - (WIN_ROW + WIN_SIZE - 1)) * CELL_SIZE
    border = Rectangle(
        (x0, y0),
        WIN_SIZE * CELL_SIZE,
        WIN_SIZE * CELL_SIZE,
        linewidth=2.5,
        edgecolor=COL_BORDER,
        facecolor="none",
        zorder=5,
    )
    ax.add_patch(border)


def draw_arrows(ax):
    """
    Flechas elegantes que indican la dirección del barrido
    del algoritmo de ventana deslizante (derecha y abajo).
    """
    # Coordenadas de la esquina inferior-derecha de la ventana
    win_right  = (WIN_COL + WIN_SIZE) * CELL_SIZE
    win_top    = (GRID_ROWS - 1 - WIN_ROW) * CELL_SIZE + CELL_SIZE
    win_bottom = (GRID_ROWS - 1 - (WIN_ROW + WIN_SIZE - 1)) * CELL_SIZE
    win_mid_y  = (win_top + win_bottom) / 2.0
    win_mid_x  = (WIN_COL * CELL_SIZE + win_right) / 2.0

    arrow_style = "Simple,head_width=8,head_length=6,tail_width=2"

    # Flecha horizontal → (dirección de columna)
    arrow_h = FancyArrowPatch(
        (win_right + 0.3, win_mid_y),
        (win_right + 2.4, win_mid_y),
        arrowstyle=arrow_style,
        color=COL_ARROW,
        alpha=0.70,
        zorder=6,
        mutation_scale=1,
    )
    ax.add_patch(arrow_h)

    # Flecha vertical ↓ (dirección de fila)
    arrow_v = FancyArrowPatch(
        (win_mid_x, win_bottom - 0.3),
        (win_mid_x, win_bottom - 2.4),
        arrowstyle=arrow_style,
        color=COL_ARROW,
        alpha=0.70,
        zorder=6,
        mutation_scale=1,
    )
    ax.add_patch(arrow_v)

    # Etiqueta descriptiva junto a la flecha horizontal
    ax.text(
        win_right + 1.35, win_mid_y + 0.55,
        r"$Barrido\ j$",
        fontsize=9,
        color=COL_LABEL,
        ha="center", va="bottom",
        style="italic",
        zorder=7,
    )

    # Etiqueta junto a la flecha vertical
    ax.text(
        win_mid_x + 0.75, win_bottom - 1.35,
        r"$Barrido\ i$",
        fontsize=9,
        color=COL_LABEL,
        ha="left", va="center",
        style="italic",
        zorder=7,
    )


def draw_labels(ax):
    """
    Coloca las etiquetas matemáticas con notación LaTeX.
    """
    # ── Etiqueta de la retícula global X_{M×N} ──
    ax.text(
        -0.3, GRID_ROWS * CELL_SIZE + 0.55,
        r"$\mathbf{X}_{M \times N}$",
        fontsize=16,
        fontweight="bold",
        color=COL_LABEL,
        ha="left", va="bottom",
        zorder=10,
    )

    # ── Etiqueta de la ventana patrón P_{u×v} ──
    # Ubicada arriba-derecha de la ventana con línea de conexión
    label_x = (WIN_COL + WIN_SIZE) * CELL_SIZE + 0.25
    label_y = (GRID_ROWS - 1 - WIN_ROW) * CELL_SIZE + CELL_SIZE + 0.8

    ax.annotate(
        r"$\mathbf{P}_{u \times v}$",
        xy=(
            (WIN_COL + WIN_SIZE) * CELL_SIZE,
            (GRID_ROWS - 1 - WIN_ROW) * CELL_SIZE + CELL_SIZE,
        ),
        xytext=(label_x + 0.6, label_y + 0.5),
        fontsize=14,
        fontweight="bold",
        color=COL_LABEL,
        ha="left", va="bottom",
        arrowprops=dict(
            arrowstyle="-|>",
            color=COL_BORDER,
            lw=1.2,
            connectionstyle="arc3,rad=-0.15",
        ),
        zorder=10,
    )

    # ── Texto descriptivo centrado debajo del diagrama ──
    ax.text(
        (GRID_COLS * CELL_SIZE) / 2.0,
        -1.2,
        r"$Evaluaci\acute{o}n\ de\ \mathbf{P} \subseteq \mathbf{X}$",
        fontsize=12,
        color=COL_LABEL,
        ha="center", va="top",
        zorder=10,
    )

    # ── Leyenda de colores (pequeña, esquina inferior derecha) ──
    legend_x = GRID_COLS * CELL_SIZE + 0.6
    legend_y_start = 3.0
    box_sz = 0.45
    gap = 0.75

    legend_items = [
        (COL_BG_INACTIVE, "Celda inactiva"),
        (COL_WINDOW_BG,   "Ventana $\\mathbf{P}$"),
        (COL_MATCH,       "Coincidencia (glider)"),
    ]

    for idx, (color, text) in enumerate(legend_items):
        y_pos = legend_y_start - idx * gap
        legend_box = Rectangle(
            (legend_x, y_pos), box_sz, box_sz,
            linewidth=0.6,
            edgecolor=COL_BORDER,
            facecolor=color,
            zorder=8,
        )
        ax.add_patch(legend_box)
        ax.text(
            legend_x + box_sz + 0.2, y_pos + box_sz / 2.0,
            text,
            fontsize=8,
            color=COL_LABEL,
            ha="left", va="center",
            zorder=8,
        )


def main():
    fig, ax = plt.subplots(
        figsize=(8.5, 8.5),
        dpi=300,
    )
    ax.set_aspect("equal")
    ax.axis("off")

    # Dibujar capas en orden
    draw_grid(ax)
    draw_window(ax)
    draw_arrows(ax)
    draw_labels(ax)

    # Ajustar límites con margen generoso para las etiquetas
    margin = 2.0
    ax.set_xlim(-margin, GRID_COLS * CELL_SIZE + 5.0)
    ax.set_ylim(-margin, GRID_ROWS * CELL_SIZE + margin)

    plt.tight_layout(pad=0.5)
    output_path = "ventana_deslizante.pdf"
    fig.savefig(output_path, format="pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Figura guardada en: {output_path}")


if __name__ == "__main__":
    main()
