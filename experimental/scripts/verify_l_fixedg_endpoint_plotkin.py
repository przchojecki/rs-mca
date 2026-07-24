#!/usr/bin/env python3
"""Verify the M31 fixed-G ordinary boundary endpoint Plotkin theorem.

Recomputes every integer in

    experimental/notes/thresholds/m31_fixed_g_boundary_endpoint_plotkin_v1.md

from the frozen deployed parameters: the one-coordinate constant-weight
Plotkin chain, the exact finite-p target-list Johnson grid, the parent
Johnson-denominator middle interval, the adjacent-shell route stop, and the
budget margins.  The coding-theory proof (Theorem 2.1) lives in the note; this
standard-library verifier checks only its exact arithmetic shadow -- the same
object the Lean package ``LFixedGEndpointPlotkin`` kernel-checks.

Every proof-critical gate raises an explicit exception, so the checks stay
active under ``python -O``.

    --check            recompute and verify every integer (default);
    --tamper-selftest  prove that proof-critical mutations fail closed
                       (exit 0 iff every injected mutation is caught).

Frozen parameters are taken from
``experimental/notes/thresholds/m31_fixed_g_universal_rs_embedding_v1.md``.
Pure standard library; runs in well under one second.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction
from typing import Any, Callable

# --- frozen deployed parameters (universal RS embedding note, parameter block) ---
P = 2**31 - 1            # 2147483647
A_DOMAIN = 1_116_023     # |S0|, deployed anchor block
R = 981_129              # |E0|, boundary length N
K = 2**20                # 1048576, deployed dimension
W = A_DOMAIN - K         # 67447, slack w = a - K
B_STAR = 2**24 - 1       # 16777215
ELL = B_STAR - 1         # 16777214, target ordinary-list upper

# the two Johnson-negative endpoints (d, m); both reduce to weight s = 72859
LOW = {"d": 5_412, "m": 72_859, "errors": 908_270}
HIGH = {"d": 840_823, "m": 908_270, "errors": 72_859}

SCHEMA_ID = "m31-fixed-g-endpoint-plotkin-summary-v1"
THEOREM_ID = "M31_FIXED_G_ORDINARY_BOUNDARY_ENDPOINT_PLOTKIN_V1"


class VerificationError(RuntimeError):
    """Raised whenever an exact verifier gate fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    """Fail closed without relying on assertions (active under ``python -O``)."""
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


# --------------------------------------------------------------------------- #
# Exact Johnson helpers (note Section 4, formula 4.1).
# --------------------------------------------------------------------------- #
def johnson_lhs(a: int) -> int:
    return (ELL - 1) * (P * a - R) ** 2


def johnson_rhs(d: int) -> int:
    return R**2 * (P - 1) ** 2 * (ELL - 1) - R * (P - 1) * P * ELL * (R - (d - 1))


def johnson_M(d: int, a: int) -> int:
    """Cleared-square-root Johnson value; agreement a is covered iff M >= 0."""
    return johnson_lhs(a) - johnson_rhs(d)


def johnson_covered(d: int, a: int) -> bool:
    """Independent exact-rational Johnson test (no trust in formula 4.1).

    Covered iff relative error e <= J_{p,ell}(delta_min).  Clearing the square
    root exactly: with t = 1 - e*p/(p-1), covered iff t >= 0 and t^2 >= 1-c*delta.
    """
    e = Fraction(R - a, R)
    delta = Fraction(R - d + 1, R)
    c = Fraction(P, P - 1) * Fraction(ELL, ELL - 1)
    inside = 1 - c * delta
    t = 1 - e * Fraction(P, P - 1)
    if inside < 0:
        return t >= 0
    if t < 0:
        return False
    return t * t >= inside


def first_covered(d: int, lo: int, hi: int) -> int:
    for a in range(lo, hi + 1):
        if johnson_covered(d, a):
            return a
    raise VerificationError(f"no covered agreement for d={d} in [{lo},{hi}]")


def limiting_first(d: int, lo: int, hi: int) -> int:
    for m in range(lo, hi + 1):
        if m * m >= R * (d - 1):
            return m
    raise VerificationError(f"no limiting-covered agreement for d={d}")


def ceildiv(x: int, y: int) -> int:
    return (x + y - 1) // y


# --------------------------------------------------------------------------- #
# Summary: recompute every claimed integer from the frozen primitives.
# --------------------------------------------------------------------------- #
def build_summary() -> dict[str, Any]:
    D = W + 1
    s = min(LOW["m"], R - LOW["m"])
    nprime = R - 1
    k = s - 1
    dnp = D * nprime
    inc = k * (nprime - k)
    plotkin_p = dnp - inc
    q_cap = dnp // plotkin_p
    q_rem = dnp % plotkin_p
    ell_cap = (R * q_cap) // s
    ell_rem = (R * q_cap) % s
    fixed_g = ell_cap + 1

    # adjacent-shell route stop (note Section 6), weight s' = 72860
    adj_s = s + 1
    one_shortening_deficit = (adj_s - 1) * (R - adj_s) - D * (R - 1)
    a2_len = R - 2
    a2_wt = adj_s - 2
    a2_num = D * a2_len
    a2_den = a2_num - a2_wt * (a2_len - a2_wt)
    a2_cap = a2_num // a2_den
    a2_rem = a2_num % a2_den
    route_cap = 30_682_446

    return {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "status": "PROVED",
        "impact": "LOCAL_ONLY",
        "parameters": {"p": P, "R": R, "w": W, "K": K, "a": A_DOMAIN,
                       "B_star": B_STAR, "ell": ELL},
        "endpoints": {
            "low": dict(LOW), "high": dict(HIGH),
            "D": D, "s": s, "nprime": nprime, "k": k,
        },
        "plotkin": {
            "D_nprime": dnp, "incidence_product": inc, "denominator_P": plotkin_p,
            "shortened_cap_Q": q_cap, "shortened_cap_remainder": q_rem,
            "ordinary_list_cap_L": ell_cap, "pullback_remainder": ell_rem,
        },
        "margins": {
            "ell_minus_L": ELL - ell_cap,
            "fixed_g_ball_cap": fixed_g,
            "B_star_minus_fixed_g": B_STAR - fixed_g,
        },
        "johnson_finite": {
            # signed M values; note Section 4 table (M<0 uncovered, M>0 covered)
            "low_M_72861": johnson_M(LOW["d"], 72_861),
            "low_M_72862": johnson_M(LOW["d"], 72_862),
            "low_M_row_72859": johnson_M(LOW["d"], LOW["m"]),
            "high_M_row_908270": johnson_M(HIGH["d"], HIGH["m"]),
            "high_M_908271": johnson_M(HIGH["d"], 908_271),
            "low_first_covered": first_covered(LOW["d"], 72_855, 72_870),
            "high_first_covered": first_covered(HIGH["d"], 908_265, 908_280),
            "low_exact_johnson_errors": R - 72_862,
            "high_exact_johnson_errors": R - 908_271,
            "low_post_johnson_gap": LOW["errors"] - (R - 72_862),
            "high_post_johnson_gap": HIGH["errors"] - (R - 908_271),
        },
        "johnson_limiting": {
            "low_deficit": R * (LOW["d"] - 1) - LOW["m"] ** 2,
            "high_deficit": R * (HIGH["d"] - 1) - HIGH["m"] ** 2,
            "low_first": limiting_first(LOW["d"], 72_850, 72_870),
            "high_first": limiting_first(HIGH["d"], 908_260, 908_280),
        },
        "interval": {
            # parent Johnson denominator m^2 - R(d-1), d=m-w; nonpositive on [72859,908270]
            "fam_72858": (72_858) ** 2 - R * ((72_858 - W) - 1),
            "fam_72859": (72_859) ** 2 - R * ((72_859 - W) - 1),
            "fam_908270": (908_270) ** 2 - R * ((908_270 - W) - 1),
            "fam_908271": (908_271) ** 2 - R * ((908_271 - W) - 1),
        },
        "route_stop": {
            "one_shortening_reverse_deficit": one_shortening_deficit,
            "adj2_length": a2_len, "adj2_weight": a2_wt,
            "adj2_numerator": a2_num, "adj2_denominator": a2_den,
            "adj2_cap": a2_cap, "adj2_remainder": a2_rem,
            "route_cap": route_cap,
            "route_first_ceiling": ceildiv(route_cap * adj_s, R),
            "route_second_ceiling": ceildiv(ceildiv(route_cap * adj_s, R) * (adj_s - 1), R - 1),
            "route_succ_first_ceiling": ceildiv((route_cap + 1) * adj_s, R),
            "route_succ_second_ceiling": ceildiv(ceildiv((route_cap + 1) * adj_s, R) * (adj_s - 1), R - 1),
            "route_excess_over_target": route_cap - ELL,
        },
    }


# --------------------------------------------------------------------------- #
# verify_summary: independently recompute from the module primitives (never
# from the summary's stored derived values) and require equality.
# --------------------------------------------------------------------------- #
def verify_summary(s: dict[str, Any]) -> None:
    require(s["schema"] == SCHEMA_ID, "schema")
    require(s["theorem_id"] == THEOREM_ID, "theorem_id")
    require(s["status"] == "PROVED", "status")
    require(s["impact"] == "LOCAL_ONLY", "impact")

    pr = s["parameters"]
    require(pr["p"] == 2**31 - 1 == P, "p == 2^31-1")
    require(pr["B_star"] == 2**24 - 1 == B_STAR, "B_star == 2^24-1")
    require(pr["w"] == A_DOMAIN - K == W, "w == a-K")
    require(pr["ell"] == B_STAR - 1 == ELL, "ell == B_star-1")
    require(pr["R"] == R and pr["K"] == K and pr["a"] == A_DOMAIN, "frozen R,K,a")

    ep = s["endpoints"]
    D = W + 1
    require(ep["D"] == D == 67_448, "D == w+1")
    for tag, row in (("low", LOW), ("high", HIGH)):
        er = ep[tag]
        require(er["m"] == row["d"] + W, f"{tag} m == d+w")
        require(er["m"] + er["errors"] == R, f"{tag} m+errors == R")
        require(er["m"] - er["d"] + 1 == D, f"{tag} D == m-d+1")
        require(min(er["m"], R - er["m"]) == 72_859, f"{tag} s == 72859")
    require(R - LOW["m"] == HIGH["m"] and R - HIGH["m"] == LOW["m"], "complement symmetry")
    s_wt = 72_859
    require(ep["s"] == s_wt, "s value")
    require(ep["nprime"] == R - 1, "nprime")
    require(ep["k"] == s_wt - 1, "k")

    # --- Plotkin chain ---
    pl = s["plotkin"]
    nprime, k = R - 1, s_wt - 1
    dnp = D * nprime
    inc = k * (nprime - k)
    plotkin_p = dnp - inc
    require(pl["D_nprime"] == dnp == 66_175_121_344, "D*nprime")
    require(pl["incidence_product"] == inc == 66_174_735_660, "incidence product")
    require(pl["denominator_P"] == plotkin_p == 385_684, "Plotkin denominator P")
    require(plotkin_p > 0, "P > 0 (Theorem 2.1 hypothesis)")
    q_cap = dnp // plotkin_p
    require(pl["shortened_cap_Q"] == q_cap == 171_578, "shortened cap Q")
    require(pl["shortened_cap_remainder"] == dnp % plotkin_p == 231_992, "Q remainder")
    require(q_cap * plotkin_p + (dnp % plotkin_p) == dnp, "Q recompose")
    ell_cap = (R * q_cap) // s_wt
    require(pl["ordinary_list_cap_L"] == ell_cap == 2_310_492, "ordinary list cap L")
    require(pl["pullback_remainder"] == (R * q_cap) % s_wt == 14_934, "pullback remainder")
    require(ell_cap * s_wt + (R * q_cap) % s_wt == R * q_cap, "L recompose")
    # Theorem 2.2 closed form floor((N/s) floor(D(N-1)/P))
    require((R * (D * (R - 1) // plotkin_p)) // s_wt == 2_310_492, "thm 2.2 closed form")
    require(ell_cap <= ELL, "L <= ell")

    mg = s["margins"]
    require(mg["ell_minus_L"] == ELL - ell_cap == 14_466_722, "safety margin ell-L")
    require(mg["fixed_g_ball_cap"] == ell_cap + 1 == 2_310_493, "fixed-G anchor addback")
    require(mg["fixed_g_ball_cap"] <= B_STAR, "fixed-G ball <= B_star")
    require(mg["B_star_minus_fixed_g"] == B_STAR - (ell_cap + 1) == 14_466_722, "fixed-G margin")

    # --- finite-p Johnson grid ---
    jf = s["johnson_finite"]
    require(jf["low_M_72861"] == johnson_M(LOW["d"], 72_861), "low M(72861) value")
    require(jf["low_M_72861"] < 0, "low M(72861) < 0")
    require(jf["low_M_72862"] == johnson_M(LOW["d"], 72_862), "low M(72862) value")
    require(jf["low_M_72862"] > 0, "low M(72862) > 0")
    require(jf["low_M_row_72859"] == johnson_M(LOW["d"], LOW["m"]), "low M(row) value")
    require(jf["low_M_row_72859"] < 0, "low row uncovered")
    require(jf["high_M_row_908270"] == johnson_M(HIGH["d"], HIGH["m"]), "high M(row) value")
    require(jf["high_M_row_908270"] < 0, "high row uncovered")
    require(jf["high_M_908271"] == johnson_M(HIGH["d"], 908_271), "high M(908271) value")
    require(jf["high_M_908271"] > 0, "high M(908271) > 0")
    # exact note-table magnitudes (digit-for-digit)
    require(-jf["low_M_72861"] == 8_221_003_905_619_924_567_540_362_320_760, "low |M(72861)|")
    require(jf["low_M_72862"] == 3_053_765_018_644_647_902_938_550_527_393, "low M(72862) exact")
    require(-jf["high_M_row_908270"] == 34_579_558_183_296_310_721_328_734_410_451, "high |M(row)|")
    require(jf["high_M_908271"] == 105_968_468_789_629_159_598_961_272_090_208, "high M(908271) exact")
    # independent exact-rational Johnson threshold (no trust in formula 4.1)
    require(jf["low_first_covered"] == first_covered(LOW["d"], 72_855, 72_870) == 72_862, "low first-covered 72862")
    require(jf["high_first_covered"] == first_covered(HIGH["d"], 908_265, 908_280) == 908_271, "high first-covered 908271")
    require(not johnson_covered(LOW["d"], LOW["m"]), "indep: low row uncovered")
    require(not johnson_covered(HIGH["d"], HIGH["m"]), "indep: high row uncovered")
    require(jf["low_exact_johnson_errors"] == R - 72_862 == 908_267, "low Johnson errors")
    require(jf["high_exact_johnson_errors"] == R - 908_271 == 72_858, "high Johnson errors")
    require(jf["low_post_johnson_gap"] == LOW["errors"] - 908_267 == 3, "low post-Johnson gap")
    require(jf["high_post_johnson_gap"] == HIGH["errors"] - 72_858 == 1, "high post-Johnson gap")

    # --- limiting quadratic Johnson ---
    jl = s["johnson_limiting"]
    require(jl["low_deficit"] == R * (LOW["d"] - 1) - LOW["m"] ** 2 == 455_138, "low classical deficit")
    require(jl["high_deficit"] == R * (HIGH["d"] - 1) - HIGH["m"] ** 2 == 455_138, "high classical deficit")
    require(jl["low_first"] == limiting_first(LOW["d"], 72_850, 72_870) == 72_863, "low limiting agreement")
    require(jl["high_first"] == limiting_first(HIGH["d"], 908_260, 908_280) == 908_271, "high limiting agreement")

    # --- parent Johnson-denominator middle interval ---
    iv = s["interval"]

    def fam(m: int) -> int:
        return m * m - R * ((m - W) - 1)

    require(iv["fam_72858"] == fam(72_858) == 380_274, "fam(72858) outside > 0")
    require(iv["fam_72859"] == fam(72_859) == -455_138, "fam(72859) endpoint")
    require(iv["fam_908270"] == fam(908_270) == -455_138, "fam(908270) endpoint")
    require(iv["fam_908271"] == fam(908_271) == 380_274, "fam(908271) outside > 0")
    require(iv["fam_72858"] > 0 and iv["fam_908271"] > 0, "interval strictly positive outside")
    require(all(fam(m) <= 0 for m in (72_859, 72_860, 490_564, 908_269, 908_270)),
            "interval nonpositive inside [72859,908270]")

    # --- adjacent-shell route stop ---
    rs = s["route_stop"]
    adj_s = s_wt + 1
    require(rs["one_shortening_reverse_deficit"]
            == (adj_s - 1) * (R - adj_s) - D * (R - 1) == 449_727, "one-shortening reverse deficit")
    require(D * (R - 1) - (adj_s - 1) * (R - adj_s) < 0, "one-shortening denominator negative")
    a2_len, a2_wt = R - 2, adj_s - 2
    a2_num = D * a2_len
    a2_den = a2_num - a2_wt * (a2_len - a2_wt)
    require(rs["adj2_length"] == a2_len == 981_127, "adj2 length")
    require(rs["adj2_weight"] == a2_wt == 72_858, "adj2 weight")
    require(rs["adj2_numerator"] == a2_num == 66_175_053_896, "adj2 numerator")
    require(rs["adj2_denominator"] == a2_den == 391_094, "adj2 denominator")
    require(a2_den > 0, "adj2 denominator positive")
    require(rs["adj2_cap"] == a2_num // a2_den == 169_204, "adj2 cap")
    require(rs["adj2_remainder"] == a2_num % a2_den == 384_720, "adj2 remainder")
    require(rs["route_cap"] == 30_682_446, "route cap")
    require(rs["route_first_ceiling"] == ceildiv(30_682_446 * adj_s, R) == 2_278_521, "route first ceiling")
    require(rs["route_second_ceiling"] == ceildiv(2_278_521 * (adj_s - 1), R - 1) == 169_204, "route second ceiling")
    require(rs["route_succ_first_ceiling"] == ceildiv((30_682_446 + 1) * adj_s, R) == 2_278_522, "route succ first ceiling")
    require(rs["route_succ_second_ceiling"] == ceildiv(2_278_522 * (adj_s - 1), R - 1) == 169_205, "route succ second ceiling")
    require(rs["route_second_ceiling"] <= 169_204 < rs["route_succ_second_ceiling"], "route cap is maximal")
    require(rs["route_excess_over_target"] == 30_682_446 - ELL == 13_905_232, "route excess over target")


# --------------------------------------------------------------------------- #
# Mutation self-test: every proof-critical field, corrupted, must be caught.
# --------------------------------------------------------------------------- #
Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def mutation_suite() -> list[Mutation]:
    return [
        ("schema", lambda s: s.__setitem__("schema", "wrong")),
        ("theorem", lambda s: s.__setitem__("theorem_id", "wrong")),
        ("status", lambda s: s.__setitem__("status", "ROW_CLOSURE")),
        ("impact", lambda s: s.__setitem__("impact", "ROW_CLOSURE")),
        ("param-p", lambda s: s["parameters"].__setitem__("p", P + 1)),
        ("param-ell", lambda s: s["parameters"].__setitem__("ell", ELL + 1)),
        ("endpoint-low-m", lambda s: s["endpoints"]["low"].__setitem__("m", 72_860)),
        ("endpoint-D", lambda s: s["endpoints"].__setitem__("D", 67_449)),
        ("endpoint-s", lambda s: s["endpoints"].__setitem__("s", 72_860)),
        ("plotkin-Dnp", lambda s: s["plotkin"].__setitem__("D_nprime", 66_175_121_345)),
        ("plotkin-incidence", lambda s: s["plotkin"].__setitem__("incidence_product", 66_174_735_661)),
        ("plotkin-P", lambda s: s["plotkin"].__setitem__("denominator_P", 385_685)),
        ("plotkin-Q", lambda s: s["plotkin"].__setitem__("shortened_cap_Q", 171_579)),
        ("plotkin-Qrem", lambda s: s["plotkin"].__setitem__("shortened_cap_remainder", 231_993)),
        ("plotkin-L", lambda s: s["plotkin"].__setitem__("ordinary_list_cap_L", 2_310_493)),
        ("plotkin-Lrem", lambda s: s["plotkin"].__setitem__("pullback_remainder", 14_935)),
        ("margin-ellL", lambda s: s["margins"].__setitem__("ell_minus_L", 14_466_723)),
        ("margin-fixedg", lambda s: s["margins"].__setitem__("fixed_g_ball_cap", 2_310_492)),
        ("margin-bstar", lambda s: s["margins"].__setitem__("B_star_minus_fixed_g", 14_466_721)),
        ("johnson-low-M72861", lambda s: s["johnson_finite"].__setitem__("low_M_72861", johnson_M(LOW["d"], 72_861) + 1)),
        ("johnson-low-M72862", lambda s: s["johnson_finite"].__setitem__("low_M_72862", johnson_M(LOW["d"], 72_862) + 1)),
        ("johnson-low-row", lambda s: s["johnson_finite"].__setitem__("low_M_row_72859", johnson_M(LOW["d"], 72_862))),  # flip sign +
        ("johnson-high-row", lambda s: s["johnson_finite"].__setitem__("high_M_row_908270", johnson_M(HIGH["d"], 908_271))),  # flip sign +
        ("johnson-high-908271", lambda s: s["johnson_finite"].__setitem__("high_M_908271", johnson_M(HIGH["d"], 908_271) + 1)),
        ("johnson-low-firstcov", lambda s: s["johnson_finite"].__setitem__("low_first_covered", 72_861)),
        ("johnson-high-firstcov", lambda s: s["johnson_finite"].__setitem__("high_first_covered", 908_270)),
        ("johnson-low-errors", lambda s: s["johnson_finite"].__setitem__("low_exact_johnson_errors", 908_268)),
        ("johnson-low-gap", lambda s: s["johnson_finite"].__setitem__("low_post_johnson_gap", 2)),
        ("johnson-high-gap", lambda s: s["johnson_finite"].__setitem__("high_post_johnson_gap", 0)),
        ("limiting-low-deficit", lambda s: s["johnson_limiting"].__setitem__("low_deficit", 455_139)),
        ("limiting-low-first", lambda s: s["johnson_limiting"].__setitem__("low_first", 72_862)),
        ("interval-fam72858", lambda s: s["interval"].__setitem__("fam_72858", -1)),
        ("interval-fam72859", lambda s: s["interval"].__setitem__("fam_72859", 0)),
        ("interval-fam908271", lambda s: s["interval"].__setitem__("fam_908271", -1)),
        ("route-one-shortening", lambda s: s["route_stop"].__setitem__("one_shortening_reverse_deficit", 449_728)),
        ("route-adj2-num", lambda s: s["route_stop"].__setitem__("adj2_numerator", 66_175_053_897)),
        ("route-adj2-den", lambda s: s["route_stop"].__setitem__("adj2_denominator", 391_095)),
        ("route-adj2-cap", lambda s: s["route_stop"].__setitem__("adj2_cap", 169_205)),
        ("route-adj2-rem", lambda s: s["route_stop"].__setitem__("adj2_remainder", 384_721)),
        ("route-cap", lambda s: s["route_stop"].__setitem__("route_cap", 30_682_447)),
        ("route-first-ceil", lambda s: s["route_stop"].__setitem__("route_first_ceiling", 2_278_522)),
        ("route-second-ceil", lambda s: s["route_stop"].__setitem__("route_second_ceiling", 169_205)),
        ("route-succ-second", lambda s: s["route_stop"].__setitem__("route_succ_second_ceiling", 169_204)),
        ("route-excess", lambda s: s["route_stop"].__setitem__("route_excess_over_target", 13_905_231)),
    ]


def run_mutation_selftest(summary: dict[str, Any]) -> dict[str, Any]:
    passed: list[str] = []
    for name, mutate in mutation_suite():
        candidate = copy.deepcopy(summary)
        mutate(candidate)
        try:
            verify_summary(candidate)
        except VerificationError:
            passed.append(name)
        else:
            raise VerificationError(f"mutation escaped detection: {name}")
    require(len(passed) == len(mutation_suite()), "all mutations detected")
    return {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "mutation_selftest": "PASS",
        "mutations_detected": len(passed),
        "mutation_names": passed,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="recompute and verify every integer (default)")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    parser.add_argument("--mutation-selftest", "--tamper-selftest",
                        dest="mutation_selftest", action="store_true",
                        help="prove that proof-critical mutations fail closed")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = build_summary()
    verify_summary(summary)
    if args.mutation_selftest:
        output = run_mutation_selftest(summary)
    else:
        output = {"schema": SCHEMA_ID, "theorem_id": THEOREM_ID,
                  "verify": "PASS", "checks": CHECKS,
                  "ordinary_list_cap_L": summary["plotkin"]["ordinary_list_cap_L"],
                  "fixed_g_ball_cap": summary["margins"]["fixed_g_ball_cap"],
                  "safety_margin": summary["margins"]["ell_minus_L"]}
    print(json.dumps(output, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
