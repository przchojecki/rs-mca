#!/usr/bin/env python3
"""Radial SVG renderer for the prize dependency DAG (stdlib only).

Layout: the PRIZE sits at the CENTER; dependencies fan outward on
concentric rings (ring = longest path to the root). Angular sectors are
assigned by a spanning tree weighted by leaf counts (classic radial tree),
then tree children are re-ordered once by the circular mean of their
subtrees' cross-edge neighbors to shorten the non-tree arcs; a min-
separation pass prevents same-ring crowding. Ring radii grow adaptively so
each ring has circumference for its population. Every node is labeled
(wrapped title + status); the canvas is deliberately large and meant to be
zoomed regionally (SVG = lossless).

Encoding: fill by status (see legend); req solid / alt dashed / ev dotted /
ref sparse red; fork tick = gate ANY; bold = key node.

Run:  python3 experimental/scripts/plot_prize_dag.py
Writes experimental/data/prize-dag/prize_dag.svg (deterministic).
"""
from __future__ import annotations

import json
import math
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DDIR = os.path.join(REPO, "experimental", "data", "prize-dag")

COLORS = {"PROVED": "#1b7837", "PROVABLE": "#7fbf7b", "CONDITIONAL": "#35978f",
          "CONJECTURE": "#e6a817", "TARGET": "#a8b8c8", "WALL": "#c0392b",
          "TEST": "#5c6bc0", "REFUTED": "#d62728"}
EDGE = {"req": 'stroke="#9aa4ac" stroke-width="1.0"',
        "alt": 'stroke="#9aa4ac" stroke-width="1.0" stroke-dasharray="6,4"',
        "ev": 'stroke="#a9b8c2" stroke-width="0.8" stroke-dasharray="2,3"',
        "ref": 'stroke="#d98880" stroke-width="0.8" stroke-dasharray="8,3"'}

DR_MIN = 380        # minimum ring spacing
ARC = 310           # arc length reserved per node on its ring
FONT = 15
LINE_H = 18
WRAP = 26           # chars per label line
LABEL_OFF = 28      # gap between node and label block


def wrap_text(t: str, width: int = WRAP, max_lines: int = 3) -> list[str]:
    words, lines, cur = t.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][:width - 1] + "…"
    return lines


def circ_mean(angles: list[float]) -> float | None:
    if not angles:
        return None
    sx = sum(math.cos(a) for a in angles)
    sy = sum(math.sin(a) for a in angles)
    if sx == sy == 0:
        return None
    return math.atan2(sy, sx) % (2 * math.pi)


def main() -> None:
    data = json.load(open(os.path.join(DDIR, "prize_dag.json")))
    nodes = {n["id"]: n for n in data["nodes"]}
    edges = data["edges"]
    root = data["root"]

    out = {i: [] for i in nodes}          # toward root
    for e in edges:
        out[e["from"]].append(e["to"])

    ring: dict[str, int] = {}
    def depth(v: str) -> int:
        if v == root:
            return 0
        if v in ring:
            return ring[v]
        ring[v] = max([depth(w) + 1 for w in out[v]] or [1])
        return ring[v]
    for v in nodes:
        depth(v)
    ring[root] = 0

    # spanning tree: primary parent = out-neighbor closest to root (tie: id)
    tree_kids: dict[str, list[str]] = {i: [] for i in nodes}
    for v in sorted(nodes):
        if v == root:
            continue
        parent = min(out[v], key=lambda w: (ring[w], w))
        tree_kids[parent].append(v)

    leaves: dict[str, int] = {}
    def count_leaves(v: str) -> int:
        if not tree_kids[v]:
            leaves[v] = 1
            return 1
        leaves[v] = sum(count_leaves(c) for c in tree_kids[v])
        return leaves[v]
    count_leaves(root)

    def assign(order_hint: dict[str, float] | None) -> dict[str, float]:
        ang: dict[str, float] = {root: 0.0}
        def rec(v: str, a0: float, a1: float) -> None:
            kids = tree_kids[v]
            if order_hint:
                kids = sorted(kids, key=lambda c: (order_hint.get(c, (a0 + a1) / 2), c))
            total = sum(leaves[c] for c in kids) or 1
            a = a0
            for c in kids:
                w = (a1 - a0) * leaves[c] / total
                ang[c] = a + w / 2
                rec(c, a, a + w)
                a += w
        rec(root, 0.0, 2 * math.pi)
        return ang

    ang = assign(None)
    # one reorder pass: pull subtrees toward their cross-edge neighbors
    cross_nbrs: dict[str, list[str]] = {i: [] for i in nodes}
    tree_pairs = {(c, min(out[c], key=lambda w: (ring[w], w))) for c in nodes if c != root}
    for e in edges:
        if (e["from"], e["to"]) not in tree_pairs:
            cross_nbrs[e["from"]].append(e["to"])
            cross_nbrs[e["to"]].append(e["from"])
    def subtree_ids(v: str) -> list[str]:
        acc = [v]
        for c in tree_kids[v]:
            acc.extend(subtree_ids(c))
        return acc
    hint: dict[str, float] = {}
    for v in nodes:
        alist = [ang[w] for u in subtree_ids(v) for w in cross_nbrs[u]]
        m = circ_mean(alist)
        hint[v] = m if m is not None else ang[v]
    ang = assign(hint)

    # adaptive ring radii + min-separation within each ring
    nring = max(ring.values()) + 1
    counts = [sum(1 for v in nodes if ring[v] == k) for k in range(nring)]
    R = [0.0] * nring
    for k in range(1, nring):
        R[k] = max(R[k - 1] + DR_MIN, counts[k] * ARC / (2 * math.pi))
    for k in range(1, nring):
        members = sorted((v for v in nodes if ring[v] == k), key=lambda v: (ang[v], v))
        minsep = ARC / R[k]
        for i in range(1, len(members)):
            prev, cur = members[i - 1], members[i]
            if ang[cur] - ang[prev] < minsep:
                ang[cur] = ang[prev] + minsep

    Rmax = R[-1]
    C = Rmax
    xy: dict[str, tuple[float, float]] = {}
    for v in nodes:
        r = R[ring[v]]
        xy[v] = (C + r * math.cos(ang[v]), C + r * math.sin(ang[v]))

    # crop the canvas to actual content (labels included), uniform margin
    LBL_W, LBL_H, MARG = 270, 115, 70
    xmin = min(x - LBL_W for x, _ in xy.values())
    xmax = max(x + LBL_W for x, _ in xy.values())
    ymin = min(y - LBL_H for _, y in xy.values())
    ymax = max(y + LBL_H for _, y in xy.values())
    dx, dy = MARG - xmin, MARG - ymin
    Wd, Hd = int(xmax - xmin + 2 * MARG), int(ymax - ymin + 2 * MARG)

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wd}" height="{Hd}" '
           f'viewBox="0 0 {Wd} {Hd}" font-family="Helvetica,Arial,sans-serif">',
           f'<rect width="{Wd}" height="{Hd}" fill="#fbfcfd"/>',
           f'<g transform="translate({dx:.0f},{dy:.0f})">']
    for e in edges:             # polar-interpolated links (leave/arrive along radii)
        a1, r1 = ang[e["from"]], R[ring[e["from"]]]
        a2, r2 = ang[e["to"]], R[ring[e["to"]]]
        x1, y1 = xy[e["from"]]
        x2, y2 = xy[e["to"]]
        rm = (r1 + r2) / 2
        c1x, c1y = C + rm * math.cos(a1), C + rm * math.sin(a1)
        c2x, c2y = C + rm * math.cos(a2), C + rm * math.sin(a2)
        svg.append(f'<path d="M{x1:.0f},{y1:.0f} C{c1x:.0f},{c1y:.0f} '
                   f'{c2x:.0f},{c2y:.0f} {x2:.0f},{y2:.0f}" fill="none" {EDGE[e["kind"]]}/>')
    for v, n in nodes.items():
        x, y = xy[v]
        c = COLORS[n["status"]]
        svg.append(f'<g><title>{escape(v)}: {escape(n["title"])} [{n["status"]}]</title>')
        if n["status"] == "REFUTED":
            svg.append(f'<g stroke="{c}" stroke-width="3.5">'
                       f'<line x1="{x-9:.0f}" y1="{y-9:.0f}" x2="{x+9:.0f}" y2="{y+9:.0f}"/>'
                       f'<line x1="{x-9:.0f}" y1="{y+9:.0f}" x2="{x+9:.0f}" y2="{y-9:.0f}"/></g>')
        elif n["status"] == "TEST":
            svg.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="#fbfcfd" '
                       f'stroke="{c}" stroke-width="3"/>')
        else:
            svg.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{20 if v == root else 12}" fill="{c}"/>')
        if n.get("gate") == "any":
            svg.append(f'<path d="M{x-8:.0f},{y+18:.0f} L{x:.0f},{y+26:.0f} L{x+8:.0f},{y+18:.0f}" '
                       f'fill="none" stroke="#666" stroke-width="2"/>')
        lines = wrap_text(n["title"]) + [f'[{n["status"]}]']
        weight = ' font-weight="bold"' if n.get("key") else ""
        if v == root:
            ux, uy, anchor = 0.0, 1.0, "middle"
        else:
            ux, uy = math.cos(ang[v]), math.sin(ang[v])
            anchor = "start" if ux >= 0.35 else ("end" if ux <= -0.35 else "middle")
        lx = x + ux * LABEL_OFF
        ly = y + uy * LABEL_OFF
        block_h = LINE_H * (len(lines) - 1)
        if anchor == "middle":
            ly = ly + 20 if uy > 0 else ly - block_h - 12
        else:
            ly -= block_h / 2 - 5
        for li, line in enumerate(lines):
            small = ' font-size="12" fill="#8a949c"' if li == len(lines) - 1 else \
                    f' font-size="{FONT}" fill="#333"'
            svg.append(f'<text x="{lx:.0f}" y="{ly + LINE_H * li:.0f}" text-anchor="{anchor}"'
                       f'{small}{weight}>{escape(line)}</text>')
        svg.append('</g>')
    svg.append('</g>')   # end translated graph group
    lx0, ly0 = 60, 80
    # legend collision check (informational): graph nodes inside the legend box?
    leg_w, leg_h = 560, 620
    clash = [v for v, (x, y) in xy.items()
             if x + dx < lx0 + leg_w and y + dy < ly0 + leg_h]
    if clash:
        print(f"WARNING: {len(clash)} node(s) under the legend box: {clash[:4]}")
    counts2: dict[str, int] = {}
    for n in nodes.values():
        counts2[n["status"]] = counts2.get(n["status"], 0) + 1
    svg.append(f'<text x="{lx0}" y="{ly0}" font-size="30" fill="#555">'
               f'{len(nodes)} nodes, {len(edges)} edges | distance from center = dependency '
               f'depth (prize at the center)</text>')
    svg.append(f'<text x="{lx0}" y="{ly0 + 40}" font-size="30" fill="#555">'
               f'solid=req dashed=alt dotted=evidence sparse-red=refutes | '
               f'fork tick = gate ANY | bold = key</text>')
    svg.append(f'<text x="{lx0}" y="{ly0 + 80}" font-size="30" fill="#555">'
               + "  ".join(f"{k}:{v}" for k, v in sorted(counts2.items())) + '</text>')
    for i, (st, c) in enumerate(COLORS.items()):
        cy = ly0 + 130 + 52 * i
        if st == "REFUTED":
            svg.append(f'<g stroke="{c}" stroke-width="4">'
                       f'<line x1="{lx0 + 4}" y1="{cy - 12}" x2="{lx0 + 28}" y2="{cy + 12}"/>'
                       f'<line x1="{lx0 + 4}" y1="{cy + 12}" x2="{lx0 + 28}" y2="{cy - 12}"/></g>')
        elif st == "TEST":
            svg.append(f'<circle cx="{lx0 + 16}" cy="{cy}" r="13" fill="#fbfcfd" '
                       f'stroke="{c}" stroke-width="4"/>')
        else:
            svg.append(f'<circle cx="{lx0 + 16}" cy="{cy}" r="15" fill="{c}"/>')
        svg.append(f'<text x="{lx0 + 44}" y="{cy + 10}" font-size="32" '
                   f'fill="#444">{st}</text>')
    svg.append("</svg>")
    path = os.path.join(DDIR, "prize_dag.svg")
    with open(path, "w") as fh:
        fh.write("\n".join(svg))
    print(f"wrote {path} ({len(nodes)} nodes, {len(edges)} edges, "
          f"{nring} rings, Rmax {Rmax:.0f}, canvas {Wd}x{Hd})")


if __name__ == "__main__":
    main()
