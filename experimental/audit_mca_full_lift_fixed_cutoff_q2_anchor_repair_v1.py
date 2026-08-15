#!/usr/bin/env python3
"""Independent constant audit of the M31 fixed-cutoff q=2 repair."""


def main() -> None:
    budget, forcing, d1, d2 = 16777215, 16895280, 284224, 258385
    lower = forcing - d1 - d2
    threshold = budget - lower + 1
    assert (lower, threshold) == (16352671, 424545)
    cases = (
        3813497,
        forcing - d1 + 94742 + 1,
        forcing - d1 + 2,
        forcing - d1 + 94742,
        forcing - d1 + 3,
    )
    assert cases == (
        3813497, 16705799, 16611058, 16705798, 16611059)
    assert max(cases) == 16705799
    assert budget - max(cases) == 71416
    assert (101157 - 6) % 3 == 0
    print(
        "MCA_FULL_LIFT_FIXED_CUTOFF_Q2_ANCHOR_REPAIR_V1_AUDIT_PASS "
        "bound=16705799 slack=71416 adjacent_q=0"
    )


if __name__ == "__main__":
    main()
