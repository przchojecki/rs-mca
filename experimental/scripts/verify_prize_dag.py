#!/usr/bin/env python3
"""Validator for experimental/data/prize-dag/prize_dag.json (AUDIT).

Checks: unique ids; edge endpoints exist; legal statuses/kinds/gates;
acyclicity; every node reaches the root; refs resolve to real files;
REFUTED nodes are never 'req' children; and the STATUS-PROPAGATION rule:
  PROVED    requires all 'req' children PROVED (+ one PROVED 'alt' if gate=any)
  PROVABLE  requires all 'req' children in {PROVED, PROVABLE} (alts likewise)
Also emits (informational) the RIPE list: CONJECTURE/TARGET nodes whose
requirements are already all PROVED/PROVABLE — candidates to close next.

Run:  python3 experimental/scripts/verify_prize_dag.py
Exit non-zero iff any check fails (RIPE list is informational).
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))          # repo root (parent of experimental/)
DAG = os.path.join(REPO, "experimental", "data", "prize-dag", "prize_dag.json")
ROADMAPS = os.path.join(REPO, "experimental", "notes", "roadmaps")

STATUSES = {"PROVED", "PROVABLE", "CONDITIONAL", "CONJECTURE", "TARGET", "WALL", "REFUTED", "TEST"}
KINDS = {"req", "alt", "ev", "ref"}
GATES = {"all", "any"}


def main() -> None:
    with open(DAG) as fh:
        data = json.load(fh)
    nodes = {n["id"]: n for n in data["nodes"]}
    edges = data["edges"]
    errors: list[str] = []

    if len(nodes) != len(data["nodes"]):
        errors.append("duplicate node ids")
    root = data["root"]
    if root not in nodes:
        errors.append(f"root {root} missing")

    for n in data["nodes"]:
        if n["status"] not in STATUSES:
            errors.append(f"{n['id']}: illegal status {n['status']}")
        if n.get("gate", "all") not in GATES:
            errors.append(f"{n['id']}: illegal gate")
        for ref in n.get("refs", []):
            path = ref.split("#")[0]
            if not (os.path.exists(os.path.join(ROADMAPS, path))
                    or os.path.exists(os.path.join(REPO, path))):
                errors.append(f"{n['id']}: ref does not resolve: {path}")

    out: dict[str, list[str]] = {i: [] for i in nodes}
    inc: dict[str, list[tuple[str, str]]] = {i: [] for i in nodes}
    for e in edges:
        if e["from"] not in nodes or e["to"] not in nodes:
            errors.append(f"edge endpoint missing: {e}")
            continue
        if e["kind"] not in KINDS:
            errors.append(f"illegal edge kind: {e}")
            continue
        out[e["from"]].append(e["to"])
        inc[e["to"]].append((e["from"], e["kind"]))
        if e["kind"] == "req" and nodes[e["from"]]["status"] == "REFUTED":
            errors.append(f"REFUTED node {e['from']} is a 'req' child of {e['to']}")

    # acyclicity (iterative DFS) + reachability to root
    color: dict[str, int] = {}
    for start in nodes:
        if color.get(start):
            continue
        stack = [(start, iter(out[start]))]
        color[start] = 1
        while stack:
            v, it = stack[-1]
            for w in it:
                if color.get(w) == 1:
                    errors.append(f"cycle through {w}")
                    color[w] = 2
                    continue
                if not color.get(w):
                    color[w] = 1
                    stack.append((w, iter(out[w])))
                    break
            else:
                color[v] = 2
                stack.pop()
    reach = {root}
    frontier = [root]
    rev: dict[str, list[str]] = {i: [] for i in nodes}
    for e in edges:
        if e["to"] in rev:
            rev[e["to"]].append(e["from"])
    while frontier:
        v = frontier.pop()
        for w in rev[v]:
            if w not in reach:
                reach.add(w)
                frontier.append(w)
    for i in nodes:
        if i not in reach:
            errors.append(f"{i} cannot reach the root")

    # status propagation + RIPE list
    ripe: list[str] = []
    okset = {"PROVED"}
    okset2 = {"PROVED", "PROVABLE"}
    for i, n in nodes.items():
        reqs = [nodes[f]["status"] for f, k in inc[i] if k == "req"]
        alts = [nodes[f]["status"] for f, k in inc[i] if k == "alt"]
        gate_any = n.get("gate", "all") == "any" and alts
        if n["status"] == "PROVED":
            if any(s not in okset for s in reqs) or (gate_any and not any(s in okset for s in alts)):
                errors.append(f"{i}: declared PROVED but requirements are not all PROVED")
        elif n["status"] == "PROVABLE":
            if any(s not in okset2 for s in reqs) or (gate_any and not any(s in okset2 for s in alts)):
                errors.append(f"{i}: declared PROVABLE but requirements exceed PROVED/PROVABLE")
        elif n["status"] in {"CONJECTURE", "TARGET"} and (reqs or gate_any):
            if all(s in okset2 for s in reqs) and (not gate_any or any(s in okset2 for s in alts)):
                ripe.append(i)

    print(f"prize-dag: {len(nodes)} nodes, {len(edges)} edges")
    counts: dict[str, int] = {}
    for n in nodes.values():
        counts[n["status"]] = counts.get(n["status"], 0) + 1
    print("status counts:", ", ".join(f"{k}:{v}" for k, v in sorted(counts.items())))
    if ripe:
        print("RIPE (requirements met, declaration pending):", ", ".join(sorted(ripe)))
    if errors:
        print("\nFAIL:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("PASS: structure, refs, acyclicity, reachability, status propagation")


if __name__ == "__main__":
    main()
