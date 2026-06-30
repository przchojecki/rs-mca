#!/usr/bin/env python3
"""Verify the L1 monomial dyadic descent proof packet.

This verifier checks the finite arithmetic in the monomial-prefix locator
classification recorded in
``experimental/notes/l1/l1_monomial_dyadic_descent_survivors.md``.  It does
not enumerate all supports in the order-512 domain.  Instead it checks the
reviewable finite gates used by the proof: the local length-16 imbalance
classification, the dyadic divisibility gate, the survivor table, the
impossible rows, explicit quotient-complement witnesses for every admissible
row, quotient-level elementary vanishings, and the lifted order-512
elementary-coefficient vanishings that make those witnesses monomial-admissible.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PACKET = ROOT / (
    "experimental/data/certificates/l1-monomial-dyadic-descent/"
    "f17_32_n512_deg256_monomial_dyadic_packet.json"
)

SCHEMA_VERSION = "l1-monomial-dyadic-descent-packet-v1"
P = 17
OMEGA = 3
N = 512
DEGREE_BOUND = 256
A_MIN = 258
A_MAX = 512

EXPECTED_CANDIDATES = [
    258,
    259,
    260,
    261,
    262,
    264,
    266,
    268,
    272,
    276,
    280,
    288,
    296,
    304,
    320,
    336,
    352,
    384,
    416,
    448,
    512,
]

EXPECTED_ADMISSIBLE = [
    258,
    259,
    260,
    262,
    264,
    268,
    272,
    280,
    288,
    304,
    320,
    352,
    384,
    512,
]

EXPECTED_IMPOSSIBLE = [261, 266, 276, 296, 336, 416, 448]


class PacketError(Exception):
    """Raised when the packet fails a verification gate."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PacketError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise PacketError(f"{path}: packet must be a JSON object")
    return data


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PacketError(message)


def require_int(value: Any, location: str) -> int:
    if not isinstance(value, int):
        raise PacketError(f"{location} must be an integer")
    return value


def require_int_list(value: Any, location: str) -> list[int]:
    if not isinstance(value, list) or not all(isinstance(item, int) for item in value):
        raise PacketError(f"{location} must be a list of integers")
    return value


def mod(value: int) -> int:
    return value % P


def multiplicative_order(value: int, prime: int) -> int:
    require(math.gcd(value, prime) == 1, "order input must be nonzero mod p")
    current = 1
    for exponent in range(1, prime):
        current = (current * value) % prime
        if current == 1:
            return exponent
    raise PacketError("multiplicative order search failed")


def eval_delta(delta: tuple[int, ...], odd_power: int) -> int:
    total = 0
    for q, coefficient in enumerate(delta):
        total += coefficient * pow(OMEGA, odd_power * q, P)
    return mod(total)


def shift_mod_u8_plus_1(delta: tuple[int, ...], shift: int) -> tuple[int, ...]:
    out = [0] * 8
    for q, coefficient in enumerate(delta):
        target = q + shift
        if target < 8:
            out[target] += coefficient
        else:
            out[target - 8] -= coefficient
    return tuple(out)


def canonical_delta(delta: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(mod(value) for value in delta)


def delta_weight(delta: tuple[int, ...]) -> int:
    return sum(1 for value in delta if value != 0)


def verify_local16(local: dict[str, Any]) -> None:
    require(local.get("p") == P, "local16.p mismatch")
    require(local.get("omega") == OMEGA, "local16.omega mismatch")
    delta0 = tuple(require_int_list(local.get("delta0"), "local16.delta0"))
    require(len(delta0) == 8, "local16.delta0 must have length 8")

    require(
        multiplicative_order(OMEGA, P) == local.get("omega_order") == 16,
        "omega must have order 16 in F_17^*",
    )
    values = [eval_delta(delta0, power) for power in (1, 3, 5)]
    require(values == local.get("delta0_values_at_1_3_5"), "delta0 value mismatch")

    expected = {canonical_delta((0,) * 8)}
    for shift in range(8):
        shifted = shift_mod_u8_plus_1(delta0, shift)
        expected.add(canonical_delta(shifted))
        expected.add(canonical_delta(tuple(-value for value in shifted)))

    solutions_13: list[tuple[int, ...]] = []
    solutions_135: list[tuple[int, ...]] = []
    for delta in itertools.product((-1, 0, 1), repeat=8):
        if eval_delta(delta, 1) == 0 and eval_delta(delta, 3) == 0:
            solutions_13.append(delta)
            if eval_delta(delta, 5) == 0:
                solutions_135.append(delta)

    require(
        len(solutions_13) == local.get("solution_count_for_1_3") == 17,
        "local16 solution count mismatch",
    )
    require(
        sorted({delta_weight(delta) for delta in solutions_13})
        == local.get("solution_weights"),
        "local16 solution weight mismatch",
    )
    require(
        {canonical_delta(delta) for delta in solutions_13} == expected,
        "local16 signed-shift classification mismatch",
    )
    require(
        solutions_135 == [(0,) * 8]
        and local.get("solution_count_for_1_3_5") == 1,
        "local16 p1/p3/p5 gate mismatch",
    )


def verify_basis_gate(basis: dict[str, Any]) -> None:
    h_values = require_int_list(basis.get("h_values"), "basis.h_values")
    require(h_values == [1, 2, 4, 8, 16, 32], "basis h-values mismatch")
    require(basis.get("binomial") == "X^h - 3", "basis binomial mismatch")
    order = multiplicative_order(3, P)
    require(order == 16, "3 must have order 16")
    for h in h_values:
        require(h == 1 or (h & (h - 1) == 0), f"h={h} must be a power of two")
        if h == 1:
            continue
        require(order % 2 == 0, "prime divisor 2 must divide ord(3)")
        require(math.gcd(h, (P - 1) // order) == 1, f"binomial gcd gate failed at h={h}")
        if h % 4 == 0:
            require(P % 4 == 1, f"binomial 4 | h gate failed at h={h}")


def forced_q(agreement: int, gates: list[dict[str, Any]]) -> int:
    q = 1
    for gate in gates:
        min_agreement = require_int(gate.get("min_A"), "descent_gates.min_A")
        forced = require_int(gate.get("forced_divisor"), "descent_gates.forced_divisor")
        if agreement >= min_agreement:
            q = max(q, forced)
    return q


def verify_descent_gates(gates: list[dict[str, Any]]) -> None:
    expected = [
        {"r": 0, "moment_threshold": 5, "min_A": 262, "forced_divisor": 2},
        {"r": 1, "moment_threshold": 10, "min_A": 267, "forced_divisor": 4},
        {"r": 2, "moment_threshold": 20, "min_A": 277, "forced_divisor": 8},
        {"r": 3, "moment_threshold": 40, "min_A": 297, "forced_divisor": 16},
        {"r": 4, "moment_threshold": 80, "min_A": 337, "forced_divisor": 32},
        {"r": 5, "moment_threshold": 160, "min_A": 417, "forced_divisor": 64},
    ]
    require(gates == expected, "descent gate table mismatch")
    for gate in gates:
        r = gate["r"]
        require(gate["moment_threshold"] == 5 * (2**r), "bad moment threshold")
        require(gate["min_A"] == DEGREE_BOUND + 1 + gate["moment_threshold"], "bad min_A")
        require(gate["forced_divisor"] == 2 ** (r + 1), "bad forced divisor")


def expected_survivor_row(agreement: int, gates: list[dict[str, Any]]) -> dict[str, int]:
    q = forced_q(agreement, gates)
    n_quotient = N // q
    b = agreement // q
    d_bound = DEGREE_BOUND // q
    return {
        "A": agreement,
        "Q": q,
        "N": n_quotient,
        "B": b,
        "D": d_bound,
        "d": b - d_bound - 1,
        "c": n_quotient - b,
    }


def verify_survivors(packet: dict[str, Any], gates: list[dict[str, Any]]) -> None:
    candidates = [
        agreement
        for agreement in range(A_MIN, A_MAX + 1)
        if agreement % forced_q(agreement, gates) == 0
    ]
    require(candidates == EXPECTED_CANDIDATES, "candidate sizes from gates mismatch")
    require(packet.get("candidate_sizes") == EXPECTED_CANDIDATES, "packet candidate list mismatch")

    rows = packet.get("survivor_rows")
    require(isinstance(rows, list), "survivor_rows must be a list")
    require([row.get("A") for row in rows] == EXPECTED_CANDIDATES, "survivor row order mismatch")

    impossible = set(EXPECTED_IMPOSSIBLE)
    admissible = set(EXPECTED_ADMISSIBLE)
    for row in rows:
        require(isinstance(row, dict), "survivor row must be an object")
        agreement = require_int(row.get("A"), "survivor_rows.A")
        expected = expected_survivor_row(agreement, gates)
        for key, value in expected.items():
            require(row.get(key) == value, f"A={agreement}: {key} mismatch")

        status = row.get("status")
        if agreement in impossible:
            require(status == "impossible", f"A={agreement}: expected impossible")
            verify_impossible_reason(row)
        elif agreement in admissible:
            require(status == "admissible", f"A={agreement}: expected admissible")
            verify_admissible_family(row)
        else:
            raise PacketError(f"A={agreement}: neither admissible nor impossible")

    require(packet.get("impossible_candidate_sizes") == EXPECTED_IMPOSSIBLE, "impossible list mismatch")
    require(packet.get("final_admissible_sizes") == EXPECTED_ADMISSIBLE, "admissible list mismatch")


def verify_impossible_reason(row: dict[str, Any]) -> None:
    agreement = row["A"]
    reason = row.get("reason")
    if agreement == 448:
        require(row["d"] == 2 and row["c"] == 1, "A=448 singleton data mismatch")
        require(reason == "one nonzero quotient-complement point cannot satisfy p_1=0", "A=448 reason mismatch")
        return
    require(row["d"] == 4 and row["c"] % 2 == 1, f"A={agreement}: parity data mismatch")
    require(reason == "d=4 with odd quotient-complement size", f"A={agreement}: reason mismatch")


def verify_e0_witness(witness: dict[str, Any]) -> None:
    e0 = require_int_list(witness.get("E0_mod_17"), "nonemptiness.E0_mod_17")
    require(e0 == [1, 2, 3, 13, 15], "E0 witness mismatch")
    require(sum(e0) % P == 0, "E0 p1 witness failed")
    require(sum((value * value) % P for value in e0) % P == 0, "E0 p2 witness failed")


def exponent_vector(exponent: int, n_quotient: int) -> tuple[int, ...]:
    require(n_quotient % 16 == 0, "quotient order must be divisible by 16")
    h = n_quotient // 16
    exponent %= n_quotient
    basis_index = exponent % h
    omega_power = exponent // h
    out = [0] * h
    out[basis_index] = pow(OMEGA, omega_power, P)
    return tuple(out)


def power_sum(exponents: set[int], n_quotient: int, power: int) -> tuple[int, ...]:
    require(power > 0, "power must be positive")
    h = n_quotient // 16
    total = [0] * h
    for exponent in exponents:
        vector = exponent_vector(exponent * power, n_quotient)
        for index, value in enumerate(vector):
            total[index] = (total[index] + value) % P
    return tuple(total)


def add_vectors(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    require(len(left) == len(right), "vector dimension mismatch")
    return tuple((a + b) % P for a, b in zip(left, right, strict=True))


def multiply_vector_by_exponent(
    vector: tuple[int, ...], exponent: int, n_quotient: int
) -> tuple[int, ...]:
    h = n_quotient // 16
    require(len(vector) == h, "field vector dimension mismatch")
    out = [0] * h
    for basis_index, coefficient in enumerate(vector):
        if coefficient == 0:
            continue
        shifted = exponent_vector(exponent + basis_index, n_quotient)
        for index, value in enumerate(shifted):
            out[index] = (out[index] + coefficient * value) % P
    return tuple(out)


def elementary_coefficients(
    exponents: set[int], n_quotient: int, degree: int
) -> list[tuple[int, ...]]:
    h = n_quotient // 16
    one = (1,) + (0,) * (h - 1)
    coefficients = [zero_vector(n_quotient) for _ in range(degree + 1)]
    coefficients[0] = one
    used = 0
    for exponent in sorted(exponents):
        used += 1
        for index in range(min(degree, used), 0, -1):
            coefficients[index] = add_vectors(
                coefficients[index],
                multiply_vector_by_exponent(
                    coefficients[index - 1], exponent, n_quotient
                ),
            )
    return coefficients


def zero_vector(n_quotient: int) -> tuple[int, ...]:
    return (0,) * (n_quotient // 16)


def logs_base_omega(values: list[int]) -> list[int]:
    table = {pow(OMEGA, exponent, P): exponent for exponent in range(16)}
    return [table[value % P] for value in values]


def order4_coset(n_quotient: int, representative: int) -> set[int]:
    step = n_quotient // 4
    return {(representative + step * index) % n_quotient for index in range(4)}


def construct_d1_witness(row: dict[str, Any]) -> set[int]:
    n_quotient = row["N"]
    c = row["c"]
    require(c % 2 == 0, "d=1 witness needs even complement size")
    pair_count = c // 2
    out: set[int] = set()
    for exponent in range(pair_count):
        out.add(exponent)
        out.add((exponent + n_quotient // 2) % n_quotient)
    return out


def construct_d2_witness(row: dict[str, Any], e0_values: list[int]) -> set[int]:
    n_quotient = row["N"]
    c = row["c"]
    h = n_quotient // 16
    e0_exponents = {h * log_value for log_value in logs_base_omega(e0_values)}
    out = set(e0_exponents)
    extra_cosets = (c - len(e0_exponents)) // 4
    require(len(e0_exponents) == 5, "E0 exponent set size mismatch")
    require(c >= 5 and (c - 5) % 4 == 0, "d=2 complement size mismatch")
    if extra_cosets == 0:
        return out
    forbidden = set()
    for exponent in e0_exponents:
        forbidden.update(order4_coset(n_quotient, exponent % (n_quotient // 4)))
    added = 0
    for representative in range(n_quotient // 4):
        coset = order4_coset(n_quotient, representative)
        if coset & forbidden:
            continue
        out.update(coset)
        added += 1
        if added == extra_cosets:
            break
    require(added == extra_cosets, f"N={n_quotient}: not enough order-4 cosets")
    return out


def construct_d3_witness(row: dict[str, Any]) -> set[int]:
    n_quotient = row["N"]
    c = row["c"]
    require(c % 4 == 0, "d=3 witness needs order-4 coset count")
    out: set[int] = set()
    for representative in range(c // 4):
        out.update(order4_coset(n_quotient, representative))
    return out


def construct_complement_witness(
    row: dict[str, Any], witnesses: dict[str, Any]
) -> set[int]:
    agreement = row["A"]
    if agreement == 512:
        return set()
    if row["d"] == 1:
        return construct_d1_witness(row)
    if row["d"] == 2:
        e0 = require_int_list(witnesses.get("E0_mod_17"), "nonemptiness.E0_mod_17")
        return construct_d2_witness(row, e0)
    if row["d"] == 3:
        return construct_d3_witness(row)
    raise PacketError(f"A={agreement}: no constructive witness rule")


def lift_quotient_support(row: dict[str, Any], support: set[int]) -> set[int]:
    q = row["Q"]
    n_quotient = row["N"]
    lifted: set[int] = set()
    for exponent in support:
        for kernel_index in range(q):
            lifted.add(exponent + kernel_index * n_quotient)
    return lifted


def verify_constructive_witnesses(packet: dict[str, Any]) -> None:
    witnesses = packet.get("nonemptiness_witnesses")
    require(isinstance(witnesses, dict), "nonemptiness_witnesses must be an object")
    rules = packet.get("constructive_witness_rules")
    require(isinstance(rules, dict), "constructive_witness_rules must be an object")
    require(
        rules.get("encoding") == "exponents of the quotient generator alpha in G_N",
        "constructive witness encoding mismatch",
    )
    require(rules.get("d1") == "first c/2 antipodal pairs", "d1 constructive rule mismatch")
    require(
        rules.get("d2") == "E0 plus first disjoint order-4 cosets",
        "d2 constructive rule mismatch",
    )
    require(rules.get("d3") == "first c/4 order-4 cosets", "d3 constructive rule mismatch")
    require(
        rules.get("direct_admissibility_check")
        == "for T=G_N\\C, verify e_1(T)=...=e_d(T)=0",
        "direct admissibility rule mismatch",
    )
    require(
        rules.get("full_lift_check")
        == "lift T to S in H and verify e_1(S)=...=e_(A-257)(S)=0",
        "full lift rule mismatch",
    )

    for row in packet["survivor_rows"]:
        if row.get("status") != "admissible":
            continue
        complement = construct_complement_witness(row, witnesses)
        agreement = row["A"]
        n_quotient = row["N"]
        c = row["c"]
        d = row["d"]
        require(len(complement) == c, f"A={agreement}: complement size mismatch")
        require(all(0 <= exponent < n_quotient for exponent in complement), f"A={agreement}: exponent outside quotient group")
        support = set(range(n_quotient)) - complement
        require(len(support) == row["B"], f"A={agreement}: quotient support size mismatch")
        if c:
            require(n_quotient >= 16, f"A={agreement}: nonempty witness needs N>=16")
            for power in range(1, d + 1):
                require(
                    power_sum(complement, n_quotient, power) == zero_vector(n_quotient),
                    f"A={agreement}: quotient complement p_{power} does not vanish",
                )
            quotient_elementary = elementary_coefficients(support, n_quotient, d)
            for index in range(1, d + 1):
                require(
                    quotient_elementary[index] == zero_vector(n_quotient),
                    f"A={agreement}: quotient support e_{index} does not vanish",
                )
        lifted_support = lift_quotient_support(row, support)
        full_degree = agreement - DEGREE_BOUND - 1
        require(len(lifted_support) == agreement, f"A={agreement}: lifted support size mismatch")
        full_elementary = elementary_coefficients(lifted_support, N, full_degree)
        for index in range(1, full_degree + 1):
            require(
                full_elementary[index] == zero_vector(N),
                f"A={agreement}: lifted support e_{index} does not vanish",
            )


def verify_admissible_family(row: dict[str, Any]) -> None:
    agreement = row["A"]
    family = row.get("family")
    d = row["d"]
    c = row["c"]
    n_quotient = row["N"]
    if agreement == 512:
        require(c == 0 and family == "empty_complement", "A=512 family mismatch")
        return
    if agreement == 384:
        require(
            d == 3 and c == 4 and family == "one_order_4_coset_in_G_16",
            "A=384 family mismatch",
        )
        return
    if d == 1:
        require(c % 2 == 0 and family == f"Z_1({n_quotient},{c})", f"A={agreement}: Z1 family mismatch")
        return
    if d == 2:
        require(family == f"Z_2({n_quotient},{c})", f"A={agreement}: Z2 family mismatch")
        require(c >= 5 and (c - 5) % 4 == 0, f"A={agreement}: E0+cosets size mismatch")
        extra_cosets = (c - 5) // 4
        if extra_cosets:
            require(n_quotient // 4 - 5 >= extra_cosets, f"A={agreement}: not enough disjoint order-4 cosets")
        return
    if d == 3:
        require(family == f"Z_3({n_quotient},{c})", f"A={agreement}: Z3 family mismatch")
        require(c % 4 == 0, f"A={agreement}: order-4 coset union size mismatch")
        return
    raise PacketError(f"A={agreement}: unsupported admissible family")


def verify_nonemptiness(packet: dict[str, Any]) -> None:
    witnesses = packet.get("nonemptiness_witnesses")
    require(isinstance(witnesses, dict), "nonemptiness_witnesses must be an object")
    verify_e0_witness(witnesses)
    require(
        witnesses.get("d1_witness") == "any 127 antipodal pairs in G_512",
        "d1 witness mismatch",
    )
    require(
        witnesses.get("d3_witness") == "union of complete order-4 cosets",
        "d3 witness mismatch",
    )


def validate_packet(packet: dict[str, Any]) -> None:
    require(packet.get("schema_version") == SCHEMA_VERSION, "schema_version mismatch")
    require(packet.get("status") == "PROVED / AUDIT", "status mismatch")

    row = packet.get("row")
    require(isinstance(row, dict), "row must be an object")
    require(row.get("base_prime") == P, "row.base_prime mismatch")
    require(row.get("extension_degree") == 32, "row.extension_degree mismatch")
    require(row.get("domain_order") == N, "row.domain_order mismatch")
    require(row.get("degree_bound_inclusive") == DEGREE_BOUND, "degree bound mismatch")
    require(row.get("standard_rs_dimension_if_promoted") == DEGREE_BOUND + 1, "dimension convention mismatch")

    agreement_range = packet.get("agreement_range")
    require(isinstance(agreement_range, dict), "agreement_range must be an object")
    require(agreement_range.get("A_min") == A_MIN, "agreement_range.A_min mismatch")
    require(agreement_range.get("A_max") == A_MAX, "agreement_range.A_max mismatch")

    verify_local16(packet.get("local16", {}))
    verify_basis_gate(packet.get("basis_gate", {}))
    gates = packet.get("descent_gates")
    require(isinstance(gates, list), "descent_gates must be a list")
    verify_descent_gates(gates)
    verify_survivors(packet, gates)
    verify_nonemptiness(packet)
    verify_constructive_witnesses(packet)

    nonclaims = packet.get("nonclaims", [])
    require(isinstance(nonclaims, list), "nonclaims must be a list")
    require(
        "not an arbitrary-word L1 local-limit theorem" in nonclaims,
        "missing arbitrary-word nonclaim",
    )
    require(
        "not an MCA, line-decoding, interleaved-list, or protocol theorem" in nonclaims,
        "missing protocol nonclaim",
    )


def check_path(path: Path) -> None:
    validate_packet(load_json(path))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--expect-fail", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    try:
        check_path(args.check)
    except PacketError as exc:
        if args.expect_fail:
            if not args.quiet:
                print(f"EXPECTED-FAIL {args.check}: {exc}")
            return 0
        print(f"FAIL {args.check}: {exc}")
        return 1

    if args.expect_fail:
        print(f"UNEXPECTED-PASS {args.check}")
        return 1
    if not args.quiet:
        print("L1 monomial dyadic descent packet checks passed")
        print("  field: F_17[z]/(z^32 - 3), |<z>|=512")
        print("  degree bound: deg P <= 256")
        print(f"  candidates after divisibility gate: {len(EXPECTED_CANDIDATES)}")
        print(f"  admissible sizes: {EXPECTED_ADMISSIBLE}")
        print("  constructive quotient-complement witnesses: checked")
        print("  quotient support elementary vanishings: checked")
        print("  lifted order-512 elementary vanishings: checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
