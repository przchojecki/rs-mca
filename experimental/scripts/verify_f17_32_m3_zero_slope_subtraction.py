#!/usr/bin/env python3
"""Verify zero-slope tangent subtraction for synthetic M3 rank-witness packets."""

from __future__ import annotations

import argparse
import importlib.util
import json
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-m3-zero-slope-subtraction-v1"
N = 512
K = 256
Q_LINE = 17**32
TARGET_BITS = 128
BUDGET = Q_LINE // 2**TARGET_BITS

SCHEMA_CHECKER = ROOT / "scripts/check_aperiodic_eliminant_packet.py"
SCHEMA = ROOT / "scripts/aperiodic_eliminant_schema.json"

OUTPUT_PATH = ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/"
    "f17_32_n512_k256_rank_witness_zero_slope_subtraction.json"
)

SOURCES = [
    {
        "packet_id": "rank_witness_a385",
        "input_ref": (
            "experimental/data/hankel-regular-minor-inputs/"
            "f17_32_n512_k256_a385_rank_witness_input.json"
        ),
        "packet_ref": (
            "experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/"
            "f17_32_n512_k256_a385_rank_witness_packet.json"
        ),
    },
    {
        "packet_id": "rank_witness_a426",
        "input_ref": (
            "experimental/data/hankel-regular-minor-inputs/"
            "f17_32_n512_k256_a426_rank_witness_input.json"
        ),
        "packet_ref": (
            "experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/"
            "f17_32_n512_k256_a426_rank_witness_packet.json"
        ),
    },
    {
        "packet_id": "fixed_top_window_a421_426",
        "input_ref": (
            "experimental/data/hankel-regular-minor-inputs/"
            "f17_32_n512_k256_a421_426_fixed_prefix92_input.json"
        ),
        "packet_ref": (
            "experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/"
            "f17_32_n512_k256_a421_426_fixed_prefix92_packet.json"
        ),
    },
]


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_schema_checker():
    spec = importlib.util.spec_from_file_location(
        "check_aperiodic_eliminant_packet", SCHEMA_CHECKER
    )
    require(spec is not None and spec.loader is not None, "could not load schema checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_refs() -> dict[str, dict[str, str]]:
    refs: dict[str, dict[str, str]] = {}
    for source in SOURCES:
        refs[source["packet_id"]] = {
            "input_ref": source["input_ref"],
            "input_sha256": sha256_file(source["input_ref"]),
            "packet_ref": source["packet_ref"],
            "packet_sha256": sha256_file(source["packet_ref"]),
        }
    return refs


def comparison(total: int) -> str:
    relation = "<=" if total <= BUDGET else ">"
    return f"{total} {relation} {BUDGET}"


def validate_packet_source(
    checker: Any,
    source: dict[str, str],
) -> dict[str, Any]:
    input_data = load_json(source["input_ref"])
    packet = load_json(source["packet_ref"])
    checker.check_path(ROOT / source["packet_ref"], SCHEMA)

    require(input_data["row"]["n"] == N, f"{source['packet_id']}: input n mismatch")
    require(input_data["row"]["k"] == K, f"{source['packet_id']}: input k mismatch")
    require(
        input_data["row"]["field"] == "F_17^32",
        f"{source['packet_id']}: input field mismatch",
    )
    require(packet["row"]["n"] == N, f"{source['packet_id']}: packet n mismatch")
    require(packet["row"]["k"] == K, f"{source['packet_id']}: packet k mismatch")
    require(
        packet["row"]["field"] == "F_17^32",
        f"{source['packet_id']}: packet field mismatch",
    )
    require(
        packet["row"]["domain_hash"] == input_data["row"]["domain_hash"],
        f"{source['packet_id']}: domain hash mismatch",
    )
    require(
        input_data["sampler"] == "finite_affine_line",
        f"{source['packet_id']}: input sampler mismatch",
    )
    require(
        packet["sampler"] == "finite_affine_line",
        f"{source['packet_id']}: packet sampler mismatch",
    )

    u_syndrome = input_data["line_syndrome"]["u"]
    require(
        len(u_syndrome) == N - K,
        f"{source['packet_id']}: unexpected u syndrome length",
    )
    require(
        all(value == 0 for value in u_syndrome),
        f"{source['packet_id']}: u syndrome is not identically zero",
    )
    require(
        input_data["exact_agreements"]
        == [item["A"] for item in packet["exact_agreements"]],
        f"{source['packet_id']}: exact agreement mismatch",
    )
    require(
        packet["root_union"] == [0],
        f"{source['packet_id']}: raw root union is not exactly {{0}}",
    )
    require(
        packet["declared_aperiodic_numerator"] == 1,
        f"{source['packet_id']}: raw numerator should be one",
    )
    require(
        packet["removed_ledgers"] == [],
        f"{source['packet_id']}: source packet should be raw before subtraction",
    )

    row_records = []
    for item in packet["exact_agreements"]:
        agreement = item["A"]
        degree = item["regular_minor"]["degree"]
        require(item["j"] == N - agreement, f"{source['packet_id']}: bad j at A={agreement}")
        require(item["t"] == agreement - K, f"{source['packet_id']}: bad t at A={agreement}")
        require(
            degree == item["j"] + 1,
            f"{source['packet_id']}: degree is not j+1 at A={agreement}",
        )
        minor_data = item["regular_minor_data"]
        require(
            minor_data["roots"] == [0],
            f"{source['packet_id']}: exact roots are not {{0}} at A={agreement}",
        )
        factors = minor_data["root_certificate"]["factors"]
        require(
            factors == [{"multiplicity": degree, "root": 0}],
            f"{source['packet_id']}: root factorization mismatch at A={agreement}",
        )
        require(
            minor_data["root_certificate"]["leading_coefficient"] != 0,
            f"{source['packet_id']}: zero leading coefficient at A={agreement}",
        )
        row_records.append(
            {
                "A": agreement,
                "j": item["j"],
                "t": item["t"],
                "B_tan": 1,
                "B_quot_support": 0,
                "B_quot_image": 0,
                "B_ap_regular_before_removed": 1,
                "B_ap_regular_after_tangent": 0,
                "B_ap_pivot": 0,
                "B_ext": 0,
                "deduped_total_upper_bound": 1,
                "budget": BUDGET,
                "comparison_to_budget": comparison(1),
                "paid_root": 0,
                "paid_root_label": "tangent_common_code_line_zero_slope",
                "residual_after_removed_ledgers": 0,
            }
        )

    return {
        "packet_id": source["packet_id"],
        "agreement_threshold": packet["agreement_threshold"],
        "exact_agreements": [row["A"] for row in row_records],
        "raw_root_union": [0],
        "tangent_paid_roots": [0],
        "residual_aperiodic_roots": [],
        "raw_declared_aperiodic_numerator": 1,
        "residual_aperiodic_numerator": 0,
        "deduped_total_upper_bound": 1,
        "budget": BUDGET,
        "comparison_to_budget": comparison(1),
        "rows": row_records,
    }


def build_certificate() -> dict[str, Any]:
    checker = load_schema_checker()
    packet_records = [validate_packet_source(checker, source) for source in SOURCES]
    domain_hashes = {
        load_json(source["packet_ref"])["row"]["domain_hash"] for source in SOURCES
    }
    require(len(domain_hashes) == 1, "source packets do not share one domain hash")
    require(BUDGET == 6, "unexpected q_line budget")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT for synthetic rank-witness packets",
        "object": "M4 tangent subtraction sidecar for M3 regular-window packets",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": sorted(domain_hashes)[0],
            "q_line": Q_LINE,
            "budget_formula": "floor(17^32 / 2^128)",
            "budget": BUDGET,
        },
        "source_artifacts": source_refs(),
        "proof_principle": {
            "finite_slope_coordinate": "Z",
            "paid_root": 0,
            "syndrome_identity": "Syn(f + Z g) = u + Z v",
            "checked_condition": "u_m = 0 for every stored syndrome coordinate",
            "conclusion": (
                "At Z=0 the line point has zero syndrome, so it is a "
                "codeword/common-code-line slope and is paid by the tangent ledger."
            ),
        },
        "packet_records": packet_records,
        "summary": {
            "packets_checked": len(packet_records),
            "exact_agreement_instances": sum(
                len(record["rows"]) for record in packet_records
            ),
            "raw_root_union_per_packet": [0],
            "paid_roots": [0],
            "max_residual_aperiodic_numerator": 0,
            "max_deduped_total_upper_bound": 1,
            "budget": BUDGET,
            "comparison_to_budget": comparison(1),
        },
        "nonclaims": [
            "synthetic rank-witness packets only",
            "not a worst-case support-wise MCA bound for the row",
            "not a quotient-support or quotient-image subtraction table",
            "not a singular-bucket or pivot-atlas certificate",
            "not a proof for arbitrary non-proportional M3 syndrome pencils",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"zero-slope subtraction certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 zero-slope subtraction sidecar")
    print(
        "packets={packets_checked}, exact-agreement instances={exact_agreement_instances}".format(
            **summary
        )
    )
    print(
        "paid roots={paid_roots}, max residual aperiodic numerator={max_residual_aperiodic_numerator}".format(
            **summary
        )
    )
    print(
        "synthetic total upper bound: {comparison_to_budget}".format(
            **summary
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    print_summary(certificate)


if __name__ == "__main__":
    main()
