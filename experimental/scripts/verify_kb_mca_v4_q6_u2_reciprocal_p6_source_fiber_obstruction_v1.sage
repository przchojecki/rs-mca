"""Independent Sage replay of the reciprocal-P6 source-fiber obstruction."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARENT_CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-q6-u2-reciprocal-p6-local-survivor-v1"
    / "kb_mca_v4_q6_u2_reciprocal_p6_local_survivor_v1.json"
)
CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-q6-u2-reciprocal-p6-source-fiber-obstruction-v1"
    / "kb_mca_v4_q6_u2_reciprocal_p6_source_fiber_obstruction_v1.json"
)

with PARENT_CERTIFICATE.open(encoding="utf-8") as handle:
    parent = json.load(handle)
with CERTIFICATE.open(encoding="utf-8") as handle:
    data = json.load(handle)

assert parent["status"] == "PROVED_LOCAL_SOURCE_FACET_SURVIVOR"
assert (
    parent["payload_sha256"]
    == "a3231f7903e255b254b202a269aca1740aec666cd04c13940711e83d29e8ce1b"
)
assert (
    data["status"]
    == "PROVED_WITNESS_SPECIFIC_ACTIVE_SOURCE_FIBER_DELETION"
)
assert data["dependency"]["parent_pr"] == 1126
assert data["dependency"]["parent_payload_sha256"] == parent["payload_sha256"]

p = Integer(data["row"]["field_characteristic"])
assert p == 2130706433
assert p.is_prime()
Fp = GF(p)
R0.<u> = PolynomialRing(Fp)
c = Fp(data["field"]["omega_square"])
assert not c.is_square()
E.<w> = GF(p^2, modulus=u^2-c)
RX.<X> = PolynomialRing(E)
RT.<T> = PolynomialRing(E)


def decode(pair):
    assert len(pair) == 2
    return E(pair[0]) + E(pair[1])*w


def encode(value):
    entries = E(value).polynomial().list()
    entries += [Fp(0)]*(2-len(entries))
    return [Integer(entries[0]), Integer(entries[1])]


def coefficients(poly, degree):
    return [encode(poly[index]) for index in range(degree+1)]


witness = parent["witness"]
source_records = data["source_rows"]
sources = [decode(record["label"]) for record in source_records]
assert len(sources) == 12
assert len(set(sources)) == 12

common_locator = RT([
    E(value)
    for value in witness["common_source_locator_coefficients"]
])
common_roots = set(common_locator.roots(multiplicities=False))
assert common_locator.degree() == 5
assert common_locator.gcd(common_locator.derivative()).degree() == 0
assert common_roots == set(sources[:5])
assert sources[5] == 0
assert sources[6:] == [
    E(value) for value in witness["alpha_noninvariant"]
]

B = prod(X^2-source for source in sources)
assert B.degree() == 24
assert B.gcd(B.derivative()).monic() == X
assert coefficients(B, 24) == data[
    "complete_source_polynomial_coefficients"
]

S_coefficients = [
    E(value)*w for value in witness["S_coefficient_multipliers"]
]
P_coefficients = [
    E(value) for value in witness["P_coefficients"]
]


def evaluate(coefficients_list, value):
    return sum(
        coefficient*value^index
        for index, coefficient in enumerate(coefficients_list)
    )


def H_row(value):
    s_value = evaluate(S_coefficients, value)
    p_value = evaluate(P_coefficients, value)
    return (
        X^4
        - s_value*X^3
        + (2+p_value)*X^2
        - s_value*X
        + 1
    )


gcd_degrees = []
for index, (source, record) in enumerate(
    zip(sources, source_records, strict=True)
):
    row = H_row(source)
    divisor = row.gcd(B).monic()
    degree = divisor.degree()
    gcd_degrees.append(degree)
    assert row.degree() == 4
    assert coefficients(row, 4) == record["H_row_coefficients"]
    assert coefficients(divisor, degree) == record[
        "gcd_with_complete_source_polynomial_coefficients"
    ]
    assert degree == record["gcd_degree"]
    assert (degree == 4) == record[
        "passes_necessary_source_fiber_gate"
    ]

assert gcd_degrees == [0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4]
assert data["obstruction"]["gcd_degree_histogram"] == {"0": 6, "4": 6}
assert data["obstruction"]["fatal_source_indices"] == list(range(6))

# Bind the six passing fibers to the exact parent P6 rows.
factor_sequence = [
    E(value)*w for value in witness["factor_sequence_multipliers"]
]
path = parent["scope"]["signature_path"]
row_factors = {}
for position, row_index in enumerate(path):
    row_factors[row_index] = (
        factor_sequence[position],
        factor_sequence[position+1],
    )
for row_index, source in enumerate(sources[6:]):
    first, second = row_factors[row_index]
    expected = (X^2-first*X+1)*(X^2-second*X+1)
    assert H_row(source) == expected
    assert expected.divides(B)

assert (
    data["obstruction"]["terminal"]
    == "DELETED_BY_ACTIVE_SOURCE_FIBER_DIVISIBILITY"
)
assert data["obstruction"]["witness_lifts_to_active_producer"] is False
assert data["obstruction"]["owner_id"] is None
assert data["obstruction"]["ledger_movement"] == 0

print("status=PROVED_WITNESS_SPECIFIC_ACTIVE_SOURCE_FIBER_DELETION")
print("field=F_%s^2<=F_%s^6" % (p, p))
print("source_rows=12")
print("gcd_degrees=%s" % gcd_degrees)
print("fatal_source_rows=6")
print("terminal=DELETED_BY_ACTIVE_SOURCE_FIBER_DIVISIBILITY")
print("ledger_movement=0")
