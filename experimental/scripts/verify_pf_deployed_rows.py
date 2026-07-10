#!/usr/bin/env python3
"""Deployed-row failure map for the degree-uniform (PF) certificate.

Hard input (b) of agents.md ("image-scale MI + MA, or a direct Sidon
payment"), adversarial lane "mismatch between asymptotic proof and finite
deployed rows".

Target: experimental/asymptotic_rs_mca_frontiers.tex @ 4e3c4ee (unchanged at
this packet's base).  def:prefix-flat-range (the pointwise minor-arc range,
the degree-uniform sufficient certificate for (MI) per admissibility (A4))
reads, with Lambda = C0 (Delta_pole + 1) sqrt|B| + |P| (circle twin-cosets:
2 C0 (Delta_pole + 1) sqrt|B|):

    (PF):  R log|B| + log C(Lambda+m-1, m) - log C(|T|, m)  <=  o(|T|).

rem:pf-numerical rewrites this for finite certificates as the exact
comparison |B|^R C(Lambda+m-1, m) <= e^{o(N)} C(N, m) -- "For finite
certificates this is the minor-character check."  This packet performs that
check, zero-slack, at the four printed v13 deployed rows (identity-prefix
chart: |T| = n = 2^21, m = a, R = w, |B| = p), against the in-tree frozen
floors of profile-envelope-numerics:

    kb_mca   a0=1116047/a1=1116048   p = 2^31-2^24+1  (smooth)
    kb_list  a0=1116046/a1=1116047   same field
    m31_mca  a0=1116023/a1=1116024   p = 2^31-1       (circle, factor 2)
    m31_list a0=1116022/a1=1116023   same field

Result: PF-exact fails at every chart at the most favorable parameters
(C0 = 1, Delta_pole = 0, |P| = 0, sqrt floored), by +280,001.27 to
+471,797.39 bits; the largest Lambda for which it holds is Lambda* in
{2, 3, 4}, versus the Weil-forced Lambda >= 46,159 (kb) / 92,680 (m31
circle).  The surplus is monotone increasing in C0, Delta_pole, |P|, so no
admissible parameter assignment flips any chart.  This is the finite
effective complement of prop:pf-deep-prefix-barrier (which proves the
asymptotic failure of the degree-uniform certificate in the deep regime
Lambda_N >= cN; the deployed rows sit at Lambda ~ 2.2%-4.4% of N, a regime
that proposition does not cover), and it calibrates the pointwise power-sum
bound that the repaired certificate thm:prefix-flatness-power-sum (PF')
would need at deployed scale: |P_j(alpha)| <= Lambda* in {2, 3, 4}.

NOT claimed: nothing about the asymptotic (PF) (along a fixed-field family
the surplus is Theta(sqrt(p) log n) = o(n): consistent); nothing about the
effective-span variant (log A_N in place of R log|B| -- ambient failure
does not imply effective failure, and A_N is not evaluable while the atlas
input (a) is open); nothing about (MA) or the phase-dependent (PF').

All verdict quantities are exact big integers (Legendre factorization +
product tree; binomial cross-validated against math.comb and against the
eight frozen in-tree floor integers).  Surpluses are printed to 2 decimals
from exact integers via a top-900-bit mantissa.  stdlib only,
deterministic, no timing in any output.

Status: EXPERIMENTAL / AUDIT
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL / AUDIT"
SCHEMA = "pf-deployed-rows-v1"
CERT_REL = Path(
    "experimental/data/certificates/pf-deployed-rows/pf_deployed_rows.json")
TEX_REL = Path("experimental/asymptotic_rs_mca_frontiers.tex")
TEX_BASE_SHA = "4e3c4ee85cb01ef7c4f1e7bbfbc13735cf6c9d15"
NUMERICS_REL = Path(
    "experimental/data/certificates/profile-envelope-numerics/"
    "profile_envelope_numerics.json")
PIN_LABELS = (
    "def:prefix-flat-range",
    "def:major-arc-aggregate",
    "def:aggregate-minor-payment",
    "prop:pf-deep-prefix-barrier",
    "prop:pf-ma-square-dichotomy",
    "thm:prefix-flatness-power-sum",
    "prop:weighted-weil-minor-arcs",
    "cor:sidon-payment-from-prefix-flatness",
    "prop:frontier-weil-separation",
    "rem:pf-numerical",
)

N = 2 ** 21
K_DIM = 2 ** 20
P_KB = 2 ** 31 - 2 ** 24 + 1
P_M31 = 2 ** 31 - 1

ROWS = [
    # row_id, kind, p, ext_deg, target_bits, a0, circle?
    ("kb_mca", "mca", P_KB, 6, 128, 1116047, False),
    ("kb_list", "list", P_KB, 6, 128, 1116046, False),
    ("m31_mca", "mca", P_M31, 4, 100, 1116023, True),
    ("m31_list", "list", P_M31, 4, 100, 1116022, True),
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    clone = dict(obj)
    clone.pop("payload_sha256", None)
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def log2_big(x: int) -> float:
    """log2 of a positive big int via top-900-bit mantissa (deterministic)."""
    bl = x.bit_length()
    if bl <= 900:
        return math.log2(x)
    shift = bl - 900
    return math.log2(x >> shift) + shift


def log2_ratio(num: int, den: int) -> float:
    return log2_big(num) - log2_big(den)


def v2(x: int) -> int:
    v = 0
    while x % 2 == 0:
        x //= 2
        v += 1
    return v


# ------------------------------------------------- exact binomials (route A)
_SIEVE_LIMIT = 2 ** 21
_PRIMES: list[int] | None = None


def _primes() -> list[int]:
    global _PRIMES
    if _PRIMES is None:
        sieve = bytearray([1]) * (_SIEVE_LIMIT + 1)
        sieve[0] = sieve[1] = 0
        for i in range(2, math.isqrt(_SIEVE_LIMIT) + 1):
            if sieve[i]:
                sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
        _PRIMES = [i for i, b in enumerate(sieve) if b]
    return _PRIMES


def _prod_tree(xs: list[int]) -> int:
    if not xs:
        return 1
    while len(xs) > 1:
        nxt = [xs[i] * xs[i + 1] for i in range(0, len(xs) - 1, 2)]
        if len(xs) % 2:
            nxt.append(xs[-1])
        xs = nxt
    return xs[0]


def fast_comb(n: int, k: int) -> int:
    """Exact C(n, k) via Legendre exponents + product tree, n <= 2^21."""
    if k < 0 or k > n:
        return 0
    if n > _SIEVE_LIMIT:
        raise ValueError("fast_comb: n exceeds sieve limit")
    nk = n - k
    factors = []
    for p in _primes():
        if p > n:
            break
        e, pk = 0, p
        while pk <= n:
            e += n // pk - k // pk - nk // pk
            pk *= p
        if e:
            factors.append(p ** e)
    return _prod_tree(factors)


_COMB_CACHE: dict[int, int] = {}


def comb_n(a: int) -> int:
    if a not in _COMB_CACHE:
        _COMB_CACHE[a] = fast_comb(N, a)
    return _COMB_CACHE[a]


def pf_exact(p: int, R: int, m: int, lam: int):
    """(holds, surplus_bits) for p^R * C(lam+m-1, m) <= C(N, m)."""
    lhs = pow(p, R) * fast_comb(lam + m - 1, m)
    rhs = comb_n(m)
    return lhs <= rhs, log2_ratio(lhs, rhs)


def lambda_flip_threshold(p: int, R: int, m: int) -> int:
    """Largest Lambda >= 1 with p^R * C(Lambda+m-1, m) <= C(N, m)."""
    rhs = comb_n(m)
    pR = pow(p, R)
    lam = 0
    val = pR                      # Lambda = 1: C(m, m) = 1
    while val <= rhs:
        lam += 1
        val = val * (lam + m) // lam
        if lam > 10 ** 6:
            raise RuntimeError("flip threshold loop ran away")
    return lam


# ----------------------------------------------------------- pins & oracle
def scan_pins(root: Path) -> tuple[dict[str, Any], bool]:
    lines = (root / TEX_REL).read_text(encoding="utf-8").splitlines()
    pins: dict[str, Any] = {}
    ok = True
    for lab in PIN_LABELS:
        entry = {"found": False, "line": 0, "sha256_line": ""}
        for i, line in enumerate(lines, 1):
            if ("\\label{%s}" % lab) in line:
                entry = {
                    "found": True,
                    "line": i,
                    "sha256_line": hashlib.sha256(
                        line.encode("utf-8")).hexdigest()[:16],
                }
                break
        ok = ok and entry["found"]
        pins[lab] = entry
    return pins, ok


def load_numerics(root: Path) -> dict[str, Any]:
    """Frozen in-tree floors (the oracle this packet is gated against).

    deployed_rows is a list of row objects keyed by "row_id"; re-key it,
    and normalize the per-chart field names (L_list_floor,
    Eprof_identity_lower)."""
    data = json.loads((root / NUMERICS_REL).read_text(encoding="utf-8"))
    out = {}
    for row in data["deployed_rows"]:
        charts = {}
        for tag in ("a0", "a1"):
            c = row[tag]
            charts[tag] = {"a": c["a"], "w": c["w"],
                           "L": c["L_list_floor"],
                           "Eprof_lo": c["Eprof_identity_lower"]}
        out[row["row_id"]] = {"B_star": row["B_star"],
                              "q_line": row["q_line"], **charts}
    return out


# ------------------------------------------------------------- certificate
def build_certificate(root: Path) -> dict[str, Any]:
    pins, pins_ok = scan_pins(root)
    dep = load_numerics(root)

    checks: list[tuple[str, bool]] = []

    def chk(name: str, ok: bool) -> None:
        checks.append((name, bool(ok)))

    # binomial route self-validation vs math.comb (small/medium)
    for (nn, kk) in ((100, 37), (2048, 1027), (65536, 30000),
                     (1162205, 46158)):
        chk("fast_comb(%d,%d) == math.comb" % (nn, kk),
            fast_comb(nn, kk) == math.comb(nn, kk))

    # field certificates
    chk("kb p == 2^31-2^24+1", P_KB == 2130706433)
    chk("m31 p == 2^31-1", P_M31 == 2147483647)
    chk("kb v2(p-1) == 24 >= 21", v2(P_KB - 1) == 24)
    chk("m31 v2(p-1) == 1 (base smooth route unavailable)",
        v2(P_M31 - 1) == 1)
    chk("m31 v2(p+1) == 31 >= 21 (circle route)", v2(P_M31 + 1) == 31)

    rows_out: dict[str, Any] = {}
    for row_id, kind, p, ext, tbits, a0, circle in ROWS:
        exp = dep[row_id]
        K = K_DIM + 1 if kind == "mca" else K_DIM
        sqrtp = math.isqrt(p)
        factor = 2 if circle else 1
        bstar = (p ** ext) >> tbits
        chk("%s B* == floor(p^%d/2^%d) == frozen" % (row_id, ext, tbits),
            bstar == exp["B_star"])
        charts: dict[str, Any] = {}
        for tag, a in (("a0", a0), ("a1", a0 + 1)):
            e = exp[tag]
            w = a - K
            chk("%s/%s w == a-K == frozen w" % (row_id, tag), w == e["w"])
            cna = comb_n(a)
            pw = pow(p, w)
            L = -(-cna // pw)
            chk("%s/%s L == ceil(C(n,a)/p^w) == frozen floor"
                % (row_id, tag), L == e["L"])
            eprof = 1 + (N - a + 1) + L
            chk("%s/%s identity lower == frozen" % (row_id, tag),
                eprof == e["Eprof_lo"])

            lam0 = factor * sqrtp          # C0=1, Dpole=0, |P|=0
            holds0, surplus0 = pf_exact(p, w, a, lam0)
            lam_star = lambda_flip_threshold(p, w, a)
            chk("%s/%s PF-exact FAILS at most-favorable Lambda"
                % (row_id, tag), not holds0)
            chk("%s/%s Lambda* < 10 << Weil-forced Lambda"
                % (row_id, tag), 1 <= lam_star < 10)

            # exact Delta_pole sweep (0,1,2); monotone in Lambda thereafter
            sweep = {}
            for dlt in (0, 1, 2):
                _, s = pf_exact(p, w, a, factor * (dlt + 1) * sqrtp)
                sweep["Dpole=%d" % dlt] = "%+.2f" % s
            # sub-admissible robustness probe: C0 = 1/2 (Lambda floored)
            _, s_half = pf_exact(p, w, a, factor * sqrtp // 2)
            sweep["C0=1/2"] = "%+.2f" % s_half
            charts[tag] = {
                "a": a, "w": w, "L_floor": L, "eprof_identity_lower": eprof,
                "lambda_most_favorable": lam0,
                "pf_exact_holds": holds0,
                "pf_surplus_bits": "%+.2f" % surplus0,
                "pf_surplus_bits_per_coordinate": "%.4f" % (surplus0 / N),
                "lambda_flip_threshold": lam_star,
                "surplus_sweep_exact_bits": sweep,
                "log2_barN0_bits": "%.4f" % log2_ratio(cna, pw),
            }
        # printed-margin reproduction (tab-level oracle)
        La0, La1 = charts["a0"]["L_floor"], charts["a1"]["L_floor"]
        chk("%s a0 exceeds B*, a1 does not" % row_id,
            La0 > bstar and La1 <= bstar)
        rows_out[row_id] = {
            "kind": kind, "p": p, "ext_deg": ext, "target_bits": tbits,
            "circle": circle, "circle_factor": factor,
            "sqrt_p_floor": sqrtp, "B_star": bstar,
            "pass_margin_bits_a0": "%+.4f" % log2_ratio(La0, bstar),
            "fail_margin_bits_a1": "%+.4f" % (-log2_ratio(bstar, La1)),
            "charts": charts,
        }

    n_fail = sum(1 for _, ok in checks if not ok)
    all_pass = n_fail == 0 and pins_ok

    cert: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "object": ("exact zero-slack evaluation of the degree-uniform (PF) "
                   "certificate (def:prefix-flat-range) at the four printed "
                   "v13 deployed rows, identity-prefix chart"),
        "hard_input": "b",
        "adversarial_lane": ("mismatch between asymptotic proof and finite "
                             "deployed rows"),
        "tex_path": str(TEX_REL),
        "base_sha": TEX_BASE_SHA,
        "numerics_oracle": str(NUMERICS_REL),
        "pins": pins,
        "pins_ok": pins_ok,
        "chart_identification": {
            "T": "n = 2^21 (full domain)", "m": "a (agreement)",
            "R": "w = a - K (prefix depth; K = k+1 for mca, k for list)",
            "B": "p (base field)",
            "validation": ("ceil of ambient scale barN0 = C(n,a)/p^w "
                           "reproduces all 8 frozen floor integers exactly "
                           "(gated above), and both printed margin pairs "
                           "per row"),
        },
        "rows": rows_out,
        "checks_total": len(checks),
        "checks_failed": n_fail,
        "all_pass": all_pass,
        "score_convention_reconciliation": {
            "note": ("fourier-sidon-payment's toy menu scores the same "
                     "quantity (score = PF surplus in bits) with a toy "
                     "cutoff score/|T| < 0.5.  At the deployed rows the "
                     "per-coordinate surplus is 0.1335 (kb) / 0.2250 (m31) "
                     "-- under that toy cutoff -- while the zero-slack "
                     "exact form fails by +280k/+472k bits.  Both are "
                     "consistent: the o(|T|) slack is exactly the open "
                     "question, and along a fixed-field family the surplus "
                     "is Theta(sqrt(p) log n) = o(n).  Parameter deltas: "
                     "toys there use C0=2 and round sqrt up; this packet "
                     "uses the most favorable C0=1 and isqrt."),
        },
        "verdict": "NO ISSUE",
        "theorem_problem_id": ("def:prefix-flat-range; rem:pf-numerical; "
                               "prop:pf-deep-prefix-barrier; "
                               "thm:prefix-flatness-power-sum"),
        "falsifiable": True,
        "weave": "quantifies the A4/(PF) cell left OPEN by #497; supplies "
                 "the deployed-row PF certificates #500 does_not_assert; "
                 "disjoint from #527's SFM1 hypothesis-ratio separation",
        "summary": {
            "verdict": "NO ISSUE",
            "hard_input_b_status": ("OPEN (unchanged; only the "
                                    "degree-uniform (PF) sub-route is "
                                    "closed at the printed rows)"),
            "hard_input_b_pf_route": "NOT_INSTANTIABLE_AT_DEPLOYED_ROWS",
            "headline": ("PF-exact fails at all 8 charts at the most "
                         "favorable parameters; surpluses +280,001.27 to "
                         "+471,797.39 bits; flip Lambda* in {2,3,4} vs "
                         "Weil-forced 46,159/92,680; no admissible "
                         "(C0, Delta_pole, |P|) flips any chart "
                         "(surplus monotone in Lambda)."),
        },
        "honest_headline": (
            "The degree-uniform (PF) route to (MI) cannot be instantiated "
            "at any of the four printed deployed rows: exact zero-slack "
            "surpluses +280,001.27 to +471,797.39 bits at the most "
            "favorable Weil parameters, flip thresholds Lambda* in {2,3,4} "
            "vs the Weil-forced 46,159 (kb) / 92,680 (m31 circle).  Finite "
            "effective complement of prop:pf-deep-prefix-barrier (different "
            "regime: deployed Lambda is ~2-4% of N, not >= cN) and an exact "
            "calibration of the pointwise bound thm:prefix-flatness-power-"
            "sum (PF') would need at deployed scale.  The draft is "
            "consistent: it asserts no deployed-row (PF) instance, and the "
            "surplus is o(n) along fixed-field families."),
        "falsifiability": ("The gate fails if any of the 8 frozen floor "
                           "integers, the exact surpluses (2dp), the flip "
                           "thresholds, or the pinned label lines change."),
        "generator_route": ("Legendre prime-factorization exponents + "
                            "product-tree exact binomials; exact integer "
                            "comparisons; flip threshold by exact ratio "
                            "recursion; surpluses via top-900-bit mantissa"),
        "checker_route": ("independent: Kummer carry-count exponents + "
                          "smallest-first heap merge; math.comb for the "
                          "cycle-index binomials; lgamma cross-estimates "
                          "with 0.5-bit tolerance; fresh pin re-scan"),
        "nonclaims": [
            "does not decide the asymptotic (PF): along a fixed-field "
            "family the surplus is Theta(sqrt(p) log n) = o(n), so the "
            "asymptotic hypothesis is consistent with these rows",
            "does not evaluate the effective-span variant (log A_N in "
            "place of R log|B|): ambient failure does not imply effective "
            "failure, and A_N is not evaluable while hard input (a) "
            "(witness-exhaustive atlas) is open",
            "does not evaluate (MA), and does not attack the "
            "phase-dependent repaired certificate (PF') of "
            "thm:prefix-flatness-power-sum -- the flip thresholds "
            "calibrate what (PF') needs, they do not refute it",
            "no claim about the four printed rows' safety or unsafety "
            "beyond the (PF)-route closure; the floor/margin "
            "reproductions are oracle checks, not new results",
        ],
        "claim_boundaries": {
            "beats_or_narrows_trivial_baseline": True,
            "independent_recheck_confirms": True,
            "is_counterexample": False,
            "is_full_canonical_statement_not_proxy_or_toy_row": True,
            "is_not_degenerate_or_tautological_by_construction": True,
            "is_novel_not_confirming_a_proven_theorem": True,
            "resolves_or_advances_prob_band": False,
        },
        "evidence_type": "ORACLE_GATED_VS_COMMITTED_VALUE",
        "proof_status": "AUDIT (exact arithmetic, dual-route)",
        "regeneration": ("python experimental/scripts/"
                         "verify_pf_deployed_rows.py --emit-defaults"),
        "failed_checks": [name for name, ok in checks if not ok],
    }
    cert["payload_sha256"] = payload_hash(cert)
    return cert


def write_cert(root: Path, cert: dict[str, Any]) -> Path:
    path = root / CERT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    return path


def run_check(root: Path) -> int:
    fresh = build_certificate(root)
    stored = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    if stored.get("payload_sha256") != payload_hash(stored):
        print("RESULT: FAIL self-hash")
        return 1
    if fresh["payload_sha256"] != stored["payload_sha256"]:
        print("RESULT: FAIL rebuild drift")
        return 1
    if not stored["all_pass"] or stored["summary"]["verdict"] != "NO ISSUE":
        print("RESULT: FAIL", stored["summary"]["verdict"],
              stored.get("failed_checks"))
        return 1
    print("RESULT: PASS (%d checks)" % stored["checks_total"])
    print("payload_sha256:", stored["payload_sha256"])
    print("verdict:", stored["summary"]["verdict"])
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--emit-defaults", action="store_true")
    p.add_argument("--check", action="store_true")
    args = p.parse_args(argv)
    root = repo_root()
    if args.emit_defaults:
        cert = build_certificate(root)
        path = write_cert(root, cert)
        print("wrote", path)
        print("payload_sha256:", cert["payload_sha256"])
        print("checks: %d, failed: %d" % (cert["checks_total"],
                                          cert["checks_failed"]))
        for row_id, row in cert["rows"].items():
            for tag, c in row["charts"].items():
                print("  %-9s %s a=%d  surplus %s bits  Lambda*=%d"
                      % (row_id, tag, c["a"], c["pf_surplus_bits"],
                         c["lambda_flip_threshold"]))
        return 0
    if args.check:
        return run_check(root)
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
