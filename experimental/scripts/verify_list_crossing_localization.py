#!/usr/bin/env python3
"""Replay a finite list-staircase crossing example.

The theorem is elementary monotonicity of the exact list-size staircase.  This
script records a tiny RS example so the endpoint convention and adjacent
crossing arithmetic are machine-checkable.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Any


P = 5
DOMAIN = tuple(range(4))
K = 2
BUDGET = 1
SCHEMA = "list-crossing-localization-v1"
CERTIFICATE = Path(
    "experimental/data/certificates/list-crossing-localization/"
    "list_crossing_localization.json"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def eval_poly(coeffs: tuple[int, ...], x: int) -> int:
    total = 0
    power = 1
    for coeff in coeffs:
        total = (total + coeff * power) % P
        power = (power * x) % P
    return total


def codewords() -> list[tuple[int, ...]]:
    words = []
    for coeffs in itertools.product(range(P), repeat=K):
        words.append(tuple(eval_poly(coeffs, x) for x in DOMAIN))
    require(len(set(words)) == P**K, "evaluation map should be injective")
    return words


def agreement(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(1 for a, b in zip(left, right) if a == b)


def list_staircase() -> list[dict[str, Any]]:
    code = codewords()
    ambient_words = list(itertools.product(range(P), repeat=len(DOMAIN)))
    rows = []
    for a in range(len(DOMAIN) + 1):
        max_list = 0
        witnesses: list[list[int]] = []
        for word in ambient_words:
            indices = [
                index
                for index, codeword in enumerate(code)
                if agreement(word, codeword) >= a
            ]
            if len(indices) > max_list:
                max_list = len(indices)
                witnesses = [list(word)]
            elif len(indices) == max_list and len(witnesses) < 3:
                witnesses.append(list(word))
        rows.append(
            {
                "agreement_at_least": a,
                "closed_radius": len(DOMAIN) - a,
                "max_list_size": max_list,
                "safe_for_budget": max_list <= BUDGET,
                "sample_witness_words": witnesses,
            }
        )
    return rows


def crossing(rows: list[dict[str, Any]]) -> dict[str, Any]:
    safe = [row for row in rows if row["safe_for_budget"]]
    unsafe = [row for row in rows if not row["safe_for_budget"]]
    require(safe, "toy row should have a safe level")
    require(unsafe, "toy row should have an unsafe level")
    first_safe = min(row["agreement_at_least"] for row in safe)
    require(first_safe > 0, "toy first safe should have an unsafe predecessor")
    predecessor = rows[first_safe - 1]
    current = rows[first_safe]
    require(not predecessor["safe_for_budget"], "predecessor should be unsafe")
    require(current["safe_for_budget"], "first safe should be safe")
    return {
        "budget": BUDGET,
        "first_safe_agreement": first_safe,
        "first_safe_closed_radius": len(DOMAIN) - first_safe,
        "adjacent_unsafe_agreement": first_safe - 1,
        "adjacent_unsafe_closed_radius": len(DOMAIN) - first_safe + 1,
        "adjacent_pinning_verified": True,
    }


def build_certificate() -> dict[str, Any]:
    rows = list_staircase()
    for before, after in zip(rows, rows[1:]):
        require(
            before["max_list_size"] >= after["max_list_size"],
            "list staircase must be nonincreasing in agreement",
        )
    return {
        "schema": SCHEMA,
        "status": "PROVED_TOY_REPLAY_FOR_ENDPOINTS",
        "theorem_replayed": (
            "L_C(a)=sup_U |{c in C: agreement(c,U)>=a}| is integer-valued "
            "and nonincreasing in a; if both safe and unsafe levels occur, "
            "the first safe level and its predecessor pin an adjacent crossing."
        ),
        "row": {
            "field": "F_5",
            "domain": list(DOMAIN),
            "n": len(DOMAIN),
            "k": K,
            "code_size": P**K,
            "ambient_word_count": P ** len(DOMAIN),
            "budget": BUDGET,
        },
        "staircase": rows,
        "crossing": crossing(rows),
    }


def check_certificate(path: Path) -> None:
    expected = build_certificate()
    actual = json.loads(path.read_text())
    require(actual == expected, f"certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    print("List crossing localization replay")
    print(f"schema: {certificate['schema']}")
    print("staircase:")
    for row in certificate["staircase"]:
        print(
            "  a>={a}: L={size}, safe={safe}".format(
                a=row["agreement_at_least"],
                size=row["max_list_size"],
                safe=row["safe_for_budget"],
            )
        )
    c = certificate["crossing"]
    print(
        "adjacent crossing: unsafe a={u}, safe a={s}".format(
            u=c["adjacent_unsafe_agreement"],
            s=c["first_safe_agreement"],
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify a toy list-staircase crossing certificate."
    )
    parser.add_argument("--emit", action="store_true", help="write certificate JSON")
    parser.add_argument("--check", type=Path, help="check an existing certificate")
    args = parser.parse_args()

    if args.emit:
        certificate = build_certificate()
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(certificate, indent=2, sort_keys=True))
        print(f"wrote {CERTIFICATE}")
        print_summary(certificate)
        return

    if args.check:
        check_certificate(args.check)
        print(f"checked {args.check}")
        print_summary(build_certificate())
        return

    print_summary(build_certificate())


if __name__ == "__main__":
    main()
