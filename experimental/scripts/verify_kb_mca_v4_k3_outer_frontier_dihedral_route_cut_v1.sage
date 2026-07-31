#!/usr/bin/env sage
"""Independent Sage replay of the fixed-point-free dihedral route cut."""

import copy
import hashlib
import json
from pathlib import Path

if "__file__" in globals():
    SCRIPT = Path(__file__).resolve()
    ROOT = SCRIPT.parents[2]
else:
    ROOT = Path.cwd()
CERTIFICATE = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-k3-outer-frontier-dihedral-route-cut-v1/"
    "kb_mca_v4_k3_outer_frontier_dihedral_route_cut_v1.json"
)


def canonical_payload(value):
    body = copy.deepcopy(value)
    body.pop("payload_sha256", None)
    encoded = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


certificate = json.loads(CERTIFICATE.read_text())
assert canonical_payload(certificate) == certificate["payload_sha256"]

p = Integer(2130706433)
N = Integer(2)^21
m = N // 2
seed = Integer(3)
assert p.is_prime()
assert p - 1 == 127 * Integer(2)^24

F = GF(p)
a = F(seed)^((p - 1) // N)
assert Integer(a) == 1213133211
assert a.multiplicative_order() == N
assert a^m == -F.one()

# The two involutions are represented projectively by these matrices.
tau1 = matrix(F, [[0, a], [1, 0]])
tau2 = matrix(F, [[0, a^3], [1, 0]])
identity = identity_matrix(F, 2)
assert tau1 * tau1 == a * identity
assert tau2 * tau2 == a^3 * identity
rotation = tau2 * tau1
assert rotation == a * matrix(F, [[a^2, 0], [0, 1]])
assert (a^2).multiplicative_order() == N // 2
generated_group_order = 2 * (N // 2)
assert generated_group_order == N

# On D=<a>, a reflection fixed point would solve 2k=1 or 2k=3 mod N.
assert gcd(2, N) == 2
assert Integer(1) % gcd(2, N) != 0
assert Integer(3) % gcd(2, N) != 0

# The quotient identity is checked in a two-variable rational function
# field, and the full degree-two fibre is checked over F_p(x).
S = PolynomialRing(F, names=("X", "T"))
X, T_symbol = S.gens()
L = FractionField(S)
R = PolynomialRing(F, "x")
x_poly = R.gen()
K = FractionField(R)
x = K(x_poly)
RT = PolynomialRing(K, "T")
T = RT.gen()
quotient_records = []
for name, exponent, coefficient_label in (
    ("q1", 1, "a"),
    ("q2", 3, "a^3"),
):
    c = a^exponent
    qT = L(T_symbol) + L(c) / L(T_symbol)
    qX = L(X) + L(c) / L(X)
    assert qT - qX == (
        (L(T_symbol) - L(X))
        * (L(T_symbol) * L(X) - L(c))
        / (L(T_symbol) * L(X))
    )
    numerator = x_poly^2 + c
    denominator = x_poly
    assert gcd(numerator, denominator) == 1
    assert max(numerator.degree(), denominator.degree()) == 2
    fibre_polynomial = T^2 - (x + K(c) / x) * T + K(c)
    assert fibre_polynomial == (T - x) * (T - K(c) / x)
    assert fibre_polynomial.degree() == 2
    assert c^N == 1
    assert Integer(exponent) % gcd(2, N) != 0
    quotient_records.append(
        {
            "name": name,
            "involution": f"x |-> {coefficient_label}/x",
            "coefficient": coefficient_label,
            "coefficient_value": Integer(c),
            "formula": f"{name}(x)=x+{coefficient_label}/x",
            "fibre_difference_formula": (
                f"{name}(T)-{name}(x)="
                f"((T-x)(T*x-{coefficient_label}))/(T*x)"
            ),
            "rational_map_degree": 2,
            "preserves_D": True,
            "complete_D_fibre_formula": (
                f"{name}^(-1)({name}(x))={{x,"
                f"{coefficient_label}/x}} for x in D"
            ),
            "D_fibre_complete": True,
            "D_fibre_reduced": True,
            "D_fibre_cardinality": 2,
        }
    )

# Independently realize the common invariant as a rational function.
u = x^m - x^(-m)
assert u.numerator().degree() == N
assert u.denominator().degree() == m
assert gcd(u.numerator(), u.denominator()) == 1
assert max(u.numerator().degree(), u.denominator().degree()) == N
assert (p - 1) % N == 0
assert gcd(p, N) == 1
zero_polynomial = x_poly^N - 1
assert zero_polynomial.degree() == N
assert gcd(zero_polynomial, zero_polynomial.derivative()) == 1
# D=<a> already supplies N distinct roots of this degree-N polynomial.
assert a.multiplicative_order() == N
zero_fibre = {
    "equation": "u^(-1)(0)=D",
    "defining_polynomial": "x^N-1",
    "cardinality": Integer(N),
    "fibre_degree": Integer(N),
    "complete": True,
    "reduced": True,
    "separability": "N divides p-1 and p does not divide N",
    "pole_support": ["0", "infinity"],
    "pole_orders": {"0": Integer(m), "infinity": Integer(m)},
    "pole_divisor_degree": Integer(N),
}
assert zero_fibre["pole_orders"]["0"] == m
assert zero_fibre["pole_orders"]["infinity"] == (
    u.numerator().degree() - u.denominator().degree()
)
assert sum(zero_fibre["pole_orders"].values()) == N

# c^N=1 and c^(N/2)=-1 for c=a,a^3.  Substitution in
# (x^N-1)/x^m gives
# ((c/x)^N-1)/(c/x)^m=(x^N-1)/x^m without expanding a degree-N
# polynomial.  Likewise (a^2)^m=1 proves rotation invariance.
for c in (a, a^3):
    assert c^N == 1
    assert c^m == -1
assert (a^2)^m == 1

# Artin's fixed-field theorem gives [F(x):F(x)^G]=|G|=N.  The rational
# map u has degree N and is G-invariant, so the inclusion F(u)<=F(x)^G
# is an equality.  On D, x^m is +/-1, hence u=x^m-x^(-m)=0.
fixed_field_degree = max(u.numerator().degree(), u.denominator().degree())
assert fixed_field_degree == generated_group_order == N
assert p.gcd(N) == 1
assert all(value - value^(-1) == 0 for value in (F.one(), -F.one()))

route = certificate["deployed_dihedral_route_cut"]
assert route["field_prime"] == p
assert route["carrier_order"] == N
assert route["carrier_generator"] == Integer(a)
assert route["quadratic_quotient_fibres"] == quotient_records
assert route["rotation_order"] == N // 2
assert route["generated_group_order"] == generated_group_order
assert route["common_invariant_rational_map_degree"] == fixed_field_degree
assert route["common_invariant_value_on_D"] == 0
assert route["common_invariant_zero_fibre"] == zero_fibre
assert route["tau1_fixed_point_free_on_D"]
assert route["tau2_fixed_point_free_on_D"]
assert route["fixed_field_intersection_proved"]
assert not route["actual_received_line_record_constructed"]

print(
    "SAGE_PASS "
    f"p={p} N={N} a={Integer(a)} "
    f"rotation_order={N // 2} dihedral_order={generated_group_order} "
    f"quadratic_fibres=complete_reduced_2 "
    f"fixed_field_degree={fixed_field_degree} "
    f"zero_fibre=complete_reduced_{N} invariant_on_D=0"
)
