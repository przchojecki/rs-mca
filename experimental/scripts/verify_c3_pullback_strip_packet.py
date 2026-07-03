#!/usr/bin/env python3
"""Verify the C-3 pullback-strip packet.

This verifier packages the Q3R.4 + QL.5/E22 bookkeeping step:

* replay the quotient-pullback auxiliary-list construction in small fields;
* record the primitive residual split after removing quotient pullbacks and
  low-defect/fixed-excess challengers;
* test the stored E15 challenger certificate against the quotient-pullback
  geometry.

The script is intentionally light.  It does not rerun the full E15 search; it
reads the existing E15 certificate and checks the fields consumed by this
packet.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / (
    "experimental/data/certificates/c3-pullback-strip-packet/"
    "c3_pullback_strip_packet.json"
)
PMA_CERT = ROOT / (
    "experimental/data/certificates/l1-pma-auxiliary-johnson/"
    "l1_pma_auxiliary_johnson.json"
)
E15_CERT = ROOT / (
    "experimental/data/certificates/l1-petal-fixed-excess/"
    "e15_worst_word_challenge.json"
)

SCHEMA_VERSION = "c3-pullback-strip-packet-v1"
DAG_NODES = ["Q3R.4", "QL.5", "E22", "pma_pullback_lists", "pma_wide_residual"]

Poly = tuple[int, ...]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def trim(poly: Iterable[int], p: int) -> Poly:
    out = [coefficient % p for coefficient in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def poly_add(a: Poly, b: Poly, p: int) -> Poly:
    size = max(len(a), len(b))
    return trim((
        ((a[idx] if idx < len(a) else 0) + (b[idx] if idx < len(b) else 0))
        for idx in range(size)
    ), p)


def poly_sub(a: Poly, b: Poly, p: int) -> Poly:
    size = max(len(a), len(b))
    return trim((
        ((a[idx] if idx < len(a) else 0) - (b[idx] if idx < len(b) else 0))
        for idx in range(size)
    ), p)


def poly_mul(a: Poly, b: Poly, p: int) -> Poly:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return trim(out, p)


def poly_eval(poly: Poly, x: int, p: int) -> int:
    value = 0
    for coefficient in reversed(poly):
        value = (value * x + coefficient) % p
    return value


def quotient_locator(roots: Iterable[int], p: int) -> Poly:
    out: Poly = (1,)
    for root in roots:
        out = poly_mul(out, ((-root) % p, 1), p)
    return out


def compose_x_power(poly: Poly, exponent: int, p: int) -> Poly:
    out = [0] * (exponent * (len(poly) - 1) + 1)
    for degree, coefficient in enumerate(poly):
        out[exponent * degree] = coefficient % p
    return trim(out, p)


def power_map_fibers(p: int, ell: int) -> dict[int, list[int]]:
    require((p - 1) % ell == 0, "ell must divide p-1")
    fibers: dict[int, list[int]] = {}
    for x in range(1, p):
        fibers.setdefault(pow(x, ell, p), []).append(x)
    require(all(len(fiber) == ell for fiber in fibers.values()), "unexpected fiber size")
    return {key: sorted(value) for key, value in sorted(fibers.items())}


def pullback_case(p: int, ell: int, m: int, petal_count_m: int) -> dict[str, Any]:
    """Replay pma_pullback_lists over F_p^* for x -> x^ell."""

    fibers = power_map_fibers(p, ell)
    require(petal_count_m <= len(fibers), "not enough quotient fibers")
    alphas = list(fibers)[:petal_count_m]
    selected_fibers = {alpha: fibers[alpha] for alpha in alphas}

    # H(Y)=Y^m.  For S of size m+1,
    # G_S(Y)=YH(Y)-prod_{alpha in S}(Y-alpha), so the leading term cancels.
    h_poly: Poly = tuple([0] * m + [1])
    y_h_poly: Poly = tuple([0] * (m + 1) + [1])
    subset_size = m + 1
    degree_d = m * ell
    agreement_a = subset_size * ell
    domain_size = petal_count_m * ell

    seen_w: set[Poly] = set()
    examples: list[dict[str, Any]] = []
    agreement_histogram: Counter[int] = Counter()
    max_degree = -1

    for subset in combinations(alphas, subset_size):
        product_poly = quotient_locator(subset, p)
        g_poly = poly_sub(y_h_poly, product_poly, p)
        require(len(g_poly) - 1 <= m, "leading terms did not cancel")
        w_poly = compose_x_power(g_poly, ell, p)
        max_degree = max(max_degree, len(w_poly) - 1)
        require(len(w_poly) - 1 <= degree_d, "pullback word exceeds degree d")

        agreements = 0
        agreement_alphas = []
        for alpha in alphas:
            target = alpha * poly_eval(h_poly, alpha, p) % p
            fiber_agreements = sum(
                1 for x in selected_fibers[alpha] if poly_eval(w_poly, x, p) == target
            )
            if fiber_agreements:
                agreement_alphas.append(alpha)
            agreements += fiber_agreements
        require(agreements == agreement_a, "wrong pullback agreement count")
        require(set(agreement_alphas) == set(subset), "agreement fibers differ from S")
        seen_w.add(w_poly)
        agreement_histogram[agreements] += 1
        if len(examples) < 5:
            examples.append(
                {
                    "quotient_subset_S": list(subset),
                    "G_S_coefficients_low_to_high": list(g_poly),
                    "W_S_coefficients_low_to_high": list(w_poly),
                    "agreement_fibers": agreement_alphas,
                    "agreement_points": agreements,
                }
            )

    expected_count = math.comb(petal_count_m, subset_size)
    require(len(seen_w) == expected_count, "pullback members are not distinct")
    sub_johnson = agreement_a * agreement_a < domain_size * degree_d
    require(sub_johnson == (subset_size * subset_size < petal_count_m * m), "sub-Johnson formula mismatch")

    return {
        "field": f"F_{p}",
        "map": f"x -> x^{ell}",
        "fiber_size_ell": ell,
        "quotient_fiber_count_M": petal_count_m,
        "m": m,
        "defect_degree_d": degree_d,
        "agreement_a": agreement_a,
        "domain_size": domain_size,
        "sub_johnson": sub_johnson,
        "sub_johnson_formula": f"({subset_size})^2 < {petal_count_m}*{m}",
        "pullback_member_count": len(seen_w),
        "pullback_member_count_formula": f"binom({petal_count_m}, {subset_size})",
        "profile_charge_count": expected_count,
        "max_W_degree": max_degree,
        "agreement_histogram": {str(key): agreement_histogram[key] for key in sorted(agreement_histogram)},
        "examples": examples,
    }


def cyclic_order(n: int, step: int) -> list[int]:
    if step == 0:
        return list(range(n))
    require(math.gcd(step, n) == 1, "cyclic layout step must be coprime to n")
    return [(step * idx) % n for idx in range(n)]


def shuffled_order(n: int, seed: int) -> list[int]:
    out = list(range(n))
    random.Random(seed).shuffle(out)
    return out


def layout_order(n: int, mode: str) -> list[int]:
    if mode.startswith("cyclic_step_"):
        return cyclic_order(n, int(mode.rsplit("_", 1)[1]))
    if mode.startswith("shuffle_"):
        return shuffled_order(n, int(mode.rsplit("_", 1)[1]))
    raise ValueError(mode)


def e15_petals(cell: dict[str, Any]) -> list[frozenset[int]]:
    ell = cell["sigma"] + 1
    order = layout_order(cell["n"], cell["layout"])
    rest = order[cell["k"] - 1 :]
    return [
        frozenset(rest[idx * ell : (idx + 1) * ell])
        for idx in range(cell["petal_count_M"])
    ]


def power_partitions_on_exponents(n: int, fiber_size: int) -> list[set[frozenset[int]]]:
    partitions = []
    for exponent in range(1, n):
        if math.gcd(exponent, n) != fiber_size:
            continue
        fibers: dict[int, set[int]] = {}
        for idx in range(n):
            fibers.setdefault((exponent * idx) % n, set()).add(idx)
        if all(len(fiber) == fiber_size for fiber in fibers.values()):
            partitions.append({frozenset(fiber) for fiber in fibers.values()})
    return partitions


def petals_are_quotient_fibers(cell: dict[str, Any]) -> bool:
    petals = set(e15_petals(cell))
    for partition in power_partitions_on_exponents(cell["n"], cell["sigma"] + 1):
        if petals <= partition:
            return True
    return False


def analyze_e15_certificate(e15: dict[str, Any]) -> dict[str, Any]:
    summary = e15["summary"]
    require(e15["schema"] == "e15-worst-word-challenge-v1", "E15 schema drift")
    require(e15["status"] == "EXPERIMENTAL_AUDIT", "E15 status drift")
    require(summary["exact_n16_sigma_one_beating_cell_count"] == 12, "E15 sigma=1 count drift")
    require(summary["exact_n16_sigma_ge_two_beating_cell_count"] == 0, "E15 sigma>=2 count drift")

    class_counts: Counter[str] = Counter()
    nonplanted_cells = []
    quotient_fiber_compatible = []
    for cell in e15["cells"]:
        if cell["kind"] != "exact_all_agreement_sets" or not cell.get("nonplanted_count", 0):
            continue
        nonplanted = {
            key: value for key, value in cell["class_counts"].items() if key != "planted"
        }
        class_counts.update(nonplanted)
        compatible = petals_are_quotient_fibers(cell)
        if compatible:
            quotient_fiber_compatible.append(cell)
        nonplanted_cells.append(
            {
                "n": cell["n"],
                "k": cell["k"],
                "sigma": cell["sigma"],
                "layout": cell["layout"],
                "scalar_mode": cell["scalar_mode"],
                "nonplanted_count": cell["nonplanted_count"],
                "nonplanted_class_counts": dict(sorted(nonplanted.items())),
                "petals_are_power_map_quotient_fibers": compatible,
            }
        )

    require(sum(class_counts.values()) == summary["total_exact_n16_nonplanted_count"], "E15 class total drift")
    require(class_counts["mixed_petal"] > class_counts["full_petal"], "E15 dominant class drift")
    require(not quotient_fiber_compatible, "E15 challenger unexpectedly has quotient-fiber petals")

    return {
        "source_summary": summary,
        "exact_nonplanted_class_counts": {key: class_counts[key] for key in sorted(class_counts)},
        "nonplanted_exact_cell_count": len(nonplanted_cells),
        "quotient_fiber_compatible_cell_count": len(quotient_fiber_compatible),
        "verdict": (
            "E15 challenger is not an instance of the pma_pullback_lists quotient-pullback family: "
            "the dominant extras are mixed-petal, and no nonplanted exact cell has petals equal "
            "to fibers of a power-map quotient on the cyclic subgroup."
        ),
        "caveat": (
            "The full_petal examples are pattern-compatible with whole-petal phenomena, "
            "but the recorded E15 layouts are not quotient-fiber layouts; they should be priced "
            "as the low-defect/fixed-excess challenger column, not as pma_pullback_lists."
        ),
        "nonplanted_cell_examples": nonplanted_cells[:8],
    }


def validate_source_certificates(pma: dict[str, Any], e15: dict[str, Any]) -> None:
    require(pma["schema"] == "l1-pma-auxiliary-johnson-v1", "PMA schema drift")
    require(
        pma["status"] == "PROVED_COMPILER__CITES_LEMMA_2_AND_THEOREM_J",
        "PMA status drift",
    )
    require("pma_aux_list_reduction" in pma["roadmap_tasks"], "PMA reduction task missing")
    require("pma_johnson_regime" in pma["roadmap_tasks"], "PMA Johnson task missing")
    require(e15["schema"] == "e15-worst-word-challenge-v1", "E15 schema drift")


def build_certificate() -> dict[str, Any]:
    pma = load_json(PMA_CERT)
    e15 = load_json(E15_CERT)
    validate_source_certificates(pma, e15)
    pullback_cases = [
        pullback_case(p=31, ell=2, m=2, petal_count_m=6),
        pullback_case(p=31, ell=3, m=2, petal_count_m=6),
        pullback_case(p=31, ell=5, m=2, petal_count_m=5),
    ]
    e15_analysis = analyze_e15_certificate(e15)

    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": "PACKET_VERIFIED / PULLBACK_CHARGED_TO_PROFILE_BUDGET",
        "task_id": "C-3",
        "dag_nodes": DAG_NODES,
        "source_artifacts": {
            "pma_auxiliary_johnson": {
                "path": str(PMA_CERT.relative_to(ROOT)),
                "sha256": sha256_file(PMA_CERT),
                "status": pma["status"],
            },
            "e15_worst_word_challenge": {
                "path": str(E15_CERT.relative_to(ROOT)),
                "sha256": sha256_file(E15_CERT),
                "status": e15["status"],
            },
        },
        "pullback_strip": {
            "construction": (
                "Choose quotient fibers T_i={x^ell=alpha_i}; set L_D=H(X^ell), "
                "U*(x)=alpha_i H(alpha_i) on T_i, and W_S=G_S(X^ell) with "
                "G_S(Y)=YH(Y)-prod_{i in S}(Y-alpha_i), |S|=m+1."
            ),
            "verified_cases": pullback_cases,
            "charge": (
                "The family is indexed by quotient-fiber subsets S, so its mass is "
                "the quotient-profile cell count binom(M,m+1), not primitive residual mass."
            ),
        },
        "primitive_residual_restatement": {
            "split": "L(D) = L_quotient_pullback union L_lowdef_fixed_excess union L_primitive",
            "charged_strata": {
                "L_quotient_pullback": "charged to dyadic/quotient-profile budget",
                "L_lowdef_fixed_excess": "covered or separately priced by fixed-excess/E15 challenger machinery",
            },
            "remaining_target": (
                "L_primitive contains non-pullback, non-low-defect wide sub-Johnson "
                "auxiliary lists; this is the only PMA wide residual left for a "
                "correlated-target or descent argument."
            ),
        },
        "e15_challenger_test": e15_analysis,
        "summary": {
            "pullback_counterexample_verified_cases": len(pullback_cases),
            "pullback_counts": [
                case["pullback_member_count_formula"] for case in pullback_cases
            ],
            "e15_is_pure_quotient_pullback": False,
            "e15_exact_nonplanted_class_counts": e15_analysis[
                "exact_nonplanted_class_counts"
            ],
            "e15_quotient_fiber_compatible_cell_count": e15_analysis[
                "quotient_fiber_compatible_cell_count"
            ],
        },
        "nonclaims": [
            "does not rerun the full E15 exhaustive/structured search",
            "does not prove the primitive residual polynomial bound",
            "does not update the DAG JSON or SVG on main",
            "does not price the list crossing numerically; it only names the extra E15 column",
        ],
    }
    payload["payload_sha256"] = sha256_json(payload)
    return payload


def check_certificate(path: Path, expected: dict[str, Any]) -> None:
    actual = json.loads(path.read_text(encoding="utf-8"))
    if actual != expected:
        raise AssertionError(f"certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("C-3 pullback-strip packet")
    print(f"status: {certificate['status']}")
    print(
        "pullback cases={pullback_counterexample_verified_cases}; "
        "E15 pure pullback={e15_is_pure_quotient_pullback}; "
        "E15 quotient-fiber compatible cells={e15_quotient_fiber_compatible_cell_count}".format(
            **summary
        )
    )
    print("E15 classes:", summary["e15_exact_nonplanted_class_counts"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        nargs="?",
        const=OUTPUT,
        type=Path,
        help="write deterministic C-3 JSON, optionally to PATH",
    )
    parser.add_argument(
        "--check",
        nargs="?",
        const=OUTPUT,
        type=Path,
        help="check deterministic C-3 JSON, optionally at PATH",
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
