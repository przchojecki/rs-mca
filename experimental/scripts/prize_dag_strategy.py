#!/usr/bin/env python3
"""Strategic classification of the prize DAG's OPEN nodes (AUDIT).

Classes (graph-relative — a new proof strategy = new edges = recompute):
  CRITICAL       on EVERY currently-mapped route to the prize
  ROUTE-CHOICE   an alternative under an open any-gate: one sibling per
                 group suffices; the others become prize-discardable the
                 moment one closes
  ROUTE-INTERNAL a prerequisite reachable to the root ONLY through some
                 non-critical alternative: needed iff that route is chosen
  SUPPORT-ONLY   contributes via evidence/refute edges alone: de-risks and
                 informs route choice, but formally satisfies no gate

Run:  python3 experimental/scripts/prize_dag_strategy.py
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DAG = os.path.join(REPO, "experimental", "data", "prize-dag", "prize_dag.json")
SAT = {"PROVED", "PROVABLE", "CONDITIONAL"}


def main() -> None:
    data = json.load(open(DAG))
    nodes = {n["id"]: n for n in data["nodes"]}
    root = data["root"]
    inc: dict[str, list[tuple[str, str]]] = {i: [] for i in nodes}
    out_proof: dict[str, list[str]] = {i: [] for i in nodes}   # req/alt edges only
    for e in data["edges"]:
        inc[e["to"]].append((e["from"], e["kind"]))
        if e["kind"] in ("req", "alt"):
            out_proof[e["from"]].append(e["to"])

    open_ids = [i for i, n in nodes.items()
                if n["status"] not in SAT and n["status"] != "REFUTED"]

    def satisfiable(granted: frozenset) -> bool:
        memo: dict[str, bool] = {}
        def sat(v: str) -> bool:
            if v in memo:
                return memo[v]
            memo[v] = False
            n = nodes[v]
            if n["status"] == "REFUTED":
                return False
            reqs = [f for f, k in inc[v] if k == "req"]
            alts = [f for f, k in inc[v] if k == "alt"]
            req_ok = all(sat(f) for f in reqs)
            alt_ok = (not (n.get("gate", "all") == "any" and alts)) or any(sat(f) for f in alts)
            base = n["status"] in SAT or v in granted
            memo[v] = req_ok and alt_ok and (base if n["status"] not in SAT else True)
            return memo[v]
        return sat(root)

    all_open = frozenset(open_ids)
    assert satisfiable(all_open), "root unsatisfiable even with all grants"
    critical = {x for x in open_ids
                if not satisfiable(frozenset(i for i in open_ids if i != x))}

    # proof-path reachability (req/alt edges only)
    on_proof_path = set()
    for x in nodes:
        stack, seen = [x], {x}
        while stack:
            v = stack.pop()
            if v == root:
                on_proof_path.add(x)
                break
            for w in out_proof[v]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)

    # alternative groups: open any-gates and their live alt siblings.
    # "available" = DEEPLY satisfiable with NO grants (hypothesis edges honored)
    def available(v: str, memo=None) -> bool:
        if memo is None:
            memo = {}
        if v in memo:
            return memo[v]
        memo[v] = False
        n = nodes[v]
        if n["status"] == "REFUTED" or n["status"] not in SAT:
            memo[v] = False if n["status"] not in SAT else memo[v]
        reqs = [f for f, k in inc[v] if k == "req"]
        alts = [f for f, k in inc[v] if k == "alt"]
        req_ok = all(available(f, memo) for f in reqs)
        alt_ok = (not (n.get("gate", "all") == "any" and alts)) or any(available(f, memo) for f in alts)
        memo[v] = n["status"] in SAT and req_ok and alt_ok
        return memo[v]
    groups = []
    for i, n in nodes.items():
        alts = [f for f, k in inc[i] if k == "alt"]
        if n.get("gate", "all") == "any" and alts:
            live = [a for a in alts if nodes[a]["status"] != "REFUTED"]
            sat_alts = [a for a in live if available(a)]
            groups.append((i, live, sat_alts))

    support_only = [x for x in open_ids if x not in on_proof_path]
    route_nodes = [x for x in open_ids if x in on_proof_path and x not in critical]

    print(f"open nodes: {len(open_ids)} | critical: {len(critical)} | "
          f"route (choice/internal): {len(route_nodes)} | support-only: {len(support_only)}")
    print("\n== CRITICAL (essential unless a new strategy adds routes) ==")
    for x in sorted(critical):
        print(f"  {x} [{nodes[x]['status']}]")
    print("\n== ALTERNATIVE GROUPS (work the cheapest; siblings discard when one closes) ==")
    for gate, live, sat_alts in sorted(groups):
        state = "ALREADY PASSABLE" if sat_alts or nodes[gate]["status"] in SAT else "open"
        print(f"  gate {gate} ({state}): " + " | ".join(
            f"{a}[{nodes[a]['status']}]" for a in live))
    print("\n== ROUTE-CHOICE / ROUTE-INTERNAL (needed only on their route) ==")
    for x in sorted(route_nodes):
        print(f"  {x} [{nodes[x]['status']}]")
    print("\n== SUPPORT-ONLY (de-risk / inform; formally satisfy nothing) ==")
    for x in sorted(support_only):
        print(f"  {x} [{nodes[x]['status']}]")


if __name__ == "__main__":
    main()
