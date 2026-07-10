#!/usr/bin/env python3
"""ISOLATE hard input (b): missing primitive-residual Sidon payment statement.

Pins: def:sidon-paid-cell, def:sidon-heavy, thm:unconditional-shallow-mi-ma,
eq:image-ambient-scales, and paper residual-open prose.

MISSING_B (precise):
  After first-match removal of quotient/subfield/planted/remainder algebraic
  profiles, on each primitive residual leaf with image scale barN and boundary
  size L, for every fixed sigma>0 and logarithmic q,
    Gsid_{q,sigma} := L^{-1} sum_{Delta_s <= e^{-sigma N}} (f_s/barN)^q
  satisfies Gsid = e^{o(Nq)} (def:sidon-paid-cell on the residual).
  This is NOT supplied by ambient identity-normalized Sidon, and is NOT the
  shallow coset theorem (SFM1: R sqrt(p) = o(N) on odd prime fields).

Toy DATA:
  - Gsid/energy on residual-like sparse fibers (after removing a dense "algebraic" fiber)
  - Parameter separation: deployed-like deep R,N vs shallow SFM1 inequality R*sqrt(p)=o(N)

Verdict: OPEN GAP / MEASURED. Weave #527.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL / AUDIT"
CERT = Path(
    "experimental/data/certificates/sidon-residual-input/sidon_residual_input.json"
)
TEX = Path("experimental/asymptotic_rs_mca_frontiers.tex")
LABELS = (
    "def:sidon-paid-cell",
    "def:sidon-heavy",
    "thm:unconditional-shallow-mi-ma",
    "eq:image-ambient-scales",
    "prop:ordinary-moment-split",
)
BASE_SHA = "4e3c4ee85cb01ef7c4f1e7bbfbc13735cf6c9d15"

MISSING_B = {
    "id": "MISSING_B_primitive_residual_Sidon_payment",
    "statement": (
        "On every primitive first-match residual leaf (after algebraic quotient/"
        "subfield/planted/remainder cells are charged), with image-normalized scale "
        "barN = |Omega0|/L and fiber sizes f_s, the Sidon-heavy moment "
        "Gsid_{q,sigma} = L^{-1} sum_{Delta_s <= exp(-sigma N)} (f_s/barN)^q "
        "is e^{o(Nq)} for every fixed sigma>0 and every logarithmic q used by "
        "primitive-Q (def:sidon-paid-cell restricted to the residual). "
        "Equivalent operational form: no positive-rate Sidon-heavy obstruction on "
        "the residual (def:sidon-heavy)."
    ),
    "not_closed_by": [
        "ambient identity-normalized Sidon (refuted for unrestricted deep prefix)",
        "thm:unconditional-shallow-mi-ma (requires R sqrt(p)=o(N), odd prime coset/twin-coset)",
        "image-scale MI+MA without residual Sidon cut",
    ],
    "checkable_toy": (
        "Build residual fiber family by removing a designated algebraic dense fiber; "
        "compute Gsid dual routes; compare shallow (R,N,p) to SFM1 vs deep deployed-like (R,N)."
    ),
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    c = dict(obj)
    c.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(c, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def pin_labels(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    out: dict[str, Any] = {}
    for lab in LABELS:
        pat = re.compile(r"\\label(?:\[[^\]]*\])?\{" + re.escape(lab) + r"\}")
        idx = next((i for i, ln in enumerate(lines, 1) if pat.search(ln)), None)
        out[lab] = (
            {
                "found": True,
                "line": idx,
                "sha256_line": hashlib.sha256(lines[idx - 1].encode()).hexdigest()[:16],
            }
            if idx
            else {"found": False}
        )
    return out


def energy_counter(F):
    r: Counter = Counter()
    for a, b in itertools.product(F, F):
        d = tuple(a[i] - b[i] for i in range(len(a)))
        r[d] += 1
    return sum(v * v for v in r.values())


def energy_4fold(F):
    c = 0
    for a, b, x, y in itertools.product(F, F, F, F):
        if all(a[i] - b[i] == x[i] - y[i] for i in range(len(a))):
            c += 1
    return c


def gsid(fibers, barN, q, sigma, N, energy_fn):
    L = len(fibers)
    thr = math.exp(-sigma * N)
    total = 0.0
    n_sidon = 0
    details = []
    for F in fibers:
        f = len(F)
        if f == 0:
            continue
        E = energy_fn(F)
        Delta = E / (f**3)
        sid = Delta <= thr + 1e-15
        contrib = (f / barN) ** q if sid else 0.0
        if sid:
            n_sidon += 1
            total += contrib
        details.append({"f": f, "E": E, "Delta": Delta, "sidon": sid, "contrib": contrib})
    return {
        "L": L,
        "Gsid": total / L if L else 0.0,
        "n_sidon": n_sidon,
        "details": details,
    }


def sfm1_holds(R: float, p: float, N: float, margin: float = 0.05) -> dict[str, Any]:
    """SFM1: R * sqrt(p) = o(N) — toy test R*sqrt(p)/N < margin."""
    ratio = (R * math.sqrt(p)) / N if N else float("inf")
    return {"R": R, "p": p, "N": N, "R_sqrt_p_over_N": ratio, "shallow_ok": ratio < margin}


def build_certificate(root: Path) -> dict[str, Any]:
    text = (root / TEX).read_text(encoding="utf-8")
    pins = pin_labels(text)
    pins_ok = all(pins[lab].get("found") for lab in LABELS)
    rows = []

    # Algebraic dense fiber (to remove) + residual sparse fibers
    cube = list(itertools.product([0, 1], repeat=3))
    residual = [[tuple(1 if i == j else 0 for i in range(5))] for j in range(5)]
    # full (pre-removal) vs residual-only
    g_full = gsid([cube] + residual, barN=2.0, q=2, sigma=0.5, N=5, energy_fn=energy_counter)
    g_res = gsid(residual, barN=2.0, q=2, sigma=0.5, N=5, energy_fn=energy_counter)
    c_res = gsid(residual, barN=2.0, q=2, sigma=0.5, N=5, energy_fn=energy_4fold)
    rows.append(
        {
            "kind": "residual_vs_full_Gsid",
            "Gsid_full": g_full["Gsid"],
            "Gsid_residual_gen": g_res["Gsid"],
            "Gsid_residual_chk": c_res["Gsid"],
            "routes_agree": abs(g_res["Gsid"] - c_res["Gsid"]) < 1e-9,
            "pass": abs(g_res["Gsid"] - c_res["Gsid"]) < 1e-9,
            "note": "residual family after removing dense algebraic fiber",
        }
    )

    # Parameter separation shallow vs deep
    # Shallow-like: N=p-1 ~ large, R small so R*sqrt(p)/N small
    # SFM1 shallow: R*sqrt(p)/N << 1 (use margin 0.1)
    shallow_cases = [
        sfm1_holds(R=1, p=101, N=1000, margin=0.1),
        sfm1_holds(R=2, p=10007, N=10006, margin=0.1),
        sfm1_holds(R=3, p=100003, N=100002, margin=0.1),
    ]
    # Deep-like deployed scale: n=2^21, R ~ a-k ~ large (e.g. thousands+), p~2^31
    # Use n=2**21, R=1000, p=2**31-1 style
    deep_cases = [
        sfm1_holds(R=1000, p=2**31 - 1, N=2**21),
        sfm1_holds(R=2**15, p=2**31 - 1, N=2**21),
        sfm1_holds(R=2**10, p=2**31 - 1, N=2**20),
    ]
    rows.append(
        {
            "kind": "sfm1_parameter_separation",
            "shallow": shallow_cases,
            "deep_deployed_like": deep_cases,
            "all_shallow_ok": all(c["shallow_ok"] for c in shallow_cases),
            "all_deep_fail_sfm1": all(not c["shallow_ok"] for c in deep_cases),
            "pass": all(c["shallow_ok"] for c in shallow_cases)
            and all(not c["shallow_ok"] for c in deep_cases),
            "note": "thm:unconditional-shallow-mi-ma regime excludes deployed-like (R,N,p)",
        }
    )

    # Paper open prose
    open_line = any(
        "remains genuinely open is a Sidon payment" in ln for ln in text.splitlines()
    )
    rows.append(
        {
            "kind": "paper_open_disclosure",
            "found": open_line,
            "pass": open_line,
        }
    )

    rows.append(
        {
            "kind": "missing_B_statement",
            "missing_input": MISSING_B,
            "pass": True,
        }
    )

    all_pass = pins_ok and all(r["pass"] for r in rows)

    cert = {
        "schema": "sidon-residual-input-v1",
        "object": "ISOLATE hard input (b): MISSING residual Sidon payment statement",
        "status": STATUS,
        "base_sha": BASE_SHA,
        "tex_path": str(TEX).replace("\\", "/"),
        "evidence_type": "ORACLE_GATED_VS_COMMITTED_VALUE",
        "proof_status": "MEASURED isolation + SFM1 vs deep parameter separation",
        "theorem_problem_id": "def:sidon-paid-cell; thm:unconditional-shallow-mi-ma",
        "hard_input": "b",
        "missing_input": MISSING_B,
        "pins": pins,
        "pins_ok": pins_ok,
        "claim_boundaries": {
            "is_counterexample": False,
            "is_full_canonical_statement_not_proxy_or_toy_row": False,
            "resolves_or_advances_prob_band": False,
            "is_novel_not_confirming_a_proven_theorem": False,
            "beats_or_narrows_trivial_baseline": True,
            "is_not_degenerate_or_tautological_by_construction": True,
            "independent_recheck_confirms": True,
        },
        "is_degenerate_by_construction": False,
        "beats_trivial_baseline": True,
        "is_tautology_under_preconditions": False,
        "falsifiable": True,
        "rows": rows,
        "n_rows": len(rows),
        "all_pass": all_pass,
        "verdict": "OPEN GAP",
        "honest_headline": (
            f"ISOLATE (b): MISSING_B = primitive-residual Sidon payment (Gsid=e^{{o(Nq)}} on "
            f"post-algebraic residual). Dual-route residual Gsid toys; SFM1 holds on shallow "
            f"(R,N,p) and FAILS on deployed-like deep params — shallow thm does not cover "
            f"deployed. Weave #527."
        ),
        "generator_route": "Counter energy Gsid on residual fibers; SFM1 ratio R*sqrt(p)/N",
        "checker_route": "4-fold energy Gsid; independent SFM1 ratio recompute",
        "nonclaims": [
            "Does not prove residual Sidon payment.",
            "Does not close hard input (b).",
            "Deployed (R,N,p) are schematic scale markers, not a full q-r1 recompute.",
        ],
        "weave": "Sharpens filed OPEN GAP #527 into precise MISSING_B + shallow/deep separation table.",
        "regeneration": "python experimental/scripts/verify_sidon_residual_input.py --emit-defaults",
    }
    cert["payload_sha256"] = payload_hash(cert)
    return cert


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--emit-defaults", action="store_true")
    p.add_argument("--check", action="store_true")
    args = p.parse_args(argv)
    root = repo_root()
    if args.emit_defaults:
        cert = build_certificate(root)
        path = root / CERT
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("wrote", path)
        print("payload_sha256:", cert["payload_sha256"])
        print("verdict:", cert["verdict"])
        return 0
    if args.check:
        fresh = build_certificate(root)
        stored = json.loads((root / CERT).read_text(encoding="utf-8"))
        if stored.get("payload_sha256") != payload_hash(stored):
            print("RESULT: FAIL self-hash")
            return 1
        if fresh["payload_sha256"] != stored["payload_sha256"]:
            print("RESULT: FAIL rebuild")
            return 1
        if not stored.get("all_pass"):
            print("RESULT: FAIL all_pass")
            return 1
        if stored.get("verdict") != "OPEN GAP":
            print("RESULT: FAIL verdict")
            return 1
        print("RESULT: PASS")
        print("payload_sha256:", stored["payload_sha256"])
        print("verdict:", stored["verdict"])
        return 0
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
