#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_geometria_celda.py
──────────────────────
Genera la figura «fig:geometria_celda» para el Capítulo 3 del Trabajo Terminal
"Computabilidad en autómatas celulares complejos".

Ilustra la geometría analítica de una celda hexagonal regular unitaria
(orientación pointy-top) centrada en el origen (0,0), incluyendo:
  • Hexágono regular con vértices V_k = (R cos θ_k, R sin θ_k), θ_k = π/2 + kπ/3
  • Circunradio R, apotema a, triángulo rectángulo interno
  • Ángulos de deflexión central (60°) y ángulo de la apotema (30°)
  • Anotaciones LaTeX con las constantes del modelo

Salida: geometria_celda.pdf
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")                       # backend no-interactivo
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Arc, Polygon
from matplotlib.path import Path
import matplotlib.patheffects as patheffects

# ──────────────────────────── Paleta de colores ────────────────────────────
COL_FILL    = "#D4E6F1"   # relleno del hexágono
COL_BORDER  = "#2C3E50"   # borde del hexágono
COL_RADIUS  = "#7B241C"   # línea del circunradio R
COL_APOTHEM = "#2C3E50"   # línea de la apotema a
COL_TRI     = "#EFEFEF"   # relleno del triángulo rectángulo
COL_AXIS    = "#C0C0C0"   # ejes coordenados sutiles
COL_ANGLE   = "#7B241C"   # arcos de ángulo
COL_TEXT    = "#2C3E50"   # texto general

# ──────────────────────────── Parámetros geométricos ───────────────────────
R = 1.0                                     # circunradio unitario
a = R * np.cos(np.pi / 6)                   # apotema = R cos(30°) = √3/2 R

# Vértices: θ_k = π/2 + k·π/3,  k = 0 … 5
angles = np.array([np.pi / 2 + k * np.pi / 3 for k in range(6)])
verts  = np.column_stack([R * np.cos(angles), R * np.sin(angles)])

# Puntos clave
origin       = np.array([0.0, 0.0])
V0           = verts[0]                     # vértice superior  (0, R)
V5           = verts[5]                     # vértice superior-derecho
mid_edge     = 0.5 * (V0 + V5)             # punto medio de la arista V0-V5

# ──────────────────────────── Configuración de la figura ───────────────────
plt.rcParams.update({
    "font.family":       "serif",
    "font.serif":        ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset":  "cm",              # Computer Modern para LaTeX
    "font.size":         11,
    "text.usetex":       False,             # no requiere LaTeX instalado
})

fig, ax = plt.subplots(figsize=(6.5, 7.0))
ax.set_aspect("equal")
ax.axis("off")

# ──────────────────────────── 1. Ejes coordenados sutiles ──────────────────
axis_ext = 1.55
ax.plot([-axis_ext, axis_ext], [0, 0],
        color=COL_AXIS, lw=0.5, ls="-", zorder=0)
ax.plot([0, 0], [-axis_ext, axis_ext],
        color=COL_AXIS, lw=0.5, ls="-", zorder=0)

# ──────────────────────────── 2. Hexágono base ─────────────────────────────
hex_closed = np.vstack([verts, verts[0]])    # cerrar polígono
hex_patch  = Polygon(verts, closed=True,
                     facecolor=COL_FILL, edgecolor=COL_BORDER,
                     linewidth=2.0, zorder=2)
ax.add_patch(hex_patch)

# ──────────────────────────── 3. Triángulo rectángulo interno (sombreado) ──
tri_verts = np.array([origin, mid_edge, V5])
tri_patch = Polygon(tri_verts, closed=True,
                    facecolor=COL_TRI, edgecolor=COL_BORDER,
                    linewidth=0.8, linestyle="-", alpha=0.85, zorder=3)
ax.add_patch(tri_patch)

# Marca del ángulo recto en el punto medio de la arista
sq_size = 0.06
# Vectores unitarios: desde mid_edge hacia el centro y hacia V5
u_center = (origin - mid_edge);  u_center /= np.linalg.norm(u_center)
u_vertex = (V5 - mid_edge);      u_vertex /= np.linalg.norm(u_vertex)
sq_pts = np.array([
    mid_edge + sq_size * u_center,
    mid_edge + sq_size * (u_center + u_vertex),
    mid_edge + sq_size * u_vertex,
])
ax.plot([sq_pts[0, 0], sq_pts[1, 0], sq_pts[2, 0]],
        [sq_pts[0, 1], sq_pts[1, 1], sq_pts[2, 1]],
        color=COL_BORDER, lw=0.7, zorder=5)

# ──────────────────────────── 4. Circunradio R (con flecha) ────────────────
# Línea del radio: origen → V0  (hacia el vértice superior)
arrow_style = dict(arrowstyle="-|>", color=COL_RADIUS,
                   lw=1.5, mutation_scale=12)
arrow_R = FancyArrowPatch(origin, V0, **arrow_style, zorder=6)
ax.add_patch(arrow_R)

# Etiqueta R en el punto medio del segmento, desplazada a la izquierda
mid_R = 0.5 * (origin + V0)
ax.annotate(r"$R$", xy=mid_R, fontsize=14, fontweight="bold",
            color=COL_RADIUS, ha="right", va="center",
            xytext=(-12, 0), textcoords="offset points", zorder=10)

# ──────────────────────────── 5. Apotema a (línea punteada) ────────────────
ax.plot([origin[0], mid_edge[0]], [origin[1], mid_edge[1]],
        color=COL_APOTHEM, lw=1.4, ls="--", zorder=5)

# Etiqueta a, desplazada ligeramente
mid_a = 0.5 * (origin + mid_edge)
ax.annotate(r"$a$", xy=mid_a, fontsize=14, fontweight="bold",
            color=COL_APOTHEM, ha="left", va="bottom",
            xytext=(6, 4), textcoords="offset points", zorder=10)

# Línea del lado del triángulo (mid_edge → V5) para reforzar visualmente
ax.plot([mid_edge[0], V5[0]], [mid_edge[1], V5[1]],
        color=COL_BORDER, lw=0.9, ls="-", zorder=4)

# ──────────────────────────── 6. Arco del ángulo central θ = 60° ──────────
# Ángulo desde la apotema (dirección a mid_edge) hasta el radio (dirección a V0)
angle_apothem_deg = np.degrees(np.arctan2(mid_edge[1], mid_edge[0]))
angle_V0_deg      = np.degrees(np.arctan2(V0[1], V0[0]))  # = 90°

arc_r = 0.22
arc_60 = Arc(origin, 2 * arc_r, 2 * arc_r,
             angle=0,
             theta1=angle_apothem_deg,
             theta2=angle_V0_deg,
             color=COL_ANGLE, lw=1.3, zorder=7)
ax.add_patch(arc_60)

# Etiqueta 60°
mid_arc_angle = np.radians(0.5 * (angle_apothem_deg + angle_V0_deg))
lbl_60_pos = (arc_r + 0.10) * np.array([np.cos(mid_arc_angle),
                                          np.sin(mid_arc_angle)])
ax.text(lbl_60_pos[0], lbl_60_pos[1], r"$60°$",
        fontsize=10, color=COL_ANGLE, ha="center", va="center", zorder=10)

# ──────────────────────────── 7. Arco del ángulo 30° en el vértice V5 ─────
# En el triángulo (origin, mid_edge, V5), el ángulo en V5 es 30°
vec_V5_to_origin = origin - V5
vec_V5_to_mid    = mid_edge - V5
ang_V5_origin = np.degrees(np.arctan2(vec_V5_to_origin[1], vec_V5_to_origin[0]))
ang_V5_mid    = np.degrees(np.arctan2(vec_V5_to_mid[1], vec_V5_to_mid[0]))

# Asegurar orden correcto (sentido antihorario)
if ang_V5_mid < ang_V5_origin:
    ang_V5_mid += 360

arc_30_r = 0.18
arc_30 = Arc(V5, 2 * arc_30_r, 2 * arc_30_r,
             angle=0,
             theta1=ang_V5_origin,
             theta2=ang_V5_mid,
             color=COL_ANGLE, lw=1.3, zorder=7)
ax.add_patch(arc_30)

mid_arc30 = np.radians(0.5 * (ang_V5_origin + ang_V5_mid))
lbl_30_pos = V5 + (arc_30_r + 0.12) * np.array([np.cos(mid_arc30),
                                                   np.sin(mid_arc30)])
ax.text(lbl_30_pos[0], lbl_30_pos[1], r"$30°$",
        fontsize=10, color=COL_ANGLE, ha="center", va="center", zorder=10)

# ──────────────────────────── 8. Puntos de referencia (nodos) ──────────────
node_kw = dict(marker="o", zorder=8, edgecolors=COL_BORDER, linewidths=0.8)

# Vértices del hexágono
ax.scatter(verts[:, 0], verts[:, 1], s=22,
           facecolors=COL_BORDER, **node_kw)

# Centro
ax.scatter(*origin, s=30, facecolors="white", **node_kw)

# Punto medio de la arista
ax.scatter(*mid_edge, s=22, facecolors=COL_RADIUS, **node_kw)

# ──────────────────────────── 9. Etiquetas de vértices ─────────────────────
vert_labels = [r"$V_0$", r"$V_1$", r"$V_2$", r"$V_3$", r"$V_4$", r"$V_5$"]
offsets_pts = [
    (0, 10),       # V0 - arriba
    (-14, 4),      # V1 - izquierda-arriba
    (-14, -6),     # V2 - izquierda-abajo
    (0, -14),      # V3 - abajo
    (12, -6),      # V4 - derecha-abajo
    (12, 4),       # V5 - derecha-arriba
]
for i_v, (lbl, off) in enumerate(zip(vert_labels, offsets_pts)):
    ax.annotate(lbl, xy=verts[i_v], fontsize=9, color=COL_TEXT,
                ha="center", va="center",
                xytext=off, textcoords="offset points", zorder=10)

# Etiqueta del origen
ax.annotate(r"$(0,\,0)$", xy=origin, fontsize=9, color=COL_TEXT,
            ha="right", va="top",
            xytext=(-8, -8), textcoords="offset points", zorder=10)

# ──────────────────────────── 10. Cuadro de anotaciones matemáticas ───────
textbox_str = (
    r"$a = \dfrac{\sqrt{3}}{2}\,R$"
    "\n\n"
    r"$A = \dfrac{3\sqrt{3}}{2}\,R^{\,2}$"
)



ax.text(1.6, -0.75, textbox_str,
        fontsize=13, color=COL_TEXT,
        ha="center", va="center", zorder=10,
        linespacing=1.6)

# ──────────────────────────── 11. Ajuste de límites ────────────────────────
margin = 0.45
ax.set_xlim(-R - margin, R + margin + 0.90)   # extra para el cuadro de texto
ax.set_ylim(-R - margin, R + margin)

# ──────────────────────────── 12. Guardar ──────────────────────────────────
out_path = "geometria_celda.pdf"
fig.savefig(out_path, format="pdf", bbox_inches="tight",
            pad_inches=0.05, dpi=300)
plt.close(fig)
print(f"Figura guardada en: {out_path}")
