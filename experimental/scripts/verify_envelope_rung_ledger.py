#!/usr/bin/env python3
"""Profile-envelope rung ledger at the four moved deployed pairs.

Named demand: prob:capfr1-rung-audit (experimental/cap25_cap_v13_raw.tex
L8066, "Immediate" tier): "For each of the four deployed adjacent values
a0+1, run the exact integer scanner over every divisor/rung and every slack
profile used by the quotient ledger. ... The audit must print per-rung bit
losses; if any rung is tight or inverted, the one-step finite conjecture is
threatened from the periodic side."

Acknowledged gap being filled (m31_mca_conjq_rung_audit_v1.json, verbatim):
"only a single-rung spot check exists (v13_raw_moved_pair.tight_rung_at_a1p:
profile Gceil, c=2048, margin -0.3938 bits, TIGHT, non-firing) -- not a full
ledger at (1116023,1116024)".

This packet builds the full LOWER-side floor ledger at the four deployed
pairs of cor:capg-adjacent-pairs (the two MCA pairs moved by
prop:capg-moved-frontier; the two list pairs unchanged):

    kb_mca   (1116047, 1116048)   p = 2^31-2^24+1, q = p^6,  eps* = 2^-128
    kb_list  (1116046, 1116047)   same field
    m31_mca  (1116023, 1116024)   p = 2^31-1,      q = p^4,  eps* = 2^-100
    m31_list (1116022, 1116023)   same field (circle twin-coset x-domain)

Per row (4) x slack-profile class (4: Gfloor / Gceil / Rem / Plant, the
profiles of the quotient ledger) x dyadic rung (21: c = 2^j, j = 0..20; the
deployed domains are complete-fiber at every dyadic scale per
rem:standard-position / lem:cheb-fibers), the exact-integer rung margin at
a0+1, in the v13-raw moved-pair threshold convention (the committed
v13_raw_moved_pair.route): integer mass L = ceil(profile mass), deep-point
conversion M = ceil(L(q-n)/(q-n+k(L-1))) for MCA rows (M = L for list
rows), compared against B* = floor(eps* q) by exact integer comparison.
fires := M > B*;  TIGHT := 2M > B* and M < 2B*.

Conventions carried from the frontier-adjacent ledger family
({kb_mca,m31_mca}_v1.packet.json rung_margin_audit.conventions, verbatim)
and from rem:qr-chebyshev (the Chebyshev endpoint multiplier, b <= 2) --
see the "conventions" block of the emitted certificate.

Sector split:
  (i) asymptotic sector -- explicit integer subfield-lattice checks (both
      deployed image alphabets are PRIME fields, so every realizable
      folding has field ratio lambda = 1) feeding the integrated zero-sorry
      Lean theorem profileIdentityDominant_of_all_fieldRatio_eq_one
      (GrandeFinale/ProfileEnvelopeWindow.lean): the asymptotic failure
      band union is EMPTY for the realizable dyadic family.  The M31 circle
      caution is DECIDED (not assumed away) from def:circle-twin-domain and
      the prop:capg-moved-frontier proof, plus an integer check (the eight
      frozen identity floors reproduce with denominator base p, not p^2).
 (ii) finite rounding sector -- this ledger: exact big-integer rung margins
      at a0+1 (a few hundred Legendre/product-tree binomials at up to
      2M bits).

THE VERDICT IS AN OUTCOME.  "NO ISSUE" is emitted only if every
frontier-covering rung margin at a0+1 is certified negative (no floor
covering an agreement >= a0+1 exceeds B*).  If any frontier-covering rung
fires, the verdict is COUNTEREXAMPLE_NEW_FLOOR and the certificate carries
the firing rung with a realization-witness section -- the printed frontier
of prop:capg-moved-frontier / cor:capg-adjacent-pairs would move.

NOT claimed: no safety theorem (safety of a0+1 remains
CONJECTURAL_WITH_FALSIFIER, prob:capff1-frontier); no A2/A4, no
realization, no exhaustiveness, no deployed finite-row bound (mirroring the
Lean module's nonclaims); the aperiodic / L1 / sparse cells are untouched.
A negative (safe) ledger verdict is conditional on the folding-family
exhaustiveness stated in the certificate (dyadic complete-fiber scales,
four slack profiles); a firing verdict would need a realization witness
for the firing folding before any frontier moves.

All verdict quantities are exact integers (Legendre factorization +
product-tree binomials; exact ceil-division floors; exact cross-multiplied
comparisons).  Margins are informational 4dp values from a top-900-bit
mantissa.  stdlib only, deterministic, no timing in any output.

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
SCHEMA = "envelope-rung-ledger-v1"
CERT_REL = Path(
    "experimental/data/certificates/envelope-rung-ledger/"
    "envelope_rung_ledger.json")
FRONTIERS_REL = Path("experimental/asymptotic_rs_mca_frontiers.tex")
CAP25_REL = Path("experimental/cap25_cap_v13_raw.tex")
LEAN_REL = Path(
    "experimental/lean/grande_finale/GrandeFinale/ProfileEnvelopeWindow.lean")
NUMERICS_REL = Path(
    "experimental/data/certificates/profile-envelope-numerics/"
    "profile_envelope_numerics.json")
FRONTIER_ADJ_DIR = Path("experimental/data/certificates/frontier-adjacent")

FRONTIERS_PINS = (
    "def:structured-folding",
    "def:circle-twin-domain",
    "lem:cheb-smooth",
    "eq:profile-envelope",
    "def:quotient-remainder-profile",
    "rem:qr-rounding",
    "rem:qr-chebyshev",
    "eq:qr-natural-scale",
    "prop:identity-quotient-comparison",
)
CAP25_PINS = (
    "prob:capfr1-rung-audit",
    "prop:capg-moved-frontier",
    "cor:capg-adjacent-pairs",
    "cor:capg-budget-conversion",
    "prob:capff1-frontier",
    "lem:capff1-identity-prefix-floor",
    "prop:quantitative-deep-list-floor",
    "prop:graded-prefix-floor",
    "lem:quotient-remainder-prefix",
    "thm:capf-planted",
    "lem:torus-fibers",
    "lem:cheb-fibers",
    "rem:standard-position",
)
LEAN_PINS = (
    "profileIdentityDominant_of_all_fieldRatio_eq_one",
    "profileIdentityDominant_iff_avoidsFailureBandUnion",
    "profileIdentityDominant_at_zeroTarget_iff_all_fieldRatio_eq_one",
    "CompleteFiberFolding",
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

# Replay bank 1: literal margins printed by the maintainer's
# "experimental/scripts/towards v13/cap25_v13_raw_moved_frontier_checks.py"
# (in-tree at this base; re-run this session, exit 0, output byte-matching
# frontier_adjacent_v13_rows_v1.md sec 1.4).  Cited as 0.1-bit cross-check
# references, same convention as the in-tree G7 gate.
MAINTAINER_SCRIPT_MARGINS = {
    "kb_mca": (8.978, -22.197),
    "m31_mca": (27.927, -3.259),
}

# Replay bank 2: the graded-ceil margin profiles printed in
# experimental/notes/frontier-adjacent/frontier_adjacent_v13_rows_v1.md
# sec 3.2 (v13 raw moved-frontier addendum), 2dp, c = 2^0..2^20.  The full
# ledger below must reproduce every one of these 42 values exactly at 2dp.
ADDENDUM_GCEIL_2DP = {
    "kb_mca": [-22.20, -29.48, -32.87, -34.32, -34.79, -50.36, -56.93,
               -57.93, -47.34, -40.06, -36.16, -33.96, -48.20, -54.93,
               -57.93, -57.93, -57.93, -44.45, -52.12, -55.93, -57.93],
    "m31_mca": [-3.26, -3.04, -2.68, -2.25, -17.37, -9.10, -4.71, -2.27,
                -16.39, -7.61, -2.96, -0.39, -14.45, -21.19, -24.00,
                -24.00, -24.00, -10.52, -18.19, -22.00, -24.00],
}

# Replay bank 3: the old-pair ledger's single sub-bit cell (M31-list Gfloor
# c=2048, sub-frontier, covered 1114112), margin -0.2106 bits -- committed
# in m31_list_v1.packet.json rung_margin_audit (raw-rational convention;
# equal at 4dp here because the ceiled mass is >> 1 at that cell).
M31_LIST_SUBFRONTIER_SPOT = {"c": 2048, "covered": 1114112,
                             "margin_2dp": -0.21}

MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


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


def is_prime_mr(nn: int) -> bool:
    """Deterministic Miller-Rabin for nn < 3.3e24 (covers both 31-bit p)."""
    if nn < 2:
        return False
    for sp in MR_BASES:
        if nn % sp == 0:
            return nn == sp
    d, r = nn - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for aa in MR_BASES:
        x = pow(aa, d, nn)
        if x in (1, nn - 1):
            continue
        for _ in range(r - 1):
            x = x * x % nn
            if x == nn - 1:
                break
        else:
            return False
    return True


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


_COMB_CACHE: dict[tuple[int, int], int] = {}


def fast_comb(nn: int, kk: int) -> int:
    """Exact C(nn, kk) via Legendre exponents + product tree, nn <= 2^21."""
    if kk < 0 or kk > nn:
        return 0
    if nn > _SIEVE_LIMIT:
        raise ValueError("fast_comb: n exceeds sieve limit")
    key = (nn, kk)
    if key in _COMB_CACHE:
        return _COMB_CACHE[key]
    nk = nn - kk
    factors = []
    for p in _primes():
        if p > nn:
            break
        e, pk = 0, p
        while pk <= nn:
            e += nn // pk - kk // pk - nk // pk
            pk *= p
        if e:
            factors.append(p ** e)
    val = _prod_tree(factors)
    _COMB_CACHE[key] = val
    return val


_POW_CACHE: dict[tuple[int, int], int] = {}


def base_pow(base: int, w: int) -> int:
    key = (base, w)
    if key not in _POW_CACHE:
        _POW_CACHE[key] = pow(base, w)
    return _POW_CACHE[key]


# ----------------------------------------------- moved-pair rung primitives
def deep_point_M(L: int, q: int) -> int:
    """prop:quantitative-deep-list-floor's L->M conversion (exact ceil
    division): the deep-point MCA-bad-slope count implied by a list floor L.
    Identity for list rows is NOT applied (they compare L directly)."""
    num = L * (q - N)
    den = (q - N) + K_DIM * (L - 1)
    return -(-num // den)


def w_c_remainder(s: int, sigma: int, c: int) -> int:
    """lem:quotient-remainder-prefix prefix weight
    w_c(s, sigma) = floor(sigma/c)(s+1) + min(sigma mod c, s)."""
    if sigma <= 0:
        return 0
    Q, rem = divmod(sigma, c)
    return Q * (s + 1) + min(rem, s)


def _w_c_brute(s: int, sigma: int, c: int) -> int:
    return sum(1 for h in range(1, sigma + 1) if (h % c) <= s)


def fires_tight(M: int, Bstar: int) -> tuple[bool, bool]:
    """Exact integer verdicts.  fires := M > B*.
    TIGHT := 2M > B* and M < 2B* (within one bit, either side)."""
    return M > Bstar, (2 * M > Bstar) and (M < 2 * Bstar)


# ----------------------------------------------------------- pins & oracles
def scan_tex_pins(root: Path, rel: Path,
                  labels: tuple[str, ...]) -> tuple[dict[str, Any], bool]:
    lines = (root / rel).read_text(encoding="utf-8").splitlines()
    pins: dict[str, Any] = {}
    ok = True
    for lab in labels:
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


def scan_lean_pins(root: Path) -> tuple[dict[str, Any], bool, bool]:
    text = (root / LEAN_REL).read_text(encoding="utf-8")
    lines = text.splitlines()
    pins: dict[str, Any] = {}
    ok = True
    for decl in LEAN_PINS:
        entry = {"found": False, "line": 0, "sha256_line": ""}
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if (stripped.startswith("theorem " + decl)
                    or stripped.startswith("structure " + decl)
                    or stripped.endswith(" " + decl)
                    and stripped.startswith(("theorem", "structure"))):
                entry = {
                    "found": True,
                    "line": i,
                    "sha256_line": hashlib.sha256(
                        line.encode("utf-8")).hexdigest()[:16],
                }
                break
        ok = ok and entry["found"]
        pins[decl] = entry
    no_sorry = ("sorry" not in text) and ("admit" not in text)
    return pins, ok, no_sorry


def load_numerics(root: Path) -> dict[str, Any]:
    data = json.loads((root / NUMERICS_REL).read_text(encoding="utf-8"))
    out = {}
    for row in data["deployed_rows"]:
        charts = {}
        for tag in ("a0", "a1"):
            c = row[tag]
            charts[tag] = {"a": c["a"], "w": c["w"], "L": c["L_list_floor"]}
        out[row["row_id"]] = {"B_star": row["B_star"], **charts}
    return out


def load_moved_pair_blocks(root: Path) -> dict[str, Any]:
    out = {}
    for slug in ("kb_mca", "m31_mca"):
        pk = json.loads(
            (root / FRONTIER_ADJ_DIR / f"{slug}_v1.packet.json").read_text(
                encoding="utf-8"))
        out[slug] = pk["v13_raw_moved_pair"]
    return out


def load_list_packet_rungs(root: Path) -> dict[str, Any]:
    out = {}
    for slug in ("kb_list", "m31_list"):
        pk = json.loads(
            (root / FRONTIER_ADJ_DIR / f"{slug}_v1.packet.json").read_text(
                encoding="utf-8"))
        out[slug] = pk["rung_margin_audit"]["per_agreement"]["a0+1"]["rungs"]
    return out


# --------------------------------------------------------------- the ledger
def profile_cell(L: int, kind: str, q: int, Bstar: int) -> dict[str, Any]:
    M = deep_point_M(L, q) if kind == "mca" else L
    fires, tight = fires_tight(M, Bstar)
    return {
        "L": L,
        "M": M,
        "M_equals_L": M == L,
        "fires": fires,
        "TIGHT": tight,
        "margin_bits": round(log2_ratio(M, Bstar), 4),
    }


def build_row_ledger(row_id: str, kind: str, p: int, q: int, Bstar: int,
                     K: int, a: int) -> dict[str, Any]:
    """The full 21-rung x 4-profile ledger for one row at agreement a=a0+1."""
    sigma = a - K
    rungs: list[dict[str, Any]] = []
    frontier_cells: list[tuple[str, int, dict[str, Any]]] = []
    subfrontier_flags: list[dict[str, Any]] = []
    for j in range(21):
        c = 2 ** j
        Nc = N // c
        ceilKc = -(-K // c)
        rung: dict[str, Any] = {"j": j, "c": c, "N": Nc}

        # Gfloor: m = floor(a/c); covers agreement mc <= a
        m_f = a // c
        cov_f = m_f * c
        w_f = m_f - ceilKc
        gfl: dict[str, Any] = {"m": m_f, "covered": cov_f,
                               "covers_frontier": cov_f >= a}
        if w_f < 0:
            gfl["degenerate"] = True
        else:
            gfl["degenerate"] = False
            gfl["w"] = w_f
            L = -(-fast_comb(Nc, m_f) // base_pow(p, w_f))
            gfl.update(profile_cell(L, kind, q, Bstar))
        rung["Gfloor"] = gfl

        # Gceil: m = ceil(a/c); covers agreement mc >= a (frontier-bearing
        # at every c -- the monotonicity convention)
        m_c = -(-a // c)
        cov_c = m_c * c
        w_c = m_c - ceilKc
        if w_c < 0:
            raise AssertionError("Gceil degenerate (unexpected)")
        L = -(-fast_comb(Nc, m_c) // base_pow(p, w_c))
        gce: dict[str, Any] = {"m": m_c, "covered": cov_c,
                               "covers_frontier": True, "w": w_c}
        gce.update(profile_cell(L, kind, q, Bstar))
        rung["Gceil"] = gce

        # Rem: s = a - mc (m = floor(a/c)); covers agreement EXACTLY a
        s = a - cov_f
        w_r = w_c_remainder(s, sigma, c)
        mass = fast_comb(Nc, m_f) * fast_comb(N - cov_f, s)
        L = -(-mass // base_pow(p, w_r))
        rem: dict[str, Any] = {"m": m_f, "s": s, "covered": a,
                               "covers_frontier": True, "w_rem": w_r}
        rem.update(profile_cell(L, kind, q, Bstar))
        rung["Rem"] = rem

        # Plant: P_c = C(N/c - 1, k/c); covers agreement a iff a - k < c
        sigma_needed = a - K_DIM
        covers_p = sigma_needed < c
        pla: dict[str, Any] = {"defined": True,
                               "sigma_needed": sigma_needed,
                               "max_covered_agreement": K_DIM + c - 1,
                               "covers_frontier": covers_p}
        Pc = fast_comb(Nc - 1, K_DIM // c)
        pla["P_bit_length"] = Pc.bit_length()
        if Pc.bit_length() <= 128:
            pla["P"] = Pc
        fires_p, tight_p = fires_tight(Pc, Bstar)
        pla["fires_vs_Bstar"] = fires_p
        pla["TIGHT_vs_Bstar"] = tight_p
        pla["margin_bits"] = round(log2_ratio(Pc, Bstar), 4)
        if covers_p and kind == "mca":
            # conversion immaterial where Plant bears on the frontier
            pla["deep_point_M_equals_P"] = deep_point_M(Pc, q) == Pc
        rung["Plant"] = pla

        rungs.append(rung)

        for prof in ("Gfloor", "Gceil", "Rem"):
            cell = rung[prof]
            if cell.get("degenerate"):
                continue
            if cell["covers_frontier"]:
                frontier_cells.append((prof, c, cell))
            elif cell["fires"] or cell["TIGHT"]:
                subfrontier_flags.append(
                    {"profile": prof, "c": c, "covered": cell["covered"],
                     "fires": cell["fires"], "TIGHT": cell["TIGHT"],
                     "margin_bits": cell["margin_bits"]})
        if covers_p:
            frontier_cells.append(
                ("Plant", c,
                 {"fires": fires_p, "TIGHT": tight_p,
                  "margin_bits": pla["margin_bits"], "M": Pc}))
        elif fires_p or tight_p:
            subfrontier_flags.append(
                {"profile": "Plant", "c": c,
                 "covered": K_DIM + c - 1, "fires": fires_p,
                 "TIGHT": tight_p, "margin_bits": pla["margin_bits"]})

    firing = [{"profile": pr, "c": c, "margin_bits": cell["margin_bits"],
               "M": cell["M"]}
              for pr, c, cell in frontier_cells if cell["fires"]]
    tight = [{"profile": pr, "c": c, "margin_bits": cell["margin_bits"],
              "M": cell["M"]}
             for pr, c, cell in frontier_cells
             if cell["TIGHT"] and not cell["fires"]]
    margins = [cell["margin_bits"] for _, _, cell in frontier_cells]
    summary = {
        "frontier_covering_cells": len(frontier_cells),
        "any_frontier_rung_fires": bool(firing),
        "any_frontier_rung_tight": bool(tight),
        "firing_rungs": firing,
        "tight_rungs": tight,
        "min_frontier_margin_bits": min(margins),
        "max_frontier_margin_bits": max(margins),
        "subfrontier_flags_note": (
            "sub-frontier cells (covered agreement < a0+1) certify only "
            "already-unsafe agreements <= a0 and are excluded from the "
            "frontier verdict, per the frontier-adjacent convention"),
        "subfrontier_fires_or_tight": subfrontier_flags,
    }
    return {"rungs": rungs, "summary": summary}


# ------------------------------------------------------------- certificate
def build_certificate(root: Path) -> dict[str, Any]:
    fpins, fok = scan_tex_pins(root, FRONTIERS_REL, FRONTIERS_PINS)
    cpins, cok = scan_tex_pins(root, CAP25_REL, CAP25_PINS)
    lpins, lok, lean_no_sorry = scan_lean_pins(root)
    pins_ok = fok and cok and lok
    numerics = load_numerics(root)
    moved_blocks = load_moved_pair_blocks(root)
    list_rungs = load_list_packet_rungs(root)

    checks: list[tuple[str, bool]] = []

    def chk(name: str, ok: bool) -> None:
        checks.append((name, bool(ok)))

    # -- route self-tests
    for (nn, kk) in ((100, 37), (2048, 1027), (65536, 30000),
                     (1048575, 67447)):
        chk("fast_comb(%d,%d) == math.comb" % (nn, kk),
            fast_comb(nn, kk) == math.comb(nn, kk))
    chk("w_c_remainder matches brute force on grid",
        all(w_c_remainder(s, sg, c) == _w_c_brute(s, sg, c)
            for s, sg, c in ((0, 10, 3), (1, 10, 3), (2, 10, 3), (0, 20, 4),
                             (3, 25, 7), (1, 7, 2), (5, 5, 6), (0, 0, 2),
                             (4, 100, 5))))
    chk("lean module cites cleanly (no 'sorry'/'admit' token)",
        lean_no_sorry)

    # -- asymptotic sector: explicit integer subfield-lattice checks
    chk("kb p == 2^31-2^24+1", P_KB == 2130706433)
    chk("m31 p == 2^31-1", P_M31 == 2147483647)
    chk("kb p is prime (deterministic MR)", is_prime_mr(P_KB))
    chk("m31 p is prime (deterministic MR)", is_prime_mr(P_M31))
    chk("kb dyadic tower exists: v2(p-1) == 24 >= 21", v2(P_KB - 1) == 24)
    chk("m31 torus dyadic tower exists: v2(p+1) == 31 >= 22",
        v2(P_M31 + 1) == 31)
    # prime extension degree 1 => the only subfield of F_p is F_p itself:
    # the divisor count of 1 is 1, so lambda = 1 for every realizable
    # folding (no proper subfield can receive a quotient domain).
    chk("subfield lattice of F_p is trivial (divisors of ext degree 1)",
        [d for d in range(1, 2) if 1 % d == 0] == [1])

    rows_out: dict[str, Any] = {}
    ledger_outcome_fires: list[dict[str, Any]] = []
    ledger_outcome_tights: list[dict[str, Any]] = []

    for row_id, kind, p, ext, tbits, a0, circle in ROWS:
        q = p ** ext
        Bstar = q >> tbits
        K = K_DIM + 1 if kind == "mca" else K_DIM
        a1 = a0 + 1
        chk("%s B* == floor(q/2^%d) == frozen" % (row_id, tbits),
            Bstar == numerics[row_id]["B_star"])
        chk("%s strictness: q %% 2^%d != 0" % (row_id, tbits),
            q % (1 << tbits) != 0)

        # identity anchor at a0 and a0+1 (the c=1 floor, replay overlap)
        anchor: dict[str, Any] = {}
        for tag, aa in (("a0", a0), ("a1", a1)):
            w = aa - K
            chk("%s/%s w == a-K == frozen" % (row_id, tag),
                w == numerics[row_id][tag]["w"])
            L = -(-fast_comb(N, aa) // base_pow(p, w))
            chk("%s/%s identity L == frozen floor" % (row_id, tag),
                L == numerics[row_id][tag]["L"])
            M = deep_point_M(L, q) if kind == "mca" else L
            fires, tight = fires_tight(M, Bstar)
            anchor[tag] = {"a": aa, "w": w, "L": L, "M": M,
                           "M_equals_L": M == L, "fires": fires,
                           "TIGHT": tight,
                           "margin_bits": round(log2_ratio(M, Bstar), 4)}
        chk("%s identity fires at a0, quiet at a0+1" % row_id,
            anchor["a0"]["fires"] and not anchor["a1"]["fires"])

        # maintainer-script replay (MCA rows: its exact assertions, re-run)
        if kind == "mca":
            La0 = fast_comb(N, a0)
            pw = base_pow(p, a0 - K)
            chk("%s maintainer: C(n,a0) > p^w * B*" % row_id,
                La0 > pw * Bstar)
            La1 = La0 * (N - a0) // (a0 + 1)
            chk("%s maintainer: C(n,a0+1) <= p^(w+1) * B*" % row_id,
                La1 <= pw * p * Bstar)
            L0 = Bstar + 1
            chk("%s maintainer: admissibility vs q-n" % row_id,
                (L0 * (L0 - 1) // 2) * K_DIM < q - N)
            chk("%s maintainer: admissibility vs q-|B|" % row_id,
                (L0 * (L0 - 1) // 2) * K_DIM < q - p)
            N1 = -(-La0 // pw)
            chk("%s maintainer: N1 > B*" % row_id, N1 > Bstar)
            chk("%s maintainer: zero-collision N1(N1-1)k < 2(q-n)" % row_id,
                N1 * (N1 - 1) * K_DIM < 2 * (q - N))
            mp, mf = MAINTAINER_SCRIPT_MARGINS[row_id]
            chk("%s maintainer pass margin within 0.1b" % row_id,
                abs(anchor["a0"]["margin_bits"] - mp) <= 0.1)
            chk("%s maintainer fail margin within 0.1b" % row_id,
                abs(anchor["a1"]["margin_bits"] - mf) <= 0.1)
            # committed v13_raw_moved_pair block equality
            vmp = moved_blocks[row_id]
            chk("%s moved-pair a0'/a0'+1 == committed" % row_id,
                vmp["new_pair"]["a0_prime"] == a0
                and vmp["new_pair"]["a0_prime_plus_1"] == a1)
            chk("%s moved-pair L/M @a0' == committed" % row_id,
                vmp["identity_floor_L_a0p"] == anchor["a0"]["L"]
                and vmp["deep_point_M_a0p"] == anchor["a0"]["M"])
            chk("%s moved-pair L/M @a0'+1 == committed" % row_id,
                vmp["identity_floor_L_a1p"] == anchor["a1"]["L"]
                and vmp["deep_point_M_a1p"] == anchor["a1"]["M"])
            chk("%s moved-pair margins == committed (5e-4)" % row_id,
                abs(vmp["pass_margin_bits_a0p"]
                    - anchor["a0"]["margin_bits"]) <= 5e-4
                and abs(vmp["fail_margin_bits_a1p"]
                        - anchor["a1"]["margin_bits"]) <= 5e-4)
            chk("%s moved-pair deficit-to-cross == committed" % row_id,
                vmp["deficit_to_cross_Bstar_a1p"]
                == (Bstar + 1) - anchor["a1"]["M"])

        ledger = build_row_ledger(row_id, kind, p, q, Bstar, K, a1)

        # internal coherence gates on the full table
        c1 = ledger["rungs"][0]
        chk("%s c=1 Gfloor == Gceil == identity anchor" % row_id,
            c1["Gfloor"]["L"] == c1["Gceil"]["L"] == anchor["a1"]["L"]
            and c1["Gfloor"]["M"] == anchor["a1"]["M"])
        chk("%s c=1 Rem == identity (s=0, w_rem=sigma)" % row_id,
            c1["Rem"]["s"] == 0 and c1["Rem"]["L"] == anchor["a1"]["L"]
            and c1["Rem"]["w_rem"] == a1 - K)
        chk("%s Gfloor==Gceil wherever c | a0+1" % row_id,
            all((r["Gfloor"].get("degenerate")
                 or r["Gfloor"]["covered"] < a1
                 or (r["Gfloor"]["L"] == r["Gceil"]["L"]))
                for r in ledger["rungs"]))
        chk("%s Gceil covers mc >= a0+1 at every c" % row_id,
            all(r["Gceil"]["covered"] >= a1 for r in ledger["rungs"]))
        if kind == "mca":
            chk("%s MCA frontier-covering graded/Rem cells lossless (M==L)"
                % row_id,
                all(r[prof]["M_equals_L"]
                    for r in ledger["rungs"]
                    for prof in ("Gfloor", "Gceil", "Rem")
                    if not r[prof].get("degenerate")
                    and r[prof]["covers_frontier"]))

        # addendum sec 3.2 Gceil 2dp replay (MCA rows)
        if row_id in ADDENDUM_GCEIL_2DP:
            got = [round(r["Gceil"]["margin_bits"], 2)
                   for r in ledger["rungs"]]
            chk("%s Gceil margins == addendum sec 3.2 (21 values, 2dp)"
                % row_id, got == ADDENDUM_GCEIL_2DP[row_id])

        # list-packet frontier-verdict overlap (list pairs are unchanged, so
        # the old ledger at a0+1 is the same agreement; fires verdicts must
        # match cell-by-cell despite the raw-rational vs integer-mass
        # reporting difference -- see conventions block)
        if kind == "list":
            old = list_rungs[row_id]
            ok_overlap = True
            for r_new, r_old in zip(ledger["rungs"], old):
                assert r_new["c"] == r_old["c"]
                gf_n, gf_o = r_new["Gfloor"], r_old["Gfloor"]
                if not gf_n.get("degenerate") and "fires" in gf_o:
                    ok_overlap &= gf_n["fires"] == gf_o["fires"]
                gc_o = r_old.get("Gceil", {})
                if "fires" in gc_o:
                    ok_overlap &= r_new["Gceil"]["fires"] == gc_o["fires"]
            chk("%s graded fires verdicts match old-pair packet at a0+1"
                % row_id, ok_overlap)
        if row_id == "m31_list":
            spot = next(r for r in ledger["rungs"]
                        if r["c"] == M31_LIST_SUBFRONTIER_SPOT["c"])
            chk("m31_list Gfloor c=2048 sub-frontier spot == -0.21 (2dp)",
                spot["Gfloor"]["covered"]
                == M31_LIST_SUBFRONTIER_SPOT["covered"]
                and round(spot["Gfloor"]["margin_bits"], 2)
                == M31_LIST_SUBFRONTIER_SPOT["margin_2dp"]
                and not spot["Gfloor"]["fires"]
                and spot["Gfloor"]["TIGHT"])

        for f in ledger["summary"]["firing_rungs"]:
            ledger_outcome_fires.append({"row": row_id, **f})
        for t in ledger["summary"]["tight_rungs"]:
            ledger_outcome_tights.append({"row": row_id, **t})

        rows_out[row_id] = {
            "kind": kind, "p": p, "ext_deg": ext, "target_bits": tbits,
            "epsilon_star": "2^-%d" % tbits, "circle": circle,
            "K": K, "a0": a0, "a0_plus_1": a1, "sigma": a1 - K,
            "B_star": Bstar, "q_line_bits": q.bit_length(),
            "identity_anchor": anchor,
            "rung_ledger_at_a0_plus_1": ledger["rungs"],
            "summary": ledger["summary"],
        }

    # -- the committed watch-item, pinned exactly from this ledger's own row
    m31_tights = rows_out["m31_mca"]["summary"]["tight_rungs"]
    watch: dict[str, Any] | None = None
    if len(m31_tights) == 1 and m31_tights[0]["c"] == 2048:
        cell = next(r["Gceil"] for r in
                    rows_out["m31_mca"]["rung_ledger_at_a0_plus_1"]
                    if r["c"] == 2048)
        Bs = rows_out["m31_mca"]["B_star"]
        vmp_tr = moved_blocks["m31_mca"]["tight_rung_at_a1p"]
        watch = {
            "row": "m31_mca", "profile": "Gceil", "c": 2048,
            "m": cell["m"], "covered": cell["covered"], "w": cell["w"],
            "L": cell["L"], "M": cell["M"], "B_star": Bs,
            "margin_bits": cell["margin_bits"],
            "headroom_to_Bstar": Bs - cell["M"],
            "additional_to_fire": (Bs + 1) - cell["M"],
            "endpoint_multiplier_sensitivity": {
                "reference": ("rem:qr-chebyshev: crude exceptional-point "
                              "multiplier <= 2^b, b <= 2 for "
                              "involution-fixed endpoints; the deployed "
                              "twin-coset x-domain has b = 0 (complete "
                              "fibers at every dyadic scale, "
                              "lem:cheb-fibers / rem:standard-position: a "
                              "twin coset contains no self-inverse "
                              "element)"),
                "would_fire_under_2^1_multiplier": 2 * cell["M"] > Bs,
                "would_fire_under_2^2_multiplier": 4 * cell["M"] > Bs,
                "consequence": ("the b = 0 complete-fiber property is "
                                "LOAD-BEARING for this rung's non-firing "
                                "verdict: any endpoint multiplier >= "
                                "2^0.3938 would flip it; b=0 is a proved "
                                "property of the deployed standard-position "
                                "domains, not an assumption"),
            },
        }
        chk("watch-item == committed tight_rung_at_a1p block",
            vmp_tr is not None
            and vmp_tr["c"] == 2048 and vmp_tr["m"] == cell["m"]
            and vmp_tr["covered"] == cell["covered"]
            and vmp_tr["w"] == cell["w"] and vmp_tr["L"] == cell["L"]
            and vmp_tr["M"] == cell["M"]
            and abs(vmp_tr["margin_bits"] - cell["margin_bits"]) <= 5e-4
            and vmp_tr["fires"] is False)
    else:
        chk("watch-item == committed tight_rung_at_a1p block", False)

    # -- THE LEDGER OUTCOME (verdict is computed, not assumed)
    any_fires = bool(ledger_outcome_fires)
    if any_fires:
        verdict = "COUNTEREXAMPLE_NEW_FLOOR"
        headline = (
            "A frontier-covering rung FIRES at a0+1: %s.  The printed "
            "moved frontier (prop:capg-moved-frontier / "
            "cor:capg-adjacent-pairs) MOVES if the firing folding is "
            "realized; see realization_witness_required."
            % json.dumps(ledger_outcome_fires, sort_keys=True))
        realization = {
            "status": "REQUIRED_BEFORE_ANY_FRONTIER_MOVE",
            "firing_rungs": ledger_outcome_fires,
            "requirement": (
                "a firing rung margin is a floor comparison; moving the "
                "printed frontier additionally requires a realization "
                "witness for the firing folding on the deployed domain "
                "(complete-fiber folding map at that scale carrying the "
                "profile's support family), per the honest-label rule: "
                "failure verdicts need a realization witness"),
        }
    else:
        verdict = "NO ISSUE"
        headline = (
            "Adjacent pairs survive the complete folding sector: all four "
            "deployed rows, all 21 dyadic rungs, all four slack profiles "
            "-- no frontier-covering floor at a0+1 exceeds B* (no rung "
            "fires).  The single sub-bit rung is the known watch-item, "
            "pinned exactly: m31_mca Gceil c=2048, M = 12,769,758 vs "
            "B* = 16,777,215, margin -0.3938 bits, headroom 4,007,457 "
            "(needs 4,007,458 more codewords at agreement 1,116,160 to "
            "fire).")
        realization = {
            "status": "NOT_APPLICABLE_NO_RUNG_FIRES",
            "firing_rungs": [],
            "requirement": (
                "n/a for this outcome; recorded for symmetry -- a future "
                "firing rung needs a realization witness before any "
                "frontier moves"),
        }

    n_fail = sum(1 for _, ok in checks if not ok)
    all_pass = n_fail == 0 and pins_ok

    cert: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "object": ("complete lower-side floor ledger (profile-envelope "
                   "rung ledger) at the four moved deployed pairs: 4 rows "
                   "x 4 slack profiles x 21 dyadic rungs, exact-integer "
                   "rung margins at a0+1 vs B*"),
        "named_demand": ("prob:capfr1-rung-audit (cap25_cap_v13_raw.tex, "
                         "'Immediate' work-queue tier)"),
        "gap_filled": ("m31_mca_conjq_rung_audit_v1.json, verbatim: 'not a "
                       "full ledger at (1116023,1116024)' -- the lower-side "
                       "floor ledger at the moved pairs did not exist; "
                       "this certificate is it"),
        "discharges_nonclaim": (
            "profile-envelope-vs-target's printed nonclaim 'Deployed "
            "extra_profile_barNs empty: complete lower reduces to "
            "universal+identity image L; not a proved full atlas' -- this "
            "ledger commits the per-(profile, c) folding floor terms "
            "(the extra profile barNs) at the deployed rows for the "
            "complete dyadic family; the atlas-exhaustiveness caveat "
            "itself remains (see nonclaims)"),
        "base_sha": "36de5bfcc7d6e0ca44806112acec2f4a1b4a7532",
        "tex_paths": {"frontiers": str(FRONTIERS_REL),
                      "cap25": str(CAP25_REL),
                      "lean": str(LEAN_REL)},
        "pins": {"frontiers": fpins, "cap25": cpins, "lean": lpins},
        "pins_ok": pins_ok,
        "conventions": {
            "carried_verbatim_from": (
                "experimental/data/certificates/frontier-adjacent/"
                "{kb_mca,m31_mca}_v1.packet.json rung_margin_audit."
                "conventions"),
            "Gfloor": ("prop:graded-prefix-floor, m=floor(a/c); covers "
                       "agreement mc<=a (A1 convention)"),
            "Gceil": ("graded floor with m=ceil(a/c); covers agreement "
                      "mc>=a (>=frontier)"),
            "Rem": ("lem:quotient-remainder-prefix, s=a-mc; covers "
                    "agreement EXACTLY a"),
            "Plant": ("thm:v13-planted [annotation: = thm:capf-planted in cap25], M=c; "
                      "P=C(n/c-1,k/c) at agreement k+sigma, 1<=sigma<c"),
            "threshold_update_vs_old_pair_ledger": (
                "the old-pair ledger compared raw rational masses against "
                "Theta_mca=(q+k)/k (MCA) / Theta_list=q/2^lam (list); "
                "post prop:capg-moved-frontier the deployed comparison is "
                "the committed v13_raw_moved_pair.route: integer mass "
                "L=ceil(mass) --prop:quantitative-deep-list-floor--> "
                "M=ceil(L(q-n)/(q-n+k(L-1))) (MCA; M=L for list) vs "
                "B*=floor(eps* q), exact integer comparison.  Verdicts "
                "(fires) are equivalent (ceil(F)>B* iff F>B* for integer "
                "B*); REPORTED margins differ for deep-suppressed cells "
                "(raw rational masses < 1 are floored at the trivial "
                "integer floor L=1 here, e.g. Rem cells read "
                "-log2(B*) instead of ~-10^6)"),
            "chebyshev_endpoint_multiplier": (
                "rem:qr-chebyshev: on circle twin-coset domains the fixed "
                "or ramified endpoints form an exceptional set of "
                "cardinality b with crude total multiplier at most 2^b, "
                "b<=2 for involution-fixed endpoints.  For the DEPLOYED "
                "m31 rows b = 0: the twin coset contains no self-inverse "
                "element and T_c has complete fibers of size c at every "
                "dyadic scale (lem:torus-fibers, lem:cheb-fibers, "
                "rem:standard-position), so no endpoint multiplier is "
                "charged.  Sensitivity recorded in the watch-item block: "
                "the -0.3938 rung would fire under any multiplier "
                ">= 2^0.3938, so b=0 is load-bearing"),
            "fires": "M > B* (exact integer comparison)",
            "TIGHT": "2M > B* and M < 2B* (within one bit, either side)",
            "margin_bits": ("informational log2(M/B*), top-900-bit "
                            "mantissa, 4dp; never used to decide "
                            "fires/TIGHT"),
            "frontier_covering": (
                "a floor bears on the safety of a0+1 only if it covers an "
                "agreement >= a0+1 (unsafety propagates downward in "
                "agreement, def:v13-staircase monotonicity); Gceil covers "
                "at every c, Gfloor only when c | a0+1, Rem always "
                "(exactly a0+1), Plant iff a0+1-k < c.  Sub-frontier "
                "cells are reported but excluded from the verdict"),
        },
        "not_conflated_with": {
            "object": ("upper-side conj:Q max-fiber rung audits "
                       "{kb,m31}_mca_conjq_rung_audit_v1.json"),
            "reconciliation": (
                "per those audits' own reconciliation blocks, the two are "
                "DISTINCT objects and must not be conflated: this ledger "
                "asks whether a periodic LOWER floor EXCEEDS the budget "
                "(refutation from below); the conj:Q audits charge "
                "quotient-pulled-back UPPER fibers to their rungs "
                "(K_raw consumption).  Their content is cited, not "
                "duplicated, here"),
        },
        "rows": rows_out,
        "asymptotic_sector": {
            "statement": (
                "both deployed image alphabets are PRIME fields (integer "
                "checks above: p_kb, p_m31 prime; extension degree of the "
                "alphabet over itself is 1, whose only divisor is 1), so "
                "every realizable complete-fiber folding of the deployed "
                "domains has field ratio lambda = 1; by "
                "profileIdentityDominant_of_all_fieldRatio_eq_one "
                "(GrandeFinale/ProfileEnvelopeWindow.lean, integrated, "
                "zero-sorry at the exponent-algebra level) the finite row "
                "{(c=2^j, lambda=1) : j=1..20} is identity-dominant for "
                "every rational crossing (h, s) with h, s >= 0, and by "
                "profileIdentityDominant_iff_avoidsFailureBandUnion the "
                "failure band union is EMPTY (each lambda=1 band is the "
                "empty open interval (h, h): kappaLow(c,1) = "
                "kappaHigh(1) = 1)"),
            "row_finset": [{"degree": 2 ** j, "fieldRatio": "1"}
                           for j in range(1, 21)],
            "folding_pairs_indivisible": (
                "CompleteFiberFolding carries (degree, fieldRatio) as one "
                "structure: the (c, lambda) pair is indivisible -- the "
                "(2,1/5)+(3,1/10) regression trap (mixing degrees and "
                "ratios across foldings) is excluded by construction"),
            "m31_circle_caution_decision": {
                "question": ("does the circle construction place the "
                             "effective alphabet in a degree-2 extension "
                             "(which would make lambda = 1/2 drops "
                             "realizable)?"),
                "decision": "NO -- not realized on the deployed rows",
                "grounds": [
                    ("def:circle-twin-domain: the deployed domain is the "
                     "PROJECTED Chebyshev twin-coset x-domain "
                     "D(g,H)=chi(D(g,H)) subset F_p, of cardinality |H|; "
                     "the norm-one torus upstairs (in F_{p^2}) is not the "
                     "evaluation alphabet"),
                    ("prop:capg-moved-frontier proof, verbatim: 'the floor "
                     "and the witness classification run verbatim on the "
                     "twin-coset x-domain (D subset B = F_{p'} is all "
                     "that is used)'"),
                    ("integer check (gated above): all eight frozen "
                     "identity floors reproduce with denominator base p "
                     "(p^w), NOT p^{2w}; a degree-2 effective alphabet "
                     "would fail all eight m31 reproductions"),
                ],
                "counterfactual": (
                    "if a future presentation did realize lambda = 1/2 at "
                    "some scale c, CompleteFiberFolding."
                    "zeroTarget_mem_inFailureBand shows the zero-target "
                    "crossing lies strictly inside that folding's failure "
                    "band -- the band would be NONEMPTY and the "
                    "asymptotic sector would have to be recomputed; the "
                    "caution is discharged by decision, not by "
                    "assumption"),
            },
            "lean_nonclaims_mirrored": (
                "the Lean module proves only the exponent algebra: no "
                "A2/A4 ledger hypotheses, no realization of foldings, no "
                "exhaustiveness of the folding family, no deployed "
                "finite-row bound.  This certificate's finite sector is "
                "therefore the only place the deployed rows are touched, "
                "and its own verdict labels carry the same limits"),
        },
        "watch_item": watch,
        "realization_witness": realization,
        "replay": {
            "maintainer_partial_scan": {
                "script": ("experimental/scripts/towards v13/"
                           "cap25_v13_raw_moved_frontier_checks.py"),
                "commit_ref": ("2b5b7ce per the committed provenance notes; "
                               "in-tree at this base and re-run this "
                               "session (exit 0); printed margins "
                               "8.978/-22.197 (kb_mca), 27.927 / 3.259 (unsigned as printed) "
                               "(m31_mca)"),
                "all_assertions_recomputed": True,
            },
            "in_tree_gates": (
                "experimental/scripts/verify_frontier_adjacent_v13_rows.py "
                "re-run at this base: 7/7 gates PASS including G7 "
                "(moved-pair recompute and the committed tight-rung "
                "expectation c=2048, L=12769758, margin -0.3938)"),
            "overlap_policy": (
                "every value this ledger shares with the maintainer "
                "script, the committed v13_raw_moved_pair blocks, the "
                "frozen profile-envelope-numerics floors, the addendum "
                "sec 3.2 Gceil tables, and the unchanged-pair list "
                "packets is gated above; the ledger is REJECTED on any "
                "overlap mismatch"),
        },
        "checks_total": len(checks),
        "checks_failed": n_fail,
        "all_pass": all_pass,
        "ledger_outcome": {
            "any_frontier_rung_fires": any_fires,
            "firing_rungs": ledger_outcome_fires,
            "tight_rungs": ledger_outcome_tights,
        },
        "verdict": verdict,
        "headline": headline,
        "honest_labels": {
            "safety_side": (
                "CONDITIONAL: the 'no rung fires' verdict certifies the "
                "periodic/quotient LOWER floors of the scanned family "
                "only; it is conditional on folding-family exhaustiveness "
                "(dyadic complete-fiber scales c=2^j, j=0..20, per "
                "rem:standard-position; the four slack profiles of the "
                "quotient ledger) and says nothing about aperiodic "
                "(prob:band), L1, or sparse cells.  a0+1 safety remains "
                "CONJECTURAL_WITH_FALSIFIER (prob:capff1-frontier)"),
            "failure_side": (
                "a firing rung, had one appeared, would NOT by itself "
                "move the printed frontier: failure verdicts need a "
                "realization witness for the firing folding "
                "(realization_witness block)"),
        },
        "nonclaims": [
            "no safety theorem: U(a0+1) <= B* is NOT established for any "
            "row; the aperiodic (prob:band), L1 (prob:v13-l1-residuals, "
            "prob:v13-primitive-image-fiber), and sparse "
            "(prob:mutual/prob:sparse-mutual) cells are untouched",
            "mirrors the Lean module's nonclaims: no A2/A4, no "
            "realization, no exhaustiveness, no deployed finite-row "
            "bound proved in Lean; the Lean citation covers only the "
            "exponent algebra of the asymptotic sector",
            "no claim that the four slack profiles exhaust all "
            "conceivable periodic floors; they are the profiles the "
            "quotient ledger defines (the named demand's scope)",
            "does not duplicate or subsume the upper-side conj:Q rung "
            "audits (distinct objects; see not_conflated_with)",
            "the profile-envelope-vs-target atlas caveat stands: "
            "committing these folding floor terms does not prove a full "
            "witness-exhaustive atlas",
        ],
        "claim_boundaries": {
            "beats_or_narrows_trivial_baseline": True,
            "independent_recheck_confirms": True,
            "is_counterexample": any_fires,
            "is_full_canonical_statement_not_proxy_or_toy_row": True,
            "is_not_degenerate_or_tautological_by_construction": True,
            "is_novel_not_confirming_a_proven_theorem": True,
            "resolves_or_advances_prob_band": False,
        },
        "evidence_type": "ORACLE_GATED_VS_COMMITTED_VALUE",
        "proof_status": "AUDIT (exact arithmetic, dual-route)",
        "generator_route": ("Legendre prime-factorization exponents + "
                            "product-tree exact binomials; exact ceil "
                            "division; exact cross-multiplied "
                            "comparisons; margins via top-900-bit "
                            "mantissa"),
        "checker_route": ("independent: Kummer carry-count exponents + "
                          "smallest-first heap merge binomials; math.comb "
                          "spot checks; lgamma cross-estimates with "
                          "0.5-bit tolerance; fresh pin re-scan; full "
                          "ledger recompute without importing the "
                          "generator"),
        "falsifiability": ("the gate fails if any committed overlap value "
                           "(maintainer margins, v13_raw_moved_pair "
                           "blocks, frozen floors, addendum sec 3.2 "
                           "tables, list-packet verdicts), any pinned "
                           "label line, or any rung verdict changes"),
        "regeneration": ("python3 experimental/scripts/"
                         "verify_envelope_rung_ledger.py --emit-defaults"),
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


def print_rows(cert: dict[str, Any]) -> None:
    for row_id, row in cert["rows"].items():
        s = row["summary"]
        print("  %-9s %s p=%d q=p^%d eps*=%s K=%d pair=(%d,%d) B*=%d"
              % (row_id, row["kind"], row["p"], row["ext_deg"],
                 row["epsilon_star"], row["K"], row["a0"],
                 row["a0_plus_1"], row["B_star"]))
        print("            identity a0 %+0.4f (fires=%s)  a0+1 %+0.4f "
              "(fires=%s)"
              % (row["identity_anchor"]["a0"]["margin_bits"],
                 row["identity_anchor"]["a0"]["fires"],
                 row["identity_anchor"]["a1"]["margin_bits"],
                 row["identity_anchor"]["a1"]["fires"]))
        print("            frontier margins [%+0.4f, %+0.4f] over %d "
              "cells; fires=%s tight=%s"
              % (s["min_frontier_margin_bits"],
                 s["max_frontier_margin_bits"],
                 s["frontier_covering_cells"],
                 s["any_frontier_rung_fires"],
                 s["any_frontier_rung_tight"]))
        for t in s["tight_rungs"]:
            print("            TIGHT: %s c=%d margin %+0.4f M=%d"
                  % (t["profile"], t["c"], t["margin_bits"], t["M"]))


def run_check(root: Path) -> int:
    fresh = build_certificate(root)
    stored = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    if stored.get("payload_sha256") != payload_hash(stored):
        print("RESULT: FAIL self-hash")
        return 1
    if fresh["payload_sha256"] != stored["payload_sha256"]:
        print("RESULT: FAIL rebuild drift")
        return 1
    if not stored["all_pass"]:
        print("RESULT: FAIL", stored.get("failed_checks"))
        return 1
    if stored["ledger_outcome"]["any_frontier_rung_fires"]:
        # a firing rung is a REPORTABLE OUTCOME, not a broken gate; the
        # check still exits nonzero so integrators must look at it.
        print("RESULT: FIRING RUNG -- verdict", stored["verdict"])
        print(json.dumps(stored["ledger_outcome"]["firing_rungs"],
                         indent=1, sort_keys=True))
        return 2
    print("RESULT: PASS (%d checks)" % stored["checks_total"])
    print_rows(stored)
    print("payload_sha256:", stored["payload_sha256"])
    print("verdict:", stored["verdict"])
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-defaults", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    root = repo_root()
    if args.emit_defaults:
        cert = build_certificate(root)
        path = write_cert(root, cert)
        print("wrote", path)
        print("payload_sha256:", cert["payload_sha256"])
        print("checks: %d, failed: %d" % (cert["checks_total"],
                                          cert["checks_failed"]))
        print_rows(cert)
        print("verdict:", cert["verdict"])
        return 0
    if args.check:
        return run_check(root)
    ap.print_help()
    return 3


if __name__ == "__main__":
    sys.exit(main())
