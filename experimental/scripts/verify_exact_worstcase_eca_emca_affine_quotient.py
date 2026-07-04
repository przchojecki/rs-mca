#!/usr/bin/env python3
"""Affine-shear quotient verifier for exact toy eca/emca staircases.

This is a stdlib-only companion to `verify_exact_worstcase_eca_emca_staircase.py`.
It uses the finite-slope-preserving affine-shear action

    (f1, f2) -> (u*f1 + s*f2, t*f2),   u,t in F_q^*, s in F_q,

on syndrome-class representatives.  Unlike full GL2, this action induces the
affine map gamma -> (u*gamma+s)/t on finite slopes and does not move a finite
slope to infinity.

The script is intended as an audit/compute rung for m=4 rows.  It can also
cross-check the quotient against the existing full syndrome-class enumeration
on small rows.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path
from typing import Any, Iterable


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def render(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def rref_modp(matrix: list[list[int]], p: int) -> tuple[list[list[int]], list[int]]:
    rows = [row[:] for row in matrix]
    if not rows:
        return rows, []
    row_count = len(rows)
    col_count = len(rows[0])
    pivots: list[int] = []
    pivot_row = 0
    for col in range(col_count):
        pivot = None
        for row in range(pivot_row, row_count):
            if rows[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inv = pow(rows[pivot_row][col] % p, p - 2, p)
        rows[pivot_row] = [(value * inv) % p for value in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or rows[row][col] % p == 0:
                continue
            factor = rows[row][col] % p
            rows[row] = [
                (value - factor * rows[pivot_row][idx]) % p
                for idx, value in enumerate(rows[row])
            ]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return rows, pivots


def generator_rows(p: int, domain: tuple[int, ...], k: int) -> list[list[int]]:
    return [[pow(x, degree, p) for x in domain] for degree in range(k)]


def inverse_modp(matrix: list[list[int]], p: int) -> list[list[int]]:
    size = len(matrix)
    augmented = [
        [value % p for value in row]
        + [1 if row_index == col_index else 0 for col_index in range(size)]
        for row_index, row in enumerate(matrix)
    ]
    rref, pivots = rref_modp(augmented, p)
    require(pivots == list(range(size)), "matrix is not invertible")
    return [row[size:] for row in rref]


def nullspace_check_matrix_for_subset(
    generator: list[list[int]], subset: tuple[int, ...], p: int
) -> list[list[tuple[int, int]]]:
    matrix = [[row[index] % p for index in subset] for row in generator]
    rref, pivots = rref_modp(matrix, p)
    pivot_set = set(pivots)
    free_cols = [col for col in range(len(subset)) if col not in pivot_set]
    basis: list[list[tuple[int, int]]] = []
    for free_col in free_cols:
        vector = [0] * len(subset)
        vector[free_col] = 1
        for row_index, pivot_col in enumerate(pivots):
            vector[pivot_col] = (-rref[row_index][free_col]) % p
        basis.append(
            [
                (subset[col], coefficient % p)
                for col, coefficient in enumerate(vector)
                if coefficient % p
            ]
        )
    return basis


def interpolation_check_matrix_for_subset(
    p: int, domain: tuple[int, ...], k: int, subset: tuple[int, ...]
) -> list[list[tuple[int, int]]]:
    size = len(subset)
    if size <= k:
        return []
    points = [domain[index] for index in subset]
    vandermonde = [[pow(point, degree, p) for degree in range(size)] for point in points]
    inverse = inverse_modp(vandermonde, p)
    return [
        [
            (subset[col], inverse[degree][col] % p)
            for col in range(size)
            if inverse[degree][col] % p
        ]
        for degree in range(k, size)
    ]


def build_subset_tables(
    p: int, n: int, k: int, r: int, domain: tuple[int, ...], method: str
) -> list[tuple[tuple[int, ...], list[list[tuple[int, int]]]]]:
    generator = generator_rows(p, domain, k)
    tables: list[tuple[tuple[int, ...], list[list[tuple[int, int]]]]] = []
    all_indices = tuple(range(n))
    for removed_size in range(r + 1):
        for removed in itertools.combinations(all_indices, removed_size):
            removed_set = set(removed)
            subset = tuple(index for index in all_indices if index not in removed_set)
            if method == "nullspace":
                checks = nullspace_check_matrix_for_subset(generator, subset, p)
            elif method == "interpolation":
                checks = interpolation_check_matrix_for_subset(p, domain, k, subset)
            else:
                raise ValueError(f"unknown table method {method!r}")
            tables.append((subset, checks))
    tables.sort(key=lambda item: (-len(item[0]), item[0]))
    return tables


def in_restricted_code(word: tuple[int, ...], checks: list[list[tuple[int, int]]], p: int) -> bool:
    return all(sum(coeff * word[index] for index, coeff in row) % p == 0 for row in checks)


def add_scaled(f1: tuple[int, ...], gamma: int, f2: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((a + gamma * b) % p for a, b in zip(f1, f2, strict=True))


def mca_bad_slopes(
    f1: tuple[int, ...],
    f2: tuple[int, ...],
    p: int,
    tables: list[tuple[tuple[int, ...], list[list[tuple[int, int]]]]],
) -> tuple[int, ...]:
    bad: list[int] = []
    for gamma in range(p):
        point = add_scaled(f1, gamma, f2, p)
        for _subset, checks in tables:
            if in_restricted_code(point, checks, p) and not in_restricted_code(f2, checks, p):
                bad.append(gamma)
                break
    return tuple(bad)


def pair_far(
    f1: tuple[int, ...],
    f2: tuple[int, ...],
    p: int,
    tables: list[tuple[tuple[int, ...], list[list[tuple[int, int]]]]],
) -> bool:
    return all(
        not (in_restricted_code(f1, checks, p) and in_restricted_code(f2, checks, p))
        for _subset, checks in tables
    )


def ca_bad_slopes(
    f1: tuple[int, ...],
    f2: tuple[int, ...],
    p: int,
    tables: list[tuple[tuple[int, ...], list[list[tuple[int, int]]]]],
) -> tuple[int, ...]:
    if not pair_far(f1, f2, p, tables):
        return ()
    bad: list[int] = []
    for gamma in range(p):
        point = add_scaled(f1, gamma, f2, p)
        if any(in_restricted_code(point, checks, p) for _subset, checks in tables):
            bad.append(gamma)
    return tuple(bad)


def sparse_support_size(f1: tuple[int, ...], f2: tuple[int, ...]) -> int:
    return sum(1 for a, b in zip(f1, f2, strict=True) if a or b)


def projective_vectors(q: int, m: int) -> Iterable[tuple[int, ...]]:
    yield (0,) * m
    for pivot in range(m):
        for suffix in itertools.product(range(q), repeat=m - pivot - 1):
            yield (0,) * pivot + (1,) + suffix


def affine_shear_tail_representatives(q: int, m: int) -> Iterable[tuple[tuple[int, ...], tuple[int, ...]]]:
    zero = (0,) * m
    for eps1_tail in projective_vectors(q, m):
        yield eps1_tail, zero
    for eps2_tail in projective_vectors(q, m):
        if eps2_tail == zero:
            continue
        pivot = next(index for index, value in enumerate(eps2_tail) if value)
        positions = [index for index in range(m) if index != pivot]
        yield zero, eps2_tail
        for pos_index, pos in enumerate(positions):
            later = positions[pos_index + 1 :]
            for suffix in itertools.product(range(q), repeat=len(later)):
                eps1 = [0] * m
                eps1[pos] = 1
                for index, value in zip(later, suffix, strict=True):
                    eps1[index] = value
                yield tuple(eps1), eps2_tail


def full_tail_representatives(q: int, m: int) -> Iterable[tuple[tuple[int, ...], tuple[int, ...]]]:
    tails = itertools.product(range(q), repeat=m)
    materialized = list(tails)
    for eps1_tail in materialized:
        for eps2_tail in materialized:
            yield eps1_tail, eps2_tail


def representative_count(q: int, m: int, mode: str) -> int:
    if mode == "full":
        return q ** (2 * m)
    projective_m = 1 + (q**m - 1) // (q - 1)
    projective_quotient = 1 + (q ** (m - 1) - 1) // (q - 1)
    return projective_m + (projective_m - 1) * projective_quotient


def full_word(k: int, tail: tuple[int, ...]) -> tuple[int, ...]:
    return (0,) * k + tail


def format_argmax(
    argmax: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]] | None
) -> dict[str, Any]:
    require(argmax is not None, "missing argmax")
    f1, f2, slopes = argmax
    return {"eps1": list(f1), "eps2": list(f2), "bad_slopes": list(slopes)}


def staircase_for_row(
    q: int,
    n: int,
    k: int,
    radii: list[int],
    *,
    mode: str,
    method: str,
) -> dict[str, Any]:
    require(0 < k < n <= q, "this affine-domain verifier expects 0 < k < n <= q")
    m = n - k
    domain = tuple(range(n))
    if mode == "full":
        tail_reps = full_tail_representatives(q, m)
    elif mode == "affine-shear":
        tail_reps = affine_shear_tail_representatives(q, m)
    else:
        raise ValueError(f"unknown representative mode {mode!r}")
    tail_reps = list(tail_reps)
    require(len(tail_reps) == representative_count(q, m, mode), "representative count mismatch")
    rows = []
    for r in radii:
        started = time.perf_counter()
        tables = build_subset_tables(q, n, k, r, domain, method)
        best_eca = -1
        best_emca = -1
        best_sigma = -1
        argmax_eca = None
        argmax_emca = None
        argmax_sigma = None
        for eps1_tail, eps2_tail in tail_reps:
            f1 = full_word(k, eps1_tail)
            f2 = full_word(k, eps2_tail)
            emca_slopes = mca_bad_slopes(f1, f2, q, tables)
            emca_count = len(emca_slopes)
            if emca_count > best_emca:
                best_emca = emca_count
                argmax_emca = (f1, f2, emca_slopes)
            eca_slopes = ca_bad_slopes(f1, f2, q, tables)
            eca_count = len(eca_slopes)
            if eca_count > best_eca:
                best_eca = eca_count
                argmax_eca = (f1, f2, eca_slopes)
            if sparse_support_size(f1, f2) <= r and emca_count > best_sigma:
                best_sigma = emca_count
                argmax_sigma = (f1, f2, emca_slopes)
        require(best_sigma >= 0, "no sparse pair considered")
        require(best_emca == max(best_eca, best_sigma), "sparsify equality failed")
        rows.append(
            {
                "r": r,
                "agreement": n - r,
                "delta": f"{r}/{n}",
                "eca_num": best_eca,
                "emca_num": best_emca,
                "sigma_num": best_sigma,
                "sparsify_rhs": max(best_eca, best_sigma),
                "sparsify_holds": True,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
                "argmax_eca": format_argmax(argmax_eca),
                "argmax_emca": format_argmax(argmax_emca),
                "argmax_sigma": format_argmax(argmax_sigma),
            }
        )
    return {
        "q": q,
        "n": n,
        "k": k,
        "m": m,
        "domain": list(domain),
        "domain_note": "canonical affine domain; staircase numerators are RS-domain invariant for these toy rows",
        "representative_mode": mode,
        "representatives_total": len(tail_reps),
        "raw_pair_classes_total": q ** (2 * m),
        "offline_provenance": True,
        "affine_shear_orbit_reduction_exact": mode == "affine-shear",
        "membership_engine": method,
        "radii": rows,
    }


def parse_row(spec: str) -> tuple[int, int, int]:
    parts = [int(part) for part in spec.replace(",", " ").split()]
    require(len(parts) == 3, "--row expects q,n,k")
    return parts[0], parts[1], parts[2]


def parse_radii(spec: str | None, m: int) -> list[int]:
    if spec is None:
        return list(range(m))
    radii = [int(part) for part in spec.replace(",", " ").split()]
    require(all(0 <= r < m for r in radii), "radii must satisfy 0 <= r < n-k")
    return radii


def stable_payload_hash(payload: dict[str, Any]) -> str:
    without_hash = {key: value for key, value in payload.items() if key != "payload_sha256"}
    return sha256_text(render(without_hash))


def check_payload(payload: dict[str, Any]) -> None:
    require(
        payload.get("schema_version") == "exact-worstcase-eca-emca-affine-quotient-v1",
        "bad schema_version",
    )
    expected_hash = payload.get("payload_sha256")
    require(isinstance(expected_hash, str), "missing payload_sha256")
    require(expected_hash == stable_payload_hash(payload), "payload_sha256 mismatch")
    require(payload.get("status") == "AUDIT / EXPERIMENTAL", "bad status")
    for row in payload.get("rows", []):
        require(row.get("offline_provenance") is True, "m4 rows must disclose offline provenance")
        require(row.get("affine_shear_orbit_reduction_exact") is True, "expected affine-shear exact flag")
        require(row.get("representative_mode") == "affine-shear", "expected affine-shear representatives")
        raw_pairs = row["q"] ** (2 * row["m"])
        require(row.get("raw_pair_classes_total") == raw_pairs, "raw pair count mismatch")
        previous_emca = -1
        for radius in row.get("radii", []):
            require(radius["emca_num"] == radius["sparsify_rhs"], "sparsify mismatch")
            require(radius["sparsify_holds"] is True, "sparsify flag mismatch")
            require(radius["eca_num"] <= radius["emca_num"], "eca exceeds emca")
            require(radius["sigma_num"] <= radius["emca_num"], "sigma exceeds emca")
            require(radius["emca_num"] >= previous_emca, "emca staircase is not monotone")
            require(radius["emca_num"] <= row["q"], "finite-slope numerator exceeds q")
            if radius["r"] == 0:
                require(radius["emca_num"] >= 1, "r=0 emca should be nonzero")
            previous_emca = radius["emca_num"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--row", help="row q,n,k")
    parser.add_argument("--radii", help="comma/space-separated radii; default all sub-capacity radii")
    parser.add_argument("--mode", choices=("affine-shear", "full"), default="affine-shear")
    parser.add_argument("--method", choices=("nullspace", "interpolation"), default="nullspace")
    parser.add_argument("--compare-full", action="store_true", help="also run full representatives and compare numerators")
    parser.add_argument("--check", type=Path, help="quick-check an offline certificate without recomputing rows")
    parser.add_argument("--write", type=Path, help="write JSON output")
    args = parser.parse_args()

    if args.check:
        payload = json.loads(args.check.read_text(encoding="utf-8"))
        check_payload(payload)
        print("PASS exact-worstcase-eca-emca-affine-quotient")
        for row in payload["rows"]:
            nums = ", ".join(f"r={radius['r']}:emca={radius['emca_num']}" for radius in row["radii"])
            print(f"  F_{row['q']} n={row['n']} k={row['k']}: {nums}")
        return

    require(args.row is not None, "--row is required unless --check is used")
    q, n, k = parse_row(args.row)
    radii = parse_radii(args.radii, n - k)
    payload = {
        "schema_version": "exact-worstcase-eca-emca-affine-quotient-v1",
        "status": "AUDIT / EXPERIMENTAL",
        "object": "worst-case finite-slope CA/MCA numerators over affine-shear orbit representatives",
        "conventions": {
            "agreement": "a=n-r",
            "radius": "r=floor(delta*n)",
            "finite_slopes_only": True,
            "affine_shear_action": "(f1,f2)->(u*f1+s*f2,t*f2), u,t nonzero",
            "non_claim": "full GL2 is not used because it can move finite slopes to infinity",
        },
        "rows": [staircase_for_row(q, n, k, radii, mode=args.mode, method=args.method)],
    }
    if args.compare_full:
        full = staircase_for_row(q, n, k, radii, mode="full", method=args.method)
        affine = payload["rows"][0]
        for left, right in zip(affine["radii"], full["radii"], strict=True):
            for field in ("eca_num", "emca_num", "sigma_num", "sparsify_rhs"):
                require(left[field] == right[field], f"{field} mismatch at r={left['r']}")
        payload["full_comparison"] = {"matches": True, "row": full}
    payload["payload_sha256"] = stable_payload_hash(payload)
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(payload), encoding="utf-8")
    print(render(payload), end="")


if __name__ == "__main__":
    main()
