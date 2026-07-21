#!/usr/bin/env python3
"""Fail-closed exact-integer replay of the four SS0.4 adjacent-pair crossings.

Independent audit (separate codebase, cross-repo): decides every crossing by
exact big-integer comparison -- no floating point in any decision branch;
floats appear only in the reported margin display. Pins the exact exponent
convention that makes MCA one factor of `p` easier than list:

    list row : unsafe(m)  <=>  C(n,m) > p^(m-K)   * floor(q * eps*)
    MCA  row : unsafe(m)  <=>  C(n,m) > p^(m-K-1) * floor(q * eps*)

(the `-1` = pencil degree of freedom / identity witness at K = k+1).

Also recomputes both field budgets B_* = floor(q * eps*) and checks them
against their independently printed values (RF3'' KoalaBear safe-row budget
at 999b8f3a; the Mersenne budget printed in PR #993).

Mutation self-test: the wrong-exponent, wrong-eps*, and off-by-one-a0
variants must all be REJECTED for the verifier to pass.

Exactness note: one binomial C(n, M0) is computed directly; every other
C(n, m) needed is derived by the exact integer recurrence
C(n, m+1) = C(n, m) * (n-m) // (m+1), whose division is always exact.
Stdlib only; runs in well under a minute. Exit 0 iff every pair, budget,
and mutation control passes.
"""
import math
import sys

N, K = 2 ** 21, 2 ** 20

# (name, p, ext_degree, eps_bits, pencil, a0_unsafe, printed_margin_bits)
ROWS = (
    ("KoalaBear MCA ", 2 ** 31 - 2 ** 24 + 1, 6, 128, 1, 1116047, "22.2"),
    ("KoalaBear list", 2 ** 31 - 2 ** 24 + 1, 6, 128, 0, 1116046, "22.0"),
    ("M31 MCA       ", 2 ** 31 - 1, 4, 100, 1, 1116023, "3.3"),
    ("M31 list      ", 2 ** 31 - 1, 4, 100, 0, 1116022, "3.1"),
)

BUDGET_PINS = {
    # KoalaBear q = p^6, eps* = 2^-128: agrees with the RF3'' KoalaBear
    # safe-row budget printed in the tree at 999b8f3a.
    (2 ** 31 - 2 ** 24 + 1, 6, 128): 274_980_728_111_395_087,
    # Mersenne q = p'^4, eps* = 2^-100 (extra-official convention):
    # agrees with the budget printed in PR #993.
    (2 ** 31 - 1, 4, 100): 16_777_215,
}

# Exact binomial ladder: one direct comb, neighbors by exact ratio steps.
M_LO = 1116021  # one below the smallest m any check touches (1116022 - 1 + safety for M3)
M_HI = 1116048


def build_comb_table() -> dict:
    table = {}
    value = math.comb(N, M_LO)
    table[M_LO] = value
    for m in range(M_LO, M_HI):
        num = value * (N - m)
        value, rem = divmod(num, m + 1)
        assert rem == 0, "binomial ladder division must be exact"
        table[m + 1] = value
    return table


COMB = build_comb_table()


def log2_int(x: int) -> float:
    b = x.bit_length()
    if b <= 64:
        return math.log2(x)
    return (b - 64) + math.log2(x >> (b - 64))


def unsafe(m: int, p: int, gate: int, pencil: int) -> bool:
    """Exact integer decision: C(N,m) > p^(m-K-pencil) * gate."""
    return COMB[m] > pow(p, m - K - pencil) * gate


def check_pair(name, p, e, eps, pencil, a0):
    gate = pow(p, e) >> eps
    pin = BUDGET_PINS.get((p, e, eps))
    if pin is not None and gate != pin:
        raise AssertionError(f"{name}: budget B_* mismatch: {gate} != {pin}")
    if not unsafe(a0, p, gate, pencil):
        raise AssertionError(f"{name}: a0={a0} not unsafe")
    if unsafe(a0 + 1, p, gate, pencil):
        raise AssertionError(f"{name}: a0+1={a0 + 1} not safe")
    margin_u = log2_int(COMB[a0]) - log2_int(pow(p, a0 - K - pencil) * gate)
    margin_s = log2_int(COMB[a0 + 1]) - log2_int(pow(p, a0 + 1 - K - pencil) * gate)
    return margin_u, margin_s


def mutation_controls() -> int:
    """Each semantic corruption must break the printed pair to be caught."""
    caught = 0

    # M1: wrong exponent on an MCA row (drop the pencil dof): the rhs grows
    # by a factor of p, so a0 must stop verifying as unsafe.
    _, p, e, eps, pencil, a0, _ = ROWS[0]
    gate = pow(p, e) >> eps
    if unsafe(a0 + 1, p, gate, pencil - 1) or not unsafe(a0, p, gate, pencil - 1):
        caught += 1

    # M2: wrong eps* on a Mersenne row (official 2^-128 instead of 2^-100):
    # the gate shrinks by 2^28, so a0+1 must stop verifying as safe.
    _, p, e, eps, pencil, a0, _ = ROWS[2]
    bad_gate = pow(p, e) >> 128
    if not unsafe(a0, p, bad_gate, pencil) or unsafe(a0 + 1, p, bad_gate, pencil):
        caught += 1

    # M3: off-by-one a0: the shifted pair (a0-1, a0) must fail the
    # unsafe/safe split because the true a0 is still unsafe.
    _, p, e, eps, pencil, a0, _ = ROWS[1]
    gate = pow(p, e) >> eps
    if not unsafe(a0 - 1, p, gate, pencil) or unsafe(a0, p, gate, pencil):
        caught += 1

    return caught


def main() -> int:
    print(f"{'row':>15} {'a0':>8} {'unsafe@a0':>10} {'safe@a0+1':>10} {'printed':>8}")
    for name, p, e, eps, pencil, a0, printed in ROWS:
        mu, ms = check_pair(name, p, e, eps, pencil, a0)
        print(f"{name:>15} {a0:>8} {'+%.3f' % mu:>10} {'%.3f' % ms:>10} {printed:>8}  PAIR OK")
    caught = mutation_controls()
    if caught != 3:
        raise AssertionError(f"mutation controls caught {caught}/3")
    print("FOUR_PAIR_CROSSING_EXACT_REPLAY_PASS pairs=4 budgets=2 mutations=3/3")
    return 0


if __name__ == "__main__":
    sys.exit(main())
