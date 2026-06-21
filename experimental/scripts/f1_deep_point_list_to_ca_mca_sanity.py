#!/usr/bin/env python3
r"""
Small check for experimental/notes/f1/f1_deep_point_list_to_ca_mca.md.

The note proves an exact simple-pole image identity:

    Bad_CA(f_alpha,g_alpha; delta_a)
      = Bad_MCA(f_alpha,g_alpha; delta_a)
      = Deep_alpha(U,a).

This script checks the identity in one small extension-field example. It is not
a deployed-parameter computation.

Toy field:
    B = F_17
    F = F_17[t]/(t^2 - 3), where 3 is nonsquare modulo 17.
    D = F_17^*.

Toy code:
    n = 16, k = 8, N = 8, a0 = 2, rho = 1/2, ell = rho*N + 2 = 6.

The test builds a slack-two quotient-locator word

    U_z(X) = X^(k+2a0) + z X^(k+a0)

and chooses a heavy quotient-locator fiber. Then, for alpha=t \in F \setminus B, it checks:

1. the full RS[F,D,k+1] list around U_z at agreement k+2a0;
2. the deep image {P(alpha)} of that full list;
3. the exact set of slopes z for which f_alpha + z g_alpha is RS[F,D,k]-close
   on some agreement-12 support;
4. the global CA far condition: g_alpha has no degree-<k explanation on any
   support of size > k.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from typing import Dict, Iterable, List, Sequence, Tuple

P = 17
NON_SQUARE = 3  # t^2 = 3 over F_17; 3 is nonsquare modulo 17.


class Fp2:
    __slots__ = ("a", "b")

    def __init__(self, a: int = 0, b: int = 0):
        self.a = a % P
        self.b = b % P

    def __add__(self, other: object) -> "Fp2":
        other = to_fp2(other)
        return Fp2(self.a + other.a, self.b + other.b)

    def __radd__(self, other: object) -> "Fp2":
        return self + other

    def __sub__(self, other: object) -> "Fp2":
        other = to_fp2(other)
        return Fp2(self.a - other.a, self.b - other.b)

    def __rsub__(self, other: object) -> "Fp2":
        return to_fp2(other) - self

    def __neg__(self) -> "Fp2":
        return Fp2(-self.a, -self.b)

    def __mul__(self, other: object) -> "Fp2":
        other = to_fp2(other)
        return Fp2(
            self.a * other.a + NON_SQUARE * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    def __rmul__(self, other: object) -> "Fp2":
        return self * other

    def inv(self) -> "Fp2":
        den = (self.a * self.a - NON_SQUARE * self.b * self.b) % P
        if den == 0:
            raise ZeroDivisionError(repr(self))
        inv_den = pow(den, -1, P)
        return Fp2(self.a * inv_den, -self.b * inv_den)

    def __truediv__(self, other: object) -> "Fp2":
        return self * to_fp2(other).inv()

    def __rtruediv__(self, other: object) -> "Fp2":
        return to_fp2(other) * self.inv()

    def __pow__(self, e: int) -> "Fp2":
        if e < 0:
            return (self.inv()) ** (-e)
        out = Fp2(1, 0)
        base = self
        while e:
            if e & 1:
                out = out * base
            base = base * base
            e >>= 1
        return out

    def __eq__(self, other: object) -> bool:
        try:
            other = to_fp2(other)
        except TypeError:
            return False
        return self.a == other.a and self.b == other.b

    def __hash__(self) -> int:
        return hash((self.a, self.b))

    def __repr__(self) -> str:
        if self.b == 0:
            return str(self.a)
        if self.a == 0:
            return f"{self.b}t"
        return f"{self.a}+{self.b}t"


def to_fp2(x: object) -> Fp2:
    if isinstance(x, Fp2):
        return x
    if isinstance(x, int):
        return Fp2(x, 0)
    raise TypeError(f"cannot coerce {type(x)!r} to Fp2")


ZERO = Fp2(0, 0)
ONE = Fp2(1, 0)
T = Fp2(0, 1)
Poly = List[Fp2]


def base(x: int) -> Fp2:
    return Fp2(x, 0)


def poly_trim(c: Sequence[Fp2]) -> Poly:
    out = list(c)
    while out and out[-1] == ZERO:
        out.pop()
    return out


def poly_key(c: Sequence[Fp2]) -> Tuple[Fp2, ...]:
    return tuple(poly_trim(c))


def poly_add(a: Sequence[Fp2], b: Sequence[Fp2]) -> Poly:
    m = max(len(a), len(b))
    out = [ZERO for _ in range(m)]
    for i in range(m):
        out[i] = (a[i] if i < len(a) else ZERO) + (b[i] if i < len(b) else ZERO)
    return poly_trim(out)


def poly_neg(a: Sequence[Fp2]) -> Poly:
    return [-x for x in a]


def poly_sub(a: Sequence[Fp2], b: Sequence[Fp2]) -> Poly:
    return poly_add(a, poly_neg(b))


def poly_mul(a: Sequence[Fp2], b: Sequence[Fp2]) -> Poly:
    if not a or not b:
        return []
    out = [ZERO for _ in range(len(a) + len(b) - 1)]
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = out[i + j] + ai * bj
    return poly_trim(out)


def poly_eval(c: Sequence[Fp2], x: Fp2) -> Fp2:
    out = ZERO
    for coeff in reversed(c):
        out = out * x + coeff
    return out


def monomial(deg: int, coeff: Fp2 = ONE) -> Poly:
    out = [ZERO for _ in range(deg + 1)]
    out[deg] = coeff
    return out


def degree(c: Sequence[Fp2]) -> int:
    return len(poly_trim(c)) - 1


def interpolate(points: Sequence[Tuple[Fp2, Fp2]]) -> Poly:
    """Return the unique polynomial of degree < len(points) through the points."""
    result: Poly = []
    for i, (xi, yi) in enumerate(points):
        basis: Poly = [ONE]
        denom = ONE
        for j, (xj, _yj) in enumerate(points):
            if i == j:
                continue
            basis = poly_mul(basis, [-xj, ONE])
            denom = denom * (xi - xj)
        scale = yi / denom
        result = poly_add(result, [scale * coeff for coeff in basis])
    return poly_trim(result)


def subgroup_full_base() -> List[Fp2]:
    """Return F_17^* as base-field elements, using 3 as a generator."""
    gen = 3
    vals: List[Fp2] = []
    x = 1
    for _ in range(16):
        vals.append(base(x))
        x = (x * gen) % P
    assert len(set(vals)) == 16
    return vals


def elementary_sum(values: Iterable[Fp2]) -> Fp2:
    out = ZERO
    for value in values:
        out = out + value
    return out


def coeff(c: Sequence[Fp2], i: int) -> Fp2:
    return c[i] if i < len(c) else ZERO


def support_close_slope(
    f_interp: Sequence[Fp2],
    g_interp: Sequence[Fp2],
    k: int,
    support_size: int,
) -> Fp2 | None:
    """
    Find the unique z, if any, for which f_interp + z*g_interp has degree < k.

    Here f_interp and g_interp are the interpolants on one support of size
    support_size. The high coefficients k,...,support_size-1 must vanish.
    """
    candidate: Fp2 | None = None
    for j in range(k, support_size):
        fj = coeff(f_interp, j)
        gj = coeff(g_interp, j)
        if gj == ZERO:
            if fj != ZERO:
                return None
            continue
        z_j = -fj / gj
        if candidate is None:
            candidate = z_j
        elif candidate != z_j:
            return None
    return candidate


def main() -> None:
    n = 16
    k = 8
    N = 8
    a0 = n // N
    ell = k // a0 + 2
    agreement = k + 2 * a0

    assert a0 == 2
    assert ell == 6
    assert agreement == 12

    D = subgroup_full_base()
    Q = sorted({x ** a0 for x in D}, key=lambda z: z.a)
    assert len(Q) == N

    fibers: Dict[Fp2, List[List[Fp2]]] = defaultdict(list)
    for A_tuple in combinations(Q, ell):
        A = list(A_tuple)
        z_A = -elementary_sum(A)
        fibers[z_A].append(A)

    z0, As = max(fibers.items(), key=lambda kv: len(kv[1]))
    U_poly = poly_add(monomial(k + 2 * a0), monomial(k + a0, z0))

    print(f"toy field: F_17[t]/(t^2-{NON_SQUARE})")
    print(f"n={n}, k={k}, agreement={agreement}, radius=1-{agreement}/{n}")
    print(f"Q size={len(Q)}, ell={ell}")
    print(f"largest quotient-locator slope fiber z0={z0}, size={len(As)}")

    # Verify the quotient-locator sublist identities.
    quotient_sublist = set()
    for A in As:
        LA: Poly = [ONE]
        for b in A:
            factor = [-b] + [ZERO] * (a0 - 1) + [ONE]
            LA = poly_mul(LA, factor)
        RA = poly_sub(poly_sub(LA, monomial(k + 2 * a0)), monomial(k + a0, z0))
        P_A = poly_neg(RA)
        assert degree(P_A) <= k
        S_A = [x for x in D if x ** a0 in set(A)]
        assert len(S_A) == agreement
        for x in S_A:
            assert poly_eval(U_poly, x) == poly_eval(P_A, x)
        quotient_sublist.add(poly_key(P_A))

    # Enumerate the full C_+ list at agreement size 12 by checking all 12-subsets.
    U_values = {x: poly_eval(U_poly, x) for x in D}
    full_cplus_list: Dict[Tuple[Fp2, ...], Poly] = {}
    for S in combinations(D, agreement):
        P_S = interpolate([(x, U_values[x]) for x in S])
        if degree(P_S) < k + 1:
            full_cplus_list[poly_key(P_S)] = P_S

    assert quotient_sublist.issubset(set(full_cplus_list))
    print(f"full RS[F,D,k+1] list size at agreement {agreement}: {len(full_cplus_list)}")

    alpha = T
    assert alpha not in D
    assert alpha.b != 0

    deep_image = {poly_eval(P_S, alpha) for P_S in full_cplus_list.values()}
    print(f"deep image size at alpha=t: {len(deep_image)}")

    # Verify the global far condition for CA: g_alpha has no degree-<k explanation
    # on any support of size k+1. This implies no explanation on any larger support.
    g_values = {x: -ONE / (x - alpha) for x in D}
    for T_support in combinations(D, k + 1):
        G_T = interpolate([(x, g_values[x]) for x in T_support])
        assert degree(G_T) >= k
    print("verified g_alpha is not degree-<k on any support of size > k")

    f_values = {x: U_values[x] / (x - alpha) for x in D}

    # Enumerate all slopes close to C_k at the same agreement size. For each support,
    # there is at most one such slope because g_alpha is not degree-<k on the support.
    close_slopes = set()
    for S in combinations(D, agreement):
        f_interp = interpolate([(x, f_values[x]) for x in S])
        g_interp = interpolate([(x, g_values[x]) for x in S])
        z = support_close_slope(f_interp, g_interp, k, agreement)
        if z is not None:
            close_slopes.add(z)

    print(f"slopes with f_alpha+z g_alpha close to C_k: {len(close_slopes)}")
    assert close_slopes == deep_image

    # Because the global far condition was verified above, every close slope is CA-bad.
    # Because the same support gives closeness and g_alpha is not explainable there,
    # every close slope is also support-wise MCA-bad.
    print("verified exact toy equality at delta_a: close slopes = Deep_alpha(U,a)")
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
