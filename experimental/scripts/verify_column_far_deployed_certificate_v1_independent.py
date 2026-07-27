#!/usr/bin/env python3
"""Independent replay of the deployed column-far certificate.

Deliberately shares no code with the primary verifier: the binomials are built
from an exact factorial ladder rather than math.comb, the row parameters are
re-derived from (p, extension degree, n, k, agreement) rather than read from the
certificate, and B* is recomputed from q = p^6 rather than quoted.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = (ROOT / "data/certificates/column-far-deployed-certificate-v1"
        / "column_far_deployed_certificate_v1.json")


def binom(n: int, k: int) -> int:
    """C(n,k) by an exact incremental ladder; no library binomials."""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    num = 1
    den = 1
    for i in range(k):
        num *= n - i
        den *= i + 1
    assert num % den == 0, "factorial ladder lost exactness"
    return num // den


def main() -> None:
    data = json.loads(CERT.read_text())
    row = data["koalabear_mca"]

    # re-derive the row from first principles
    p, deg = row["p"], row["extension_degree"]
    n, k, a = row["n"], row["k"], row["agreement"]
    q = p ** deg
    B = q >> 128
    assert B == row["B_star"], "B* mismatch: recomputed q//2^128 differs"

    R = n - k
    t = n - a
    assert (R, t) == (row["R"], row["r"]), "row parameters mismatch"

    vals = [binom(R + nu, nu + 1) // binom(R + nu - t - 1, nu) for nu in range(12)]
    assert vals == row["values"], "independent evaluation differs"

    paid = [nu for nu, v in enumerate(vals) if v <= B]
    assert paid == list(range(11)), f"paid set differs: {paid}"
    assert vals[11] > B

    # the crossing is strict and adjacent
    assert vals[10] <= B < vals[11]

    print(
        "COLUMN_FAR_DEPLOYED_CERTIFICATE_V1_INDEPENDENT_PASS "
        f"B*={B} nu10={vals[10]} nu11={vals[11]}"
    )


if __name__ == "__main__":
    main()
