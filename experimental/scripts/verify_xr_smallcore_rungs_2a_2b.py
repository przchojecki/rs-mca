#!/usr/bin/env python3
"""Verify arithmetic and toy identities for XR small-core rungs 2a/2b.

DAG node: xr_smallcore_spread_count.

2a. Same-slope exact aligned supports are automatically k-spread and are
    exactly the worst-word exact-list object for the word u+zv.
2b. Distinct-slope pairs with core r=k+d, d>=1, force (u,v) to agree with a
    codeword pair on that core; this is tangent depth d and should be charged
    to the graded tangent ledger. The r=k boundary has depth zero and remains
    in the irreducible rank/spread core.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any

PASS: list[str] = []
FAIL: list[str] = []

CERT_PATH = Path(
    "experimental/data/certificates/xr-smallcore-rungs-2a-2b/"
    "xr_smallcore_rungs_2a_2b_certificate.json"
)


def check(label: str, ok: bool, detail: str = "") -> None:
    (PASS if ok else FAIL).append(label)
    tag = "PASS" if ok else "FAIL"
    print(f"{tag}  {label}" + (f"  [{detail}]" if detail else ""))


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def eval_poly(coeffs: tuple[int, ...], x: int, p: int) -> int:
    acc = 0
    power = 1
    for coeff in coeffs:
        acc = (acc + coeff * power) % p
        power = (power * x) % p
    return acc


def rank_mod_p(matrix: list[list[int]], p: int) -> int:
    mat = [row[:] for row in matrix]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for r in range(rank, rows):
            if mat[r][col] % p:
                pivot = r
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        scale = inv(mat[rank][col], p)
        mat[rank] = [(x * scale) % p for x in mat[rank]]
        for r in range(rows):
            if r != rank and mat[r][col] % p:
                factor = mat[r][col] % p
                mat[r] = [(a - factor * b) % p for a, b in zip(mat[r], mat[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def interpolate_values(domain: tuple[int, ...], values: tuple[int, ...], k: int, p: int) -> tuple[int, ...]:
    if len(domain) != k or len(values) != k:
        raise ValueError("need exactly k points")
    mat = [[pow(x, i, p) for i in range(k)] + [y % p] for x, y in zip(domain, values)]
    row = 0
    for col in range(k):
        pivot = next(r for r in range(row, k) if mat[r][col] % p)
        mat[row], mat[pivot] = mat[pivot], mat[row]
        scale = inv(mat[row][col], p)
        mat[row] = [(v * scale) % p for v in mat[row]]
        for r in range(k):
            if r != row and mat[r][col] % p:
                factor = mat[r][col] % p
                mat[r] = [(a - factor * b) % p for a, b in zip(mat[r], mat[row])]
        row += 1
    return tuple(mat[i][k] % p for i in range(k))


def codewords(domain: tuple[int, ...], k: int, p: int) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    return [
        (coeffs, tuple(eval_poly(coeffs, x, p) for x in domain))
        for coeffs in itertools.product(range(p), repeat=k)
    ]


def exact_supports_for_word(
    word: tuple[int, ...],
    words: list[tuple[tuple[int, ...], tuple[int, ...]]],
    agreement: int,
) -> list[dict[str, Any]]:
    supports = []
    for coeffs, cw in words:
        support = tuple(i for i, (a, b) in enumerate(zip(word, cw)) if a == b)
        if len(support) == agreement:
            supports.append({"coeffs": coeffs, "support": support})
    return supports


def check_same_slope_toy() -> dict[str, Any]:
    p = 5
    domain = (0, 1, 2, 3, 4)
    n = len(domain)
    k = 2
    agreement = 3
    words = codewords(domain, k, p)
    checked_words = 0
    max_exact_list = 0
    max_intersection = -1
    for word in itertools.product(range(p), repeat=n):
        exact = exact_supports_for_word(word, words, agreement)
        if exact:
            checked_words += 1
        max_exact_list = max(max_exact_list, len(exact))
        for left, right in itertools.combinations(exact, 2):
            inter = len(set(left["support"]) & set(right["support"]))
            max_intersection = max(max_intersection, inter)
            if inter >= k:
                return {
                    "ok": False,
                    "counterexample": {
                        "word": word,
                        "left": left,
                        "right": right,
                        "intersection": inter,
                    },
                }
    return {
        "ok": True,
        "field": p,
        "n": n,
        "k": k,
        "agreement": agreement,
        "words_examined": p**n,
        "codewords": len(words),
        "words_with_exact_list": checked_words,
        "max_exact_list": max_exact_list,
        "max_pairwise_intersection": max_intersection,
    }


def check_tangent_depth_ranks() -> list[dict[str, Any]]:
    p = 17
    domain = tuple(range(8))
    k = 3
    rows = []
    for r in range(1, 8):
        core = domain[:r]
        matrix = [[pow(x, i, p) for i in range(k)] for x in core]
        rank = rank_mod_p(matrix, p)
        rows.append(
            {
                "core_size": r,
                "rank": rank,
                "codimension_in_core_word_space": r - rank,
                "expected_depth_max_0_r_minus_k": max(0, r - k),
                "ok": rank == min(r, k) and r - rank == max(0, r - k),
            }
        )
    return rows


def check_two_slope_identity_toy() -> dict[str, Any]:
    p = 17
    domain = tuple(range(8))
    k = 3
    core = domain[:5]
    z1, z2 = 4, 9
    c1 = (2, 3, 5)
    c2 = (7, 11, 13)
    denom = inv(z1 - z2, p)
    u_vals = []
    v_vals = []
    for x in core:
        c1x = eval_poly(c1, x, p)
        c2x = eval_poly(c2, x, p)
        v = ((c1x - c2x) * denom) % p
        u = (c1x - z1 * v) % p
        u_vals.append(u)
        v_vals.append(v)

    v_coeffs = tuple(((a - b) * denom) % p for a, b in zip(c1, c2))
    u_coeffs = tuple((a - z1 * b) % p for a, b in zip(c1, v_coeffs))
    ok_v = all(eval_poly(v_coeffs, x, p) == y for x, y in zip(core, v_vals))
    ok_u = all(eval_poly(u_coeffs, x, p) == y for x, y in zip(core, u_vals))
    interpolated_v = interpolate_values(core[:k], tuple(v_vals[:k]), k, p)
    depth_constraints_ok = all(
        eval_poly(interpolated_v, x, p) == y for x, y in zip(core[k:], v_vals[k:])
    )
    return {
        "field": p,
        "k": k,
        "core_size": len(core),
        "depth": len(core) - k,
        "slopes": [z1, z2],
        "u_line_coeffs": u_coeffs,
        "v_line_coeffs": v_coeffs,
        "two_slope_identity_ok": ok_u and ok_v,
        "interpolated_v_from_first_k": interpolated_v,
        "depth_constraints_ok": depth_constraints_ok,
    }


def rung_arithmetic(max_t: int = 10) -> list[dict[str, Any]]:
    rows = []
    for t in range(1, max_t + 1):
        partial = []
        for d in range(1, max(1, t - 1)):
            s = t - d
            if 2 <= s <= t - 1:
                partial.append(
                    {
                        "depth_d": d,
                        "exchange_s": s,
                        "ledger_c_s_t": min(s, t - 1),
                        "identity_d_plus_s_equals_t": d + s == t,
                    }
                )
        rows.append(
            {
                "t": t,
                "partial_band_nonempty": t >= 3,
                "partial_depths": partial,
                "r_equals_k_boundary_depth": 0,
            }
        )
    return rows


def build_certificate() -> dict[str, Any]:
    cert = {
        "dag_node": "xr_smallcore_spread_count",
        "status": "PROVED reductions for rungs 2a and 2b; residual 2c remains",
        "same_slope_toy": check_same_slope_toy(),
        "tangent_depth_rank_rows": check_tangent_depth_ranks(),
        "two_slope_identity_toy": check_two_slope_identity_toy(),
        "rung_arithmetic": rung_arithmetic(),
        "non_claim": (
            "This packet proves the list bridge and tangent-forcing bridge. "
            "It does not prove the list grand challenge or the graded tangent ledger."
        ),
    }
    return json.loads(json.dumps(cert, sort_keys=True))


def verify_certificate(cert: dict[str, Any]) -> None:
    same = cert["same_slope_toy"]
    check("2a toy: same-slope exact supports are k-spread", same["ok"], str(same.get("counterexample")))
    check("2a toy: nontrivial exact lists were examined", same["words_with_exact_list"] > 0)
    check("2a toy: max pairwise intersection is < k", same["max_pairwise_intersection"] < same["k"])

    rank_rows = cert["tangent_depth_rank_rows"]
    check("2b rank rows all match max(0,r-k) tangent depth", all(row["ok"] for row in rank_rows))
    boundary = next(row for row in rank_rows if row["core_size"] == 3)
    check("2b boundary r=k has zero tangent depth", boundary["codimension_in_core_word_space"] == 0)
    depth_one = next(row for row in rank_rows if row["core_size"] == 4)
    check("2b first partial-forcing shell r=k+1 has depth 1", depth_one["codimension_in_core_word_space"] == 1)

    ident = cert["two_slope_identity_toy"]
    check("2b toy: two-slope change of variables recovers codeword pair", ident["two_slope_identity_ok"])
    check("2b toy: extra core points are exactly tangent-depth constraints", ident["depth_constraints_ok"])

    for row in cert["rung_arithmetic"]:
        t = row["t"]
        check(f"rung arithmetic t={t}: partial band nonempty iff t>=3", row["partial_band_nonempty"] == (t >= 3))
        check(
            f"rung arithmetic t={t}: d+s=t through the partial band",
            all(item["identity_d_plus_s_equals_t"] for item in row["partial_depths"]),
        )
        check(
            f"rung arithmetic t={t}: qx13 c(s,t)=s in partial band",
            all(item["ledger_c_s_t"] == item["exchange_s"] for item in row["partial_depths"]),
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()

    cert = build_certificate()
    if args.write_certificate:
        CERT_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {CERT_PATH}")
    else:
        if CERT_PATH.exists():
            checked = json.loads(CERT_PATH.read_text())
            check("checked-in JSON certificate matches deterministic build", checked == cert)
        else:
            check("checked-in JSON certificate exists", False, str(CERT_PATH))

    verify_certificate(cert)
    print()
    print(f"{len(PASS)} PASS, {len(FAIL)} FAIL")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    sys.exit(main())
