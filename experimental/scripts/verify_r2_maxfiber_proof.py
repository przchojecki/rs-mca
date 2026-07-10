#!/usr/bin/env python3
"""W52-M1: R=2 max-fiber control — proved special cases + honest REDUCED core.

PROVED-SPECIAL (line-checkable):
  Lemma R2-fixed-m: For the R=2 power-sum map Phi=(sum, sumsq) on m-subsets of
  a size-N ground set, every fiber satisfies f_s <= N^{m-2} (m>=2; for m=2,
  f_s <= 1). Proof by induction fixing one element. Consequently, for fixed m
  (or m = o(N/log N)) and barN >= 1,
    log(max_f / barN)/N <= (m-2) log N / N -> 0,
  so the reduced C9 input holds without any energy hypothesis on this subclass.

  Lemma R2-m2: For m=2, R>=2, each fiber has size <= 1 (pair determined by
  sum and product from sumsq).

  Lemma R2-m3: For m=3, R=2, char != 2, f_s <= N (for each a, at most one
  complementary pair {b,c}).

REDUCED (open prize core): when m = Theta(N) (fixed density), R=2, deep charts
  (R sqrt(p) not o(N)), prove low-energy fibers still satisfy f_s <= exp(o(N)) barN.
  The polynomial bound N^{m-2} is useless for m~N/2.

generator route: inductive combinatorial bound; exact fiber-size certificates on toys.
checker route: independent fiber enumeration vs N^{m-2}; phase0 cube3.

Status: EXPERIMENTAL.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL"
CERT = Path(
    "experimental/data/certificates/r2-maxfiber-proof/r2_maxfiber_proof.json"
)
IMAGE_SCALE = Path(
    "experimental/data/certificates/image-scale-mi-ma/image_scale_mi_ma.json"
)
BASE_SHA = "e190193cebced1d3752d068a1c24136bc69a85d9"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import w49_sidon_model as m  # noqa: E402


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    c = dict(obj)
    c.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(c, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def phase0_cube3(root: Path) -> dict[str, Any]:
    A = list(itertools.product([0, 1], repeat=3))
    e1 = m.energy_diff_counter(A)
    e2 = m.energy_four_tuple(A)
    cert_E = None
    if (root / IMAGE_SCALE).is_file():
        cert = json.loads((root / IMAGE_SCALE).read_text(encoding="utf-8"))
        row = next(r for r in cert["rows"] if r.get("kind") == "sidon_energy_cube3")
        cert_E = row["gen"]["energy"]
    ok = e1 == 216 and e2 == 216 and cert_E == 216
    return {
        "energy_diff": e1,
        "energy_4tuple": e2,
        "cert_energy": cert_E,
        "pass": ok,
        "paste": "image_scale_mi_ma sidon_energy_cube3 energy=216 Delta=27/64",
    }


PROOF_R2_FIXED_M = r"""
Lemma (R=2 fiber size for any m >= 2).
Let T be a ground set of size N, Omega the m-subsets of T, and
Phi(S) = (sum_{t in S} t, sum_{t in S} t^2) with values in an ambient field
(or Z). For every target s, the fiber F_s = { S in Omega : Phi(S)=s } satisfies
  |F_s| <= N^{m-2}    for m >= 2,
with the convention N^{0} = 1, and in fact |F_s| <= 1 when m = 2.

Proof. Proceed by induction on m.
Base m=2: S={a,b}, a+b=A, a^2+b^2=Q. Then 2ab = A^2-Q, so {a,b} is the
unordered root pair of X^2 - A X + (A^2-Q)/2 = 0 (char != 2), or by direct
check at most one unordered pair in T has a given (A,Q). Thus |F_s| <= 1 = N^0.

Inductive step: fix m >= 3 and assume the claim for m-1. For each a in T, let
F_s(a) be the (m-1)-subsets U of T\{a} with sum(U)=A-a and sumsq(U)=Q-a^2
(when s=(A,Q)). By induction |F_s(a)| <= (N-1)^{m-3} <= N^{m-3}. Every
m-subset containing a that lies in F_s arises uniquely this way, and every
member of F_s contains some a, so
  |F_s| <= sum_{a in T} |F_s(a)| <= N * N^{m-3} = N^{m-2}.

Corollary (fixed-m reduced input). If m is fixed (independent of N) and
barN >= 1, then max_s f_s <= N^{m-2}, hence
  log(max_s f_s / barN) / N <= (m-2) log N / N -> 0 as N -> infinity.
Thus the reduced C9 / low-energy max-fiber input holds for R=2 at fixed m
even without an energy hypothesis (the energy restriction only shrinks F_s).

What stays open: m = Theta(N) (fixed positive density), where N^{m-2} is
super-exponential and does not give exp(o(N)) control.
"""

PROOF_R2_M3 = r"""
Lemma (R=2, m=3). Under char != 2, |F_s| <= N.
Proof (specialization of the induction). For each a in T there is at most one
unordered pair {b,c} subset T\{a} with b+c=A-a and b^2+c^2=Q-a^2, because that
pair is determined by sum and product. Summing over a and dividing by the triple
counting multiplicity (each triple counted 3 times) still yields |F_s| <= N.
"""

REDUCED = r"""
REDUCED open core (density regime):
For m = floor(alpha N) with fixed alpha in (0,1), R=2, deep rows
(R sqrt(p) not o(N)), prove that every fiber F_s of Phi=(sum,sumsq) that is
low-energy (Delta_s <= exp(-sigma N)) satisfies |F_s| <= exp(o(N)) barN.
The fixed-m polynomial bound is insufficient; need additive structure of large
Boolean families of constant-weight vectors with two power-sum constraints, or
a Fourier/Weil bound on the number of m-subsets with given (e1,e2) that form a
Sidon-like set.
"""


def max_fiber_R2(p: int, N: int, m_sz: int) -> dict[str, Any]:
    T = list(range(1, N + 1))
    Omega = m.all_m_subsets(T, m_sz)
    fibers = m.build_fibers(Omega, R=2, p=p)
    max_f = max(len(v) for v in fibers.values()) if fibers else 0
    bound = 1 if m_sz == 2 else N ** (m_sz - 2)
    return {
        "p": p,
        "N": N,
        "m": m_sz,
        "R": 2,
        "M": len(Omega),
        "L": len(fibers),
        "max_f": max_f,
        "bound_N_pow_m_minus_2": bound,
        "bound_holds": max_f <= bound,
    }


def build_certificate(root: Path) -> dict[str, Any]:
    phase0 = phase0_cube3(root)
    # toys: fixed small m, R=2
    toys = []
    for p, N, m_sz in (
        (17, 8, 2),
        (17, 8, 3),
        (17, 8, 4),
        (19, 10, 2),
        (19, 10, 3),
        (19, 10, 4),
        (23, 12, 2),
        (23, 12, 3),
        (23, 12, 4),
        (31, 12, 3),
        (31, 14, 4),
        (13, 8, 3),
        (17, 10, 5),
    ):
        if p <= N or math.comb(N, m_sz) > 15000:
            continue
        toys.append(max_fiber_R2(p, N, m_sz))

    all_bound = all(t["bound_holds"] for t in toys) and len(toys) >= 8
    # density-regime note: m ~ N/2 bound is huge — not claimed as useful
    density_note = {
        "example_N": 20,
        "example_m": 10,
        "poly_bound": 20 ** 8,
        "useful_for_exp_o_N": False,
        "reason": "N^{m-2} with m=Theta(N) is not exp(o(N))",
    }

    rung = "PROVED-SPECIAL"
    # Also state REDUCED as secondary
    payload = {
        "schema": "r2_maxfiber_proof.v1",
        "object": "R=2 max-fiber control (fixed-m proved; density REDUCED)",
        "status": STATUS,
        "proof_status": rung,
        "rung": rung,
        "verdict": rung,
        "base_sha": BASE_SHA,
        "hard_input": "b / reduced C9 / R=2",
        "weave": ["W50", "W51", "#575", "#577", "C9"],
        "phase0": phase0,
        "proof_texts": {
            "R2_fixed_m": PROOF_R2_FIXED_M.strip(),
            "R2_m3": PROOF_R2_M3.strip(),
            "REDUCED_density": REDUCED.strip(),
        },
        "toys": toys,
        "n_toys": len(toys),
        "all_toys_respect_bound": all_bound,
        "density_regime_note": density_note,
        "discharged_subclass": (
            "R=2 with fixed m (or m=o(N/log N)): max fiber <= N^{m-2} => "
            "log(ratio)/N -> 0 for barN>=1"
        ),
        "open_core_reduced": REDUCED.strip(),
        "generator_route": (
            "inductive combinatorial bound f_s<=N^{m-2} for R=2; exact fiber enumeration toys"
        ),
        "checker_route": (
            "independent max-fiber count vs N^{m-2} on toys; phase0 cube3 dual energy"
        ),
        "claim_boundaries": {
            "is_counterexample": False,
            "is_theorem": True,
            "is_measurement": False,
            "theorem_scope": "R=2 fixed-m fiber size; not density regime",
        },
        "evidence_type": "FINITE_TOY_ROW",
        "falsifiable": True,
        "is_tautology_under_preconditions": False,
        "is_degenerate_by_construction": False,
        "beats_trivial_baseline": True,
        "nonclaims": [
            "Does not prove density regime m=Theta(N).",
            "N^{m-2} is useless for m~N/2.",
            "Low-energy hypothesis not needed for fixed-m bound (bound is unconditional on fibers).",
        ],
        "honest_headline": (
            f"Rung {rung}: R=2 f_s<=N^{{m-2}} (fixed m); density m=Theta(N) REDUCED open; "
            f"toys_ok={all_bound}"
        ),
        "regeneration": "py -3.13 experimental/scripts/verify_r2_maxfiber_proof.py",
        "all_pass": phase0["pass"] and all_bound,
    }
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def emit(root: Path) -> dict[str, Any]:
    cert = build_certificate(root)
    out = root / CERT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return cert


def check(root: Path) -> int:
    path = root / CERT
    if not path.is_file():
        print("RESULT: FAIL missing cert", file=sys.stderr)
        return 1
    cert = json.loads(path.read_text(encoding="utf-8"))
    rebuilt = build_certificate(root)
    ok = cert.get("payload_sha256") == rebuilt.get("payload_sha256")
    ok = ok and cert.get("phase0", {}).get("pass")
    ok = ok and cert.get("all_toys_respect_bound")
    # spot-check one toy
    if cert.get("toys"):
        t0 = cert["toys"][0]
        if t0["max_f"] > t0["bound_N_pow_m_minus_2"]:
            ok = False
    if ok:
        print("RESULT: PASS")
        print(f"payload_sha256: {cert['payload_sha256']}")
        print(f"verdict: {cert.get('verdict')}")
        print(f"phase0: {cert.get('phase0', {}).get('paste')}")
        print(f"n_toys: {cert.get('n_toys')} all_bound={cert.get('all_toys_respect_bound')}")
        return 0
    print("RESULT: FAIL", file=sys.stderr)
    return 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    root = repo_root()
    if args.emit or not args.check:
        cert = emit(root)
        print("EMITTED", root / CERT)
        print("payload_sha256:", cert["payload_sha256"])
        print("verdict:", cert["verdict"])
        if not args.check:
            return 0 if cert.get("all_pass") else 1
    if args.check:
        return check(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
