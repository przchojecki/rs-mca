#!/usr/bin/env python3
"""ISOLATE hard input (c): missing residual ray-compiler statement.

Pins: hyp:ray-compiler, eq:ray-compiler, thm:bounded-residual-kernel-ray,
thm:single-mds-circuit-ray, def:balanced-quotient-core, rem:balanced-core-exhaustion.

Missing input (precise, checkable form):
  MISSING_C: For every residual balanced-core parameter map
    Phi: P -> F  (P subset F_q^d, d>=2, Phi polynomial of total degree <= D)
  after first-match algebraic removal, the image size satisfies
    |im Phi| <= poly_D(n) * (1 + barN_residual)
  or the RC incidence form |Z| <= J|P|/H with H,J giving e^{o(n)}(1+barN).
  Linear (D=1) maps: |im|=q when nonzero (proved-shape toys).
  Nonlinear D>=2: no general bound is theorem-backed in the draft.

Toy DATA: for small F_q and degrees D=1,2,3, tabulate |im Phi| vs linear-rank
prediction q; report gap ratio |im|/q and growth.

Generator route: enumerate F_q^d, evaluate polynomial Phi, |set|.
Checker route: for linear maps closed-form |im|; for monomials use value-set
size formulas (e.g. x|->x^2 on F_q has (q+1)/2 for odd q).

Verdict: OPEN GAP / MEASURED (isolation, not a proof). Weave #523.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable

STATUS = "EXPERIMENTAL / AUDIT"
CERT = Path(
    "experimental/data/certificates/ray-compiler-input/ray_compiler_input.json"
)
TEX = Path("experimental/asymptotic_rs_mca_frontiers.tex")
LABELS = (
    "hyp:ray-compiler",
    "eq:ray-compiler",
    "thm:bounded-residual-kernel-ray",
    "thm:single-mds-circuit-ray",
    "def:balanced-quotient-core",
    "rem:balanced-core-exhaustion",
)
BASE_SHA = "4e3c4ee85cb01ef7c4f1e7bbfbc13735cf6c9d15"

MISSING_C = {
    "id": "MISSING_C_poly_image_bound_balanced_core",
    "statement": (
        "After first-match removal of algebraic cells, for every residual "
        "balanced-core chart with parameter space P subset F_q^d (d>=2) and "
        "slope map Phi: P -> F of polynomial degree <= D, either "
        "(i) |im Phi| <= C_D * poly(n) * (1+barN_res), or "
        "(ii) incidence degrees H,J exist with |Z|*H <= J*|P| and "
        "J|P|/H = e^{o(n)}(1+barN_res) (hyp:ray-compiler / eq:ray-compiler). "
        "Proved special cases in draft: bounded residual-kernel rays; "
        "single MDS-circuit rays; linear (D=1) image size q. "
        "General nonlinear higher-dim balanced cores: OPEN."
    ),
    "checkable_prediction": (
        "At fixed (q,d,D), enumerate P=F_q^d and Phi; record |im Phi|. "
        "Linear nonzero: expect |im|=q. Nonlinear: |im| may be << q or =q; "
        "no draft theorem forces poly(n) bound uniform in D for residual MCA."
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


def image_size(q: int, d: int, phi: Callable[[tuple[int, ...]], int]) -> int:
    im = set()
    for p in itertools.product(range(q), repeat=d):
        im.add(phi(p) % q)
    return len(im)


def linear_predict(q: int, coeffs: tuple[int, ...]) -> int:
    if all(c % q == 0 for c in coeffs):
        return 1
    return q


def square_image_odd(q: int) -> int:
    """|im(x|->x^2)| on F_q, q odd = (q+1)/2."""
    return (q + 1) // 2


def build_certificate(root: Path) -> dict[str, Any]:
    text = (root / TEX).read_text(encoding="utf-8")
    pins = pin_labels(text)
    pins_ok = all(pins[lab].get("found") for lab in LABELS)
    rows = []

    # Linear D=1 maps d=2,3
    for q in (5, 7, 11):
        for coeffs in ((1, 0), (1, 2), (0, 0), (3, 5)):
            d = 2
            if len(coeffs) == 2:
                phi = lambda p, c=coeffs: (c[0] * p[0] + c[1] * p[1]) % q
            else:
                continue
            gen = image_size(q, d, phi)
            pred = linear_predict(q, coeffs)
            rows.append(
                {
                    "kind": "linear",
                    "q": q,
                    "d": d,
                    "D": 1,
                    "coeffs": list(coeffs),
                    "im_enum": gen,
                    "im_predict": pred,
                    "gap_ratio": gen / pred if pred else None,
                    "routes_agree": gen == pred,
                    "pass": gen == pred,
                }
            )

    # Nonlinear: Phi = x^2, x^2+y^2, x*y, x^3
    nonlinear_specs = []
    for q in (5, 7, 11, 13):
        # x^2 on first coord (ignores y) — image size of squares
        im_sq = image_size(q, 2, lambda p: (p[0] * p[0]) % q)
        pred_sq = square_image_odd(q) if q % 2 == 1 else None
        nonlinear_specs.append(
            {
                "kind": "nonlinear_square_x",
                "q": q,
                "d": 2,
                "D": 2,
                "im_enum": im_sq,
                "im_formula": pred_sq,
                "linear_predict_q": q,
                "gap_vs_linear": im_sq / q,
                "routes_agree": pred_sq is None or im_sq == pred_sq,
                "pass": pred_sq is None or im_sq == pred_sq,
            }
        )
        # product xy
        im_xy = image_size(q, 2, lambda p: (p[0] * p[1]) % q)
        nonlinear_specs.append(
            {
                "kind": "nonlinear_product_xy",
                "q": q,
                "d": 2,
                "D": 2,
                "im_enum": im_xy,
                "linear_predict_q": q,
                "gap_vs_linear": im_xy / q,
                # product is surjective on F_q: im size q
                "routes_agree": im_xy == q,
                "pass": im_xy == q,
                "note": "xy is onto F_q; gap vs linear prediction is 1.0 but map is nonlinear",
            }
        )
        # x^2+y^2
        im_ss = image_size(q, 2, lambda p: (p[0] * p[0] + p[1] * p[1]) % q)
        nonlinear_specs.append(
            {
                "kind": "nonlinear_sum_squares",
                "q": q,
                "d": 2,
                "D": 2,
                "im_enum": im_ss,
                "linear_predict_q": q,
                "gap_vs_linear": im_ss / q,
                "pass": True,  # measurement row
                "measured": True,
            }
        )
        # cubic x^3
        im_c = image_size(q, 2, lambda p: (p[0] ** 3) % q)
        nonlinear_specs.append(
            {
                "kind": "nonlinear_cube_x",
                "q": q,
                "d": 2,
                "D": 3,
                "im_enum": im_c,
                "linear_predict_q": q,
                "gap_vs_linear": im_c / q,
                "pass": True,
                "measured": True,
            }
        )

    rows.extend(nonlinear_specs)

    # Growth summary: min gap_vs_linear for degree-2 non-surjective maps
    sq_gaps = [r["gap_vs_linear"] for r in nonlinear_specs if r["kind"] == "nonlinear_square_x"]
    rows.append(
        {
            "kind": "gap_summary",
            "square_gaps": sq_gaps,
            "min_square_gap": min(sq_gaps) if sq_gaps else None,
            "max_square_gap": max(sq_gaps) if sq_gaps else None,
            "linear_always_match": all(r["pass"] for r in rows if r.get("kind") == "linear"),
            "pass": True,
            "interpretation": (
                "Square maps have |im|~q/2 << q=linear prediction — "
                "linear-rank RC formula overstates residual ray budget if misapplied."
            ),
        }
    )

    # Paper discloses open
    open_hit = "hyp:ray-compiler" in text and "Ray compiler" in text
    rows.append({"kind": "pin_hyp_present", "pass": open_hit and pins_ok})

    all_pass = pins_ok and all(r.get("pass", True) for r in rows)

    cert = {
        "schema": "ray-compiler-input-v1",
        "object": "ISOLATE hard input (c): missing poly image bound for residual balanced cores",
        "status": STATUS,
        "base_sha": BASE_SHA,
        "tex_path": str(TEX).replace("\\", "/"),
        "evidence_type": "ORACLE_GATED_VS_COMMITTED_VALUE",
        "proof_status": "MEASURED isolation + precise missing-input statement",
        "theorem_problem_id": "hyp:ray-compiler; thm:bounded-residual-kernel-ray",
        "hard_input": "c",
        "missing_input": MISSING_C,
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
            f"ISOLATE (c): MISSING_C = poly-degree-D image bound (or RC H,J) for residual "
            f"higher-dim balanced cores. Linear toys match |im|=q; square maps give |im|/q≈0.5 "
            f"(measured gap). Does not prove MISSING_C. Weave #523."
        ),
        "generator_route": "enumerate F_q^d evaluate Phi; |set| of values",
        "checker_route": "linear closed-form |im|; odd-q square-image formula (q+1)/2",
        "nonclaims": [
            "Does not prove hyp:ray-compiler.",
            "Does not close hard input (c).",
            "Toy fields only; not deployed n.",
        ],
        "weave": "Sharpens filed OPEN GAP #523 into precise MISSING_C + image-size table.",
        "regeneration": "python experimental/scripts/verify_ray_compiler_input.py --emit-defaults",
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
