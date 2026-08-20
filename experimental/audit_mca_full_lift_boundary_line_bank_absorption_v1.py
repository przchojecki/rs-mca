#!/usr/bin/env python3
"""Independent endpoint audit of the M31 boundary line bank."""


def replay(e: int, prefix: int, layers: int, groups: int,
           budget: int = 16777215) -> tuple[int, ...]:
    base = prefix + layers - groups
    required = budget - base + 1
    threshold = (required + groups - 1) // groups
    N, m, c, K = 1048582, 67454, 5, 6
    core = (threshold * m - N + threshold - 2) // (threshold - 1)
    inside = core - c
    sync = e - inside + K
    agreement = m - sync + 1
    n = N - e
    low = n * (agreement - c) // (agreement * agreement - n * c)
    bound = e * low + (N - m + 1)
    return base, threshold, core, inside, sync, agreement, low, bound


def main() -> None:
    last = replay(124805, 1636955, 2182, 34560)
    adjacent = replay(124806, 1636968, 2182, 34564)
    assert last == (
        1604577, 440, 65220, 65215, 59596, 7859, 126, 16706559)
    assert adjacent == (
        1604586, 439, 65214, 65209, 59603, 7852, 127, 16831491)
    assert 16777215 - last[-1] == 70656
    assert adjacent[-1] - 16777215 == 54276
    assert 124805 - 101157 + 1 == 23649
    print(
        "MCA_FULL_LIFT_BOUNDARY_LINE_BANK_ABSORPTION_V1_AUDIT_PASS "
        "last=124805 slack=70656 adjacent_excess=54276"
    )


if __name__ == "__main__":
    main()
