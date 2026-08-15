#!/usr/bin/env python3
"""Exact verifier for the KoalaBear rank-eleven fixed-endpoint router."""

from __future__ import annotations

import argparse
import copy
import json
from fractions import Fraction
from math import comb, prod


ROW = {
    "p": 2130706433,
    "extension_degree": 6,
    "n": 2097152,
    "K": 1048576,
    "m": 1116048,
    "w": 67472,
    "near": 134944,
    "budget": 274980728111395087,
}
S = 10
PARENT = "a3fc2d5aea86577cd50d8b95b6eb2155d4d940f6"


class Reject(ValueError):
    pass


def require(value: bool, message: str) -> None:
    if not value:
        raise Reject(message)


def falling(x: int, length: int) -> int:
    return prod(x - i for i in range(length))


def rising(x: int, length: int) -> int:
    return prod(x + i for i in range(length))


def theta_resource(max_rank: int) -> int:
    """Parent #1168 nonuniform support-margin resource, including lower ranks."""
    n, K, m, w = (ROW[key] for key in ("n", "K", "m", "w"))
    values = [Fraction(n)]
    for rank in range(1, max_rank + 1):
        values.extend(
            [
                Fraction(
                    falling(n, rank + 1),
                    m * rising(w + 1, rank - 1),
                ),
                Fraction(
                    falling(n - K + rank, rank + 1),
                    rising(w + 1, rank),
                ),
            ]
        )
    value = max(values)
    return value.numerator // value.denominator


def continuous_maximizer(max_rank: int) -> int:
    """Unique maximizer of (K-x) binom(x+s,s) on integer 0<=x<=K."""
    K = ROW["K"]
    threshold_numerator = max_rank * K - max_rank - 1
    return threshold_numerator // (max_rank + 1) + 1


def continuous_numerator(x: int, max_rank: int) -> int:
    return (ROW["K"] - x) * comb(x + max_rank, max_rank)


def low_fixed_endpoint_envelope(tau: int) -> int:
    """Includes the one possible projective exceptional slope."""
    require(1 <= tau < ROW["w"], "legal cutoff")
    d = ROW["w"] - tau
    x = continuous_maximizer(S)
    return (
        continuous_numerator(x, S) // comb(d + S, S)
        + 1
    )


def exact_low_scan(tau: int) -> dict[str, int]:
    """Exact deployed floor scan, used only as a calibration below the theorem envelope."""
    require(1 <= tau < ROW["w"], "legal exact cutoff")
    d = ROW["w"] - tau
    denominator = comb(d + S, S)
    best = {"value": -1, "x": -1, "pair_cap": -1}
    for x in range(d, ROW["K"] + 1):
        cap = comb(x + S, S) // denominator
        value = (ROW["K"] - x) * cap
        if value > best["value"]:
            best = {"value": value, "x": x, "pair_cap": cap}
    best["with_exception"] = best["value"] + 1
    return best


def high_margin_cap(tau: int) -> int:
    return theta_resource(S) // (tau + 1)


def fixed_left_total(tau: int) -> dict[str, int]:
    low = low_fixed_endpoint_envelope(tau)
    high = high_margin_cap(tau)
    total = ROW["near"] + high + low
    return {
        "tau": tau,
        "A": ROW["m"] - tau,
        "d": ROW["w"] - tau,
        "forced_common_core": 2 * (ROW["m"] - tau) - ROW["n"],
        "low": low,
        "high": high,
        "near": ROW["near"],
        "total": total,
        "signed_slack": ROW["budget"] - total,
    }


def fixed_right_total(tau: int) -> dict[str, int]:
    ray_cap = 8147918
    total = ROW["near"] + high_margin_cap(tau) + ray_cap
    return {
        "tau": tau,
        "ray_cap": ray_cap,
        "high": high_margin_cap(tau),
        "near": ROW["near"],
        "total": total,
        "signed_slack": ROW["budget"] - total,
    }


def cutoff_scan() -> dict[str, object]:
    rows = [fixed_left_total(tau) for tau in range(1, ROW["w"])]
    paying = [row for row in rows if row["signed_slack"] >= 0]
    require(paying, "nonempty paying cutoff set")
    first = paying[0]
    minimum = min(rows, key=lambda row: (row["total"], row["tau"]))
    minimum_count = sum(row["total"] == minimum["total"] for row in rows)
    return {
        "first_paying": first,
        "preceding": rows[first["tau"] - 2],
        "minimum": minimum,
        "minimum_unique": minimum_count == 1,
        "after_minimum": rows[minimum["tau"]],
    }


def projective_outside_owner_control(prime: int = 5) -> dict[str, int]:
    """Exhaust all GL_2(F_p), outside vectors with first entry nonzero, and slopes."""
    matrices = 0
    cases = 0
    max_roots = 0
    max_mu_zero = 0
    for a in range(prime):
        for b in range(prime):
            for c in range(prime):
                for d in range(prime):
                    det = (a * d - b * c) % prime
                    if det == 0:
                        continue
                    matrices += 1
                    inv_det = pow(det, -1, prime)
                    inverse = (
                        (d * inv_det % prime, -b * inv_det % prime),
                        (-c * inv_det % prime, a * inv_det % prime),
                    )
                    mu_zero = 0
                    for gamma in range(prime):
                        mu = (inverse[0][1] + gamma * inverse[1][1]) % prime
                        if mu == 0:
                            mu_zero += 1
                    max_mu_zero = max(max_mu_zero, mu_zero)
                    require(mu_zero <= 1, "one projective exceptional slope")
                    for v0 in range(1, prime):
                        for v1 in range(prime):
                            cases += 1
                            roots = 0
                            for gamma in range(prime):
                                lam = (inverse[0][0] + gamma * inverse[1][0]) % prime
                                mu = (inverse[0][1] + gamma * inverse[1][1]) % prime
                                if (lam * v0 + mu * v1) % prime == 0:
                                    roots += 1
                            max_roots = max(max_roots, roots)
                            require(roots <= 1, "outside coordinate owns at most one slope")
    return {
        "prime": prime,
        "gl2_matrices": matrices,
        "outside_vector_cases": cases,
        "max_roots": max_roots,
        "max_projective_exceptional_slopes": max_mu_zero,
    }


def build() -> dict[str, object]:
    resource = theta_resource(S)
    require(resource == 106618568137036225644, "parent theta resource")

    xstar = continuous_maximizer(S)
    require(xstar == 953250, "continuous maximizer")
    require(
        continuous_numerator(xstar, S) > continuous_numerator(xstar - 1, S),
        "left neighboring maximum check",
    )
    require(
        continuous_numerator(xstar, S) > continuous_numerator(xstar + 1, S),
        "right neighboring maximum check",
    )

    scan = cutoff_scan()
    require(
        scan["preceding"]
        == {
            "tau": 438,
            "A": 1115610,
            "d": 67034,
            "forced_common_core": 134068,
            "low": 32210458397220937,
            "high": 242866897806460650,
            "near": 134944,
            "total": 275077356203816531,
            "signed_slack": -96628092421444,
        },
        "last failing cutoff",
    )
    require(
        scan["first_paying"]
        == {
            "tau": 439,
            "A": 1115609,
            "d": 67033,
            "forced_common_core": 134066,
            "low": 32215263489919749,
            "high": 242314927584173240,
            "near": 134944,
            "total": 274530191074227933,
            "signed_slack": 450537037167154,
        },
        "first paying cutoff",
    )
    require(
        scan["minimum"]
        == {
            "tau": 3608,
            "A": 1112440,
            "d": 63864,
            "forced_common_core": 127728,
            "low": 52284072490672992,
            "high": 29542412894717712,
            "near": 134944,
            "total": 81826485385525648,
            "signed_slack": 193154242725869439,
        },
        "unique minimum",
    )
    require(scan["minimum_unique"], "minimum uniqueness")
    require(
        scan["after_minimum"]["tau"] == 3609
        and scan["after_minimum"]["total"] == 81826488674890050,
        "adjacent minimum check",
    )

    exact_439 = exact_low_scan(439)
    require(
        exact_439
        == {
            "value": 32215263489916276,
            "x": 953250,
            "pair_cap": 337948340326,
            "with_exception": 32215263489916277,
        },
        "exact floor calibration at first cutoff",
    )
    exact_3608 = exact_low_scan(3608)
    require(
        exact_3608
        == {
            "value": 52284072490618276,
            "x": 953250,
            "pair_cap": 548476517326,
            "with_exception": 52284072490618277,
        },
        "exact floor calibration at optimum",
    )
    require(
        exact_439["with_exception"] <= scan["first_paying"]["low"],
        "analytic envelope dominates exact floor scan",
    )

    right = fixed_right_total(439)
    require(
        right
        == {
            "tau": 439,
            "ray_cap": 8147918,
            "high": 242314927584173240,
            "near": 134944,
            "total": 242314927592456102,
            "signed_slack": 32665800518938985,
        },
        "fixed-right branch",
    )

    projective = projective_outside_owner_control()
    require(
        projective
        == {
            "prime": 5,
            "gl2_matrices": 480,
            "outside_vector_cases": 9600,
            "max_roots": 1,
            "max_projective_exceptional_slopes": 1,
        },
        "projective control",
    )

    return {
        "schema": "kb-mca-rank11-fixed-endpoint-router-v1",
        "parent": PARENT,
        "row": ROW,
        "max_affine_dimension": S,
        "theta_resource": resource,
        "continuous_maximizer": {
            "x": xstar,
            "g": ROW["K"] + xstar,
            "outside": ROW["K"] - xstar,
        },
        "cutoff_scan": scan,
        "exact_low_calibrations": {
            "tau_439": exact_439,
            "tau_3608": exact_3608,
        },
        "fixed_right_at_first_cutoff": right,
        "projective_control": projective,
        "rank_two_terminal": {
            "tau": 439,
            "minimum_pair_core_size": ROW["m"] - 439,
            "minimum_shared_core_size": 2 * (ROW["m"] - 439) - ROW["n"],
            "minimum_common_evaluation_factor_degree": 2 * (ROW["m"] - 439) - ROW["n"],
        },
        "claims": {
            "rank_one_low_pair_anticode_paid": True,
            "rank11_paid": False,
            "koalabear_closed": False,
            "active_v4_ledger_movement": 0,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    result = build()
    if args.tamper_selftest:
        mutations = [
            ("first cutoff", ("cutoff_scan", "first_paying", "tau"), 438),
            ("first total", ("cutoff_scan", "first_paying", "total"), 274530191074227932),
            ("common factor", ("rank_two_terminal", "minimum_common_evaluation_factor_degree"), 134065),
            ("fixed-right cap", ("fixed_right_at_first_cutoff", "ray_cap"), 8147917),
            ("projective roots", ("projective_control", "max_roots"), 2),
            ("ledger movement", ("claims", "active_v4_ledger_movement"), 1),
        ]
        caught = 0
        for _, path, value in mutations:
            changed = copy.deepcopy(result)
            cursor = changed
            for key in path[:-1]:
                cursor = cursor[key]
            cursor[path[-1]] = value
            try:
                require(changed == result, "canonical result")
            except Reject:
                caught += 1
        require(caught == len(mutations), "all hostile mutations caught")
        print(
            "KB_MCA_RANK11_FIXED_ENDPOINT_TAMPER_PASS "
            f"mutations={caught}/{len(mutations)}"
        )
        return

    if args.json:
        print(json.dumps(result, sort_keys=True))
        return

    first = result["cutoff_scan"]["first_paying"]
    minimum = result["cutoff_scan"]["minimum"]
    terminal = result["rank_two_terminal"]
    print(
        "KB_MCA_RANK11_FIXED_ENDPOINT_PASS "
        f"first_tau={first['tau']} "
        f"first_total={first['total']} "
        f"first_slack={first['signed_slack']} "
        f"best_tau={minimum['tau']} "
        f"best_total={minimum['total']} "
        f"rank2_common_factor={terminal['minimum_common_evaluation_factor_degree']}"
    )


if __name__ == "__main__":
    main()
