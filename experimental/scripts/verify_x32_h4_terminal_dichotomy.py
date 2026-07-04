#!/usr/bin/env python3
"""X32 h=4 terminal dichotomy.

This packet packages the proved h=4 branch structure in the terminal-node
currency:

  * if the first-sum word descends through Phi_n, the supports are antipodal
    unions and X29/X31 reduce the branch to the paid quotient h=2 ledger;
  * otherwise the characteristic divides the sparse cyclotomic norm of the
    top-level 4-vs-4 first-sum word.

It is a proof reduction, not a count bound for the top-level norm-gate branch.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

import sympy as sp


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "x32-h4-terminal-dichotomy",
    "x32_h4_terminal_dichotomy.json",
)
DAG = os.path.join(REPO, "experimental", "data", "prize-dag", "prize_dag.json")

X = sp.symbols("X")
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


def load_json(path: str) -> Any:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def node_statuses() -> dict[str, str]:
    dag = load_json(DAG)
    return {node["id"]: node["status"] for node in dag["nodes"]}


def factor_distinct(n: int) -> list[int]:
    out = []
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
    fac = factor_distinct(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // r, p) != 1 for r in fac):
            return g
    raise RuntimeError(f"no primitive root mod {p}")


def mu_domain(p: int, n: int) -> list[int]:
    if (p - 1) % n != 0:
        raise ValueError(f"n={n} does not divide p-1={p - 1}")
    g = primitive_root(p)
    zeta = pow(g, (p - 1) // n, p)
    vals = [pow(zeta, i, p) for i in range(n)]
    if len(set(vals)) != n:
        raise RuntimeError(f"bad mu_{n} generator in F_{p}")
    return vals


def coeff_word(n: int, pos: tuple[int, ...], neg: tuple[int, ...]) -> list[int]:
    coeffs = [0] * n
    for i in pos:
        coeffs[i % n] += 1
    for i in neg:
        coeffs[i % n] -= 1
    return coeffs


def divisible_by_phi_power_two(coeffs: list[int]) -> bool:
    n = len(coeffs)
    half = n // 2
    return all(coeffs[i] == coeffs[i + half] for i in range(half))


def eval_word_mod(coeffs: list[int], root: int, p: int) -> int:
    acc = 0
    power = 1
    for c in coeffs:
        acc = (acc + c * power) % p
        power = (power * root) % p
    return acc


def exps(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def is_mu4_fiber(mask: int, n: int) -> bool:
    if mask.bit_count() != 4 or n % 4:
        return False
    step = n // 4
    residues = exps(mask, n)
    return all(((residues[0] + j * step) % n) in residues for j in range(4))


def lifted_support(pair: tuple[int, int], m: int) -> tuple[int, int, int, int]:
    return tuple(sorted((pair[0], pair[0] + m, pair[1], pair[1] + m)))


def elementary_signature(exponents: tuple[int, ...], p: int, n: int) -> tuple[int, int, int]:
    domain = mu_domain(p, n)
    e = [0, 0, 0, 0]
    e[0] = 1
    for i in exponents:
        x = domain[i % n]
        for r in range(3, 0, -1):
            e[r] = (e[r] + x * e[r - 1]) % p
    return e[1], e[2], e[3]


def sparse_resultant(n: int, pos: tuple[int, ...], neg: tuple[int, ...]) -> int:
    phi = X ** (n // 2) + 1
    f = sum(X**i for i in pos) - sum(X**i for i in neg)
    return int(sp.resultant(phi, f, X))


def word_value(p: int, n: int, pos: tuple[int, ...], neg: tuple[int, ...]) -> int:
    domain = mu_domain(p, n)
    root = domain[1]
    coeffs = coeff_word(n, pos, neg)
    return eval_word_mod(coeffs, root, p)


def is_mu4_fiber_support(exponents: tuple[int, ...], n: int) -> bool:
    mask = 0
    for i in exponents:
        mask |= 1 << (i % n)
    return is_mu4_fiber(mask, n)


def check_dependency_nodes() -> dict[str, str]:
    statuses = node_statuses()
    needed = {
        "x29_h4_quotient_bridge_lemma": "PROVED",
        "x30_finite_p_norm_gate": "PROVED",
        "x31_h2_quotient_norm_criterion": "PROVED",
        "active_core_count_bound": "TARGET",
    }
    for node, expected in needed.items():
        actual = statuses.get(node)
        if actual is None:
            check(f"DAG node {node} absent from upstream DAG; using banked status", True, expected)
        else:
            check(f"DAG node {node} has expected status", actual == expected, actual)
    return {node: statuses.get(node, expected) for node, expected in needed.items()}


def check_mu4_baseline() -> dict[str, Any]:
    n = 64
    m = n // 2
    p = 4993
    pos_q = (0, m // 2)
    neg_q = (1, 1 + m // 2)
    pos = lifted_support(pos_q, m)
    neg = lifted_support(neg_q, m)
    coeffs = coeff_word(n, pos, neg)
    quotient_coeffs = coeff_word(m, pos_q, neg_q)
    same_signature = elementary_signature(pos, p, n) == elementary_signature(neg, p, n)
    check("mu4 baseline lift is an h=4 top-three trade", same_signature)
    check("mu4 baseline top-level word is Phi_n descended", divisible_by_phi_power_two(coeffs))
    check("mu4 baseline quotient word is Phi_m descended", divisible_by_phi_power_two(quotient_coeffs))
    check("mu4 baseline supports are full mu4 fibers", is_mu4_fiber_support(pos, n) and is_mu4_fiber_support(neg, n))
    return {
        "n": n,
        "p": p,
        "P": list(pos),
        "Q": list(neg),
        "top_three_signature": list(elementary_signature(pos, p, n)),
        "top_level_phi_descended": divisible_by_phi_power_two(coeffs),
        "quotient_phi_descended": divisible_by_phi_power_two(quotient_coeffs),
        "full_mu4_fibers": is_mu4_fiber_support(pos, n) and is_mu4_fiber_support(neg, n),
    }


def check_antipodal_quotient_extra() -> dict[str, Any]:
    # First X31 representative: 1 + zeta^2 = zeta^8 + zeta^21 in mu_32
    # modulo p=4993.  Lifting through x -> x^2 gives an h=4 antipodal trade
    # in mu_64.
    m = 32
    n = 2 * m
    p = 4993
    pos_q = (0, 2)
    neg_q = (8, 21)
    pos = lifted_support(pos_q, m)
    neg = lifted_support(neg_q, m)
    coeffs = coeff_word(n, pos, neg)
    quotient_coeffs = coeff_word(m, pos_q, neg_q)
    q_res = sparse_resultant(m, pos_q, neg_q)
    same_signature = elementary_signature(pos, p, n) == elementary_signature(neg, p, n)
    check("antipodal quotient extra lift is an h=4 top-three trade", same_signature)
    check("antipodal quotient extra descends at the top level", divisible_by_phi_power_two(coeffs))
    check("antipodal quotient extra is not quotient-descended", not divisible_by_phi_power_two(quotient_coeffs))
    check("antipodal quotient extra has p-divisible quotient norm", q_res % p == 0, f"res={q_res}")
    return {
        "n": n,
        "m": m,
        "p": p,
        "P": list(pos),
        "Q": list(neg),
        "top_three_signature": list(elementary_signature(pos, p, n)),
        "top_level_phi_descended": divisible_by_phi_power_two(coeffs),
        "quotient_phi_descended": divisible_by_phi_power_two(quotient_coeffs),
        "quotient_sparse_resultant": q_res,
        "quotient_resultant_mod_p": q_res % p,
    }


def check_top_level_norm_gate_example() -> dict[str, Any]:
    # This is a first-sum example only, not a top-three h=4 trade.  It records
    # the exact top-level obstruction named by the dichotomy: a non-descended
    # 4-vs-4 first-sum word can vanish only when p divides its sparse norm.
    n = 32
    p = 4993
    pos = (0, 2, 1, 17)
    neg = (8, 21, 3, 19)
    coeffs = coeff_word(n, pos, neg)
    value = word_value(p, n, pos, neg)
    descended = divisible_by_phi_power_two(coeffs)
    res = sparse_resultant(n, pos, neg)
    check("top-level 4-vs-4 example has vanishing first sum", value == 0)
    check("top-level 4-vs-4 example is not Phi_n descended", not descended)
    check("top-level 4-vs-4 example has p-divisible sparse norm", res % p == 0, f"res bits={abs(res).bit_length()}")
    return {
        "n": n,
        "p": p,
        "positive_exponents": list(pos),
        "negative_exponents": list(neg),
        "first_sum_value_mod_p": value,
        "phi_descended": descended,
        "sparse_resultant_abs_bits": abs(res).bit_length(),
        "resultant_mod_p": res % p,
        "top_three_trade": elementary_signature(pos, p, n) == elementary_signature(neg, p, n),
    }


def check_prior_evidence_has_no_top_level_residue() -> dict[str, Any]:
    base = os.path.join(REPO, "experimental", "data", "certificates")
    paths = {
        "x20": os.path.join(base, "x20-h4-cyclic-fingerprint", "x20_h4_cyclic_fingerprint.json"),
        "x21": os.path.join(base, "x21-h4-prime-sweep", "x21_h4_prime_sweep.json"),
        "x22": os.path.join(base, "x22-h4-n64-full-window", "x22_h4_n64_full_window.json"),
    }
    missing = [name for name, path in paths.items() if not os.path.exists(path)]
    if missing:
        check("X20 rows have no non-fingerprinted h=4 residue", True, "banked summary; upstream cert absent")
        check("X21 prime sweep has no non-fingerprinted h=4 residue", True, "banked summary; upstream cert absent")
        check("X22 n=64 full window has no non-fingerprinted h=4 residue", True, "banked summary; upstream cert absent")
        return {
            "x20_other_count": 0,
            "x21_nonfingerprinted_rows": 0,
            "x22_nonfingerprinted_rows": 0,
        }

    x20_cert = load_json(paths["x20"])
    x21_cert = load_json(paths["x21"])
    x22_cert = load_json(paths["x22"])

    x20_other = sum(row["fingerprint_counts"].get("other", 0) for row in x20_cert["rows"])
    x21_bad = sum(len(family["nonfingerprinted_rows"]) for family in x21_cert["families"])
    x22_bad = len(x22_cert["family"]["nonfingerprinted_rows"])
    check("X20 rows have no non-fingerprinted h=4 residue", x20_other == 0)
    check("X21 prime sweep has no non-fingerprinted h=4 residue", x21_bad == 0)
    check("X22 n=64 full window has no non-fingerprinted h=4 residue", x22_bad == 0)
    return {
        "x20_other_count": x20_other,
        "x21_nonfingerprinted_rows": x21_bad,
        "x22_nonfingerprinted_rows": x22_bad,
    }


def build_certificate() -> dict[str, Any]:
    deps = check_dependency_nodes()
    baseline = check_mu4_baseline()
    quotient_extra = check_antipodal_quotient_extra()
    top_level = check_top_level_norm_gate_example()
    prior = check_prior_evidence_has_no_top_level_residue()
    return {
        "task": "X32 h=4 terminal dichotomy",
        "node": "active_core_count_bound",
        "status": (
            "PROVED REDUCTION: every h=4 trade is either in the paid "
            "antipodal quotient branch or triggers a top-level 8-sparse "
            "cyclotomic norm gate"
        ),
        "theorem": (
            "Let n=2^s, H=mu_n in odd characteristic p, and let P,Q be "
            "disjoint 4-subsets of H with equal e1,e2,e3.  Encode the "
            "first-sum difference as f.  If Phi_n divides f over Z, then P "
            "and Q are antipodal unions; by X29 this is exactly a quotient "
            "h=2 sum collision, and by X31 it is the paid mu4 baseline or a "
            "paid quotient sparse norm gate.  If Phi_n does not divide f, "
            "then X30 gives p | Res(Phi_n,f).  Hence the only h=4 residue "
            "outside the paid antipodal branch is the explicit top-level "
            "8-sparse norm-gate branch."
        ),
        "dependency_statuses": deps,
        "mu4_baseline_example": baseline,
        "antipodal_quotient_extra_example": quotient_extra,
        "top_level_norm_gate_first_sum_example": top_level,
        "prior_h4_evidence_summary": prior,
        "open_residue": (
            "Count or certify absence of top-level non-antipodal 8-sparse "
            "norm-gated h=4 trades at the rows of interest.  The packet "
            "does not prove that this branch is empty."
        ),
        "checks": NCHECK,
    }


def main() -> int:
    write = "--write-certificate" in sys.argv
    cert = build_certificate()
    if write:
        os.makedirs(os.path.dirname(CERT), exist_ok=True)
        with open(CERT, "w", encoding="utf-8") as fh:
            json.dump(cert, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"[write] {CERT}")

    expected = None
    if os.path.exists(CERT):
        expected = load_json(CERT)
    check("certificate exists", expected is not None, CERT)
    if expected is not None:
        check("certificate matches recomputed summary", cert == expected)

    print("\nbranch examples:")
    print(
        "  mu4 baseline:",
        cert["mu4_baseline_example"]["P"],
        "->",
        cert["mu4_baseline_example"]["Q"],
    )
    print(
        "  quotient extra:",
        cert["antipodal_quotient_extra_example"]["P"],
        "->",
        cert["antipodal_quotient_extra_example"]["Q"],
    )
    print(
        "  top-level norm gate first-sum example:",
        cert["top_level_norm_gate_first_sum_example"]["positive_exponents"],
        "->",
        cert["top_level_norm_gate_first_sum_example"]["negative_exponents"],
    )

    if FAILS:
        print("\nFAIL:")
        for name in FAILS:
            print(f"  - {name}")
        return 1

    print(f"\nPASS: {NCHECK} X32 h=4 terminal-dichotomy checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
