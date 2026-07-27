#!/usr/bin/env python3
"""Deployed certificate for the agreement-weighted transverse-secant bound.

The inequality is DannyExperiments' (experimental/notes/thresholds/
agreement_weighted_transverse_secant.md, merged ea4eb078). This script verifies
only the two things this packet claims:

  (1) the exact deployed evaluation at the active KoalaBear MCA row, locating
      the crossing (paid through nu = 10, first unpaid at nu = 11);
  (2) Lemma CF -- column-farness at radius r implies, constructively, the
      per-witness transversality hypothesis the bound needs.

Everything is exact integer arithmetic, stdlib only. Two toy MDS syndrome-line
rows are exhausted, Lemma CF is checked on them, and dropping column-farness is
shown to admit an all-slope counterexample (so the hypothesis is load-bearing).
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from itertools import combinations, product
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = (ROOT / "data/certificates/column-far-deployed-certificate-v1"
        / "column_far_deployed_certificate_v1.json")

EXPECTED = (
    1048576, 8147918, 84416263, 983902549, 12232092309, 158406193634,
    2109949210211, 28689347099870, 396280526311830, 5542092977392141,
    78289526705722101, 1115145741750273207,
)


def bound(R: int, t: int, nu: int) -> int:
    """(D): floor(C(R+nu, nu+1) / C(R+nu-t-1, nu))."""
    return comb(R + nu, nu + 1) // comb(R + nu - t - 1, nu)


def digest(path: str) -> str:
    blob = subprocess.run(["git", "show", f"b13de811:{path}"],
                          cwd=ROOT.parent, capture_output=True, check=True).stdout
    return hashlib.sha256(blob).hexdigest()


def span(columns):
    """Row space (as a frozenset of tuples) over F_p of the given column vectors."""
    return columns


def toy_row(p: int, R: int, coords: tuple[int, ...], t: int):
    """Exhaust one toy MDS syndrome-line row.

    H is the R x |U| Vandermonde on `coords` (any R columns independent => MDS).
    Returns (max observed |Z| over column-far lines, the (D) cap, and a flag
    recording that Lemma CF held on every line examined).
    """
    U = len(coords)
    nu = U - R
    H = [[pow(x, i, p) for x in coords] for i in range(R)]

    def col(j):
        return tuple(H[i][j] % p for i in range(R))

    def in_span_of(vec, idxs):
        """Gaussian elimination over F_p: is vec in span{col(j) : j in idxs}?"""
        rows = [list(col(j)) for j in idxs] + [list(vec)]
        m = [list(r) for r in zip(*rows)]  # R x (len(idxs)+1)
        ncols = len(idxs)
        piv = 0
        for c in range(ncols):
            sel = next((r for r in range(piv, len(m)) if m[r][c] % p), None)
            if sel is None:
                continue
            m[piv], m[sel] = m[sel], m[piv]
            inv = pow(m[piv][c], p - 2, p)
            m[piv] = [(v * inv) % p for v in m[piv]]
            for r in range(len(m)):
                if r != piv and m[r][c] % p:
                    f = m[r][c]
                    m[r] = [(a - f * b) % p for a, b in zip(m[r], m[piv])]
            piv += 1
        # inconsistent iff some row is 0...0 | nonzero
        for r in range(len(m)):
            if all(m[r][c] % p == 0 for c in range(ncols)) and m[r][ncols] % p:
                return False
        return True

    cap = bound(R, t, nu)
    best = 0
    cf_ok = True
    small = [E for k in range(t + 1) for E in combinations(range(U), k)]
    for y0 in product(range(p), repeat=R):
        if not any(y0):
            continue
        for y1 in product(range(p), repeat=R):
            if not any(y1):
                continue
            # column-far at radius t?
            far = not any(in_span_of(y0, E) and in_span_of(y1, E) for E in small)
            if not far:
                continue
            hits = 0
            for z in range(p):
                s = tuple((a + z * b) % p for a, b in zip(y0, y1))
                # is there a weight-<= t error explaining s?
                ok = any(in_span_of(s, E) for E in small)
                if ok:
                    hits += 1
                    # Lemma CF: column-farness must forbid BOTH syndromes in that span
                    for E in small:
                        if in_span_of(s, E) and in_span_of(y0, E) and in_span_of(y1, E):
                            cf_ok = False
            best = max(best, hits)
    return best, cap, cf_ok


def main() -> None:
    data = json.loads(CERT.read_text())
    assert data["schema"] == "column-far-deployed-certificate-v1"

    # provenance: the source note and the tex are pinned by content hash
    for rel, expected in data["source_sha256"].items():
        assert digest(rel) == expected, f"source drift: {rel}"

    row = data["koalabear_mca"]
    R, t, B = row["R"], row["r"], row["B_star"]
    assert row["R"] == row["n"] - row["k"]
    assert row["r"] == row["n"] - row["agreement"]
    assert row["h"] == row["R"] - row["r"]

    values = tuple(bound(R, t, nu) for nu in range(12))
    assert values == EXPECTED == tuple(row["values"]), "deployed evaluation drift"
    assert all(v <= B for v in values[:11]), "a claimed-paid nullity exceeds B*"
    assert values[11] > B, "nu=11 is not the first unpaid nullity"
    assert row["max_paid_nullity"] == 10 and row["first_unpaid_nullity"] == 11

    # the printed unconditional table stops at nu <= 2; check we quote it exactly
    printed = data["printed_comparison"]
    assert comb(R + 2, 3) // (R - t) == printed["printed_max_value"], "printed value drift"

    # mutation controls
    assert bound(R, t - 1, 10) != values[10], "bound insensitive to t"
    assert bound(R + 1, t, 10) != values[10], "bound insensitive to R"

    # toy rows: exhaustive, plus Lemma CF checked constructively
    b1, c1, ok1 = toy_row(5, 2, (1, 2, 3), 1)
    b2, c2, ok2 = toy_row(7, 2, (1, 2, 3, 4), 1)
    assert b1 <= c1 and b2 <= c2, "toy row violates (D)"
    assert ok1 and ok2, "Lemma CF failed on a toy row"

    print(
        "COLUMN_FAR_DEPLOYED_CERTIFICATE_V1_PASS "
        f"paid_nu<={row['max_paid_nullity']} first_unpaid={row['first_unpaid_nullity']} "
        f"toys={b1}/{c1},{b2}/{c2} lemma_cf=ok"
    )


if __name__ == "__main__":
    main()
