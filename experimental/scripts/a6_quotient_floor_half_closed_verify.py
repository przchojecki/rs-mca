#!/usr/bin/env python3
"""A6: the prize-rate quotient floor closed form  A(N', ell') = (3^{n1}-1)/2.

Pure standard library. Reproduces Paper B (slackMCA_v4) thm:exactcount at the
prize rate rho = 1/2 (ell' = n1 + 1), and certifies the elementary binomial
parity split that proves it, plus the Pascal recurrence used by the stdlib-Lean
formalization RsMca/A6QuotientFloorClosed.lean.

Run:  python3 a6_quotient_floor_half_closed_verify.py
"""
from math import comb


def quotient_floor(n1, ellp):
    """Paper B A(N'=2 n1, ell') as the exact stdlib foldr (mirrors Lean quotientFloor):
    sum over u>=0 with t=ell'-2u>=0 and u+t<=n1 of choose(n1,t) * 2^t."""
    tot = 0
    for u in range(ellp + 1):
        t = ellp - 2 * u
        if t >= 0 and 2 * u <= ellp and u + t <= n1:
            tot += comb(n1, t) * 2 ** t
    return tot


def odd_sum(n1):
    return sum(comb(n1, t) * 2 ** t for t in range(n1 + 1) if t % 2 == 1)


def even_sum(n1):
    return sum(comb(n1, t) * 2 ** t for t in range(n1 + 1) if t % 2 == 0)


def pep(n):
    """Pascal recurrence (Se,So): the engine of the Lean proof.
    Se(n+1)=Se+2So, So(n+1)=2Se+So, (Se,So)(0)=(1,0)."""
    se, so = 1, 0
    for _ in range(n):
        se, so = se + 2 * so, 2 * se + so
    return se, so


def main():
    fails = []

    # (1) Elementary binomial parity split of (1 +/- 2)^n.
    for n in range(0, 40):
        if odd_sum(n) != (3 ** n - (-1) ** n) // 2:
            fails.append(("odd-split", n))
        if even_sum(n) != (3 ** n + (-1) ** n) // 2:
            fails.append(("even-split", n))

    # (2) Pascal recurrence reproduces the literal choose-sums.
    for n in range(0, 40):
        if pep(n) != (even_sum(n), odd_sum(n)):
            fails.append(("recurrence", n))

    # (3) Re-indexing: at rho=1/2 the active term set is the FULL parity class
    #     opposite to n1 in [0, n1]; floor = that minority sum.
    for n1 in range(1, 60):
        ellp = n1 + 1
        # active u: u >= ell'-n1 = 1 and 2u <= ell'  ->  t = ell'-2u opposite parity to n1
        active_t = {ellp - 2 * u for u in range(ellp + 1)
                    if ellp - 2 * u >= 0 and 2 * u <= ellp and (ellp - u) <= n1}
        full_class = {t for t in range(n1 + 1) if t % 2 == (n1 + 1) % 2}
        if active_t != full_class:
            fails.append(("reindex", n1))
        minority = odd_sum(n1) if n1 % 2 == 0 else even_sum(n1)
        if quotient_floor(n1, ellp) != minority:
            fails.append(("floor=minority", n1))

    # (4) The closed form (3^{n1}-1)/2 holds for BOTH parities of n1.
    for n1 in range(1, 80):
        if quotient_floor(n1, n1 + 1) != (3 ** n1 - 1) // 2:
            fails.append(("closed-form", n1))

    # Named Paper B instances.
    inst = {
        (16, 9): 3280,
        (32, 17): 21523360,
    }
    for (Np, ellp), want in inst.items():
        n1 = Np // 2
        got = quotient_floor(n1, ellp)
        cf = (3 ** n1 - 1) // 2
        print(f"A({Np},{ellp}) = {got}  closed (3^{n1}-1)/2 = {cf}  "
              f"published {want}  ok={got == want == cf}")
        if not (got == want == cf):
            fails.append(("instance", (Np, ellp)))

    print(f"\nkey identity n1=8 : odd_sum={odd_sum(8)} (3^8-1)/2={(3**8-1)//2}")
    print(f"key identity n1=16: odd_sum={odd_sum(16)} (3^16-1)/2={(3**16-1)//2}")
    print(f"\nALL CHECKS PASS: {not fails}")
    if fails:
        print("FAILURES:", fails)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
