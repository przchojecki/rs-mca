#!/usr/bin/env python3
"""Verify an explicit line-value lift of the F_17^32 M3 top-window packet.

The regular-minor extractor consumes syndrome pencils.  Paper D starts from
line values f,g:D -> F and then applies the weighted RS syndrome map.  For the
order-512 subgroup H, this script uses the inverse Fourier section

    y(x) = sum_m s_m x^(-m-1)

to lift the fixed top-window synthetic syndrome pencil back to explicit values
on all 512 domain points, then checks that Syn(y)=s.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (  # noqa: E402
    Field,
    K,
    MODULUS,
    N,
    P,
)


SCHEMA_VERSION = "f17-32-m3-line-value-lift-v1"
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
FIXED_INPUT_REF = (
    "experimental/data/hankel-regular-minor-inputs/"
    "f17_32_n512_k256_a421_426_fixed_prefix92_input.json"
)
FIXED_PACKET_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/"
    "f17_32_n512_k256_a421_426_fixed_prefix92_packet.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-line-value-lift/"
    "f17_32_n512_k256_a421_426_fixed_prefix92_line_values.json"
)


def add(field: Field, left: Any, right: Any) -> tuple[int, ...]:
    a = field.normalize(left)
    b = field.normalize(right)
    return tuple((a[index] + b[index]) % field.p for index in range(field.degree))


def load_json(ref: str | Path) -> dict[str, Any]:
    path = Path(ref)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return json.loads(path.read_text(encoding="utf-8"))


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def hash_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def sha256_file(ref: str) -> str:
    return sha256((REPO_ROOT / ref).read_bytes()).hexdigest()


def scalar_inv(field: Field, value: int) -> tuple[int, ...]:
    return field.pow(field.normalize(value), field.size - 2)


def subgroup_dual_weights(field: Field, domain: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    inv_order = scalar_inv(field, len(domain))
    weights = [field.mul(point, inv_order) for point in domain]
    for point, weight in zip(domain, weights):
        derivative = field.mul(field.normalize(len(domain)), field.pow(point, len(domain) - 1))
        if field.mul(weight, derivative) != field.one:
            raise AssertionError("subgroup dual-weight formula failed")
    return weights


def anti_code_values(
    field: Field,
    domain: list[tuple[int, ...]],
    syndrome: list[tuple[int, ...]],
) -> list[tuple[int, ...]]:
    values = []
    for point in domain:
        inverse = field.pow(point, N - 1)
        power = inverse
        total = field.zero
        for moment in syndrome:
            total = add(field, total, field.mul(moment, power))
            power = field.mul(power, inverse)
        values.append(total)
    return values


def syndrome_from_values(
    field: Field,
    domain: list[tuple[int, ...]],
    weights: list[tuple[int, ...]],
    values: list[tuple[int, ...]],
    length: int,
) -> list[tuple[int, ...]]:
    powers = [field.one for _ in domain]
    out = []
    for _ in range(length):
        total = field.zero
        for point_power, weight, value in zip(powers, weights, values):
            total = add(field, total, field.mul(field.mul(weight, point_power), value))
        out.append(total)
        powers = [field.mul(power, point) for power, point in zip(powers, domain)]
    return out


def encoded(values: list[tuple[int, ...]], field: Field) -> list[int]:
    return [field.encode(value) for value in values]


def check_all_pass(checks: list[dict[str, Any]]) -> None:
    failures = [check["name"] for check in checks if check["status"] != "PASS"]
    if failures:
        raise AssertionError(f"line-value lift checks failed: {failures}")


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    extractor_input = load_json(FIXED_INPUT_REF)
    packet = load_json(FIXED_PACKET_REF)
    field = Field(P, MODULUS)
    domain = [field.decode(value) for value in descriptor["domain"]["domain_encodings"]]
    weights = subgroup_dual_weights(field, domain)
    syndrome_encoding = extractor_input["line_syndrome"]["field_encoding"]
    if syndrome_encoding != "base-p low-to-high integer":
        raise AssertionError("unexpected syndrome encoding")
    u_syndrome = [field.decode(value) for value in extractor_input["line_syndrome"]["u"]]
    v_syndrome = [field.decode(value) for value in extractor_input["line_syndrome"]["v"]]
    f_values = anti_code_values(field, domain, u_syndrome)
    g_values = anti_code_values(field, domain, v_syndrome)
    replay_u = syndrome_from_values(
        field,
        domain,
        weights,
        f_values,
        extractor_input["line_syndrome"]["length"],
    )
    replay_v = syndrome_from_values(
        field,
        domain,
        weights,
        g_values,
        extractor_input["line_syndrome"]["length"],
    )
    encoded_f = encoded(f_values, field)
    encoded_g = encoded(g_values, field)
    checks = [
        {
            "name": "row_descriptor_matches_input",
            "status": "PASS"
            if descriptor["row"]["domain_hash"] == extractor_input["row"]["domain_hash"]
            else "FAIL",
        },
        {
            "name": "domain_weight_formula",
            "status": "PASS",
            "detail": "lambda_x = x / 512 for H = roots of X^512 - 1",
        },
        {
            "name": "u_syndrome_replay",
            "status": "PASS" if replay_u == u_syndrome else "FAIL",
            "replayed_hash": hash_json(encoded(replay_u, field)),
            "target_hash": hash_json(extractor_input["line_syndrome"]["u"]),
        },
        {
            "name": "v_syndrome_replay",
            "status": "PASS" if replay_v == v_syndrome else "FAIL",
            "replayed_hash": hash_json(encoded(replay_v, field)),
            "target_hash": hash_json(extractor_input["line_syndrome"]["v"]),
        },
        {
            "name": "fixed_packet_uses_input",
            "status": "PASS"
            if packet["extractor"]["input_sha256"] == sha256_file(FIXED_INPUT_REF)
            else "FAIL",
        },
        {
            "name": "fixed_packet_root_union",
            "status": "PASS"
            if packet.get("root_union") == [0]
            and packet.get("declared_aperiodic_numerator") == 1
            else "FAIL",
        },
    ]
    check_all_pass(checks)
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": {
            "field": "F_17^32",
            "n": N,
            "k": K,
            "domain_hash": descriptor["row"]["domain_hash"],
            "row_descriptor_ref": ROW_DESCRIPTOR_REF,
            "row_descriptor_sha256": sha256_file(ROW_DESCRIPTOR_REF),
        },
        "source_packet": {
            "fixed_top_window_input_ref": FIXED_INPUT_REF,
            "fixed_top_window_input_sha256": sha256_file(FIXED_INPUT_REF),
            "fixed_top_window_packet_ref": FIXED_PACKET_REF,
            "fixed_top_window_packet_sha256": sha256_file(FIXED_PACKET_REF),
        },
        "construction": {
            "syndrome_map": "Syn(y)_m = sum_x lambda_x x^m y(x)",
            "dual_weight_formula": "lambda_x = x / 512 on the order-512 subgroup",
            "inverse_fourier_section": "y(x) = sum_{0<=m<256} Syn(y)_m x^(-m-1)",
            "reason": (
                "Since sum_{x in H} x^a is 512 for a=0 mod 512 and 0 otherwise, "
                "this section replays the first 256 syndrome moments exactly."
            ),
        },
        "line_values": {
            "field_encoding": "base-p low-to-high integer",
            "length": len(domain),
            "f": encoded_f,
            "g": encoded_g,
            "f_hash": hash_json(encoded_f),
            "g_hash": hash_json(encoded_g),
        },
        "syndrome_replay": {
            "length": extractor_input["line_syndrome"]["length"],
            "u_hash": hash_json(extractor_input["line_syndrome"]["u"]),
            "v_hash": hash_json(extractor_input["line_syndrome"]["v"]),
            "matches_fixed_top_window_input": True,
        },
        "checks": checks,
        "nonclaims": [
            "does not prove a worst-case MCA bound",
            "does not make the synthetic top-window line a tangent/quotient-deduped row",
            "does not supply actual-row root tables for the whole 385..426 window",
            "does not classify singular pivot buckets",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"line-value lift mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    row = certificate["row"]
    print("F_17^32 M3 line-value lift")
    print("row: field={field}, n={n}, k={k}".format(**row))
    print("line_values={length}, syndrome_length={syndrome_length}".format(
        length=certificate["line_values"]["length"],
        syndrome_length=certificate["syndrome_replay"]["length"],
    ))
    print("matches_fixed_top_window_input=True")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic lift JSON")
    parser.add_argument("--check", type=Path, help="check deterministic lift JSON")
    parser.add_argument("--json", action="store_true", help="print lift JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
