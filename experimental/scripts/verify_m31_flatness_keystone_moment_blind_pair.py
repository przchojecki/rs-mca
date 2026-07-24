#!/usr/bin/env python3
"""Exact stdlib replay for the M31 990-moment flatness obstruction."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT = Path("experimental/data/certificates/m31-flatness-keystone-moment-blind-pair/m31_flatness_keystone_moment_blind_pair.json")
NOTE = Path("experimental/notes/thresholds/m31_flatness_keystone_moment_blind_pair.md")
SCRIPT = Path("experimental/scripts/verify_m31_flatness_keystone_moment_blind_pair.py")
SUMS = Path("experimental/data/certificates/m31-flatness-keystone-moment-blind-pair/SHA256SUMS.txt")
HASHED = (NOTE, CERT, SCRIPT)
BASE = "d968e1cb9a3a6dbcfba35ecf9f448b4a373a35bb"
UPSTREAM = "71f64349a8fa8cbf05678a6e9d4e00e8e06d7de5"
PINS = {
    "experimental/grande_finale.tex": "8a5d9791900ca9eed773feba146b92ad296704ce",
    "experimental/notes/frontier-adjacent/four_row_exact_completion_compiler_v1.md": "375f99c02d59cefb6842b91115f07b88e2e258cc",
    "experimental/notes/thresholds/m31_quotient_prefix_flatness_t64_witness.md": "f422a80d89568bed5be9688b7cc1975786d5d983",
    "experimental/notes/thresholds/m31_quotient_band_swap_census_t16_mixing.md": "9f2756cd3225787d4990acca9474fffb7ccd7e9e",
    "experimental/notes/thresholds/m31_quotient_t16_mixing_floor.md": "a8576317dfcbbdd4d516167a1c61e500b1a6e1fc",
    "experimental/notes/thresholds/cap25_v13_gammar_order_floor.md": "814f3ae327cb507a5326f7ff5ec4b129e8c10e97",
}
STATUSES = ["PROVED_ABSTRACT", "COUNTEREXAMPLE_TO_HISTOGRAM_MOMENT_ONLY_INFERENCE", "ROUTE_CUT", "OPEN_RS_PREFIX_REALIZABILITY"]
NONCLAIMS = [
    "not an RS locator-prefix map",
    "not a received word or list-decoding counterexample",
    "not a first-match survivor",
    "not a codeword, explanation, ray, or slope projection",
    "not a U_Q upper or lower row atom",
    "not a claim that all order-991 Prouhet constructions fail",
    "not a refutation of target-labelled Fourier, kernel, or RS-realizability inputs",
]

class Fail(RuntimeError):
    pass

CHECKS = 0

def req(ok: bool, msg: str) -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        raise Fail(msg)

def intval(x: Any, name: str) -> int:
    if isinstance(x, bool):
        raise Fail(f"{name}: bool is not an integer")
    if isinstance(x, int):
        return x
    if isinstance(x, str) and x.isdigit() and (x == "0" or not x.startswith("0")):
        return int(x)
    raise Fail(f"{name}: expected canonical nonnegative integer")

def canon(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"

def load() -> dict[str, Any]:
    text = (ROOT / CERT).read_text(encoding="utf-8")
    data = json.loads(text)
    req(isinstance(data, dict), "certificate root")
    req(text == canon(data), "canonical certificate JSON")
    return data

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def parse_sums(text: str) -> dict[Path, str]:
    out: dict[Path, str] = {}
    for line in text.splitlines():
        digest, sep, raw = line.partition("  ")
        req(bool(sep) and len(digest) == 64 and all(c in "0123456789abcdef" for c in digest), "checksum syntax")
        p = Path(raw)
        req(not p.is_absolute() and ".." not in p.parts and p not in out, "checksum path")
        out[p] = digest
    return out

def parse_note(text: str) -> dict[str, int]:
    a, b = "<!-- VERIFIED-INTEGERS-BEGIN -->", "<!-- VERIFIED-INTEGERS-END -->"
    req(text.count(a) == text.count(b) == 1, "verified block markers")
    body = text.split(a, 1)[1].split(b, 1)[0].strip()
    out: dict[str, int] = {}
    for line in body.splitlines():
        key, sep, raw = line.partition("=")
        req(bool(sep) and key.replace("_", "").isalnum() and raw.isdigit() and key not in out, "verified block syntax")
        out[key] = int(raw)
    return out

def derive(data: dict[str, Any], heavy: bool) -> dict[str, int]:
    req(data.get("schema_version") == 1, "schema")
    req(data.get("packet_id") == "M31_FLATNESS_KEYSTONE_MOMENT_BLIND_PAIR_V1", "packet id")
    req(data.get("date") == "2026-07-23", "date")
    req(data.get("status") == STATUSES, "statuses")
    req(data.get("nonclaims") == NONCLAIMS, "nonclaims")
    expected_workboard = {
        "B_star": 16777215,
        "agreement": 1116023,
        "architecture": "DIRECT_ABSTRACT_OCCUPANCY_OBSTRUCTION",
        "atom_or_cell": "Q / depth-32 quotient prefix maximum versus average",
        "item": "M1", "object": "LIST", "row": "Mersenne-31 list at 2^-100", "target_epsilon": "2^-100",
    }
    req(data.get("workboard") == expected_workboard, "workboard")
    prov = data.get("provenance")
    req(isinstance(prov, dict), "provenance")
    req(prov.get("lab_base_commit") == BASE and prov.get("upstream_commit") == UPSTREAM, "commit provenance")
    req(prov.get("proof_dependency") == "SELF_CONTAINED_FINITE_DIFFERENCE_IDENTITY_AND_EXACT_INTEGER_ARITHMETIC", "proof dependency")
    context = prov.get("context_sources")
    req(isinstance(context, list), "context list")
    req({x.get("path"): x.get("git_blob_sha1") for x in context if isinstance(x, dict)} == PINS, "context pins")
    req(all(isinstance(x, dict) and x.get("gating") is False for x in context), "context must not gate")
    steering = prov.get("steering_sources")
    req(isinstance(steering, list), "steering provenance shape")
    req(all(isinstance(s, dict) and s.get("gating") is False for s in steering), "steering must not gate")

    p, d, n, w, B = 2**31 - 1, 32, 1022, 479, 16777215
    q, N = p**d, math.comb(n, w)
    floor_avg, rem = divmod(N, q)
    ceil_avg = floor_avg + (rem != 0)
    r, m, h = 990, 991, B // 990
    x, M = B - r*h, 2**r
    twice, T = 2*x + m*h, 2**(r-1) * (2*x + m*h)
    K, S = q - M, N - T
    c, t = divmod(S, K)
    bad = x + m*h
    r2, m2, h2, x2 = 991, 992, B // 992 + 1, 0
    twice2 = 2*x2 + m2*h2
    T2 = 2**(m2-2) * twice2

    expected_instance = {
        "average_remainder": str(rem), "ceil_average": ceil_avg, "depth": d,
        "domain_size": n, "floor_average": floor_avg, "full_image": True,
        "p": p, "support_size": w, "target_bins": str(q), "total_supports": str(N),
    }
    expected_pair = {
        "bad_excess": bad-B, "bad_max": bad, "bad_parity": "ODD", "bins_per_parity": str(M),
        "block_mass_per_side": str(T), "block_twice_mean": twice,
        "falling_moment_orders_equal": "0..990", "filler_bins": str(K),
        "filler_high": c+1, "filler_high_multiplicity": str(t), "filler_low": c,
        "filler_low_multiplicity": str(K-t), "filler_mass": str(S),
        "finite_difference_order": m, "good_max": B, "good_parity": "EVEN",
        "minimum_fiber": x, "moment_order": r, "offset": x,
        "raw_moment_orders_equal": "0..990", "step": h,
    }
    expected_boundary = {
        "exceeds_total_supports_by": str(T2-N), "finite_difference_order": m2,
        "minimizing_offset": x2, "minimizing_step": h2,
        "minimum_block_mass_per_side": str(T2), "minimum_twice_mean": twice2,
        "moment_order": r2,
        "scope": "single affine binomial parity block with nonnegative integer offset and positive integer step",
    }
    req(data.get("instance") == expected_instance, "instance arithmetic")
    req(data.get("moment_blind_pair") == expected_pair, "pair arithmetic")
    req(data.get("next_order_affine_binomial_boundary") == expected_boundary, "next-order arithmetic")

    req(0 < x < c < c+1 < B < bad, "positive full-image ordering")
    req(sum(math.comb(m,j) for j in range(0,m+1,2)) == M, "even bin count")
    req(sum(math.comb(m,j) for j in range(1,m+1,2)) == M, "odd bin count")
    req(sum(math.comb(m,j)*(x+j*h) for j in range(0,m+1,2)) == T, "even block mass")
    req(sum(math.comb(m,j)*(x+j*h) for j in range(1,m+1,2)) == T, "odd block mass")
    req(M+K == q and T+c*K+t == N and 0 < t < K, "filler totals")

    lo = 2*B + 2 - m2*(h2-1)
    req(lo > m2*h2 == twice2, "two-case next-order minimum")
    candidates = []
    for hh in range(1, B//(m2-1)+1):
        xx = max(0, B-m2*hh+1)
        if xx+(m2-1)*hh <= B < xx+m2*hh:
            candidates.append((2*xx+m2*hh, hh, xx))
    req(min(candidates) == (twice2,h2,x2), "brute next-order minimum")
    req(T2 > N, "next-order block exceeds support total")

    if heavy:
        coeff = [math.comb(m,j)*(1 if j%2 == 0 else -1) for j in range(m+1)]
        values = [x+j*h for j in range(m+1)]
        powers = [1]*(m+1)
        falling = [1]*(m+1)
        for k in range(r+1):
            req(sum(a*b for a,b in zip(coeff,powers,strict=True)) == 0, f"raw moment {k}")
            req(sum(a*b for a,b in zip(coeff,falling,strict=True)) == 0, f"falling moment {k}")
            if k < r:
                powers = [a*b for a,b in zip(powers,values,strict=True)]
                falling = [a*(b-k) for a,b in zip(falling,values,strict=True)]

    return dict(p=p,depth=d,domain_size=n,support_size=w,q=q,N=N,floor_average=floor_avg,
                ceil_average=ceil_avg,remainder=rem,B=B,r=r,m=m,h=h,x=x,M=M,
                good_max=B,bad_max=bad,bad_excess=bad-B,twice_mean=twice,T=T,
                K=K,S=S,c=c,t=t,r2=r2,m2=m2,h2=h2,x2=x2,twice_mean2=twice2,T2=T2)

def note_expected(v: dict[str,int]) -> dict[str,int]:
    return {
        "p":v["p"], "depth":v["depth"], "domain_size":v["domain_size"], "support_size":v["support_size"],
        "target_bins":v["q"], "total_supports":v["N"], "floor_average":v["floor_average"],
        "ceil_average":v["ceil_average"], "average_remainder":v["remainder"], "budget":v["B"],
        "moment_order":v["r"], "finite_difference_order":v["m"], "step":v["h"], "offset":v["x"],
        "bins_per_parity":v["M"], "good_max":v["good_max"], "bad_max":v["bad_max"],
        "bad_excess":v["bad_excess"], "block_twice_mean":v["twice_mean"], "block_mass_per_side":v["T"],
        "filler_bins":v["K"], "filler_mass":v["S"], "filler_low":v["c"], "filler_high":v["c"]+1,
        "filler_high_multiplicity":v["t"], "filler_low_multiplicity":v["K"]-v["t"],
        "next_moment_order":v["r2"], "next_finite_difference_order":v["m2"],
        "next_minimizing_step":v["h2"], "next_minimizing_offset":v["x2"],
        "next_minimum_twice_mean":v["twice_mean2"], "next_minimum_block_mass_per_side":v["T2"],
        "next_block_exceeds_total_by":v["T2"]-v["N"],
    }

def finish(v: dict[str,int]) -> None:
    note = (ROOT/NOTE).read_text(encoding="utf-8")
    req(parse_note(note) == note_expected(v), "note integer block")
    for phrase in ("PROVED_ABSTRACT", "COUNTEREXAMPLE_TO_HISTOGRAM_MOMENT_ONLY_INFERENCE", "OPEN_RS_PREFIX_REALIZABILITY", "This is not a Reed--Solomon counterexample.", "# OPEN GAP"):
        req(phrase in note, f"note boundary {phrase}")
    sums = parse_sums((ROOT/SUMS).read_text(encoding="utf-8"))
    req(set(sums) == set(HASHED), "checksum file set")
    for rel in HASHED:
        req((ROOT/rel).is_file() and sha(ROOT/rel) == sums[rel], f"checksum {rel}")

def check(heavy: bool=True) -> dict[str,int]:
    v = derive(load(), heavy)
    finish(v)
    return v

def must_fail(fn: Any, label: str) -> None:
    try: fn()
    except Fail: return
    raise Fail(f"tamper accepted: {label}")

def tamper() -> int:
    base, v = load(), check(True)
    cases = [
        (("instance","p"),2**31-2), (("instance","depth"),31),
        (("instance","total_supports"),str(v["N"]+1)), (("workboard","B_star"),v["B"]-1),
        (("moment_blind_pair","moment_order"),989), (("moment_blind_pair","step"),v["h"]+1),
        (("moment_blind_pair","offset"),v["x"]+1), (("moment_blind_pair","good_max"),v["B"]-1),
        (("moment_blind_pair","bad_max"),v["bad_max"]-1), (("moment_blind_pair","filler_low"),v["c"]+1),
        (("next_order_affine_binomial_boundary","minimizing_step"),v["h2"]+1),
        (("next_order_affine_binomial_boundary","minimum_block_mass_per_side"),str(v["T2"]-1)),
        (("nonclaims",),NONCLAIMS[:-1]),
    ]
    caught = 0
    for path, replacement in cases:
        d = copy.deepcopy(base); target: Any = d
        for key in path[:-1]: target = target[key]
        target[path[-1]] = replacement
        must_fail(lambda d=d: derive(d,False), str(path)); caught += 1
    for section in ("context_sources","steering_sources"):
        d=copy.deepcopy(base); d["provenance"][section][0]["gating"]=True
        must_fail(lambda d=d: derive(d,False), section); caught += 1
    text=(ROOT/NOTE).read_text(); altered=text.replace(f"bad_max={v['bad_max']}",f"bad_max={v['bad_max']-1}",1)
    must_fail(lambda: req(parse_note(altered)==note_expected(v),"note tamper"),"note"); caught += 1
    sums=parse_sums((ROOT/SUMS).read_text()); first=HASHED[0]; sums[first]="0"*64
    must_fail(lambda: req(sha(ROOT/first)==sums[first],"hash tamper"),"hash"); caught += 1
    coeff=[math.comb(v["m"],j)*(1 if j%2==0 else -1) for j in range(v["m"]+1)]; coeff[0]+=1
    must_fail(lambda: req(sum(coeff)==0,"coefficient tamper"),"moment coefficient"); caught += 1
    return caught

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--check",action="store_true"); g.add_argument("--tamper-selftest",action="store_true")
    args=parser.parse_args()
    global CHECKS; CHECKS=0
    try:
        if args.check:
            v=check(True); print(f"PASS: {CHECKS} checks; moments 0..{v['r']}; maxima {v['good_max']} / {v['bad_max']}")
        else:
            print(f"PASS: tamper self-test rejected {tamper()} mutations")
    except (Fail,OSError,json.JSONDecodeError,ValueError) as exc:
        print(f"FAIL: {exc}",file=sys.stderr); return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
