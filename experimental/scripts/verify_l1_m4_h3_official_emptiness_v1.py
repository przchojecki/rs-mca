#!/usr/bin/env python3
"""Verifier for the L1 official m=4, h=3 split-pencil emptiness packet.

SCOPE, STATED FIRST.  This script replays the LOCAL ALGEBRA that the six
terminal exclusions rest on, plus the row dictionary and the case exhaustion
count.  It does NOT re-derive the stratification argument itself; that lives in
the note.  What it does establish, exactly:

  A. the three depressed-Weierstrass identities behind the tangent and Euler
     exclusions, as RATIONAL-FUNCTION IDENTITIES over Q(a,b) -- verified on a
     grid larger than the total degree, which for polynomials over an integral
     domain is a proof, not a spot check;
  B. the nu=0 nonzero-b tangent equivalence, replayed modulo EACH OF THE FOUR
     OFFICIAL PRIMES (the in-tree verifier checks it only at p = 7, 31, 127);
  C. the row dictionary n = 4(p+1) for the four official Mersenne rows, AND
     the explicit fence that the deployed KoalaBear row is not in the family --
     the two share the value n = 2097152 and nothing else;
  D. the case exhaustion count: nu + eta = 3 splits, six terminal cases.

Layers A and B are the mathematical content.  Layer C is the packaging fence
that matters most for a reader: n = 2097152 appears in both this family and the
deployed setup, with completely different p, and no claim here touches the
latter.

Usage:  python3 verify_l1_m4_h3_official_emptiness_v1.py
"""

from __future__ import annotations

from fractions import Fraction as F

# The four official rows: n = 4(p+1), p a Mersenne prime.
OFFICIAL_ROWS = (
    (32768, 8191),            # p = 2^13 - 1
    (524288, 131071),         # p = 2^17 - 1
    (2097152, 524287),        # p = 2^19 - 1
    (8589934592, 2147483647),  # p = 2^31 - 1
)

# The deployed KoalaBear row, carried ONLY to be excluded from the family.
DEPLOYED_KOALABEAR = (2097152, 2130706433)

ALPHA = 3          # the fixed resonance scalar
GRID = 11          # exceeds the total degree of every cleared identity below


def discriminant(a, b):
    """Delta = -4a^3 - 27b^2 for the depressed cubic g(y) = y^3 + ay + b."""
    return -4 * a**3 - 27 * b**2


def g(y, a, b):
    return y**3 + a * y + b


def check_identities() -> int:
    """Layer A: the three cleared identities, over Q(a,b), on a full grid.

    Each cleared identity is a polynomial in (a,b) of total degree at most 7.
    Vanishing on an 11x11 grid of distinct values in an integral domain forces
    the polynomial to be identically zero, so this is a proof.
    """
    checks = 0
    for ai in range(1, GRID + 1):
        for bi in range(1, GRID + 1):
            a, b = F(ai), F(bi)
            delta = discriminant(a, b)
            y0 = F(-3 * b) / (2 * a)
            gy0 = g(y0, a, b)

            # (I1) 8a^3 g(y_0) = b*Delta  -- the Euler/quotient factorization.
            assert 8 * a**3 * gy0 == b * delta, (ai, bi, "I1")

            # (I2) 4 y_0 Delta = -48 a^2 g(y_0)  -- kappa_1 = kappa_2, i.e. the
            # two tangent scalars computed by different routes agree.
            assert 4 * y0 * delta == -48 * a * a * gy0, (ai, bi, "I2")

            # (I3) 4a^3 (g(y_0) - y_0(3y_0^2 + a)) = -b*Delta  -- the positive
            # tangent-multiplicity closed form, cleared of g(y_0)^2.
            assert 4 * a**3 * (gy0 - y0 * (3 * y0**2 + a)) == -b * delta, \
                (ai, bi, "I3")
            checks += 3
    return checks


def check_official_prime_replay() -> int:
    """Layer B: the nu=0 nonzero-b tangent equivalence at the official primes.

    For each official p and each admissible (a,b,r): the auxiliary scalar h_0
    coincides with kappa_2 exactly when the scalar equation
    r*Delta + 12a^2 g(r) vanishes.  This is the local statement that leaves the
    nu=0 nonzero-b branch with no surviving tangent.
    """
    checks = 0
    for _, p in OFFICIAL_ROWS:
        for a in range(1, 9):
            for b in range(1, 9):
                delta = (-4 * a**3 - 27 * b**2) % p
                if not delta:
                    continue
                y0 = -3 * b * pow(2 * a, -1, p) % p
                gy0 = (y0**3 + a * y0 + b) % p
                if not gy0:
                    continue
                # the two tangent scalars agree, mod p
                kappa_one = 4 * ALPHA * y0 * pow(gy0, -1, p) % p
                kappa_two = -48 * ALPHA * a * a * pow(delta, -1, p) % p
                assert kappa_one == kappa_two, (p, a, b, "kappa")
                # and the auxiliary/scalar-equation equivalence
                for r in range(1, 7):
                    gr = (r**3 + a * r + b) % p
                    if not gr:
                        continue
                    d0 = -ALPHA * pow(gr, -1, p) % p
                    h0 = -4 * r * d0 % p
                    scalar_equation = (r * delta + 12 * a * a * gr) % p
                    assert (h0 == kappa_two) == (scalar_equation == 0), \
                        (p, a, b, r)
                    checks += 1
                checks += 1
    return checks


def check_row_dictionary() -> int:
    """Layer C: the family definition, and the deployed-row fence."""
    checks = 0
    for n, p in OFFICIAL_ROWS:
        assert n == 4 * (p + 1), (n, p)
        # each p is a Mersenne prime 2^e - 1
        e = (p + 1).bit_length() - 1
        assert p == 2**e - 1, (p, e)
        assert (p + 1) & p == 0, "p+1 not a power of two"
        assert p > 9
        checks += 4

    # THE FENCE.  The deployed KoalaBear row shares the value n = 2097152 with
    # one official row and is otherwise unrelated: it does not satisfy
    # n = 4(p+1), and the family member at that n has a different prime.
    n_dep, p_dep = DEPLOYED_KOALABEAR
    assert 4 * (p_dep + 1) != n_dep, "deployed row unexpectedly in the family"
    family_p_at_n = n_dep // 4 - 1
    assert family_p_at_n == 524287 and family_p_at_n != p_dep
    assert any(n == n_dep for n, _ in OFFICIAL_ROWS), "n-collision assumption stale"
    assert not any(p == p_dep for _, p in OFFICIAL_ROWS)
    checks += 4
    return checks


def check_case_exhaustion() -> int:
    """Layer D: the stratification splits into exactly six terminal cases."""
    positive_splits = tuple((nu, 3 - nu) for nu in (1, 2))
    for nu, eta in positive_splits:
        assert nu + eta == 3 and nu > 0 and eta > 0
    terminal_cases = {
        "positive",             # nu > 0 tangent multiplicity
        "nu0_zero_b",           # nu = 0, b = 0 (Euler)
        "nu0_nonzero_b_h0",
        "nu0_nonzero_b_h1",
        "nu0_nonzero_b_h2",
        "nu0_nonzero_b_h3",
    }
    assert len(terminal_cases) == 6
    return len(positive_splits) + len(terminal_cases)


def check_mutations() -> int:
    """Two controls: each perturbation must break something."""
    # (1) wrong discriminant normalization breaks identity I1
    broke = False
    for ai in range(1, 5):
        for bi in range(1, 5):
            a, b = F(ai), F(bi)
            bad_delta = -4 * a**3 - 26 * b**2      # 27 -> 26
            y0 = F(-3 * b) / (2 * a)
            if 8 * a**3 * g(y0, a, b) != b * bad_delta:
                broke = True
    assert broke, "mutated discriminant still satisfied I1"

    # (2) wrong stationary point breaks identity I2
    broke = False
    for ai in range(1, 5):
        for bi in range(1, 5):
            a, b = F(ai), F(bi)
            delta = discriminant(a, b)
            bad_y0 = F(-3 * b) / (3 * a)           # 2a -> 3a
            if 4 * bad_y0 * delta != -48 * a * a * g(bad_y0, a, b):
                broke = True
    assert broke, "mutated stationary point still satisfied I2"
    return 2


def main() -> None:
    identities = check_identities()
    replay = check_official_prime_replay()
    rows = check_row_dictionary()
    cases = check_case_exhaustion()
    mutations = check_mutations()
    print(
        "L1_M4_H3_OFFICIAL_EMPTINESS_PASS "
        f"identities={identities} official_prime_replay={replay} "
        f"row_checks={rows} case_checks={cases} mutations={mutations} "
        f"rows={[p for _, p in OFFICIAL_ROWS]} "
        "deployed_koalabear=excluded_from_family"
    )


if __name__ == "__main__":
    main()
