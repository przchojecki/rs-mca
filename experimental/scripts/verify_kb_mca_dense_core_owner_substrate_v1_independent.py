#!/usr/bin/env python3
"""Independent replay of the KoalaBear dense-core owner substrate."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-dense-core-owner-substrate-v1/manifest.json"


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def payload(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical(unsigned)).hexdigest()


def poly_trim(poly: list[int], p: int) -> list[int]:
    out = [coefficient % p for coefficient in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_mul(left: list[int], right: list[int], p: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = (out[i + j] + a * b) % p
    return poly_trim(out, p)


def poly_rem(left: list[int], modulus: list[int], p: int) -> list[int]:
    out = poly_trim(left, p)
    inverse = pow(modulus[-1], -1, p)
    while out != [0] and len(out) >= len(modulus):
        coefficient = out[-1] * inverse % p
        shift = len(out) - len(modulus)
        for index, value in enumerate(modulus):
            out[index + shift] = (out[index + shift] - coefficient * value) % p
        out = poly_trim(out, p)
    return out


def poly_gcd(left: list[int], right: list[int], p: int) -> list[int]:
    a, b = poly_trim(left, p), poly_trim(right, p)
    while b != [0]:
        a, b = b, poly_rem(a, b, p)
    inverse = pow(a[-1], -1, p)
    return poly_trim([inverse * value for value in a], p)


def frobenius(poly: list[int], modulus: list[int], p: int) -> list[int]:
    result = [1]
    base = poly[:]
    exponent = p
    while exponent:
        if exponent & 1:
            result = poly_rem(poly_mul(result, base, p), modulus, p)
        base = poly_rem(poly_mul(base, base, p), modulus, p)
        exponent >>= 1
    return result


def evaluate(poly: tuple[int, ...], x: int, p: int) -> int:
    value = 0
    for coefficient in reversed(poly):
        value = (value * x + coefficient) % p
    return value


def check_packet(value: dict[str, Any]) -> None:
    require(value.get("schema") == "kb-mca-dense-core-owner-substrate-v1", "schema")
    require(
        value.get("exact_parent") == "6a5dcdae1591fc7f044eda6a942bfe178521a48c",
        "parent",
    )
    require(value.get("payload_sha256") == payload(value), "payload")
    files = value.get("packet_files")
    hashes = value.get("packet_file_sha256")
    require(isinstance(files, list) and isinstance(hashes, dict), "packet index")
    require(set(files) == set(hashes), "packet hash domain")
    for path in files:
        require(
            hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == hashes[path],
            f"packet drift: {path}",
        )

    nodes = value.get("source_prize_dag", {}).get("nodes", {})
    expected_nodes = {
        "reserve_repricing": (
            "2607c6fa7957eac4883547f9af3bbcaf9495e572",
            "f64dcacc0bb3b7a94a2fba1e3713f0172a7e3e5d",
            "background/nodes/rate_half_mca_two_anchor_reserve_repricing",
        ),
        "unguarded_transport_counterexample": (
            "80d430a681ee1f823ec1941e8a57a204a73843a0",
            "05070eb518cd275cf194d55357f99c45c1cce464",
            "background/nodes/rate_half_mca_kplus1_badness_transport_counterexample",
        ),
        "guarded_lattice_adapter": (
            "3f626c84d1f6d76fff77a26e7d3d1586ebc869f8",
            "ba43f74f8deb085889b8d5d5c6d605436f7bafc5",
            "background/nodes/rate_half_mca_degree_guarded_shifted_lattice_witness_adapter",
        ),
        "typed_pole_line_witness": (
            "d888aff329548ad92691e5f6c192ba037da13cc6",
            "e035a3feb580244957e2c258191c401714426395",
            "background/nodes/rate_half_mca_pole_line_typed_witness_certificate",
        ),
    }
    require(set(nodes) == set(expected_nodes), "source node set")
    for name, (commit, tree, path) in expected_nodes.items():
        require(nodes[name].get("commit") == commit, f"source commit: {name}")
        require(nodes[name].get("tree") == tree, f"source tree: {name}")
        require(nodes[name].get("path") == path, f"source path: {name}")


def check_reserve(value: dict[str, Any]) -> None:
    reserve = value.get("reserve_repricing")
    require(isinstance(reserve, dict) and reserve.get("exception_cap") == 31, "reserve")
    rows = reserve.get("rows")
    require(isinstance(rows, list) and len(rows) == 2, "reserve rows")
    fixed_rows = (
        ("KoalaBear MCA", 2097152, 1048576, 1116048, 274980728111395087, 57198030366),
        ("Mersenne-31 MCA stress row", 2097152, 1048576, 1116024, 16777215, 1752700),
    )
    for row, fixed in zip(rows, fixed_rows):
        name, n, k, m, budget, average = fixed
        require(
            tuple(row.get(key) for key in ("name", "n", "K", "m", "budget", "average_ceiling"))
            == fixed,
            f"fixed reserve row: {name}",
        )
        w = m - k
        combined = 2 * w + 31
        g_min = 2 * m - k + 1
        target_min = budget - combined - (n - g_min)
        target_full = budget - combined
        quotient, remainder = divmod(target_full, average)
        require(
            tuple(
                row.get(key)
                for key in (
                    "w",
                    "two_w",
                    "combined_reserve",
                    "g_min",
                    "target_g_min",
                    "target_full",
                    "full_average_quotient",
                    "full_average_remainder",
                )
            )
            == (w, 2 * w, combined, g_min, target_min, target_full, quotient, remainder),
            f"reserve arithmetic: {name}",
        )
        require(2 * w > 31 and combined + n < budget, f"reserve margins: {name}")
        for g in (g_min, (g_min + n) // 2, n):
            target = target_min + g - g_min
            require(2 * w + 31 + n - g + target == budget, "affine owner identity")


def check_transport_and_adapter(value: dict[str, Any]) -> None:
    record = value.get("unguarded_transport_counterexample")
    require(isinstance(record, dict), "transport record")
    fixed = (2130706433, 2097152, 1048576, 1116048, 1213133211, 67473, 0)
    require(
        tuple(record.get(key) for key in ("p", "n", "k", "m", "zeta", "error_prefix_size", "slope"))
        == fixed,
        "transport constants",
    )
    p, n, k, m, zeta, e, _ = fixed
    require(p - 1 == 127 * 2**24, "base factorization")
    require(pow(zeta, n, p) == 1 and pow(zeta, n // 2, p) == p - 1, "subgroup")
    require(e + m == record.get("support_end_exclusive") < n, "support interval")
    require(
        record.get("direction_degree") == k
        and record.get("in_code_k") is False
        and record.get("in_code_kplus1") is True
        and record.get("root_surplus") == m - k > 0,
        "dimension mutation",
    )

    adapter = value.get("guarded_lattice_adapter")
    require(isinstance(adapter, dict), "adapter")
    row = adapter.get("official_row")
    guards = adapter.get("guards")
    require(isinstance(row, dict) and isinstance(guards, dict), "adapter records")
    omega = n - m
    require(
        tuple(
            row.get(key)
            for key in (
                "n",
                "k",
                "effective_k",
                "m",
                "omega",
                "effective_numerator_degree_cap",
                "actual_numerator_degree_cap",
            )
        )
        == (n, k, k + 1, m, omega, omega + k, omega + k - 1),
        "one-coefficient guard",
    )
    require(guards.get("quotient") == "deg(N/W)<k", "quotient guard")

    # Independent same-support controls over GF(7).
    toy_k = 3
    support = (1, 2, 3, 4)
    u = (0, 0, 0, 1)
    v = (0, 0, 0, -1)
    require(
        all((evaluate(u, x, 7) + evaluate(v, x, 7)) % 7 == 0 for x in support),
        "explained slope word",
    )
    require(len(u) - 1 >= toy_k and len(v) - 1 >= toy_k, "pair noncontainment")
    require(len((1, 2, 1)) - 1 < toy_k and len((3, 1)) - 1 < toy_k, "contained control")


def check_typed_witness(value: dict[str, Any]) -> None:
    witness = value.get("typed_pole_line_witness")
    require(isinstance(witness, dict), "typed witness")
    p = 2130706433
    modulus = witness.get("extension_modulus_low_to_high")
    require(modulus == [6, 1, 0, 0, 0, 0, 1], "extension modulus")
    x = [0, 1]
    powers = {0: x}
    current = x
    for index in range(1, 7):
        current = frobenius(current, modulus, p)
        powers[index] = current
    require(powers[6] == x, "extension closure")
    for index in (2, 3):
        delta = powers[index][:]
        if len(delta) < 2:
            delta += [0] * (2 - len(delta))
        delta[1] = (delta[1] - 1) % p
        require(poly_gcd(modulus, delta, p) == [1], "proper extension factor")

    n, k, effective_k, m, e = 2097152, 1048576, 1048577, 1116048, 67473
    require(witness.get("id") == "KB_SPARSE_BOUNDARY_ACTUAL_RECORD_V1", "record id")
    require(
        witness.get("error_prefix_size") == e
        and witness.get("support_start") == e
        and witness.get("support_end_exclusive") == e + m < n,
        "typed support",
    )
    require(witness.get("guarded_quotient_degree") == -1, "zero quotient")
    require(
        witness.get("d1_code_shift") == witness.get("d1_effective_shift") == e,
        "shifted minima",
    )
    require(n - e > k + e - 1 and m > effective_k, "root-count margins")
    require(
        witness.get("actual_root_margin") == m - k == 67472
        and witness.get("effective_root_margin") == m - effective_k == 67471,
        "typed root margins",
    )
    require(
        all(witness.get(key) == "UNASSIGNED" for key in ("frozen_Q_owner", "frozen_BC_owner", "frozen_U_new_owner")),
        "owner nonclaim",
    )


def check_bridge(value: dict[str, Any]) -> None:
    bridge = value.get("dense_core_bridge")
    claims = value.get("claims")
    require(isinstance(bridge, dict) and isinstance(claims, dict), "bridge records")
    require(
        bridge.get("core_deficiency_at_most") == 4
        and bridge.get("owned_slopes_at_least") == 200632,
        "#1168 terminal",
    )
    requirements = bridge.get("requirements")
    require(isinstance(requirements, list) and len(requirements) == 6, "bridge obligations")
    require(claims.get("witness_adapter_sound") is True, "adapter claim")
    require(claims.get("reserve_arithmetic_viable") is True, "reserve claim")
    require(claims.get("dense_core_owner_theorem") is False, "owner nonclaim")
    require(claims.get("rank11_paid") is False, "rank-11 nonclaim")
    require(claims.get("active_v4_ledger_movement") == 0, "ledger nonclaim")
    require(claims.get("KoalaBear_closed") is False, "closure nonclaim")


def check(value: dict[str, Any]) -> None:
    check_packet(value)
    check_reserve(value)
    check_transport_and_adapter(value)
    check_typed_witness(value)
    check_bridge(value)


def main() -> None:
    value = json.loads(MANIFEST.read_text())
    check(value)
    controls = []
    mutations = (
        lambda item: item["reserve_repricing"]["rows"][0].__setitem__("target_full", 1),
        lambda item: item["guarded_lattice_adapter"]["official_row"].__setitem__(
            "actual_numerator_degree_cap", 2029680
        ),
        lambda item: item["typed_pole_line_witness"].__setitem__("frozen_Q_owner", "Q"),
        lambda item: item["dense_core_bridge"].__setitem__("core_deficiency_at_most", 5),
    )
    for mutate in mutations:
        altered = copy.deepcopy(value)
        mutate(altered)
        altered["payload_sha256"] = payload(altered)
        try:
            check(altered)
        except Reject:
            controls.append(True)
        else:
            controls.append(False)
    require(all(controls), "independent mutations")
    print(
        "KB_MCA_DENSE_CORE_OWNER_SUBSTRATE_INDEPENDENT_PASS "
        f"checks=packet,reserve,transport,adapter,pole,bridge controls={sum(controls)}/4"
    )


if __name__ == "__main__":
    main()
