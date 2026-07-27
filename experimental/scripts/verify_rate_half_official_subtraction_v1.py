#!/usr/bin/env python3
"""Rate-1/2 official row: subtraction against thm:official, bracket, MDS fence.

This packet leads with a NEGATIVE result about our own material, then keeps the
two pieces that survive it.

  PART 1 (subtraction).  On the official rate-1/2 row n=2^41, k=2^40, the bare
  quadratic staircase (thm:quadratic / the cor:target hypothesis) reaches
  B <= B_Q = 389,500,552,609 -- which is EXACTLY the B already tabulated in
  tab:proth for this rate.  thm:official reaches B <= 2^39 - 2 =
  549,755,813,886, i.e. 41.1% further.  Any "determined family" claim on
  2^128 < q < 2^166.503 is therefore CONCORDANT with thm:official, not novel.
  The residual seam above thm:official is exactly THREE values of B.

  PART 2 (bracket, outside the compiler).  For q >= 2^169 one has
  B* = floor(q/2^128) >= 2^41 > n-k-1, so the cor:target hypothesis fails and
  thm:official does not apply.  There the high-field bracket (HD2) gives
  k + 8,594,128,896 <= a_RH(q) <= 3n/4.

  PART 3 (route cut).  The exact quadratic staircase does NOT extend to the
  next radius by an MDS-only argument: an explicit F_5 instance is column-far
  at radius one and still has four CA-bad finite slopes.  This is replayed here
  in full.

Usage:  python3 verify_rate_half_official_subtraction_v1.py
"""

from __future__ import annotations

N = 2**41
K = 2**40

# His tab:proth entry for rate 1/2.
TAB_PROTH_B_RATE_HALF = 389500552609

# His thm:official, rho = 1/2:  r_sharp = n/4 - 3, safe set determined for
# 1 <= B <= r_sharp + 1.
R_SHARP = N // 4 - 3
OFFICIAL_B_MAX = R_SHARP + 1

# The draft claim (i) seam top, retained only to size the residual.
DRAFT_SEAM_TOP = 2**39 + 1

HD2_LOWER_OFFSET = 8594128896      # a_RH >= k + this, for q >= 2^169


def quadratic_hypothesis(B: int) -> bool:
    """The cor:target / thm:quadratic condition at target count B."""
    return (N - B + 1) ** 2 >= N * (K + B - 1)


def quadratic_reach() -> int:
    """Largest B satisfying the quadratic hypothesis (exact bisection)."""
    lo, hi = 1, N
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if quadratic_hypothesis(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def part1_subtraction() -> dict:
    B_Q = quadratic_reach()
    # the reach is sharp
    assert quadratic_hypothesis(B_Q) and not quadratic_hypothesis(B_Q + 1)
    # and it coincides with his tabulated row
    assert B_Q == TAB_PROTH_B_RATE_HALF, (B_Q, TAB_PROTH_B_RATE_HALF)
    # thm:official strictly dominates it
    assert OFFICIAL_B_MAX > B_Q
    gap = OFFICIAL_B_MAX - B_Q
    assert gap == 160255261277, gap
    # so our claimed family sits strictly inside his determined range
    assert B_Q <= OFFICIAL_B_MAX
    # residual seam above thm:official, using the draft's own top
    residual = list(range(OFFICIAL_B_MAX + 1, DRAFT_SEAM_TOP + 1))
    assert residual == [2**39 - 1, 2**39, 2**39 + 1], residual
    assert len(residual) == 3
    return {"B_Q": B_Q, "official_max": OFFICIAL_B_MAX, "gap": gap,
            "residual": residual}


def part2_bracket() -> dict:
    """q >= 2^169 lies outside cor:target's hypothesis; state the bracket."""
    q_min = 2**169
    B_star = q_min // 2**128
    assert B_star == 2**41
    # cor:target requires B <= n - k - 1; it fails here, so thm:official is mute
    assert B_star > N - K - 1
    assert not quadratic_hypothesis(B_star)
    lower = K + HD2_LOWER_OFFSET
    upper = 3 * N // 4
    assert lower < upper, (lower, upper)
    assert upper == 1649267441664
    # the bracket sits strictly above the message dimension and below 3n/4
    assert K < lower < upper < N
    return {"B_star_at_2_169": B_star, "compiler_applies": False,
            "lower": lower, "upper": upper}


def part3_mds_fence() -> dict:
    """Replay the F_5 column-far radius-one instance with four CA-bad slopes."""
    p = 5
    # parity-check column directions h_x = (1, x), x in D = {0,1,2,3}
    h = {x: (1, x) for x in range(4)}
    y0, y1 = (0, 1), (1, 4)
    # the four claimed (lambda, mu, column) incidences
    claimed = {1: (1, 0), 2: (2, 2), 3: (3, 1), 4: (4, 3)}
    hits = []
    for lam in range(1, p):
        combo = ((y0[0] + lam * y1[0]) % p, (y0[1] + lam * y1[1]) % p)
        mu, col = claimed[lam]
        target = ((mu * h[col][0]) % p, (mu * h[col][1]) % p)
        assert combo == target, (lam, combo, target)
        hits.append((lam, mu, col))
    # exactly four distinct CA-bad finite slopes, on four distinct columns
    assert len(hits) == 4
    assert len({c for _, _, c in hits}) == 4
    # sanity: the two syndromes are independent, so the pair is genuinely a pair
    det = (y0[0] * y1[1] - y0[1] * y1[0]) % p
    assert det != 0, "syndromes are proportional; not a valid received pair"
    # mutation control: perturbing one syndrome must break at least one incidence
    broke = False
    bad_y1 = (1, 3)
    for lam in range(1, p):
        combo = ((y0[0] + lam * bad_y1[0]) % p, (y0[1] + lam * bad_y1[1]) % p)
        mu, col = claimed[lam]
        if combo != ((mu * h[col][0]) % p, (mu * h[col][1]) % p):
            broke = True
    assert broke, "mutated syndrome still reproduced every incidence"
    return {"bad_slopes": len(hits), "distinct_columns": 4}


def main() -> None:
    p1 = part1_subtraction()
    p2 = part2_bracket()
    p3 = part3_mds_fence()
    print(
        "RATE_HALF_OFFICIAL_SUBTRACTION_PASS "
        f"B_Q={p1['B_Q']} (== tab:proth rate-1/2) "
        f"thm_official_max={p1['official_max']} "
        f"domination_gap={p1['gap']} residual_seam={len(p1['residual'])} "
        f"compiler_applies_at_2^169={p2['compiler_applies']} "
        f"bracket=[k+{HD2_LOWER_OFFSET},{p2['upper']}] "
        f"mds_fence_bad_slopes={p3['bad_slopes']}"
    )


if __name__ == "__main__":
    main()
