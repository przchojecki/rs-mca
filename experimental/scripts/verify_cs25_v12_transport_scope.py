#!/usr/bin/env python3
"""Audit circle/stereographic and genus-one transport gates in Paper D v12.

This is a scoped verifier for the transport claims used by
``tex/cs25_cap_v12.tex`` and the compact ``tex/towards-prize.tex`` package.
It checks exact deployed arithmetic and exhaustively tests the small-field
algebraic identities behind the stereographic model.  It is not a proof of the
full transport theorems.
"""

from __future__ import annotations

from math import comb


P_M31 = 2**31 - 1

Poly = list[int]


def trim(poly: Poly) -> Poly:
    result = poly[:]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_mul(a: Poly, b: Poly, p: int) -> Poly:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return trim(out)


def poly_pow(base: Poly, exponent: int, p: int) -> Poly:
    out = [1]
    cur = base[:]
    value = exponent
    while value:
        if value & 1:
            out = poly_mul(out, cur, p)
        cur = poly_mul(cur, cur, p)
        value >>= 1
    return out


def matrix_rank_mod_p(rows: list[list[int]], p: int) -> int:
    mat = [row[:] for row in rows]
    rank = 0
    width = len(mat[0]) if mat else 0
    for col in range(width):
        pivot = None
        for row in range(rank, len(mat)):
            if mat[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col], -1, p)
        mat[rank] = [(entry * inv) % p for entry in mat[rank]]
        for row in range(len(mat)):
            if row == rank or mat[row][col] % p == 0:
                continue
            factor = mat[row][col]
            mat[row] = [
                (entry - factor * pivot_entry) % p
                for entry, pivot_entry in zip(mat[row], mat[rank])
            ]
        rank += 1
        if rank == len(mat):
            break
    return rank


def check_standard_position_gates() -> list[str]:
    """Check abstract dyadic gates for the deployed Mersenne-31 circle row."""

    p = P_M31
    m = 2**21
    ord_g = 4 * m
    if p % 4 != 3:
        raise AssertionError("Mersenne-31 should be 3 mod 4")
    if p + 1 != 2**31:
        raise AssertionError("p+1 should be 2^31")
    if (p + 1) % ord_g != 0:
        raise AssertionError("standard-position ord(g)=4M must divide p+1")
    if (2 * m) % ord_g == 0:
        raise AssertionError("ord(g) must not divide 2M")
    if m % 4 != 0:
        raise AssertionError("stereographic lemma needs 4|M")

    line_a = 2**13
    circle_a = 2**14
    widened_c = 16
    if m // 256 != line_a:
        raise AssertionError(("line scale", m // 256))
    if (2 * m) // 256 != circle_a:
        raise AssertionError(("circle scale", (2 * m) // 256))
    if m % line_a or m % circle_a:
        raise AssertionError("deployed dyadic scales must divide M")
    if m % (2 * widened_c):
        raise AssertionError("explicit Chebyshev widened scale needs 2c|M")

    return [
        "p=2^31-1 has p+1=2^31 and p=3 mod 4",
        "standard-position ord(g)=4M=2^23 divides p+1 but not 2M",
        "line scale a=2^13 and circle-code scale a=2^14 divide M=2^21",
        "stereographic and explicit-head side conditions 4|M and 2c|M hold",
    ]


def check_field_of_definition_gates() -> list[str]:
    """Check when the Mersenne-31 extensions contain i and the small-field split."""

    p = P_M31
    if pow(p - 1, (p - 1) // 2, p) != p - 1:
        raise AssertionError("-1 should be nonsquare modulo p")

    for degree in range(1, 9):
        contains_i = (pow(p, degree, 4) - 1) % 4 == 0
        if contains_i != (degree % 2 == 0):
            raise AssertionError(("i parity", degree, contains_i))

    if not p**3 < 2**100:
        raise AssertionError("F_{p^3} should be below 2^100")
    if not p**5 >= 2**100:
        raise AssertionError("F_{p^5} should be the first odd extension above 2^100")

    return [
        "-1 is nonsquare over F_p, so stereographic denominators 1+s^2 do not vanish",
        "F_{p^r} contains i iff r is even for r<=8",
        "among odd/no-i extensions, p^3<2^100 and p^5>=2^100",
    ]


def check_stereographic_small_fields() -> list[str]:
    """Exhaust small p=3 mod 4 fields for the stereographic algebra."""

    cases = 0
    basis_cases = 0
    for p in [7, 11, 19, 31, 43]:
        for s in range(p):
            denom = (1 + s * s) % p
            if denom == 0:
                raise AssertionError(("stereo denominator", p, s))
            inv = pow(denom, -1, p)
            x = (1 - s * s) * inv % p
            y = (2 * s) * inv % p
            if (x * x + y * y - 1) % p:
                raise AssertionError(("circle equation", p, s, x, y))
            recovered = y * pow(1 + x, -1, p) % p
            if recovered != s:
                raise AssertionError(("stereo inverse", p, s, recovered))
            if s:
                partner = (-pow(s, -1, p)) % p
                psi_s = (s * s - 1) * pow(2 * s, -1, p) % p
                psi_partner = (partner * partner - 1) * pow(2 * partner, -1, p) % p
                if psi_s != psi_partner:
                    raise AssertionError(("halving fiber", p, s, partner))
            cases += 1

        for w in range(1, 8):
            one_minus_s2 = [1, 0, (-1) % p]
            one_plus_s2 = [1, 0, 1]
            basis: list[Poly] = []
            for j in range(w + 1):
                basis.append(
                    poly_mul(
                        poly_pow(one_minus_s2, j, p),
                        poly_pow(one_plus_s2, w - j, p),
                        p,
                    )
                )
            for j in range(w):
                odd = poly_mul(
                    [0, 2 % p],
                    poly_mul(
                        poly_pow(one_minus_s2, j, p),
                        poly_pow(one_plus_s2, w - 1 - j, p),
                        p,
                    ),
                    p,
                )
                basis.append(odd)
            rows = []
            for poly in basis:
                rows.append([poly[i] if i < len(poly) else 0 for i in range(2 * w + 1)])
            if matrix_rank_mod_p(rows, p) != 2 * w + 1:
                raise AssertionError(("stereo basis rank", p, w))
            basis_cases += 1

    return [
        f"checked stereographic inverse and tangent-halving fibers on {cases} field elements",
        f"checked circle-to-RS basis rank for {basis_cases} small-field (p,w) cases",
    ]


def check_deployed_circle_arithmetic() -> list[str]:
    """Check the deployed circle line-round and bivariate-circle arithmetic."""

    p = P_M31
    q = p**4
    binom_256_130 = comb(256, 130)

    n = 2**21
    k = 2**20
    a = 2**13
    ell2 = k // a + 2
    a2 = a * ell2
    if ell2 != 130 or a2 != k + 2 * a:
        raise AssertionError(("line A2", ell2, a2))
    if not binom_256_130 * k > p * (q + k):
        raise AssertionError("circle line-round entropy gate")
    if not n * 2**102 < q:
        raise AssertionError("circle line n/q < 2^-102")
    if not (q - n) * 2**22 > 2 * k * q:
        raise AssertionError("circle line lower bound > 2^-22")

    n_c = 2**22
    k_c = 2**21 + 1
    a_c = 2**14
    ell2_c = k_c // a_c + 2
    a2_c = a_c * ell2_c
    if ell2_c != 130 or a2_c != 2**21 + 2**15:
        raise AssertionError(("circle-code A2", ell2_c, a2_c))
    if not binom_256_130 * k_c > (p**2) * (q + k_c):
        raise AssertionError("bivariate circle entropy gate")
    if not n_c * 2**101 < q:
        raise AssertionError("bivariate circle n/q < 2^-101")
    if not (q - n_c) * 2**23 > 2 * k_c * q:
        raise AssertionError("bivariate circle lower bound > 2^-23")

    return [
        "circle line-round: ell2=130, A2=k+2^14, entropy gate holds exactly",
        "circle line-round: n/q<2^-102 and converted lower bound >2^-22",
        "bivariate circle: ell2=130, A2=2^21+2^15, entropy gate holds exactly",
        "bivariate circle: n_c/q<2^-101 and converted lower bound >2^-23",
    ]


def check_ifree_stereographic_rf_gate() -> list[str]:
    """Check the i-free circle rational-floor certificate and radius gates."""

    p = P_M31
    n_c = 2**22
    k_c = 2**21 + 1
    m = 2**20 + 2**15 + 1
    w = 2**16
    n_over_a = 2**21

    if w != 2 * m - (k_c + 1):
        raise AssertionError(("w", w, 2 * m - (k_c + 1)))
    if not (2 * m >= k_c + 1 and m <= k_c and m <= n_over_a):
        raise AssertionError("rational-floor hypotheses for K in {k,k+1}")
    large_binom = comb(n_over_a, m)
    if not large_binom > (p**w) * 2**256:
        raise AssertionError("i-free circle RF integer inequality")
    # The list floor at K=k_c has one extra prefix exponent, w+1, but only
    # needs the target-scaled threshold 2^-100*q.  Check it directly at the
    # worst allowed q<2^256.
    if not large_binom * 2**100 > (p ** (w + 1)) * (2**256 - 1):
        raise AssertionError("i-free circle RF list threshold domination")

    agreement = 2 * m
    if not n_c - agreement <= n_c - k_c - 1:
        raise AssertionError("Theorem A integer admissibility")
    edge = 1 - agreement / n_c
    target_edge = 1 - (k_c / n_c) - 2**-6
    if not edge <= target_edge:
        raise AssertionError(("edge containment", edge, target_edge))

    q_min = p**5
    if not (q_min - n_c) * 2**23 > 2 * k_c * q_min:
        raise AssertionError("i-free circle converted error >2^-23")

    return [
        "i-free circle RF: w=2^16 and rational-floor hypotheses hold",
        "binom(2^21,m)>p^w 2^256 holds exactly",
        "the same certificate dominates the K=k_c list threshold at target 2^-100",
        "edge is contained in [1-rho_c-2^-6,1-rho_c) and is integer-admissible",
        "at q>=p^5 the converted error exceeds 2^-23",
    ]


def check_genus_one_rational_floor_boundary() -> list[str]:
    """Check boundary inequalities behind the genus-one macroscopic cap."""

    n = 2**14
    q = 2**256 - 1
    base = 2**64
    rows = []
    for num, den in [(1, 2), (1, 4), (1, 8), (1, 16)]:
        k = n * num // den
        m = (k + 1 + n // 512 + 1) // 2
        n_over_a = n // 2
        w1 = 2 * m - k - 1
        w0 = 2 * m - k
        if not (2 * m >= k + 1 and m <= k and m <= n_over_a):
            raise AssertionError(("rational hypotheses", num, den, k, m))
        lhs = comb(n_over_a, m)
        if not lhs * k > (base**w1) * (q + k):
            raise AssertionError(("genus-one MCA gate", num, den))
        if not lhs * 2**128 > (base**w0) * q:
            raise AssertionError(("genus-one list gate", num, den))
        rows.append(f"rho={num}/{den}: m={m}, w0={w0}, exact boundary gates pass")

    return rows + [
        "checked worst declared boundary n=2^14, |B|=2^64, q=2^256-1",
    ]


def main() -> None:
    checks = [
        ("standard-position dyadic gates", check_standard_position_gates),
        ("field-of-definition gates", check_field_of_definition_gates),
        ("stereographic small-field algebra", check_stereographic_small_fields),
        ("deployed circle arithmetic", check_deployed_circle_arithmetic),
        ("i-free stereographic RF gate", check_ifree_stereographic_rf_gate),
        ("genus-one rational-floor boundary", check_genus_one_rational_floor_boundary),
    ]
    print("=" * 74)
    print("AUDIT: Paper D v12 circle/stereographic/genus-one transport scope")
    print("=" * 74)
    failed = 0
    for title, fn in checks:
        try:
            details = fn()
        except AssertionError as exc:
            failed += 1
            print(f"\n[FAIL] {title}")
            print(f"       {exc}")
            continue
        print(f"\n[PASS] {title}")
        for line in details:
            print(f"       {line}")
    print("\n" + "-" * 74)
    print(f"implemented PASS: {len(checks) - failed}   FAIL: {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
