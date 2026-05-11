#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de la figura 'espacio_toroidal.pdf'
=============================================
Capítulo 3 — Geometría computacional y formalización algebraica
Trabajo Terminal: Computabilidad en autómatas celulares complejos

Descripción:
  Diagrama topológico del espacio cociente T^2 que ilustra las
  condiciones de frontera periódicas sobre una retícula hexagonal.
  Muestra el pegado algebraico de las aristas opuestas de un
  rectángulo para formar un toroide, y la continuidad de la
  vecindad hexagonal a través de la costura.

Salida:
  report/figures/chapter-03/espacio_toroidal.pdf
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyArrow
from matplotlib.collections import PatchCollection
from matplotlib.path import Path
import matplotlib.patheffects as pe
import os

# ──────────────────────────────────────────────────────────────
# 0. CONFIGURACIÓN GLOBAL DE ESTILO
# ──────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "cm",
    "text.usetex": False,
    "font.size": 10,
})

# Paleta de colores académica
COL_BG      = "#EFEFEF"   # Fondo del rectángulo
COL_BORDER  = "#2C3E50"   # Contorno del rectángulo
COL_CENTER  = "#7B241C"   # Celda central
COL_NEIGH   = "#D4E6F1"   # Celdas vecinas
COL_HEX_BG  = "#D5D8DC"   # Hexágonos tenues de fondo
COL_ARROW_H = "#1A5276"   # Flechas horizontales (doble ▷▷)
COL_ARROW_V = "#6C3483"   # Flechas verticales   (simple ▲)
COL_ARC     = "#E74C3C"   # Arcos de conexión (costura)
COL_TEXT    = "#1B2631"   # Texto general

# ──────────────────────────────────────────────────────────────
# 1. GEOMETRÍA GENERAL DEL DIAGRAMA
# ──────────────────────────────────────────────────────────────
# Rectángulo central  (esquina inferior izquierda, ancho, alto)
RECT_X, RECT_Y = 0.0, 0.0
RECT_W, RECT_H = 10.0, 7.0

# Parámetros de la retícula hexagonal
HEX_R = 0.42          # circunradio de cada hexágono
HEX_A = HEX_R * np.sqrt(3) / 2   # apotema


# ──────────────────────────────────────────────────────────────
# 2. FUNCIONES AUXILIARES
# ──────────────────────────────────────────────────────────────
def hex_vertices(cx, cy, R):
    """Vértices de un hexágono pointy-top centrado en (cx, cy)."""
    angles = np.linspace(np.pi / 6, np.pi / 6 + 2 * np.pi, 7)
    xs = cx + R * np.cos(angles)
    ys = cy + R * np.sin(angles)
    return list(zip(xs, ys))


def hex_patch(cx, cy, R, **kwargs):
    """Devuelve un RegularPolygon (hexágono pointy-top)."""
    return mpatches.RegularPolygon(
        (cx, cy), numVertices=6, radius=R,
        orientation=0, **kwargs
    )


def hex_center_oddr(col, row, R):
    """Centro (x, y) para coordenadas offset odd-r."""
    a = R * np.sqrt(3) / 2
    x = (col + 0.5 * (row % 2)) * 2 * a
    y = row * 1.5 * R
    return x, y


def draw_arrow_on_edge(ax, start, end, color, n_arrows=2,
                       head_length=0.18, head_width=0.14,
                       lw=2.2, offset=0.0):
    """
    Dibuja n_arrows flechas equiespaciadas sobre el segmento
    (start → end).  `offset` desplaza transversalmente.
    """
    sx, sy = np.array(start, dtype=float), np.array(end, dtype=float)
    direction = sy - sx
    length = np.linalg.norm(direction)
    udir = direction / length
    # Vector normal unitario
    normal = np.array([-udir[1], udir[0]])
    for k in range(n_arrows):
        t = (k + 1) / (n_arrows + 1)
        base = sx + t * direction + normal * offset
        ax.annotate(
            "",
            xy=base + udir * head_length * 0.5,
            xytext=base - udir * head_length * 0.5,
            arrowprops=dict(
                arrowstyle="-|>",
                color=color,
                lw=lw,
                mutation_scale=14,
            ),
        )


# ──────────────────────────────────────────────────────────────
# 3. CREAR FIGURA Y EJES
# ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 9.5))
ax.set_aspect("equal")
ax.axis("off")

# Márgenes para los arcos exteriores
margin = 2.0
ax.set_xlim(RECT_X - margin, RECT_X + RECT_W + margin)
ax.set_ylim(RECT_Y - margin - 0.5, RECT_Y + RECT_H + margin + 0.5)


# ──────────────────────────────────────────────────────────────
# 4. PLANO BASE (RECTÁNGULO)
# ──────────────────────────────────────────────────────────────
rect = mpatches.FancyBboxPatch(
    (RECT_X, RECT_Y), RECT_W, RECT_H,
    boxstyle="round,pad=0.05",
    facecolor=COL_BG, edgecolor=COL_BORDER,
    linewidth=3.0, zorder=1,
)
ax.add_patch(rect)


# ──────────────────────────────────────────────────────────────
# 5. FLECHAS DE PEGADO TOPOLÓGICO
# ──────────────────────────────────────────────────────────────
arrow_off = 0.20   # separación del borde

# — Bordes superior e inferior: dobles flechas → derecha (naranja oscuro)
for y_pos in [RECT_Y - arrow_off, RECT_Y + RECT_H + arrow_off]:
    draw_arrow_on_edge(
        ax,
        (RECT_X + 0.6, y_pos), (RECT_X + RECT_W - 0.6, y_pos),
        color=COL_ARROW_H, n_arrows=2,
        head_length=0.28, head_width=0.18, lw=2.8,
    )

# — Bordes izquierdo y derecho: flechas simples ↑ (púrpura)
for x_pos in [RECT_X - arrow_off, RECT_X + RECT_W + arrow_off]:
    draw_arrow_on_edge(
        ax,
        (x_pos, RECT_Y + 0.6), (x_pos, RECT_Y + RECT_H - 0.6),
        color=COL_ARROW_V, n_arrows=1,
        head_length=0.28, head_width=0.18, lw=2.8,
    )


# ──────────────────────────────────────────────────────────────
# 6. PANAL DE HEXÁGONOS TENUES (FONDO) + lookup de posiciones
# ──────────────────────────────────────────────────────────────
# Offsets globales del origen de la cuadrícula
GRID_OX = RECT_X + HEX_A * 0.5
GRID_OY = RECT_Y + HEX_R * 0.3

def grid_pos(col, row):
    """Posición (x, y) real de la celda (col, row) en la cuadrícula."""
    cx, cy = hex_center_oddr(col, row, HEX_R)
    return cx + GRID_OX, cy + GRID_OY

bg_patches = []
n_cols = int(RECT_W / (2 * HEX_A)) + 3
n_rows = int(RECT_H / (1.5 * HEX_R)) + 3

# Construir lookup {(col, row): (x, y)} y dibujar fondo
grid_lookup = {}
for row in range(-1, n_rows + 1):
    for col in range(-1, n_cols + 1):
        cx, cy = grid_pos(col, row)
        grid_lookup[(col, row)] = (cx, cy)
        # Solo dibujar si el centro está dentro del rectángulo (con margen)
        if (RECT_X + 0.15 < cx < RECT_X + RECT_W - 0.15 and
                RECT_Y + 0.15 < cy < RECT_Y + RECT_H - 0.15):
            p = hex_patch(cx, cy, HEX_R,
                          facecolor="none",
                          edgecolor=COL_HEX_BG,
                          linewidth=0.6, zorder=2)
            bg_patches.append(p)
            ax.add_patch(p)


# ──────────────────────────────────────────────────────────────
# 7. VECINDAD HEXAGONAL EN LA FRONTERA DERECHA
# ──────────────────────────────────────────────────────────────
# Encontrar la celda de la cuadrícula cuyo centro cae más cerca
# del borde derecho a la altura media del rectángulo.
target_x = RECT_X + RECT_W
target_y = RECT_Y + RECT_H / 2

best_cell = None
best_dist = float("inf")
for (col, row), (cx, cy) in grid_lookup.items():
    d = abs(cx - target_x) + 0.3 * abs(cy - target_y)
    if d < best_dist:
        best_dist = d
        best_cell = (col, row)

center_col, center_row = best_cell
center_x, center_y = grid_lookup[best_cell]

# Tabla de vecinos odd-r  (depende de la paridad de la fila)
# Fuente: Red Blob Games — Hexagonal Grids
ODD_R_NEIGHBORS = {
    0: [  # fila par
        (+1,  0), (-1,  0),    # derecha, izquierda
        ( 0, -1), (-1, -1),    # abajo-derecha, abajo-izquierda
        ( 0, +1), (-1, +1),    # arriba-derecha, arriba-izquierda
    ],
    1: [  # fila impar
        (+1,  0), (-1,  0),
        (+1, -1), ( 0, -1),
        (+1, +1), ( 0, +1),
    ],
}

parity = center_row % 2
neighbor_cells = [
    (center_col + dc, center_row + dr)
    for dc, dr in ODD_R_NEIGHBORS[parity]
]

# Clip regions = el rectángulo principal
clip_path_right = mpatches.Rectangle(
    (RECT_X, RECT_Y), RECT_W, RECT_H,
    transform=ax.transData
)
clip_path_left = mpatches.Rectangle(
    (RECT_X, RECT_Y), RECT_W, RECT_H,
    transform=ax.transData
)

# --- Celda central (cortada por el borde derecho) ---
center_hex = hex_patch(
    center_x, center_y, HEX_R,
    facecolor=COL_CENTER, edgecolor=COL_BORDER,
    linewidth=1.8, alpha=0.92, zorder=10
)
center_hex.set_clip_path(clip_path_right)
ax.add_patch(center_hex)

# --- Vecinos (parcialmente cortados por el borde derecho) ---
right_neigh_patches = []
for nc, nr in neighbor_cells:
    nx, ny = grid_pos(nc, nr)
    p = hex_patch(
        nx, ny, HEX_R,
        facecolor=COL_NEIGH, edgecolor=COL_BORDER,
        linewidth=1.4, alpha=0.85, zorder=9
    )
    p.set_clip_path(clip_path_right)
    ax.add_patch(p)
    right_neigh_patches.append((nx, ny))


# ──────────────────────────────────────────────────────────────
# 8. PROYECCIÓN PERIÓDICA EN EL BORDE IZQUIERDO
# ──────────────────────────────────────────────────────────────
# Buscar la celda del grid más cercana al borde izquierdo
# a la misma altura que la celda central del lado derecho.
mirror_target_x = RECT_X
mirror_target_y = center_y

best_mirror = None
best_mirror_dist = float("inf")
for (col, row), (cx, cy) in grid_lookup.items():
    d = abs(cx - mirror_target_x) + 0.3 * abs(cy - mirror_target_y)
    if d < best_mirror_dist:
        best_mirror_dist = d
        best_mirror = (col, row)

mirror_col, mirror_row = best_mirror
mirror_x, mirror_y = grid_lookup[best_mirror]

# Vecinos de la celda espejo (mismas reglas odd-r)
mirror_parity = mirror_row % 2
mirror_neighbor_cells = [
    (mirror_col + dc, mirror_row + dr)
    for dc, dr in ODD_R_NEIGHBORS[mirror_parity]
]

# Celda central reflejada
mirror_center = hex_patch(
    mirror_x, mirror_y, HEX_R,
    facecolor=COL_CENTER, edgecolor=COL_BORDER,
    linewidth=1.8, alpha=0.92, zorder=10
)
mirror_center.set_clip_path(clip_path_left)
ax.add_patch(mirror_center)

# Vecinos reflejados
left_neigh_positions = []
for nc, nr in mirror_neighbor_cells:
    nx, ny = grid_pos(nc, nr)
    p = hex_patch(
        nx, ny, HEX_R,
        facecolor=COL_NEIGH, edgecolor=COL_BORDER,
        linewidth=1.4, alpha=0.85, zorder=9
    )
    p.set_clip_path(clip_path_left)
    ax.add_patch(p)
    left_neigh_positions.append((nx, ny))


# Distancias usadas por los arcos (sección 9)
dx = np.sqrt(3) * HEX_R
dy = 1.5 * HEX_R

# ──────────────────────────────────────────────────────────────
# 9. ARCOS DE CONEXIÓN (COSTURA TOROIDAL)
# ──────────────────────────────────────────────────────────────
# Conectar la celda central y algunos vecinos con arcos curvos
# que salen por la derecha y entran por la izquierda.
arc_pairs = [
    # (y_derecho, y_izquierdo, above)
    (center_y,       mirror_y,       True),
    (center_y + dy,  mirror_y + dy,  True),
    (center_y - dy,  mirror_y - dy,  False),
]

for pt_ry, pt_ly, above in arc_pairs:
    rx = center_x     # posición real de la celda en el borde derecho
    lx = mirror_x     # posición real de la celda espejo en el borde izquierdo

    # Altura de la curva (cuánto se separa del rectángulo)
    arc_h = 1.6
    if above:
        ctrl_y = max(pt_ry, pt_ly) + arc_h
    else:
        ctrl_y = min(pt_ry, pt_ly) - arc_h

    # Dos segmentos cúbicos Bézier concatenados:
    #   Segmento 1: borde derecho → ápice del arco
    #   Segmento 2: ápice del arco → borde izquierdo
    mid_x = RECT_X + RECT_W / 2
    verts = [
        (rx + 0.05, pt_ry),                    # P0 inicio
        (rx + 1.4,  pt_ry),                    # C1 salir horizontal
        (rx + 1.4,  ctrl_y),                   # C2 subir/bajar
        (mid_x,     ctrl_y),                   # P3 ápice (fin seg.1)
        (lx - 1.4,  ctrl_y),                   # C4 bajar/subir
        (lx - 1.4,  pt_ly),                    # C5 entrar horizontal
        (lx - 0.05, pt_ly),                    # P6 fin
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,   # segmento 1
        Path.CURVE4, Path.CURVE4, Path.CURVE4,   # segmento 2
    ]

    path = Path(verts, codes)
    pp = mpatches.PathPatch(
        path,
        facecolor="none",
        edgecolor=COL_ARC,
        linewidth=1.6,
        linestyle=(0, (6, 4)),
        zorder=15,
    )
    ax.add_patch(pp)

    # Punta de flecha en el extremo izquierdo (entrada)
    ax.annotate(
        "",
        xy=(lx - 0.05, pt_ly),
        xytext=(lx - 0.55, pt_ly),
        arrowprops=dict(
            arrowstyle="-|>",
            color=COL_ARC,
            lw=1.6,
            mutation_scale=13,
        ),
        zorder=16,
    )
    # Punta de flecha en el extremo derecho (salida)
    ax.annotate(
        "",
        xy=(rx + 0.55, pt_ry + (0.12 if above else -0.12)),
        xytext=(rx + 0.05, pt_ry),
        arrowprops=dict(
            arrowstyle="-|>",
            color=COL_ARC,
            lw=1.6,
            mutation_scale=13,
        ),
        zorder=16,
    )


# ──────────────────────────────────────────────────────────────
# 10. ANOTACIONES MATEMÁTICAS
# ──────────────────────────────────────────────────────────────
# Símbolo del espacio cociente T^2 — esquina superior izquierda interior
ax.text(
    RECT_X + 0.55, RECT_Y + RECT_H - 0.55,
    r"$\mathbb{T}^2 \cong \mathbb{Z}^2 / (M\mathbb{Z} \times N\mathbb{Z})$",
    fontsize=14, color=COL_TEXT,
    ha="left", va="top",
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
              edgecolor=COL_BORDER, alpha=0.85),
    zorder=20,
)

# Etiqueta de congruencia algebraica junto a la vecindad cortada (derecha)
ax.text(
    RECT_X + RECT_W + 0.35, center_y + dy + 0.95,
    r"$(i,\, j) \;\sim\; (i \ \text{mod} \ M,\; j \ \text{mod} \ N)$",
    fontsize=11, color=COL_ARC,
    ha="center", va="bottom",
    fontstyle="italic",
    bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
              edgecolor=COL_ARC, alpha=0.82, linewidth=1.0),
    zorder=20,
)

# Etiquetas de las flechas de pegado
# Horizontal
ax.text(
    RECT_X + RECT_W / 2, RECT_Y + RECT_H + 0.62,
    r"Identificación horizontal: $x \equiv x + M$",
    fontsize=9, color=COL_ARROW_H,
    ha="center", va="bottom",
    zorder=20,
)
ax.text(
    RECT_X + RECT_W / 2, RECT_Y - 0.62,
    r"Identificación horizontal: $x \equiv x + M$",
    fontsize=9, color=COL_ARROW_H,
    ha="center", va="top",
    zorder=20,
)

# Vertical
ax.text(
    RECT_X - 0.62, RECT_Y + RECT_H / 2,
    r"$y \equiv y + N$",
    fontsize=9, color=COL_ARROW_V,
    ha="right", va="center",
    rotation=90,
    zorder=20,
)
ax.text(
    RECT_X + RECT_W + 0.62, RECT_Y + RECT_H / 2,
    r"$y \equiv y + N$",
    fontsize=9, color=COL_ARROW_V,
    ha="left", va="center",
    rotation=90,
    zorder=20,
)

# Etiqueta "celda central" y "vecindad periódica"
ax.annotate(
    r"Celda central $c_{(i,j)}$",
    xy=(center_x - 0.35, center_y),
    xytext=(center_x - 2.2, center_y - 1.8),
    fontsize=9, color=COL_CENTER,
    ha="center",
    arrowprops=dict(
        arrowstyle="->",
        color=COL_CENTER,
        lw=1.2,
        connectionstyle="arc3,rad=-0.2",
    ),
    zorder=20,
    bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
              edgecolor=COL_CENTER, alpha=0.85),
)

ax.annotate(
    r"Imagen periódica $c_{(i \ \text{mod} \ M,\, j)}$",
    xy=(mirror_x + 0.35, center_y),
    xytext=(mirror_x + 2.5, center_y - 1.8),
    fontsize=9, color=COL_CENTER,
    ha="center",
    arrowprops=dict(
        arrowstyle="->",
        color=COL_CENTER,
        lw=1.2,
        connectionstyle="arc3,rad=0.2",
    ),
    zorder=20,
    bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
              edgecolor=COL_CENTER, alpha=0.85),
)

# Dimensiones M y N
ax.annotate(
    "", xy=(RECT_X + RECT_W, RECT_Y - 1.25),
    xytext=(RECT_X, RECT_Y - 1.25),
    arrowprops=dict(arrowstyle="<->", color=COL_BORDER, lw=1.5),
    zorder=20,
)
ax.text(
    RECT_X + RECT_W / 2, RECT_Y - 1.45,
    r"$M$ columnas",
    fontsize=10, color=COL_BORDER,
    ha="center", va="top",
    zorder=20,
)

ax.annotate(
    "", xy=(RECT_X - 1.25, RECT_Y + RECT_H),
    xytext=(RECT_X - 1.25, RECT_Y),
    arrowprops=dict(arrowstyle="<->", color=COL_BORDER, lw=1.5),
    zorder=20,
)
ax.text(
    RECT_X - 1.45, RECT_Y + RECT_H / 2,
    r"$N$ filas",
    fontsize=10, color=COL_BORDER,
    ha="right", va="center",
    rotation=90,
    zorder=20,
)


# ──────────────────────────────────────────────────────────────
# 11. GUARDAR FIGURA
# ──────────────────────────────────────────────────────────────
output_path = "espacio_toroidal.pdf"

fig.savefig(output_path, format="pdf", bbox_inches="tight",
            pad_inches=0.2, dpi=300)
plt.close(fig)

print(f"[OK] Figura guardada en: {output_path}")
