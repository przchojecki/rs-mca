#!/usr/bin/env python3
"""Verify the exact arithmetic in quotient_census_window_compiler.md."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import comb, log2
from pathlib import Path


TARGET_EXP = 128
Q_MAX = 2**256 - 1
M = 2**TARGET_EXP
OFFICIAL_RATES = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16)]


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    details: list[str]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def a2_count(N: int, ell: int) -> int:
    """Paper B 2-power antipodal count A_2(N,ell)."""
    require(N > 0 and N % 2 == 0, "N must be positive and even")
    require(0 <= ell <= N, "ell must lie in [0,N]")
    n1 = N // 2
    total = 0
    u = 0
    while ell - 2 * u >= 0:
        t = ell - 2 * u
        if u <= n1 - t and t <= n1:
            total += comb(n1, t) * (2**t)
        u += 1
    return total


def ell_for_rate(N: int, rho: Fraction) -> int | None:
    value = rho * N + 1
    if value.denominator != 1:
        return None
    ell = value.numerator
    if not (0 <= ell <= N):
        return None
    return ell


def exact_count_for_rate(N: int, rho: Fraction) -> int | None:
    ell = ell_for_rate(N, rho)
    if ell is None:
        return None
    return a2_count(N, ell)


def first_relaxed_crossing(rho: Fraction, budget: int, limit: int = 1024) -> tuple[int | None, int | None]:
    last_le: int | None = None
    first_gt: int | None = None
    for N in range(2, limit + 1, 2):
        count = exact_count_for_rate(N, rho)
        if count is None:
            continue
        if count <= budget:
            last_le = N
        elif first_gt is None:
            first_gt = N
            break
    return last_le, first_gt


def first_dyadic_crossing(rho: Fraction, budget: int, max_exp: int = 12) -> tuple[int | None, int | None]:
    last_le: int | None = None
    first_gt: int | None = None
    for exp in range(1, max_exp + 1):
        N = 2**exp
        count = exact_count_for_rate(N, rho)
        if count is None:
            continue
        if count <= budget:
            last_le = N
        elif first_gt is None:
            first_gt = N
            break
    return last_le, first_gt


def q_interval_from_budget_window(lower: int, upper: int, q_max: int = Q_MAX) -> tuple[int, int] | None:
    """Return q with floor(q/2^128) in [lower, upper), clipped to [0,q_max]."""
    require(0 <= lower <= upper, "need 0 <= lower <= upper")
    if lower == upper:
        return None
    lo = lower * M
    hi = upper * M - 1
    lo = max(0, lo)
    hi = min(q_max, hi)
    if lo > hi:
        return None
    return lo, hi


def count_congruence_interval(lo: int, hi: int, modulus: int, residue: int = 1) -> int:
    require(modulus > 0, "positive modulus required")
    if lo > hi:
        return 0
    residue %= modulus
    return (hi - residue) // modulus - ((lo - 1 - residue) // modulus)


def classify_budget(budget: int, lower: int, upper: int) -> str:
    require(lower <= upper, "lower <= upper required")
    if budget < lower:
        return "CERTIFIED_UNSAFE_BY_LOWER"
    if budget >= upper:
        return "CERTIFIED_SAFE_BY_UPPER"
    return "UNDECIDED_WINDOW"


def divisors(n: int) -> list[int]:
    out = []
    for d in range(1, int(n**0.5) + 1):
        if n % d == 0:
            out.append(d)
            if d * d != n:
                out.append(n // d)
    return sorted(out)


def dyadic_profile_count(n: int, k: int, sigma: int) -> dict[str, object]:
    """Exact Paper B quotient-core profile for 2-power rows.

    Returns the maximizing integer binomial count instead of log2(count).
    """

    require(n > 0 and k > 0 and k <= n, "need 0 < k <= n")
    require(n & (n - 1) == 0, "n must be a power of two")
    require(0 <= sigma <= n, "sigma must lie in [0,n]")
    g = k
    require(n % g == 0 or g <= n, "k should divide n in the official dyadic rows")
    active = []
    M = 1
    while M <= k:
        if k % M == 0 and n % M == 0 and sigma < M and k // M <= n // M - 1:
            N = n // M
            ell = k // M
            count = comb(N - 1, ell)
            active.append({"M": M, "N": N, "ell": ell, "count": count})
        M *= 2
    if not active:
        return {"status": "EMPTY", "active": []}
    best = max(active, key=lambda row: row["count"])
    return {"status": "NONEMPTY", "best": best, "active": active}


def generic_profile_count(n: int, k: int, sigma: int) -> dict[str, object]:
    """Definition-level finite max over all divisors of gcd(n,k), for toy checks."""

    from math import gcd

    active = []
    for M in divisors(gcd(n, k)):
        if sigma < M and k // M <= n // M - 1:
            active.append({"M": M, "N": n // M, "ell": k // M, "count": comb(n // M - 1, k // M)})
    if not active:
        return {"status": "EMPTY", "active": []}
    return {"status": "NONEMPTY", "best": max(active, key=lambda row: row["count"]), "active": active}


def check_exact_count_formula() -> CheckResult:
    details = []
    named = {
        (16, 9): 3280,
        (32, 17): 21523360,
    }
    for (N, ell), want in named.items():
        got = a2_count(N, ell)
        require(got == want, f"A_2({N},{ell}) mismatch")
        details.append(f"A_2({N},{ell}) = {got}")

    for exp in range(1, 10):
        N = 2**exp
        n1 = N // 2
        ell = n1 + 1
        got = a2_count(N, ell)
        closed = (3**n1 - 1) // 2
        require(got == closed, f"rate-half closed form failed at N={N}")
    details.append("rate 1/2 closed form (3^(N/2)-1)/2 checked for N=2..512")

    max_bits_400 = 0
    max_bits_512 = 0
    for rho in OFFICIAL_RATES:
        for N in range(2, 401, 2):
            count = exact_count_for_rate(N, rho)
            if count is not None:
                max_bits_400 = max(max_bits_400, count.bit_length())
        for exp in range(1, 10):
            N = 2**exp
            count = exact_count_for_rate(N, rho)
            if count is not None:
                max_bits_512 = max(max_bits_512, count.bit_length())
    details.append(f"all official-rate relaxed counts N<=400 evaluated exactly; max bit length {max_bits_400}")
    details.append(f"all official-rate dyadic counts N<=512 evaluated exactly; max bit length {max_bits_512}")
    return CheckResult("exact 2-power quotient count evaluation", "PASS", details)


def check_bounded_scale_tables() -> CheckResult:
    expected_relaxed = {
        64: {
            Fraction(1, 2): (82, 84),
            Fraction(1, 4): (84, 88),
            Fraction(1, 8): (120, 128),
            Fraction(1, 16): (176, 192),
        },
        96: {
            Fraction(1, 2): (122, 124),
            Fraction(1, 4): (128, 132),
            Fraction(1, 8): (176, 184),
            Fraction(1, 16): (272, 288),
        },
        128: {
            Fraction(1, 2): (162, 164),
            Fraction(1, 4): (172, 176),
            Fraction(1, 8): (240, 248),
            Fraction(1, 16): (368, 384),
        },
    }
    details = []
    for bits, table in expected_relaxed.items():
        budget = 2**bits - 1
        row = []
        for rho in OFFICIAL_RATES:
            got = first_relaxed_crossing(rho, budget)
            require(got == table[rho], f"relaxed crossing mismatch bits={bits}, rho={rho}: {got}")
            row.append(f"{rho}: {got[0]}->{got[1]}")
        details.append(f"budget bits {bits}: " + "; ".join(row))

    dyadic_expected = {
        Fraction(1, 2): (128, 256),
        Fraction(1, 4): (128, 256),
        Fraction(1, 8): (128, 256),
        Fraction(1, 16): (256, 512),
    }
    dyadic = []
    budget_max = Q_MAX // M
    require(budget_max == 2**128 - 1, "unexpected max budget")
    for rho in OFFICIAL_RATES:
        got = first_dyadic_crossing(rho, budget_max)
        require(got == dyadic_expected[rho], f"dyadic crossing mismatch rho={rho}: {got}")
        dyadic.append(f"{rho}: {got[0]}->{got[1]}")
    details.append("dyadic B_max crossings: " + "; ".join(dyadic))
    details.append("relaxed first crossings are <=384; dyadic coarsening reaches 512 only at rate 1/16")
    return CheckResult("bounded exact-count scale census", "PASS", details)


def check_budget_window_arithmetic() -> CheckResult:
    K = a2_count(16, 9)
    L = 3264
    require(K == 3280 and L < K, "window example mismatch")
    interval = q_interval_from_budget_window(L, K)
    require(interval is not None, "expected nonempty interval")
    lo, hi = interval
    require(lo == L * M, "q window lower endpoint mismatch")
    require(hi == K * M - 1, "q window upper endpoint mismatch")

    modulus = 512
    count = count_congruence_interval(lo, hi, modulus, 1)
    expected_count = (K - L) * (M // modulus)
    require(count == expected_count, "congruence-window count mismatch")

    empty = q_interval_from_budget_window(K, K)
    require(empty is None, "L=K should make an empty window")
    require(classify_budget(L - 1, L, K) == "CERTIFIED_UNSAFE_BY_LOWER", "low budget classification")
    require(classify_budget(K, L, K) == "CERTIFIED_SAFE_BY_UPPER", "high budget classification")
    require(classify_budget(L, L, K) == "UNDECIDED_WINDOW", "window classification")

    clipped = q_interval_from_budget_window(2**128 - 5, 2**128 + 10)
    require(clipped is not None and clipped[1] == Q_MAX, "field-range clipping mismatch")
    details = [
        f"A_2(16,9)=K={K}; certified lower L={L}; budget window has {K-L} integer budget values",
        f"q interval: [{lo}, {hi}]",
        f"q == 1 mod {modulus} admissible integers in window: {count}",
        "L=K gives an empty unresolved window",
        "field-range clipping at q<2^256 checked",
    ]
    return CheckResult("exact budget-window arithmetic", "PASS", details)


def check_dyadic_profile_evaluation() -> CheckResult:
    # Definition-level equality on a small row, all integer slacks.
    n, k = 16, 8
    for sigma in range(0, n + 1):
        dy = dyadic_profile_count(n, k, sigma)
        gen = generic_profile_count(n, k, sigma)
        require(dy["status"] == gen["status"], f"profile status mismatch at sigma={sigma}")
        if dy["status"] == "NONEMPTY":
            require(dy["best"] == gen["best"], f"profile best mismatch at sigma={sigma}")

    # Empty boundary: no divisor M of gcd(n,k) can exceed sigma once sigma >= k.
    for rho in OFFICIAL_RATES:
        n = 4096
        k_frac = rho * n
        require(k_frac.denominator == 1, "official test k integral")
        k = k_frac.numerator
        require(dyadic_profile_count(n, k, k)["status"] == "EMPTY", f"empty boundary failed rho={rho}")

    # Bounded-order replay in the near-capacity regime.
    profile_rows = []
    max_order_128 = 0
    max_order_256 = 0
    for rho in OFFICIAL_RATES:
        n = 2**20
        k = int(rho * n)
        for denom in (128, 256):
            sigma = n // denom
            prof = dyadic_profile_count(n, k, sigma)
            require(prof["status"] == "NONEMPTY", f"profile unexpectedly empty rho={rho}, denom={denom}")
            best = prof["best"]
            active = prof["active"]
            max_order = max(row["N"] for row in active)
            if denom == 128:
                max_order_128 = max(max_order_128, max_order)
                require(max_order <= 64, "sigma>=n/128 should force N<=64")
            if denom == 256:
                max_order_256 = max(max_order_256, max_order)
                require(max_order <= 128, "sigma>=n/256 should force N<=128")
            # In all replayed official-rate bounded-order cases, the largest
            # binomial occurs at the smallest active M, equivalently largest N.
            smallest_M = min(row["M"] for row in active)
            require(best["M"] == smallest_M, "best profile scale was not the first active dyadic scale")
            profile_rows.append(
                f"rho={rho}, sigma=n/{denom}: best M={best['M']}, N={best['N']}, "
                f"ell={best['ell']}, count_bits={best['count'].bit_length()}"
            )

    details = [
        "definition-level dyadic evaluator matches the finite divisor max on n=16,k=8 for all sigma",
        "empty boundary checked at sigma >= k for all official rates on n=4096",
        f"sigma>=n/128 forces active quotient order N<=64 in replay; observed max {max_order_128}",
        f"sigma>=n/256 forces active quotient order N<=128 in replay; observed max {max_order_256}",
        *profile_rows,
    ]
    return CheckResult("exact dyadic quotient-profile evaluation", "PASS", details)


CHECKS = [
    check_exact_count_formula,
    check_bounded_scale_tables,
    check_budget_window_arithmetic,
    check_dyadic_profile_evaluation,
]


def run_checks() -> list[CheckResult]:
    return [fn() for fn in CHECKS]


def emit_certificate(results: list[CheckResult]) -> Path:
    repo = Path(__file__).resolve().parents[2]
    out_dir = repo / "experimental" / "data" / "certificates" / "quotient-census-window"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "quotient_census_window_compiler.json"
    payload = {
        "status": "PROVED-COMPILER-ARITHMETIC / 2-POWER QUOTIENT COUNT",
        "note": "experimental/notes/thresholds/quotient_census_window_compiler.md",
        "script": "experimental/scripts/verify_quotient_census_window_compiler.py",
        "dag_nodes": [
            "census_bounded_scales",
            "census_exact_counts",
            "census_window_arithmetic",
            "dyadic_profile_evaluation",
        ],
        "target_exponent": TARGET_EXP,
        "field_range": "q < 2^256",
        "checks": [asdict(result) for result in results],
        "non_claims": [
            "does not resolve quotient collisions below the norm threshold",
            "does not count primes inside admissible-integer q windows",
            "does not prove mixed-radix exact quotient counts",
            "does not prove global quotient-periodic exhaustion",
        ],
    }
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON certificate")
    args = parser.parse_args()

    print("=" * 74)
    print("VERIFY: quotient census window compiler")
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
