#!/usr/bin/env python3
"""Route-boundary verifier for the E1 first-band cubic-Hermite norm certificate.

WHAT THIS PACKET CLAIMS.  The cubic-Hermite majorant used to exclude
autocorrelation-variance levels in the `N=256`, folded-profile `(3,4,0)` first
band tests a FIXED, variance-independent Hermite basis against the three
moments

    m_1 = 16,     m_2 = 256 + V,     m_3 = 4096 + 48 V + M_3,

each of which is affine in `(V, M_3)`.  The tested log-form is therefore affine
in `(V, M_3)`, the margin is monotone decreasing in `M_3`, and the exclusion
boundary `M_3^*(V)` is consequently an AFFINE function of `V`.  That function
has a zero near `V = 49.9`: below it the certificate excludes nothing.

This is a ROUTE CUT, not a theorem about collisions.  It says where a named
tool stops working; it does not decide any variance level, and it is not a
counterexample to any exclusion.

WHAT IS VERIFIED HERE, all in exact rational arithmetic with rigorous
Taylor-remainder log bounds (no floating point anywhere):

  1. the affine model of the log-2 coefficient reproduces all FOUR shipped
     coefficients exactly;
  2. the margin functional is monotone decreasing in `M_3` (exact sign);
  3. the three certified thresholds 1947 / 1732 / 1517 at V = 68 / 66 / 64 are
     each reproduced TWO-SIDED -- positive margin at `M_3^*`, negative at
     `M_3^* + 1` -- which pins the threshold exactly;
  4. the boundary slope is bounded strictly inside `(107, 108)`, so the three
     certified integers are collinear-by-structure and not by coincidence;
  5. THE ROUTE CUT: for every even `V` in the live residual range `2..48` the
     margin is already negative at `M_3 = 0`, so the certificate excludes no
     chamber whose third-moment maximum is nonnegative;
  6. `V = 50` still has a positive threshold, so the cut is sharp at the
     even-level granularity: 50 works, 48 does not;
  7. two mutation controls: perturbing the Hermite basis, or the moment
     structure, destroys the reproduction in (3).

Usage:  python3 verify_e1_first_band_variance_route_boundary_v1.py
"""

from __future__ import annotations

from fractions import Fraction as F

# ---------------------------------------------------------------------------
# Shipped constants.  The Hermite basis and the log-2 coefficients below are
# transcribed from the exact rational certificates that produced the three
# published thresholds; they are inputs to this audit, not outputs of it.
# ---------------------------------------------------------------------------

HERMITE = (
    (F(48735, 79507), F(30772, 79507), F(-3445, 1849)),
    (F(4788, 79507), F(-4788, 79507), F(301253, 1475502)),
    (F(-213, 79507), F(213, 79507), F(-4243, 737751)),
    (F(2, 79507), F(-2, 79507), F(71, 1475502)),
)

LOG2_DEN = 2544224

# (V, M_3) -> exact numerator of the log-2 coefficient, as shipped.
SHIPPED_LOG2_NUM = {
    (64, 1517): -555577,
    (64, 1518): -555449,
    (68, 1947): -530489,
    (68, 1948): -530361,
}

# The published exclusion thresholds.
#
# The first three were used to state the affine law.  The last two were
# produced LATER and INDEPENDENTLY, by a separate descent campaign that had no
# access to the law; they are exactly what it predicts, and are carried here as
# an out-of-sample confirmation.  Both groups are pinned two-sided below.
FITTED_THRESHOLDS = {68: 1947, 66: 1732, 64: 1517}
OUT_OF_SAMPLE_THRESHOLDS = {62: 1302, 60: 1087}
CERTIFIED_THRESHOLDS = {**FITTED_THRESHOLDS, **OUT_OF_SAMPLE_THRESHOLDS}

SQUARE_MASS = 16          # m_1: the band's square mass, 3*2^2 + 4*1^2
TAYLOR_TERMS = 40


def atanh_log_bounds(value: F, terms: int) -> tuple[F, F]:
    """Rigorous rational (lower, upper) bounds for log(value), value > 1."""
    parameter = (value - 1) / (value + 1)
    lower = 2 * sum(parameter ** (2 * i + 1) / (2 * i + 1) for i in range(terms))
    degree = 2 * terms + 1
    remainder = 2 * parameter**degree / (degree * (1 - parameter * parameter))
    return lower, lower + remainder


LOG2_LO, LOG2_HI = atanh_log_bounds(F(2), TAYLOR_TERMS)
LOG87_LO, LOG87_HI = atanh_log_bounds(F(8, 7), TAYLOR_TERMS)
LOG6457_LO, LOG6457_HI = atanh_log_bounds(F(64, 57), TAYLOR_TERMS)


def log2_numerator(V: int, M3: int) -> F:
    """The affine model of the shipped log-2 coefficient numerator."""
    return F(-7488) * V + F(128) * M3 - 270521


def form(V: int, M3: int, basis=HERMITE, mass=SQUARE_MASS,
         m2_slope: int = 1, m3_vslope: int = 48) -> tuple[F, F, F]:
    """The tested cubic-Hermite log-form at (V, M_3)."""
    moments = (F(1), F(mass), F(256 + m2_slope * V),
               F(4096 + m3_vslope * V + M3))
    return tuple(sum(c * basis[i][j] for i, c in enumerate(moments))
                 for j in range(3))


def margin_lower(V: int, M3: int, **kw) -> F:
    """Conservative lower bound on the norm margin: > 0 certifies exclusion.

    The log-2 coefficient is negative, so it is paired with the UPPER bound on
    log 2; the two positive coefficients are paired with LOWER bounds.  This is
    the same pairing the shipped certificates use.
    """
    f = form(V, M3, **kw)
    c = F(log2_numerator(V, M3), LOG2_DEN)
    assert c < 0, "log-2 coefficient changed sign; pairing below is invalid"
    assert f[0] > 0 and f[1] > 0, "form coefficient changed sign; re-derive pairing"
    return c * LOG2_HI + f[0] * LOG87_LO + f[1] * LOG6457_LO - f[2]


def margin_upper(V: int, M3: int, **kw) -> F:
    """Optimistic upper bound: < 0 certifies that exclusion FAILS."""
    f = form(V, M3, **kw)
    c = F(log2_numerator(V, M3), LOG2_DEN)
    return c * LOG2_LO + f[0] * LOG87_HI + f[1] * LOG6457_HI - f[2]


def threshold_is(V: int, M3: int, **kw) -> bool:
    """M_3 is the exact threshold at V: excluded at M_3, not excluded above."""
    return margin_lower(V, M3, **kw) > 0 and margin_upper(V, M3 + 1, **kw) < 0


def main() -> None:
    # --- 1. the affine log-2 model reproduces every shipped coefficient ------
    for (V, M3), num in SHIPPED_LOG2_NUM.items():
        got = log2_numerator(V, M3)
        assert got == num, f"log-2 model mismatch at ({V},{M3}): {got} != {num}"

    # --- 2. the margin is strictly monotone decreasing in M_3 ---------------
    # One unit of M_3 moves the form by HERMITE[3] and the log-2 coefficient by
    # 128/LOG2_DEN.  Bound that step above by zero using the pairing that makes
    # it LARGEST, so the conclusion is rigorous.
    step_upper = (F(128, LOG2_DEN) * LOG2_HI
                  + HERMITE[3][0] * LOG87_HI
                  + HERMITE[3][1] * LOG6457_LO
                  - HERMITE[3][2])
    assert step_upper < 0, "margin is not monotone decreasing in M_3"

    # --- 3. the three certified thresholds, each pinned two-sided -----------
    for V, M3 in sorted(CERTIFIED_THRESHOLDS.items(), reverse=True):
        assert threshold_is(V, M3), f"threshold {M3} not reproduced at V={V}"

    # --- 4. the boundary slope lies strictly inside (107, 108) --------------
    # dM_3/dV = (d margin/dV) / (-d margin/dM_3), both bounded rigorously.
    dV_lo = (F(-7488, LOG2_DEN) * LOG2_HI
             + (HERMITE[2][0] + 48 * HERMITE[3][0]) * LOG87_HI
             + (HERMITE[2][1] + 48 * HERMITE[3][1]) * LOG6457_LO
             - (HERMITE[2][2] + 48 * HERMITE[3][2]))
    dV_hi = (F(-7488, LOG2_DEN) * LOG2_LO
             + (HERMITE[2][0] + 48 * HERMITE[3][0]) * LOG87_LO
             + (HERMITE[2][1] + 48 * HERMITE[3][1]) * LOG6457_HI
             - (HERMITE[2][2] + 48 * HERMITE[3][2]))
    step_lower = (F(128, LOG2_DEN) * LOG2_LO
                  + HERMITE[3][0] * LOG87_LO
                  + HERMITE[3][1] * LOG6457_HI
                  - HERMITE[3][2])
    assert dV_lo > 0 and dV_hi > 0, "margin is not increasing in V"
    slope_lo, slope_hi = dV_lo / (-step_lower), dV_hi / (-step_upper)
    assert 107 < slope_lo <= slope_hi < 108, (
        f"boundary slope escaped (107,108): [{float(slope_lo)}, {float(slope_hi)}]")

    # --- 5. THE ROUTE CUT ---------------------------------------------------
    # For every even V in the live residual range, the certificate already
    # fails at M_3 = 0, hence excludes nothing with a nonnegative third moment.
    dead = []
    for V in range(2, 49, 2):
        assert margin_upper(V, 0) < 0, f"certificate still alive at V={V}"
        dead.append(V)
    assert dead == list(range(2, 49, 2))

    # --- 6. sharpness: V=50 still carries a positive threshold --------------
    assert margin_lower(50, 0) > 0, "V=50 should still be excludable at M_3=0"
    fifty = max(m for m in range(0, 400) if margin_lower(50, m) > 0)
    assert threshold_is(50, fifty), "V=50 threshold not pinned two-sided"

    # --- 7. mutation controls ----------------------------------------------
    bad_basis = (HERMITE[0], HERMITE[1], HERMITE[2],
                 (HERMITE[3][0], HERMITE[3][1], HERMITE[3][2] + F(1, 1475502)))
    assert not any(threshold_is(V, M3, basis=bad_basis)
                   for V, M3 in CERTIFIED_THRESHOLDS.items()), \
        "perturbed Hermite basis still reproduced a threshold"
    assert not any(threshold_is(V, M3, m3_vslope=47)
                   for V, M3 in CERTIFIED_THRESHOLDS.items()), \
        "perturbed moment structure still reproduced a threshold"

    print(
        "E1_FIRST_BAND_VARIANCE_ROUTE_BOUNDARY_PASS "
        f"fitted={[FITTED_THRESHOLDS[v] for v in (68, 66, 64)]} "
        f"out_of_sample={[OUT_OF_SAMPLE_THRESHOLDS[v] for v in (62, 60)]} "
        f"slope_in=(107,108) last_live_even_V=50 threshold_at_50={fifty} "
        f"dead_even_V={dead[0]}..{dead[-1]} mutations=2"
    )


if __name__ == "__main__":
    main()
