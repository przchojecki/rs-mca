#!/usr/bin/env python3
"""Minimal SVG renderer for the prize dependency DAG (stdlib only).

Layout: root (the prize) at the TOP; a node's layer = longest path to the
root; within-layer order by a deterministic barycenter pass to reduce
crossings. Design goal per the maintainers of this chart: EVERY node in the
picture, minimal ink, labels only on nodes marked "key".

Encoding:
  fill by status  PROVED dark green / PROVABLE light green / CONDITIONAL
                  teal / CONJECTURE amber / TARGET pale grey-blue /
                  WALL red / TEST indigo ring / REFUTED grey cross
  edges           req solid grey, alt dashed, ev dotted (light), ref thin red
  gate=any        drawn as a small fork tick under the node

Run:  python3 experimental/scripts/plot_prize_dag.py
Writes experimental/data/prize-dag/prize_dag.svg (deterministic).
"""
from __future__ import annotations

import json
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DDIR = os.path.join(REPO, "experimental", "data", "prize-dag")

COLORS = {"PROVED": "#1b7837", "PROVABLE": "#7fbf7b", "CONDITIONAL": "#35978f",
          "CONJECTURE": "#e6a817", "TARGET": "#a8b8c8", "WALL": "#c0392b",
          "TEST": "#5c6bc0", "REFUTED": "#9e9e9e"}
EDGE = {"req": ('stroke="#9aa4ac" stroke-width="0.8"', None),
        "alt": ('stroke="#9aa4ac" stroke-width="0.8" stroke-dasharray="4,3"', None),
        "ev": ('stroke="#a9b8c2" stroke-width="0.75" stroke-dasharray="1.5,2.5"', None),
        "ref": ('stroke="#d98880" stroke-width="0.6" stroke-dasharray="6,2"', None)}


def main() -> None:
    data = json.load(open(os.path.join(DDIR, "prize_dag.json")))
    nodes = {n["id"]: n for n in data["nodes"]}
    edges = data["edges"]
    root = data["root"]

    out = {i: [] for i in nodes}
    for e in edges:
        out[e["from"]].append(e["to"])

    # layer = longest path to root (root = 0), memoized
    layer: dict[str, int] = {}
    def depth(v: str, seen=()) -> int:
        if v == root:
            return 0
        if v in layer:
            return layer[v]
        ds = [depth(w) + 1 for w in out[v]] or [1]
        layer[v] = max(ds)
        return layer[v]
    for v in nodes:
        depth(v)
    layer[root] = 0
    nlay = max(layer.values()) + 1
    rows: list[list[str]] = [[] for _ in range(nlay)]
    for v in sorted(nodes):
        rows[layer[v]].append(v)

    # barycenter ordering, few deterministic sweeps
    nbrs: dict[str, list[str]] = {i: [] for i in nodes}
    for e in edges:
        nbrs[e["from"]].append(e["to"])
        nbrs[e["to"]].append(e["from"])
    pos: dict[str, float] = {}
    for _ in range(6):
        for row in rows:
            for i, v in enumerate(row):
                pos[v] = i
            row.sort(key=lambda v: (sum(pos.get(w, 0.0) for w in nbrs[v]) / len(nbrs[v])
                                    if nbrs[v] else pos[v], v))
    MAXROW = 8
    drawn: list[tuple[list[str], bool]] = []   # (sub-row, is_first_of_layer)
    for row in rows:
        chunks = [row[i:i + MAXROW] for i in range(0, len(row), MAXROW)] or [[]]
        for ci, ch in enumerate(chunks):
            drawn.append((ch, ci == 0))
    W = 40 + 92 * MAXROW
    dy_layer, dy_wrap = 72, 46                 # bigger gap at layer boundaries
    ys: list[float] = []
    y = 56.0
    for ch, first in drawn:
        if ys:
            y += dy_layer if first else dy_wrap
        ys.append(y)
    Hgt = int(y + 96)
    xy: dict[str, tuple[float, float]] = {}
    for (ch, _), yy in zip(drawn, ys):
        step = (W - 40) / (len(ch) + 1)
        for i, v in enumerate(ch):
            xy[v] = (20 + step * (i + 1), yy)

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hgt}" '
           f'font-family="Helvetica,Arial,sans-serif">',
           f'<rect width="{W}" height="{Hgt}" fill="#fbfcfd"/>']
    for e in edges:  # edges under nodes; slight curve toward the parent
        x1, y1 = xy[e["from"]]
        x2, y2 = xy[e["to"]]
        style, _ = EDGE[e["kind"]]
        mx = (x1 + x2) / 2
        svg.append(f'<path d="M{x1:.0f},{y1:.0f} C{x1:.0f},{(y1+y2)/2:.0f} '
                   f'{mx:.0f},{(y1+y2)/2:.0f} {x2:.0f},{y2:.0f}" fill="none" {style}/>')
    for v, n in nodes.items():
        x, y = xy[v]
        c = COLORS[n["status"]]
        svg.append(f'<g><title>{escape(v)}: {escape(n["title"])} [{n["status"]}]</title>')
        if n["status"] == "REFUTED":
            svg.append(f'<g stroke="{c}" stroke-width="1.4">'
                       f'<line x1="{x-4:.0f}" y1="{y-4:.0f}" x2="{x+4:.0f}" y2="{y+4:.0f}"/>'
                       f'<line x1="{x-4:.0f}" y1="{y+4:.0f}" x2="{x+4:.0f}" y2="{y-4:.0f}"/></g>')
        elif n["status"] == "TEST":
            svg.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4.5" fill="none" '
                       f'stroke="{c}" stroke-width="1.6"/>')
        else:
            svg.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{7 if v == root else 5}" fill="{c}"/>')
        if n.get("gate") == "any":
            svg.append(f'<path d="M{x-4:.0f},{y+8:.0f} L{x:.0f},{y+12:.0f} L{x+4:.0f},{y+8:.0f}" '
                       f'fill="none" stroke="#666" stroke-width="0.9"/>')
        if n.get("key"):
            lbl = escape(n["title"].split(":")[0][:34])
            if x > W - 190:
                svg.append(f'<text x="{x-8:.0f}" y="{y+3:.0f}" font-size="9" fill="#333" '
                           f'text-anchor="end">{lbl}</text>')
            else:
                svg.append(f'<text x="{x+8:.0f}" y="{y+3:.0f}" font-size="9" fill="#333">{lbl}</text>')
        svg.append('</g>')
    # legend + stats
    lx, ly = 16, Hgt - 26
    for i, (s, c) in enumerate(COLORS.items()):
        svg.append(f'<circle cx="{lx + 108*i + 5}" cy="{ly}" r="4" fill="{c}"/>')
        svg.append(f'<text x="{lx + 108*i + 13}" y="{ly+3}" font-size="9" fill="#444">{s}</text>')
    counts: dict[str, int] = {}
    for n in nodes.values():
        counts[n["status"]] = counts.get(n["status"], 0) + 1
    svg.append(f'<text x="{lx}" y="{ly-14}" font-size="9" fill="#666">'
               f'{len(nodes)} nodes, {len(edges)} edges | solid=req dashed=alt dotted=evidence | '
               f'fork tick = gate ANY | ' + " ".join(f"{k}:{v}" for k, v in sorted(counts.items()))
               + '</text>')
    svg.append("</svg>")
    path = os.path.join(DDIR, "prize_dag.svg")
    with open(path, "w") as fh:
        fh.write("\n".join(svg))
    print(f"wrote {path} ({len(nodes)} nodes, {len(edges)} edges, {nlay} layers, {W}x{Hgt})")


if __name__ == "__main__":
    main()
