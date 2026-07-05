#!/usr/bin/env python3
"""Master-flatness incidence enumerator for split locator flats.

Status: EXPERIMENTAL / AUDIT.  This script enumerates split locators
`L_A = prod_{a in A}(X-a)` for `A subset mu_n`, records signed locator
coefficient prefixes, and counts incidences with structured affine flats.
The default emitted packet uses exact CPU enumeration for replayable rows and
records a witness-only large row whose full count is intentionally left to GPU
or later specialized runs.

The optional GPU entry point is lazy: importing this file never imports CuPy.
The committed certificates are verified by `verify_master_flatness_incidence.py`
with pure stdlib arithmetic.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from math import comb
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "master-flatness-incidence-v1"
STATUS = "EXPERIMENTAL"
THEOREM_PROBLEM_ID = "Conjecture-F-master-flatness"

RAWKERNEL_SOURCE = r"""
extern "C" __global__
void flatness_prefix_kernel(const long long *coeffs,
                            const long long *targets,
                            unsigned int *hits,
                            int rows,
                            int width,
                            int codim) {
  int row = blockDim.x * blockIdx.x + threadIdx.x;
  if (row >= rows) return;
  bool ok = true;
  for (int i = 0; i < codim; ++i) {
    if (coeffs[row * width + i] != targets[i]) {
      ok = false;
    }
  }
  if (ok) atomicAdd(hits, 1u);
}
"""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value in {2, 3}:
        return True
    if value % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def primitive_root(p: int) -> int:
    require(is_prime(p), "p must be prime")
    factors = prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for p={p}")


def subgroup_domain(p: int, n: int) -> list[int]:
    require((p - 1) % n == 0, "n must divide p-1")
    step = pow(primitive_root(p), (p - 1) // n, p)
    out: list[int] = []
    x = 1
    for _ in range(n):
        out.append(x)
        x = (x * step) % p
    require(x == 1 and len(set(out)) == n, "bad domain generator")
    return out


def signed_elementary(values: Iterable[int], j: int, p: int) -> tuple[int, ...]:
    elementary = [0] * (j + 1)
    elementary[0] = 1
    used = 0
    for value in values:
        used += 1
        upper = min(used, j)
        for degree in range(upper, 0, -1):
            elementary[degree] = (elementary[degree] + elementary[degree - 1] * value) % p
    require(used == j, "subset size mismatch")
    return tuple(((-1 if degree % 2 else 1) * elementary[degree]) % p for degree in range(1, j + 1))


def locator_coefficients(values: Iterable[int], p: int) -> tuple[int, ...]:
    roots = list(values)
    signed = signed_elementary(roots, len(roots), p)
    return tuple(reversed(signed)) + (1,)


def divisors(value: int) -> list[int]:
    return [d for d in range(1, value + 1) if value % d == 0]


def periodicity_scale(indices: Iterable[int], n: int) -> int:
    support = set(indices)
    best = 1
    for scale in divisors(n):
        step = n // scale
        ok = True
        for index in support:
            for offset in range(scale):
                if (index + offset * step) % n not in support:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            best = max(best, scale)
    return best


def flat_accepts(coeffs: tuple[int, ...], flat: dict[str, Any], p: int) -> bool:
    kind = flat["kind"]
    if kind == "prefix_affine":
        target = tuple(int(x) % p for x in flat["target"])
        return coeffs[: len(target)] == target
    if kind == "linear":
        matrix = flat["matrix"]
        rhs = flat["rhs"]
        for row, value in zip(matrix, rhs, strict=True):
            if sum((int(a) % p) * c for a, c in zip(row, coeffs, strict=True)) % p != int(value) % p:
                return False
        return True
    raise ValueError(f"unknown flat kind {kind!r}")


def density_floor(total: int, p: int, codim: int) -> int:
    return total // (p ** codim)


def subset_record(indices: tuple[int, ...], domain: list[int], p: int, flat: dict[str, Any]) -> dict[str, Any]:
    roots = [domain[index] for index in indices]
    coeffs = signed_elementary(roots, len(indices), p)
    return {
        "indices": list(indices),
        "roots": roots,
        "signed_coefficients": list(coeffs),
        "locator_coefficients_low_to_high": list(locator_coefficients(roots, p)),
        "scale": periodicity_scale(indices, len(domain)),
        "flat_accepts": flat_accepts(coeffs, flat, p),
    }


def sweep_prefix_family(p: int, n: int, j: int, codim: int) -> dict[str, Any]:
    domain = subgroup_domain(p, n)
    buckets: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    scale_counter: Counter[int] = Counter()
    for indices in itertools.combinations(range(n), j):
        coeffs = signed_elementary([domain[index] for index in indices], j, p)
        buckets[coeffs[:codim]].append(indices)
        scale_counter[periodicity_scale(indices, n)] += 1
    histogram = Counter(len(items) for items in buckets.values())
    max_size = max(histogram) if histogram else 0
    max_keys = sorted(key for key, items in buckets.items() if len(items) == max_size)
    target = max_keys[0] if max_keys else tuple()
    flat = {"kind": "prefix_affine", "target": list(target), "codim": codim}
    witnesses = [subset_record(indices, domain, p, flat) for indices in buckets.get(target, [])[:16]]
    total = comb(n, j)
    return {
        "schema_version": SCHEMA_VERSION,
        "status": STATUS,
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "object": "Dloc_j(mu_n) signed coefficient incidence against prefix-affine flats",
        "coverage": "full-enumeration",
        "parameters": {"p": p, "n": n, "j": j, "codim": codim, "flat_family": "prefix_affine"},
        "domain": {"order": n, "elements": domain},
        "counts": {
            "total_locators": total,
            "distinct_flats_hit": len(buckets),
            "occupancy_histogram": {str(k): v for k, v in sorted(histogram.items())},
            "max_occupancy": max_size,
            "max_flat_count": len(max_keys),
            "density_floor": density_floor(total, p, codim),
            "scale_histogram": {str(k): v for k, v in sorted(scale_counter.items())},
        },
        "oracle_regression": oracle_regression(p, n, j, codim, histogram, len(buckets), max_size),
        "extremal_flat": flat,
        "argmax_witnesses": witnesses,
        "non_claims": [
            "No growing-dimensional incidence theorem is claimed.",
            "No resolution of Conjecture-F or prob:band is claimed.",
        ],
    }


def all_j_oracle(p: int, n: int) -> dict[str, Any]:
    domain = subgroup_domain(p, n)
    summaries = []
    for j in range(n + 1):
        scale_counter: Counter[int] = Counter()
        for indices in itertools.combinations(range(n), j):
            scale_counter[periodicity_scale(indices, n)] += 1
        summaries.append(
            {
                "j": j,
                "total_locators": comb(n, j),
                "scale_histogram": {str(k): v for k, v in sorted(scale_counter.items())},
            }
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "status": STATUS,
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "object": "Dloc_j(mu_n) all-degree locator count and periodicity oracle",
        "coverage": "full-enumeration",
        "parameters": {"p": p, "n": n},
        "domain": {"order": n, "elements": domain},
        "j_summaries": summaries,
        "non_claims": ["This is a counting oracle, not an incidence bound."],
    }


def witness_only_row(p: int, n: int, j: int, codim: int, indices: tuple[int, ...]) -> dict[str, Any]:
    domain = subgroup_domain(p, n)
    roots = [domain[index] for index in indices]
    coeffs = signed_elementary(roots, j, p)
    flat = {"kind": "prefix_affine", "target": list(coeffs[:codim]), "codim": codim}
    total = comb(n, j)
    return {
        "schema_version": SCHEMA_VERSION,
        "status": STATUS,
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "object": "Dloc_j(mu_n) large-row witness-only incidence record",
        "coverage": "witness-only-large-row",
        "parameters": {"p": p, "n": n, "j": j, "codim": codim, "flat_family": "prefix_affine"},
        "domain": {"order": n, "generator": domain[1], "element_count": len(domain)},
        "counts": {
            "total_locators": total,
            "density_floor": density_floor(total, p, codim),
            "full_occupancy_recount": None,
        },
        "extremal_flat": flat,
        "argmax_witnesses": [subset_record(indices, domain, p, flat)],
        "deviations": [
            "This row records an exact large-row locator witness and density comparator but does not claim full occupancy enumeration.",
        ],
        "non_claims": [
            "No maximum over all flats is claimed for this large row.",
            "No Conjecture-F or prob:band conclusion is claimed.",
        ],
    }


def oracle_regression(
    p: int,
    n: int,
    j: int,
    codim: int,
    histogram: Counter[int],
    distinct: int,
    max_size: int,
) -> dict[str, Any] | None:
    if (p, n, j, codim) == (17, 16, 6, 4):
        return {
            "source": "verify_l1_prefix_divisor_count.py --p 17 --n 16 --k 6 --sigma 4",
            "matches": {
                "total_locators": comb(n, j) == 8008,
                "distinct_prefix_values": distinct == 7968,
                "occupancy_histogram": dict(histogram) == {1: 7928, 2: 40},
                "max_occupancy": max_size == 2,
            },
            "expected": {
                "total_locators": 8008,
                "distinct_prefix_values": 7968,
                "occupancy_histogram": {"1": 7928, "2": 40},
                "max_occupancy": 2,
            },
        }
    return None


def sha256_payload(payload: dict[str, Any]) -> str:
    clean = json.loads(json.dumps(payload, sort_keys=True))
    clean.pop("payload_sha256", None)
    blob = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def finalize(payload: dict[str, Any]) -> dict[str, Any]:
    payload["rawkernel_source_sha256"] = hashlib.sha256(RAWKERNEL_SOURCE.encode("utf-8")).hexdigest()
    payload["payload_sha256"] = sha256_payload(payload)
    return payload


def emit_defaults(out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = {
        "f17_n16_oracle.json": finalize(all_j_oracle(17, 16)),
        "f17_n16_prefix_oracle.json": finalize(sweep_prefix_family(17, 16, 6, 4)),
        "f31_n30_j5.json": finalize(sweep_prefix_family(31, 30, 5, 2)),
        "f97_n96_j3.json": finalize(sweep_prefix_family(97, 96, 3, 2)),
        "f41_n40_j10.json": finalize(witness_only_row(41, 40, 10, 3, tuple(range(10)))),
    }
    paths = []
    for name, payload in rows.items():
        path = out_dir / name
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        paths.append(path)
    return paths


def load_cupy() -> Any | None:
    try:
        import cupy as cp  # type: ignore
    except Exception:
        return None
    return cp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-defaults", action="store_true", help="emit the default certificate packet")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("experimental/data/certificates/master-flatness-incidence"),
        help="output directory for default certificates",
    )
    parser.add_argument("--gpu-smoke", action="store_true", help="compile a tiny lazy CuPy RawKernel smoke test")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.gpu_smoke:
        cp = load_cupy()
        if cp is None:
            print("gpu_smoke: status=EXPERIMENTAL result=SKIP reason=no_cupy")
        else:
            cp.RawKernel(RAWKERNEL_SOURCE, "flatness_prefix_kernel")
            print("gpu_smoke: status=EXPERIMENTAL result=PASS")
    if args.emit_defaults:
        paths = emit_defaults(args.out_dir)
        print("master_flatness_incidence_engine: status=EXPERIMENTAL result=PASS")
        for path in paths:
            print(path.as_posix())
    if not args.emit_defaults and not args.gpu_smoke:
        raise SystemExit("nothing requested; use --emit-defaults or --gpu-smoke")


if __name__ == "__main__":
    main()
