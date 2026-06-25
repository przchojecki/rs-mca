#!/usr/bin/env python3
"""Symbolic sanity check for the Cycle 18 resonance slope-map reduction.

Status: AUDIT. This checks only the formal algebra in the restricted
`B=F_p`, `F=F_{p^2}`, `t=sigma=2`, `j=3`, off-`R0` toy window. It does not
check source validity, split cubic density, or any corrected-reserve theorem.

The check models `F=B+alpha B` with `alpha^2=nu in B`, keeps `tau3` as a base
variable, and verifies:

    Delta = (p1 - tau3)(q2 - tau3) - p2 q1

has base component monic quadratic in `tau3` and alpha component degree <= 1.
It also checks the cleared-remainder identity for the graph gate

    s^2 Delta0 = Delta1 * (s tau3 + A s - h) + G,

where Delta0=tau3^2 + A tau3 + B, Delta1=s tau3 + h, and
G=h^2-Ahs+Bs^2.

Finally it verifies the slope-map normal form obtained by eliminating tau3:

    q1 z^2 - (p1 - q2) z - p2 = 0.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple


VARS = (
    "p10", "p11", "p20", "p21",
    "q10", "q11", "q20", "q21",
    "z0", "z1", "nu", "tau3",
)
TAU3_IDX = VARS.index("tau3")
Monomial = Tuple[int, ...]


@dataclass(frozen=True)
class Poly:
    terms: Dict[Monomial, int]

    @staticmethod
    def zero() -> "Poly":
        return Poly({})

    @staticmethod
    def one() -> "Poly":
        return Poly({(0,) * len(VARS): 1})

    @staticmethod
    def var(name: str) -> "Poly":
        exp = [0] * len(VARS)
        exp[VARS.index(name)] = 1
        return Poly({tuple(exp): 1})

    def __add__(self, other: "Poly") -> "Poly":
        out = dict(self.terms)
        for mon, coeff in other.terms.items():
            out[mon] = out.get(mon, 0) + coeff
            if out[mon] == 0:
                del out[mon]
        return Poly(out)

    def __neg__(self) -> "Poly":
        return Poly({mon: -coeff for mon, coeff in self.terms.items()})

    def __sub__(self, other: "Poly") -> "Poly":
        return self + (-other)

    def __mul__(self, other: "Poly") -> "Poly":
        out: Dict[Monomial, int] = {}
        for mon_a, coeff_a in self.terms.items():
            for mon_b, coeff_b in other.terms.items():
                mon = tuple(a + b for a, b in zip(mon_a, mon_b))
                out[mon] = out.get(mon, 0) + coeff_a * coeff_b
                if out[mon] == 0:
                    del out[mon]
        return Poly(out)

    def degree_in(self, name: str) -> int:
        if not self.terms:
            return -1
        idx = VARS.index(name)
        return max(mon[idx] for mon in self.terms)

    def coeff_of_power(self, name: str, power: int) -> "Poly":
        idx = VARS.index(name)
        out: Dict[Monomial, int] = {}
        for mon, coeff in self.terms.items():
            if mon[idx] != power:
                continue
            reduced = list(mon)
            reduced[idx] = 0
            out[tuple(reduced)] = out.get(tuple(reduced), 0) + coeff
        return Poly({mon: coeff for mon, coeff in out.items() if coeff})

    def format(self) -> str:
        if not self.terms:
            return "0"
        chunks = []
        for mon in sorted(self.terms):
            coeff = self.terms[mon]
            factors = []
            for var, exp in zip(VARS, mon):
                if exp == 1:
                    factors.append(var)
                elif exp > 1:
                    factors.append(f"{var}^{exp}")
            body = "*".join(factors)
            if body:
                if coeff == 1:
                    chunks.append(body)
                elif coeff == -1:
                    chunks.append(f"-{body}")
                else:
                    chunks.append(f"{coeff}*{body}")
            else:
                chunks.append(str(coeff))
        return " + ".join(chunks).replace("+ -", "- ")


@dataclass(frozen=True)
class FElem:
    b0: Poly
    b1: Poly

    def __add__(self, other: "FElem") -> "FElem":
        return FElem(self.b0 + other.b0, self.b1 + other.b1)

    def __neg__(self) -> "FElem":
        return FElem(-self.b0, -self.b1)

    def __sub__(self, other: "FElem") -> "FElem":
        return self + (-other)

    def __mul__(self, other: "FElem") -> "FElem":
        nu = Poly.var("nu")
        return FElem(
            self.b0 * other.b0 + nu * self.b1 * other.b1,
            self.b0 * other.b1 + self.b1 * other.b0,
        )


def fvar(base: str) -> FElem:
    return FElem(Poly.var(f"{base}0"), Poly.var(f"{base}1"))


def bvar(name: str) -> FElem:
    return FElem(Poly.var(name), Poly.zero())


def assert_equal(actual: Poly, expected: Poly, label: str) -> None:
    if actual.terms != expected.terms:
        raise AssertionError(
            f"{label} failed:\nactual:   {actual.format()}\nexpected: {expected.format()}"
        )


def assert_felem_equal(actual: FElem, expected: FElem, label: str) -> None:
    assert_equal(actual.b0, expected.b0, f"{label} base")
    assert_equal(actual.b1, expected.b1, f"{label} alpha")


def main() -> None:
    p1 = fvar("p1")
    p2 = fvar("p2")
    q1 = fvar("q1")
    q2 = fvar("q2")
    z = fvar("z")
    tau3 = bvar("tau3")

    # Coordinates in the F-basis {[W]_E, b}:
    # iota=(p1-tau3)[W]_E + p2 b, mu=q1[W]_E + (q2-tau3)b.
    delta = (p1 - tau3) * (q2 - tau3) - p2 * q1

    tau = Poly.var("tau3")
    p10 = Poly.var("p10")
    p11 = Poly.var("p11")
    p20 = Poly.var("p20")
    p21 = Poly.var("p21")
    q10 = Poly.var("q10")
    q11 = Poly.var("q11")
    q20 = Poly.var("q20")
    q21 = Poly.var("q21")
    nu = Poly.var("nu")

    expected_delta0 = (
        tau * tau
        - (p10 + q20) * tau
        + p10 * q20
        + nu * p11 * q21
        - p20 * q10
        - nu * p21 * q11
    )
    expected_delta1 = (
        -(p11 + q21) * tau
        + p10 * q21
        + p11 * q20
        - p20 * q11
        - p21 * q10
    )

    assert_equal(delta.b0, expected_delta0, "Delta0")
    assert_equal(delta.b1, expected_delta1, "Delta1")
    assert_equal(delta.b0.coeff_of_power("tau3", 2), Poly.one(), "Delta0 tau3^2 coefficient")
    if delta.b1.degree_in("tau3") > 1:
        raise AssertionError("Delta1 unexpectedly has tau3 degree > 1")

    s = delta.b1.coeff_of_power("tau3", 1)
    h = delta.b1.coeff_of_power("tau3", 0)
    a_coeff = delta.b0.coeff_of_power("tau3", 1)
    b_coeff = delta.b0.coeff_of_power("tau3", 0)
    g_gate = h * h - a_coeff * h * s + b_coeff * s * s
    multiplier = s * tau + a_coeff * s - h
    remainder_identity = s * s * delta.b0 - delta.b1 * multiplier - g_gate
    assert_equal(remainder_identity, Poly.zero(), "G cleared-remainder identity")

    tau3_from_first_coordinate = p1 - z * q1
    slope_quadratic = q1 * z * z - (p1 - q2) * z - p2
    second_coordinate_residual = p2 - z * (q2 - tau3_from_first_coordinate)
    assert_felem_equal(
        second_coordinate_residual + slope_quadratic,
        FElem(Poly.zero(), Poly.zero()),
        "slope quadratic elimination",
    )

    print("delta_identity_ok=True")
    print("g_remainder_identity_ok=True")
    print("slope_quadratic_identity_ok=True")
    print(f"Delta0_deg_tau3={delta.b0.degree_in('tau3')}")
    print("Delta0_tau3^2_coeff=1")
    print(f"Delta1_deg_tau3={delta.b1.degree_in('tau3')}")
    print(f"Delta1_tau3_coeff_s={s.format()}")
    print(f"Delta1_tau3_constant_h={h.format()}")
    print("graph_branch=if s != 0, Delta1=0 gives tau3=-h/s")
    print("slope_branch=on q1 != 0, z=(p1+h/s)/q1 on that graph")


if __name__ == "__main__":
    main()
