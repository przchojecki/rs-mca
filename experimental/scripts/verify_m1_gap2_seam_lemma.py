#!/usr/bin/env python3
"""Verify the GAP-2 quotient-periodic seam arithmetic.

The note proved by this verifier is intentionally narrow.  It checks the
integer arithmetic behind the S4 claim:

  * a pullback denominator E(X)=g(X^M) has degree divisible by M;
  * when M | gcd(n,k), exact-bucket support periodicity M | j is equivalent
    to window periodicity M | t_win, with j=n-A and t_win=A-k;
  * when M | n and M | j but M does not divide k, the fold is not
    rate-preserving and cannot be a quotient row with dimension k/M.

Run:
    python3 experimental/scripts/verify_m1_gap2_seam_lemma.py
    python3 experimental/scripts/verify_m1_gap2_seam_lemma.py --emit
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "m1-gap2-seam"
    / "gap2_seam_certificate.json"
)

RATES = {
    "1/2": (1, 2),
    "1/4": (1, 4),
    "1/8": (1, 8),
    "1/16": (1, 16),
}


def divisors(value: int) -> list[int]:
    return [d for d in range(1, value + 1) if value % d == 0]


def powers_of_two_rows(min_exp: int = 4, max_exp: int = 12) -> list[int]:
    return [2**exp for exp in range(min_exp, max_exp + 1)]


def rate_k(n: int, rate: tuple[int, int]) -> int:
    numerator, denominator = rate
    assert n % denominator == 0
    return n * numerator // denominator


def bucket(n: int, k: int, agreement: int) -> tuple[int, int, int]:
    j = n - agreement
    t_win = agreement - k
    r = n - k
    assert j + t_win == r
    return j, t_win, r


def check_pullback_degree_divisibility() -> tuple[bool, list[str], dict[str, object]]:
    checked = 0
    bad: list[dict[str, int]] = []
    for n in range(2, 129):
        for m in divisors(n):
            if m == 1:
                continue
            for deg_g in range(1, 17):
                t_denom = m * deg_g
                checked += 1
                if t_denom % m != 0:
                    bad.append({"n": n, "M": m, "deg_g": deg_g, "t_denom": t_denom})
    ok = not bad
    payload = {"checked_pullback_degrees": checked, "counterexamples": bad[:5]}
    return ok, [
        f"checked pullback degrees E(X)=g(X^M): {checked}",
        f"counterexamples to M | deg(E): {len(bad)}",
    ], payload


def check_rate_preserving_equivalence() -> tuple[bool, list[str], dict[str, object]]:
    checked = 0
    bad: list[dict[str, int | str]] = []
    examples: list[dict[str, int | str]] = []
    for n in powers_of_two_rows():
        for label, rate in RATES.items():
            k = rate_k(n, rate)
            for m in divisors(math.gcd(n, k)):
                if m == 1:
                    continue
                for agreement in range(k, n + 1):
                    j, t_win, r = bucket(n, k, agreement)
                    checked += 1
                    equivalent = (j % m == 0) == (t_win % m == 0)
                    quotient_integral = (
                        n % m == 0
                        and k % m == 0
                        and (j % m == 0) == (agreement % m == 0)
                    )
                    if not (equivalent and quotient_integral and r % m == 0):
                        bad.append({
                            "n": n,
                            "rate": label,
                            "k": k,
                            "M": m,
                            "A": agreement,
                            "j": j,
                            "t_win": t_win,
                            "r": r,
                        })
                    if len(examples) < 6 and j % m == 0:
                        examples.append({
                            "n": n,
                            "rate": label,
                            "k": k,
                            "M": m,
                            "A": agreement,
                            "quotient_n": n // m,
                            "quotient_k": k // m,
                            "quotient_A": agreement // m,
                            "quotient_j": j // m,
                            "quotient_t_win": t_win // m,
                        })
    ok = not bad
    payload = {
        "checked_rate_preserving_buckets": checked,
        "counterexamples": bad[:5],
        "sample_descents": examples,
    }
    return ok, [
        f"checked exact buckets with M | gcd(n,k): {checked}",
        f"counterexamples to M|j iff M|t_win: {len(bad)}",
        f"sample quotient descents recorded: {len(examples)}",
    ], payload


def check_non_rate_preserving_seam() -> tuple[bool, list[str], dict[str, object]]:
    checked = 0
    seam = 0
    bad: list[dict[str, int | str]] = []
    examples: list[dict[str, int | str]] = []
    for n in powers_of_two_rows():
        for label, rate in RATES.items():
            k = rate_k(n, rate)
            for m in divisors(n):
                if m == 1 or k % m == 0:
                    continue
                for agreement in range(k, n + 1):
                    j, t_win, r = bucket(n, k, agreement)
                    if j % m != 0:
                        continue
                    checked += 1
                    is_seam = (
                        n % m == 0
                        and agreement % m == 0
                        and k % m != 0
                        and t_win % m != 0
                        and r % m != 0
                    )
                    if is_seam:
                        seam += 1
                        if len(examples) < 8:
                            examples.append({
                                "n": n,
                                "rate": label,
                                "k": k,
                                "M": m,
                                "A": agreement,
                                "j": j,
                                "t_win": t_win,
                                "reason": "A and j descend but k and t_win do not",
                            })
                    else:
                        bad.append({
                            "n": n,
                            "rate": label,
                            "k": k,
                            "M": m,
                            "A": agreement,
                            "j": j,
                            "t_win": t_win,
                            "r": r,
                        })
    ok = checked == seam and not bad
    payload = {
        "checked_support_periodic_non_rate_preserving_buckets": checked,
        "seam_buckets": seam,
        "counterexamples": bad[:5],
        "sample_seams": examples,
    }
    return ok, [
        f"support-periodic but non-rate-preserving buckets checked: {checked}",
        f"classified as seam: {seam}",
        f"counterexamples: {len(bad)}",
    ], payload


def official_profile_summary() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for exp in (8, 12, 16):
        n = 2**exp
        for label, rate in RATES.items():
            k = rate_k(n, rate)
            active_m = [m for m in divisors(math.gcd(n, k)) if m > 1]
            rows.append({
                "n": n,
                "rate": label,
                "k": k,
                "gcd_n_k": math.gcd(n, k),
                "rate_preserving_pullback_scales": active_m,
                "max_rate_preserving_scale": max(active_m) if active_m else 1,
            })
    return rows


def build_artifact() -> dict[str, object]:
    pull_ok, _, pull = check_pullback_degree_divisibility()
    rate_ok, _, rate = check_rate_preserving_equivalence()
    seam_ok, _, seam = check_non_rate_preserving_seam()
    classification = (
        "GAP2_SEAM_ARITHMETIC_CLOSED_FOR_RATE_PRESERVING_PULLBACKS"
        if pull_ok and rate_ok and seam_ok
        else "GAP2_SEAM_ARITHMETIC_FAILURE"
    )
    return {
        "schema_version": "m1-gap2-seam-v1",
        "status": "PROVED/ARITHMETIC",
        "dag_target": "gap2_seam",
        "classification": classification,
        "lemma": {
            "variables": "n,k,A,j=n-A,t_win=A-k,r=n-k,M",
            "rate_preserving_hypothesis": "M divides gcd(n,k)",
            "conclusion": "M|j iff M|t_win; quotient row parameters n/M,k/M,A/M exist exactly on these buckets",
            "non_rate_preserving_seam": "M|n and M|j but M not dividing k gives no quotient row of dimension k/M",
        },
        "pullback_degree_divisibility": pull,
        "rate_preserving_equivalence": rate,
        "non_rate_preserving_seam": seam,
        "official_2power_profiles": official_profile_summary(),
        "nonclaims": [
            "does not prove stable support implies pullback denominator",
            "does not prove GAP-1 non-equivariant periodic pricing",
            "does not prove the aperiodic local limit",
            "does not change Papers A-D",
        ],
    }


def write_artifact() -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(build_artifact(), indent=2, sort_keys=True) + "\n")


def check_artifact_replay() -> tuple[bool, list[str], dict[str, object]]:
    if not ARTIFACT.exists():
        return False, ["artifact missing; rerun with --emit"], {}
    actual = json.loads(ARTIFACT.read_text())
    expected = build_artifact()
    ok = actual == expected
    return ok, [
        f"artifact path: {ARTIFACT.relative_to(REPO)}",
        f"artifact matches deterministic builder: {ok}",
        f"classification: {actual.get('classification')}",
    ], {}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON certificate")
    args = parser.parse_args()
    if args.emit:
        write_artifact()

    checks = [
        ("pullback degree divisibility", check_pullback_degree_divisibility),
        ("rate-preserving bucket equivalence", check_rate_preserving_equivalence),
        ("non-rate-preserving seam classification", check_non_rate_preserving_seam),
        ("artifact replay", check_artifact_replay),
    ]

    print("=" * 78)
    print("M1 GAP-2 quotient-periodic seam arithmetic")
    print("=" * 78)
    passed = failed = 0
    for title, check in checks:
        ok, details, _ = check()
        passed += int(ok)
        failed += int(not ok)
        print(f"\n[{'PASS' if ok else 'FAIL':4}] {title}")
        for line in details:
            print(f"       {line}")
    print("\n" + "-" * 78)
    print(f"classification: {build_artifact()['classification']}")
    print(f"PASS: {passed}   FAIL: {failed}")
    print("-" * 78)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
