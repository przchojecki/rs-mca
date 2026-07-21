#!/usr/bin/env python3
"""Fail-closed exact-integer audit of the quotient-cell prefix-fiber floor.

Companion to experimental/notes/audits/
audit_quotient_cell_prefix_fiber_and_split_pencil_census.md.

The object: for C = RS[F, D, n/2], c | n/2, N = n/c, 0 < s < c,
1 <= d <= N/2 - 1, m = N/2 + d, cyclic rotation modulo Y^N - delta plus a
fixed s-point tail produces at least

    ceil( C(N-1, m) / (N * q^(d-1)) )                       (CR1)

distinct codewords agreeing on exactly n/2 + d*c + s points.  This is a
QUOTIENT-CELL construction (it lives on the quotient of length N = n/c,
c > 1): under the first-match ledger its fibers are assigned to the
quotient cell, NOT the primitive leaf.  It exhibits a super-polynomial
fiber one cell over from the primitive leaf, so it does not refute (Q).

This script decides every claim by exact big-integer comparison (floats
only in the reported margin displays):

  A. the pigeonhole floor logic itself (generic exact self-test);
  B. the sigma = 2^34 - 1 endpoint instance (n = 2^41, c = 2^33, d = 1,
     N = 256, m = 129): fiber floor > 2^238 >> 2^128, even at q = 2^256;
  C. the cap-row instance (c = 2^22, d = 2048, N = 524288, m = 264192):
     the unsafe criterion N*q^d < 2^128 * C(N-1, m) holds at q = 2^256
     with a ~75.08-bit margin;
  D. mutation controls: wrong denominator exponent, tightened envelope,
     and an over-strict field exponent must each be REJECTED.

Stdlib only; runs in a few seconds.  Exit 0 iff everything passes.
"""
import math
import sys


def log2_int(x: int) -> float:
    b = x.bit_length()
    if b <= 64:
        return math.log2(x)
    return (b - 64) + math.log2(x >> (b - 64))


def fiber_floor(N: int, m: int, q: int, d: int) -> int:
    """ceil( C(N-1, m) / (N * q^(d-1)) ) by exact integer arithmetic."""
    count = math.comb(N - 1, m)
    buckets = N * pow(q, d - 1)
    return -(-count // buckets)


def pigeonhole_self_test() -> None:
    # Generic exactness: for a battery of (count, buckets), the floor is the
    # least integer f with f * buckets >= count.
    for count, buckets in ((10, 3), (12, 4), (1, 7), (2 ** 137 + 5, 2 ** 19),
                           (math.comb(255, 129), 256)):
        f = -(-count // buckets)
        assert f * buckets >= count and (f - 1) * buckets < count


def endpoint_instance() -> tuple[float, int]:
    # n = 2^41, k = 2^40, c = 2^33, d = 1, s = c-1: sigma = d*c + s = 2^34-1,
    # quotient length N = n/c = 256, m = k/c + d = 129.
    n, k, c, d = 1 << 41, 1 << 40, 1 << 33, 1
    s = c - 1
    sigma = d * c + s
    N, m = n // c, k // c + d
    assert (sigma, N, m) == ((1 << 34) - 1, 256, 129)
    assert c > 1 and (n // 2) % c == 0 and 0 < s < c and 1 <= d <= N // 2 - 1
    q = 1 << 256  # the worst admissible field under the official cap
    floor = fiber_floor(N, m, q, d)
    assert floor > 1 << 238
    assert floor > 1 << 128  # super-polynomial past the 2^-128 envelope
    # the unsafe criterion at the endpoint: N*q^d < 2^128 * C(N-1, m)
    assert N * pow(q, d) < (math.comb(N - 1, m) << 128)
    return log2_int(floor), sigma


def cap_row_instance() -> float:
    # n = 2^41, c = 2^22, d = 2048, N = 524288, m = 264192 (statement cap row).
    n, k, c, d = 1 << 41, 1 << 40, 1 << 22, 2048
    N, m = n // c, k // c + d
    assert (N, m) == (524288, 264192)
    assert c > 1 and (n // 2) % c == 0 and 1 <= d <= N // 2 - 1
    q = 1 << 256
    lhs = N * pow(q, d)
    rhs = math.comb(N - 1, m) << 128
    assert lhs < rhs  # (CR3) at the official cap
    return log2_int(rhs) - log2_int(lhs)


def mutation_controls() -> int:
    caught = 0
    N, m, q, d = 256, 129, 1 << 256, 1

    # M1: wrong denominator exponent (d-1 -> d): the floor must collapse
    # below the envelope.
    bad = -(-math.comb(N - 1, m) // (N * pow(q, d)))
    if bad <= 1 << 128:
        caught += 1

    # M2: tightened envelope (2^-128 -> 2^-256): the endpoint floor must no
    # longer clear it.
    floor = fiber_floor(N, m, q, d)
    if floor <= 1 << 256:
        caught += 1

    # M3: over-strict field exponent at the cap row (q = 2^257 > cap): the
    # margin (~75 bits) must not survive 2048 extra field bits.
    Nc, mc, dc = 524288, 264192, 2048
    if Nc * pow(1 << 257, dc) >= (math.comb(Nc - 1, mc) << 128):
        caught += 1

    return caught


def main() -> int:
    pigeonhole_self_test()
    floor_bits, sigma = endpoint_instance()
    margin = cap_row_instance()
    caught = mutation_controls()
    if caught != 3:
        raise AssertionError(f"mutation controls caught {caught}/3")
    print(f"QUOTIENT_CELL_PREFIX_FIBER_FLOOR_PASS endpoint_sigma={sigma} "
          f"endpoint_floor_bits={floor_bits:.2f} cap_margin_bits={margin:.6f} "
          f"mutations=3/3")
    return 0


if __name__ == "__main__":
    sys.exit(main())
