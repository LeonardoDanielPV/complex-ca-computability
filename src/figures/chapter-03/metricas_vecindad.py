#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_metricas_vecindad.py
========================
Genera la figura teórica «fig:metricas_vecindad» del Capítulo 3:
  Comparación geométrica de las vecindades inducidas por las métricas
  L₁ (Manhattan / von Neumann), L₂ (Euclídea) y L∞ (Chebyshev / Moore)
  sobre la retícula discreta Z².

Salida: metricas_vecindad.pdf  (vector, listo para \includegraphics)

Uso:
    python gen_metricas_vecindad.py
"""

import numpy as np
import matplotlib
matplotlib.use("pdf")                     # backend no-interactivo
import matplotlib.pyplot as plt
from matplotlib.patches import (
    FancyBboxPatch, Circle, Polygon, RegularPolygon
)
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as patheffects

# ──────────────────────────────────────────────
# Paleta de colores académica
# ──────────────────────────────────────────────
CLR_GRID_BG      = "#EFEFEF"       # fondo de celda
CLR_GRID_EDGE    = "#2C3E50"       # borde de retícula (tenue)
CLR_ACTIVE       = "#D4E6F1"       # celdas activas d ≤ 1
CLR_ORIGIN       = "#2C3E50"       # celda central (origen)
CLR_ORIGIN_MARK  = "#FFFFFF"       # marcador sobre origen
CLR_BALL_BORDER  = "#7B241C"       # frontera continua de B(0,1)
CLR_TITLE        = "#2C3E50"       # títulos
CLR_FORMULA      = "#2C3E50"       # fórmulas LaTeX

GRID_EDGE_ALPHA  = 0.25            # transparencia del borde de la malla
BALL_LW          = 2.2             # grosor de la frontera de la bola

# ──────────────────────────────────────────────
# Tipografía
# ──────────────────────────────────────────────
plt.rcParams.update({
    "font.family":        "serif",
    "font.serif":         ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset":   "cm",          # Computer Modern para fórmulas
    "text.usetex":        False,         # no requiere instalación de LaTeX
    "axes.unicode_minus": False,
    "pdf.fonttype":       42,            # TrueType → texto seleccionable
})


# ──────────────────────────────────────────────
# Datos de cada panel
# ──────────────────────────────────────────────
# Rango de la retícula: -2 … +2  →  5×5
RMIN, RMAX = -2, 2

def active_L1(x, y):
    """Celda activa bajo distancia Manhattan (L₁) con r=1."""
    return abs(x) + abs(y) <= 1

def active_L2(x, y):
    """Celda activa bajo distancia Euclídea (L₂) con r=1."""
    return np.sqrt(x**2 + y**2) <= 1.0

def active_Linf(x, y):
    """Celda activa bajo distancia Chebyshev (L∞) con r=1."""
    return max(abs(x), abs(y)) <= 1

panels = [
    {
        "title":  r"$L_1$: Distancia de Manhattan (von Neumann)",
        "formula": r"$d_1(\mathbf{x},\mathbf{y}) = |x_1 - y_1| + |x_2 - y_2|$",
        "active": active_L1,
        "ball":   "diamond",
    },
    {
        "title":  r"$L_2$: Distancia Euclídea",
        "formula": r"$d_2(\mathbf{x},\mathbf{y}) = \sqrt{(x_1 - y_1)^2 + (x_2 - y_2)^2}$",
        "active": active_L2,
        "ball":   "circle",
    },
    {
        "title":  r"$L_\infty$: Distancia de Chebyshev (Moore)",
        "formula": r"$d_\infty(\mathbf{x},\mathbf{y}) = \max(|x_1 - y_1|,\, |x_2 - y_2|)$",
        "active": active_Linf,
        "ball":   "square",
    },
]


# ──────────────────────────────────────────────
# Generación de la figura
# ──────────────────────────────────────────────
fig, axes = plt.subplots(
    1, 3,
    figsize=(14.5, 5.4),
    gridspec_kw={"wspace": 0.32},
)

CELL = 1.0  # tamaño de lado de cada celda

for ax, pdata in zip(axes, panels):

    ax.set_aspect("equal")
    ax.axis("off")

    # Márgenes del panel
    margin = 0.65
    ax.set_xlim(RMIN - 0.5 - margin, RMAX + 0.5 + margin)
    ax.set_ylim(RMIN - 0.5 - margin - 0.55, RMAX + 0.5 + margin + 0.45)

    # ── 1. Retícula de fondo ──────────────────────
    for ix in range(RMIN, RMAX + 1):
        for iy in range(RMIN, RMAX + 1):
            is_active = pdata["active"](ix, iy)
            is_origin = (ix == 0 and iy == 0)

            if is_origin:
                fc = CLR_ORIGIN
            elif is_active:
                fc = CLR_ACTIVE
            else:
                fc = CLR_GRID_BG

            rect = plt.Rectangle(
                (ix - 0.5, iy - 0.5), CELL, CELL,
                linewidth=0.7,
                edgecolor=CLR_GRID_EDGE,
                facecolor=fc,
                alpha=1.0 if (is_active or is_origin) else 1.0,
                zorder=1,
            )
            # Bordes tenues
            rect.set_edgecolor(
                (*matplotlib.colors.to_rgb(CLR_GRID_EDGE), GRID_EDGE_ALPHA)
            )
            ax.add_patch(rect)

    # Marcador del origen (punto blanco)
    ax.plot(
        0, 0,
        marker="o", markersize=6,
        markerfacecolor=CLR_ORIGIN_MARK,
        markeredgecolor=CLR_ORIGIN_MARK,
        markeredgewidth=0.6,
        zorder=5,
    )

    # Coordenadas tenues en cada celda
    for ix in range(RMIN, RMAX + 1):
        for iy in range(RMIN, RMAX + 1):
            is_origin = (ix == 0 and iy == 0)
            is_active = pdata["active"](ix, iy)
            # Solo mostrar coordenadas en las celdas activas para legibilidad
            if is_active or is_origin:
                txt_color = CLR_ORIGIN_MARK if is_origin else "#5D6D7E"
                ax.text(
                    ix, iy,
                    f"({ix},{iy})",
                    fontsize=5.5, fontweight="normal",
                    ha="center", va="center",
                    color=txt_color,
                    zorder=6,
                )

    # ── 2. Frontera geométrica continua B(0,1) ───
    ball_kw = dict(
        linewidth=BALL_LW,
        edgecolor=CLR_BALL_BORDER,
        facecolor="none",
        zorder=4,
        linestyle="-",
    )

    if pdata["ball"] == "diamond":
        # Rombo: vértices en (±1, 0), (0, ±1)
        diamond_verts = np.array([
            [ 1,  0],
            [ 0,  1],
            [-1,  0],
            [ 0, -1],
            [ 1,  0],   # cierre
        ])
        diamond = Polygon(diamond_verts, closed=True, **ball_kw)
        ax.add_patch(diamond)

    elif pdata["ball"] == "circle":
        circle = Circle((0, 0), radius=1.0, **ball_kw)
        ax.add_patch(circle)

    elif pdata["ball"] == "square":
        sq = plt.Rectangle(
            (-1, -1), 2, 2,
            **ball_kw,
        )
        ax.add_patch(sq)

    # ── 3. Título superior ────────────────────────
    ax.set_title(
        pdata["title"],
        fontsize=10.5,
        fontweight="bold",
        color=CLR_TITLE,
        pad=14,
    )

    # ── 4. Fórmula inferior ───────────────────────
    ax.text(
        0, RMIN - 0.5 - margin - 0.18,
        pdata["formula"],
        fontsize=9.5,
        ha="center", va="top",
        color=CLR_FORMULA,
        style="italic",
    )

# ──────────────────────────────────────────────
# Ajustes globales y exportación
# ──────────────────────────────────────────────
fig.suptitle("")   # sin super-título
fig.tight_layout(rect=[0, 0.01, 1, 0.97])

output_path = "metricas_vecindad.pdf"
fig.savefig(
    output_path,
    format="pdf",
    bbox_inches="tight",
    pad_inches=0.15,
    dpi=300,
)
plt.close(fig)
print(f"✓ Figura exportada → {output_path}")
