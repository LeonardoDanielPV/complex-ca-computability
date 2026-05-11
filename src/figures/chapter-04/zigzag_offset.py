#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_zigzag_offset.py
====================
Genera la figura teórica ``fig:zigzag_offset`` del Capítulo 4.
Muestra una cuadrícula 5×4 donde las columnas impares están desplazadas
verticalmente medio incremento respecto a las pares, ilustrando la
discontinuidad espacial del mapeo zig-zag y la operación módulo 2.

Salida: zigzag_offset.pdf
"""

import matplotlib
matplotlib.use("Agg")  # backend no interactivo

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

# ──────────────────────────── Parámetros globales ────────────────────────────
COLS, ROWS = 5, 4          # columnas i ∈ [0,4], filas j ∈ [0,3]
CELL  = 1.0                # lado de cada celda cuadrada
GAP   = 0.15               # espacio entre columnas (horizontal)
HALF  = CELL / 2.0         # desfase vertical para columnas impares

# Paleta sobria y académica
COL_EVEN_FILL  = "#EFEFEF"
COL_ODD_FILL   = "#D4E6F1"
BORDER_COLOR   = "#2C3E50"
TEXT_COLOR      = "#2C3E50"
ACCENT_COLOR   = "#7B241C"
DASH_ALPHA     = 0.40
BORDER_LW      = 1.5

# Tipografía
plt.rcParams.update({
    "text.usetex":        False,
    "mathtext.fontset":   "cm",       # Computer Modern – aspecto LaTeX
    "font.family":        "serif",
    "font.serif":         ["Times New Roman", "DejaVu Serif"],
    "font.size":          10,
})


# ─────────────────── Funciones auxiliares de geometría ───────────────────────
def cell_origin(i: int, j: int) -> tuple[float, float]:
    """Esquina inferior-izquierda de la celda (i, j)."""
    x = i * (CELL + GAP)
    y_offset = HALF if (i % 2 == 1) else 0.0
    y = j * CELL - y_offset          # desplazar hacia abajo las impares
    return x, y


def cell_center(i: int, j: int) -> tuple[float, float]:
    """Centro geométrico de la celda (i, j)."""
    ox, oy = cell_origin(i, j)
    return ox + CELL / 2.0, oy + CELL / 2.0


# ────────────────────────── Construcción de la figura ────────────────────────
fig, ax = plt.subplots(figsize=(8.5, 6.2))
ax.set_aspect("equal")
ax.axis("off")

# ① Dibujar todas las celdas (rectangles + etiquetas de coordenadas)
for i in range(COLS):
    fill = COL_EVEN_FILL if i % 2 == 0 else COL_ODD_FILL
    for j in range(ROWS):
        ox, oy = cell_origin(i, j)
        rect = mpatches.FancyBboxPatch(
            (ox, oy), CELL, CELL,
            boxstyle="round,pad=0.02",
            facecolor=fill,
            edgecolor=BORDER_COLOR,
            linewidth=BORDER_LW,
            zorder=2,
        )
        ax.add_patch(rect)

        # Etiqueta $(i, j)$
        cx, cy = cell_center(i, j)
        ax.text(
            cx, cy,
            rf"$({i},\,{j})$",
            ha="center", va="center",
            fontsize=9, color=TEXT_COLOR,
            zorder=3,
        )

# ② Líneas punteadas de referencia horizontal (desde la base de celdas pares)
#    Se proyectan desde la base de (0, j) hacia la derecha, cruzando la col 1.
for j in range(ROWS):
    y_base = cell_origin(0, j)[1]            # base de la celda par
    x_start = cell_origin(0, j)[0] - 0.10
    x_end   = cell_origin(1, j)[0] + CELL + 0.30
    ax.plot(
        [x_start, x_end], [y_base, y_base],
        linestyle=":",
        color=BORDER_COLOR,
        alpha=DASH_ALPHA,
        linewidth=1.0,
        zorder=1,
    )

# ③ Flecha de cota bidireccional que mide Δy (desfase vertical)
#    Se coloca entre la base de (0,0) y la base de (1,0).
base_00  = cell_origin(0, 0)[1]              # y-base de celda (0,0)
base_10  = cell_origin(1, 0)[1]              # y-base de celda (1,0) desplazada

# Posición x de la cota: un poco a la derecha de la columna 1
x_cota = cell_origin(1, 0)[0] + CELL + 0.35

arrow = FancyArrowPatch(
    (x_cota, base_00), (x_cota, base_10),
    arrowstyle="<->",
    color=ACCENT_COLOR,
    linewidth=1.8,
    mutation_scale=12,
    zorder=4,
)
ax.add_patch(arrow)

# Etiqueta Δy junto a la flecha
mid_y = (base_00 + base_10) / 2.0
ax.text(
    x_cota + 0.20, mid_y,
    r"$\Delta y$",
    ha="left", va="center",
    fontsize=13, fontweight="bold",
    color=ACCENT_COLOR,
    zorder=5,
)

# ④ Anotaciones de paridad en la parte superior
top_y = max(cell_origin(i, ROWS - 1)[1] + CELL for i in range(COLS)) + 0.55

# Paridad 0 centrada sobre i=0
cx0, _ = cell_center(0, ROWS - 1)
ax.text(
    cx0, top_y,
    r"Paridad 0: $i \ \text{mod} \ 2 = 0$",
    ha="center", va="bottom",
    fontsize=10, color=BORDER_COLOR,
    fontstyle="italic",
    zorder=5,
)

# Paridad 1 centrada sobre i=1
cx1, _ = cell_center(1, ROWS - 1)
ax.text(
    cx1, top_y + 0.2,
    r"Paridad 1: $i \ \text{mod} \ 2 = 1$",
    ha="center", va="bottom",
    fontsize=10, color=COL_ODD_FILL if False else ACCENT_COLOR,
    fontstyle="italic",
    zorder=5,
)

# Pequeñas flechas desde las etiquetas de paridad hacia la primera celda de cada col
for idx, cx_label in enumerate([cx0, cx1]):
    target_y = cell_origin(idx, ROWS - 1)[1] + CELL + 0.08
    ax.annotate(
        "",
        xy=(cx_label, target_y),
        xytext=(cx_label, top_y - 0.08),
        arrowprops=dict(
            arrowstyle="-|>",
            color=BORDER_COLOR,
            lw=1.0,
            alpha=0.5,
        ),
        zorder=4,
    )

# ⑤ Etiquetas de eje: índices de columna y fila (decorativas, estilo libro)
#    Columnas
for i in range(COLS):
    cx, _ = cell_center(i, 0)
    bottom_y = min(cell_origin(c, 0)[1] for c in range(COLS)) - 0.45
    ax.text(
        cx, bottom_y,
        rf"$i={i}$",
        ha="center", va="top",
        fontsize=9, color=BORDER_COLOR,
        zorder=5,
    )

# ⑥ Ajustar límites del lienzo
x_min = -0.4
x_max = cell_origin(COLS - 1, 0)[0] + CELL + 1.0
y_min = min(cell_origin(i, 0)[1] for i in range(COLS)) - 0.85
y_max = top_y + 0.55
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# ──────────────────────────── Exportación ────────────────────────────────────
output_path = "zigzag_offset.pdf"
fig.savefig(output_path, bbox_inches="tight", pad_inches=0.1)
plt.close(fig)

print(f"✓ Figura guardada exitosamente en: {output_path}")
