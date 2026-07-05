#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path
from typing import Any, Iterable

import numpy as np


RAWKERNEL_SOURCE = r'''
extern "C" __global__ void staircase_counts(
    const int* reps,
    const int* coeffs,
    const int* check_counts,
    int* eca_out,
    int* emca_out,
    int* sigma_out,
    unsigned long long rep_count,
    int table_count,
    int q,
    int m,
    int max_checks,
    int r
) {
    unsigned long long idx = blockDim.x * (unsigned long long)blockIdx.x + threadIdx.x;
    if (idx >= rep_count) return;

    const int* row = reps + idx * (2 * m);
    const int* a = row;
    const int* b = row + m;

    int support = 0;
    for (int col = 0; col < m; ++col) {
        if (a[col] != 0 || b[col] != 0) support += 1;
    }

    int pair_far = 1;
    for (int table = 0; table < table_count && pair_far; ++table) {
        int checks = check_counts[table];
        int a_in = 1;
        int b_in = 1;
        for (int check = 0; check < checks; ++check) {
            int dota = 0;
            int dotb = 0;
            int base = (table * max_checks + check) * m;
            for (int col = 0; col < m; ++col) {
                int c = coeffs[base + col];
                dota += c * a[col];
                dotb += c * b[col];
            }
            if ((dota % q) != 0) a_in = 0;
            if ((dotb % q) != 0) b_in = 0;
        }
        if (a_in && b_in) pair_far = 0;
    }

    int eca = 0;
    int emca = 0;
    for (int gamma = 0; gamma < q; ++gamma) {
        int close_any = 0;
        int mca_bad = 0;
        for (int table = 0; table < table_count; ++table) {
            int checks = check_counts[table];
            int point_in = 1;
            int b_in = 1;
            for (int check = 0; check < checks; ++check) {
                int dotp = 0;
                int dotb = 0;
                int base = (table * max_checks + check) * m;
                for (int col = 0; col < m; ++col) {
                    int c = coeffs[base + col];
                    int bv = b[col];
                    dotb += c * bv;
                    dotp += c * (a[col] + gamma * bv);
                }
                if ((dotp % q) != 0) point_in = 0;
                if ((dotb % q) != 0) b_in = 0;
            }
            if (point_in) {
                close_any = 1;
                if (!b_in) {
                    mca_bad = 1;
                    break;
                }
            }
        }
        if (mca_bad) emca += 1;
        if (pair_far && close_any) eca += 1;
    }

    eca_out[idx] = eca;
    emca_out[idx] = emca;
    sigma_out[idx] = (support <= r) ? emca : -1;
}
'''


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


def build_subset_tables(
    p: int, n: int, k: int, r: int, domain: tuple[int, ...]
) -> list[list[list[tuple[int, int]]]]:
    generator = generator_rows(p, domain, k)
    tables: list[list[list[tuple[int, int]]]] = []
    all_indices = tuple(range(n))
    for removed_size in range(r + 1):
        for removed in itertools.combinations(all_indices, removed_size):
            removed_set = set(removed)
            subset = tuple(index for index in all_indices if index not in removed_set)
            tables.append(nullspace_check_matrix_for_subset(generator, subset, p))
    return tables


def compact_tables(
    tables: list[list[list[tuple[int, int]]]], *, k: int, m: int
) -> tuple[np.ndarray, np.ndarray]:
    max_checks = max((len(table) for table in tables), default=0)
    coeffs = np.zeros((len(tables), max_checks, m), dtype=np.int32)
    check_counts = np.zeros(len(tables), dtype=np.int32)
    for table_index, checks in enumerate(tables):
        check_counts[table_index] = len(checks)
        for check_index, row in enumerate(checks):
            for coord, coeff in row:
                if coord >= k:
                    coeffs[table_index, check_index, coord - k] = coeff
    return coeffs.reshape(-1), check_counts


def in_restricted_tail(tail: tuple[int, ...], checks: list[list[tuple[int, int]]], p: int, k: int) -> bool:
    for row in checks:
        total = 0
        for index, coeff in row:
            if index >= k:
                total += coeff * tail[index - k]
        if total % p:
            return False
    return True


def add_scaled_tail(f1: tuple[int, ...], gamma: int, f2: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((a + gamma * b) % p for a, b in zip(f1, f2, strict=True))


def exact_counts_for_tail_pair(
    f1: tuple[int, ...],
    f2: tuple[int, ...],
    *,
    q: int,
    k: int,
    tables: list[list[list[tuple[int, int]]]],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    pair_far = all(
        not (in_restricted_tail(f1, checks, q, k) and in_restricted_tail(f2, checks, q, k))
        for checks in tables
    )
    eca_bad: list[int] = []
    emca_bad: list[int] = []
    for gamma in range(q):
        point = add_scaled_tail(f1, gamma, f2, q)
        close = False
        mca = False
        for checks in tables:
            if in_restricted_tail(point, checks, q, k):
                close = True
                if not in_restricted_tail(f2, checks, q, k):
                    mca = True
                    break
        if pair_far and close:
            eca_bad.append(gamma)
        if mca:
            emca_bad.append(gamma)
    return tuple(eca_bad), tuple(emca_bad)


def projective_vectors(q: int, m: int) -> Iterable[tuple[int, ...]]:
    yield (0,) * m
    for pivot in range(m):
        for suffix in itertools.product(range(q), repeat=m - pivot - 1):
            yield (0,) * pivot + (1,) + suffix


def affine_shear_tail_representatives(q: int, m: int) -> np.ndarray:
    zero = (0,) * m
    reps: list[tuple[int, ...]] = []
    for eps1_tail in projective_vectors(q, m):
        reps.append(eps1_tail + zero)
    for eps2_tail in projective_vectors(q, m):
        if eps2_tail == zero:
            continue
        pivot = next(index for index, value in enumerate(eps2_tail) if value)
        positions = [index for index in range(m) if index != pivot]
        reps.append(zero + eps2_tail)
        for pos_index, pos in enumerate(positions):
            later = positions[pos_index + 1 :]
            for suffix in itertools.product(range(q), repeat=len(later)):
                eps1 = [0] * m
                eps1[pos] = 1
                for index, value in zip(later, suffix, strict=True):
                    eps1[index] = value
                reps.append(tuple(eps1) + eps2_tail)
    return np.asarray(reps, dtype=np.int32)


def representative_count(q: int, m: int) -> int:
    projective_m = 1 + (q**m - 1) // (q - 1)
    projective_quotient = 1 + (q ** (m - 1) - 1) // (q - 1)
    return projective_m + (projective_m - 1) * projective_quotient


def full_word(k: int, tail: tuple[int, ...]) -> list[int]:
    return [0] * k + list(tail)


def run_radius(q: int, n: int, k: int, r: int, *, sample_seed: int, sample_size: int) -> dict[str, Any]:
    import cupy as cp

    started = time.perf_counter()
    m = n - k
    domain = tuple(range(n))
    tables = build_subset_tables(q, n, k, r, domain)
    coeffs_np, check_counts_np = compact_tables(tables, k=k, m=m)
    reps_np = affine_shear_tail_representatives(q, m)
    require(len(reps_np) == representative_count(q, m), "bad representative count")

    reps = cp.asarray(reps_np)
    coeffs = cp.asarray(coeffs_np)
    check_counts = cp.asarray(check_counts_np)
    eca = cp.empty(len(reps_np), dtype=cp.int32)
    emca = cp.empty(len(reps_np), dtype=cp.int32)
    sigma = cp.empty(len(reps_np), dtype=cp.int32)
    kernel = cp.RawKernel(RAWKERNEL_SOURCE, "staircase_counts")
    threads = (128,)
    blocks = ((len(reps_np) + threads[0] - 1) // threads[0],)
    launch_started = time.perf_counter()
    kernel(
        blocks,
        threads,
        (
            reps,
            coeffs,
            check_counts,
            eca,
            emca,
            sigma,
            np.uint64(len(reps_np)),
            np.int32(len(check_counts_np)),
            np.int32(q),
            np.int32(m),
            np.int32(max((len(table) for table in tables), default=0)),
            np.int32(r),
        ),
    )
    cp.cuda.Stream.null.synchronize()
    gpu_elapsed = time.perf_counter() - launch_started

    eca_np = cp.asnumpy(eca)
    emca_np = cp.asnumpy(emca)
    sigma_np = cp.asnumpy(sigma)
    best_eca = int(eca_np.max())
    best_emca = int(emca_np.max())
    best_sigma = int(sigma_np.max())
    require(best_emca == max(best_eca, best_sigma), "sparsify equality failed")

    argmax_eca_index = int(np.flatnonzero(eca_np == best_eca)[0])
    argmax_emca_index = int(np.flatnonzero(emca_np == best_emca)[0])
    argmax_sigma_index = int(np.flatnonzero(sigma_np == best_sigma)[0])

    def exact_record(index: int, kind: str) -> dict[str, Any]:
        row = reps_np[index]
        f1 = tuple(int(x) for x in row[:m])
        f2 = tuple(int(x) for x in row[m:])
        eca_slopes, emca_slopes = exact_counts_for_tail_pair(f1, f2, q=q, k=k, tables=tables)
        if kind == "eca":
            slopes = eca_slopes
            expected = best_eca
        else:
            slopes = emca_slopes
            expected = best_sigma if kind == "sigma" else best_emca
        require(len(slopes) == expected, f"{kind} CPU exact recheck mismatch")
        return {
            "representative_index": index,
            "eps1": full_word(k, f1),
            "eps2": full_word(k, f2),
            "bad_slopes": list(slopes),
        }

    rng = np.random.default_rng(sample_seed)
    sample_count = min(sample_size, len(reps_np))
    sample_indices = rng.choice(len(reps_np), size=sample_count, replace=False)
    mismatches = 0
    for index in sample_indices:
        row = reps_np[int(index)]
        f1 = tuple(int(x) for x in row[:m])
        f2 = tuple(int(x) for x in row[m:])
        eca_slopes, emca_slopes = exact_counts_for_tail_pair(f1, f2, q=q, k=k, tables=tables)
        support = sum(1 for a, b in zip(f1, f2, strict=True) if a or b)
        expected_sigma = len(emca_slopes) if support <= r else -1
        if (
            len(eca_slopes) != int(eca_np[int(index)])
            or len(emca_slopes) != int(emca_np[int(index)])
            or expected_sigma != int(sigma_np[int(index)])
        ):
            mismatches += 1
            if mismatches >= 5:
                break
    require(mismatches == 0, "GPU-vs-CPU parity sample mismatch")

    return {
        "r": r,
        "agreement": n - r,
        "delta": f"{r}/{n}",
        "eca_num": best_eca,
        "emca_num": best_emca,
        "sigma_num": best_sigma,
        "sparsify_rhs": max(best_eca, best_sigma),
        "sparsify_holds": True,
        "argmax_eca": exact_record(argmax_eca_index, "eca"),
        "argmax_emca": exact_record(argmax_emca_index, "emca"),
        "argmax_sigma": exact_record(argmax_sigma_index, "sigma"),
        "gpu_elapsed_seconds": round(gpu_elapsed, 6),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "representatives_total": int(len(reps_np)),
        "subset_table_count": int(len(tables)),
        "max_checks_per_subset": int(max((len(table) for table in tables), default=0)),
        "parity_sample": {
            "seed": sample_seed,
            "sample_size": sample_count,
            "mismatches": mismatches,
        },
    }


def build_payload(q: int, n: int, k: int, radii: list[int], *, sample_seed: int, sample_size: int) -> dict[str, Any]:
    import cupy as cp

    props = cp.cuda.runtime.getDeviceProperties(0)
    name = props["name"].decode() if isinstance(props.get("name"), bytes) else str(props.get("name"))
    m = n - k
    started = time.perf_counter()
    rows = [run_radius(q, n, k, r, sample_seed=sample_seed + r, sample_size=sample_size) for r in radii]
    payload = {
        "schema_version": "exact-worstcase-eca-emca-affine-quotient-gpu-accelerator-v1",
        "status": "AUDIT / EXPERIMENTAL",
        "object": "worst-case finite-slope CA/MCA numerators over affine-shear orbit representatives",
        "endpoint_conventions": {
            "agreement": "a=n-r",
            "radius": "r=floor(delta*n)",
            "finite_slopes_only": True,
            "pair_distance": "same radius r for point closeness and pair-far condition",
        },
        "row": {
            "q": q,
            "n": n,
            "k": k,
            "m": m,
            "domain": list(range(n)),
            "representative_mode": "affine-shear",
            "representatives_total": representative_count(q, m),
            "raw_pair_classes_total": q ** (2 * m),
            "offline_provenance": True,
            "affine_shear_orbit_reduction_exact": True,
            "membership_engine": "nullspace restricted-code checks, evaluated by cuBLAS-free RawKernel",
            "radii": rows,
        },
        "gpu_run": {
            "device": name,
            "cupy_version": cp.__version__,
            "kernel_source_sha256": sha256_text(RAWKERNEL_SOURCE),
            "elapsed_seconds": round(time.perf_counter() - started, 6),
            "integer_arithmetic": "int32 modular dot products; no cuBLAS",
        },
        "non_claims": [
            "not a deployed-row certificate",
            "not a q_chal or protocol soundness claim",
            "finite slopes only; no projective infinity slope",
        ],
    }
    payload["payload_sha256"] = sha256_text(render({k: v for k, v in payload.items() if k != "payload_sha256"}))
    return payload


def parse_radii(spec: str, m: int) -> list[int]:
    if spec == "all":
        return list(range(m))
    radii = [int(part) for part in spec.replace(",", " ").split()]
    require(all(0 <= r < m for r in radii), "radii must satisfy 0 <= r < n-k")
    return radii


def main() -> int:
    parser = argparse.ArgumentParser(description="Optional cuBLAS-free GPU exact staircase client.")
    parser.add_argument("--row", required=True, help="q,n,k")
    parser.add_argument("--radii", default="all")
    parser.add_argument("--sample-seed", type=int, default=20260704)
    parser.add_argument("--sample-size", type=int, default=5000)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    q, n, k = [int(part) for part in args.row.replace(",", " ").split()]
    radii = parse_radii(args.radii, n - k)
    payload = build_payload(q, n, k, radii, sample_seed=args.sample_seed, sample_size=args.sample_size)
    text = render(payload)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
