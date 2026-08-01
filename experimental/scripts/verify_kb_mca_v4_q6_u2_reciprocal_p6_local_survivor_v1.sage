"""Independent Sage replay of the deployed reciprocal-P6 witness."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-q6-u2-reciprocal-p6-local-survivor-v1"
    / "kb_mca_v4_q6_u2_reciprocal_p6_local_survivor_v1.json"
)
with CERTIFICATE.open(encoding="utf-8") as handle:
    data = json.load(handle)

assert data["status"] == "PROVED_LOCAL_SOURCE_FACET_SURVIVOR"
assert data["scope"]["terminal"] == "UNROUTED_LOCAL_COMPONENT"
assert data["scope"]["owner_id"] is None
assert data["scope"]["ledger_movement"] == 0

p = Integer(data["row"]["field_characteristic"])
assert p == 2130706433
assert p.is_prime()
assert data["row"]["field_extension_degree"] == 6
Fp = GF(p)
Rp.<Z> = PolynomialRing(Fp)
witness = data["witness"]
c = Fp(witness["quadratic_subfield"]["omega_square"])
assert not c.is_square()
E.<w> = GF(p^2, modulus=Z^2-c)
Rlambda.<L> = PolynomialRing(E)

alpha = [E(value) for value in witness["alpha_noninvariant"]]
factor_multipliers = witness["factor_sequence_multipliers"]
factors = [E(value)*w for value in factor_multipliers]
path = data["scope"]["signature_path"]
right_permutation = data["scope"]["right_label_permutation"]

assert len(set(alpha)) == 6
assert all(value != 0 for value in alpha)
assert all(value^2 != 1 for value in alpha)
assert alpha[3] == 1/alpha[1]
assert alpha[5] == 1/alpha[4]
assert len(set(factors)) == 7
assert all(q^2 != 4 for q in factors)
assert all(
    len((L^2-q*L+1).roots(multiplicities=False)) == 2
    for q in factors
)

row_factors = {}
for position, label in enumerate(path):
    row_factors[label] = (
        factors[position],
        factors[position+1],
    )
s_values = [sum(row_factors[label]) for label in range(6)]
p_values = [
    row_factors[label][0]*row_factors[label][1]
    for label in range(6)
]

def interpolate3(values):
    matrix3 = matrix(
        E,
        [[1, alpha[index], alpha[index]^2] for index in range(3)],
    )
    coefficients = matrix3.solve_right(vector(E, values[:3]))
    return sum(coefficients[index]*L^index for index in range(3))

S = interpolate3(s_values)
P = interpolate3(p_values)
assert [S(value) for value in alpha] == s_values
assert [P(value) for value in alpha] == p_values
assert [S[index]/w for index in range(3)] == [
    E(value) for value in witness["S_coefficient_multipliers"]
]
assert [P[index] for index in range(3)] == [
    E(value) for value in witness["P_coefficients"]
]
assert S[1]*P[2]-S[2]*P[1] != 0

rows = {
    label:
    (L^2-row_factors[label][0]*L+1)
    *(L^2-row_factors[label][1]*L+1)
    for label in range(6)
}
path_edges = {
    tuple(sorted((path[index], path[index+1])))
    for index in range(5)
}
for left in range(6):
    assert rows[left].gcd(rows[left].derivative()).degree() == 0
    for right in range(left+1, 6):
        expected = 2 if (left, right) in path_edges else 0
        assert rows[left].gcd(rows[right]).degree() == expected

scale_coefficients = witness["weighted_GRS_scale_coefficients"]
assert scale_coefficients == [1, 0, 0]
for moment in range(3):
    for coefficient_index in range(4):
        parity_check = E(0)
        for index, value in enumerate(alpha):
            denominator = prod(
                value-other
                for other_index, other in enumerate(alpha)
                if other_index != index
            )
            scale_value = sum(
                E(scale_coefficients[degree])*value^degree
                for degree in range(3)
            )
            parity_check += (
                value^moment
                * scale_value
                * rows[index][coefficient_index]
                / denominator
            )
        assert parity_check == 0

RT.<T> = PolynomialRing(E)
RX.<X> = PolynomialRing(RT)
S_T = sum(E(S[index])*T^index for index in range(3))
P_T = sum(E(P[index])*T^index for index in range(3))
H = X^4-S_T*X^3+(2+P_T)*X^2-S_T*X+1
for index, value in enumerate(alpha):
    evaluated = Rlambda([
        E(coefficient(value)) for coefficient in H.list()
    ])
    assert evaluated == rows[index]

a = factors[2]
b = factors[5]
common = [E(0), a, -a, -b, b]
common_decic = prod(L^2-q*L+1 for q in common)
assert common_decic.degree() == 10
assert common_decic.list() == list(reversed(common_decic.list()))
assert all(common_decic[index] == 0 for index in range(1, 10, 2))
assert common_decic.gcd(common_decic.derivative()).degree() == 0
assert common_decic.gcd(L^2-1).degree() == 0

free0 = factors[0]
free2 = factors[6]
candidate = vector(E, [1, -free0, -1]).cross_product(
    vector(E, [1, -free2, -1])
)
assert candidate[0] != 0
assert candidate/candidate[0] == vector(E, [1, 0, 1])

pole_edges = (
    {(left, left) for left in range(6)}
    | {(left, (left-1) % 6) for left in range(6)}
)
assert all(
    right_permutation[right] != left
    for left, right in pole_edges
)
for endpoint, free in [(0, free0), (2, free2)]:
    right_vertices = [endpoint, (endpoint-1) % 6]
    source_indices = [
        right_permutation[right] for right in right_vertices
    ]
    source_values = [alpha[index] for index in source_indices]
    assert sum(source_values) == free^2-2
    assert prod(source_values) == 1
    assert endpoint not in source_indices

locator = (
    (L+1)
    *(L^2+(2-a^2)*L+1)
    *(L^2+(2-b^2)*L+1)
)
assert locator.list() == [
    E(value)
    for value in witness["common_source_locator_coefficients"]
]
assert locator.gcd(locator.derivative()).degree() == 0
assert locator(-1) == 0
assert locator(1) != 0
assert locator(0) != 0
assert all(locator(value) != 0 for value in alpha)
assert locator.list() == list(reversed(locator.list()))
common_source_labels = locator.roots(multiplicities=False)
assert len(common_source_labels) == 5
all_source_labels = set(alpha + common_source_labels + [E(0)])
assert len(all_source_labels) == 12

print("status=PROVED_LOCAL_SOURCE_FACET_SURVIVOR")
print("field=F_%s^2<=F_%s^6" % (p, p))
print("source_labels=12")
print("weighted_GRS_checks=12")
print("signature=P6")
print("terminal=UNROUTED_LOCAL_COMPONENT")
print("ledger_movement=0")
