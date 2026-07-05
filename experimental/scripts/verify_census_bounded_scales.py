#!/usr/bin/env python3
"""Replay the census bounded-scales packet."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "census_bounded_scales.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "census-bounded-scales"
    / "census_bounded_scales.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "census_bounded_scales",
    "forced_ratio": "l'/N' = j/n",
    "exact_binomial": "Q(N') = binom(N', l')",
    "row_uniform": "row-length",
    "non_claim": "does not by itself decide the pointwise safe or unsafe row inequalities",
}


def entropy(x: float) -> float:
    if x <= 0 or x >= 1:
        return 0.0
    return -(x * math.log2(x) + (1 - x) * math.log2(1 - x))


def pow2_scales(n: int, t: int) -> list[int]:
    out = []
    m = 1
    while m <= n:
        if n % m == 0 and m > t:
            out.append(n // m)
        m *= 2
    return sorted(set(out))


def count_at_scale(nprime: int, ratio: float) -> tuple[int, int]:
    selected = round(ratio * nprime)
    return math.comb(nprime, selected), selected


def row_deciding_data(n: int, k: int, agreement: int) -> dict[str, object]:
    t = agreement - k
    j = n - agreement
    ratio = Fraction(j, n)
    substantive = []
    for nprime in pow2_scales(n, t):
        count, selected = count_at_scale(nprime, float(ratio))
        if 0 < selected < nprime and count > 1:
            substantive.append(
                {
                    "Nprime": nprime,
                    "selected": selected,
                    "log2_count": round(math.log2(count), 6),
                }
            )
    if not substantive:
        raise AssertionError("no substantive scales")
    top = substantive[-1]
    top_gap = (
        top["log2_count"] - substantive[-2]["log2_count"]
        if len(substantive) >= 2
        else float("inf")
    )
    return {
        "n": n,
        "k": k,
        "agreement": agreement,
        "t": t,
        "j": j,
        "ratio": f"{ratio.numerator}/{ratio.denominator}",
        "substantive_scales": substantive,
        "strictly_increasing": all(
            left["log2_count"] < right["log2_count"]
            for left, right in zip(substantive, substantive[1:])
        ),
        "deciding_scale": top["Nprime"],
        "deciding_selected": top["selected"],
        "deciding_log2_count": top["log2_count"],
        "top_gap_bits": round(top_gap, 6),
        "top_gap_large": top_gap >= 30,
    }


def toy_check() -> dict[str, object]:
    entropy_bound = entropy(0.40)
    row_specs = [
        ("RowC 1/4", 2**10, 2**8, 261),
        ("prize 1/4", 2**41, 2**39, 558345748481),
        ("RowC 1/8", 2**10, 2**7, 133),
        ("prize 1/8", 2**41, 2**38, 283467841537),
        ("RowC 1/16", 2**10, 2**6, 67),
        ("prize 1/16", 2**41, 2**37, 141733920769),
    ]
    rows = {name: row_deciding_data(n, k, agreement) for name, n, k, agreement in row_specs}
    invariance = {}
    for rate in ["1/4", "1/8", "1/16"]:
        left = rows[f"RowC {rate}"]
        right = rows[f"prize {rate}"]
        invariance[rate] = {
            "same_deciding_scale": left["deciding_scale"] == right["deciding_scale"],
            "same_selected_count": left["deciding_selected"] == right["deciding_selected"],
            "same_log2_count": left["deciding_log2_count"] == right["deciding_log2_count"],
        }
    return {
        "entropy_H_0_40": round(entropy_bound, 8),
        "entropy_bound_holds": entropy_bound >= 0.97,
        "rows": rows,
        "all_rows_strictly_increasing": all(row["strictly_increasing"] for row in rows.values()),
        "all_rows_large_top_gap": all(row["top_gap_large"] for row in rows.values()),
        "row_length_invariance": invariance,
        "all_invariance_checks_hold": all(
            all(checks.values()) for checks in invariance.values()
        ),
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "census-bounded-scales-v1",
        "status": "PROVED",
        "source_dag_node": "census_bounded_scales",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not decide pointwise safe inequalities",
            "does not decide pointwise unsafe inequalities",
            "does not replace exact counting at the deciding scale",
        ],
        "note": "experimental/notes/thresholds/census_bounded_scales.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "census-bounded-scales-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    toy = cert["toy_check"]
    if not isinstance(toy, dict):
        raise AssertionError("missing toy check")
    for key in [
        "entropy_bound_holds",
        "all_rows_strictly_increasing",
        "all_rows_large_top_gap",
        "all_invariance_checks_hold",
    ]:
        if not toy.get(key):
            raise AssertionError(f"failed toy check: {key}")


def assert_same(expected: dict[str, object], actual: dict[str, object]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(REPO)}")
    if args.check:
        actual = json.loads(args.check.read_text(encoding="utf-8"))
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print(f"{cert['status']}: {cert['source_dag_node']}")


if __name__ == "__main__":
    main()
