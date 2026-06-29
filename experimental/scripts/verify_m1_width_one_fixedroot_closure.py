#!/usr/bin/env python3
"""Verify the M1 width-one fixed-root algebra in small fields.

This checks the bounded-complement tail recursion and the first residual gate
from experimental/notes/m1/m1_width_one_fixedroot_closure.md.  The gate is the
first product coefficient not forced by the tail readout.
"""

from __future__ import annotations

from itertools import combinations, product
from random import Random


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return out


def locator(roots: list[int], p: int) -> list[int]:
    poly = [1]
    for root in roots:
        poly = poly_mul(poly, [(-root) % p, 1], p)
    return poly


def elementary(roots: list[int], max_degree: int, p: int) -> list[int]:
    values = [1] + [0] * max_degree
    for root in roots:
        for degree in range(max_degree, 0, -1):
            values[degree] = (values[degree] + root * values[degree - 1]) % p
    return values


def high_coefficients(monic_poly: list[int], degree: int, count: int, p: int) -> list[int]:
    assert len(monic_poly) == degree + 1
    assert monic_poly[degree] % p == 1
    return [monic_poly[degree - i] % p for i in range(1, count + 1)]


def tail_recursion(e_d: list[int], u_values: list[int], s: int, p: int) -> list[int]:
    o_values = [1] + [0] * (s + 1)
    for i in range(1, s + 2):
        correction = sum(u_values[j] * o_values[i - j] for j in range(1, i + 1))
        o_values[i] = (e_d[i] - correction) % p
    return o_values


def complement_from_o(o_values: list[int], s: int, p: int) -> list[int]:
    poly = [0] * (s + 2)
    for i in range(s + 2):
        poly[s + 1 - i] = ((-1) ** i * o_values[i]) % p
    return poly


def first_gate(e_d: list[int], u_values: list[int], o_values: list[int], s: int, p: int) -> int:
    rhs = u_values[s + 2]
    rhs += sum(u_values[j] * o_values[s + 2 - j] for j in range(1, s + 2))
    return (e_d[s + 2] - rhs) % p


def check_tail_recovers_complement() -> None:
    for p in (7, 11, 17, 23):
        for s in range(0, 4):
            for q in range(s + 3, min(p - s, s + 8)):
                domain = list(range(q + s))
                e_d = elementary(domain, s + 2, p)
                for complement in combinations(domain, s + 1):
                    complement_list = list(complement)
                    z_roots = [root for root in domain if root not in complement]
                    ell_z = locator(z_roots, p)
                    coeffs = high_coefficients(ell_z, q - 1, s + 2, p)
                    u_values = [1]
                    u_values.extend(((-1) ** i * coeffs[i - 1]) % p for i in range(1, s + 3))
                    o_values = tail_recursion(e_d, u_values, s, p)

                    expected_o = elementary(complement_list, s + 1, p)
                    assert o_values == expected_o, (
                        p,
                        s,
                        q,
                        complement,
                        o_values,
                        expected_o,
                    )

                    ell_o = complement_from_o(o_values, s, p)
                    assert ell_o == locator(complement_list, p), (
                        p,
                        s,
                        q,
                        complement,
                        ell_o,
                        locator(complement_list, p),
                    )
                    assert first_gate(e_d, u_values, o_values, s, p) == 0, (
                        p,
                        s,
                        q,
                        complement,
                    )


def check_first_gate_is_residual_coefficient() -> None:
    rng = Random(20260707)
    for p in (7, 11, 17, 23):
        for s in range(0, 4):
            for q in range(s + 3, min(p - s, s + 7)):
                domain = list(range(q + s))
                ell_d = locator(domain, p)
                e_d = elementary(domain, s + 2, p)
                for _ in range(200):
                    # Random monic degree-(q-1) candidate L.  It need not split.
                    ell_l = [rng.randrange(p) for _ in range(q - 1)] + [1]
                    coeffs = high_coefficients(ell_l, q - 1, s + 2, p)
                    u_values = [1]
                    u_values.extend(((-1) ** i * coeffs[i - 1]) % p for i in range(1, s + 3))
                    o_values = tail_recursion(e_d, u_values, s, p)
                    ell_o = complement_from_o(o_values, s, p)
                    residual = [
                        (a - b) % p
                        for a, b in zip(ell_d, poly_mul(ell_o, ell_l, p))
                    ]

                    # Degree q-2 is the first coefficient after the leading
                    # term and next s+1 tail-controlled coefficients.
                    residual_coeff = residual[q - 2] % p
                    signed_gate = (((-1) ** (s + 2)) * first_gate(e_d, u_values, o_values, s, p)) % p
                    assert residual_coeff == signed_gate, (
                        p,
                        s,
                        q,
                        ell_l,
                        residual_coeff,
                        signed_gate,
                    )


def check_gate_degree_bound() -> None:
    # Interpolate the first gate along random monic affine pencils and verify
    # that finite differences of order s+3 vanish, as degree <= s+2 predicts.
    rng = Random(20260708)
    for p in (11, 17, 23):
        for s in range(0, 4):
            for q in range(s + 3, min(p - s, s + 7)):
                domain = list(range(q + s))
                e_d = elementary(domain, s + 2, p)
                m_poly = [rng.randrange(p) for _ in range(q - 1)] + [1]
                n_poly = [rng.randrange(p) for _ in range(q - 1)] + [0]

                values: list[int] = []
                for lam in range(p):
                    ell_l = [(m_poly[i] + lam * n_poly[i]) % p for i in range(q)]
                    coeffs = high_coefficients(ell_l, q - 1, s + 2, p)
                    u_values = [1]
                    u_values.extend(((-1) ** i * coeffs[i - 1]) % p for i in range(1, s + 3))
                    o_values = tail_recursion(e_d, u_values, s, p)
                    values.append(first_gate(e_d, u_values, o_values, s, p))

                differences = values
                for _ in range(s + 3):
                    differences = [
                        (differences[i + 1] - differences[i]) % p
                        for i in range(len(differences) - 1)
                    ]
                assert all(value == 0 for value in differences), (
                    p,
                    s,
                    q,
                    values,
                    differences,
                )


def main() -> None:
    check_tail_recovers_complement()
    check_first_gate_is_residual_coefficient()
    check_gate_degree_bound()
    print("M1 width-one fixed-root verifier passed")


if __name__ == "__main__":
    main()
