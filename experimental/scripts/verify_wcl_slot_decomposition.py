#!/usr/bin/env python3
"""Completeness certificate for the WCL ten-slot decomposition (portable).

Companion to experimental/notes/wcl_slot_contributor_requests.md. From the
pinned primitives (dyadic tower, extended ledger window, Newton short-window
bound, the proved weight floors, the zero-event mass threshold), enumerate
every surviving (ell, w) cell and assert the result is EXACTLY the ten open
cells the contributor requests name (plus the two census-closed siblings).
Contributors can therefore trust that the requested sweeps jointly exhaust
the obligation: closing the ten cells closes the zone statement.

Mutation controls prove the enumeration is sensitive to each primitive,
including a simulated level-index/level-dimension conflation (the historical
error class this machinery exists to prevent).

Stdlib only; runs in under a second. Exit 0 iff everything passes.
"""
from fractions import Fraction

T = 2 ** 33                                # dyadic tower total
N_LEVELS = 34
THRESHOLD = Fraction(1, 32)                # per-level zone mass bound
WINDOW_LO, WINDOW_HI = 1, 7                # extended ledger [L+1, L+7], L = DIMENSION
AMBIENT_EXCLUDED = {(1, 3), (1, 4)}        # proved weight-3/4 ambient census theorems
CENSUS_CLOSED = {(2, 5), (2, 6)}           # closed by norm-gcd / recursive-norm certificates

OPEN_CELLS = {(1, 5), (1, 6), (1, 7), (1, 8),
              (2, 7), (2, 8), (2, 9),
              (4, 9), (4, 10), (4, 11)}


def tower_dims():
    return [-(-(T // 2 ** j) // 2) for j in range(N_LEVELS)]


def newton_floor(ell):
    """Newton short-window theorem: reduced vanishers need w >= 2*ell + 1."""
    return 2 * ell + 1


def one_orbit_mass(ell, w):
    return Fraction(2 * 256 * ell, 2 ** w)


def enumerate_cells(dims=None, window_hi=WINDOW_HI, newton=newton_floor,
                    ambient=AMBIENT_EXCLUDED, threshold=THRESHOLD):
    live, closed, weighted = set(), set(), set()
    for ell in set(dims if dims is not None else tower_dims()):
        for w in range(ell + WINDOW_LO, ell + window_hi + 1):
            if w < newton(ell):
                continue
            if (ell, w) in ambient:
                continue
            if one_orbit_mass(ell, w) <= threshold:
                weighted.add((ell, w))
                continue
            (closed if (ell, w) in CENSUS_CLOSED else live).add((ell, w))
    return live, closed, weighted


def main() -> int:
    dims = tower_dims()
    assert sum(dims) == T and len(dims) == N_LEVELS
    assert dims.count(1) == 2  # two terminal dimension-1 levels share the (1, w) cells

    live, closed, weighted = enumerate_cells()
    assert weighted == set(), f"non-zero-event cells inside a window: {weighted}"
    assert closed == CENSUS_CLOSED
    assert live == OPEN_CELLS, f"DECOMPOSITION MISMATCH: {sorted(live ^ OPEN_CELLS)}"
    for ell, w in sorted(live):
        assert one_orbit_mass(ell, w) >= 32 * THRESHOLD  # every open cell zero-event, >= 32x margin

    caught = 0
    l1, _, w1 = enumerate_cells(threshold=Fraction(3, 1))
    if w1 or l1 != OPEN_CELLS:
        caught += 1
    l2, _, _ = enumerate_cells(window_hi=WINDOW_HI + 1)
    if l2 - OPEN_CELLS == {(1, 9), (2, 10), (4, 12)}:
        caught += 1
    l3, _, _ = enumerate_cells(newton=lambda ell: 2 * ell + 2)
    if (4, 9) not in l3 and l3 != OPEN_CELLS:
        caught += 1
    l4, _, _ = enumerate_cells(ambient=set())
    if l4 - OPEN_CELLS == {(1, 3), (1, 4)}:
        caught += 1
    idx_cells = set()
    for j, ell in enumerate(tower_dims()):
        L = j + 1  # the conflation: windows keyed to level INDEX
        for w in range(L + WINDOW_LO, L + WINDOW_HI + 1):
            if w >= newton_floor(ell) and (ell, w) not in AMBIENT_EXCLUDED \
               and one_orbit_mass(ell, w) > THRESHOLD:
                idx_cells.add((ell, w))
    if idx_cells != OPEN_CELLS | CENSUS_CLOSED:
        caught += 1
    assert caught == 5, f"mutation controls caught {caught}/5"

    print("WCL_SLOT_DECOMPOSITION_PASS open=10 closed=2 weighted=0 "
          "min_margin=32x mutations=5/5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
