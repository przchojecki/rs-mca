#!/usr/bin/env python3
"""Independent checker for pf-deployed-rows (no generator import).

Disjoint routes from the generator throughout:

  big binomials C(n,a)   generator: Legendre floor-sum exponents +
                         product-tree.  here: Kummer carry-count exponents
                         (carries when adding a and n-a in base p) +
                         smallest-first heap merging.
  cycle-index binomials  generator: Legendre + product tree.
                         here: math.comb directly.
  floors / margins       recomputed from the checker's own integers with
                         ceil division; compared to BOTH the certificate
                         and the frozen in-tree numerics JSON.
  surpluses              recomputed with a top-1100-bit mantissa log2
                         (different width than the generator's 900) and an
                         lgamma cross-estimate (0.5-bit tolerance).
  flip thresholds        fresh upward scan using math.comb.
  pins                   fresh scan of the tex with fresh line hashes.

Accepts --check for convention parity (the check always runs).
Exit 0 with RESULT: PASS, nonzero otherwise.
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
    "experimental/data/certificates/pf-deployed-rows/pf_deployed_rows.json")
NUMERICS_REL = Path(
    "experimental/data/certificates/profile-envelope-numerics/"
    "profile_envelope_numerics.json")

N = 2 ** 21
K_DIM = 2 ** 20


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


def heap_comb(a: int, b: int, primes) -> int:
    """C(a,b) via Kummer exponents + smallest-first heap merging."""
    exps = [(pr, kummer_e(a, b, pr)) for pr in primes if pr <= a]
    heap = [pr ** e for pr, e in exps if e]
    heapq.heapify(heap)
    while len(heap) > 1:
        x = heapq.heappop(heap)
        y = heapq.heappop(heap)
        heapq.heappush(heap, x * y)
    return heap[0] if heap else 1


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


def run(root: Path) -> int:
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    assert cert.get("payload_sha256") == payload_hash(cert), "self-hash"
    assert cert["all_pass"] and cert["summary"]["verdict"] == "NO ISSUE"
    assert cert["checks_failed"] == 0 and not cert["failed_checks"]

    # ---- pins, fresh scan (against the file at the packet's tex_path)
    lines = (root / cert["tex_path"]).read_text(
        encoding="utf-8").splitlines()
    for lab, pin in cert["pins"].items():
        assert pin["found"], "pin not found in cert: %s" % lab
        line = lines[pin["line"] - 1]
        assert ("\\label{%s}" % lab) in line, "pin moved: %s" % lab
        assert hashlib.sha256(line.encode("utf-8")).hexdigest()[:16] \
            == pin["sha256_line"], "pin hash drift: %s" % lab
    assert cert["pins_ok"]
    print("pins: OK (%d labels)" % len(cert["pins"]))

    # ---- frozen numerics oracle, re-keyed independently
    ndata = json.loads((root / NUMERICS_REL).read_text(encoding="utf-8"))
    frozen = {row["row_id"]: row for row in ndata["deployed_rows"]}

    primes = sieve(N)
    for row_id, row in cert["rows"].items():
        p = row["p"]
        fr = frozen[row_id]
        assert row["B_star"] == fr["B_star"] == (p ** row["ext_deg"]) \
            >> row["target_bits"]
        assert row["circle"] == (row_id.startswith("m31"))
        factor = 2 if row["circle"] else 1
        assert row["circle_factor"] == factor
        sqrtp = math.isqrt(p)
        assert sqrtp == row["sqrt_p_floor"]
        assert sqrtp * sqrtp <= p < (sqrtp + 1) * (sqrtp + 1)
        K = K_DIM + 1 if row["kind"] == "mca" else K_DIM

        for tag, c in row["charts"].items():
            a, w = c["a"], c["w"]
            assert w == a - K == fr[tag]["w"] and a == fr[tag]["a"]
            cna = heap_comb(N, a, primes)
            # lgamma cross-estimate on the big binomial
            est = lgamma_log2_comb(N, a)
            assert abs(est - lg2(cna)) < 0.5, "lgamma drift C(n,a)"
            pw = p ** w
            L = -(-cna // pw)
            assert L == c["L_floor"] == fr[tag]["L_list_floor"], \
                "%s/%s floor" % (row_id, tag)
            assert 1 + (N - a + 1) + L == c["eprof_identity_lower"] \
                == fr[tag]["Eprof_identity_lower"]

            lam0 = factor * sqrtp
            assert lam0 == c["lambda_most_favorable"]
            clam = math.comb(lam0 + a - 1, a)          # disjoint route
            lhs = pw * clam
            holds = lhs <= cna
            assert holds is False
            assert c["pf_exact_holds"] is False
            surplus = lg2(lhs) - lg2(cna)
            assert abs(surplus - float(c["pf_surplus_bits"])) < 0.005, \
                "%s/%s surplus %.4f vs %s" % (row_id, tag, surplus,
                                              c["pf_surplus_bits"])
            est_l = w * math.log2(p) + lgamma_log2_comb(lam0 + a - 1, a) \
                - lgamma_log2_comb(N, a)
            assert abs(est_l - surplus) < 0.5, "lgamma drift surplus"
            assert abs(float(c["pf_surplus_bits_per_coordinate"])
                       - surplus / N) < 1e-4

            # flip threshold, fresh upward scan with math.comb
            lam = 1
            while pw * math.comb(lam + a - 1, a) <= cna:
                lam += 1
            assert lam - 1 == c["lambda_flip_threshold"], \
                "%s/%s flip" % (row_id, tag)
            assert 1 <= lam - 1 < 10 < lam0

            # exact Delta_pole sweep entries (monotone increasing)
            prev = None
            for dlt in (0, 1, 2):
                s = lg2(pw * math.comb(factor * (dlt + 1) * sqrtp + a - 1,
                                       a)) - lg2(cna)
                stored = float(c["surplus_sweep_exact_bits"]
                               ["Dpole=%d" % dlt])
                assert abs(s - stored) < 0.005
                assert prev is None or s > prev
                prev = s
            # C0 = 1/2 robustness probe entry
            s_half = lg2(pw * math.comb(factor * sqrtp // 2 + a - 1, a)) \
                - lg2(cna)
            assert abs(s_half - float(c["surplus_sweep_exact_bits"]
                                      ["C0=1/2"])) < 0.005
            assert s_half > 0
            print("  %-9s %s a=%d floor, eprof, surplus %s, Lambda*=%d, "
                  "sweep: OK" % (row_id, tag, a, c["pf_surplus_bits"],
                                 c["lambda_flip_threshold"]))

        La0 = row["charts"]["a0"]["L_floor"]
        La1 = row["charts"]["a1"]["L_floor"]
        assert La0 > row["B_star"] >= La1
        assert abs(float(row["pass_margin_bits_a0"])
                   - (lg2(La0) - lg2(row["B_star"]))) < 0.005
        assert abs(float(row["fail_margin_bits_a1"])
                   - (lg2(La1) - lg2(row["B_star"]))) < 0.005

    # ---- headline consistency
    hs = [float(c["pf_surplus_bits"]) for row in cert["rows"].values()
          for c in row["charts"].values()]
    assert min(hs) > 280001 and max(hs) < 471798
    flips = sorted({c["lambda_flip_threshold"]
                    for row in cert["rows"].values()
                    for c in row["charts"].values()})
    assert flips == [2, 3, 4]

    print("RESULT: PASS")
    print("payload_sha256:", cert["payload_sha256"])
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true",
                   help="accepted for convention parity; the check always runs")
    p.parse_args(argv)
    return run(repo_root())


if __name__ == "__main__":
    sys.exit(main())
