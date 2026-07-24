#!/usr/bin/env python3
"""Independent exact-integer verifier for the KoalaBear rank-or-pencil census stop.

Stdlib only, runs in well under a minute.  Recomputes every displayed integer in
the rank-or-pencil census-stop note and in the two Lean modules
(AsymptoticSpine/KoalaBearMergedResidual.lean and
AsymptoticSpine/KoalaBearRankOrPencilS1.lean) from a minimal set of source
primitives, and asserts each recomputation against the printed literal.  Nothing
is imported from the Lean build; the arithmetic is reimplemented here in Python
bignums.

Primitives (the only inputs assumed, taken from the frozen KoalaBear row):
  p_KB = 2130706433              KoalaBear prime  (= 2**31 - 2**24 + 1)
  ext  = 6                       sextic extension degree
  n    = 2097152                 code length
  k    = 1048576                 code dimension
  a    = 1116048                 agreement
  B*   = 274980728111395087      target budget
  U_paid = 981104                paid tangent atom (unconditional)
  U_Q  = 400389155870            tangent-rooted Q-shell cap  (conditional)
  congestionQCap = 442607801512  rival congestion Q cap
  provedQFloor   = 57198030365   unconditional Q floor
  scalarExceptionCap = 1
  onePencilSlopeCap  = 2

Everything else -- fieldOrder, the proper rank-49/50 caps (via the exact
proper-intersection falling-factorial formula), the closure threshold, the
merged-residual cap, the iff boundary, the threshold-derived chart count, the
obstruction-model charges, the fits-below gap, the sibling all-pencil count, the
congestion gap, and the rank-50 overshoot -- is recomputed and checked.

Gates (all must pass for `--check` to exit 0):
  G1  fieldOrder = p_KB**ext, digit-for-digit, and fieldOrder // 2**128 = B*.
  G2  row derivations: redundancy, errorRadius (= U_paid), supportExcess.
  G3  proper caps from the exact formula floor(31*(s+1)*ff(n,s+1)/ff(a,s+1)):
      P_49 = properRank49Cap, P_50 = properRank50Cap.
  G4  ledger chain: B* - U_paid - U_Q = post-Q reserve; floor(reserve/2) =
      closureThreshold; and the sharp closure identities (reserve is B*-1 at the
      bound, B*+1 one past it).
  G5  merged-residual identity: properRank49Cap + 1 + 2*chartCap = closureThreshold.
  G6  threshold-derived chart count: leftover = closureThreshold-properRank49Cap-1,
      chartCap = leftover//2, 2*chartCap = leftover.
  G7  iff boundary is tight: charge(chartCap) = closureThreshold (equality),
      charge(chartCap+1) = closureThreshold+2 (first failing).
  G8  obstruction model: boundary+1 chart count, its 2x slope-token count, the
      collapsed split charge > threshold, and the direct token count < threshold
      by the exact fits-below gap.
  G9  ambient ceiling nonclosing: censusRefutationBoundary < fieldOrder and the
      split with fieldOrder charts overshoots the threshold.
  G10 route-cut siblings: sibling all-pencil count = closureThreshold//2;
      congestion cap = floor((B*-U_paid-congestionQCap)/2), its gap below the
      merged cap; rank-50 overshoot; one-pencil incidence bracket; Q-floor
      consistency; p_KB = 2**31 - 2**24 + 1.

`--tamper-selftest` mutates each pinned literal in turn (+1) and confirms every
mutation is caught by at least one gate; it exits 0 iff all mutations are caught.
"""

import argparse
import sys


# ---------------------------------------------------------------------------
# Values under test.  In --check these are the true source/displayed values.
# In --tamper-selftest each entry is perturbed in turn and the gates must catch it.
# ---------------------------------------------------------------------------
def base_constants():
    return {
        # primitives
        "p_KB": 2_130_706_433,
        "ext": 6,
        "n": 2_097_152,
        "k": 1_048_576,
        "a": 1_116_048,
        "budget": 274_980_728_111_395_087,
        "U_paid": 981_104,
        "U_Q": 400_389_155_870,
        "congestionQCap": 442_607_801_512,
        "provedQFloor": 57_198_030_365,
        "scalarExceptionCap": 1,
        "onePencilSlopeCap": 2,
        # displayed / derived literals to pin
        "fieldOrder": 93_571_093_019_388_561_295_270_373_781_649_880_353_786_165_192_103_559_169,
        "redundancy": 1_048_576,
        "errorRadius": 981_104,
        "supportExcess": 67_472,
        "properRank49Cap": 77_251_422_090_159_989,
        "properRank50Cap": 148_068_539_552_473_273,
        "closureThreshold": 137_490_163_860_629_056,
        "normalizedPencilChartCap": 30_119_370_885_234_533,
        "postQReserve": 274_980_327_721_258_113,
        "leftoverPencilSlopeBudget": 60_238_741_770_469_066,
        "closureMinusProper": 60_238_741_770_469_067,
        "firstFailingCharge": 137_490_163_860_629_058,
        "obstructionChartCount": 60_238_741_770_469_067,
        "obstructionSlopeCount": 120_477_483_540_938_134,
        "obstructionSplitCharge": 197_728_905_631_098_124,
        "fitsBelowGap": 17_012_680_319_690_922,
        "siblingAllPencilCount": 68_745_081_930_314_528,
        "congestionRequiredN": 137_490_142_751_306_235,
        "congestionGap": 21_109_322_821,
        "rank50Overshoot": 10_578_375_691_844_217,
    }


def falling_factorial(nn, kk):
    """nn*(nn-1)*...*(nn-kk+1); exactly Lean's fallingFactorial (kk factors)."""
    acc = 1
    for i in range(kk):
        acc *= (nn - i)
    return acc


def proper_correction_bound(K, s):
    """floor(31*(s+1)*ff(n,s+1)/ff(a,s+1)); the deployed proper-intersection formula."""
    num = 31 * (s + 1) * falling_factorial(K["n"], s + 1)
    den = falling_factorial(K["a"], s + 1)
    return num // den


def run_gates(K):
    """Return list of (gate_name, ok_bool).  Pure function of K."""
    results = []

    def chk(name, cond):
        results.append((name, bool(cond)))

    twoPow128 = 2 ** 128

    # G1 -- field order digit-for-digit and budget quotient
    chk("G1a fieldOrder=p_KB**ext", K["p_KB"] ** K["ext"] == K["fieldOrder"])
    chk("G1b fieldOrder//2**128=budget", K["fieldOrder"] // twoPow128 == K["budget"])

    # G2 -- row derivations
    chk("G2a redundancy=n-k", K["n"] - K["k"] == K["redundancy"])
    chk("G2b errorRadius=n-a", K["n"] - K["a"] == K["errorRadius"])
    chk("G2c errorRadius=U_paid", K["errorRadius"] == K["U_paid"])
    chk("G2d supportExcess=a-k", K["a"] - K["k"] == K["supportExcess"])

    # G3 -- proper caps via the exact formula (independent recompute)
    chk("G3a P_49=properRank49Cap", proper_correction_bound(K, 49) == K["properRank49Cap"])
    chk("G3b P_50=properRank50Cap", proper_correction_bound(K, 50) == K["properRank50Cap"])

    # G4 -- ledger chain + sharp closure
    reserve = K["budget"] - K["U_paid"] - K["U_Q"]
    chk("G4a postQReserve=B*-U_paid-U_Q", reserve == K["postQReserve"])
    chk("G4b threshold=floor(reserve/2)", reserve // 2 == K["closureThreshold"])
    chk(
        "G4c sharp: U_paid+U_Q+2*thr=B*-1",
        K["U_paid"] + K["U_Q"] + 2 * K["closureThreshold"] == K["budget"] - 1,
    )
    chk(
        "G4d sharp: U_paid+U_Q+2*(thr+1)=B*+1",
        K["U_paid"] + K["U_Q"] + 2 * (K["closureThreshold"] + 1) == K["budget"] + 1,
    )

    # G5 -- merged residual identity
    merged = (
        K["properRank49Cap"]
        + K["scalarExceptionCap"]
        + K["onePencilSlopeCap"] * K["normalizedPencilChartCap"]
    )
    chk("G5a mergedResidualCap=closureThreshold", merged == K["closureThreshold"])
    chk(
        "G5b closureThreshold-properRank49Cap",
        K["closureThreshold"] - K["properRank49Cap"] == K["closureMinusProper"],
    )

    # G6 -- threshold-derived chart count
    leftover = K["closureThreshold"] - K["properRank49Cap"] - K["scalarExceptionCap"]
    chk("G6a leftover=thr-proper-1", leftover == K["leftoverPencilSlopeBudget"])
    chk("G6b chartCap=leftover//2", leftover // K["onePencilSlopeCap"] == K["normalizedPencilChartCap"])
    chk(
        "G6c 2*chartCap=leftover",
        K["onePencilSlopeCap"] * K["normalizedPencilChartCap"] == leftover,
    )

    # G7 -- iff boundary tightness
    def charge(nn):
        return K["properRank49Cap"] + K["scalarExceptionCap"] + K["onePencilSlopeCap"] * nn

    chk("G7a charge(chartCap)=threshold", charge(K["normalizedPencilChartCap"]) == K["closureThreshold"])
    chk(
        "G7b charge(chartCap+1)=threshold+2",
        charge(K["normalizedPencilChartCap"] + 1) == K["closureThreshold"] + 2,
    )
    chk("G7c firstFailingCharge=threshold+2", K["closureThreshold"] + 2 == K["firstFailingCharge"])
    chk("G7d charge(chartCap+1)>threshold", charge(K["normalizedPencilChartCap"] + 1) > K["closureThreshold"])

    # G8 -- obstruction model
    boundary = K["closureThreshold"] - K["properRank49Cap"] - K["scalarExceptionCap"]
    obs_charts = boundary + 1
    chk("G8a obstructionChartCount=boundary+1", obs_charts == K["obstructionChartCount"])
    chk(
        "G8b obstructionSlopeCount=2*charts",
        K["onePencilSlopeCap"] * obs_charts == K["obstructionSlopeCount"],
    )
    chk("G8c splitCharge=proper+1+2*charts", charge(obs_charts) == K["obstructionSplitCharge"])
    chk("G8d splitCharge>threshold", charge(obs_charts) > K["closureThreshold"])
    chk(
        "G8e fitsBelowGap=threshold-slopeCount",
        K["closureThreshold"] - K["obstructionSlopeCount"] == K["fitsBelowGap"],
    )
    chk("G8f slopeCount<threshold", K["obstructionSlopeCount"] < K["closureThreshold"])

    # G9 -- ambient ceiling nonclosing
    chk("G9a boundary<fieldOrder", boundary < K["fieldOrder"])
    chk(
        "G9b split(fieldOrder)>threshold",
        K["closureThreshold"] < charge(K["fieldOrder"]),
    )

    # G10 -- route-cut siblings and provenance
    chk(
        "G10a siblingAllPencil=threshold//2",
        K["closureThreshold"] // 2 == K["siblingAllPencilCount"],
    )
    chk(
        "G10b congestionRequiredN",
        (K["budget"] - K["U_paid"] - K["congestionQCap"]) // 2 == K["congestionRequiredN"],
    )
    chk("G10c congestionRequiredN<mergedCap", K["congestionRequiredN"] < merged)
    chk("G10d congestionGap", merged - K["congestionRequiredN"] == K["congestionGap"])
    chk("G10e rank50Overshoot", K["properRank50Cap"] - K["closureThreshold"] == K["rank50Overshoot"])
    chk("G10f threshold<properRank50Cap", K["closureThreshold"] < K["properRank50Cap"])
    chk("G10g incidence 2*errorRadius<=n", 2 * K["errorRadius"] <= K["n"])
    chk("G10h incidence n<3*errorRadius", K["n"] < 3 * K["errorRadius"])
    chk("G10i qFloor<=U_Q", K["provedQFloor"] <= K["U_Q"])
    chk("G10j qFloor<=congestionQCap", K["provedQFloor"] <= K["congestionQCap"])
    # pin the pure-leaf literals so tamper on them is total
    chk("G10k congestionQCap literal", K["congestionQCap"] == 442_607_801_512)
    chk("G10l provedQFloor literal", K["provedQFloor"] == 57_198_030_365)
    chk("G10m U_Q literal", K["U_Q"] == 400_389_155_870)
    chk("G10n p_KB=2**31-2**24+1", K["p_KB"] == 2 ** 31 - 2 ** 24 + 1)
    chk("G10o ext literal", K["ext"] == 6)
    chk("G10p scalarExceptionCap=1", K["scalarExceptionCap"] == 1)
    chk("G10q onePencilSlopeCap=2", K["onePencilSlopeCap"] == 2)

    return results


def do_check(verbose=True):
    K = base_constants()
    results = run_gates(K)
    failed = [name for name, ok in results if not ok]
    if verbose:
        for name, ok in results:
            print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        print(f"\n{len(results) - len(failed)}/{len(results)} checks passed.")
    if failed:
        print("FAILED: " + ", ".join(failed), file=sys.stderr)
        return 1
    print("ALL CHECKS PASSED")
    return 0


def do_tamper_selftest():
    """Every pinned constant, when mutated by +1, must break >=1 gate."""
    base = base_constants()
    # sanity: untampered must be fully green
    if any(not ok for _, ok in run_gates(base)):
        print("SELFTEST ABORT: base constants do not pass all gates", file=sys.stderr)
        return 1
    uncaught = []
    for key in base:
        mutated = dict(base)
        mutated[key] = mutated[key] + 1
        results = run_gates(mutated)
        if all(ok for _, ok in results):
            uncaught.append(key)
    if uncaught:
        print(
            "TAMPER SELFTEST FAILED; mutations NOT caught for: "
            + ", ".join(uncaught),
            file=sys.stderr,
        )
        return 1
    print(f"TAMPER SELFTEST PASSED: all {len(base)} single-constant mutations caught")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="recompute and verify (default)")
    group.add_argument(
        "--tamper-selftest",
        action="store_true",
        help="confirm every pinned constant is sensitive (exit 0 iff all mutations caught)",
    )
    args = parser.parse_args(argv)
    if args.tamper_selftest:
        return do_tamper_selftest()
    return do_check()


if __name__ == "__main__":
    sys.exit(main())
