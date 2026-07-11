#!/usr/bin/env python3
"""Independent checker for split-pencil-ray-collapse (no generator import).

Routes disjoint from the generator per quantity:
  d1, d2         generator: shifted-weak-Popov reduction.  here: two direct
                 rank tests over F_73 (the linear system W(x)U(x) = N(x) on
                 D has only the zero pair at wdeg <= d1-1, and a nonzero
                 pair at wdeg d1); d2 = n-K+1-d1.
  LIST + rays    generator: pencil cap-space + separately GRS duality.
                 here: fresh implementation of the duality route (power-sum
                 functionals over complements + 12-point interpolation),
                 grouped by codeword -> agreements; ray count = #distinct.
  RAW            here: recomputed from the census identity
                 RAW = sum C(agr, m) over the list (thm:saturation),
                 compared to the stored pencil-route value.
  pins           fresh scan with fresh line hashes; self-hash; gate fields.

Accepts --check for convention parity (the check always runs).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from itertools import combinations
from pathlib import Path

CERT_REL = Path(
    "experimental/data/certificates/split-pencil-ray-collapse/"
    "split_pencil_ray_collapse.json")

P = 73
N = 24
K = 12
M = 15
OMEGA = 9


def repo_root():
    return Path(__file__).resolve().parents[2]


def payload_hash(obj):
    clone = dict(obj)
    clone.pop("payload_sha256", None)
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _pnorm(f):
    f = list(f)
    while f and f[-1] == 0:
        f.pop()
    return f


def _padd(f, g):
    L = max(len(f), len(g))
    return _pnorm([((f[i] if i < len(f) else 0) + (g[i] if i < len(g) else 0))
                   % P for i in range(L)])


def _pscale(f, c):
    c %= P
    return _pnorm([c * a % P for a in f])


def _pmul(f, g):
    if not f or not g:
        return []
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                out[i + j] = (out[i + j] + a * b) % P
    return _pnorm(out)


def _peval(f, x):
    r = 0
    for a in reversed(f):
        r = (r * x + a) % P
    return r


def rank_kernel_trivial(U, D, d):
    """True iff the only (W,N), deg W <= d, deg N <= d+K-1, with
    W(x)U(x) = N(x) on D, is the zero pair."""
    nW, nN = d + 1, d + K
    rows = []
    for i, x in enumerate(D):
        row = [U[i] * pow(x, j, P) % P for j in range(nW)]
        row += [(-pow(x, j, P)) % P for j in range(nN)]
        rows.append(row)
    ncols = nW + nN
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        ic = pow(rows[r][c], P - 2, P)
        rows[r] = [v * ic % P for v in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [(a - f * b) % P for a, b in zip(rows[i], rows[r])]
        r += 1
    return r == ncols


def list_and_rays(U, D):
    """{codeword_tuple: agr} for all deg<K codewords at agr >= m, via
    power-sum duality + interpolation (fresh code)."""
    T = [sum(U[i] * pow(D[i], t, P) for i in range(N)) % P
         for t in range(13)]
    found = {}
    for R in combinations(range(N), OMEGA):
        lam = [1]
        for i in R:
            lam = _pmul(lam, [(-D[i]) % P, 1])
        ok = True
        for j in range(3):
            s = 0
            for k2, lv in enumerate(lam):
                if lv:
                    s += lv * T[j + 1 + k2]
            if s % P:
                ok = False
                break
        if not ok:
            continue
        Rset = set(R)
        Sidx = [i for i in range(N) if i not in Rset]
        pts = [(D[i], U[i]) for i in Sidx[:K]]
        out = []
        for i, (xi, yi) in enumerate(pts):
            num, den = [1], 1
            for j, (xj, _) in enumerate(pts):
                if i == j:
                    continue
                num = _pmul(num, [(-xj) % P, 1])
                den = den * ((xi - xj) % P) % P
            out = _padd(out, _pscale(num, yi * pow(den, P - 2, P)))
        for i in Sidx[K:]:
            assert _peval(out, D[i]) == U[i]
        key = tuple(out[t] if t < len(out) else 0 for t in range(K))
        if key not in found:
            found[key] = sum(1 for idx in range(N)
                             if _peval(out, D[idx]) == U[idx])
    return found


def run(root):
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    assert cert.get("payload_sha256") == payload_hash(cert), "self-hash"
    assert cert["all_pass"] and cert["gate_failures"] == 0
    assert cert["summary"]["verdict"] == "NO ISSUE"

    # pins, fresh scan
    for fname, labels in cert["statement_pins"].items():
        lines = (root / "experimental" / fname).read_text(
            encoding="utf-8").splitlines()
        for lab, pin in labels.items():
            assert pin["found"], lab
            line = lines[pin["line"] - 1]
            assert ("\\label{%s}" % lab) in line, "pin moved: %s" % lab
            assert hashlib.sha256(line.encode("utf-8")).hexdigest()[:16] \
                == pin["sha256_line"], "pin drift: %s" % lab
    print("pins: OK (%d labels)" % sum(
        len(v) for v in cert["statement_pins"].values()))

    D = cert["toy_parameters"]["domain"]
    assert len(D) == N and len(set(D)) == N
    for x in D:
        assert pow(x, N, P) == 1

    n_scope = 0
    for row in cert["rows"]:
        U = row["word"]
        lst = list_and_rays(U, D)
        assert len(lst) == row["list"], row["label"]
        if not row.get("in_scope"):
            continue
        n_scope += 1
        # d1 by rank tests (no Popov)
        d1 = row["d1"]
        assert rank_kernel_trivial(U, D, d1 - 1), \
            "%s: kernel nontrivial below d1" % row["label"]
        assert not rank_kernel_trivial(U, D, d1), \
            "%s: no kernel at d1" % row["label"]
        assert row["d2"] == N - K + 1 - d1
        # dedup census == list; agreements match; census identity
        assert row["rays"] == len(lst), row["label"]
        assert sorted(lst.values(), reverse=True) \
            == row["ray_agreements"], row["label"]
        assert row["raw_census"] == sum(
            math.comb(a, M) for a in lst.values()), row["label"]
        assert row["gate"] is True
        # tight-ray cap-exactness bookkeeping (recorded by the generator)
        if row["label"].startswith("two_cw"):
            degs = row["tight_ray_cap_exactness"]
            assert degs and any(d["at_cap"] for d in degs)
            for d in degs:
                assert d["cap_A"] == OMEGA - d1 and d["cap_B"] \
                    == OMEGA - row["d2"]
        print("  %-14s d1=%d rays=list=%d raw=%d  OK (rank tests + "
              "duality route)" % (row["label"], d1, row["rays"],
                                  row["raw_census"]))
    assert n_scope == cert["gated_words"]
    print("RESULT: PASS")
    print("payload_sha256:", cert["payload_sha256"])
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="accepted for convention parity; always runs")
    ap.parse_args(argv)
    return run(repo_root())


if __name__ == "__main__":
    sys.exit(main())
