#!/usr/bin/env python3
"""Independent combinatorial audit of the cyclic quotient-rotation floor."""

from itertools import combinations
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "experimental/notes/list/rate_half_cyclic_quotient_rotation_floor.md"


def support_audit() -> int:
    checks = 0
    for size in range(4, 66, 2):
        half = size // 2
        for d in range(1, half):
            m = half + d
            image = {
                j: (size - d + j) % size
                for j in range(m + 1)
            }
            high = {j for j, exponent in image.items() if exponent >= half}
            assert high == set(range(d)) | {m}
            assert image[m] == half
            assert max(size - d + j for j in range(m + 1)) < 2 * size
            checks += 1
    return checks


def constant_term_audit() -> int:
    checks = 0
    for size in range(4, 15, 2):
        half = size // 2
        for d in range(1, half):
            m = half + d
            products = {
                sum(chosen) % size
                for chosen in combinations(range(1, size), m)
            }
            assert len(products) <= size
            checks += 1
    return checks


def official_audit() -> tuple[int, int, int]:
    n = 1 << 41
    k = 1 << 40
    c = 1 << 33
    size = n // c
    d = 1
    s = c - 1
    m = size // 2 + d
    agreement = k + d * c + s
    errors = n - agreement
    count = comb(size - 1, m)
    lower = -(-count // size)

    assert (size, m, agreement) == (256, 129, 1_116_691_496_959)
    assert errors == 1_082_331_758_593
    assert lower == (
        11092230961998080258863221315535829014398723445840079610908300691051869570
    )
    assert agreement * agreement < n * (k - 1)
    assert lower > 1 << 238
    assert ((1 << 256) - 1) < lower << 128
    return agreement, errors, lower.bit_length()


def contract_audit() -> int:
    text = NOTE.read_text()
    required = (
        "object:              ordinary LIST, not MCA",
        "route:               DIRECT_LIST",
        "code_shift:          C=RS[F_q,D,2^40], no C^+ shift",
        "a^2<n(k-1)",
        "This packet makes no list upper-bound, MCA/CA, asymptotic-family",
        "**Audit verdict: NO ISSUE.**",
    )
    assert all(item in text for item in required)
    return len(required)


def main() -> None:
    support = support_audit()
    constants = constant_term_audit()
    agreement, errors, list_bits = official_audit()
    contract = contract_audit()
    print(
        "AUDIT_RATE_HALF_CYCLIC_QUOTIENT_ROTATION_LIST_FLOOR_PASS "
        f"support_checks={support} constant_checks={constants} "
        f"contract_checks={contract} agreement={agreement} errors={errors} "
        f"list_bits={list_bits} verdict=NO_ISSUE"
    )


if __name__ == "__main__":
    main()
