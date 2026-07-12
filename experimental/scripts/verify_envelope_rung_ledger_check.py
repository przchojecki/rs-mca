#!/usr/bin/env python3
"""Independent checker for envelope-rung-ledger (no generator import).

Disjoint routes from the generator throughout:

  binomials             generator: Legendre floor-sum exponents +
                        product-tree.  here: Kummer carry-count exponents
                        (carries when adding b and a-b in base p) +
                        smallest-first heap merging; math.comb spot checks
                        on small arguments.
  floors / conversions  recomputed from the checker's own integers with
                        ceil division; deep-point conversion re-derived.
  verdicts              fires / TIGHT re-decided by exact cross
                        comparisons; the certificate verdict itself is
                        re-derived from the recomputed cells (a firing
                        frontier-covering cell forces
                        COUNTEREXAMPLE_NEW_FLOOR).
  margins               recomputed with a top-1100-bit mantissa log2
                        (different width than the generator's 900) and an
                        lgamma cross-estimate (0.5-bit tolerance).
  pins                  fresh scan of both tex files and the Lean module
                        with fresh line hashes.
  oracles               frozen numerics floors, committed
                        v13_raw_moved_pair blocks, unchanged-pair list
                        packets, and the addendum sec 3.2 tables re-read
                        and re-compared independently.

Accepts --check for convention parity (the check always runs).
Exit 0 with RESULT: PASS, nonzero otherwise.  No timing in any output.
"""
from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import math
import sys
from pathlib import Path

CERT_REL = Path(
    "experimental/data/certificates/envelope-rung-ledger/"
    "envelope_rung_ledger.json")
NUMERICS_REL = Path(
    "experimental/data/certificates/profile-envelope-numerics/"
    "profile_envelope_numerics.json")
FRONTIER_ADJ_DIR = Path("experimental/data/certificates/frontier-adjacent")

N = 2 ** 21
K_DIM = 2 ** 20

ADDENDUM_GCEIL_2DP = {
    "kb_mca": [-22.20, -29.48, -32.87, -34.32, -34.79, -50.36, -56.93,
               -57.93, -47.34, -40.06, -36.16, -33.96, -48.20, -54.93,
               -57.93, -57.93, -57.93, -44.45, -52.12, -55.93, -57.93],
    "m31_mca": [-3.26, -3.04, -2.68, -2.25, -17.37, -9.10, -4.71, -2.27,
                -16.39, -7.61, -2.96, -0.39, -14.45, -21.19, -24.00,
                -24.00, -24.00, -10.52, -18.19, -22.00, -24.00],
}
MAINTAINER_SCRIPT_MARGINS = {
    "kb_mca": (8.978, -22.197),
    "m31_mca": (27.927, -3.259),
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj) -> str:
    clone = dict(obj)
    clone.pop("payload_sha256", None)
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def kummer_e(a: int, b: int, p: int) -> int:
    """exponent of p in C(a,b): carries when adding b + (a-b) in base p."""
    carries, carry = 0, 0
    x, y = b, a - b
    while x or y or carry:
        s = x % p + y % p + carry
        carry = 1 if s >= p else 0
        carries += carry
        x //= p
        y //= p
    return carries


def sieve(limit: int):
    isp = bytearray([1]) * (limit + 1)
    isp[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(limit) + 1):
        if isp[i]:
            isp[i * i::i] = bytearray(len(isp[i * i::i]))
    return [i for i in range(limit + 1) if isp[i]]


_PRIMES = None


def primes():
    global _PRIMES
    if _PRIMES is None:
        _PRIMES = sieve(N)
    return _PRIMES


_CACHE: dict[tuple[int, int], int] = {}


def heap_comb(a: int, b: int) -> int:
    """C(a,b) via Kummer exponents + smallest-first heap merging."""
    if b < 0 or b > a:
        return 0
    b = min(b, a - b)
    key = (a, b)
    if key in _CACHE:
        return _CACHE[key]
    heap = []
    for pr in primes():
        if pr > a:
            break
        e = kummer_e(a, b, pr)
        if e:
            heap.append(pr ** e)
    heapq.heapify(heap)
    while len(heap) > 1:
        x = heapq.heappop(heap)
        y = heapq.heappop(heap)
        heapq.heappush(heap, x * y)
    val = heap[0] if heap else 1
    _CACHE[key] = val
    return val


def lg2(x: int) -> float:
    """log2 via top-1100-bit mantissa (different width than generator)."""
    bl = x.bit_length()
    if bl <= 1100:
        return math.log2(x)
    shift = bl - 1100
    return math.log2(x >> shift) + shift


def lgamma_log2_comb(a: int, b: int) -> float:
    return (math.lgamma(a + 1) - math.lgamma(b + 1)
            - math.lgamma(a - b + 1)) / math.log(2)


def deep_point_M(L: int, q: int) -> int:
    num = L * (q - N)
    den = (q - N) + K_DIM * (L - 1)
    return -(-num // den)


def w_c_remainder(s: int, sigma: int, c: int) -> int:
    if sigma <= 0:
        return 0
    Q, rem = divmod(sigma, c)
    return Q * (s + 1) + min(rem, s)


def check_margin(stored: float, num: int, den: int, what: str) -> None:
    got = lg2(num) - lg2(den)
    assert abs(stored - got) <= 2e-4, \
        "%s margin %.4f vs recomputed %.6f" % (what, stored, got)


def run(root: Path) -> int:
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    assert cert.get("payload_sha256") == payload_hash(cert), "self-hash"
    assert cert["checks_failed"] == 0 and not cert["failed_checks"]
    assert cert["all_pass"] is True

    # ---- pins, fresh scan (tex labels and Lean declarations)
    for group, labeler in (("frontiers", "\\label{%s}"),
                           ("cap25", "\\label{%s}")):
        rel = cert["tex_paths"][group]
        lines = (root / rel).read_text(encoding="utf-8").splitlines()
        for lab, pin in cert["pins"][group].items():
            assert pin["found"], "pin not found in cert: %s" % lab
            line = lines[pin["line"] - 1]
            assert (labeler % lab) in line, "pin moved: %s" % lab
            assert hashlib.sha256(line.encode("utf-8")).hexdigest()[:16] \
                == pin["sha256_line"], "pin hash drift: %s" % lab
    lean_text = (root / cert["tex_paths"]["lean"]).read_text(
        encoding="utf-8")
    lean_lines = lean_text.splitlines()
    for decl, pin in cert["pins"]["lean"].items():
        assert pin["found"], "lean pin not found in cert: %s" % decl
        line = lean_lines[pin["line"] - 1]
        assert decl in line and line.strip().startswith(
            ("theorem", "structure")), "lean pin moved: %s" % decl
        assert hashlib.sha256(line.encode("utf-8")).hexdigest()[:16] \
            == pin["sha256_line"], "lean pin hash drift: %s" % decl
    assert "sorry" not in lean_text and "admit" not in lean_text
    assert cert["pins_ok"]
    npins = sum(len(v) for v in cert["pins"].values())
    print("pins: OK (%d labels/declarations, 3 files)" % npins)

    # ---- oracles, re-read independently
    ndata = json.loads((root / NUMERICS_REL).read_text(encoding="utf-8"))
    frozen = {row["row_id"]: row for row in ndata["deployed_rows"]}
    moved = {}
    for slug in ("kb_mca", "m31_mca"):
        pk = json.loads((root / FRONTIER_ADJ_DIR
                         / f"{slug}_v1.packet.json").read_text(
                             encoding="utf-8"))
        moved[slug] = pk["v13_raw_moved_pair"]
    list_old = {}
    for slug in ("kb_list", "m31_list"):
        pk = json.loads((root / FRONTIER_ADJ_DIR
                         / f"{slug}_v1.packet.json").read_text(
                             encoding="utf-8"))
        list_old[slug] = pk["rung_margin_audit"]["per_agreement"]["a0+1"][
            "rungs"]

    # ---- spot self-test of the binomial route
    for (nn, kk) in ((100, 37), (2048, 1027), (65536, 30000)):
        assert heap_comb(nn, kk) == math.comb(nn, kk)

    any_fires_recomputed = False
    firing_recomputed = []
    tight_recomputed = []

    for row_id, row in cert["rows"].items():
        p, ext, tbits = row["p"], row["ext_deg"], row["target_bits"]
        kind, K = row["kind"], row["K"]
        a0, a1 = row["a0"], row["a0_plus_1"]
        q = p ** ext
        Bstar = q >> tbits
        assert Bstar == row["B_star"] == frozen[row_id]["B_star"]
        assert q % (1 << tbits) != 0
        assert K == (K_DIM + 1 if kind == "mca" else K_DIM)
        assert a1 == a0 + 1 and row["sigma"] == a1 - K
        assert q.bit_length() == row["q_line_bits"]
        print("  %-9s %s p=%d q=p^%d eps*=2^-%d K=%d pair=(%d,%d) B*=%d"
              % (row_id, kind, p, ext, tbits, K, a0, a1, Bstar))

        # identity anchors vs frozen floors and committed moved-pair blocks
        for tag, aa in (("a0", a0), ("a1", a1)):
            anc = row["identity_anchor"][tag]
            w = aa - K
            assert anc["a"] == aa == frozen[row_id][tag]["a"]
            assert anc["w"] == w == frozen[row_id][tag]["w"]
            cna = heap_comb(N, aa)
            est = lgamma_log2_comb(N, aa)
            assert abs(est - lg2(cna)) < 0.5, "lgamma drift C(n,a)"
            L = -(-cna // p ** w)
            assert L == anc["L"] == frozen[row_id][tag]["L_list_floor"]
            M = deep_point_M(L, q) if kind == "mca" else L
            assert M == anc["M"] and anc["M_equals_L"] == (M == L)
            fires = M > Bstar
            tight = (2 * M > Bstar) and (M < 2 * Bstar)
            assert anc["fires"] == fires and anc["TIGHT"] == tight
            check_margin(anc["margin_bits"], M, Bstar,
                         "%s/%s identity" % (row_id, tag))
        assert row["identity_anchor"]["a0"]["fires"] is True
        assert row["identity_anchor"]["a1"]["fires"] is False

        if kind == "mca":
            vmp = moved[row_id]
            anc0 = row["identity_anchor"]["a0"]
            anc1 = row["identity_anchor"]["a1"]
            assert vmp["new_pair"]["a0_prime"] == a0
            assert vmp["new_pair"]["a0_prime_plus_1"] == a1
            assert vmp["identity_floor_L_a0p"] == anc0["L"]
            assert vmp["deep_point_M_a0p"] == anc0["M"]
            assert vmp["identity_floor_L_a1p"] == anc1["L"]
            assert vmp["deep_point_M_a1p"] == anc1["M"]
            assert abs(vmp["pass_margin_bits_a0p"]
                       - anc0["margin_bits"]) <= 5e-4
            assert abs(vmp["fail_margin_bits_a1p"]
                       - anc1["margin_bits"]) <= 5e-4
            assert vmp["deficit_to_cross_Bstar_a1p"] \
                == (Bstar + 1) - anc1["M"]
            mp, mf = MAINTAINER_SCRIPT_MARGINS[row_id]
            assert abs(anc0["margin_bits"] - mp) <= 0.1
            assert abs(anc1["margin_bits"] - mf) <= 0.1
            # the maintainer script's own assertions, from our integers
            cna0 = heap_comb(N, a0)
            pw = p ** (a0 - K)
            assert cna0 > pw * Bstar
            assert cna0 * (N - a0) // (a0 + 1) <= pw * p * Bstar
            L0 = Bstar + 1
            assert (L0 * (L0 - 1) // 2) * K_DIM < q - N
            assert (L0 * (L0 - 1) // 2) * K_DIM < q - p
            N1 = -(-cna0 // pw)
            assert N1 > Bstar
            assert N1 * (N1 - 1) * K_DIM < 2 * (q - N)

        # ---- the full rung ledger, cell by cell
        sigma = a1 - K
        rungs = row["rung_ledger_at_a0_plus_1"]
        assert [r["c"] for r in rungs] == [2 ** j for j in range(21)]
        for r in rungs:
            c, Nc = r["c"], r["N"]
            assert Nc == N // c
            ceilKc = -(-K // c)

            gfl = r["Gfloor"]
            m_f = a1 // c
            assert gfl["m"] == m_f and gfl["covered"] == m_f * c
            assert gfl["covers_frontier"] == (m_f * c >= a1)
            w_f = m_f - ceilKc
            if w_f < 0:
                assert gfl["degenerate"] is True
            else:
                assert gfl["degenerate"] is False and gfl["w"] == w_f
                L = -(-heap_comb(Nc, m_f) // p ** w_f)
                M = deep_point_M(L, q) if kind == "mca" else L
                assert gfl["L"] == L and gfl["M"] == M
                assert gfl["fires"] == (M > Bstar)
                assert gfl["TIGHT"] == ((2 * M > Bstar) and (M < 2 * Bstar))
                check_margin(gfl["margin_bits"], M, Bstar,
                             "%s Gfloor c=%d" % (row_id, c))

            gce = r["Gceil"]
            m_c = -(-a1 // c)
            assert gce["m"] == m_c and gce["covered"] == m_c * c
            assert gce["covers_frontier"] is True and m_c * c >= a1
            w_c = m_c - ceilKc
            assert w_c >= 0 and gce["w"] == w_c
            L = -(-heap_comb(Nc, m_c) // p ** w_c)
            M = deep_point_M(L, q) if kind == "mca" else L
            assert gce["L"] == L and gce["M"] == M
            assert gce["fires"] == (M > Bstar)
            assert gce["TIGHT"] == ((2 * M > Bstar) and (M < 2 * Bstar))
            check_margin(gce["margin_bits"], M, Bstar,
                         "%s Gceil c=%d" % (row_id, c))
            if c > 1 and gfl["covers_frontier"] \
                    and not gfl.get("degenerate"):
                assert gfl["L"] == gce["L"], "c|a Gfloor != Gceil"

            rem = r["Rem"]
            s = a1 - m_f * c
            w_r = w_c_remainder(s, sigma, c)
            assert rem["m"] == m_f and rem["s"] == s
            assert rem["covered"] == a1 and rem["covers_frontier"] is True
            assert rem["w_rem"] == w_r
            mass = heap_comb(Nc, m_f) * heap_comb(N - m_f * c, s)
            L = -(-mass // p ** w_r)
            M = deep_point_M(L, q) if kind == "mca" else L
            assert rem["L"] == L and rem["M"] == M
            assert rem["fires"] == (M > Bstar)
            assert rem["TIGHT"] == ((2 * M > Bstar) and (M < 2 * Bstar))
            check_margin(rem["margin_bits"], M, Bstar,
                         "%s Rem c=%d" % (row_id, c))
            if c == 1:
                assert s == 0 and w_r == sigma
                assert L == row["identity_anchor"]["a1"]["L"]

            pla = r["Plant"]
            Pc = heap_comb(Nc - 1, K_DIM // c)
            assert pla["defined"] is True
            assert pla["sigma_needed"] == a1 - K_DIM
            assert pla["max_covered_agreement"] == K_DIM + c - 1
            assert pla["covers_frontier"] == (a1 - K_DIM < c)
            assert pla["P_bit_length"] == Pc.bit_length()
            if "P" in pla:
                assert pla["P"] == Pc and Pc.bit_length() <= 128
            assert pla["fires_vs_Bstar"] == (Pc > Bstar)
            assert pla["TIGHT_vs_Bstar"] \
                == ((2 * Pc > Bstar) and (Pc < 2 * Bstar))
            check_margin(pla["margin_bits"], Pc, Bstar,
                         "%s Plant c=%d" % (row_id, c))
            if pla["covers_frontier"] and kind == "mca":
                assert pla["deep_point_M_equals_P"] \
                    == (deep_point_M(Pc, q) == Pc)

            # frontier verdict accumulation (re-derived)
            for prof in ("Gfloor", "Gceil", "Rem"):
                cell = r[prof]
                if cell.get("degenerate") or not cell["covers_frontier"]:
                    continue
                if cell["fires"]:
                    any_fires_recomputed = True
                    firing_recomputed.append((row_id, prof, c))
                elif cell["TIGHT"]:
                    tight_recomputed.append(
                        (row_id, prof, c, cell["margin_bits"]))
            if pla["covers_frontier"]:
                if pla["fires_vs_Bstar"]:
                    any_fires_recomputed = True
                    firing_recomputed.append((row_id, "Plant", c))
                elif pla["TIGHT_vs_Bstar"]:
                    tight_recomputed.append(
                        (row_id, "Plant", c, pla["margin_bits"]))

        # row summary re-derivation
        s_ = row["summary"]
        fr_margins = []
        for r in rungs:
            for prof in ("Gfloor", "Gceil", "Rem"):
                cell = r[prof]
                if not cell.get("degenerate") and cell["covers_frontier"]:
                    fr_margins.append(cell["margin_bits"])
            if r["Plant"]["covers_frontier"]:
                fr_margins.append(r["Plant"]["margin_bits"])
        assert s_["frontier_covering_cells"] == len(fr_margins)
        assert s_["min_frontier_margin_bits"] == min(fr_margins)
        assert s_["max_frontier_margin_bits"] == max(fr_margins)
        assert s_["any_frontier_rung_fires"] \
            == any(row_id == fr[0] for fr in firing_recomputed)
        assert s_["any_frontier_rung_tight"] \
            == any(row_id == t[0] for t in tight_recomputed)

        # addendum sec 3.2 replay (MCA rows) from recomputed cells
        if row_id in ADDENDUM_GCEIL_2DP:
            got = [round(r["Gceil"]["margin_bits"], 2) for r in rungs]
            assert got == ADDENDUM_GCEIL_2DP[row_id], \
                "%s addendum sec 3.2 drift" % row_id

        # unchanged-pair list packets: graded fires verdicts must agree
        if kind == "list":
            for r_new, r_old in zip(rungs, list_old[row_id]):
                assert r_new["c"] == r_old["c"]
                gf_n, gf_o = r_new["Gfloor"], r_old["Gfloor"]
                if not gf_n.get("degenerate") and "fires" in gf_o:
                    assert gf_n["fires"] == gf_o["fires"]
                gc_o = r_old.get("Gceil", {})
                if "fires" in gc_o:
                    assert r_new["Gceil"]["fires"] == gc_o["fires"]
        print("            rung ledger: 21 rungs x 4 profiles recomputed, "
              "all cells match")

    # ---- verdict is an outcome: re-derive it
    assert cert["ledger_outcome"]["any_frontier_rung_fires"] \
        == any_fires_recomputed
    assert len(cert["ledger_outcome"]["firing_rungs"]) \
        == len(firing_recomputed)
    assert len(cert["ledger_outcome"]["tight_rungs"]) \
        == len(tight_recomputed)
    if any_fires_recomputed:
        assert cert["verdict"] == "COUNTEREXAMPLE_NEW_FLOOR"
        print("RESULT: FIRING RUNG -- verdict COUNTEREXAMPLE_NEW_FLOOR")
        print(firing_recomputed)
        return 2
    assert cert["verdict"] == "NO ISSUE"

    # the committed watch-item, from the recomputed tight set
    w = cert["watch_item"]
    assert w is not None and len(tight_recomputed) == 1
    trow, tprof, tc, tmargin = tight_recomputed[0]
    assert (trow, tprof, tc) == ("m31_mca", "Gceil", 2048)
    assert w["row"] == trow and w["profile"] == tprof and w["c"] == tc
    assert w["L"] == w["M"] == 12769758 and w["B_star"] == 16777215
    assert abs(w["margin_bits"] - (-0.3938)) <= 5e-4
    assert w["headroom_to_Bstar"] == 16777215 - 12769758 == 4007457
    assert w["additional_to_fire"] == 4007458
    assert w["endpoint_multiplier_sensitivity"][
        "would_fire_under_2^1_multiplier"] is True
    vmp_tr = moved["m31_mca"]["tight_rung_at_a1p"]
    assert vmp_tr["L"] == w["L"] and vmp_tr["M"] == w["M"]
    assert vmp_tr["c"] == w["c"] and vmp_tr["covered"] == w["covered"]
    assert abs(vmp_tr["margin_bits"] - w["margin_bits"]) <= 5e-4

    print("RESULT: PASS")
    print("payload_sha256:", cert["payload_sha256"])
    print("verdict:", cert["verdict"])
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="accepted for convention parity; the check "
                         "always runs")
    ap.parse_args(argv)
    return run(repo_root())


if __name__ == "__main__":
    sys.exit(main())
