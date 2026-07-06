#!/usr/bin/env python3
"""verify_frontier_extension_cell_targets.py

Zero-arg, stdlib-only, deterministic verifier for
experimental/data/certificates/frontier-adjacent/extension_cell_targets_v1.json
and its companion note
experimental/notes/frontier-adjacent/frontier_extension_cell_targets_v1.md.

This packet does NOT certify U(a0+1) <= B_star and does NOT pay the
paid_extension cell. It is a TARGET specification for the open K=F
(full-orbit) branch of that cell, at the four deployed v14 rows (KoalaBear
MCA/list, Mersenne-31 MCA/list). This verifier's job is to independently
recompute every numeric field in the packet from n, k, and the two field
primes alone -- not to trust the packet's own arithmetic -- and to confirm
every cited tex/markdown label and source script actually exists.

Ten gate classes; exit 0 iff ALL pass, nonzero on ANY failure:

  G1  Field primes: exact value + prime_form identity (2^31-2^24+1 KoalaBear,
      2^31-1 Mersenne-31) + primality (trial division, both ~2^31 so cheap).
  G2  B* budgets: floor(p^6/2^128) (KB) and floor(p'^4/2^100) (M31), exact
      integer, plus their log2 (loose tolerance, informational only).
  G3  Subfield lattice: divisors of e (KB e=6 -> diamond {1,2,3,6}, M31 e=4
      -> chain {1,2,4}, confirmed structurally via gcd/lcm-vs-divisor-pair
      comparability, not just asserted) and the four/three confinement
      densities |K|/q = p^-(e-d) per subfield.
  G4  Full K=F stratum: deg-exactly-e element counts via the exact Mobius
      formula sum_{d|e} mu(e/d) p^d, the derived Frobenius-orbit count
      (count // e, with count % e == 0 as a hard consistency gate), and the
      proper-subfield ambient count sum_{d|e,d<e} p^d.
  G5  e_Y cost verdicts: p vs B* and p^2 vs B* (exact integer), matching the
      packet's "fits"/"EXCEEDS absolute budget" verdict strings.
  G6  The four v14 (a0, a0+1) pairs -- checked against a hardcoded canonical
      list independent of the JSON (KB MCA (1116047,1116048), KB list
      (1116046,1116047), M31 MCA (1116023,1116024), M31 list
      (1116022,1116023)) -- plus w_at_a0 = a0-k-1 (mca) / a0-k (list).
  G7  THE HEADLINE GATE. Exact-integer (no floating point) recompute of:
        (a) unsafe(a0):  comb(n,a0)   >  p^w   * B*
        (b) safe(a0+1):  comb(n,a0+1) <= p^(w+1) * B*
        (c) Delta_ext_ceiling_int = floor( p^(w+1)*B* / comb(n,a0+1) ),
            i.e. floor(2^fail_margin_bits) computed as an EXACT integer
            ratio of huge integers, not via math.log2/lgamma.
      Also cross-checks fail_margin_bits itself (a float, via the same
      log2-binomial/lgamma route used by compute_ext.py and
      "towards v13/cap25_v14_moved_frontier_checks.py") at loose tolerance,
      and confirms e_Y_forced=0 follows from log2(p) exceeding every row's
      fail_margin_bits.
      NOTE ON A CAUGHT BUG: the session draft (wave9_extension_numbers.json)
      computed Delta_ext_ceiling_int by printing 2**fail_margin via Python's
      ':,.0f' format, which ROUNDS to nearest. The design semantics need
      FLOOR (Delta_ext is a nonneg integer degree with Delta_ext <=
      2^fail_margin). For the two KoalaBear rows this rounding-vs-flooring
      difference flips the last digit: KB-MCA 4807521->4807520, KB-list
      4226237->4226236 (the two Mersenne-31 rows, 9 and 8, were already the
      correct floor and are unchanged). This verifier's gate G7 checks the
      SHIPPED (corrected) packet against the exact-integer floor, so it
      would have FAILED against the original draft's numbers -- see the
      packet's own "audit_corrections" block.
  G8  Reference existence: every tex label cited in the companion note's Refs
      section is grepped for in tex/cs25_cap_v12.tex or
      experimental/cap25_v13_experimental.tex (label name only, not the
      exact cited line -- several citations point at the \\begin{env} line
      one above the actual \\label{...} line, which is an existing citation
      convention in this repo, confirmed by inspection, not a defect); every
      cited experimental/notes/{f1,ef}/*.md file exists; the scanner
      function (extension_chart_upper) and its printed non-claim string
      exist in verify_paid_ledger_functions.py at the cited neighborhood;
      "towards v13/cap25_v14_moved_frontier_checks.py" exists.
  G9  Packet/note hygiene: meta.n/meta.k match n/k, the audit_corrections
      block is internally consistent (corrected_value + 1 ==
      source_draft_value for both entries), the shipped JSON's filename
      does not collide with any of PR #329's four packet filenames
      (kb_list_v1.packet.json, kb_mca_v1.packet.json, m31_list_v1.packet.json,
      m31_mca_v1.packet.json), and the companion note file exists on disk and
      contains its required non-claim / merge-hygiene language.
  G10 Scanner cross-execution (added for the shipped F1 toy scanner). Imports
      experimental/scripts/f1_extension_full_orbit_scan.py and RE-RUNS a fast
      subset of its menu inside this verifier -- trusting the scanner's code,
      not its emitted JSON: (a) the slack-t=1 divided-difference growth
      full_count == C(n_toy, k_toy+1) == supports_scanned at p0 in {2,3}
      (chain e=4); (b) the slack-t>=2 zero-count -- p0 in {2,3} at t=2 are
      INFEASIBLE (k+t>n, so vacuously no K=F bad slope), and the smallest
      feasible t=2 tower (p0=5 chain) has full_count == 0 and
      aggregate_full_count == 0. ~2-3s added (all fields <=625). This makes
      the note's Q4 slack-scope qualifier executable. (Numbered G10 because
      G8/G9 above were already taken by the reference/hygiene gates.)

Hidden self-test:  python3 verify_frontier_extension_cell_targets.py --tamper-selftest
    Each gate function takes a tamper=False parameter; in self-test mode it is
    called with tamper=True, which corrupts exactly ONE stored/expected value
    used inside that gate's first check (never the from-scratch recomputed
    side) and asserts the gate then reports a mismatch (CAUGHT). This proves
    every gate has teeth. The shipped default is zero-arg (tamper=False
    everywhere) and does not depend on which mode ran first: the expensive
    shared bignum computation (see PERFORMANCE) runs exactly once regardless
    of mode or how many gates use it.

PERFORMANCE. The four rows' a0 values cluster into two tight runs of three
consecutive integers (KB: 1116046,1116047,1116048; M31: 1116022,1116023,
1116024). math.comb(2**21, ~1.1e6) costs ~15s per call (measured) because the
result has ~2.1e6 bits; computing it 6 times (let alone the 8+ times a naive
per-row implementation would need) would blow the time budget. This script
calls math.comb() exactly ONCE per field (at the smallest needed m) and reaches
the other two values per field via the exact O(size) recurrence
C(n,m+1) = C(n,m)*(n-m)//(m+1). Total measured runtime is ~30s, independent of
--tamper-selftest. sys.set_int_max_str_digits is raised because comb(n, ~1.1e6)
has far more than the default 4300-digit str-conversion ceiling; this script
never actually stringifies those values (only their .bit_length() or booleans
are printed), but the raise is kept as a defensive match to this repo's
convention in other big-integer verifiers.

All arithmetic is exact (Python ints) except the informational log2/lgamma
cross-checks explicitly marked as such (loose tolerance, never gates a
PASS/FAIL verdict on its own -- G7's Delta_ext_ceiling_int check is the exact
integer one). No network, no writes, no non-stdlib imports.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from math import lgamma, log, log2

sys.set_int_max_str_digits(2_000_000)

# ---------------------------------------------------------------------------
# paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
JSON_PATH = os.path.join(REPO_ROOT, "experimental", "data", "certificates",
                         "frontier-adjacent", "extension_cell_targets_v1.json")
NOTE_PATH = os.path.join(REPO_ROOT, "experimental", "notes", "frontier-adjacent",
                         "frontier_extension_cell_targets_v1.md")

# ---------------------------------------------------------------------------
# constants (from-scratch ground truth; independent of the JSON)
# ---------------------------------------------------------------------------
n = 2 ** 21
k = 2 ** 20
p_KB = 2 ** 31 - 2 ** 24 + 1
p_M31 = 2 ** 31 - 1
FIELD = {
    "KB": dict(p=p_KB, e=6, t=128),
    "M31": dict(p=p_M31, e=4, t=100),
}

# canonical v14 pairs, hardcoded independently of the JSON (task ground truth)
CANON_PAIRS = {
    "KB-MCA": (1116047, 1116048, "KB", "mca"),
    "KB-list": (1116046, 1116047, "KB", "list"),
    "M31-MCA": (1116023, 1116024, "M31", "mca"),
    "M31-list": (1116022, 1116023, "M31", "list"),
}

FORBIDDEN_329_PACKET_NAMES = {
    "kb_list_v1.packet.json", "kb_mca_v1.packet.json",
    "m31_list_v1.packet.json", "m31_mca_v1.packet.json",
}

TEX_LABELS = [
    ("tex/cs25_cap_v12.tex", "lem:confine"),
    ("tex/cs25_cap_v12.tex", "cor:Fvalued"),
    ("tex/cs25_cap_v12.tex", "cor:base-rational-line-inertness-chart"),
    ("tex/cs25_cap_v12.tex", "thm:weil-lines"),
    ("tex/cs25_cap_v12.tex", "cor:T3-status"),
    ("tex/cs25_cap_v12.tex", "thm:extension-line-dimension-degree-ledger"),
    ("tex/cs25_cap_v12.tex", "thm:conditional-mca"),
    ("tex/cs25_cap_v12.tex", "rem:conditional-status"),
    ("tex/cs25_cap_v12.tex", "cor:extension-pole-deep-list-floor"),
    ("tex/cs25_cap_v12.tex", "cor:extension-pole-quotient-remainder-floor"),
    ("experimental/cap25_v13_experimental.tex", "prop:v13-extension"),
    ("experimental/cap25_v13_experimental.tex", "prop:v13f1-identity-frontier"),
    ("experimental/cap25_v13_experimental.tex", "prob:v13f1-frontier"),
]

NOTE_FILES = [
    "experimental/notes/f1/f1_minimal_field_descent.md",
    "experimental/notes/f1/f1_extension_coordinate_transfer.md",
    "experimental/notes/f1/f1_extension_import_lemma.md",
    "experimental/notes/ef/ef_galois_stabilizer_descent.md",
    "experimental/notes/ef/ef_full_orbit_cycle_descent.md",
    "experimental/notes/ef/ef_descended_cycle_inventory_soundness.md",
    "experimental/notes/ef/ef_descended_cycle_classification_soundness.md",
]

SCRIPT_SNIPPETS = [
    ("experimental/scripts/verify_paid_ledger_functions.py", "def extension_chart_upper"),
    ("experimental/scripts/verify_paid_ledger_functions.py",
     "does not classify every extension-valued residual chart"),
]
TOWARDS_V13_SCRIPT = os.path.join("experimental", "scripts", "towards v13",
                                   "cap25_v14_moved_frontier_checks.py")


# ---------------------------------------------------------------------------
# generic tamper/check helpers
# ---------------------------------------------------------------------------
def _corrupt(x):
    """Perturb a single stored/expected value for the tamper self-test."""
    if isinstance(x, bool):
        return not x
    if isinstance(x, int):
        return x + 1
    if isinstance(x, float):
        return x + 1.0
    if isinstance(x, str):
        return x + "_TAMPERED_NONEXISTENT"
    if isinstance(x, (list, tuple)):
        return list(x[:-1]) if x else [999999]
    return x


def check(actual, expected, *, tol=None, tamper=False):
    """Return True iff actual matches expected (within tol if given).
    Under tamper=True, `expected` (the stored/guarded side) is corrupted
    first -- this checks that the recompute (`actual`) would then disagree."""
    if tamper:
        expected = _corrupt(expected)
    if tol is not None:
        return abs(actual - expected) <= tol
    return actual == expected


# ---------------------------------------------------------------------------
# from-scratch number theory (small, cheap)
# ---------------------------------------------------------------------------
def is_prime(m: int) -> bool:
    if m < 2:
        return False
    for d in (2, 3):
        if m % d == 0:
            return m == d
    i = 5
    while i * i <= m:
        if m % i == 0 or m % (i + 2) == 0:
            return False
        i += 6
    return True


def divisors(e: int) -> list[int]:
    return [d for d in range(1, e + 1) if e % d == 0]


def mobius(m: int) -> int:
    if m == 1:
        return 1
    result, x, prime_factors = 1, m, 0
    d = 2
    while d * d <= x:
        if x % d == 0:
            x //= d
            prime_factors += 1
            if x % d == 0:
                return 0
        d += 1
    if x > 1:
        prime_factors += 1
    return -1 if prime_factors % 2 else 1


def deg_exactly_e_count(p: int, e: int) -> int:
    return sum(mobius(e // d) * p ** d for d in divisors(e))


def log2binom(N: int, M: int) -> float:
    return (lgamma(N + 1) - lgamma(M + 1) - lgamma(N - M + 1)) / log(2)


# ---------------------------------------------------------------------------
# expensive shared precompute -- runs EXACTLY ONCE, cached at module scope
# ---------------------------------------------------------------------------
def comb_cluster(nn: int, m_values: list[int]) -> dict[int, int]:
    """One math.comb() call at the smallest m, then exact O(size) ratio
    walk for the rest (m_values must be consecutive integers)."""
    m_values = sorted(set(m_values))
    base = m_values[0]
    c = math.comb(nn, base)
    out = {base: c}
    cur = base
    for m in m_values[1:]:
        while cur < m:
            c = c * (nn - cur) // (cur + 1)
            cur += 1
            out[cur] = c
    return out


_PRECOMPUTE: dict = {}


def precompute() -> None:
    if _PRECOMPUTE:
        return
    t0 = time.time()
    comb_KB = comb_cluster(n, [1116046, 1116047, 1116048])
    comb_M31 = comb_cluster(n, [1116022, 1116023, 1116024])
    pow_cache = {}
    for name, spec in FIELD.items():
        p = spec["p"]
        w_lo = 67470 if name == "KB" else 67446
        pw = pow(p, w_lo)
        pow_cache[(name, w_lo)] = pw
        pow_cache[(name, w_lo + 1)] = pw * p
    _PRECOMPUTE["comb"] = {"KB": comb_KB, "M31": comb_M31}
    _PRECOMPUTE["pow"] = pow_cache
    _PRECOMPUTE["dt"] = time.time() - t0


def bstar(name: str) -> int:
    spec = FIELD[name]
    return spec["p"] ** spec["e"] // (2 ** spec["t"])


# ---------------------------------------------------------------------------
# packet loader
# ---------------------------------------------------------------------------
def load_packet() -> dict:
    with open(JSON_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def load_note_text() -> str:
    with open(NOTE_PATH, encoding="utf-8") as fh:
        return fh.read()


def read_repo_file(rel_path: str) -> str:
    with open(os.path.join(REPO_ROOT, rel_path), encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# G1 -- field primes
# ---------------------------------------------------------------------------
def gate_G1_primes(packet, tamper=False):
    ok = True
    msgs = []
    for name, spec in FIELD.items():
        p = spec["p"]
        stored = packet["fields"][name]["prime_p"]
        first = (name == "KB")
        ok_i = check(p, stored, tamper=(tamper and first))
        ok_i = ok_i and is_prime(p)
        ok = ok and ok_i
        msgs.append(f"{name} p={p} stored={stored} prime={is_prime(p)} ok={ok_i}")
    assert p_KB == 2 ** 31 - 2 ** 24 + 1
    assert p_M31 == 2 ** 31 - 1
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# G2 -- B* budgets
# ---------------------------------------------------------------------------
def gate_G2_bstar(packet, tamper=False):
    ok = True
    msgs = []
    for idx, name in enumerate(("KB", "M31")):
        b = bstar(name)
        stored_b = packet["fields"][name]["B_star_budget"]
        stored_log2 = packet["fields"][name]["log2_B_star"]
        ok_b = check(b, stored_b, tamper=(tamper and idx == 0))
        ok_log2 = check(log2(b), stored_log2, tol=2e-3)
        ok = ok and ok_b and ok_log2
        msgs.append(f"{name} B*={b} stored={stored_b} log2 ok={ok_log2} ok={ok_b}")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# G3 -- subfield lattice + confinement densities
# ---------------------------------------------------------------------------
def gate_G3_subfields(packet, tamper=False):
    ok = True
    msgs = []
    for idx, name in enumerate(("KB", "M31")):
        spec = FIELD[name]
        e, p = spec["e"], spec["p"]
        divs = divisors(e)
        stored_divs = packet["fields"][name]["subfield_divisors"]
        ok_divs = check(divs, stored_divs, tamper=(tamper and idx == 0))
        # structural chain-vs-diamond check: KB (e=6) must be a non-chain
        # (2,3 incomparable); M31 (e=4) must be a full chain.
        pairs_comparable = all((d1 % d2 == 0 or d2 % d1 == 0)
                                for d1 in divs for d2 in divs)
        is_chain = pairs_comparable
        expect_chain = (name == "M31")
        ok_shape = (is_chain == expect_chain)
        # densities
        stored_dens = packet["fields"][name]["confinement_density_by_subfield"]
        dens_ok = True
        for d in divs:
            key = f"F_p{d}_{'base' if d == 1 else ('full' if d == e else 'tower')}"
            expected_log2 = (d - e) * log2(p)
            if key in stored_dens:
                dens_ok = dens_ok and check(expected_log2, stored_dens[key]["log2"], tol=2e-3)
        ok_i = ok_divs and ok_shape and dens_ok
        ok = ok and ok_i
        msgs.append(f"{name} divisors={divs} chain={is_chain}(expect {expect_chain}) dens_ok={dens_ok} ok={ok_i}")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# G4 -- full K=F stratum Mobius counts + Frobenius orbit divisibility
# ---------------------------------------------------------------------------
def gate_G4_full_stratum(packet, tamper=False):
    ok = True
    msgs = []
    for idx, name in enumerate(("KB", "M31")):
        spec = FIELD[name]
        e, p = spec["e"], spec["p"]
        cnt = deg_exactly_e_count(p, e)
        key = f"deg_exactly_{e}_count"
        stored = packet["fields"][name]["full_stratum_KeqF"]
        stored_cnt = int(stored[key])
        ok_cnt = check(cnt, stored_cnt, tamper=(tamper and idx == 0))
        remainder_zero = (cnt % e == 0)
        orbits = cnt // e
        stored_orbits = int(stored["num_frobenius_orbits"])
        ok_orbits = check(orbits, stored_orbits)
        proper = sum(p ** d for d in divisors(e) if d < e)
        stored_proper = int(str(packet["fields"][name]["proper_subfield_ambient_count"]["value"]).split("=")[-1].strip())
        ok_proper = check(proper, stored_proper)
        ok_i = ok_cnt and remainder_zero and ok_orbits and ok_proper
        ok = ok and ok_i
        msgs.append(f"{name} cnt_ok={ok_cnt} mod_e_zero={remainder_zero} orbits_ok={ok_orbits} proper_ok={ok_proper}")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# G5 -- e_Y cost verdicts (exact integer)
# ---------------------------------------------------------------------------
def gate_G5_ey_cost(packet, tamper=False):
    ok = True
    msgs = []
    for idx, name in enumerate(("KB", "M31")):
        p = FIELD[name]["p"]
        b = bstar(name)
        exceeds_1 = p > b
        exceeds_2 = p * p > b
        stored_v1 = packet["fields"][name]["one_pos_dim_chart_cost"]["verdict_vs_B_star"]
        stored_v2 = packet["fields"][name]["one_pos_dim_chart_cost"]["e_Y=2"]
        v1_says_exceeds = stored_v1.strip().startswith("EXCEEDS")
        v2_says_exceeds = "EXCEEDS" in stored_v2
        ok_1 = check(exceeds_1, v1_says_exceeds, tamper=(tamper and idx == 0))
        ok_2 = check(exceeds_2, v2_says_exceeds)
        ok_i = ok_1 and ok_2
        ok = ok and ok_i
        msgs.append(f"{name} e_Y=1 exceeds={exceeds_1}(stored {v1_says_exceeds}) e_Y=2 exceeds={exceeds_2}(stored {v2_says_exceeds}) ok={ok_i}")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# G6 -- the four v14 pairs + w_at_a0 (canonical, independent of JSON)
# ---------------------------------------------------------------------------
def gate_G6_pairs(packet, tamper=False):
    ok = True
    msgs = []
    rows_by_name = {r["row"]: r for r in packet["rows"]}
    for idx, (row_name, (a0, a1, field, kind)) in enumerate(CANON_PAIRS.items()):
        canon_a0 = _corrupt(a0) if (tamper and idx == 0) else a0
        row = rows_by_name[row_name]
        ok_a0 = (row["a0"] == canon_a0)
        ok_a1 = (row["a0_plus_1"] == a1) and (row["a0_plus_1"] == row["a0"] + 1)
        ok_pair = (row["line_pair_v14"] == [row["a0"], row["a0_plus_1"]])
        w_expect = (a0 - k - 1) if kind == "mca" else (a0 - k)
        ok_w = (row["w_at_a0"] == w_expect)
        ok_i = ok_a0 and ok_a1 and ok_pair and ok_w
        ok = ok and ok_i
        msgs.append(f"{row_name} a0={row['a0']}(canon {canon_a0}) w={row['w_at_a0']}(expect {w_expect}) ok={ok_i}")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# G7 -- THE HEADLINE GATE: exact unsafe/safe + exact Delta_ext ceiling floor
# ---------------------------------------------------------------------------
def gate_G7_exact_ledger(packet, tamper=False):
    ok = True
    msgs = []
    rows_by_name = {r["row"]: r for r in packet["rows"]}
    first = True
    for row_name, (a0, a1, field, kind) in CANON_PAIRS.items():
        row = rows_by_name[row_name]
        p = FIELD[field]["p"]
        B = bstar(field)
        w = row["w_at_a0"]
        L0 = _PRECOMPUTE["comb"][field][a0]
        L1 = _PRECOMPUTE["comb"][field][a1]
        pw0 = _PRECOMPUTE["pow"][(field, w)]
        pw1 = _PRECOMPUTE["pow"][(field, w + 1)]

        unsafe_ok = L0 > pw0 * B
        safe_ok = L1 <= pw1 * B
        exact_ceiling = (pw1 * B) // L1  # EXACT floor(2**fail_margin_bits), no floats

        stored_unsafe = row["unsafe_a0_exact"]
        stored_safe = row["safe_a0p1_exact"]
        stored_ceiling = row["ext_target"]["Delta_ext_ceiling_int"]

        # tamper targets exactly one guarded datum: the ceiling int on the
        # first row visited (this is the exact field the caught bug lives in)
        ceiling_check = check(exact_ceiling, stored_ceiling, tamper=(tamper and first))
        unsafe_check = check(unsafe_ok, stored_unsafe)
        safe_check = check(safe_ok, stored_safe)

        # loose float cross-check of fail_margin_bits (informational; not the
        # exact gate) via the same lgamma route as compute_ext.py
        fail_m = -(log2binom(n, a1) - (w + 1) * log2(p) - log2(B))
        margin_check = check(fail_m, row["fail_margin_bits"], tol=2e-3)

        # e_Y forced to 0: log2(p) must exceed every row's fail margin
        ey_forced_ok = (log2(p) > row["fail_margin_bits"]) == (row["ext_target"]["e_Y_forced"] == 0)

        ok_i = unsafe_check and safe_check and ceiling_check and margin_check and ey_forced_ok
        ok = ok and ok_i
        msgs.append(f"{row_name}: unsafe={unsafe_ok} safe={safe_ok} exact_ceiling={exact_ceiling}"
                    f"(stored {stored_ceiling}) margin~{fail_m:.4f}b ok={ok_i}")
        first = False
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# G8 -- reference existence (tex labels, note files, script snippets)
# ---------------------------------------------------------------------------
def gate_G8_refs_exist(tamper=False):
    ok = True
    msgs = []
    first = True
    for rel_path, label in TEX_LABELS:
        needle = f"label{{{label}}}"
        if tamper and first:
            needle = needle + "_TAMPERED_NONEXISTENT"
            first = False
        try:
            text = read_repo_file(rel_path)
        except OSError as exc:
            ok = False
            msgs.append(f"MISSING FILE {rel_path}: {exc}")
            continue
        found = needle in text
        ok = ok and found
        if not found:
            msgs.append(f"NOT FOUND: {label} in {rel_path}")
    for rel_path in NOTE_FILES:
        exists = os.path.isfile(os.path.join(REPO_ROOT, rel_path))
        ok = ok and exists
        if not exists:
            msgs.append(f"MISSING NOTE: {rel_path}")
    for rel_path, snippet in SCRIPT_SNIPPETS:
        try:
            text = read_repo_file(rel_path)
        except OSError as exc:
            ok = False
            msgs.append(f"MISSING FILE {rel_path}: {exc}")
            continue
        found = snippet in text
        ok = ok and found
        if not found:
            msgs.append(f"NOT FOUND snippet in {rel_path}: {snippet!r}")
    towards_exists = os.path.isfile(os.path.join(REPO_ROOT, TOWARDS_V13_SCRIPT))
    ok = ok and towards_exists
    if not towards_exists:
        msgs.append(f"MISSING: {TOWARDS_V13_SCRIPT}")
    if not msgs:
        msgs.append(f"all {len(TEX_LABELS)} tex labels + {len(NOTE_FILES)} note files + "
                     f"{len(SCRIPT_SNIPPETS)} script snippets + towards-v13 script found")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# G9 -- packet/note hygiene
# ---------------------------------------------------------------------------
def gate_G9_hygiene(packet, tamper=False):
    ok = True
    msgs = []
    ok_n = check(packet["meta"]["n"], n, tamper=tamper)
    ok_k = check(packet["meta"]["k"], k)
    ok = ok and ok_n and ok_k
    msgs.append(f"meta.n/k ok={ok_n and ok_k}")

    corr = packet.get("audit_corrections", [])
    ok_corr = len(corr) == 2 and all(
        entry["corrected_value"] + 1 == entry["source_draft_value"] for entry in corr
    )
    ok = ok and ok_corr
    msgs.append(f"audit_corrections consistent={ok_corr} (n={len(corr)})")

    shipped_name = os.path.basename(JSON_PATH)
    no_collision = shipped_name not in FORBIDDEN_329_PACKET_NAMES
    ok = ok and no_collision
    msgs.append(f"no_collision_with_pr329={no_collision} ({shipped_name!r})")

    try:
        note_text = load_note_text()
    except OSError as exc:
        ok = False
        msgs.append(f"note file missing: {exc}")
        note_text = ""
    required_markers = ["does not pay", "Merge hygiene", "PAID_BY_THEOREM", "CONDITIONAL_ON_NAMED_INPUT"]
    markers_ok = all(m in note_text for m in required_markers)
    ok = ok and markers_ok
    msgs.append(f"note markers ok={markers_ok}")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# G10 -- scanner cross-execution (re-run the shipped F1 toy scanner, fast subset)
# ---------------------------------------------------------------------------
def gate_G10_scanner_crosscheck(tamper=False):
    """Import the shipped f1_extension_full_orbit_scan.py and re-execute a fast
    subset of its menu here, trusting the scanner's code (not its emitted JSON).
    (a) slack t=1: full_count == C(n_toy,k_toy+1) == supports_scanned at p0 in
        {2,3}, chain e=4 (the divided-difference growth boundary);
    (b) slack t>=2: p0 in {2,3} at t=2 are INFEASIBLE (k+t>n -> vacuously zero),
        and the smallest feasible t=2 tower (p0=5 chain) has full_count == 0 and
        aggregate_full_count == 0."""
    import importlib
    scripts_dir = os.path.join(REPO_ROOT, "experimental", "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    try:
        scanner = importlib.import_module("f1_extension_full_orbit_scan")
    except Exception as exc:  # noqa: BLE001 -- surface as a failed gate, not a crash
        return False, f"could not import f1_extension_full_orbit_scan: {exc}"

    ok = True
    msgs = []
    first = True
    # (a) t=1 divided-difference growth: full_count == C(n,k+1) == supports
    for p0 in (2, 3):
        res = scanner.scan_tower(p0, 4, 1, "chain")
        n_toy, k_toy = res["n"], res["k"]
        expected = math.comb(n_toy, k_toy + 1)
        fc = res["primary_slope_field_statistic"]["best_over_full_orbit_beta_only"]["full_count"]
        supports = res["supports_scanned"]
        ok_eq = check(fc, expected, tamper=(tamper and first))  # tamper: the one guarded datum
        ok_sup = check(supports, expected)
        ok = ok and ok_eq and ok_sup
        msgs.append(f"t=1 p0={p0}: full_count={fc} C({n_toy},{k_toy + 1})={expected} "
                    f"supports={supports} ok={ok_eq and ok_sup}")
        first = False
    # (b) t>=2 zero-count: p0=2,3 infeasible at t=2; p0=5 chain genuine zero
    for p0 in (2, 3):
        r = scanner.scan_tower(p0, 4, 2, "chain")
        infeasible = (r.get("feasible") is False)
        ok = ok and infeasible
        msgs.append(f"t=2 p0={p0}: feasible={r.get('feasible')} (expect False->vacuous 0) ok={infeasible}")
    r5 = scanner.scan_tower(5, 4, 2, "chain")
    fc5 = r5["primary_slope_field_statistic"]["best_over_full_orbit_beta_only"]["full_count"]
    agg5 = r5["diagnostic_aggregate_statistic"]["aggregate_full_count"]
    ok_zero = check(fc5, 0) and check(agg5, 0)
    ok = ok and ok_zero
    msgs.append(f"t=2 p0=5 (smallest feasible): full_count={fc5} aggregate_full={agg5} "
                f"(expect 0/0) ok={ok_zero}")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
GATE_SPECS = [
    ("G1 field primes + forms                 ", lambda packet, t: gate_G1_primes(packet, t)),
    ("G2 B* budgets                            ", lambda packet, t: gate_G2_bstar(packet, t)),
    ("G3 subfield lattice + confinement dens.  ", lambda packet, t: gate_G3_subfields(packet, t)),
    ("G4 full K=F stratum (Mobius + orbits)    ", lambda packet, t: gate_G4_full_stratum(packet, t)),
    ("G5 e_Y cost verdicts                     ", lambda packet, t: gate_G5_ey_cost(packet, t)),
    ("G6 four v14 pairs + w_at_a0              ", lambda packet, t: gate_G6_pairs(packet, t)),
    ("G7 exact unsafe/safe + Delta_ext ceiling ", lambda packet, t: gate_G7_exact_ledger(packet, t)),
    ("G8 tex/md/script reference existence     ", lambda packet, t: gate_G8_refs_exist(t)),
    ("G9 packet/note hygiene                   ", lambda packet, t: gate_G9_hygiene(packet, t)),
    ("G10 scanner cross-exec (t=1 C(n,k+1)/t>=2 0)", lambda packet, t: gate_G10_scanner_crosscheck(t)),
]


def main() -> int:
    t0 = time.time()
    selftest = "--tamper-selftest" in sys.argv
    print("=" * 90)
    if selftest:
        print(" TAMPER SELF-TEST: each gate must FAIL when its guarded datum is corrupted")
    else:
        print(" verify_frontier_extension_cell_targets  (zero-arg)")
        print(" paid_extension cell targets, 4 deployed v14 rows -- TARGETS ONLY, does not pay the cell")
    print("=" * 90)

    try:
        packet = load_packet()
    except Exception as exc:  # noqa: BLE001 -- surface as a failed run, not a crash
        print(f"FATAL: could not load packet JSON: {exc}")
        return 1

    precompute()
    print(f" (shared bignum precompute: {_PRECOMPUTE['dt']:.1f}s, cached; not repeated per gate)")

    all_good = True
    for label, fn in GATE_SPECS:
        ok, summary = fn(packet, selftest)
        caught_or_pass = (not ok) if selftest else ok
        all_good = all_good and caught_or_pass
        tag = ("CAUGHT " if caught_or_pass else "MISSED!") if selftest else ("PASS" if ok else "FAIL")
        print(f"  {label}  {tag}")
        print(f"        {summary}")

    print("=" * 90)
    dt = time.time() - t0
    if selftest:
        print(f" SELF-TEST RESULT: {'all tampers CAUGHT' if all_good else 'A TAMPER WAS MISSED'}   ({dt:.1f}s)")
    else:
        print(f" RESULT: {'ALL GATES PASS' if all_good else 'FAILURE'}   ({dt:.1f}s)")
    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main())
