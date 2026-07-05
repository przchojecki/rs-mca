#!/usr/bin/env python3
"""Direct finite test of the mode-at-null prefix-fiber statement.

Status: EXPERIMENTAL.  The default packet enumerates all m-subsets of small
multiplicative subgroups and records the exact prefix-fiber histogram
N_w(z) for the signed elementary-symmetric prefix map Phi_w.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any


STATUS = "EXPERIMENTAL"
THEOREM_PROBLEM_ID = "prob:band; Q3 mode-at-null; Phi_w prefix fibers"
SCHEMA_VERSION = "mode-at-null-direct-v2"
DEFAULT_OUTPUT = Path(
    "experimental/data/certificates/mode-at-null-direct/mode_at_null_direct.json"
)
ROWS = (
    (5, 4, 2, 2),
    (5, 4, 2, 3),
    (7, 6, 3, 2),
    (7, 6, 3, 3),
    (11, 10, 5, 2),
    (11, 10, 5, 3),
    (13, 12, 6, 2),
    (13, 12, 6, 3),
    (17, 16, 8, 2),
    (17, 16, 8, 3),
    (17, 16, 6, 2),
    (17, 16, 10, 2),
)
STRATEGY_KAPPA_BAND = (Fraction(43, 5), Fraction(45, 1))


def primitive_root(p: int) -> int:
    factors: list[int] = []
    value = p - 1
    d = 2
    while d * d <= value:
        if value % d == 0:
            factors.append(d)
            while value % d == 0:
                value //= d
        d += 1 if d == 2 else 2
    if value > 1:
        factors.append(value)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root for F_{p}")


def subgroup(p: int, n: int) -> tuple[int, ...]:
    if (p - 1) % n:
        raise ValueError("n must divide p-1")
    omega = pow(primitive_root(p), (p - 1) // n, p)
    values = tuple(pow(omega, index, p) for index in range(n))
    if len(set(values)) != n:
        raise AssertionError("bad multiplicative subgroup")
    return values


def signed_elementary_prefix(values: tuple[int, ...], w: int, p: int) -> tuple[int, ...]:
    elementary = [0] * (w + 1)
    elementary[0] = 1
    for value in values:
        for degree in range(w, 0, -1):
            elementary[degree] = (elementary[degree] + elementary[degree - 1] * value) % p
    return tuple(((-1 if degree % 2 else 1) * elementary[degree]) % p for degree in range(1, w + 1))


def fraction_record(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": f"{value.numerator}/{value.denominator}",
    }


def row_payload(p: int, n: int, m: int, w: int) -> dict[str, Any]:
    domain = subgroup(p, n)
    histogram: Counter[tuple[int, ...]] = Counter()
    for support in itertools.combinations(range(n), m):
        values = tuple(domain[index] for index in support)
        histogram[signed_elementary_prefix(values, w, p)] += 1
    total = comb(n, m)
    zero_prefix = (0,) * w
    null_count = histogram.get(zero_prefix, 0)
    max_count = max(histogram.values())
    strict_margin = max_count - null_count
    zero_realized = null_count > 0
    argmax_prefixes = sorted(prefix for prefix, count in histogram.items() if count == max_count)
    avg = Fraction(total, p**w)
    kappa_null = Fraction(null_count * p**w, total)
    kappa_max = Fraction(max_count * p**w, total)
    mode_holds = max_count <= null_count
    histogram_entries = [
        {"z": list(prefix), "count": count}
        for prefix, count in sorted(histogram.items())
    ]
    top_fibers = [
        {"z": list(prefix), "count": count}
        for prefix, count in sorted(histogram.items(), key=lambda item: (-item[1], item[0]))[:12]
    ]
    return {
        "label": f"f{p}_n{n}_m{m}_w{w}",
        "p": p,
        "q_gen": p,
        "q_line": p,
        "q_chal": p,
        "n": n,
        "m": m,
        "w": w,
        "domain": list(domain),
        "subsets_total": total,
        "realized_fibers": len(histogram),
        "average_fiber_size": fraction_record(avg),
        "zero_prefix": list(zero_prefix),
        "N_w_zero": null_count,
        "z_zero_realized": zero_realized,
        "argmax_count": max_count,
        "strict_margin": strict_margin,
        "argmax_prefixes": [list(prefix) for prefix in argmax_prefixes[:12]],
        "argmax_prefixes_truncated": len(argmax_prefixes) > 12,
        "mode_at_null_holds": mode_holds,
        "kappa_null": fraction_record(kappa_null),
        "kappa_max": fraction_record(kappa_max),
        "kappa_strategy_band": {
            "lower": fraction_record(STRATEGY_KAPPA_BAND[0]),
            "upper": fraction_record(STRATEGY_KAPPA_BAND[1]),
            "kappa_max_in_band": STRATEGY_KAPPA_BAND[0] <= kappa_max <= STRATEGY_KAPPA_BAND[1],
        },
        "failure_witnesses": []
        if mode_holds or not zero_realized
        else [
            {
                "z": list(prefix),
                "N_w_z": max_count,
                "N_w_zero": null_count,
                "excess": max_count - null_count,
            }
            for prefix in argmax_prefixes[:8]
        ],
        "top_fibers": top_fibers,
        "fiber_histogram": histogram_entries,
    }


def payload_hash(payload: dict[str, Any]) -> str:
    clone = {key: value for key, value in payload.items() if key != "payload_sha256"}
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def build_certificate() -> dict[str, Any]:
    rows = [row_payload(*row) for row in ROWS]
    vacuous = [
        {
            "row": row["label"],
            "reason": "zero prefix is not realized",
            "N_w_zero": row["N_w_zero"],
            "argmax_count": row["argmax_count"],
            "strict_margin": row["strict_margin"],
        }
        for row in rows
        if not row["z_zero_realized"]
    ]
    genuine = [
        {
            "row": row["label"],
            "N_w_zero": row["N_w_zero"],
            "argmax_count": row["argmax_count"],
            "strict_margin": row["strict_margin"],
            "witnesses": row["failure_witnesses"],
        }
        for row in rows
        if row["z_zero_realized"] and not row["mode_at_null_holds"]
    ]
    realized = [row for row in rows if row["z_zero_realized"]]
    exact_mode_count = sum(1 for row in realized if row["strict_margin"] == 0)
    one_below_count = sum(1 for row in realized if row["strict_margin"] == 1)
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "proof_status": STATUS,
        "claim": "finite direct tests of whether the all-zero Phi_w fiber is the mode",
        "row_rule": "all m-subsets of mu_n on small prime fields; middle-slice rows plus two realized-null F_17 controls",
        "realized_null_summary": {
            "realized_rows": len(realized),
            "exact_mode_rows": exact_mode_count,
            "one_below_mode_rows": one_below_count,
            "max_strict_margin_on_realized_rows": max((row["strict_margin"] for row in realized), default=0),
        },
        "strategy_kappa_band": {
            "lower": fraction_record(STRATEGY_KAPPA_BAND[0]),
            "upper": fraction_record(STRATEGY_KAPPA_BAND[1]),
        },
        "non_claims": [
            "No asymptotic mode-at-null theorem is claimed.",
            "No resolution of prob:band is claimed.",
            "Vacuous rows with an unrealized zero prefix are not counted as mode-at-null failures.",
            "Strict finite failures are recorded only for the listed realized-null toy rows.",
        ],
        "rows": rows,
        "vacuous_null_rows": vacuous,
        "genuine_strict_failures": genuine,
    }
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-defaults", action="store_true", help="write the default certificate")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.emit_defaults:
        raise SystemExit("nothing requested; use --emit-defaults")
    cert = build_certificate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(cert, indent=2, sort_keys=True))
    else:
        print(
            "mode_at_null_direct: "
            f"status={STATUS} result=PASS rows={len(cert['rows'])} "
            f"vacuous={len(cert['vacuous_null_rows'])} "
            f"strict_failures={len(cert['genuine_strict_failures'])}"
        )
        print(args.output.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
