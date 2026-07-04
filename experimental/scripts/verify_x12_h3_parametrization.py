#!/usr/bin/env python3
"""Verifier for the h=3 active-core rational parametrization.

For P={1,a,b}, another triple Q={x,y,z} has the same top two locator
coefficients exactly when

    x+y+z = 1+a+b,
    xy+xz+yz = a+b+ab.

Eliminating z gives a conic in (x,y).  Parametrizing the conic by the line
through (1,a) with slope t gives the three rational functions recorded in
the certificate and note.  This script checks the symbolic identities and
then verifies the parametrization against brute active pairs on toy rows.
"""

from __future__ import annotations

from array import array
from collections import Counter
from dataclasses import dataclass
from itertools import combinations
import json
import math
import os
import sys
from typing import Any

import numpy as np
import sympy as sy


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "x12-h3-parametrization",
    "x12_h3_parametrization.json",
)

FAILS: list[str] = []
NCHECK = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global NCHECK
    NCHECK += 1
    tag = "PASS" if cond else "FAIL"
    line = f"[{tag}] {name}"
    if detail:
        line += f"   ({detail})"
    print(line, flush=True)
    if not cond:
        FAILS.append(name)


def symbolic_checks() -> dict[str, str]:
    x, a, b, t = sy.symbols("x a b t")
    S = 1 + a + b
    E = a + b + a * b
    D = t**2 + t + 1
    Nx = -a * t + b * t + b + t**2 + t
    Ny = a * t + a + b * t**2 + b * t - t
    Nz = a * t**2 + a * t - b * t + t + 1
    y_line = a + t * (x - 1)
    conic = x**2 + x * y_line + y_line**2 - S * x - S * y_line + E

    identities = {
        "line_conic_factorization": sy.expand(conic - (x - 1) * (D * x - Nx)),
        "sum_identity": sy.expand(Nx + Ny + Nz - S * D),
        "pair_sum_identity": sy.expand(Nx * Ny + Nx * Nz + Ny * Nz - E * D**2),
    }
    for name, expr in identities.items():
        check(f"symbolic {name}", sy.factor(expr) == 0)

    return {
        "D": sy.sstr(D),
        "Nx": sy.sstr(Nx),
        "Ny": sy.sstr(Ny),
        "Nz": sy.sstr(Nz),
        "Nx_minus_D": sy.sstr(sy.expand(Nx - D)),
        "x_of_t": sy.sstr(Nx / D),
        "y_of_t": sy.sstr(Ny / D),
        "z_of_t": sy.sstr(Nz / D),
        "line_conic_factorization": "F(x, a+t(x-1)) = (x-1) * ((t^2+t+1)x - Nx)",
        "sum_identity": "Nx+Ny+Nz = (1+a+b)(t^2+t+1)",
        "pair_sum_identity": "Nx*Ny+Nx*Nz+Ny*Nz = (a+b+ab)(t^2+t+1)^2",
        "nonzero_membership_polynomial": (
            "For valid distinct 1,a,b, Nx^n-D^n is nonzero: if Nx=zeta*D, "
            "leading coefficients force zeta=1, then Nx-D=(b-a)t+(b-1), "
            "which would force a=b=1."
        ),
    }


def mod_inv(x: int, p: int) -> int:
    if x % p == 0:
        raise ZeroDivisionError("zero has no inverse")
    return pow(x, p - 2, p)


def factor_distinct(n: int) -> list[int]:
    out: list[int] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.append(n)
    return out


def primitive_root(p: int) -> int:
    factors = factor_distinct(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // r, p) != 1 for r in factors):
            return g
    raise RuntimeError(f"no primitive root mod {p}")


def mu_domain(p: int, n: int) -> list[int]:
    if (p - 1) % n:
        raise ValueError(f"n={n} does not divide p-1={p - 1}")
    zeta = pow(primitive_root(p), (p - 1) // n, p)
    values = [pow(zeta, i, p) for i in range(n)]
    if len(set(values)) != n:
        raise RuntimeError(f"bad mu_{n} generator in F_{p}")
    return values


def eval_param(a: int, b: int, t: int, p: int) -> tuple[int, int, int] | None:
    D = (t * t + t + 1) % p
    if D == 0:
        return None
    invD = mod_inv(D, p)
    Nx = (-a * t + b * t + b + t * t + t) % p
    Ny = (a * t + a + b * t * t + b * t - t) % p
    Nz = (a * t * t + a * t - b * t + t + 1) % p
    return (Nx * invD) % p, (Ny * invD) % p, (Nz * invD) % p


def signature(values: tuple[int, int, int], p: int) -> tuple[int, int]:
    x, y, z = values
    return (x + y + z) % p, (x * y + x * z + y * z) % p


def triple_code(i: int, j: int, k: int) -> int:
    return i | (j << 8) | (k << 16)


def decode_triple(code: int) -> tuple[int, int, int]:
    return code & 255, (code >> 8) & 255, (code >> 16) & 255


def mask_from_code(code: int) -> int:
    i, j, k = decode_triple(code)
    return (1 << i) | (1 << j) | (1 << k)


def exps_from_mask(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


@dataclass(frozen=True)
class ActiveRow:
    label: str
    p: int
    n: int


ACTIVE_ROWS = (
    ActiveRow("F17921_mu128_h3", 17921, 128),
    ActiveRow("F65537_mu256_h3", 65537, 256),
)


def signature_arrays(p: int, n: int, domain: list[int]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    keys = array("Q")
    triples = array("I")
    for i, j, k in combinations(range(n), 3):
        vals = (domain[i], domain[j], domain[k])
        e1, e2 = signature(vals, p)
        keys.append(e1 + p * e2)
        triples.append(triple_code(i, j, k))
    key_arr = np.frombuffer(keys, dtype=np.uint64).copy()
    triple_arr = np.frombuffer(triples, dtype=np.uint32).copy()
    order = np.argsort(key_arr, kind="stable")
    return key_arr, triple_arr, order


def active_pairs(row: ActiveRow) -> tuple[list[tuple[int, int]], int, int]:
    domain = mu_domain(row.p, row.n)
    key_arr, triple_arr, order = signature_arrays(row.p, row.n, domain)
    pairs: list[tuple[int, int]] = []
    groups = 0
    max_group = 1

    start = 0
    while start < len(order):
        end = start + 1
        code = key_arr[order[start]]
        while end < len(order) and key_arr[order[end]] == code:
            end += 1
        if end - start > 1:
            groups += 1
            max_group = max(max_group, end - start)
            masks = [mask_from_code(int(triple_arr[order[i]])) for i in range(start, end)]
            for p_mask in masks:
                if not (p_mask & 1):
                    continue
                for q_mask in masks:
                    if q_mask != p_mask and not (q_mask & p_mask):
                        pairs.append((p_mask, q_mask))
        start = end

    return pairs, groups, max_group


def verify_pair_recovery(row: ActiveRow, p_mask: int, q_mask: int, domain: list[int]) -> dict[str, Any]:
    p_exps = exps_from_mask(p_mask, row.n)
    q_exps = exps_from_mask(q_mask, row.n)
    if p_exps[0] != 0:
        raise AssertionError("active P is expected to be anchored")
    one = domain[0]
    a = domain[p_exps[1]]
    b = domain[p_exps[2]]
    x = domain[q_exps[0]]
    y = domain[q_exps[1]]
    z = domain[q_exps[2]]

    t = ((y - a) * mod_inv((x - one) % row.p, row.p)) % row.p
    recovered = eval_param(a, b, t, row.p)
    ok = recovered == (x, y, z)
    same_signature = signature((one, a, b), row.p) == signature((x, y, z), row.p)
    return {
        "P_exponents": p_exps,
        "Q_exponents": q_exps,
        "t": t,
        "denominator": (t * t + t + 1) % row.p,
        "recovered": list(recovered) if recovered is not None else None,
        "ok": ok,
        "same_signature": same_signature,
    }


def analyze_active_row(row: ActiveRow) -> dict[str, Any]:
    check(f"{row.label}: n divides p-1", (row.p - 1) % row.n == 0)
    domain = mu_domain(row.p, row.n)
    pairs, groups, max_group = active_pairs(row)
    failures = []
    denominator_zero = 0
    examples = []
    multiplicities = Counter()
    for p_mask, q_mask in pairs:
        rec = verify_pair_recovery(row, p_mask, q_mask, domain)
        if rec["denominator"] == 0:
            denominator_zero += 1
        if not rec["ok"] or not rec["same_signature"]:
            failures.append(rec)
        if len(examples) < 8:
            examples.append(rec)
        multiplicities[p_mask] += 1

    check(
        f"{row.label}: every active pair is recovered by parametrization",
        not failures,
        f"pairs={len(pairs)}, failures={len(failures)}",
    )
    check(
        f"{row.label}: parametrization denominator nonzero on active pairs",
        denominator_zero == 0,
        f"denominator_zero={denominator_zero}",
    )
    check(
        f"{row.label}: active-pair count matches X-12 boundary signal",
        len(pairs) in (18, 129),
        f"pairs={len(pairs)}",
    )

    return {
        "label": row.label,
        "p": row.p,
        "n": row.n,
        "h": 3,
        "signature_collision_groups": groups,
        "max_signature_group_size": max_group,
        "anchored_active_pairs": len(pairs),
        "anchored_active_cores": len(multiplicities),
        "active_core_multiplicity_histogram": {
            str(k): v for k, v in sorted(Counter(multiplicities.values()).items())
        },
        "denominator_zero_on_active_pairs": denominator_zero,
        "recovery_failures": len(failures),
        "examples": examples,
    }


def small_forward_exhaustive() -> dict[str, Any]:
    """Exhaustively test the forward parametrization on a small tame row."""
    p = 97
    n = 16
    domain = mu_domain(p, n)
    H = set(domain)
    generated_h_triples = 0
    generated_disjoint_partners = 0
    signature_failures = 0
    distinctness_failures = 0
    for i, j in combinations(range(1, n), 2):
        P = (domain[0], domain[i], domain[j])
        P_set = set(P)
        a = domain[i]
        b = domain[j]
        for t in range(p):
            out = eval_param(a, b, t, p)
            if out is None:
                continue
            if signature(P, p) != signature(out, p):
                signature_failures += 1
            if len(set(out)) < 3:
                distinctness_failures += 1
            if all(v in H for v in out):
                generated_h_triples += 1
                if P_set.isdisjoint(out):
                    generated_disjoint_partners += 1
    check("small forward exhaustive signatures hold", signature_failures == 0)
    return {
        "p": p,
        "n": n,
        "anchored_P_choices": math.comb(n - 1, 2),
        "t_values_per_P": p,
        "generated_H_triples": generated_h_triples,
        "generated_disjoint_partners": generated_disjoint_partners,
        "signature_failures": signature_failures,
        "distinct_output_count_failures": distinctness_failures,
    }


def cubic_cap_checks() -> dict[str, Any]:
    rows = []
    for n in (8, 16, 32, 64, 128, 256, 1024):
        anchored_core_count = math.comb(n - 1, 2)
        per_core_cap = 2 * n
        total_cap = anchored_core_count * per_core_cap
        check(
            f"h=3 cubic cap arithmetic n={n}",
            total_cap < n**3,
            f"cap={total_cap}, n^3={n**3}",
        )
        rows.append(
            {
                "n": n,
                "anchored_core_count": anchored_core_count,
                "per_core_cap": per_core_cap,
                "total_cap": total_cap,
                "n_cubed": n**3,
                "strictly_below_n_cubed": total_cap < n**3,
            }
        )
    return {
        "statement": "For h=3, anchored active pairs are < n^3 in odd characteristic with p not dividing n.",
        "proof_count": "C(n-1,2) anchored cores times at most 2n slope parameters per core equals n(n-1)(n-2) < n^3.",
        "rows": rows,
    }


def build_certificate() -> dict[str, Any]:
    symbolic = symbolic_checks()
    active_rows = [analyze_active_row(row) for row in ACTIVE_ROWS]
    small = small_forward_exhaustive()
    cubic_cap = cubic_cap_checks()
    check(
        "boundary active counts are 18 and 129",
        [row["anchored_active_pairs"] for row in active_rows] == [18, 129],
    )
    check(
        "all checked active cores have one partner",
        all(row["active_core_multiplicity_histogram"] == {"1": row["anchored_active_cores"]} for row in active_rows),
    )
    return {
        "node": "active_core_count_bound",
        "task": "X12 h=3 rational parametrization",
        "status": "PROVED: h=3 active partners reduce to a three-rational-function subgroup incidence",
        "symbolic_formulas": symbolic,
        "h3_cubic_cap": cubic_cap,
        "active_row_checks": active_rows,
        "small_forward_exhaustive": small,
        "checks": NCHECK,
    }


def main() -> int:
    write = "--write-certificate" in sys.argv
    result = build_certificate()

    if write:
        os.makedirs(os.path.dirname(CERT), exist_ok=True)
        with open(CERT, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"[write] {CERT}")

    expected = None
    if os.path.exists(CERT):
        with open(CERT, encoding="utf-8") as fh:
            expected = json.load(fh)
    check("certificate exists", expected is not None, CERT)
    if expected is not None:
        check("certificate matches recomputed parametrization checks", result == expected)

    print("\nactive-row summary:")
    for row in result["active_row_checks"]:
        print(
            f"{row['label']:18s} groups={row['signature_collision_groups']:<5d} "
            f"active_pairs={row['anchored_active_pairs']:<4d} "
            f"failures={row['recovery_failures']}"
        )

    if FAILS:
        print("\nFAIL:")
        for name in FAILS:
            print(f"  - {name}")
        return 1

    print(f"\nPASS: {NCHECK} X-12 h=3 parametrization checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
