#!/usr/bin/env python3
"""SVG renderer for the prize dependency DAG (stdlib only).

Design (per chart owner): EVERY node labeled with its full title; the image
is deliberately large — it is meant to be zoomed, not viewed whole (SVG is
vector, so zoom costs nothing). Root (the prize) at the TOP; a node's layer
= longest path to the root; layers wrap into sub-rows of MAXROW nodes;
generous margins so nothing clips at the edges.

Encoding:
  fill by status  PROVED dark green / PROVABLE light green / CONDITIONAL
                  teal / CONJECTURE amber / TARGET pale grey-blue /
                  WALL red / TEST indigo ring / REFUTED grey cross
  edges           req solid grey, alt dashed, ev dotted, ref sparse red
  gate=any        small fork tick under the node
  key nodes       bold label

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
EDGE = {"req": 'stroke="#9aa4ac" stroke-width="1.0"',
        "alt": 'stroke="#9aa4ac" stroke-width="1.0" stroke-dasharray="6,4"',
        "ev": 'stroke="#a9b8c2" stroke-width="0.8" stroke-dasharray="2,3"',
        "ref": 'stroke="#d98880" stroke-width="0.8" stroke-dasharray="8,3"'}

MAXROW = 6          # nodes per drawn row (portrait bias)
CELL = 280          # horizontal space per node (fits wrapped labels)
PAD = 60            # outer margin
DY_LAYER = 150      # gap at true layer boundaries
DY_WRAP = 118       # gap between wrapped sub-rows of one layer
FONT = 12
LINE_H = 14
WRAP = 30           # chars per label line


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


def main() -> None:
    data = json.load(open(os.path.join(DDIR, "prize_dag.json")))
    nodes = {n["id"]: n for n in data["nodes"]}
    edges = data["edges"]
    root = data["root"]

    out = {i: [] for i in nodes}
    for e in edges:
        out[e["from"]].append(e["to"])

    layer: dict[str, int] = {}
    def depth(v: str) -> int:
        if v == root:
            return 0
        if v in layer:
            return layer[v]
        layer[v] = max([depth(w) + 1 for w in out[v]] or [1])
        return layer[v]
    for v in nodes:
        depth(v)
    layer[root] = 0
    nlay = max(layer.values()) + 1
    rows: list[list[str]] = [[] for _ in range(nlay)]
    for v in sorted(nodes):
        rows[layer[v]].append(v)

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

    drawn: list[tuple[list[str], bool]] = []
    for row in rows:
        chunks = [row[i:i + MAXROW] for i in range(0, len(row), MAXROW)] or [[]]
        for ci, ch in enumerate(chunks):
            drawn.append((ch, ci == 0))

    W = 2 * PAD + MAXROW * CELL
    ys: list[float] = []
    y = float(PAD + 30)
    for ch, first in drawn:
        if ys:
            y += DY_LAYER if first else DY_WRAP
        ys.append(y)
    Hgt = int(y + PAD + 90)

    xy: dict[str, tuple[float, float]] = {}
    for (ch, _), yy in zip(drawn, ys):
        step = (W - 2 * PAD) / (len(ch) + 1)
        for i, v in enumerate(ch):
            xy[v] = (PAD + step * (i + 1), yy)

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hgt}" '
           f'viewBox="0 0 {W} {Hgt}" font-family="Helvetica,Arial,sans-serif">',
           f'<rect width="{W}" height="{Hgt}" fill="#fbfcfd"/>']
    for e in edges:
        x1, y1 = xy[e["from"]]
        x2, y2 = xy[e["to"]]
        mx = (x1 + x2) / 2
        svg.append(f'<path d="M{x1:.0f},{y1:.0f} C{x1:.0f},{(y1+y2)/2:.0f} '
                   f'{mx:.0f},{(y1+y2)/2:.0f} {x2:.0f},{y2:.0f}" fill="none" {EDGE[e["kind"]]}/>')
    for v, n in nodes.items():
        x, y0 = xy[v]
        c = COLORS[n["status"]]
        svg.append(f'<g><title>{escape(v)}: {escape(n["title"])} [{n["status"]}]</title>')
        if n["status"] == "REFUTED":
            svg.append(f'<g stroke="{c}" stroke-width="2">'
                       f'<line x1="{x-5:.0f}" y1="{y0-5:.0f}" x2="{x+5:.0f}" y2="{y0+5:.0f}"/>'
                       f'<line x1="{x-5:.0f}" y1="{y0+5:.0f}" x2="{x+5:.0f}" y2="{y0-5:.0f}"/></g>')
        elif n["status"] == "TEST":
            svg.append(f'<circle cx="{x:.0f}" cy="{y0:.0f}" r="6" fill="#fbfcfd" '
                       f'stroke="{c}" stroke-width="2"/>')
        else:
            svg.append(f'<circle cx="{x:.0f}" cy="{y0:.0f}" r="{9 if v == root else 7}" fill="{c}"/>')
        if n.get("gate") == "any":
            svg.append(f'<path d="M{x-5:.0f},{y0+10:.0f} L{x:.0f},{y0+15:.0f} L{x+5:.0f},{y0+10:.0f}" '
                       f'fill="none" stroke="#666" stroke-width="1.2"/>')
        weight = ' font-weight="bold"' if n.get("key") else ""
        lines = wrap_text(n["title"])
        for li, line in enumerate(lines):
            svg.append(f'<text x="{x:.0f}" y="{y0 + 26 + LINE_H * li:.0f}" font-size="{FONT}" '
                       f'fill="#333" text-anchor="middle"{weight}>{escape(line)}</text>')
        svg.append(f'<text x="{x:.0f}" y="{y0 + 26 + LINE_H * len(lines):.0f}" '
                   f'font-size="{FONT-2}" fill="#8a949c" text-anchor="middle">[{n["status"]}]</text>')
        svg.append('</g>')
    lx, ly = PAD, Hgt - 34
    for i, (s, c) in enumerate(COLORS.items()):
        svg.append(f'<circle cx="{lx + 150*i + 6}" cy="{ly}" r="5" fill="{c}"/>')
        svg.append(f'<text x="{lx + 150*i + 16}" y="{ly+4}" font-size="11" fill="#444">{s}</text>')
    counts: dict[str, int] = {}
    for n in nodes.values():
        counts[n["status"]] = counts.get(n["status"], 0) + 1
    svg.append(f'<text x="{lx}" y="{ly-20}" font-size="11" fill="#666">'
               f'{len(nodes)} nodes, {len(edges)} edges | solid=req dashed=alt dotted=evidence '
               f'sparse-red=refutes | fork tick = gate ANY | bold = key node | '
               + " ".join(f"{k}:{v}" for k, v in sorted(counts.items())) + '</text>')
    svg.append("</svg>")
    path = os.path.join(DDIR, "prize_dag.svg")
    with open(path, "w") as fh:
        fh.write("\n".join(svg))
    print(f"wrote {path} ({len(nodes)} nodes, {len(edges)} edges, {nlay} layers, {W}x{Hgt})")


if __name__ == "__main__":
    main()
