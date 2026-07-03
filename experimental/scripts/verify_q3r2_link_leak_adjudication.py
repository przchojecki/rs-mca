#!/usr/bin/env python3
"""Verify the Q3R.2 adjudication of #209 link-leak candidates.

The source packet `verify_xr_pair_orbit_globalness.py` reports ten
post-quotient-strip rows whose small fixed-core links are dense.  This checker
does not rerun the sampled n=32 telemetry.  It rebuilds only the exact
F_97, n=16, j=8, t=2 corpus, computes the finite slope attached to each
aligned support, and applies the local T2 tangent-overlap strip:

    a same-slope (j-1)-core bucket with at least two completions is paid.

After that strip, it checks the residual number of completions above every
(j-1)-core.  Max residual core count <= 1 is safe for the first-unpaid
L_tan=1 convention.  Max residual core count <= 2 is safe for the
residual-edge L_tan=2 convention.  Anything above 2 would be a genuine unpaid
tangent leak for the Q3R.2 gate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any

import verify_xr_pair_orbit_globalness as xr


ROOT = Path(__file__).resolve().parents[2]
SOURCE_CERTIFICATE = ROOT / (
    "experimental/data/certificates/xr-pair-orbit-globalness/"
    "xr_pair_orbit_globalness.json"
)
OUTPUT = ROOT / (
    "experimental/data/certificates/q3r2-link-leak-adjudication/"
    "q3r2_link_leak_adjudication.json"
)

SCHEMA_VERSION = "q3r2-link-leak-adjudication-v1"
LTAN_FIRST_UNPAID = 1
LTAN_RESIDUAL_EDGE = 2

EXPECTED_CANDIDATES: dict[str, dict[str, Any]] = {
    "delta_character_13": {
        "aligned_count": 6537,
        "slope_count": 57,
        "t2_paid_support_count": 6456,
        "residual_support_count": 81,
        "residual_max_j_minus_1_core_count": 1,
        "verdict": "strippable_tangent_ltan1",
    },
    "delta_character_10": {
        "aligned_count": 6537,
        "slope_count": 57,
        "t2_paid_support_count": 6456,
        "residual_support_count": 81,
        "residual_max_j_minus_1_core_count": 1,
        "verdict": "strippable_tangent_ltan1",
    },
    "delta_character_9": {
        "aligned_count": 6510,
        "slope_count": 46,
        "t2_paid_support_count": 6456,
        "residual_support_count": 54,
        "residual_max_j_minus_1_core_count": 1,
        "verdict": "strippable_tangent_ltan1",
    },
    "delta_character_14": {
        "aligned_count": 6510,
        "slope_count": 46,
        "t2_paid_support_count": 6456,
        "residual_support_count": 54,
        "residual_max_j_minus_1_core_count": 1,
        "verdict": "strippable_tangent_ltan1",
    },
    "delta_character_8": {
        "aligned_count": 6471,
        "slope_count": 33,
        "t2_paid_support_count": 6435,
        "residual_support_count": 36,
        "residual_max_j_minus_1_core_count": 1,
        "verdict": "strippable_tangent_ltan1",
    },
    "delta_character_15": {
        "aligned_count": 6471,
        "slope_count": 33,
        "t2_paid_support_count": 6435,
        "residual_support_count": 36,
        "residual_max_j_minus_1_core_count": 1,
        "verdict": "strippable_tangent_ltan1",
    },
    "delta_character_12": {
        "aligned_count": 6524,
        "slope_count": 46,
        "t2_paid_support_count": 6470,
        "residual_support_count": 54,
        "residual_max_j_minus_1_core_count": 1,
        "verdict": "strippable_tangent_ltan1",
    },
    "delta_character_11": {
        "aligned_count": 6524,
        "slope_count": 46,
        "t2_paid_support_count": 6470,
        "residual_support_count": 54,
        "residual_max_j_minus_1_core_count": 1,
        "verdict": "strippable_tangent_ltan1",
    },
    "character_pair_9_13": {
        "aligned_count": 2048,
        "slope_count": 20,
        "t2_paid_support_count": 1968,
        "residual_support_count": 80,
        "residual_max_j_minus_1_core_count": 2,
        "verdict": "strippable_residual_edge_ltan2",
    },
    "character_pair_10_14": {
        "aligned_count": 2048,
        "slope_count": 20,
        "t2_paid_support_count": 1968,
        "residual_support_count": 80,
        "residual_max_j_minus_1_core_count": 2,
        "verdict": "strippable_residual_edge_ltan2",
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def fraction_record(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "float": float(value),
    }


def load_source_certificate() -> dict[str, Any]:
    source = json.loads(SOURCE_CERTIFICATE.read_text(encoding="utf-8"))
    case = source["exact_n16"]["case"]
    require(case["field"] == "F_97", "unexpected source field")
    require(case["n"] == 16, "unexpected source n")
    require(case["j"] == 8, "unexpected source j")
    require(case["window_t"] == 2, "unexpected source t")
    link_leaks = source["exact_n16"]["link_leaks"]
    require(
        [row["pair_id"] for row in link_leaks] == list(EXPECTED_CANDIDATES),
        "source link-leak candidate order changed",
    )
    require(
        all(row["classification"] == "post_strip_tangent_link_leak_candidate" for row in link_leaks),
        "source candidate classification changed",
    )
    require(
        all(not row["kllm_proxy_leaking_radii"] for row in link_leaks),
        "source KLLM proxy leak status changed",
    )
    return source


def support_slope(
    case: xr.JohnsonCase,
    syndromes_u: tuple[int, ...],
    syndromes_v: tuple[int, ...],
    locator: tuple[int, ...],
) -> int:
    a = xr.hankel_product(syndromes_u, locator, case.t, case.p)
    b = xr.hankel_product(syndromes_v, locator, case.t, case.p)
    require(any(entry % case.p for entry in b), "inactive v-vector reached slope extraction")
    require(
        all(
            (a[row] * b[col] - a[col] * b[row]) % case.p == 0
            for row in range(case.t)
            for col in range(row + 1, case.t)
        ),
        "non-parallel support reached slope extraction",
    )
    for a_entry, b_entry in zip(a, b):
        if b_entry % case.p:
            return (-a_entry * pow(b_entry, -1, case.p)) % case.p
    raise AssertionError("unreachable slope extraction branch")


def residual_link_summary(
    case: xr.JohnsonCase,
    residual_indices: list[int],
    radius: int,
) -> dict[str, Any]:
    counts: Counter[tuple[int, ...]] = Counter()
    for index in residual_indices:
        counts.update(combinations(case.vertices[index], radius))
    link_size = math.comb(case.n - radius, case.j - radius)
    if not counts:
        return {
            "r": radius,
            "max_count": 0,
            "link_size": link_size,
            "max_link_density": fraction_record(Fraction(0, 1)),
            "max_core": [],
        }
    max_core, max_count = max(counts.items(), key=lambda item: (item[1], item[0]))
    return {
        "r": radius,
        "max_count": max_count,
        "link_size": link_size,
        "max_link_density": fraction_record(Fraction(max_count, link_size)),
        "max_core": list(max_core),
    }


def verdict(max_residual_core_count: int) -> str:
    if max_residual_core_count <= LTAN_FIRST_UNPAID:
        return "strippable_tangent_ltan1"
    if max_residual_core_count <= LTAN_RESIDUAL_EDGE:
        return "strippable_residual_edge_ltan2"
    return "genuine_unpaid_tangent_leak"


def summarize_candidate(
    case: xr.JohnsonCase,
    pair: dict[str, Any],
    leak_row: dict[str, Any],
) -> dict[str, Any]:
    aligned = xr.aligned_indices(case, pair)
    upto = case.j + case.t - 1
    syndromes_u = xr.word_syndromes(pair["u"], case.points, upto, case.p)
    syndromes_v = xr.word_syndromes(pair["v"], case.points, upto, case.p)
    slopes = {
        index: support_slope(case, syndromes_u, syndromes_v, case.locators[index])
        for index in aligned
    }

    same_slope_core_buckets: defaultdict[tuple[tuple[int, ...], int], list[int]] = defaultdict(list)
    for index in aligned:
        support = case.vertices[index]
        slope = slopes[index]
        for removed in support:
            core = tuple(value for value in support if value != removed)
            same_slope_core_buckets[(core, slope)].append(index)

    t2_paid = set()
    bucket_size_histogram: Counter[int] = Counter()
    for bucket in same_slope_core_buckets.values():
        unique_bucket = set(bucket)
        bucket_size_histogram[len(unique_bucket)] += 1
        if len(unique_bucket) >= 2:
            t2_paid.update(unique_bucket)

    residual = [index for index in aligned if index not in t2_paid]
    residual_j_minus_1_counts: Counter[tuple[int, ...]] = Counter()
    for index in residual:
        support = case.vertices[index]
        for removed in support:
            core = tuple(value for value in support if value != removed)
            residual_j_minus_1_counts[core] += 1

    max_residual_core_count = max(residual_j_minus_1_counts.values(), default=0)
    result = {
        "pair_id": pair["pair_id"],
        "family": pair["family"],
        "parameters": pair["parameters"],
        "source_paid_tangent_proxy_radii": leak_row["paid_tangent_proxy_leaking_radii"],
        "source_kllm_proxy_radii": leak_row["kllm_proxy_leaking_radii"],
        "aligned_count": len(aligned),
        "slope_count": len(set(slopes.values())),
        "same_slope_core_bucket_size_histogram": [
            {"bucket_size": size, "bucket_count": count}
            for size, count in sorted(bucket_size_histogram.items())
        ],
        "t2_paid_support_count": len(t2_paid),
        "residual_support_count": len(residual),
        "residual_max_j_minus_1_core_count": max_residual_core_count,
        "residual_ltan1_ok": max_residual_core_count <= LTAN_FIRST_UNPAID,
        "residual_ltan2_ok": max_residual_core_count <= LTAN_RESIDUAL_EDGE,
        "verdict": verdict(max_residual_core_count),
        "residual_link_maxima": [
            residual_link_summary(case, residual, radius)
            for radius in (1, 2, 3, 4, case.j - 1)
        ],
    }

    expected = EXPECTED_CANDIDATES[pair["pair_id"]]
    for key, expected_value in expected.items():
        require(result[key] == expected_value, f"{pair['pair_id']} drifted at {key}")
    return result


def build_certificate() -> dict[str, Any]:
    source = load_source_certificate()
    case = xr.JohnsonCase(n=16, j=8)
    pairs = {pair["pair_id"]: pair for pair in xr.pair_corpus(case, xr.N16_RANDOM_PAIRS)}
    leaks = source["exact_n16"]["link_leaks"]
    candidates = [
        summarize_candidate(case, pairs[leak["pair_id"]], leak)
        for leak in leaks
    ]

    verdict_counts = Counter(row["verdict"] for row in candidates)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / EXACT_N16_CORPUS_ADJUDICATION",
        "campaign_id": "C-1",
        "dag_nodes": ["xr_globalness_from_ledger", "Q3R.2"],
        "source": {
            "certificate": str(SOURCE_CERTIFICATE.relative_to(ROOT)),
            "source_schema_version": source["schema_version"],
            "source_payload_sha256": source["payload_sha256"],
            "case": source["exact_n16"]["case"],
            "source_link_leak_count": len(leaks),
        },
        "ltan_conventions": {
            "first_unpaid": LTAN_FIRST_UNPAID,
            "residual_edge": LTAN_RESIDUAL_EDGE,
            "t2_strip_rule": (
                "same-slope (j-1)-core buckets with at least two completions "
                "are charged to T2 paid:tangent"
            ),
        },
        "summary": {
            "candidate_count": len(candidates),
            "verdict_counts": dict(sorted(verdict_counts.items())),
            "ltan1_safe_candidate_count": sum(row["residual_ltan1_ok"] for row in candidates),
            "ltan2_safe_candidate_count": sum(row["residual_ltan2_ok"] for row in candidates),
            "genuine_unpaid_tangent_leak_count_ltan2": sum(
                not row["residual_ltan2_ok"] for row in candidates
            ),
            "all_candidates_strippable_under_residual_edge_ltan2": all(
                row["residual_ltan2_ok"] for row in candidates
            ),
            "convention_sensitive_ltan1_pair_ids": [
                row["pair_id"]
                for row in candidates
                if row["residual_ltan2_ok"] and not row["residual_ltan1_ok"]
            ],
        },
        "candidates": candidates,
        "nonclaims": [
            "does not enumerate all projective word pairs over F_97",
            "does not rerun or adjudicate the sampled n=32 telemetry",
            "does not prove the imported KLLM globalness constants",
            "does not prove the full c_xr_content classification",
        ],
    }
    require(len(candidates) == 10, "candidate count changed")
    require(
        payload["summary"]["genuine_unpaid_tangent_leak_count_ltan2"] == 0,
        "found a residual-edge L_tan=2 leak",
    )
    require(
        payload["summary"]["convention_sensitive_ltan1_pair_ids"]
        == ["character_pair_9_13", "character_pair_10_14"],
        "L_tan=1 convention-sensitive rows changed",
    )
    payload["payload_sha256"] = sha256_json(payload)
    return payload


def check_certificate(path: Path, expected: dict[str, Any]) -> None:
    actual = json.loads(path.read_text(encoding="utf-8"))
    if actual != expected:
        raise AssertionError(f"certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("Q3R.2 link-leak adjudication")
    print(f"status: {certificate['status']}")
    print(
        "candidates={candidate_count}, L_tan=1 safe={ltan1_safe_candidate_count}, "
        "L_tan=2 safe={ltan2_safe_candidate_count}, genuine L_tan=2 leaks="
        "{genuine_unpaid_tangent_leak_count_ltan2}".format(**summary)
    )
    print(
        "L_tan=1 convention-sensitive:",
        ", ".join(summary["convention_sensitive_ltan1_pair_ids"]) or "none",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        nargs="?",
        const=OUTPUT,
        type=Path,
        help="write deterministic adjudication JSON, optionally to PATH",
    )
    parser.add_argument(
        "--check",
        nargs="?",
        const=OUTPUT,
        type=Path,
        help="check deterministic adjudication JSON, optionally at PATH",
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
