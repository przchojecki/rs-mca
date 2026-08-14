#!/usr/bin/env python3
"""Verify the guarded owner substrate stacked on the rank-11 pair-core cut."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-dense-core-owner-substrate-v1/manifest.json"
PARENT = "6a5dcdae1591fc7f044eda6a942bfe178521a48c"
PACKET_FILES = [
    "agents.md",
    "experimental/agents-log.md",
    "experimental/grande_finale.tex",
    "experimental/notes/thresholds/kb_mca_dense_core_owner_substrate_v1.md",
    "experimental/data/certificates/kb-mca-dense-core-owner-substrate-v1/README.md",
    "experimental/scripts/verify_kb_mca_dense_core_owner_substrate_v1.py",
    "experimental/scripts/verify_kb_mca_dense_core_owner_substrate_v1_independent.py",
]
SOURCE_NODES = {
    "reserve_repricing": {
        "id": "rate_half_mca_two_anchor_reserve_repricing",
        "path": "background/nodes/rate_half_mca_two_anchor_reserve_repricing",
        "commit": "2607c6fa7957eac4883547f9af3bbcaf9495e572",
        "tree": "f64dcacc0bb3b7a94a2fba1e3713f0172a7e3e5d",
        "contract_sha256": "172934ca92647c61e054f30b8ec25be83844f2859f32245a20c5234eda11f56e",
    },
    "unguarded_transport_counterexample": {
        "id": "rate_half_mca_kplus1_badness_transport_counterexample",
        "path": "background/nodes/rate_half_mca_kplus1_badness_transport_counterexample",
        "commit": "80d430a681ee1f823ec1941e8a57a204a73843a0",
        "tree": "05070eb518cd275cf194d55357f99c45c1cce464",
        "contract_sha256": "391421a32ad5f40bb1be20754760065ea31490f226e13151e79a3ad61a837365",
    },
    "guarded_lattice_adapter": {
        "id": "rate_half_mca_degree_guarded_shifted_lattice_witness_adapter",
        "path": "background/nodes/rate_half_mca_degree_guarded_shifted_lattice_witness_adapter",
        "commit": "3f626c84d1f6d76fff77a26e7d3d1586ebc869f8",
        "tree": "ba43f74f8deb085889b8d5d5c6d605436f7bafc5",
        "contract_sha256": "94935311eaf6f4292add51fe8be92c08d66a17362babc07510b2b5b6a9532517",
    },
    "typed_pole_line_witness": {
        "id": "rate_half_mca_pole_line_typed_witness_certificate",
        "path": "background/nodes/rate_half_mca_pole_line_typed_witness_certificate",
        "commit": "d888aff329548ad92691e5f6c192ba037da13cc6",
        "tree": "e035a3feb580244957e2c258191c401714426395",
        "contract_sha256": "9423f8ab7c0444205ba7eb9a78fdf16a818d58d1dc0e17c6a81c74a78eb2edc4",
    },
}
ROWS = (
    {
        "name": "KoalaBear MCA",
        "n": 2097152,
        "K": 1048576,
        "m": 1116048,
        "budget": 274980728111395087,
        "average_ceiling": 57198030366,
    },
    {
        "name": "Mersenne-31 MCA stress row",
        "n": 2097152,
        "K": 1048576,
        "m": 1116024,
        "budget": 16777215,
        "average_ceiling": 1752700,
    },
)


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def trim(poly: list[int], p: int) -> list[int]:
    out = [value % p for value in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def degree(poly: list[int], p: int) -> int:
    value = trim(poly, p)
    return -1 if value == [0] else len(value) - 1


def add(left: list[int], right: list[int], p: int) -> list[int]:
    size = max(len(left), len(right))
    return trim(
        [
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
            for index in range(size)
        ],
        p,
    )


def scale(poly: list[int], scalar: int, p: int) -> list[int]:
    return trim([scalar * value for value in poly], p)


def multiply(left: list[int], right: list[int], p: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = (out[i + j] + a * b) % p
    return trim(out, p)


def divide(left: list[int], right: list[int], p: int) -> tuple[list[int], list[int]]:
    dividend = trim(left[:], p)
    divisor = trim(right[:], p)
    require(divisor != [0], "polynomial division by zero")
    if len(dividend) < len(divisor):
        return [0], dividend
    quotient = [0] * (len(dividend) - len(divisor) + 1)
    inverse = pow(divisor[-1], -1, p)
    while dividend != [0] and len(dividend) >= len(divisor):
        shift = len(dividend) - len(divisor)
        coefficient = dividend[-1] * inverse % p
        quotient[shift] = coefficient
        for index, value in enumerate(divisor):
            dividend[index + shift] = (
                dividend[index + shift] - coefficient * value
            ) % p
        dividend = trim(dividend, p)
    return trim(quotient, p), dividend


def gcd(left: list[int], right: list[int], p: int) -> list[int]:
    a, b = trim(left, p), trim(right, p)
    while b != [0]:
        _, remainder = divide(a, b, p)
        a, b = b, remainder
    inverse = pow(a[-1], -1, p)
    return trim([inverse * value for value in a], p)


def pow_x(exponent: int, modulus: list[int], p: int) -> list[int]:
    result = [1]
    base = [0, 1]
    while exponent:
        if exponent & 1:
            result = divide(multiply(result, base, p), modulus, p)[1]
        base = divide(multiply(base, base, p), modulus, p)[1]
        exponent >>= 1
    return trim(result, p)


def interpolate(points: tuple[int, ...], values: tuple[int, ...], p: int) -> list[int]:
    out = [0]
    for i, (x_i, y_i) in enumerate(zip(points, values)):
        basis = [1]
        denominator = 1
        for j, x_j in enumerate(points):
            if i == j:
                continue
            basis = multiply(basis, [(-x_j) % p, 1], p)
            denominator = denominator * (x_i - x_j) % p
        out = add(out, scale(basis, y_i * pow(denominator, -1, p), p), p)
    return trim(out, p)


def reserve_rows() -> list[dict[str, int | str]]:
    output: list[dict[str, int | str]] = []
    for row in ROWS:
        n, dimension, agreement, budget, average = (
            row[key] for key in ("n", "K", "m", "budget", "average_ceiling")
        )
        w = agreement - dimension
        two_w = 2 * w
        reserve = two_w + 31
        g_min = 2 * agreement - dimension + 1
        target_min = budget - reserve - (n - g_min)
        target_full = budget - reserve
        quotient, remainder = divmod(target_full, average)
        require(two_w > 31, "near reserve is not a 31-slope exception")
        require(reserve + n < budget, "middle branch margin")
        require(reserve + n - agreement + 1 < budget, "small-owner margin")
        for g in range(g_min, n + 1):
            target = budget - reserve - (n - g)
            require(two_w + 31 + (n - g) + target == budget, "owner sum")
            require(
                budget - 31 - (n - g) - target == two_w,
                "exact repricing",
            )
        output.append(
            {
                **row,
                "w": w,
                "two_w": two_w,
                "combined_reserve": reserve,
                "g_min": g_min,
                "target_g_min": target_min,
                "target_full": target_full,
                "full_average_quotient": quotient,
                "full_average_remainder": remainder,
            }
        )
    return output


def field_and_transport() -> dict[str, Any]:
    p = 2130706433
    n = 1 << 21
    k = 1 << 20
    m = 1116048
    e = 67473
    zeta = pow(3, (p - 1) // n, p)
    require(p - 1 == 127 * 2**24, "base factorization")
    for prime, witness in ((2, 3), (127, 2)):
        require(pow(witness, p - 1, p) == 1, "Pocklington power")
        require(
            math.gcd(pow(witness, (p - 1) // prime, p) - 1, p) == 1,
            "Pocklington gcd",
        )
    require(zeta == 1213133211, "carrier generator")
    require(pow(zeta, n, p) == 1 and pow(zeta, n // 2, p) == p - 1, "carrier order")
    require(e + m == 1183521 < n, "prefix/support separation")
    require(not (k < k) and k < k + 1 and m > k, "dimension switch")
    return {
        "p": p,
        "p_minus_1_factorization": "127*2^24",
        "pocklington_witnesses": {"2": 3, "127": 2},
        "n": n,
        "k": k,
        "m": m,
        "zeta": zeta,
        "error_prefix_size": e,
        "support_end_exclusive": e + m,
        "slope": 0,
        "direction_degree": k,
        "in_code_k": False,
        "in_code_kplus1": True,
        "root_surplus": m - k,
    }


def guarded_adapter() -> dict[str, Any]:
    n, k, m = 2097152, 1048576, 1116048
    omega = n - m
    require(omega + k == 2029680, "effective cap")
    require(omega + k - 1 == 2029679, "actual cap")
    shift_checks = 0
    for deg_w in range(9):
        for deg_n in range(-1, 11):
            effective = max(deg_w, deg_n - k)
            actual = max(deg_w, deg_n - (k - 1))
            require(effective <= actual <= effective + 1, "shift gap")
            shift_checks += 1

    p = 7
    domain = tuple(range(6))
    toy_k = 3
    records = 0
    actual_records = []
    for support in itertools.combinations(domain, 4):
        count = 0
        for values in itertools.product(range(p), repeat=4):
            records += 1
            if degree(interpolate(support, values, p), p) < toy_k:
                count += 1
        require(count == p**toy_k, "toy exact-support dimension")
        actual_records.append(count)
    require(records == 36015, "toy record total")
    return {
        "shift_formulas": {
            "code": "max(deg W,deg N-(k-1))",
            "effective": "max(deg W,deg N-k)",
            "maximum_gap": 1,
        },
        "official_row": {
            "n": n,
            "k": k,
            "effective_k": k + 1,
            "m": m,
            "omega": omega,
            "effective_numerator_degree_cap": omega + k,
            "actual_numerator_degree_cap": omega + k - 1,
        },
        "guards": {
            "quotient": "deg(N/W)<k",
            "numerator": "deg N<=omega+k-1",
            "code_shift": "s_k(W,N)<=omega",
            "pair_noncontainment": "at least one degree-below-m support interpolant has degree at least k",
        },
        "toy_exhaustion": {
            "field": p,
            "domain_size": len(domain),
            "k": toy_k,
            "m": 4,
            "supports": len(actual_records),
            "records": records,
            "actual_records_per_support": p**toy_k,
            "shift_checks": shift_checks,
        },
    }


def typed_pole_line() -> dict[str, Any]:
    p = 2130706433
    modulus = [6, 1, 0, 0, 0, 0, 1]
    x = [0, 1]
    require(pow_x(p**6, modulus, p) == x, "extension closure")
    for exponent in (p**2, p**3):
        difference = add(pow_x(exponent, modulus, p), [0, -1], p)
        require(gcd(modulus, difference, p) == [1], "extension irreducibility")

    n, k, effective_k, m, e = 2097152, 1048576, 1048577, 1116048, 67473
    omega = n - m
    off_error = n - e
    actual_n_degree = k + e - 2
    effective_n_degree = k + e - 1
    require(off_error > effective_n_degree > actual_n_degree, "minimum root margin")
    require(m > effective_k and e + m < n, "typed support")
    require(e == m - k + 1 == m - effective_k + 2, "profile ledger")
    return {
        "id": "KB_SPARSE_BOUNDARY_ACTUAL_RECORD_V1",
        "extension_modulus_low_to_high": modulus,
        "error_prefix_size": e,
        "support_start": e,
        "support_end_exclusive": e + m,
        "slope": "alpha",
        "r0": "indicator_E + alpha/(x-alpha)",
        "r1": "-1/(x-alpha)",
        "slope_word": "indicator_E",
        "explanation": "0",
        "guarded_quotient_degree": -1,
        "d1_code_shift": e,
        "d1_effective_shift": e,
        "actual_root_margin": m - k,
        "effective_root_margin": m - effective_k,
        "frozen_Q_owner": "UNASSIGNED",
        "frozen_BC_owner": "UNASSIGNED",
        "frozen_U_new_owner": "UNASSIGNED",
    }


def build() -> dict[str, Any]:
    return {
        "schema": "kb-mca-dense-core-owner-substrate-v1",
        "exact_parent": PARENT,
        "source_prize_dag": {
            "repository": "AllenGrahamHart/rs-mca-prize-dag",
            "nodes": SOURCE_NODES,
        },
        "upstream_source_pins": {
            "pr1159_head": "e603e0cedc5220ec2f29bd53836e732e3ec14934",
            "pr1160_head": "c5f4ea7a0c78828c901ae5f3428894a8b2e2806b",
            "pr1163_head": "e26c15b2d2c2f98ae12dda17b97c40981f76e1ff",
        },
        "reserve_repricing": {
            "exception_cap": 31,
            "owner_target": "B*-(2w+31)-(n-g)",
            "rows": reserve_rows(),
        },
        "unguarded_transport_counterexample": field_and_transport(),
        "guarded_lattice_adapter": guarded_adapter(),
        "typed_pole_line_witness": typed_pole_line(),
        "dense_core_bridge": {
            "source": "PR #1168 rank-eleven pair-core terminal",
            "core_deficiency_at_most": 4,
            "owned_slopes_at_least": 200632,
            "requirements": [
                "separate 2w and 31 first-match charges",
                "repriced large-owner target when the S/A/E assembly is reused",
                "degree-below-k quotient guard",
                "same-support pair-noncontainment test",
                "actual-line and owner-chronology preservation",
                "typed pole-line acceptance and unguarded-transport rejection",
            ],
        },
        "claims": {
            "witness_adapter_sound": True,
            "reserve_arithmetic_viable": True,
            "dense_core_owner_theorem": False,
            "rank11_paid": False,
            "active_v4_ledger_movement": 0,
            "KoalaBear_closed": False,
        },
        "packet_files": PACKET_FILES,
        "packet_file_sha256": {
            path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            for path in PACKET_FILES
        },
    }


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def payload(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical(unsigned)).hexdigest()


def validate(value: dict[str, Any], expected: dict[str, Any]) -> None:
    require(value == expected, "canonical certificate")
    require(value["payload_sha256"] == payload(value), "payload hash")


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations = (
        lambda item: item["reserve_repricing"]["rows"][0].__setitem__("target_full", 0),
        lambda item: item["reserve_repricing"].__setitem__("exception_cap", 30),
        lambda item: item["unguarded_transport_counterexample"].__setitem__("in_code_k", True),
        lambda item: item["guarded_lattice_adapter"]["official_row"].__setitem__(
            "actual_numerator_degree_cap", 2029680
        ),
        lambda item: item["typed_pole_line_witness"].__setitem__("frozen_BC_owner", "BC"),
        lambda item: item["dense_core_bridge"].__setitem__("owned_slopes_at_least", 200631),
        lambda item: item["claims"].__setitem__("rank11_paid", True),
        lambda item: item["source_prize_dag"]["nodes"]["guarded_lattice_adapter"].__setitem__(
            "commit", "0" * 40
        ),
    )
    caught = 0
    for mutate in mutations:
        changed = copy.deepcopy(expected)
        mutate(changed)
        changed["payload_sha256"] = payload(changed)
        try:
            validate(changed, expected)
        except Reject:
            caught += 1
    require(caught == len(mutations), "all hostile mutations caught")
    return caught


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    expected = build()
    expected["payload_sha256"] = payload(expected)
    if args.write:
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(expected, indent=2) + "\n")
        print(f"WROTE {MANIFEST}")
        return
    actual = json.loads(MANIFEST.read_text())
    validate(actual, expected)
    if args.tamper_selftest:
        caught = tamper_selftest(expected)
        print(f"KB_MCA_DENSE_CORE_OWNER_SUBSTRATE_TAMPER_PASS mutations={caught}/8")
        return
    koala, mersenne = expected["reserve_repricing"]["rows"]
    adapter = expected["guarded_lattice_adapter"]["toy_exhaustion"]
    print(
        "KB_MCA_DENSE_CORE_OWNER_SUBSTRATE_PASS "
        f"targets={koala['target_full']},{mersenne['target_full']} "
        f"toy_records={adapter['records']} d1={expected['typed_pole_line_witness']['d1_code_shift']} "
        "owner=UNASSIGNED"
    )


if __name__ == "__main__":
    main()
