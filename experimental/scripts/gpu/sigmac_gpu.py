#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np


RAWKERNEL_SOURCE = r'''
__device__ int modp(int x, int q) {
    int r = x % q;
    return r < 0 ? r + q : r;
}

__device__ unsigned int slope_mask_for_pair(
    unsigned long long value_index,
    const int* support,
    int support_size,
    const int* value_a,
    const int* value_b,
    int value_base,
    const int* tensor,
    int n,
    int t_count,
    int rows_count,
    int q,
    const int* inv_table
) {
    int avals[6];
    int bvals[6];
    unsigned long long tmp = value_index;
    for (int pos = 0; pos < support_size; ++pos) {
        int digit = (int)(tmp % (unsigned long long)value_base);
        tmp /= (unsigned long long)value_base;
        avals[pos] = value_a[digit];
        bvals[pos] = value_b[digit];
    }

    unsigned int mask = 0u;
    for (int t = 0; t < t_count; ++t) {
        int gamma = -1;
        int ok = 1;
        int h2_any = 0;
        for (int row = 0; row < rows_count; ++row) {
            int h1 = 0;
            int h2 = 0;
            for (int pos = 0; pos < support_size; ++pos) {
                int j = support[pos];
                int coeff = tensor[(j * t_count + t) * rows_count + row];
                h1 += avals[pos] * coeff;
                h2 += bvals[pos] * coeff;
            }
            h1 = modp(h1, q);
            h2 = modp(h2, q);
            if (h2 != 0) {
                h2_any = 1;
                int local_gamma = modp(-h1 * inv_table[h2], q);
                if (gamma < 0) gamma = local_gamma;
                else if (gamma != local_gamma) ok = 0;
            } else if (h1 != 0) {
                ok = 0;
            }
        }
        if (ok && h2_any && gamma >= 0) {
            mask |= (1u << gamma);
        }
    }
    return mask;
}

extern "C" __global__ void scan_support_hist(
    const int* support,
    int support_size,
    const int* value_a,
    const int* value_b,
    int value_base,
    const int* tensor,
    int n,
    int t_count,
    int rows_count,
    int q,
    const int* inv_table,
    unsigned long long value_count,
    unsigned long long* hist,
    int* max_count
) {
    unsigned long long idx = blockDim.x * (unsigned long long)blockIdx.x + threadIdx.x;
    if (idx >= value_count) return;
    unsigned int mask = slope_mask_for_pair(
        idx, support, support_size, value_a, value_b, value_base,
        tensor, n, t_count, rows_count, q, inv_table
    );
    int count = __popc(mask);
    atomicAdd(&hist[count], 1ULL);
    atomicMax(max_count, count);
}

extern "C" __global__ void collect_support_records(
    const int* support,
    int support_size,
    const int* value_a,
    const int* value_b,
    int value_base,
    const int* tensor,
    int n,
    int t_count,
    int rows_count,
    int q,
    const int* inv_table,
    unsigned long long value_count,
    int target_count,
    unsigned long long* cursor,
    int max_records,
    unsigned long long* record_indices,
    unsigned int* record_masks
) {
    unsigned long long idx = blockDim.x * (unsigned long long)blockIdx.x + threadIdx.x;
    if (idx >= value_count) return;
    unsigned int mask = slope_mask_for_pair(
        idx, support, support_size, value_a, value_b, value_base,
        tensor, n, t_count, rows_count, q, inv_table
    );
    int count = __popc(mask);
    if (count == target_count) {
        unsigned long long pos = atomicAdd(cursor, 1ULL);
        if (pos < (unsigned long long)max_records) {
            record_indices[pos] = idx;
            record_masks[pos] = mask;
        }
    }
}
'''


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def render(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def inv(a: int, q: int) -> int:
    return pow(a % q, q - 2, q)


def primitive_root(p: int) -> int:
    factors: list[int] = []
    value = p - 1
    d = 2
    while d * d <= value:
        if value % d == 0:
            factors.append(d)
            while value % d == 0:
                value //= d
        d += 1
    if value > 1:
        factors.append(value)
    for g in range(2, p):
        if all(pow(g, (p - 1) // factor, p) != 1 for factor in factors):
            return g
    raise ValueError(f"no primitive root for F_{p}")


def subgroup_domain(q: int, n: int) -> tuple[int, ...]:
    require((q - 1) % n == 0, "n must divide q-1")
    g = primitive_root(q)
    step = pow(g, (q - 1) // n, q)
    x = 1
    out: list[int] = []
    for _ in range(n):
        out.append(x)
        x = (x * step) % q
    require(x == 1 and len(set(out)) == n, "bad subgroup domain")
    return tuple(out)


def lagrange_weights(domain: tuple[int, ...], q: int) -> tuple[int, ...]:
    out: list[int] = []
    for i, x in enumerate(domain):
        denom = 1
        for j, y in enumerate(domain):
            if i != j:
                denom = (denom * (x - y)) % q
        out.append(inv(denom, q))
    return tuple(out)


def locator_coefficients(domain: tuple[int, ...], disagreement_set: tuple[int, ...], q: int) -> tuple[int, ...]:
    coeffs = [1]
    for index in disagreement_set:
        x = domain[index]
        nxt = [0] * (len(coeffs) + 1)
        for power, coeff in enumerate(coeffs):
            nxt[power] = (nxt[power] - coeff * x) % q
            nxt[power + 1] = (nxt[power + 1] + coeff) % q
        coeffs = nxt
    return tuple(coeffs)


def contribution_tensor(q: int, n: int, k: int, r: int) -> tuple[np.ndarray, tuple[int, ...], list[tuple[int, ...]]]:
    m = n - k
    rows = m - r
    require(rows > 0, "sigma_C Hankel scan expects sub-capacity r <= n-k-1")
    domain = subgroup_domain(q, n)
    weights = lagrange_weights(domain, q)
    disagreements = list(itertools.combinations(range(n), r))
    tensor = np.zeros((n, len(disagreements), rows), dtype=np.int32)
    for t_index, t_set in enumerate(disagreements):
        ell = locator_coefficients(domain, t_set, q)
        for j, x in enumerate(domain):
            for row in range(rows):
                value = 0
                for col, coeff in enumerate(ell):
                    value = (value + coeff * pow(x, row + col, q)) % q
                tensor[j, t_index, row] = (weights[j] * value) % q
    return tensor, domain, disagreements


def value_pair_tables(q: int) -> tuple[np.ndarray, np.ndarray]:
    pairs = [(a, b) for a in range(q) for b in range(q) if a or b]
    return (
        np.asarray([a for a, _b in pairs], dtype=np.int32),
        np.asarray([b for _a, b in pairs], dtype=np.int32),
    )


def decode_pair_values(q: int, support: tuple[int, ...], value_index: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    pairs = [(a, b) for a in range(q) for b in range(q) if a or b]
    base = len(pairs)
    eps1 = [0] * (max(support) + 1 if support else 0)
    eps2 = [0] * (max(support) + 1 if support else 0)
    for index in support:
        if index >= len(eps1):
            eps1.extend([0] * (index + 1 - len(eps1)))
            eps2.extend([0] * (index + 1 - len(eps2)))
        digit = value_index % base
        value_index //= base
        eps1[index], eps2[index] = pairs[digit]
    return tuple(eps1), tuple(eps2)


def expand_pair(q: int, n: int, support: tuple[int, ...], value_index: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    pairs = [(a, b) for a in range(q) for b in range(q) if a or b]
    base = len(pairs)
    eps1 = [0] * n
    eps2 = [0] * n
    for index in support:
        digit = value_index % base
        value_index //= base
        eps1[index], eps2[index] = pairs[digit]
    return tuple(eps1), tuple(eps2)


def poly_eval(coeffs: tuple[int, ...], x: int, q: int) -> int:
    acc = 0
    power = 1
    for coeff in coeffs:
        acc = (acc + coeff * power) % q
        power = (power * x) % q
    return acc


def poly_add(left: list[int], right: list[int], q: int) -> list[int]:
    size = max(len(left), len(right))
    out = [0] * size
    for index in range(size):
        out[index] = ((left[index] if index < len(left) else 0) + (right[index] if index < len(right) else 0)) % q
    return out


def poly_mul_linear(poly: list[int], root: int, q: int) -> list[int]:
    out = [0] * (len(poly) + 1)
    for index, coeff in enumerate(poly):
        out[index] = (out[index] - coeff * root) % q
        out[index + 1] = (out[index + 1] + coeff) % q
    return out


def interpolate_coefficients(points: list[tuple[int, int]], q: int) -> tuple[int, ...]:
    if not points:
        return (0,)
    coeffs = [0]
    for i, (xi, yi) in enumerate(points):
        basis = [1]
        denom = 1
        for j, (xj, _yj) in enumerate(points):
            if i == j:
                continue
            basis = poly_mul_linear(basis, xj, q)
            denom = (denom * (xi - xj)) % q
        scale = yi * inv(denom, q)
        coeffs = poly_add(coeffs, [(scale * coeff) % q for coeff in basis], q)
    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop()
    return tuple(coeffs)


def restriction_coefficients(
    values: tuple[int, ...],
    support: tuple[int, ...],
    domain: tuple[int, ...],
    k: int,
    q: int,
) -> tuple[int, ...] | None:
    if len(support) <= k:
        return interpolate_coefficients([(domain[index], values[index]) for index in support], q)
    base = support[:k]
    coeffs = interpolate_coefficients([(domain[index], values[index]) for index in base], q)
    if all(poly_eval(coeffs, domain[index], q) == values[index] for index in support):
        return coeffs
    return None


def candidate_gamma_for_shape(h1_ell: tuple[int, ...], h2_ell: tuple[int, ...], q: int) -> int | None:
    gamma: int | None = None
    for left, right in zip(h1_ell, h2_ell, strict=True):
        left %= q
        right %= q
        if right == 0:
            if left != 0:
                return None
            continue
        local_gamma = (-left * inv(right, q)) % q
        if gamma is None:
            gamma = local_gamma
        elif gamma != local_gamma:
            return None
    return gamma


def direct_maximal_witness_from_disagreement(
    eps1: tuple[int, ...],
    eps2: tuple[int, ...],
    q: int,
    n: int,
    k: int,
    r: int,
    gamma: int,
    disagreement_set: tuple[int, ...],
) -> dict[str, Any]:
    domain = subgroup_domain(q, n)
    word = tuple((eps1[index] + gamma * eps2[index]) % q for index in range(n))
    witness_set = tuple(index for index in range(n) if index not in disagreement_set)
    codeword_coeffs = restriction_coefficients(word, witness_set, domain, k, q)
    require(codeword_coeffs is not None, "closed-ball witness does not interpolate")
    codeword = tuple(poly_eval(codeword_coeffs, x, q) for x in domain)
    maximal_support = tuple(index for index, (left, right) in enumerate(zip(word, codeword, strict=True)) if left == right)
    distance = n - len(maximal_support)
    require(distance <= r, "reconstructed codeword outside radius")
    eps2_coeffs = restriction_coefficients(eps2, maximal_support, domain, k, q)
    require(eps2_coeffs is None, "maximal witness set mutually extends")
    return {
        "gamma": gamma,
        "distance": distance,
        "agreement": len(maximal_support),
        "disagreement_set": list(disagreement_set),
        "closed_ball_witness_set": list(witness_set),
        "maximal_witness_set": list(maximal_support),
        "codeword_coefficients": list(codeword_coeffs),
    }


def cpu_bad_slope_witnesses(
    eps1: tuple[int, ...],
    eps2: tuple[int, ...],
    q: int,
    n: int,
    k: int,
    r: int,
) -> list[dict[str, Any]]:
    m = n - k
    tensor, _domain, disagreements = contribution_tensor(q, n, k, r)
    by_gamma: dict[int, dict[str, Any]] = {}
    support = [index for index, (a, b) in enumerate(zip(eps1, eps2, strict=True)) if a or b]
    for t_index, disagreement_set in enumerate(disagreements):
        h1 = []
        h2 = []
        for row in range(m - r):
            left = sum(eps1[j] * int(tensor[j, t_index, row]) for j in support) % q
            right = sum(eps2[j] * int(tensor[j, t_index, row]) for j in support) % q
            h1.append(left)
            h2.append(right)
        if not any(h2):
            continue
        gamma = candidate_gamma_for_shape(tuple(h1), tuple(h2), q)
        if gamma is None or gamma in by_gamma:
            continue
        direct = direct_maximal_witness_from_disagreement(eps1, eps2, q, n, k, r, gamma, disagreement_set)
        by_gamma[gamma] = {
            **direct,
            "noncontainment_vector": h2,
        }
    return [by_gamma[gamma] for gamma in sorted(by_gamma)]


def mask_to_slopes(mask: int, q: int) -> list[int]:
    return [gamma for gamma in range(q) if mask & (1 << gamma)]


def total_sparse_pair_count(q: int, n: int, r: int) -> int:
    base = q * q - 1
    return sum(math.comb(n, size) * (base**size) for size in range(r + 1))


def scan_row(
    q: int,
    n: int,
    k: int,
    r: int,
    *,
    max_records: int,
    collect_records: bool,
) -> dict[str, Any]:
    import cupy as cp

    started = time.perf_counter()
    tensor_np, domain, disagreements = contribution_tensor(q, n, k, r)
    rows_count = n - k - r
    tensor = cp.asarray(tensor_np.reshape(-1).astype(np.int32))
    value_a_np, value_b_np = value_pair_tables(q)
    value_a = cp.asarray(value_a_np)
    value_b = cp.asarray(value_b_np)
    inv_np = np.zeros(q, dtype=np.int32)
    for value in range(1, q):
        inv_np[value] = inv(value, q)
    inv_table = cp.asarray(inv_np)
    kernel_hist = cp.RawKernel(RAWKERNEL_SOURCE, "scan_support_hist")
    kernel_collect = cp.RawKernel(RAWKERNEL_SOURCE, "collect_support_records")
    base = q * q - 1
    hist_total = np.zeros(q + 1, dtype=np.uint64)
    max_count = 0
    pairs_scanned = 0
    support_summaries: list[dict[str, Any]] = []
    threads = (256,)

    for support_size in range(r + 1):
        for support in itertools.combinations(range(n), support_size):
            value_count = base**support_size
            support_gpu = cp.asarray(np.asarray(support, dtype=np.int32))
            hist_gpu = cp.zeros(q + 1, dtype=cp.uint64)
            max_gpu = cp.zeros(1, dtype=cp.int32)
            blocks = ((value_count + threads[0] - 1) // threads[0],)
            launch_started = time.perf_counter()
            kernel_hist(
                blocks,
                threads,
                (
                    support_gpu,
                    np.int32(support_size),
                    value_a,
                    value_b,
                    np.int32(base),
                    tensor,
                    np.int32(n),
                    np.int32(len(disagreements)),
                    np.int32(rows_count),
                    np.int32(q),
                    inv_table,
                    np.uint64(value_count),
                    hist_gpu,
                    max_gpu,
                ),
            )
            cp.cuda.Stream.null.synchronize()
            hist_np = cp.asnumpy(hist_gpu)
            local_max = int(cp.asnumpy(max_gpu)[0])
            hist_total += hist_np
            max_count = max(max_count, local_max)
            pairs_scanned += value_count
            support_summaries.append(
                {
                    "support": list(support),
                    "pair_count": int(value_count),
                    "max_bad_slope_count": local_max,
                    "histogram": {str(i): int(v) for i, v in enumerate(hist_np) if int(v)},
                    "elapsed_seconds": round(time.perf_counter() - launch_started, 6),
                }
            )

    records: list[dict[str, Any]] = []
    if collect_records and max_count > 0:
        for support_size in range(r + 1):
            for support in itertools.combinations(range(n), support_size):
                if len(records) >= max_records:
                    break
                value_count = base**support_size
                support_gpu = cp.asarray(np.asarray(support, dtype=np.int32))
                remaining = max_records - len(records)
                cursor = cp.zeros(1, dtype=cp.uint64)
                record_indices = cp.zeros(remaining, dtype=cp.uint64)
                record_masks = cp.zeros(remaining, dtype=cp.uint32)
                blocks = ((value_count + threads[0] - 1) // threads[0],)
                kernel_collect(
                    blocks,
                    threads,
                    (
                        support_gpu,
                        np.int32(support_size),
                        value_a,
                        value_b,
                        np.int32(base),
                        tensor,
                        np.int32(n),
                        np.int32(len(disagreements)),
                        np.int32(rows_count),
                        np.int32(q),
                        inv_table,
                        np.uint64(value_count),
                        np.int32(max_count),
                        cursor,
                        np.int32(remaining),
                        record_indices,
                        record_masks,
                    ),
                )
                cp.cuda.Stream.null.synchronize()
                found = min(int(cp.asnumpy(cursor)[0]), remaining)
                indices_np = cp.asnumpy(record_indices)[:found]
                masks_np = cp.asnumpy(record_masks)[:found]
                for value_index, mask in zip(indices_np, masks_np, strict=True):
                    eps1, eps2 = expand_pair(q, n, support, int(value_index))
                    witnesses = cpu_bad_slope_witnesses(eps1, eps2, q, n, k, r)
                    slopes = [int(witness["gamma"]) for witness in witnesses]
                    require(slopes == mask_to_slopes(int(mask), q), "CPU witness replay disagrees with GPU mask")
                    require(len(slopes) == max_count, "argmax record does not match max_count")
                    records.append(
                        {
                            "support": list(support),
                            "value_index": int(value_index),
                            "eps1": list(eps1),
                            "eps2": list(eps2),
                            "bad_slope_count": len(slopes),
                            "bad_slopes": witnesses,
                        }
                    )
                if len(records) >= max_records:
                    break

    require(pairs_scanned == total_sparse_pair_count(q, n, r), "pair count mismatch")
    return {
        "q_line": q,
        "q_gen": q,
        "q_chal": None,
        "n": n,
        "k": k,
        "m": n - k,
        "rho": f"{k}/{n}",
        "r": r,
        "delta_floor_convention": "r=floor(delta*n)",
        "domain": list(domain),
        "codeword_materialization": False,
        "pairs_scanned": int(pairs_scanned),
        "pairs_total": total_sparse_pair_count(q, n, r),
        "bad_pair_count": int(sum(hist_total[1:])),
        "sigma_c": int(max_count),
        "sigma_c_lower_bound": int(max_count),
        "census_coverage": "full_hankel_scan",
        "early_stop_reason": None,
        "bad_slope_count_histogram": {str(i): int(v) for i, v in enumerate(hist_total) if int(v)},
        "max_pairs_sample": records,
        "support_summaries": support_summaries,
        "elapsed_s": round(time.perf_counter() - started, 6),
        "disagreement_shape_count": len(disagreements),
    }


def build_payload(rows: list[tuple[int, int, int, int]], *, max_records: int) -> dict[str, Any]:
    import cupy as cp

    props = cp.cuda.runtime.getDeviceProperties(0)
    name = props["name"].decode() if isinstance(props.get("name"), bytes) else str(props.get("name"))
    started = time.perf_counter()
    checked = [
        scan_row(q, n, k, r, max_records=max_records, collect_records=True)
        for q, n, k, r in rows
    ]
    payload = {
        "schema_version": "sigma-c-sparse-census-hankel-scan-gpu-accelerator-v1",
        "status": "AUDIT / Pade-Hankel sparse-pair scan certificate",
        "theorem_or_problem_id": "towards-prize prob:mutual; thm:sparsify sparse mutual layer",
        "object": "sigma_C(r)=max sparse-pair count of finite MCA-bad slopes",
        "conventions": {
            "finite_slopes_only": True,
            "slope_denominator": "q_line",
            "delta_floor": "r=floor(delta*n)",
            "witness_set": "Pade-Hankel closed-ball shape T, followed by exact maximal S_z reconstruction",
            "symmetry_policy": "no Mobius/projective quotient",
            "field_ledger": "toy prime-field rows use q_gen=q_line; no q_chal soundness division is claimed",
        },
        "rows": checked,
        "gpu_run": {
            "device": name,
            "cupy_version": cp.__version__,
            "kernel_source_sha256": sha256_text(RAWKERNEL_SOURCE),
            "elapsed_seconds": round(time.perf_counter() - started, 6),
            "integer_arithmetic": "int32 modular Pade-Hankel dot products; no cuBLAS",
        },
        "non_claims": [
            "No deployed/prize-band row is claimed.",
            "GF(9) and extension-field rows are out of scope for this prime-field verifier.",
        ],
    }
    payload["payload_sha256"] = sha256_text(render({k: v for k, v in payload.items() if k != "payload_sha256"}))
    return payload


def parse_row(spec: str) -> tuple[int, int, int, int]:
    parts = [int(part) for part in spec.replace(",", " ").split()]
    require(len(parts) == 4, "--row expects q,n,k,r")
    return parts[0], parts[1], parts[2], parts[3]


def main() -> int:
    parser = argparse.ArgumentParser(description="Optional cuBLAS-free GPU sigma_C sparse census.")
    parser.add_argument("--row", action="append", required=True, help="q,n,k,r")
    parser.add_argument("--max-records", type=int, default=3)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    payload = build_payload([parse_row(spec) for spec in args.row], max_records=args.max_records)
    text = render(payload)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
