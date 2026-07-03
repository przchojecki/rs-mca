#!/usr/bin/env python3
"""Verify E26 dihedral window arithmetic.

E26 is deliberately arithmetic-only.  It enumerates the scales reachable by
dihedral/Chebyshev twin-fiber windows on 2-power multiplicative rows:

    d = m * ell,

where ``m`` is the twin-fiber size and ``ell`` is the number of twin fibers
selected.  On a row of length ``n = 2^N``, the achievable twin-fiber sizes are
``m = 2, 4, ..., n``.  A pure dihedral window has ``m=2``; ``m>2`` records a
mixed multiplicative-then-dihedral window.

The checker answers the rate-1/2 coverage-gap question from E26:
whether any dihedral or mixed scale lands strictly beyond the old 2-power
multiplicative endpoint ``M_max = 2^33`` and at or below
``sigma* = 8,592,912,738`` at the prize-max row.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / (
    "experimental/data/certificates/e26-dihedral-window-arithmetic/"
    "e26_dihedral_window_arithmetic.json"
)

SCHEMA_VERSION = "e26-dihedral-window-arithmetic-v1"
DAG_NODES = ["rate_half_coverage_gap", "dihedral_quotient_stratum"]
PRIZE_N = 2**41
PRIZE_SIGMA_STAR = 8_592_912_738
PRIZE_MULTIPLICATIVE_M_MAX = 2**33
PRIZE_Q_BITS = 255.9
TARGET_BITS = 128


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def log2_int(value: int) -> float:
    bits = value.bit_length()
    if bits <= 900:
        return math.log2(value)
    shift = bits - 900
    return math.log2(value >> shift) + shift


LN2 = math.log(2.0)


def log2_binom_bracket(n: int, k: int) -> tuple[float, float]:
    """Rigorous enough Robbins bracket for log2 binom(n,k).

    For the toy rows the exact integer is used.  For prize-scale rows, Robbins'
    factorial bounds give a stable bracket much narrower than one bit.
    """

    if k < 0 or k > n:
        raise ValueError((n, k))
    if k == 0 or k == n:
        return 0.0, 0.0
    k = min(k, n - k)
    if n <= 4096:
        exact = log2_int(math.comb(n, k))
        return exact, exact

    main = k * math.log(n / k) + (n - k) * math.log(n / (n - k))
    half = 0.5 * math.log(n / (2 * math.pi * k * (n - k)))
    lo_r = 1 / (12 * n + 1) - 1 / (12 * k) - 1 / (12 * (n - k))
    hi_r = 1 / (12 * n) - 1 / (12 * k + 1) - 1 / (12 * (n - k) + 1)
    pad = 4e-15 * abs(main) + 1e-9
    return (main + half + lo_r - pad) / LN2, (main + half + hi_r + pad) / LN2


def powers_of_two_through(n: int) -> list[int]:
    out = []
    value = 1
    while value <= n:
        out.append(value)
        value *= 2
    return out


def floor_power_of_two_at_most(value: int) -> int:
    require(value > 0, "value must be positive")
    return 1 << (value.bit_length() - 1)


@dataclass(frozen=True)
class RowSpec:
    label: str
    n: int
    k: int
    sigma_star: int
    q_bits: float
    old_multiplicative_endpoint: int | None = None

    @property
    def bstar_log2(self) -> float:
        if self.label == "pinned_f17_mu512":
            return math.log2((17**32) // 2**TARGET_BITS)
        return self.q_bits - TARGET_BITS


def hit_interval_for_m(m: int, lower: int, upper: int) -> tuple[int, int, int]:
    """Return (count, first_d, last_d) for multiples of m in [lower, upper]."""

    first_ell = (lower + m - 1) // m
    last_ell = upper // m
    if last_ell < first_ell:
        return 0, 0, 0
    return last_ell - first_ell + 1, first_ell * m, last_ell * m


def window_count_record(n: int, m: int, d: int, bstar_log2: float) -> dict[str, Any]:
    ell = d // m
    fiber_count = n // m
    lo, hi = log2_binom_bracket(fiber_count, ell)
    return {
        "formula": f"binom({fiber_count}, {ell})",
        "twin_fiber_size_m": m,
        "ell": ell,
        "scale_d": d,
        "fiber_count": fiber_count,
        "log2_count_lower": round(lo, 6),
        "log2_count_upper": round(hi, 6),
        "bstar_log2": round(bstar_log2, 6),
        "count_exceeds_Bstar": lo > bstar_log2,
    }


def row_arithmetic(spec: RowSpec) -> dict[str, Any]:
    old_endpoint = spec.old_multiplicative_endpoint
    if old_endpoint is None:
        old_endpoint = floor_power_of_two_at_most(spec.sigma_star)
    require(old_endpoint <= spec.sigma_star, "old endpoint must lie at or below sigma*")
    require(spec.n & (spec.n - 1) == 0, "E26 verifier currently handles 2-power rows")

    inclusive_lower = old_endpoint
    strict_lower = old_endpoint + 1
    upper = spec.sigma_star
    twin_sizes = [m for m in powers_of_two_through(spec.n) if m >= 2]

    classes = []
    strict_classes = []
    for m in twin_sizes:
        inclusive_count, inclusive_first, inclusive_last = hit_interval_for_m(
            m, inclusive_lower, upper
        )
        strict_count, strict_first, strict_last = hit_interval_for_m(m, strict_lower, upper)
        if inclusive_count:
            record = {
                "kind": "pure_dihedral" if m == 2 else "mixed_dihedral_multiplicative",
                "twin_fiber_size_m": m,
                "quotient_twin_fiber_count": spec.n // m,
                "inclusive_hit_count": inclusive_count,
                "inclusive_first_scale": inclusive_first,
                "inclusive_last_scale": inclusive_last,
                "strict_new_hit_count": strict_count,
                "strict_first_new_scale": strict_first if strict_count else None,
                "strict_last_new_scale": strict_last if strict_count else None,
            }
            classes.append(record)
            if strict_count:
                strict_classes.append(record)

    first_strict = min(
        (row for row in strict_classes),
        key=lambda row: (row["strict_first_new_scale"], row["twin_fiber_size_m"]),
        default=None,
    )
    endpoint = window_count_record(spec.n, 2, old_endpoint, spec.bstar_log2)
    first_new = (
        window_count_record(
            spec.n,
            first_strict["twin_fiber_size_m"],
            first_strict["strict_first_new_scale"],
            spec.bstar_log2,
        )
        if first_strict
        else None
    )

    strict_hit_count = sum(row["strict_new_hit_count"] for row in classes)
    max_mixed_m = max(
        (
            row["twin_fiber_size_m"]
            for row in strict_classes
            if row["kind"] == "mixed_dihedral_multiplicative"
        ),
        default=None,
    )
    pure_dihedral_strict_count = next(
        (
            row["strict_new_hit_count"]
            for row in classes
            if row["kind"] == "pure_dihedral"
        ),
        0,
    )
    checks = {
        "endpoint_is_power_of_two": old_endpoint & (old_endpoint - 1) == 0,
        "inclusive_band_count_matches_bounds": upper - inclusive_lower + 1
        == spec.sigma_star - old_endpoint + 1,
        "strict_band_count_matches_bounds": max(0, upper - strict_lower + 1)
        == max(0, spec.sigma_star - old_endpoint),
        "strict_hit_count_nonnegative": strict_hit_count >= 0,
        "first_new_count_exceeds_budget_when_present": (
            first_new is None or first_new["count_exceeds_Bstar"]
        ),
    }

    return {
        "label": spec.label,
        "n": spec.n,
        "k": spec.k,
        "rate": f"{spec.k}/{spec.n}",
        "sigma_star": spec.sigma_star,
        "old_multiplicative_endpoint": old_endpoint,
        "inclusive_interval": {
            "lower": inclusive_lower,
            "upper": upper,
            "count": max(0, upper - inclusive_lower + 1),
        },
        "strict_new_interval": {
            "lower": strict_lower,
            "upper": upper,
            "count": max(0, upper - strict_lower + 1),
        },
        "coverage_found_strictly_beyond_old_endpoint": bool(strict_classes),
        "strict_hit_class_count": len(strict_classes),
        "strict_hit_scale_count_with_twin_size_multiplicity": strict_hit_count,
        "strict_distinct_scale_hit_count": pure_dihedral_strict_count,
        "max_mixed_twin_fiber_size_with_new_hit": max_mixed_m,
        "endpoint_dihedral_formula": endpoint,
        "first_new_dihedral_formula": first_new,
        "hit_classes": classes,
        "checks": checks,
    }


def build_certificate() -> dict[str, Any]:
    rows = [
        RowSpec(
            label="pinned_f17_mu512",
            n=512,
            k=256,
            sigma_star=4,
            q_bits=log2_int(17**32),
            old_multiplicative_endpoint=4,
        ),
        RowSpec(
            label="row_c_n1024",
            n=1024,
            k=512,
            sigma_star=4,
            q_bits=250.0,
            old_multiplicative_endpoint=4,
        ),
        RowSpec(
            label="prize_max_rate_half",
            n=PRIZE_N,
            k=PRIZE_N // 2,
            sigma_star=PRIZE_SIGMA_STAR,
            q_bits=PRIZE_Q_BITS,
            old_multiplicative_endpoint=PRIZE_MULTIPLICATIVE_M_MAX,
        ),
    ]
    row_payloads = [row_arithmetic(row) for row in rows]
    prize = next(row for row in row_payloads if row["label"] == "prize_max_rate_half")
    require(
        prize["inclusive_interval"]["count"] == 2_978_147,
        "rate-1/2 inclusive band count drifted",
    )
    require(
        prize["strict_new_interval"]["count"] == 2_978_146,
        "rate-1/2 strict band count drifted",
    )
    require(
        prize["first_new_dihedral_formula"]["scale_d"] == PRIZE_MULTIPLICATIVE_M_MAX + 2,
        "first new pure-dihedral scale drifted",
    )
    require(
        prize["coverage_found_strictly_beyond_old_endpoint"],
        "E26 coverage unexpectedly absent",
    )
    require(
        prize["first_new_dihedral_formula"]["count_exceeds_Bstar"],
        "first new dihedral formula no longer exceeds B*",
    )

    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED_ARITHMETIC / COVERAGE_FOUND_CONDITIONAL_ON_DIHEDRAL_LEDGER",
        "task_id": "E26",
        "dag_nodes": DAG_NODES,
        "model": {
            "window_scale": "d = m * ell",
            "twin_fiber_size_m": (
                "m=2 is pure inversion-pair/Chebyshev; m>2 is mixed "
                "multiplicative quotient followed by inversion"
            ),
            "unsafe_count_formula": "binom(n/m, ell) for moving twin-fiber windows",
            "old_endpoint_policy": (
                "the old multiplicative endpoint is counted separately; "
                "new coverage means d > old endpoint"
            ),
        },
        "summary": {
            "rate_half_coverage_found": prize[
                "coverage_found_strictly_beyond_old_endpoint"
            ],
            "rate_half_old_endpoint": prize["old_multiplicative_endpoint"],
            "rate_half_sigma_star": prize["sigma_star"],
            "rate_half_inclusive_band_count": prize["inclusive_interval"]["count"],
            "rate_half_strict_new_band_count": prize["strict_new_interval"]["count"],
            "rate_half_strict_distinct_dihedral_scale_count": prize[
                "strict_distinct_scale_hit_count"
            ],
            "first_new_scale": prize["first_new_dihedral_formula"]["scale_d"],
            "first_new_twin_fiber_size": prize["first_new_dihedral_formula"][
                "twin_fiber_size_m"
            ],
            "first_new_formula": prize["first_new_dihedral_formula"]["formula"],
            "first_new_log2_count_lower": prize["first_new_dihedral_formula"][
                "log2_count_lower"
            ],
            "first_new_exceeds_Bstar": prize["first_new_dihedral_formula"][
                "count_exceeds_Bstar"
            ],
            "mixed_hit_max_twin_fiber_size": prize[
                "max_mixed_twin_fiber_size_with_new_hit"
            ],
        },
        "rows": row_payloads,
        "nonclaims": [
            "does not prove the dihedral stratum is paid; that is E25",
            "does not solve alignment systems or run M5 charts",
            "does not enumerate received-word pairs",
            "does not claim non-2-power quotient coverage",
        ],
    }
    require(all(all(row["checks"].values()) for row in row_payloads), "row check failed")
    payload["payload_sha256"] = sha256_json(payload)
    return payload


def check_certificate(path: Path, expected: dict[str, Any]) -> None:
    actual = json.loads(path.read_text(encoding="utf-8"))
    if actual != expected:
        raise AssertionError(f"certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("E26 dihedral window arithmetic")
    print(f"status: {certificate['status']}")
    print(
        "rate-1/2 band: old endpoint={rate_half_old_endpoint}, "
        "sigma*={rate_half_sigma_star}, strict new radii={rate_half_strict_new_band_count}".format(
            **summary
        )
    )
    print(
        "first new scale: d={first_new_scale}, m={first_new_twin_fiber_size}, "
        "{first_new_formula}, log2 count lower={first_new_log2_count_lower}".format(
            **summary
        )
    )
    print("coverage found:", summary["rate_half_coverage_found"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        nargs="?",
        const=OUTPUT,
        type=Path,
        help="write deterministic E26 JSON, optionally to PATH",
    )
    parser.add_argument(
        "--check",
        nargs="?",
        const=OUTPUT,
        type=Path,
        help="check deterministic E26 JSON, optionally at PATH",
    )
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check, certificate)
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
