#!/usr/bin/env python3
"""Verify the M1 deficiency-one U1-U5 chart chain on exact toy families."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


OUTPUT = Path(
    "experimental/data/certificates/m1-deficiency-one-u1-u5-chain/"
    "m1_deficiency_one_u1_u5_chain.json"
)


@dataclass(frozen=True)
class ToyFamily:
    name: str
    p: int
    u: tuple[int, ...]
    v: tuple[int, ...]


F13 = ToyFamily(
    "F_13 smoke family",
    13,
    (1, 2, 3, 4, 5, 6, 7, 8),
    (8, 1, 5, 2, 9, 3, 7, 4),
)

F97 = ToyFamily(
    "F_97/mu_16 acid-scale family",
    97,
    (3, 17, 58, 91, 26, 44, 10, 73),
    (12, 5, 81, 33, 70, 9, 61, 48),
)


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def is_zero_poly(poly: list[int]) -> bool:
    return all(x == 0 for x in poly)


def poly_eval(poly: list[int], x: int, p: int) -> int:
    acc = 0
    for coeff in reversed(poly):
        acc = (acc * x + coeff) % p
    return acc


def poly_add(a: list[int], b: list[int], p: int) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
    return trim(out)


def poly_sub(a: list[int], b: list[int], p: int) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = ((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p
    return trim(out)


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, av in enumerate(a):
        for j, bv in enumerate(b):
            out[i + j] = (out[i + j] + av * bv) % p
    return trim(out)


def poly_scale(a: list[int], scalar: int, p: int) -> list[int]:
    return trim([(scalar * x) % p for x in a])


def poly_divmod(a: list[int], b: list[int], p: int) -> tuple[list[int], list[int]]:
    a = trim(a[:])
    b = trim(b[:])
    if is_zero_poly(b):
        raise ZeroDivisionError("zero divisor")
    if len(a) < len(b):
        return [0], a
    q = [0] * (len(a) - len(b) + 1)
    lead_inv = inv(b[-1], p)
    while len(a) >= len(b) and not is_zero_poly(a):
        shift = len(a) - len(b)
        coeff = a[-1] * lead_inv % p
        q[shift] = coeff
        for i in range(len(b)):
            a[shift + i] = (a[shift + i] - coeff * b[i]) % p
        trim(a)
    return trim(q), trim(a)


def poly_gcd_monic(a: list[int], b: list[int], p: int) -> list[int]:
    a, b = trim(a[:]), trim(b[:])
    while not is_zero_poly(b):
        _, r = poly_divmod(a, b, p)
        a, b = b, r
    if is_zero_poly(a):
        return [0]
    return poly_scale(a, inv(a[-1], p), p)


def interpolate_full_field(values: list[int], p: int) -> list[int]:
    if len(values) != p:
        raise ValueError("expected one value for each field element")
    out = [0]
    for x, y in enumerate(values):
        if y % p == 0:
            continue
        basis = [1]
        denom = 1
        for a in range(p):
            if a == x:
                continue
            basis = poly_mul(basis, [(-a) % p, 1], p)
            denom = denom * ((x - a) % p) % p
        out = poly_add(out, poly_scale(basis, y * inv(denom, p), p), p)
    return trim(out)


def hankel(seq: list[int], rows: int = 4, cols: int = 5) -> list[list[int]]:
    return [[seq[i + j] for j in range(cols)] for i in range(rows)]


def det_mod(matrix: list[list[int]], p: int) -> int:
    n = len(matrix)
    a = [row[:] for row in matrix]
    det = 1
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col] % p), None)
        if pivot is None:
            return 0
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = -det % p
        pv = a[col][col] % p
        det = det * pv % p
        pv_inv = inv(pv, p)
        for r in range(col + 1, n):
            factor = a[r][col] * pv_inv % p
            if factor:
                for c in range(col, n):
                    a[r][c] = (a[r][c] - factor * a[col][c]) % p
    return det % p


def rank_rref_kernel(matrix: list[list[int]], p: int) -> tuple[int, list[int]]:
    a = [row[:] for row in matrix]
    rows, cols = len(a), len(a[0])
    pivots: list[int] = []
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if a[i][c] % p), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = inv(a[r][c], p)
        a[r] = [(scale * x) % p for x in a[r]]
        for i in range(rows):
            if i == r:
                continue
            factor = a[i][c] % p
            if factor:
                a[i] = [(a[i][j] - factor * a[r][j]) % p for j in range(cols)]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    free = next((c for c in range(cols) if c not in pivots), None)
    if free is None:
        return r, [0] * cols
    vec = [0] * cols
    vec[free] = 1
    for row, pivot_col in enumerate(pivots):
        vec[pivot_col] = (-a[row][free]) % p
    return r, vec


def cramer_kernel_vector(matrix: list[list[int]], p: int) -> list[int]:
    rows, cols = len(matrix), len(matrix[0])
    if cols != rows + 1:
        raise ValueError("expected deficiency one")
    out = []
    for omitted in range(cols):
        minor = [
            [row[c] for c in range(cols) if c != omitted]
            for row in matrix
        ]
        value = det_mod(minor, p)
        if omitted % 2:
            value = -value
        out.append(value % p)
    return out


def mat_vec_zero(matrix: list[list[int]], vector: list[int], p: int) -> bool:
    return all(sum(row[i] * vector[i] for i in range(len(vector))) % p == 0 for row in matrix)


def proportional_nonzero(a: list[int], b: list[int], p: int) -> bool:
    if all(x % p == 0 for x in a) or all(x % p == 0 for x in b):
        return False
    i = next(i for i, x in enumerate(b) if x % p)
    scalar = a[i] * inv(b[i], p) % p
    return all(a[j] % p == scalar * b[j] % p for j in range(len(a)))


def pseudo_remainder(dividend: list[int], divisor: list[int], p: int) -> list[int]:
    rem = trim(dividend[:])
    divisor = trim(divisor[:])
    if is_zero_poly(divisor):
        raise ZeroDivisionError("zero divisor")
    n = len(rem) - 1
    j = len(divisor) - 1
    lc = divisor[-1] % p
    for d in range(n, j - 1, -1):
        coeff = rem[d] if d < len(rem) else 0
        rem = poly_scale(rem, lc, p)
        if coeff:
            shifted = [0] * (d - j) + poly_scale(divisor, coeff, p)
            rem = poly_sub(rem, shifted, p)
        if len(rem) <= d:
            rem += [0] * (d + 1 - len(rem))
        rem[d] = 0
        trim(rem)
    return trim(rem[:j] if len(rem) > j else rem)


def family_matrix(family: ToyFamily, z: int) -> list[list[int]]:
    seq = [(a + z * b) % family.p for a, b in zip(family.u, family.v)]
    return hankel(seq)


def verify_u1_u2_family(family: ToyFamily) -> dict[str, Any]:
    p = family.p
    full_rank = 0
    rank_drop: list[int] = []
    nonzero_cert: dict[str, int] | None = None
    for z in range(p):
        matrix = family_matrix(family, z)
        rank, rref_kernel = rank_rref_kernel(matrix, p)
        cramer = cramer_kernel_vector(matrix, p)
        if not mat_vec_zero(matrix, cramer, p):
            raise AssertionError((family.name, z, "Cramer vector not in kernel"))
        if rank == 4:
            full_rank += 1
            if not proportional_nonzero(cramer, rref_kernel, p):
                raise AssertionError((family.name, z, "Cramer/RREF mismatch", cramer, rref_kernel))
            if nonzero_cert is None:
                omitted = next(i for i, x in enumerate(cramer) if x % p)
                nonzero_cert = {"slope": z, "omitted_column": omitted, "minor_value": cramer[omitted]}
        else:
            rank_drop.append(z)
            if any(cramer):
                raise AssertionError((family.name, z, "rank drop with nonzero maximal minor"))
    if nonzero_cert is None:
        raise AssertionError((family.name, "no nonzero maximal-minor certificate"))
    return {
        "family": family.name,
        "field": f"F_{p}",
        "full_row_rank_slopes": full_rank,
        "rank_drop_slopes": rank_drop,
        "u1_cramer_matches_rref": True,
        "u2_nonzero_minor_certificate": nonzero_cert,
    }


def verify_f97_u3_u5() -> dict[str, Any]:
    p = F97.p
    n = 16
    j = 4
    subgroup = [x for x in range(1, p) if pow(x, n, p) == 1]
    if len(subgroup) != n:
        raise AssertionError(("wrong subgroup size", len(subgroup)))
    dividend = [p - 1] + [0] * (n - 1) + [1]
    values = [[] for _ in range(j)]
    chart_counts = {"top": 0, "low_degree": 0, "rank_drop": 0}
    valid_slopes: list[dict[str, Any]] = []
    mismatches: list[Any] = []

    for z in range(p):
        matrix = family_matrix(F97, z)
        rank, _ = rank_rref_kernel(matrix, p)
        cramer = cramer_kernel_vector(matrix, p)
        if rank != j:
            chart_counts["rank_drop"] += 1
            continue
        if cramer[j] == 0:
            chart_counts["low_degree"] += 1
            continue
        chart_counts["top"] += 1
        _, direct_rem = poly_divmod(dividend, cramer, p)
        prem = pseudo_remainder(dividend, cramer, p)
        scaled_direct = poly_scale(direct_rem, pow(cramer[-1], n - j + 1, p), p)
        if trim(prem[:]) != trim(scaled_direct[:]):
            mismatches.append((z, "pseudo/direct", prem, scaled_direct))
        roots = [h for h in subgroup if poly_eval(cramer, h, p) == 0]
        direct_zero = is_zero_poly(direct_rem)
        pseudo_zero = is_zero_poly(prem)
        root_valid = len(roots) == j
        if not (direct_zero == pseudo_zero == root_valid):
            mismatches.append((z, "validity", direct_zero, pseudo_zero, root_valid, roots))
        padded = prem + [0] * (j - len(prem))
        for i in range(j):
            values[i].append(padded[i] % p)
        if direct_zero:
            valid_slopes.append({"slope": z, "roots": roots})

    if mismatches:
        raise AssertionError(mismatches[:3])
    if chart_counts["top"] != p:
        raise AssertionError(("declared F97 family should stay in top chart", chart_counts))

    coeff_polys = [interpolate_full_field(vs, p) for vs in values]
    for i, poly in enumerate(coeff_polys):
        if any(poly_eval(poly, z, p) != values[i][z] for z in range(p)):
            raise AssertionError(("interpolation failed", i))
    gcd_poly: list[int] | None = None
    for poly in coeff_polys:
        if is_zero_poly(poly):
            continue
        gcd_poly = poly if gcd_poly is None else poly_gcd_monic(gcd_poly, poly, p)
    if gcd_poly is None:
        gcd_poly = [0]
    gcd_roots = [z for z in range(p) if poly_eval(gcd_poly, z, p) == 0]
    if gcd_poly != [1] or gcd_roots or valid_slopes:
        raise AssertionError(("unexpected U5 outcome", gcd_poly, gcd_roots, valid_slopes))

    coeff_hashes = [
        hashlib.sha256(json.dumps(poly, separators=(",", ":")).encode()).hexdigest()
        for poly in coeff_polys
    ]
    return {
        "family": F97.name,
        "field": "F_97",
        "n": n,
        "k": 8,
        "agreement": 12,
        "t": 4,
        "j": j,
        "subgroup_order": len(subgroup),
        "separable": n % p != 0,
        "chart_counts": chart_counts,
        "u3_divisibility_agrees_with_roots": True,
        "u4_pseudo_remainder_agrees_with_direct_division": True,
        "pseudo_remainder_delta": n - j + 1,
        "coefficient_polynomial_degrees": [len(poly) - 1 for poly in coeff_polys],
        "coefficient_polynomial_hashes": coeff_hashes,
        "u5_gcd_eliminant": gcd_poly,
        "u5_gcd_roots": gcd_roots,
        "valid_top_chart_slopes": valid_slopes,
    }


def build_certificate() -> dict[str, Any]:
    u1_u2 = [verify_u1_u2_family(F13), verify_u1_u2_family(F97)]
    f97 = verify_f97_u3_u5()
    if f97["coefficient_polynomial_degrees"] != [52, 52, 52, 52]:
        raise AssertionError(("degree mismatch", f97["coefficient_polynomial_degrees"]))
    return {
        "schema": "m1-deficiency-one-u1-u5-chain-v1",
        "status": "PROVED_SYMBOLIC_WITH_TOY_REPLAY",
        "dag_targets": [
            "u1_cramer",
            "u2_nondegeneracy",
            "u3_divisibility",
            "u4_pseudoremainder",
            "u5_dichotomy",
        ],
        "theorem": {
            "u1": "signed maximal-minor vector spans the kernel at full row rank",
            "u2": "one nonzero maximal-minor evaluation certifies a nondegenerate Cramer chart",
            "u3": "top degree-j locator is valid iff it divides X^n-1",
            "u4": "top-chart pseudo-remainder has the same zero set as direct divisibility",
            "u5": "nonzero pseudo-remainder coefficients give an eliminant; all zero is an identically valid residual",
            "pinned_global_cap": "for n=512,k=256,A=384, t+(n-j+1)t = 49408",
        },
        "u1_u2_families": u1_u2,
        "f97_u3_u5_acid_test": f97,
        "non_claims": [
            "does not compute the F_17^32 root table",
            "does not classify identically valid residual pencils",
            "does not close higher-dimensional SPI",
        ],
    }


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("M1 deficiency-one U1-U5 chart chain")
    for row in cert["u1_u2_families"]:
        print(
            f"  {row['family']}: full_rank={row['full_row_rank_slopes']} "
            f"rank_drop={row['rank_drop_slopes']}"
        )
    f97 = cert["f97_u3_u5_acid_test"]
    print(
        "  F_97 U3-U5: "
        f"charts={f97['chart_counts']} degrees={f97['coefficient_polynomial_degrees']} "
        f"gcd={f97['u5_gcd_eliminant']}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUTPUT}")
    if args.check:
        actual = json.loads(args.check.read_text())
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print_summary(cert)


if __name__ == "__main__":
    main()
