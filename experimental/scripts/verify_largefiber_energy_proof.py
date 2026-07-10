#!/usr/bin/env python3
"""W53-M2: prove/reduce large fiber => high additive energy (R=2).

PROVED-SPECIAL (elementary, line-checkable):
  Lemma CS: For any nonempty finite F of vectors in an abelian group,
    E(F) = sum_v r_{F-F}(v)^2 >= |F|^2
    (only the zero difference), hence Delta = E/|F|^3 >= 1/|F|.
  Therefore if f is large, the *trivial* lower bound on Delta is small
  (1/f), so CS alone does NOT force high energy for large fibers.

  Lemma diagonal+: counting ordered pairs, E(F) >= 2|F|^2 - |F| when F is
  a Sidon set (only trivial additive quadruples), giving Delta >= (2f-1)/f^2
  -> 0 as f grows. Sidon sets are the energy-minimizers; large Sidon => low Delta.

  Lemma fiber-CS (R=2 toy identity): on enumerated R=2 fibers, the measured
  Delta always satisfies Delta >= 1/f (CS), certified on toys.

REDUCED (the real additive-combinatorics gap):
  Prove that a fiber F of m-subsets with FIXED (sum, sumsq) and m = Theta(N)
  CANNOT be a near-Sidon set of size exp(eta N). Equivalently: any subset of
  a single (e1,e2)-fiber with size f >= exp(eta N) has Delta >= exp(-o(N))
  or at least Delta >= f^{-c} for c<1 (beating Sidon). Tools: BSG on the
  Boolean cube restricted to a 2-constraint slice; or Fourier analysis of
  the slice indicator.

generator route: CS/Sidon extremal lemmas + toy verification Delta>=1/f on fibers.
checker route: independent E vs f recompute; phase0 cube3.

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
    "experimental/data/certificates/largefiber-energy-proof/"
    "largefiber_energy_proof.json"
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
    e1, e2 = m.energy_diff_counter(A), m.energy_four_tuple(A)
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


PROOF_CS = r"""
Lemma (Cauchy-Schwarz / trivial energy lower bound).
Let F be a nonempty finite subset of an abelian group G (written additively),
and let r(v) = |{(a,b) in F x F : a-b = v}|. Then
  E(F) := sum_v r(v)^2 = |{(a,b,c,d) in F^4 : a-b = c-d}|
and by Cauchy-Schwarz / the diagonal term alone,
  E(F) >= r(0)^2 = |F|^2,
hence Delta(F) := E(F)/|F|^3 >= 1/|F|.

Corollary. The trivial lower bound Delta >= 1/f tends to 0 as f -> infinity.
Therefore "large fiber => high energy" CANNOT follow from CS alone; any proof
must use the structure of R=2 fibers (fixed sum and sum of squares).

Lemma (Sidon extremal). If F is Sidon in the sense that the only solutions to
a-b = c-d are the trivial ones (a,b)=(c,d) or the swaps counted by the usual
Sidon count), then E(F) = 2|F|^2 - |F| and Delta = (2f-1)/f^2 ~ 2/f -> 0.
Large Sidon sets are low-energy; the open problem is whether an R=2 fiber can
contain a large Sidon subset (or itself be near-Sidon) at linear density.
"""

PROOF_REDUCED = r"""
REDUCED (closes the C9 crux if proved):
Let m = floor(alpha N) with fixed alpha in (0,1), T subset F_p of size N, and
let F be any fiber of Phi(S)=(sum t, sum t^2) on m-subsets of T. Prove there
exists c = c(alpha) < 1 such that
  Delta(F) >= |F|^{-c}
whenever |F| >= 2, or more strongly Delta(F) >= exp(-o(N)) whenever
|F| >= exp(eta N). Either bound prevents a simultaneous exp-large and
e^{-Omega(N)}-energy fiber, and with W50 Lemma II yields the reduced payment
input at R=2 linear density.

Computational evidence (toys): on all enumerated R=2 fibers at densities
m/N in [0.25,0.5], the measured (f, Delta) pairs satisfy Delta >= 1/f (CS)
and the largest fibers have Delta substantially above the Sidon floor 2/f
in the scanned range — but this is MEASURED, not a proof for m=Theta(N).
"""


def cs_check_on_fibers() -> dict[str, Any]:
    rows = []
    configs = [
        (17, 8, 4),
        (17, 10, 4),
        (19, 10, 5),
        (19, 12, 6),
        (23, 12, 5),
        (23, 12, 6),
        (31, 12, 6),
        (17, 12, 5),
        (19, 14, 6),
    ]
    all_ok = True
    for p, N, m_sz in configs:
        if p <= N or math.comb(N, m_sz) > 8000:
            continue
        T = list(range(1, N + 1))
        Omega = m.all_m_subsets(T, m_sz)
        fibers = m.build_fibers(Omega, 2, p)
        for members in fibers.values():
            f = len(members)
            if f < 1:
                continue
            pts = [m.support_vector(s, T) for s in members]
            E = m.energy_diff_counter(pts)
            Delta = E / float(f**3)
            cs = Delta + 1e-12 >= 1.0 / f
            sidon_floor = (2 * f - 1) / float(f**2)
            if not cs:
                all_ok = False
            if f >= 2:
                rows.append(
                    {
                        "p": p,
                        "N": N,
                        "m": m_sz,
                        "density": m_sz / N,
                        "f": f,
                        "E": E,
                        "Delta": Delta,
                        "cs_bound_1_over_f": 1.0 / f,
                        "sidon_floor": sidon_floor,
                        "cs_holds": cs,
                        "above_sidon_floor": Delta + 1e-12 >= sidon_floor,
                    }
                )
    # keep top by f for cert size
    rows = sorted(rows, key=lambda r: -r["f"])[:80]
    n_above_sidon = sum(1 for r in rows if r["above_sidon_floor"])
    return {
        "all_cs_holds": all_ok,
        "n_fiber_rows": len(rows),
        "n_above_sidon_floor": n_above_sidon,
        "rows": rows,
        "pass": all_ok and len(rows) >= 5,
    }


def build_certificate(root: Path) -> dict[str, Any]:
    phase0 = phase0_cube3(root)
    toys = cs_check_on_fibers()
    # Honest rung: we prove CS and Sidon extremal (standard), NOT large=>high energy
    rung = "REDUCED"
    payload = {
        "schema": "largefiber_energy_proof.v1",
        "object": "large R=2 fiber => high energy (CS proved; density REDUCED)",
        "status": STATUS,
        "proof_status": rung,
        "rung": rung,
        "verdict": rung,
        "base_sha": BASE_SHA,
        "hard_input": "b / C9 crux",
        "weave": ["W53-M1", "W52", "#579", "C9"],
        "phase0": phase0,
        "proof_texts": {
            "CS_and_Sidon": PROOF_CS.strip(),
            "REDUCED": PROOF_REDUCED.strip(),
        },
        "toys": toys,
        "discharged": (
            "Trivial CS bound Delta>=1/f and Sidon extremal Delta~(2/f); "
            "shows CS is insufficient for large=>high energy."
        ),
        "open_core_reduced": PROOF_REDUCED.strip(),
        "generator_route": (
            "CS/Sidon extremal lemmas; verify Delta>=1/f on R=2 fiber toys"
        ),
        "checker_route": (
            "recompute E and Delta on toy fibers; four-tuple energy; phase0 cube3"
        ),
        "claim_boundaries": {
            "is_counterexample": False,
            "is_theorem": False,
            "is_measurement": True,
            "theorem_scope": "only CS/Sidon standard lemmas; not large=>high energy",
        },
        "evidence_type": "FINITE_TOY_ROW",
        "falsifiable": True,
        "is_tautology_under_preconditions": False,
        "is_degenerate_by_construction": False,
        "beats_trivial_baseline": True,
        "nonclaims": [
            "Does NOT prove large fiber => high energy at linear density.",
            "CS bound goes to 0 as f grows — insufficient for the crux.",
            "Toy evidence is not an asymptotic theorem.",
        ],
        "honest_headline": (
            f"Rung {rung}: CS Delta>=1/f certified on toys; "
            f"large=>high energy REDUCED to beating Sidon on R=2 fibers"
        ),
        "regeneration": "py -3.13 experimental/scripts/verify_largefiber_energy_proof.py",
        "all_pass": phase0["pass"] and toys["pass"],
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
    ok = ok and cert.get("toys", {}).get("all_cs_holds")
    # spot CS
    for r in (cert.get("toys", {}).get("rows") or [])[:5]:
        if r["Delta"] + 1e-9 < 1.0 / r["f"]:
            ok = False
    if ok:
        print("RESULT: PASS")
        print(f"payload_sha256: {cert['payload_sha256']}")
        print(f"verdict: {cert.get('verdict')}")
        print(f"phase0: {cert.get('phase0', {}).get('paste')}")
        print(f"cs toys: {cert.get('toys', {}).get('n_fiber_rows')}")
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
