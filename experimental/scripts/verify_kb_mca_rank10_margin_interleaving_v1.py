#!/usr/bin/env python3
"""Exact certificate for the KoalaBear rank-10 margin/interleaving split."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from math import comb, prod
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank10-margin-interleaving-v1/manifest.json"
PARENT = "b67078c7c0254ce9e54e5748634de5133fae98ef"
PACKET_FILES = [
    "agents.md",
    "experimental/agents-log.md",
    "experimental/grande_finale.tex",
    "experimental/notes/thresholds/kb_mca_rank10_margin_interleaving_split_v1.md",
    "experimental/data/certificates/kb-mca-rank10-margin-interleaving-v1/README.md",
    "experimental/scripts/verify_kb_mca_rank10_margin_interleaving_v1.py",
    "experimental/scripts/verify_kb_mca_rank10_margin_interleaving_v1.sage",
    "experimental/campaigns/kb-mca-rank10-margin-interleaving-post-1166/campaign.json",
    "experimental/campaigns/kb-mca-rank10-margin-interleaving-post-1166/00_contract.md",
    "experimental/campaigns/kb-mca-rank10-margin-interleaving-post-1166/01_frontier_map.md",
    "experimental/campaigns/kb-mca-rank10-margin-interleaving-post-1166/02_controls.md",
    "experimental/campaigns/kb-mca-rank10-margin-interleaving-post-1166/03_idea_ledger.csv",
    "experimental/campaigns/kb-mca-rank10-margin-interleaving-post-1166/04_dependency_ledger.csv",
    "experimental/campaigns/kb-mca-rank10-margin-interleaving-post-1166/05_claim_registry.csv",
    "experimental/campaigns/kb-mca-rank10-margin-interleaving-post-1166/06_review_registry.csv",
    "experimental/campaigns/kb-mca-rank10-margin-interleaving-post-1166/reviews/literature_sweep.md",
]


class Reject(ValueError):
    pass


def require(value: bool, message: str) -> None:
    if not value:
        raise Reject(message)


def falling(x: int, length: int) -> int:
    return prod(x - i for i in range(length))


def rising(x: int, length: int) -> int:
    return prod(x + i for i in range(length))


def high_cap(row: dict[str, int], rank: int, threshold: int) -> int:
    n, K, m, w = (row[key] for key in ("n", "K", "m", "w"))
    value = max(
        Fraction(falling(n, rank + 1), m * threshold * rising(w + 1, rank - 1)),
        Fraction(falling(n - K + rank, rank + 1), threshold * rising(w + 1, rank)),
    )
    return value.numerator // value.denominator


def split(row: dict[str, int], rank: int, threshold: int) -> dict[str, Any]:
    n, K, m, w = (row[key] for key in ("n", "K", "m", "w"))
    require(2 <= threshold <= w, "legal threshold")
    agreement = m - threshold + 1
    require(agreement > K, "strict ordinary-list agreement")
    ordinary = comb(n - K + rank, rank) // comb(agreement - K + rank, rank)
    rank_caps = [n // threshold]
    rank_caps.extend(high_cap(row, r, threshold) for r in range(1, rank + 1))
    high = max(rank_caps)
    low = (n - agreement) * ordinary
    total = row["near"] + high + low
    return {
        "threshold": threshold,
        "agreement": agreement,
        "ordinary_list_cap": ordinary,
        "high_cap": high,
        "high_rank": rank_caps.index(high),
        "low_cap": low,
        "total": total,
        "slack": row["budget"] - total,
        "subsquare_over_line_field": ordinary * ordinary < row["p"] ** row["extension_degree"],
        "subsquare_over_base_field": ordinary * ordinary < row["p"],
    }


def scan_summary(row: dict[str, int], rank: int) -> tuple[dict[str, Any], int | None, int, int]:
    best: dict[str, Any] | None = None
    first_paying: int | None = None
    count = 0
    best_multiplicity = 0
    for threshold in range(2, row["w"] + 1):
        item = split(row, rank, threshold)
        if not item["subsquare_over_line_field"]:
            continue
        count += 1
        if first_paying is None and item["total"] <= row["budget"]:
            first_paying = threshold
        if best is None or (item["total"], threshold) < (best["total"], best["threshold"]):
            best = item
            best_multiplicity = 1
        elif item["total"] == best["total"]:
            best_multiplicity += 1
    require(best is not None, "nonempty legal scan")
    return best, first_paying, count, best_multiplicity


def star_fixture() -> dict[str, Any]:
    p, n, K, m = 11, 10, 1, 3
    core = [0, 1]
    slopes = list(range(8))
    r0 = [0, 0] + [(-gamma) % p for gamma in slopes]
    r1 = [0, 0] + [1] * len(slopes)
    supports = [core + [2 + gamma] for gamma in slopes]
    for gamma, support in zip(slopes, supports):
        agreements = [i for i in range(n) if (r0[i] + gamma * r1[i]) % p == 0]
        require(agreements == support, "exact maximal support")
        require(len({r0[i] for i in support}) > 1 or len({r1[i] for i in support}) > 1,
                "pair noncontainment")
        word = [(r0[i] + gamma * r1[i]) % p for i in range(n)]
        max_constant_agreement = max(word.count(value) for value in range(p))
        require(n - max_constant_agreement > m - K, "post-near")
    agreement = m - 2 + 1
    require(len(slopes) == n - agreement, "sharp n-A multiplicity")
    return {
        "field": p,
        "n": n,
        "K": K,
        "m": m,
        "threshold": 2,
        "common_pair": [0, 0],
        "common_core_size": len(core),
        "owners": len(slopes),
        "n_minus_A": n - agreement,
        "support_digest": hashlib.sha256(json.dumps(supports, separators=(",", ":")).encode()).hexdigest(),
    }


def build() -> dict[str, Any]:
    row = {
        "p": 2130706433,
        "extension_degree": 6,
        "n": 2097152,
        "K": 1048576,
        "m": 1116048,
        "w": 67472,
        "near": 134944,
        "budget": 274980728111395087,
    }
    summaries = {rank: scan_summary(row, rank) for rank in range(9, 13)}
    optima = {rank: summary[0] for rank, summary in summaries.items()}
    require(summaries[9][1] == 16, "first paying threshold")
    require(summaries[9][3] == 1, "unique rank-nine optimum")
    expected = {
        9: (667, 61871313426765543),
        10: (876, 1040506078215897711),
        11: (1146, 18020673627684167414),
        12: (1487, 323734765765217100200),
    }
    require({rank: (item["threshold"], item["total"]) for rank, item in optima.items()} == expected,
            "rank optima")
    optimum = optima[9]
    require(optimum["agreement"] == 1115382, "agreement")
    require(optimum["ordinary_list_cap"] == 57781140652, "ordinary cap")
    require(optimum["high_cap"] == 5143522968716559, "high cap")
    require(optimum["low_cap"] == 56727790457914040, "low cap")
    require(optimum["slack"] == 213109414684629544, "slack")
    require(optimum["subsquare_over_line_field"] and not optimum["subsquare_over_base_field"],
            "field-of-definition guard")
    return {
        "schema": "kb-mca-rank10-margin-interleaving-v1",
        "parent": PARENT,
        "row": row,
        "formula": "2w+max_{0<=j<=s}H_j(T)+(n-m+T-1)M_s(T)",
        "first_paying_threshold_rank9": summaries[9][1],
        "optima": {str(rank): item for rank, item in optima.items()},
        "neighbor_totals_rank9": {
            "666": split(row, 9, 666)["total"],
            "668": split(row, 9, 668)["total"],
        },
        "star_multiplicity_control": star_fixture(),
        "claims": {
            "error_rank_10": "PAID",
            "error_rank_11_or_more": "UNPAID_BY_THIS_FORMULA",
            "active_v4_ledger_movement": 0,
            "KoalaBear_closed": False,
        },
        "scan_counts": {str(rank): summary[2] for rank, summary in summaries.items()},
        "provenance": {
            "repository": "przchojecki/rs-mca",
            "exact_pr1166_parent": PARENT,
            "public_dag_candidate": "c2c37ceb81f2512736f82d619a3a0e63e4156482",
            "exa_sources_reviewed": 20,
            "load_bearing_external_lemma": False,
            "wolfram_exact_T667_replay": True,
        },
        "packet_files": PACKET_FILES,
        "packet_file_sha256": {
            path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            for path in PACKET_FILES
        },
    }


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def payload(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical(unsigned)).hexdigest()


def validate(value: dict[str, Any], expected: dict[str, Any]) -> None:
    require(value == expected, "canonical certificate")
    require(value["payload_sha256"] == payload(value), "payload hash")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if args.write:
        value = build()
        value["payload_sha256"] = payload(value)
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(value, indent=2) + "\n")
        print(f"WROTE {MANIFEST}")
        return
    actual = json.loads(MANIFEST.read_text())
    expected = build()
    expected["payload_sha256"] = payload(expected)
    validate(actual, expected)
    if args.tamper_selftest:
        mutations = [
            ("first_paying_threshold_rank9", 17),
            ("formula", "WRONG"),
        ]
        caught = 0
        for key, replacement in mutations:
            changed = copy.deepcopy(actual)
            changed[key] = replacement
            changed["payload_sha256"] = payload(changed)
            try:
                validate(changed, expected)
            except Reject:
                caught += 1
        changed = copy.deepcopy(actual)
        changed["claims"]["KoalaBear_closed"] = True
        changed["payload_sha256"] = payload(changed)
        try:
            validate(changed, expected)
        except Reject:
            caught += 1
        require(caught == 3, "mutations caught")
        print(f"KB_MCA_RANK10_MARGIN_INTERLEAVING_TAMPER_PASS mutations={caught}/3")
        return
    optimum = actual["optima"]["9"]
    print(
        "KB_MCA_RANK10_MARGIN_INTERLEAVING_PASS "
        f"T={optimum['threshold']} total={optimum['total']} slack={optimum['slack']} "
        f"payload_sha256={actual['payload_sha256']}"
    )


if __name__ == "__main__":
    main()
