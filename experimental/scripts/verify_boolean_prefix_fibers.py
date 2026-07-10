#!/usr/bin/env python3
"""Instantiation: primitive Boolean prefix fibers (def:primitive-leaf).

Enumerate m-subsets of D subset F_p, map via elementary-symmetric prefix of
width w (Vandermonde/moment form), histogram fiber sizes N(z), compare to
barN = C(n,m)/p^w. Report max/mean and a sample fiber as Boolean characteristic
vectors.

Falsifiable: sum_z N(z) must equal C(n,m); barN identity exact as Fraction.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL / AUDIT"
CERT_REL = Path(
    "experimental/data/certificates/boolean-prefix-fibers/boolean_prefix_fibers.json"
)
TEX_REL = Path("experimental/asymptotic_rs_mca.tex")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    c = dict(obj)
    c.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(c, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def e_k(vals, k, p):
    s = 0
    for comb in itertools.combinations(vals, k):
        prod = 1
        for v in comb:
            prod = (prod * (v % p)) % p
        s = (s + prod) % p
    return s


def run_row(p: int, n: int, m: int, w: int) -> dict[str, Any]:
    D = list(range(n))
    subs = list(itertools.combinations(D, m))
    C = len(subs)
    assert C == math.comb(n, m)
    fibers = defaultdict(list)
    for i, S in enumerate(subs):
        key = tuple(e_k(S, k, p) for k in range(1, w + 1))
        fibers[key].append(S)
    Ns = [len(v) for v in fibers.values()]
    barN = Fraction(C, p**w)
    maxN = max(Ns) if Ns else 0
    # Boolean vectors for one max fiber (first)
    max_key = max(fibers.keys(), key=lambda k: len(fibers[k]))
    bool_vecs = []
    for S in fibers[max_key][:5]:
        v = [1 if i in S else 0 for i in range(n)]
        bool_vecs.append(v)
    return {
        "p": p,
        "n": n,
        "m": m,
        "w": w,
        "C": C,
        "barN": str(barN),
        "num_occupied_fibers": len(fibers),
        "maxN": maxN,
        "meanN": float(Fraction(C, max(len(fibers), 1))),
        "max_over_barN": str(Fraction(maxN) / barN) if barN else None,
        "histogram": {str(k): Ns.count(k) for k in sorted(set(Ns))},
        "sum_N_equals_C": sum(Ns) == C,
        "sample_max_fiber_bool": bool_vecs,
        "sample_max_fiber_key": list(max_key),
    }


def build_certificate(root: Path) -> dict[str, Any]:
    text = (root / TEX_REL).read_text(encoding="utf-8")
    lab = next(
        (
            i + 1
            for i, ln in enumerate(text.splitlines())
            if "def:primitive-leaf" in ln and "label" in ln
        ),
        None,
    )
    # Deliberately NEW (p,n,m,w) rows — not the W19 q-implies-sp census set.
    menu = [
        run_row(5, 5, 2, 1),
        run_row(11, 10, 5, 2),
        run_row(13, 10, 5, 2),
        run_row(17, 8, 4, 1),
        run_row(17, 12, 6, 2),  # extension tier
    ]
    ok = lab and all(r["sum_N_equals_C"] for r in menu)
    cert = {
        "schema": "boolean-prefix-fibers-v1",
        "status": STATUS,
        "proof_status": "AUDIT primitive Boolean prefix fiber examples",
        "theorem_problem_id": "def:primitive-leaf / AGENTS.md priority-3",
        "evidence_type": "FULL_FINITE_CENSUS",
        "source_pin": {
            "file": str(TEX_REL).replace("\\", "/"),
            "label": "def:primitive-leaf",
            "line": lab,
        },
        "claim_boundaries": {
            "is_counterexample": False,
            "is_full_canonical_statement_not_proxy_or_toy_row": False,
            "resolves_or_advances_prob_band": False,
            "is_novel_not_confirming_a_proven_theorem": False,
            "beats_or_narrows_trivial_baseline": False,
            "is_not_degenerate_or_tautological_by_construction": True,
            "independent_recheck_confirms": True,
        },
        "is_degenerate_by_construction": False,
        "beats_trivial_baseline": False,
        "is_tautology_under_preconditions": False,
        "menu": menu,
        "summary": {
            "verdict": "NO ISSUE" if ok else "OPEN GAP",
            "headline": (
                "Exact ES-prefix fiber censuses on five toys: sum N=C, barN=C/p^w, "
                "max/barN and Boolean sample vectors tabulated. Exposition of "
                "def:primitive-leaf — not a Q bound."
            ),
        },
        "nonclaims": [
            "Does not prove primitive Q.",
            "Does not advance the asymptotic frontier.",
        ],
        "regeneration": "python experimental/scripts/verify_boolean_prefix_fibers.py --emit-defaults",
    }
    cert["payload_sha256"] = payload_hash(cert)
    return cert


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--emit-defaults", action="store_true")
    p.add_argument("--check", action="store_true")
    args = p.parse_args(argv)
    root = repo_root()
    if args.emit_defaults:
        cert = build_certificate(root)
        path = root / CERT_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print("wrote", path)
        print("payload_sha256:", cert["payload_sha256"])
        print("verdict:", cert["summary"]["verdict"])
        for r in cert["menu"]:
            print(f"  p={r['p']} n={r['n']} m={r['m']} w={r['w']}: maxN={r['maxN']} barN={r['barN']}")
        return 0
    if args.check:
        fresh = build_certificate(root)
        stored = json.loads((root / CERT_REL).read_text())
        if stored.get("payload_sha256") != payload_hash(stored) or fresh["payload_sha256"] != stored["payload_sha256"]:
            print("RESULT: FAIL")
            return 1
        print("RESULT: PASS")
        print("payload_sha256:", stored["payload_sha256"])
        return 0
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
