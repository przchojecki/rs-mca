#!/usr/bin/env python3
"""Verify exact worst-case eca/emca staircases for toy RS rows.

The primary engine enumerates syndrome-class representatives and uses nullspace
parity-check membership tests for restrictions of RS codes.  A second exact
engine uses Vandermonde interpolation coefficients for the same restricted
membership predicates.  Neither engine materializes q^k codewords.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
CERT_DIR = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "exact-worstcase-eca-emca-staircase"
)
CERT_PATH = CERT_DIR / "exact_worstcase_eca_emca_staircase_cpu_rows.json"

CPU_ROWS = (
    (5, 4, 2),
    (7, 6, 5),
    (7, 6, 3),
    (11, 10, 8),
    (13, 12, 10),
    (17, 16, 14),
)

EXPECTED_EMCA = {
    (5, 4, 2): {0: 1, 1: 4},
    (7, 6, 5): {0: 1},
    (7, 6, 3): {0: 1, 1: 2, 2: 7},
    (11, 10, 8): {0: 1, 1: 10},
    (13, 12, 10): {0: 1, 1: 12},
    (17, 16, 14): {0: 1, 1: 16},
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def render_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


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
                (rows[row][idx] - factor * rows[pivot_row][idx]) % p
                for idx in range(col_count)
            ]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return rows, pivots


def generator_rows(p: int, domain: tuple[int, ...], k: int) -> list[list[int]]:
    rows: list[list[int]] = []
    for degree in range(k):
        rows.append([pow(x, degree, p) for x in domain])
    return rows


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
    """Return sparse rows K with K * w|subset = 0 iff w|subset is in C|subset."""

    # Nullspace of G[:, subset], where the variables are coordinates of subset.
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
        sparse = [
            (subset[col], coefficient % p)
            for col, coefficient in enumerate(vector)
            if coefficient % p
        ]
        basis.append(sparse)
    return basis


def interpolation_check_matrix_for_subset(
    p: int, domain: tuple[int, ...], k: int, subset: tuple[int, ...]
) -> list[list[tuple[int, int]]]:
    """Membership by interpolation: high-degree coefficients must vanish."""

    size = len(subset)
    if size <= k:
        return []
    points = [domain[index] for index in subset]
    vandermonde = [[pow(point, degree, p) for degree in range(size)] for point in points]
    inverse = inverse_modp(vandermonde, p)
    checks: list[list[tuple[int, int]]] = []
    for degree in range(k, size):
        row = [
            (subset[col], inverse[degree][col] % p)
            for col in range(size)
            if inverse[degree][col] % p
        ]
        checks.append(row)
    return checks


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
    for row in checks:
        if sum(coeff * word[index] for index, coeff in row) % p:
            return False
    return True


def coset_representatives(p: int, n: int, k: int) -> list[tuple[int, ...]]:
    tail = tuple(range(k, n))
    reps: list[tuple[int, ...]] = []
    for values in itertools.product(range(p), repeat=n - k):
        word = [0] * n
        for index, coord in enumerate(tail):
            word[coord] = values[index]
        reps.append(tuple(word))
    return reps


def add_scaled(f1: tuple[int, ...], gamma: int, f2: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((a + gamma * b) % p for a, b in zip(f1, f2))


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
    for _subset, checks in tables:
        if in_restricted_code(f1, checks, p) and in_restricted_code(f2, checks, p):
            return False
    return True


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
    return sum(1 for a, b in zip(f1, f2) if a or b)


def staircase_for_row(q: int, n: int, k: int, method: str) -> dict[str, Any]:
    domain = tuple(range(n))
    reps = coset_representatives(q, n, k)
    radii = []
    for r in range(n - k):
        tables = build_subset_tables(q, n, k, r, domain, method)
        best_eca = -1
        best_emca = -1
        best_sigma = -1
        argmax_eca: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]] | None = None
        argmax_emca: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]] | None = None
        argmax_sigma: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]] | None = None
        for f1 in reps:
            for f2 in reps:
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
        require(best_sigma >= 0, f"no sparse pair considered for {(q, n, k, r)}")
        require(best_emca == max(best_eca, best_sigma), "thm:sparsify equality failed")
        require(
            EXPECTED_EMCA[(q, n, k)][r] == best_emca,
            f"unexpected emca for {(q, n, k, r)}",
        )
        radii.append(
            {
                "r": r,
                "agreement": n - r,
                "delta": f"{r}/{n}",
                "eca_num": best_eca,
                "emca_num": best_emca,
                "sigma_num": best_sigma,
                "sparsify_rhs": max(best_eca, best_sigma),
                "sparsify_holds": True,
                "argmax_eca": format_argmax(argmax_eca),
                "argmax_emca": format_argmax(argmax_emca),
                "argmax_sigma": format_argmax(argmax_sigma),
            }
        )
    return {
        "q": q,
        "n": n,
        "k": k,
        "m": n - k,
        "domain": list(domain),
        "domain_note": "canonical affine domain; staircase numerators are RS-domain invariant for these toy rows",
        "pair_classes_total": q ** (2 * (n - k)),
        "word_classes_total": q ** (n - k),
        "codeword_materialization_feasible": q**k <= 20000,
        "membership_engine": method,
        "radii": radii,
    }


def format_argmax(
    argmax: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]] | None
) -> dict[str, Any]:
    require(argmax is not None, "missing argmax")
    f1, f2, slopes = argmax
    return {"eps1": list(f1), "eps2": list(f2), "bad_slopes": list(slopes)}


def build_payload() -> dict[str, Any]:
    rows = []
    for row in CPU_ROWS:
        primary = staircase_for_row(*row, method="nullspace")
        secondary = staircase_for_row(*row, method="interpolation")
        matched = []
        for primary_radius, secondary_radius in zip(primary["radii"], secondary["radii"]):
            require(primary_radius["r"] == secondary_radius["r"], "radius mismatch")
            for field in ("eca_num", "emca_num", "sigma_num", "sparsify_rhs"):
                require(
                    primary_radius[field] == secondary_radius[field],
                    f"{field} mismatch for {row} r={primary_radius['r']}",
                )
            matched.append(primary_radius["r"])
        primary["engine_cross_check"] = {
            "secondary_membership_engine": "interpolation",
            "matched_radii": matched,
            "matches": True,
        }
        rows.append(primary)
    payload = {
        "schema_version": "exact-worstcase-eca-emca-staircase-v1",
        "status": "AUDIT",
        "proof_status": "EXPERIMENTAL",
        "theorem_problem_id": "towards-prize-thm-sparsify-toy-staircases",
        "object": "worst-case finite-slope CA/MCA numerators over syndrome-class pair representatives",
        "endpoint_conventions": {
            "agreement": "a = n - r",
            "radius": "r = floor(delta*n), with sub-capacity r in [0, n-k-1]",
            "slopes": "finite slopes gamma in F_q only; denominator q_line=q",
            "pair_distance": "same radius r for CA point closeness and pair-far condition",
            "mca_witness": "exists S with |S| >= n-r, point restricted to S in C|S, and eps2|S not in C|S",
        },
        "engines": {
            "primary": "syndrome-class representatives plus nullspace parity-check restricted-code membership",
            "secondary": "same pair enumeration with Vandermonde interpolation high-coefficient membership checks",
            "codeword_tables": "not used by the committed verifier; q^k materialization is deliberately avoided",
        },
        "rows": rows,
        "family_signals": summarize(rows),
        "non_claims": [
            "not a deployed-row certificate",
            "not a leaderboard or protocol q_chal claim",
            "not a proof for q>=97",
            "toy rows use q_line=q finite slopes",
        ],
    }
    payload["payload_sha256"] = sha256_text(render_json({k: v for k, v in payload.items() if k != "payload_sha256"}))
    return payload


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        first_gt_r = None
        saturation = []
        for radius in row["radii"]:
            if first_gt_r is None and radius["emca_num"] > radius["r"]:
                first_gt_r = radius["r"]
            if radius["emca_num"] == row["q"]:
                saturation.append(radius["r"])
        out.append(
            {
                "q": row["q"],
                "n": row["n"],
                "k": row["k"],
                "m": row["m"],
                "first_r_with_emca_gt_r": first_gt_r,
                "saturation_radii": saturation,
            }
        )
    return out


def check_payload(payload: dict[str, Any]) -> None:
    require(payload["schema_version"] == "exact-worstcase-eca-emca-staircase-v1", "bad schema")
    for row in payload["rows"]:
        for radius in row["radii"]:
            require(radius["emca_num"] == radius["sparsify_rhs"], "sparsify mismatch")
            require(radius["sparsify_holds"] is True, "sparsify flag mismatch")
            require(radius["eca_num"] <= radius["emca_num"], "eca exceeds emca")
            require(radius["emca_num"] >= 1, "emca should be nonzero in these rows")
    expected_hash = payload.get("payload_sha256")
    payload_without_hash = {k: v for k, v in payload.items() if k != "payload_sha256"}
    require(expected_hash == sha256_text(render_json(payload_without_hash)), "payload_sha256 mismatch")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write the canonical certificate")
    parser.add_argument("--check", type=Path, default=CERT_PATH, help="certificate path to replay")
    parser.add_argument("--json", action="store_true", help="print the computed certificate JSON")
    args = parser.parse_args()

    payload = build_payload()
    check_payload(payload)
    if args.json:
        print(render_json(payload), end="")
        return
    if args.write:
        CERT_DIR.mkdir(parents=True, exist_ok=True)
        CERT_PATH.write_text(render_json(payload), encoding="utf-8")
        print(f"wrote {CERT_PATH.relative_to(REPO).as_posix()}")
        return
    expected = json.loads(args.check.read_text(encoding="utf-8"))
    require(expected == payload, "certificate does not match verifier output; rerun with --write")
    print("PASS exact-worstcase-eca-emca-staircase")
    for row in payload["rows"]:
        nums = ", ".join(f"r={r['r']}:emca={r['emca_num']}" for r in row["radii"])
        print(f"  F_{row['q']} n={row['n']} k={row['k']}: {nums}")


if __name__ == "__main__":
    main()
