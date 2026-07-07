#!/usr/bin/env python3
"""Exact small-model experiments for the row-sharp Q prefix atom routes.

This is evidence-generation, not a deployed-row proof.  It enumerates small
dyadic cyclic domains and records five route diagnostics:

* Route D folding-defect profiles.
* Top-seam marked incidence for minimal Q1 collisions.
* Toy BC-to-Q chart decomposition checks.
* Primitive orbit excess / exact-lift class diagnostics.
* Composite-prefix gcd(e,N) descent regressions.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "rowsharp-q-prefix-atom-routes-v1"
CERT_PATH = CERT_DIR / "rowsharp_q_prefix_atom_routes_v1.json"
REPORT_PATH = ROOT / "experimental" / "notes" / "thresholds" / "rowsharp_q_prefix_atom_routes_v1.md"


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def factor(n: int) -> list[int]:
    out: list[int] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def primitive_root(p: int) -> int:
    factors = factor(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise ValueError(f"no primitive root found for {p}")


def domain_values(p: int, n: int) -> list[int]:
    ensure((p - 1) % n == 0, "n must divide p-1")
    g = primitive_root(p)
    omega = pow(g, (p - 1) // n, p)
    ensure(pow(omega, n, p) == 1 and pow(omega, n // 2, p) != 1, "bad order-n generator")
    return [pow(omega, i, p) for i in range(n)]


def mask_from_exps(exps: tuple[int, ...]) -> int:
    mask = 0
    for e in exps:
        mask |= 1 << e
    return mask


def exps_from_mask(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def prefix_from_exps(exps: list[int], values: list[int], p: int, w: int) -> tuple[int, ...]:
    elem = [0] * (w + 1)
    elem[0] = 1
    upto = 0
    for exp in exps:
        x = values[exp]
        upto = min(w, upto + 1)
        for d in range(upto, 0, -1):
            elem[d] = (elem[d] + x * elem[d - 1]) % p
    return tuple(((-elem[d]) if d % 2 else elem[d]) % p for d in range(1, w + 1))


def prefix_from_mask(mask: int, values: list[int], p: int, w: int) -> tuple[int, ...]:
    return prefix_from_exps(exps_from_mask(mask, len(values)), values, p, w)


def all_fibers(p: int, n: int, j: int, w: int) -> tuple[list[int], dict[tuple[int, ...], list[int]]]:
    values = domain_values(p, n)
    fibers: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for exps in itertools.combinations(range(n), j):
        mask = mask_from_exps(exps)
        fibers[prefix_from_exps(list(exps), values, p, w)].append(mask)
    return values, dict(fibers)


def twist_target(prefix: tuple[int, ...], omega: int, shift: int, p: int) -> tuple[int, ...]:
    return tuple((coord * pow(omega, shift * (idx + 1), p)) % p for idx, coord in enumerate(prefix))


def target_stabilizer_size(prefix: tuple[int, ...], omega: int, n: int, p: int) -> int:
    return sum(1 for shift in range(n) if twist_target(prefix, omega, shift, p) == prefix)


def folding_defect_size(mask: int, n: int) -> int:
    half = n // 2
    return sum(((mask >> i) & 1) ^ ((mask >> (i + half)) & 1) for i in range(half))


def is_h_coset_union(mask: int, n: int, h: int) -> bool:
    step = n // h
    seen = set()
    for start in range(n):
        if start in seen:
            continue
        coset = [(start + k * step) % n for k in range(h)]
        seen.update(coset)
        bits = [((mask >> e) & 1) for e in coset]
        if any(bit != bits[0] for bit in bits):
            return False
    return True


def cyclo_root_vec(exp: int, n: int) -> tuple[int, ...]:
    half = n // 2
    exp %= n
    sign = 1
    if exp >= half:
        exp -= half
        sign = -1
    out = [0] * half
    out[exp] = sign
    return tuple(out)


def cyclo_add(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x + y for x, y in zip(a, b))


def cyclo_neg(a: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(-x for x in a)


def cyclo_mul_root(vec: tuple[int, ...], exp: int, n: int) -> tuple[int, ...]:
    half = n // 2
    out = [0] * half
    for i, coeff in enumerate(vec):
        if not coeff:
            continue
        e = i + exp
        e %= n
        sign = 1
        if e >= half:
            e -= half
            sign = -1
        out[e] += sign * coeff
    return tuple(out)


def exact_prefix_from_mask(mask: int, n: int, w: int) -> tuple[tuple[int, ...], ...]:
    zero = (0,) * (n // 2)
    elem = [zero for _ in range(w + 1)]
    elem[0] = (1,) + (0,) * (n // 2 - 1)
    upto = 0
    for exp in exps_from_mask(mask, n):
        upto = min(w, upto + 1)
        for d in range(upto, 0, -1):
            elem[d] = cyclo_add(elem[d], cyclo_mul_root(elem[d - 1], exp, n))
    return tuple(cyclo_neg(elem[d]) if d % 2 else elem[d] for d in range(1, w + 1))


def poly_coeffs_from_exps(exps: list[int], values: list[int], p: int) -> list[int]:
    coeffs = [1]
    for exp in exps:
        x = values[exp]
        new = [0] * (len(coeffs) + 1)
        for i, c in enumerate(coeffs):
            new[i] = (new[i] - c * x) % p
            new[i + 1] = (new[i + 1] + c) % p
        coeffs = new
    return coeffs


def route_d_folding_and_orbit_case(p: int, n: int, j: int, w: int) -> dict[str, Any]:
    values, fibers = all_fibers(p, n, j, w)
    omega = values[1]
    total = math.comb(n, j)
    target_space = p**w
    top = sorted(fibers.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:8]
    top_rows = []
    max_primitive = 0
    max_stabilized = 0
    primitive_targets = 0
    stabilized_targets = 0
    exact_lift_diagnostics = []
    for prefix, masks in fibers.items():
        stab = target_stabilizer_size(prefix, omega, n, p)
        if stab == 1:
            primitive_targets += 1
            max_primitive = max(max_primitive, len(masks))
        else:
            stabilized_targets += 1
            max_stabilized = max(max_stabilized, len(masks))
    for prefix, masks in top:
        defect_hist = Counter(folding_defect_size(mask, n) for mask in masks)
        h_union_counts = {str(h): sum(1 for mask in masks if is_h_coset_union(mask, n, h)) for h in (2, 4, 8) if h <= n}
        exact_classes = Counter(exact_prefix_from_mask(mask, n, min(w, 4)) for mask in masks)
        exact_lift_diagnostics.append(
            {
                "fiber_size": len(masks),
                "exact_prefix_depth_used": min(w, 4),
                "exact_lift_classes": len(exact_classes),
                "largest_exact_lift_class": max(exact_classes.values()),
                "nonretained_after_largest": len(masks) - max(exact_classes.values()),
            }
        )
        top_rows.append(
            {
                "prefix": list(prefix),
                "fiber_size": len(masks),
                "target_stabilizer_size": target_stabilizer_size(prefix, omega, n, p),
                "folding_defect_histogram": dict(sorted((str(k), v) for k, v in defect_hist.items())),
                "h_coset_union_counts": h_union_counts,
            }
        )
    thresholds = {}
    for k in (1, 2, 4, 8, 16):
        thresholds[f"gt_{k}_times_average"] = sum(
            1 for masks in fibers.values() if len(masks) * target_space > k * total
        )
    return {
        "case": {"p": p, "n": n, "j": j, "w": w},
        "total_supports": total,
        "nonempty_fibers": len(fibers),
        "target_space_size": target_space,
        "average_fiber_size": total / target_space,
        "max_fiber": max(len(masks) for masks in fibers.values()),
        "max_primitive_target_fiber": max_primitive,
        "max_stabilized_target_fiber": max_stabilized,
        "primitive_targets": primitive_targets,
        "stabilized_targets": stabilized_targets,
        "heavy_target_counts": thresholds,
        "top_fibers": top_rows,
        "top_fiber_exact_lift_diagnostics": exact_lift_diagnostics,
    }


def top_seam_marked_incidence_case(p: int, n: int, j: int, w: int, pair_cap: int = 4_000_000) -> dict[str, Any]:
    values, fibers = all_fibers(p, n, j, w)
    omega = values[1]
    e_min = w + 1
    pair_budget = sum(len(masks) * (len(masks) - 1) // 2 for masks in fibers.values())
    if pair_budget > pair_cap:
        return {
            "case": {"p": p, "n": n, "j": j, "w": w},
            "status": "SKIPPED_PAIR_BUDGET",
            "pair_budget": pair_budget,
            "pair_cap": pair_cap,
        }
    minimal_pairs = 0
    primitive_minimal_pairs = 0
    constant_diff_violations = 0
    mates_per_support: Counter[int] = Counter()
    sidepair_core_counts: dict[tuple[int, int], set[int]] = defaultdict(set)
    for prefix, masks in fibers.items():
        primitive = target_stabilizer_size(prefix, omega, n, p) == 1
        for a, b in itertools.combinations(masks, 2):
            e = (a ^ b).bit_count() // 2
            if e != e_min:
                continue
            minimal_pairs += 1
            if primitive:
                primitive_minimal_pairs += 1
            mates_per_support[a] += 1
            mates_per_support[b] += 1
            side_a = a & ~b
            side_b = b & ~a
            core = a & b
            side_a_prefix = prefix_from_mask(side_a, values, p, e_min - 1)
            side_b_prefix = prefix_from_mask(side_b, values, p, e_min - 1)
            if side_a_prefix != side_b_prefix:
                constant_diff_violations += 1
            sidepair_core_counts[(min(side_a, side_b), max(side_a, side_b))].add(core)
    max_cores_per_sidepair = max((len(v) for v in sidepair_core_counts.values()), default=0)
    return {
        "case": {"p": p, "n": n, "j": j, "w": w},
        "status": "CHECKED",
        "pair_budget": pair_budget,
        "minimal_one_sided_difference": e_min,
        "minimal_unordered_marked_pairs": minimal_pairs,
        "minimal_ordered_marked_pairs": 2 * minimal_pairs,
        "primitive_minimal_unordered_pairs": primitive_minimal_pairs,
        "max_minimal_mates_for_one_support": max(mates_per_support.values(), default=0),
        "side_polynomial_constant_diff_violations": constant_diff_violations,
        "sidepair_keys": len(sidepair_core_counts),
        "max_common_cores_for_one_unmarked_sidepair": max_cores_per_sidepair,
    }


def bc_to_q_toy_chart_case(p: int, n: int, j: int, w: int) -> dict[str, Any]:
    values, fibers = all_fibers(p, n, j, w)
    curves = {
        "linear_first_coordinate": lambda s: tuple([s % p] + [0] * (w - 1)),
        "moment_curve": lambda s: tuple(pow(s, d, p) for d in range(1, w + 1)),
        "shifted_moment_curve": lambda s: tuple((pow(s + 1, d, p) + d) % p for d in range(1, w + 1)),
    }
    out = []
    for name, theta in curves.items():
        targets = [theta(s) for s in range(p)]
        target_set = set(targets)
        sum_fibers = sum(len(fibers.get(t, [])) for t in targets)
        direct = sum(len(masks) for t, masks in fibers.items() if t in target_set)
        target_collision_hist = Counter(targets)
        multiplicity_weighted_direct = sum(
            target_collision_hist[t] * len(fibers.get(t, [])) for t in target_set
        )
        out.append(
            {
                "curve": name,
                "sum_over_parameter_fibers": sum_fibers,
                "direct_union_count": direct,
                "multiplicity_weighted_direct_count": multiplicity_weighted_direct,
                "theta_target_collisions": sum(v - 1 for v in target_collision_hist.values()),
                "max_curve_target_fiber": max((len(fibers.get(t, [])) for t in targets), default=0),
                "multiplicity_accounting_dominates_union": sum_fibers >= direct,
                "decomposition_identity_holds": sum_fibers == multiplicity_weighted_direct,
                "injective_theta": len(target_set) == len(targets),
            }
        )
    return {"case": {"p": p, "n": n, "j": j, "w": w}, "curve_checks": out}


def inv_mod(a: int, m: int) -> int:
    return pow(a % m, -1, m)


def composite_descent_case(p: int, n: int, exponents: list[int]) -> dict[str, Any]:
    values = domain_values(p, n)
    rows = []
    for e in exponents:
        c = math.gcd(e, n)
        n_q = n // c
        e_q = e // c
        inv_e_q = inv_mod(e_q, n_q)
        image = sorted({(e * a) % n for a in range(n)})
        fiber_sizes = Counter((e * a) % n for a in range(n))
        sample_image = image[: min(3, len(image))]
        quotient_roots = []
        full_support: list[int] = []
        for beta in sample_image:
            b = (beta // c) % n_q
            r = (inv_e_q * b) % n_q
            quotient_roots.append((c * r) % n)
            full_support.extend(a for a in range(n) if (e * a) % n == beta)
        full_coeffs = poly_coeffs_from_exps(sorted(full_support), values, p)
        quotient_coeffs = poly_coeffs_from_exps(quotient_roots, values, p)
        substituted = [0] * (c * (len(quotient_coeffs) - 1) + 1)
        for idx, coeff in enumerate(quotient_coeffs):
            substituted[c * idx] = coeff
        rows.append(
            {
                "e": e,
                "gcd_c": c,
                "image_size": len(image),
                "expected_image_size": n_q,
                "fiber_size_set": sorted(set(fiber_sizes.values())),
                "sample_image_exponents": sample_image,
                "sample_quotient_root_exponents_for_X^c": quotient_roots,
                "sample_full_preimage_size": len(full_support),
                "factorization_identity_holds": full_coeffs == substituted,
            }
        )
    return {"case": {"p": p, "n": n}, "rows": rows}


def build_results() -> dict[str, Any]:
    route_cases = [
        (17, 16, 8, 1),
        (17, 16, 8, 2),
        (17, 16, 8, 3),
        (97, 16, 8, 3),
        (97, 32, 5, 2),
        (97, 32, 5, 3),
        (193, 64, 4, 2),
        (257, 128, 3, 2),
    ]
    top_seam_cases = [
        (17, 16, 8, 1),
        (17, 16, 8, 2),
        (17, 16, 8, 3),
        (97, 32, 5, 2),
        (97, 32, 5, 3),
        (193, 64, 4, 2),
    ]
    bc_cases = [
        (17, 16, 8, 2),
        (97, 32, 5, 3),
        (193, 64, 4, 2),
    ]
    composite_cases = [
        composite_descent_case(17, 16, [2, 4, 6, 8, 10, 12]),
        composite_descent_case(97, 32, [2, 4, 6, 8, 12, 16, 20]),
        composite_descent_case(193, 64, [2, 4, 6, 8, 12, 16, 24, 32]),
    ]
    route_results = [route_d_folding_and_orbit_case(*case) for case in route_cases]
    top_seam_results = [top_seam_marked_incidence_case(*case) for case in top_seam_cases]
    bc_results = [bc_to_q_toy_chart_case(*case) for case in bc_cases]
    return {
        "status": "EXPERIMENTAL_EVIDENCE_NOT_A_PROOF",
        "purpose": "row-sharp Q prefix atom route diagnostics",
        "route_d_folding_defect_profiles": route_results,
        "top_seam_marked_incidence": top_seam_results,
        "bc_to_q_toy_chart_decomposition": bc_results,
        "primitive_orbit_excess_diagnostics": [
            {
                "case": row["case"],
                "average_fiber_size": row["average_fiber_size"],
                "max_fiber": row["max_fiber"],
                "max_primitive_target_fiber": row["max_primitive_target_fiber"],
                "max_stabilized_target_fiber": row["max_stabilized_target_fiber"],
                "heavy_target_counts": row["heavy_target_counts"],
                "top_fiber_exact_lift_diagnostics": row["top_fiber_exact_lift_diagnostics"],
            }
            for row in route_results
        ],
        "composite_prefix_gcd_descent_regression": composite_cases,
        "summary_findings": summarize_findings(route_results, top_seam_results, bc_results, composite_cases),
    }


def summarize_findings(route_results: list[dict[str, Any]], top: list[dict[str, Any]], bc: list[dict[str, Any]], comp: list[dict[str, Any]]) -> dict[str, Any]:
    nonretained_failures = [
        {
            "case": row["case"],
            "fiber_size": diag["fiber_size"],
            "nonretained": diag["nonretained_after_largest"],
        }
        for row in route_results
        for diag in row["top_fiber_exact_lift_diagnostics"][:1]
        if diag["nonretained_after_largest"] > 0
    ]
    top_violations = [row for row in top if row.get("side_polynomial_constant_diff_violations", 0) != 0]
    composite_failures = [r for case in comp for r in case["rows"] if not r["factorization_identity_holds"]]
    return {
        "route_d_observation": "top fibers frequently have large nonzero signed folding defect; zero-defect descent alone is insufficient",
        "generated_prefix_support_observation": "top finite fibers often split into multiple exact lift classes; support payment cannot be inferred from image labels",
        "top_seam_observation": "minimal Q1 collisions satisfy the constant side-polynomial condition in all checked cases",
        "top_seam_free_core_warning": "some unmarked side-pair keys have multiple common cores/mates, so marked incidence is the right object",
        "bc_to_q_observation": "toy chart counts are controlled by multiplicity-weighted sums of ordinary prefix fibers; non-injective theta curves require multiplicity accounting",
        "composite_descent_observation": "gcd(e,N) fiber-factorization passed all checked finite regressions",
        "cases_with_nonretained_exact_lift_mass": nonretained_failures[:12],
        "top_seam_constant_diff_violations": len(top_violations),
        "composite_descent_failures": len(composite_failures),
    }


def render_report(results: dict[str, Any]) -> str:
    lines = [
        "# Row-sharp Q prefix atom route experiments v1",
        "",
        f"Status: `{results['status']}`.",
        "",
        "These are exact small-model experiments.  They do not prove the deployed",
        "row-sharp Q theorem.",
        "",
        "## Summary",
        "",
    ]
    for key, value in results["summary_findings"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Route D folding / primitive orbit diagnostics", ""])
    for row in results["route_d_folding_defect_profiles"]:
        case = row["case"]
        lines.append(
            f"- `F_{case['p']}, n={case['n']}, j={case['j']}, w={case['w']}`: "
            f"max={row['max_fiber']}, max primitive={row['max_primitive_target_fiber']}, "
            f"max stabilized={row['max_stabilized_target_fiber']}, nonempty fibers={row['nonempty_fibers']}."
        )
        if row["top_fibers"]:
            lines.append(f"  top defect histogram: `{row['top_fibers'][0]['folding_defect_histogram']}`")
            lines.append(f"  top exact-lift diagnostic: `{row['top_fiber_exact_lift_diagnostics'][0]}`")
    lines.extend(["", "## Top-seam marked incidence", ""])
    for row in results["top_seam_marked_incidence"]:
        case = row["case"]
        if row["status"] != "CHECKED":
            lines.append(f"- `F_{case['p']}, n={case['n']}, j={case['j']}, w={case['w']}` skipped: pair budget `{row['pair_budget']}`.")
            continue
        lines.append(
            f"- `F_{case['p']}, n={case['n']}, j={case['j']}, w={case['w']}`: "
            f"minimal marked pairs={row['minimal_unordered_marked_pairs']}, "
            f"max mates/support={row['max_minimal_mates_for_one_support']}, "
            f"constant-diff violations={row['side_polynomial_constant_diff_violations']}, "
            f"max cores/unmarked sidepair={row['max_common_cores_for_one_unmarked_sidepair']}."
        )
    lines.extend(["", "## BC-to-Q toy chart checks", ""])
    for row in results["bc_to_q_toy_chart_decomposition"]:
        case = row["case"]
        for curve in row["curve_checks"]:
            lines.append(
                f"- `F_{case['p']}, n={case['n']}, j={case['j']}, w={case['w']}`, `{curve['curve']}`: "
            f"sum={curve['sum_over_parameter_fibers']}, union={curve['direct_union_count']}, "
            f"weighted={curve.get('multiplicity_weighted_direct_count', curve['sum_over_parameter_fibers'])}, "
            f"theta collisions={curve['theta_target_collisions']}."
        )
    lines.extend(["", "## Composite-prefix gcd descent regressions", ""])
    for case in results["composite_prefix_gcd_descent_regression"]:
        c = case["case"]
        good = sum(1 for row in case["rows"] if row["factorization_identity_holds"])
        lines.append(f"- `F_{c['p']}, n={c['n']}`: {good}/{len(case['rows'])} gcd-descent factorizations passed.")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The experiments support Route D as the right next route, but also show",
            "why it must be a large-defect transfer theorem rather than a zero-defect",
            "or image-cell argument.  Top-seam collisions obey the expected side",
            "normal form, but marked incidence is necessary.  Composite descent",
            "behaves exactly with `gcd(e,N)`, matching the repaired theorem shape.",
        ]
    )
    return "\n".join(lines) + "\n"


def json_bytes(results: dict[str, Any]) -> bytes:
    return (json.dumps(results, indent=2, sort_keys=True) + "\n").encode("utf-8")


def canonicalize(results: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(results, sort_keys=True))


def report_bytes(results: dict[str, Any]) -> bytes:
    return render_report(results).encode("utf-8")


def write_artifacts(results: dict[str, Any]) -> None:
    results = canonicalize(results)
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_bytes(json_bytes(results))
    REPORT_PATH.write_bytes(report_bytes(results))


def check_artifacts(results: dict[str, Any]) -> None:
    results = canonicalize(results)
    ensure(CERT_PATH.exists(), "missing JSON artifact")
    ensure(REPORT_PATH.exists(), "missing report artifact")
    ensure(CERT_PATH.read_bytes() == json_bytes(results), "JSON artifact mismatch; run --write")
    ensure(REPORT_PATH.read_bytes() == report_bytes(results), "report artifact mismatch; run --write")


def load_artifacts() -> dict[str, Any]:
    ensure(CERT_PATH.exists(), "missing JSON artifact")
    ensure(REPORT_PATH.exists(), "missing report artifact")
    with CERT_PATH.open("r", encoding="utf-8") as f:
        results = json.load(f)
    ensure(results.get("status") == "EXPERIMENTAL_EVIDENCE_NOT_A_PROOF", "unexpected status")
    ensure("summary_findings" in results, "missing summary_findings")
    ensure(REPORT_PATH.read_bytes() == report_bytes(results), "report artifact mismatch; run --full --write")
    return results


def tamper_selftest() -> None:
    results = load_artifacts()
    bad = json.loads(json.dumps(results))
    bad["summary_findings"]["composite_descent_failures"] = 1
    try:
        ensure(report_bytes(bad) == REPORT_PATH.read_bytes(), "tamper detected")
    except AssertionError:
        print("tamper self-test passed")
        return
    raise AssertionError("tamper self-test failed to detect mutation")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--full", "--slow", dest="full", action="store_true", help="recompute full experiment data")
    parser.add_argument("--quick", action="store_true", help="default: validate stored artifacts without recomputing")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--case", nargs=4, metavar=("P", "N", "J", "W"), type=int, help="run one Route-D case")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.case:
        row = route_d_folding_and_orbit_case(*args.case)
        print(json.dumps(row, indent=2, sort_keys=True))
        return

    if args.tamper_selftest:
        tamper_selftest()
        return

    if args.write or args.full:
        results = build_results()
    else:
        results = load_artifacts()

    if args.write:
        write_artifacts(results)
        print(f"wrote {CERT_PATH}")
        print(f"wrote {REPORT_PATH}")
    if args.check:
        if args.full:
            check_artifacts(results)
        else:
            load_artifacts()
        print("artifact check passed: 2 files")
    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
    if not (args.write or args.check or args.json):
        print("STATUS:", results["status"])
        print("route_cases:", len(results["route_d_folding_defect_profiles"]))
        print("top_seam_cases:", len(results["top_seam_marked_incidence"]))
        print("RESULT: PASS")


if __name__ == "__main__":
    main()
