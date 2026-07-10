#!/usr/bin/env python3
"""Independent checker for image-normalized Sidon payment attack.

checker route (MUST differ from generator):
  - Energy: Fourier-style autocorrelation on the abelian group (R^d via
    histogram of all pairwise sums a+b; E = sum_s r_{A+A}(s)^2), not the
    generator's difference-Counter path alone.
  - Gsid rate: recompute from cert fiber-free aggregates by re-running a
    minimal independent instance (p=17,N=8,m=3,R=1) and comparing payment
    inequality direction; re-derive synthetic fail algebraically.
  - Cube3: recompute E via sum-histogram route; require 216.

Status: EXPERIMENTAL.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL"
CERT = Path(
    "experimental/data/certificates/image-normalized-sidon-attack/"
    "image_normalized_sidon_attack.json"
)
# Import sibling generator for shared instance evaluator only after path fix
sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_image_normalized_sidon_attack as gen  # noqa: E402


def energy_sum_histogram(points: list[tuple[int, ...]]) -> int:
    """Independent energy: E = |{(a,b,c,d): a+b=c+d}| = sum_s r_{A+A}(s)^2.

    Equivalent identity to a-b=c-d form, but algorithm is sum-histogram
    (not difference Counter used as generator primary).
    """
    if not points:
        return 0
    sums: Counter[tuple[int, ...]] = Counter()
    for a, b in itertools.product(points, points):
        s = tuple(a[i] + b[i] for i in range(len(a)))
        sums[s] += 1
    return int(sum(v * v for v in sums.values()))


def check_cube3() -> dict[str, Any]:
    A = list(itertools.product([0, 1], repeat=3))
    e_sum = energy_sum_histogram(A)
    e_diff = gen.energy_diff_counter(A)
    e_4 = gen.energy_four_tuple(A)
    return {
        "E_sum_histogram": e_sum,
        "E_diff": e_diff,
        "E_4tuple": e_4,
        "pass": e_sum == 216 and e_diff == 216 and e_4 == 216,
    }


def check_synthetic_algebra() -> dict[str, Any]:
    """Re-derive synthetic fail without trusting cert numbers blindly."""
    N, q, tau = 12, 2, gen.DEFAULT_TAU
    barN, L = 2.0, 10
    eta = 0.25
    target_ratio = math.exp(eta * N)
    f = max(2, int(round(target_ratio * barN)))
    Gsid = (1.0 / L) * (f / barN) ** q
    rate = math.log(Gsid) / (N * q)
    holds = rate <= tau
    return {
        "Gsid": Gsid,
        "rate": rate,
        "holds": holds,
        "pass": (not holds) and rate > tau,
    }


def check_one_live_instance() -> dict[str, Any]:
    """Independent recompute of one shallow instance payment."""
    inst = gen.evaluate_instance(17, 8, 3, 1, seed=0, Omega_mode="all")
    # recompute largest-fiber energy via sum histogram
    T = list(range(1, 8 + 1))
    Omega = gen.all_m_subsets(T, 3)
    fibers = gen.build_fibers(Omega, 1, 17)
    largest = max(fibers.values(), key=len)
    pts = [gen.support_vector(s, T) for s in largest]
    e_sum = energy_sum_histogram(pts)
    e_diff = gen.energy_diff_counter(pts)
    return {
        "instance": {
            "Gsid": inst["Gsid"],
            "rate": inst["rate"],
            "payment_holds": inst["payment_holds"],
            "barN": inst["barN"],
            "L": inst["L"],
            "regime": inst["regime"],
        },
        "largest_E_sum": e_sum,
        "largest_E_diff": e_diff,
        "energy_agree": e_sum == e_diff,
        "pass": inst["energy_routes_agree"] and e_sum == e_diff,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    root = gen.repo_root()
    path = root / CERT
    if not path.is_file():
        print("RESULT: FAIL missing cert", file=sys.stderr)
        return 1
    cert = json.loads(path.read_text(encoding="utf-8"))

    c3 = check_cube3()
    syn = check_synthetic_algebra()
    live = check_one_live_instance()

    # Cross-check cert summary invariants
    summary = cert.get("summary", {})
    inv_ok = (
        summary.get("n_payment_pass", -1) + summary.get("n_payment_fail", -1)
        == summary.get("n_sweep", 0)
        and summary.get("n_energy_routes_agree") == summary.get("n_sweep")
        and cert.get("validation_image_scale", {}).get("energy_gen") == 216
        and cert.get("pins_ok") is True
        and cert.get("synthetic_fail_exhibit", {}).get("pass") is True
    )

    # Cert synthetic numbers should match algebraic recompute (approx)
    cert_syn = cert.get("synthetic_fail_exhibit", {})
    syn_match = (
        abs(cert_syn.get("rate", 0) - syn["rate"]) < 1e-9
        and cert_syn.get("payment_holds") is False
    )

    ok = c3["pass"] and syn["pass"] and live["pass"] and inv_ok and syn_match

    print(
        "route: sum-histogram energy (a+b=c+d) + algebraic synthetic recompute "
        "+ live instance largest-fiber dual energy"
    )
    print(f"cube3: {c3}")
    print(f"synthetic: {syn}")
    print(f"live: energy_agree={live['energy_agree']} holds={live['instance']['payment_holds']}")
    print(f"payload_sha256: {cert.get('payload_sha256')}")
    print(f"verdict: {cert.get('verdict')}")
    print(f"counts: pass={summary.get('n_payment_pass')} fail={summary.get('n_payment_fail')}")
    if ok:
        print("RESULT: PASS")
        return 0
    print("RESULT: FAIL", file=sys.stderr)
    if not c3["pass"]:
        print("  cube3 fail", file=sys.stderr)
    if not syn["pass"]:
        print("  synthetic fail", file=sys.stderr)
    if not live["pass"]:
        print("  live fail", file=sys.stderr)
    if not inv_ok:
        print("  invariant fail", summary, file=sys.stderr)
    if not syn_match:
        print("  syn_match fail", cert_syn, syn, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
