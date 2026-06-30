#!/usr/bin/env python3
"""Step 5 (towards-prize.md S1): carve the SOLVED high-agreement region of the
prize envelope using the row-independent high-agreement compiler.

THE COMPILER (promoted tangent theorem + the 2^-128 gate).
For C = RS[F, L, k] with n = |L|, line/challenge field size q = q_line, write
    B_Q = floor(q / 2^128),     r = n - a   (redundancy at agreement a).
The tangent staircase gives the EXACT value
    LD_sw(C, a) = n - a + 1 = r + 1     whenever   r = n - a <= floor((n-k)/3),
and the target gate is:  emca(C, delta) > 2^-128  <=>  LD_sw(C, a) >= B_Q + 1.
Hence IF
    1 <= B_Q <= floor((n-k)/3),
then the single line / MCA / CA grid threshold is pinned EXACTLY:
    r <= B_Q - 1  is SAFE,     r = B_Q  is UNSAFE,
equivalently  agreement a >= n - B_Q + 1 is safe, a = n - B_Q is the first unsafe.
Rows meeting this hypothesis are the SOLVED high-agreement region of the envelope.

This script computes the carving (solved vs not, and the exact pinned threshold)
across the four prize rates rho in {1/2, 1/4, 1/8, 1/16}, anchors it on the
flagship F_17^32 row, and pins the exact boundary of the solved region.

HONEST SCOPE.
The solved region is the HIGH-AGREEMENT regime: the pinned threshold sits at
radius ~ B_Q / n, which is tiny (6/512 ~ 0.012 for the flagship) and FAR below the
Johnson radius 1 - sqrt(rho).  This carves the EASY slice of the prize envelope; it
does NOT resolve the prize-determining near-capacity content.  No claim is made
beyond the promoted tangent theorem's exact-equality range r <= floor((n-k)/3).

Run:  python3 experimental/scripts/verify_step5_envelope_carving.py
Exit non-zero iff any implemented check fails.
"""
from __future__ import annotations

import json
import math  # decimal radii are display-only; PASS assertions use exact integers
from pathlib import Path

TWO128 = 2 ** 128
RATES = [(1, 2), (1, 4), (1, 8), (1, 16)]   # the four grand-challenge rates


def solved_region(rho, n, q):
    """Carving verdict for C = RS[F, L, k], n = |L|, line field size q.
    rho = (num, den) with k = rho * n (must be an integer)."""
    num, den = rho
    if (n * num) % den != 0:
        raise ValueError(f"k = {num}/{den} * {n} is not an integer")
    k = n * num // den
    nk = n - k
    cap = nk // 3                       # floor((n-k)/3)
    b_q = q // TWO128                   # floor(q / 2^128)
    applies = (1 <= b_q <= cap)
    res = {"n": n, "k": k, "nk": nk, "cap": cap, "B_Q": b_q, "solved": applies}
    if applies:
        res["threshold_r"] = b_q                 # r = B_Q unsafe, r <= B_Q-1 safe
        res["safe_min_agreement"] = n - b_q + 1  # a >= this is safe
        res["first_unsafe_agreement"] = n - b_q  # a = n - B_Q is unsafe
    return res


def check_flagship_anchor():
    """The flagship F_17^32 row lands in the solved region and the compiler pins it
    to the value already on the board (a=506 unsafe, a=507 safe)."""
    d = []
    ok = True
    q = 17 ** 32
    r = solved_region((1, 2), 512, q)
    d.append(f"B_Q = floor(17^32/2^128) = {r['B_Q']} ; cap = floor((n-k)/3) = {r['cap']}")
    d.append(f"solved (1 <= B_Q <= cap) : {r['solved']}")
    ok &= r["solved"] and (r["B_Q"] == 6) and (r["cap"] == 85)
    d.append(f"pinned threshold: a >= {r.get('safe_min_agreement')} safe, "
             f"a = {r.get('first_unsafe_agreement')} unsafe")
    ok &= (r.get("safe_min_agreement") == 507) and (r.get("first_unsafe_agreement") == 506)
    # cross-check against the on-main board record (tangent506-exact-gate)
    d.append("matches board tangent506-exact-gate (506 unsafe / 507 safe) : "
             f"{r.get('first_unsafe_agreement') == 506 and r.get('safe_min_agreement') == 507}")
    return ok, d


def check_solved_region_boundary():
    """The solved region is EXACTLY B_Q <= floor((n-k)/3): at n=512, rho=1/2 (cap=85),
    B_Q=85 is solved, B_Q=86 exits the region; B_Q=0 (q<=2^128) does not apply."""
    d = []
    ok = True
    n = 512
    cap = (512 - 256) // 3
    inside = solved_region((1, 2), n, 85 * TWO128 + 1)     # B_Q = 85 = cap
    outside = solved_region((1, 2), n, 86 * TWO128)        # B_Q = 86 > cap
    degenerate = solved_region((1, 2), n, TWO128 - 1)      # B_Q = 0 -> compiler n/a
    d.append(f"cap = floor((n-k)/3) = {cap}")
    d.append(f"B_Q = {cap} (= cap)  solved : {inside['solved']}")
    d.append(f"B_Q = {cap + 1} (> cap)  solved : {outside['solved']} (expect False)")
    d.append(f"B_Q = 0 (q <= 2^128)  solved : {degenerate['solved']} (expect False; compiler n/a)")
    ok &= inside["solved"] and (not outside["solved"]) and (not degenerate["solved"])
    return ok, d


def check_multi_rate_grid():
    """Carve the envelope across all four grand-challenge rates rho in {1/2,1/4,1/8,1/16}.
    At fixed q the threshold is fixed by B_Q, while the cap floor((n-k)/3) GROWS as the
    rate drops -- so lower-rate rows are solved with more room.  Also a large-n row."""
    d = []
    ok = True
    n, q = 512, 17 ** 32
    b_q = q // TWO128
    expected_cap = {(1, 2): 85, (1, 4): 128, (1, 8): 149, (1, 16): 160}
    d.append(f"at n={n}, q=17^32 (B_Q={b_q}):")
    for rho in RATES:
        r = solved_region(rho, n, q)
        b_in = solved_region(rho, n, r["cap"] * TWO128 + 1)["solved"]      # B_Q = cap
        b_out = solved_region(rho, n, (r["cap"] + 1) * TWO128)["solved"]   # B_Q = cap+1
        row_ok = (r["cap"] == expected_cap[rho] and r["solved"]
                  and r.get("safe_min_agreement") == 507
                  and r.get("first_unsafe_agreement") == 506
                  and b_in and not b_out)
        ok &= row_ok
        d.append(f"  rho={rho[0]}/{rho[1]}: k={r['k']}, n-k={r['nk']}, cap={r['cap']}; "
                 f"solved={r['solved']}, safe a>={r.get('safe_min_agreement')}; "
                 f"boundary[in={b_in},out={not b_out}] : {row_ok}")
    # n-scaling: a large row stays solved at this q, pinned at a = n - B_Q + 1
    big = solved_region((1, 2), 2 ** 20, q)
    big_ok = big["solved"] and big.get("safe_min_agreement") == 2 ** 20 - b_q + 1
    d.append(f"  large row n=2^20, rho=1/2, q=17^32: solved={big['solved']}, "
             f"safe a>={big.get('safe_min_agreement')} (= n-B_Q+1) : {big_ok}")
    ok &= big_ok
    return ok, d


def check_high_agreement_scope():
    """HONEST SCOPE: the pinned transition radius ~ B_Q/n sits far BELOW the Johnson
    radius 1 - sqrt(rho).  Exact test (no floats in the assertion):
        B_Q/n < 1 - sqrt(k/n)   <=>   k*n < (n - B_Q)^2.
    So the carved region is the EASY high-agreement slice, not near-capacity content."""
    d = []
    ok = True
    n, q = 512, 17 ** 32
    b_q = q // TWO128
    for rho in RATES:
        k = solved_region(rho, n, q)["k"]
        below = (k * n < (n - b_q) ** 2)            # exact integer form of pinned < Johnson
        pinned = b_q / n                            # display only
        johnson = 1 - math.sqrt(k / n)              # display only
        d.append(f"  rho={rho[0]}/{rho[1]}: pinned B_Q/n={pinned:.4f}, "
                 f"Johnson 1-sqrt(rho)={johnson:.4f}; pinned << Johnson "
                 f"(k*n={k * n} < (n-B_Q)^2={(n - b_q) ** 2}) : {below}")
        ok &= below
    d.append("=> the solved region is HIGH-AGREEMENT (radius ~B_Q/n), far below Johnson; "
             "it carves the EASY slice, NOT the near-capacity prize content.")
    return ok, d


def _rho_str(rho):
    return f"{rho[0]}/{rho[1]}"


def _parse_rho(s):
    a, b = s.split("/")
    return (int(a), int(b))


def _envelope_rows():
    """Canonical, deterministic set of rows for the envelope map."""
    q = 17 ** 32
    rows = [(rho, 512, q, "17^32") for rho in RATES]
    rows.append(((1, 2), 2 ** 20, q, "17^32"))                       # large row
    rows.append(((1, 2), 512, 85 * TWO128 + 1, "85*2^128+1 (B_Q=cap=85)"))   # boundary in
    rows.append(((1, 2), 512, 86 * TWO128, "86*2^128 (B_Q=86>cap)"))          # boundary out
    return rows


def _map_path():
    root = Path(__file__).resolve().parents[2]
    return root / "experimental" / "data" / "step5-envelope-map" / "envelope_map.json"


def check_emit_envelope_map():
    """Emit a deterministic JSON map of the carved rows, then re-read it and recompute
    every row via solved_region to confirm the artifact agrees with the compiler."""
    d = []
    ok = True
    rows = []
    for rho, n, q, label in _envelope_rows():
        r = solved_region(rho, n, q)
        rows.append({
            "rho": _rho_str(rho), "n": n, "q": str(q), "q_label": label,
            "k": r["k"], "nk": r["nk"], "cap": r["cap"], "B_Q": r["B_Q"],
            "solved": r["solved"],
            "safe_min_agreement": r.get("safe_min_agreement"),
            "first_unsafe_agreement": r.get("first_unsafe_agreement"),
        })
    payload = {
        "convention": ("C=RS[F,L,k], n=|L|, q=q_line; B_Q=floor(q/2^128); "
                       "solved iff 1<=B_Q<=floor((n-k)/3); then threshold pinned at r=B_Q, "
                       "safe iff agreement a>=n-B_Q+1"),
        "rows": rows,
    }
    path = _map_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")
    with open(path) as f:
        back = json.load(f)
    consistent = True
    for row in back["rows"]:
        rr = solved_region(_parse_rho(row["rho"]), row["n"], int(row["q"]))
        if (rr["solved"] != row["solved"] or rr["cap"] != row["cap"]
                or rr["B_Q"] != row["B_Q"]
                or rr.get("safe_min_agreement") != row["safe_min_agreement"]):
            consistent = False
    n_solved = sum(1 for r in rows if r["solved"])
    d.append("emitted -> experimental/data/step5-envelope-map/envelope_map.json")
    d.append(f"re-read JSON and recomputed every row via solved_region : {consistent}")
    d.append(f"solved rows: {n_solved}/{len(rows)} (expect 6/7)")
    ok &= consistent and (n_solved == 6) and (len(rows) == 7)
    return ok, d


def _pending():
    return None, ["PENDING -- added in a later loop iteration"]


CHECKS = [
    ("compiler formula / flagship anchor", check_flagship_anchor),
    ("solved-region boundary",             check_solved_region_boundary),
    ("multi-rate envelope grid",           check_multi_rate_grid),
    ("high-agreement scope vs Johnson",    check_high_agreement_scope),
    ("emit envelope map artifact",         check_emit_envelope_map),
]


def main():
    print("=" * 74)
    print("Step 5: carve the SOLVED high-agreement region of the prize envelope")
    print("compiler: 1 <= B_Q=floor(q/2^128) <= floor((n-k)/3)  =>  threshold pinned at r=B_Q")
    print("=" * 74)
    failed = done = pending = 0
    for title, fn in CHECKS:
        status, details = fn()
        tag = "PENDING" if status is None else ("PASS" if status else "FAIL")
        if status is None:
            pending += 1
        elif status:
            done += 1
        else:
            failed += 1
        print(f"\n[{tag:7}] {title}")
        for line in details:
            print(f"          {line}")
    print("\n" + "-" * 74)
    print(f"implemented PASS: {done}   FAIL: {failed}   PENDING: {pending}")
    print("-" * 74)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
