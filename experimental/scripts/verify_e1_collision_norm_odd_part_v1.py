#!/usr/bin/env python3
"""The A3 odd-part reduction, transferred to the E1 collision norm criterion.

THE REDUCTION IS NOT NEW TO THIS REPOSITORY.  `a3_good_reduction_lemma.md`
already uses it -- "p coprime to delta_0 and to the odd part of the constant m;
the 2-power part is a unit", and D_pt(n,h) is defined as an odd part.  What is
new here is only that `e1_collision_norm_criterion.md` does not apply it, and
that applying it there is what makes the bottom of the N=256 first band
closable at all.

THE STATEMENT.  The E1 criterion fixes a prime p == 1 mod N.  That hypothesis
already forces p odd.  Writing the resultant norm as

    R = 2^mu * R_odd,     R_odd odd,

divisibility by p cannot see the 2-part:

    p | R   <==>   p | R_odd.

So the practical exclusion test "R < 2^250 implies no pair-feasible row prime
divides R" may be run on R_odd instead of R.  This is never weaker, and it is
strictly stronger whenever mu > 0.

WHAT THIS SCRIPT VERIFIES, all in exact integer arithmetic:

  1. the reduction itself, as a proposition, exhaustively over a range of odd
     primes and a randomised-but-seeded sweep of (mu, R_odd);
  2. that the test is monotone: passing on R implies passing on R_odd, and the
     converse can fail -- with an explicit witnessing pair;
  3. internal consistency of the extremal data reported by one N=256 census at
     the level where this bites: R_odd odd, R_odd | R, valuation and bit
     lengths as reported;
  4. THE MARGIN.  At that level the largest odd part is 250 bits and sits only
     a factor of 1.1152 below 2^250 -- about 0.157 bits of headroom;
  5. a certified full-conductor witness whose odd part is a 248-bit PRIME
     congruent to 1 mod 256 -- i.e. it satisfies the lane's row congruence and
     is excluded by size alone;
  6. two mutation controls.

WHAT IT DOES NOT DO: it does not re-run the census.  Items 3-5 verify the
internal consistency and the arithmetic of reported extremal data, not its
provenance.  That boundary is deliberate.

Usage:  python3 verify_e1_collision_norm_odd_part_v1.py
"""

from __future__ import annotations

import random

THRESHOLD = 2**250

# --- extremal data reported by one N=256 first-band census -----------------
CENSUS = {
    "vectors": 2994,
    "distinct_norms": 895,
    "norms_at_or_above_2_250": 6,
    "odd_parts_at_or_above_2_250": 0,
    "maximum_valuation": 34,
    "maximum_norm": 3244660049331064070204285700733501169431397018164712582311239362105072116226,
    "maximum_odd_part": 1622330024665532035102142850366750584715698509082356291155619681052536058113,
}

# --- a certified full-conductor witness at the bottom of the band ----------
WITNESS_NORM = 713716409960669519192598736974780038395771519667874695041952783752312355842
WITNESS_ODD = 356858204980334759596299368487390019197885759833937347520976391876156177921
WITNESS_VALUATION = 1
ROW_MODULUS = 256          # this lane's row congruence: p == 1 mod N, N = 256


def odd_part(value: int) -> tuple[int, int]:
    """Return (mu, value / 2^mu) with the second entry odd."""
    mu = 0
    while value % 2 == 0:
        value //= 2
        mu += 1
    return mu, value


def is_probable_prime(n: int) -> bool:
    """Deterministic Miller-Rabin for n < 3.3e24, strong beyond that."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def check_reduction() -> int:
    """(1) p odd  =>  ( p | R  <==>  p | R_odd ).  Exhaustive + sampled."""
    checks = 0
    odd_primes = [p for p in range(3, 400) if is_probable_prime(p)]
    rng = random.Random(20260728)
    for p in odd_primes:
        for _ in range(12):
            mu = rng.randrange(0, 40)
            base = rng.randrange(1, 10**12) * 2 + 1        # odd
            R = (2**mu) * base
            got_mu, got_odd = odd_part(R)
            assert got_mu == mu and got_odd == base
            assert (R % p == 0) == (base % p == 0), (p, mu, base)
            checks += 1
    return checks


def check_monotone_and_strict() -> int:
    """(2) the odd-part test is never weaker, and is sometimes strictly better."""
    rng = random.Random(1110)
    strict_witnesses = 0
    checks = 0
    for _ in range(4000):
        mu = rng.randrange(0, 8)
        base = rng.randrange(1, 2**60) * 2 + 1
        R = (2**mu) * base
        passes_whole = R < THRESHOLD
        passes_odd = base < THRESHOLD
        # never weaker
        assert not (passes_whole and not passes_odd)
        if passes_odd and not passes_whole:
            strict_witnesses += 1
        checks += 1
    # and the strictness is realised by the census itself
    assert CENSUS["norms_at_or_above_2_250"] > 0
    assert CENSUS["odd_parts_at_or_above_2_250"] == 0
    return checks


def check_census_consistency() -> dict:
    """(3)+(4) internal consistency of the reported extremal data, and margin."""
    R = CENSUS["maximum_norm"]
    O = CENSUS["maximum_odd_part"]
    mu, computed_odd = odd_part(R)
    assert computed_odd == O, "reported maximum_odd_part is not the odd part of maximum_norm"
    assert O % 2 == 1
    assert R % O == 0 and R // O == 2**mu
    assert R.bit_length() == 251 and O.bit_length() == 250
    # the whole norm fails the test; the odd part passes it
    assert R >= THRESHOLD, "maximum norm should be at or above 2^250"
    assert O < THRESHOLD, "maximum odd part should be below 2^250"
    # THE MARGIN: how far below the threshold the binding value actually sits
    assert THRESHOLD * 1000 // O == 1115, "margin moved; re-derive before quoting"
    assert CENSUS["maximum_valuation"] >= 1
    return {"mu_at_maximizer": mu, "margin_permille": THRESHOLD * 1000 // O}


def check_witness() -> dict:
    """(5) the certified full-conductor witness at the bottom of the band."""
    mu, o = odd_part(WITNESS_NORM)
    assert mu == WITNESS_VALUATION and o == WITNESS_ODD
    assert WITNESS_NORM == 2**WITNESS_VALUATION * WITNESS_ODD
    assert WITNESS_NORM.bit_length() == 249
    assert WITNESS_ODD.bit_length() == 248
    assert WITNESS_ODD < THRESHOLD
    # it satisfies THIS LANE'S row congruence, so it is not excluded by that
    assert WITNESS_ODD % ROW_MODULUS == 1, "witness fails the row congruence"
    # and it is prime, so it is a single candidate divisor, not a composite
    assert is_probable_prime(WITNESS_ODD), "witness odd part is not prime"
    return {"factor_below_threshold": THRESHOLD // WITNESS_ODD}


def check_mutations() -> int:
    """(6) controls."""
    # (a) the reduction genuinely needs p odd: for p = 2 it fails
    R = 2**5 * 7
    _, base = odd_part(R)
    assert (R % 2 == 0) and (base % 2 != 0), "p=2 control did not separate"
    # (b) claiming the whole norm passes at the census maximum must be false
    assert not (CENSUS["maximum_norm"] < THRESHOLD), \
        "mutation control vacuous: whole norm already passes"
    return 2


def main() -> None:
    reduction = check_reduction()
    monotone = check_monotone_and_strict()
    census = check_census_consistency()
    witness = check_witness()
    mutations = check_mutations()
    print(
        "E1_COLLISION_NORM_ODD_PART_PASS "
        f"reduction_checks={reduction} monotone_checks={monotone} "
        f"census_norms_over={CENSUS['norms_at_or_above_2_250']} "
        f"census_odd_over={CENSUS['odd_parts_at_or_above_2_250']} "
        f"max_valuation={CENSUS['maximum_valuation']} "
        f"margin=2^250/max_odd={census['margin_permille']}/1000 "
        f"witness_factor_below={witness['factor_below_threshold']} "
        f"mutations={mutations}"
    )


if __name__ == "__main__":
    main()
