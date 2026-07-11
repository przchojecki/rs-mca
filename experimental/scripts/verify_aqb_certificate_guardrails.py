#!/usr/bin/env python3
"""Replay AQB certificate-interface guardrails.

The script checks the finite-deficit arithmetic and the toy certificate
semantics imported from the smooth-RS prize DAG.  It does not construct the
open AQB coupled-family manifest.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import product


SIGMA_STAR = 8_592_912_738
N = 2**40
D = 4_296_456_369
M = 2**39 + D
Q_MAX = Decimal(256)
THRESHOLD = 429_645_547

PI_TEXT = (
    "3.141592653589793238462643383279502884197169399375105820974944"
    "59230781640628620899"
)
PI = Decimal(PI_TEXT)


def log_factorial_bounds(n: int) -> tuple[Decimal, Decimal]:
    """Robbins bounds for ln(n!) for n >= 1."""
    x = Decimal(n)
    base = (x + Decimal("0.5")) * x.ln() - x
    base += Decimal("0.5") * (Decimal(2) * PI).ln()
    lower = base + Decimal(1) / (Decimal(12) * x + 1)
    upper = base + Decimal(1) / (Decimal(12) * x)
    return lower, upper


def check_deficit_arithmetic() -> None:
    getcontext().prec = 100
    log2 = Decimal(2).ln()

    n_lo, n_hi = log_factorial_bounds(N)
    m_lo, m_hi = log_factorial_bounds(M)
    r_lo, r_hi = log_factorial_bounds(N - M)

    log_c_lo = n_lo - m_hi - r_hi
    log_c_hi = n_hi - m_lo - r_lo

    deficit_lo = Decimal(D) * Q_MAX - 40 - log_c_hi / log2
    deficit_hi = Decimal(D) * Q_MAX - 40 - log_c_lo / log2
    qcrit_lo = (log_c_lo / log2 + 40) / Decimal(D)
    qcrit_hi = (log_c_hi / log2 + 40) / Decimal(D)
    per_fiber = Decimal(THRESHOLD) / Decimal(N)

    assert Decimal("429645546.7") < deficit_lo <= deficit_hi < Decimal("429645546.9")
    assert deficit_hi - deficit_lo < Decimal("1e-24")
    assert Decimal(THRESHOLD) - deficit_hi > Decimal("0.226")
    assert Decimal("255.9000000") < qcrit_lo <= qcrit_hi < Decimal("255.9000001")
    assert Decimal("0.0003907603") < per_fiber < Decimal("0.0003907604")

    print("deficit_arithmetic: PASS")
    print(f"  deficit_bits=[{deficit_lo:.30f}, {deficit_hi:.30f}]")
    print(f"  margin_bits={Decimal(THRESHOLD) - deficit_hi:.30f}")
    print(f"  qcrit=[{qcrit_lo:.30f}, {qcrit_hi:.30f}]")


def check_average_member_transfer() -> None:
    for length in range(1, 7):
        for values in product(range(5), repeat=length):
            for threshold_num in range(9):
                threshold = Fraction(threshold_num, 2)
                avg = sum(Fraction(value, 1) for value in values) / length
                if avg > threshold:
                    assert any(Fraction(value, 1) > threshold for value in values)

    print("average_member_transfer: PASS")


def verify_family_certificate(cert: dict) -> None:
    assert cert["sigma_star"] == SIGMA_STAR
    assert cert["c"] == 2

    shared = cert["shared"]
    assert shared["quotient_cell"]
    assert shared["fiber_data"]
    assert shared["reusable_box_charge"] is True

    members = cert["members"]
    assert isinstance(members, list)
    assert members

    seen = set()
    for member in members:
        ident = member["id"]
        assert ident not in seen
        seen.add(ident)
        assert member["sigma_star"] == SIGMA_STAR
        assert member["c"] == 2
        assert member["quotient_cell"] == shared["quotient_cell"]
        assert member["transfer_witness"]


def certified_net(ledger: dict) -> int:
    positives = [ledger["shared_entropy_lower"]]
    costs = [
        ledger["charged_box_upper"],
        ledger["overlap_upper"],
        ledger["multiplicity_upper"],
        ledger["quotient_fiber_upper"],
    ]
    return sum(positives) - sum(costs)


def accepts_entropy_ledger(ledger: dict) -> bool:
    required = {
        "shared_entropy_lower",
        "charged_box_upper",
        "overlap_upper",
        "multiplicity_upper",
        "quotient_fiber_upper",
    }
    if set(ledger) != required:
        return False
    return certified_net(ledger) >= THRESHOLD


def verify_coupled_manifest(manifest: dict) -> None:
    verify_family_certificate(manifest)

    member_ids = [member["id"] for member in manifest["members"]]
    ledger = manifest["ledger"]
    assert ledger["member_ids"] == member_ids
    assert ledger["quotient_cell"] == manifest["shared"]["quotient_cell"]
    assert certified_net(ledger) >= THRESHOLD


def toy_manifest() -> dict:
    return {
        "sigma_star": SIGMA_STAR,
        "c": 2,
        "shared": {
            "quotient_cell": "Q0",
            "fiber_data": {"fiber_rank": 40},
            "reusable_box_charge": True,
        },
        "members": [
            {
                "id": "w0",
                "sigma_star": SIGMA_STAR,
                "c": 2,
                "quotient_cell": "Q0",
                "transfer_witness": "L0",
            },
            {
                "id": "w1",
                "sigma_star": SIGMA_STAR,
                "c": 2,
                "quotient_cell": "Q0",
                "transfer_witness": "L1",
            },
        ],
        "ledger": {
            "member_ids": ["w0", "w1"],
            "quotient_cell": "Q0",
            "shared_entropy_lower": THRESHOLD + 1000,
            "charged_box_upper": 300,
            "overlap_upper": 200,
            "multiplicity_upper": 100,
            "quotient_fiber_upper": 50,
        },
    }


def check_certificate_semantics() -> None:
    manifest = toy_manifest()
    verify_family_certificate(manifest)
    verify_coupled_manifest(manifest)

    good_ledger = {
        "shared_entropy_lower": THRESHOLD + 1000,
        "charged_box_upper": 300,
        "overlap_upper": 200,
        "multiplicity_upper": 100,
        "quotient_fiber_upper": 50,
    }
    assert accepts_entropy_ledger(good_ledger)

    weak_ledger = dict(good_ledger)
    weak_ledger["shared_entropy_lower"] = THRESHOLD + 649
    assert not accepts_entropy_ledger(weak_ledger)

    missing_ledger = dict(good_ledger)
    missing_ledger.pop("overlap_upper")
    assert not accepts_entropy_ledger(missing_ledger)

    print("certificate_semantics: PASS")


def main() -> int:
    check_deficit_arithmetic()
    check_average_member_transfer()
    check_certificate_semantics()
    print("AQB_CERTIFICATE_GUARDRAILS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
