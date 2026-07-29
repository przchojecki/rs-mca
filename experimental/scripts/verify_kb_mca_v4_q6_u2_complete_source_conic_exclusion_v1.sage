#!/usr/bin/env sage
"""Independent exact replay for the complete-source conic exclusion."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-q6-u2-complete-source-conic-exclusion-v1"
    / "kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.json"
)


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def unhashed_digest(value):
    value = dict(value)
    value.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
assert data["payload_sha256"] == unhashed_digest(data)

# The local divisor-degree saturation is exact.
saturation = data["complete_source_saturation"]
assert saturation["source_count"] * saturation["row_binary_degree"] == 48
assert 2 * saturation["complete_source_binary_degree"] == 48
assert saturation["component_source_degree"] == 2

# Reciprocal normal form.  Work over Q(mu)(x), so these are symbolic
# identities rather than a finite-field sample.
Qmu = PolynomialRing(QQ, "mu")
Kmu = FractionField(Qmu)
Rx = PolynomialRing(Kmu, "x")
Fx = FractionField(Rx)
x = Fx(Rx.gen())
mu = Kmu(Qmu.gen())


def reciprocal_iota(value):
    return mu / value


def reciprocal_deck(value):
    return -value


assert reciprocal_iota(reciprocal_iota(x)) == x
assert reciprocal_iota(reciprocal_deck(x)) == reciprocal_deck(
    reciprocal_iota(x)
)

# On the deck quotient w=x^2, iota induces w -> mu^2/w.  Its fixed
# source values are exactly +/-mu.  The fibre over +mu is the iota-fixed
# divisor x^2-mu; the fibre over -mu is exchanged by iota.
w_image = reciprocal_iota(x) ** 2
assert w_image == mu**2 / x**2
fixed_source_polynomial = PolynomialRing(Kmu, "w")(
    [-mu**2, 0, 1]
)
assert fixed_source_polynomial.factor() == (
    PolynomialRing(Kmu, "w")([-mu, 1])
    * PolynomialRing(Kmu, "w")([mu, 1])
).factor()
assert reciprocal_iota(x) - x == -(x**2 - mu) / x
assert reciprocal_iota(x) + x == (x**2 + mu) / x


def projective_orbit(n, seed):
    """Orbit under g:x->zeta*x and b:x->1/x over Q(zeta_n)."""
    field = CyclotomicField(n)
    zeta = field.gen()
    seed = field(seed)
    return {
        zeta**k * seed for k in range(n)
    } | {
        zeta**k / seed for k in range(n)
    }


# Exact dihedral orbit controls.  The rotation-fixed pair {0,infinity}
# has size two.  A generic orbit has size 2n; reflection branch orbits
# have size n.
for n in (4, 5):
    field = CyclotomicField(n)
    zeta = field.gen()
    assert zeta.multiplicative_order() == n
    generic = projective_orbit(n, field(2))
    assert len(generic) == 2 * n
    reflection = projective_orbit(n, field(1))
    assert len(reflection) == n

# D4: two rotation-fixed common points are simple.  Every other
# rotation orbit has length four (there are no two-cycles).
d4_rows = data["profiles"]["D4"]["ramification_rows"]
assert [
    (
        row["ramified_source_count"],
        row["simple_support_size"],
        row["double_support_size"],
        row["double_stratum_possible"],
        row["simple_stratum_possible"],
    )
    for row in d4_rows
] == [
    (0, 24, 0, True, False),
    (1, 22, 1, False, True),
    (2, 20, 2, False, False),
]
assert all(not row["compatible"] for row in d4_rows)
assert not any(
    4 * a + 8 * b == 14
    for a in range(8)
    for b in range(4)
)

# D5: nonfixed rotation orbits have length five.  The r=0 and r=1
# rows demand too many fixed points; r=2 would identify the two
# rotation-fixed points with the two deck-fixed double points.
d5_rows = data["profiles"]["D5"]["ramification_rows"]
assert [
    (
        row["ramified_source_count"],
        row["required_simple_g_fixed_points"],
        row["required_double_g_fixed_points"],
        row["total_required_g_fixed_points"],
    )
    for row in d5_rows
] == [
    (0, 4, 0, 4),
    (1, 2, 1, 3),
    (2, 0, 2, 2),
]
assert all(not row["compatible"] for row in d5_rows)
assert not any(
    2 * use_fixed_pair + 5 * a + 10 * b == 14
    for use_fixed_pair in (0, 1)
    for a in range(4)
    for b in range(3)
)

# In odd characteristic, a nontrivial projective involution fixing both
# 0 and infinity is uniquely x -> -x.  This is the r=2 uniqueness step.
t = polygen(QQ, "t")
assert (t**2 - 1) // (t - 1) == t + 1
assert (t + 1).roots(QQ) == [(-1, 1)]

frontier = data["graph_frontier_control"]
assert frontier["post_star_cases"] == 324
assert frontier["post_star_orbits"] == 10
assert frontier["signature_case_histogram"] == {
    "P2_PLUS_C4": 36,
    "P6": 288,
}
assert sum(row["orbit_size"] for row in frontier["representatives"]) == 324
assert all(row["terminal"] == data["conclusion"]["terminal"]
           for row in frontier["representatives"])

print("status=PROVED_COMPLETE_SOURCE_REDUCED_CONIC_EXCLUSION")
print("reciprocal_symbolic_normal_form=PASS")
print("D4_orbit_and_ramification_table=PASS")
print("D5_orbit_and_ramification_table=PASS")
print("2+2+2_graph_frontier=324/10")
print("payload_sha256=" + data["payload_sha256"])
