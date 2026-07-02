#!/usr/bin/env python3
"""Verify the compiler arithmetic in paid_ledger_functions.md."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import comb
from pathlib import Path


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    details: list[str]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def ceil_div(a: int, b: int) -> int:
    require(b > 0, "positive denominator required")
    return -(-a // b)


def paid_tan_hi(n: int, k: int, A: int) -> dict[str, int | str]:
    require(0 <= k <= n, "need 0 <= k <= n")
    require(0 <= A <= n, "need 0 <= A <= n")
    r = n - A
    radius_cap = (n - k) // 3
    if 0 <= r <= radius_cap:
        return {
            "status": "EXACT_HIGH_AGREEMENT",
            "numerator": r + 1,
            "radius": r,
            "radius_cap": radius_cap,
        }
    return {
        "status": "UNAVAILABLE_OUTSIDE_HIGH_AGREEMENT",
        "radius": r,
        "radius_cap": radius_cap,
    }


def quotient_support_safe_sum(n: int, threshold: int, divisors: list[int]) -> int:
    require(0 <= threshold <= n, "threshold must be in [0,n]")
    require(divisors, "divisor set must be nonempty")
    require(all(c > 0 and n % c == 0 for c in divisors), "each c must divide n")
    total = 0
    for c in sorted(set(divisors)):
        for A in range(threshold, n + 1):
            m, s = divmod(A, c)
            total += comb(n // c, m) * comb(n - c * m, s)
    return total


def quotient_supports_by_enumeration(n: int, threshold: int, divisors: list[int]) -> set[frozenset[int]]:
    """Small exact support union for arithmetic checks.

    The domain is represented by indices 0..n-1, split into consecutive c-fibers.
    This is enough to check the support-union versus safe-sum arithmetic; it is
    not a field-valued quotient-image scanner.
    """

    from itertools import combinations

    require(n <= 20, "toy enumerator is intentionally small")
    all_idx = set(range(n))
    supports: set[frozenset[int]] = set()
    for A in range(threshold, n + 1):
        for c in sorted(set(divisors)):
            m, s = divmod(A, c)
            fibers = [set(range(start, start + c)) for start in range(0, n, c)]
            for chosen in combinations(range(len(fibers)), m):
                full: set[int] = set()
                for idx in chosen:
                    full.update(fibers[idx])
                rest = sorted(all_idx - full)
                for residual in combinations(rest, s):
                    S = frozenset(full | set(residual))
                    if len(S) == A:
                        supports.add(S)
    return supports


def norm_exact_gate(q_line: int, quotient_order: int, rho: Fraction) -> bool:
    require(q_line > 1, "q_line must be > 1")
    require(quotient_order > 0, "positive quotient order required")
    ell = rho * quotient_order + 1
    require(ell.denominator == 1, "rho*N' must be integral for this cell")
    ell_i = ell.numerator
    return (2 * ell_i) ** quotient_order <= q_line**2


def quotient_zone(q_line: int, quotient_order: int, rho: Fraction, *, cap_floor: bool = False) -> str:
    if norm_exact_gate(q_line, quotient_order, rho):
        return "ZONE_A_NORM_EXACT"
    if cap_floor:
        return "ZONE_C_CAP_FLOOR"
    return "ZONE_B_COLLISION_OPEN_INTERVAL"


def extension_only_cell(q_line: int, q_gen: int) -> dict[str, int | str]:
    require(q_line >= q_gen > 0, "need q_line >= q_gen > 0")
    if q_line == q_gen:
        return {"status": "ZERO_GENERATING", "numerator": 0}
    return {"status": "PROPER_EXTENSION", "field_gap": q_line - q_gen}


def extension_pole_floor(q_line: int, q_gen: int, k: int, list_size: int) -> int:
    require(0 < q_gen < q_line, "need a proper extension")
    require(k > 0 and list_size > 0, "k and list_size must be positive")
    gap = q_line - q_gen
    return ceil_div(list_size * gap, gap + k * list_size)


def extension_chart_upper(q_gen: int, charts: list[tuple[int, int]]) -> int:
    """Sum Delta*q_gen^e over (Delta,e) chart data."""

    require(q_gen > 0, "q_gen must be positive")
    total = 0
    for delta, dim in charts:
        require(delta >= 0 and dim >= 0, "chart degree/dimension must be nonnegative")
        total += delta * (q_gen**dim)
    return total


def check_tangent_function() -> CheckResult:
    n, k = 512, 256
    q = 17**32
    budget = q // 2**128
    a506 = paid_tan_hi(n, k, 506)
    a507 = paid_tan_hi(n, k, 507)
    a426 = paid_tan_hi(n, k, 426)
    require(budget == 6, "unexpected F_17^32 budget")
    require(a506["status"] == "EXACT_HIGH_AGREEMENT" and a506["numerator"] == 7, "A=506 mismatch")
    require(a507["status"] == "EXACT_HIGH_AGREEMENT" and a507["numerator"] == 6, "A=507 mismatch")
    require(a426["status"] == "UNAVAILABLE_OUTSIDE_HIGH_AGREEMENT", "A=426 should be outside high agreement")

    swept = 0
    for nn in range(2, 50):
        for kk in range(1, nn + 1):
            cap = (nn - kk) // 3
            for A in range(0, nn + 1):
                cell = paid_tan_hi(nn, kk, A)
                active = cell["status"] == "EXACT_HIGH_AGREEMENT"
                require(active == (0 <= nn - A <= cap), "tangent range predicate mismatch")
                swept += 1
    return CheckResult(
        "Paid_tan high-agreement partial function",
        "PASS",
        [
            f"F_17^32 budget floor(17^32/2^128) = {budget}",
            f"A=506 cell: {a506}",
            f"A=507 cell: {a507}",
            f"A=426 cell: {a426}",
            f"swept {swept} small (n,k,A) range predicates",
        ],
    )


def check_quotient_support_function() -> CheckResult:
    n, threshold, divisors = 12, 8, [2, 3]
    exact_supports = quotient_supports_by_enumeration(n, threshold, divisors)
    safe_sum = quotient_support_safe_sum(n, threshold, divisors)
    require(len(exact_supports) <= safe_sum, "support union exceeds safe sum")
    require(len(exact_supports) == 182, "toy support-union count changed")
    require(safe_sum == 213, "toy safe-sum count changed")

    monotone = []
    previous = None
    for A in range(0, n + 1):
        value = quotient_support_safe_sum(n, A, divisors)
        if previous is not None:
            require(value <= previous, "safe sum should decrease as threshold increases")
        previous = value
        monotone.append(value)

    zone80 = quotient_zone(2**256, 80, Fraction(1, 2))
    zone82 = quotient_zone(2**256, 82, Fraction(1, 2))
    require(zone80 == "ZONE_A_NORM_EXACT", "N'=80 should pass norm gate at q=2^256")
    require(zone82 == "ZONE_B_COLLISION_OPEN_INTERVAL", "N'=82 should be zone-b at q=2^256")
    zone82_cap = quotient_zone(2**256, 82, Fraction(1, 2), cap_floor=True)
    require(zone82_cap == "ZONE_C_CAP_FLOOR", "cap-floor override failed")

    return CheckResult(
        "Paid_quot support function and zone tags",
        "PASS",
        [
            f"toy n={n}, A={threshold}, divisors={divisors}: exact support union = {len(exact_supports)}",
            f"safe support sum = {safe_sum}",
            "safe sum is monotone decreasing in the threshold A",
            f"rate 1/2, q=2^256: N'=80 -> {zone80}; N'=82 -> {zone82}",
            f"cap-floor override: N'=82 -> {zone82_cap}",
        ],
    )


def check_extension_function() -> CheckResult:
    generating = extension_only_cell(17**32, 17**32)
    require(generating == {"status": "ZERO_GENERATING", "numerator": 0}, "generating extension cell mismatch")

    proper = extension_only_cell(17**32, 17)
    require(proper["status"] == "PROPER_EXTENSION", "proper extension not detected")
    require(proper["field_gap"] == 17**32 - 17, "field gap mismatch")

    p = 2**31 - 2**24 + 1
    q = p**6
    k = 2**20
    list_size = ceil_div(comb(256, 130), p)
    pole = extension_pole_floor(q, p, k, list_size)
    require(pole > q // 2**128, "KoalaBear-style extension pole should cross 2^-128 numerator gate")
    require(extension_pole_floor(5**2, 5, 3, 1) == 1, "small pole floor mismatch")
    require(extension_pole_floor(5**2, 5, 3, 10) == 4, "larger pole floor mismatch")

    charts = [(2, 0), (3, 1), (1, 2)]
    chart_upper = extension_chart_upper(5, charts)
    require(chart_upper == 2 + 3 * 5 + 25, "chart upper mismatch")
    normalized = Fraction(chart_upper, 5**3)

    return CheckResult(
        "Paid_ext generating guard, pole floor, and chart upper",
        "PASS",
        [
            f"generating F_17^32 cell: {generating}",
            f"proper extension field gap example: {proper['field_gap']}",
            f"KoalaBear-style L=ceil(C(256,130)/p) has extension-pole numerator {pole}",
            f"q/2^128 budget floor = {q // 2**128}",
            f"toy chart upper over q_gen=5, charts={charts}: {chart_upper}, normalized={normalized}",
        ],
    )


CHECKS = [
    check_tangent_function,
    check_quotient_support_function,
    check_extension_function,
]


def run_checks() -> list[CheckResult]:
    return [fn() for fn in CHECKS]


def emit_certificate(results: list[CheckResult]) -> Path:
    repo = Path(__file__).resolve().parents[2]
    out_dir = repo / "experimental" / "data" / "certificates" / "paid-ledger-functions"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "paid_ledger_functions.json"
    payload = {
        "status": "PROVED-COMPILER-ARITHMETIC / CITED-LEDGER INTERFACE",
        "note": "experimental/notes/thresholds/paid_ledger_functions.md",
        "script": "experimental/scripts/verify_paid_ledger_functions.py",
        "dag_nodes": ["paid_tan_fn", "paid_quot_fn", "paid_ext_fn"],
        "checks": [asdict(result) for result in results],
        "non_claims": [
            "does not prove global quotient-periodic exhaustion",
            "does not resolve zone-b quotient collisions",
            "does not prove the aperiodic local limit",
            "does not classify every extension-valued residual chart",
        ],
    }
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON certificate")
    args = parser.parse_args()

    print("=" * 74)
    print("VERIFY: paid ledger functions")
    print("=" * 74)
    results: list[CheckResult] = []
    failed = 0
    for fn in CHECKS:
        try:
            result = fn()
        except AssertionError as exc:
            failed += 1
            print(f"\n[FAIL] {fn.__name__}")
            print(f"       {exc}")
            continue
        results.append(result)
        print(f"\n[{result.status}] {result.name}")
        for line in result.details:
            print(f"       {line}")
    print("\n" + "-" * 74)
    print(f"implemented PASS: {len(results)}   FAIL: {failed}")
    if failed:
        raise SystemExit(1)
    if args.emit:
        out = emit_certificate(results)
        print(f"emitted: {out.relative_to(Path(__file__).resolve().parents[2])}")


if __name__ == "__main__":
    main()
