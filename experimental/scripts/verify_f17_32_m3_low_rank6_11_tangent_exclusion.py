#!/usr/bin/env python3
"""Verify tangent/common-code-line exclusion for M3 low-rank ranks 6..11.

This audit consumes the exact finite-root certificates for the nested
low-rank families at ranks 6, 7, 8 and the compact rank-9..11 sweep.  It then
checks the unique possible common-code-line slope from moment zero:

    Syn_0(u+zv) = |X| + s z.

Because s is nonzero in characteristic 17 for 6 <= s <= 11, the only possible
common-code-line slope is z=-|X|/s.  If the regular-minor polynomial Delta_s
is nonzero at that slope, none of its finite roots can be paid by the
tangent/common-code-line ledger.  This is a targeted M4-style subtraction
audit for the synthetic low-rank slack families, not a quotient audit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.extract_regular_hankel_minors import (
    PolynomialBasisField,
    fpoly_degree,
    fpoly_eval,
    hash_json,
    render,
)
from experimental.scripts.verify_f17_32_m3_low_rank9_11_slack_sweep import (
    AGREEMENT_MAX,
    AGREEMENT_MIN,
    K,
    N,
    ROW_DESCRIPTOR,
    TWO128,
    low_rank_coefficients_from_basis_values,
    update_basis_values,
)


SCHEMA_VERSION = "f17-32-m3-low-rank6-11-tangent-exclusion-v1"
RANKS = [6, 7, 8, 9, 10, 11]
MAX_RANK = max(RANKS)
LOW_RANK6_REF = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-slack-family/"
    "f17_32_n512_k256_m3_low_rank6_slack_family_certificate.json"
)
LOW_RANK7_REF = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank7-slack-family/"
    "f17_32_n512_k256_m3_low_rank7_slack_family_certificate.json"
)
LOW_RANK8_REF = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank8-slack-family/"
    "f17_32_n512_k256_m3_low_rank8_slack_family_certificate.json"
)
LOW_RANK9_11_REF = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank9-11-slack-sweep/"
    "f17_32_n512_k256_m3_low_rank9_11_slack_sweep_certificate.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-tangent-exclusion/"
    "f17_32_n512_k256_m3_low_rank6_11_tangent_exclusion_certificate.json"
)

EXPECTED_ROOT_SUMS = {6: 35, 7: 43, 8: 34, 9: 35, 10: 47, 11: 44}
EXPECTED_ROOT_HISTOGRAMS = {
    6: {"0": 16, "1": 17, "2": 9},
    7: {"0": 16, "1": 15, "2": 6, "3": 4, "4": 1},
    8: {"0": 22, "1": 10, "2": 7, "3": 2, "4": 1},
    9: {"0": 17, "1": 17, "2": 6, "3": 2},
    10: {"0": 8, "1": 23, "2": 9, "3": 2},
    11: {"0": 15, "1": 16, "2": 5, "3": 6},
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def source_artifacts() -> dict[int, tuple[Path, dict[str, Any]]]:
    artifacts = {
        6: (LOW_RANK6_REF, load_json(LOW_RANK6_REF)),
        7: (LOW_RANK7_REF, load_json(LOW_RANK7_REF)),
        8: (LOW_RANK8_REF, load_json(LOW_RANK8_REF)),
    }
    sweep = load_json(LOW_RANK9_11_REF)
    artifacts[9] = (LOW_RANK9_11_REF, sweep)
    artifacts[10] = (LOW_RANK9_11_REF, sweep)
    artifacts[11] = (LOW_RANK9_11_REF, sweep)
    return artifacts


def validate_source_artifacts(artifacts: dict[int, tuple[Path, dict[str, Any]]]) -> None:
    expected_schemas = {
        6: "f17-32-m3-low-rank6-slack-family-v1",
        7: "f17-32-m3-low-rank7-slack-family-v1",
        8: "f17-32-m3-low-rank8-slack-family-v1",
        9: "f17-32-m3-low-rank9-11-slack-sweep-v1",
        10: "f17-32-m3-low-rank9-11-slack-sweep-v1",
        11: "f17-32-m3-low-rank9-11-slack-sweep-v1",
    }
    for rank, (_path, artifact) in artifacts.items():
        require(
            artifact["schema_version"] == expected_schemas[rank],
            f"rank={rank}: source schema mismatch",
        )
        require(
            artifact["agreement_range"] == [AGREEMENT_MIN, AGREEMENT_MAX],
            f"rank={rank}: source window mismatch",
        )
    for rank in [6, 7, 8]:
        aggregate = artifacts[rank][1]["aggregate"]
        require(
            aggregate["exact_regular_root_count_sum"] == EXPECTED_ROOT_SUMS[rank],
            f"rank={rank}: source root sum mismatch",
        )
        require(
            aggregate["linear_root_count_histogram"]
            == EXPECTED_ROOT_HISTOGRAMS[rank],
            f"rank={rank}: source root histogram mismatch",
        )
    sweep_summaries = artifacts[9][1]["aggregate"]["rank_summaries"]
    for rank in [9, 10, 11]:
        summary = sweep_summaries[str(rank)]
        require(
            summary["exact_regular_root_count_sum"] == EXPECTED_ROOT_SUMS[rank],
            f"rank={rank}: source sweep root sum mismatch",
        )
        require(
            summary["linear_root_count_histogram"]
            == EXPECTED_ROOT_HISTOGRAMS[rank],
            f"rank={rank}: source sweep root histogram mismatch",
        )


def source_root_counts(
    artifacts: dict[int, tuple[Path, dict[str, Any]]]
) -> dict[tuple[int, int], dict[str, Any]]:
    counts: dict[tuple[int, int], dict[str, Any]] = {}
    for rank in [6, 7, 8]:
        for record in artifacts[rank][1]["records"]:
            counts[(rank, int(record["A"]))] = {
                "root_count": int(record["root_count"]),
                "root_count_hash": record["root_count_hash"],
                "source_ref": str(artifacts[rank][0].relative_to(REPO_ROOT)),
            }
    sweep_ref = str(LOW_RANK9_11_REF.relative_to(REPO_ROOT))
    for record in artifacts[9][1]["records"]:
        rank = int(record["rank"])
        counts[(rank, int(record["A"]))] = {
            "root_count": int(record["root_count"]),
            "root_count_hash": record["root_count_hash"],
            "source_ref": sweep_ref,
        }
    require(
        len(counts) == len(RANKS) * (AGREEMENT_MAX - AGREEMENT_MIN + 1),
        "source root-count map size mismatch",
    )
    return counts


def build_records(
    field: PolynomialBasisField,
    domain: list[tuple[int, ...]],
    root_counts: dict[tuple[int, int], dict[str, Any]],
) -> list[dict[str, Any]]:
    records = []
    base_nodes: list[tuple[int, ...]] = []
    denominators: list[tuple[int, ...]] = []
    base_determinant = field.one

    for size in range(1, N - AGREEMENT_MIN + 2):
        new_node = domain[size - 1]
        new_denominator = field.one
        for old_node in base_nodes:
            new_denominator = field.mul(
                new_denominator, field.sub(new_node, old_node)
            )
        for index, old_node in enumerate(base_nodes):
            denominators[index] = field.mul(
                denominators[index], field.sub(old_node, new_node)
            )
        denominators.append(new_denominator)
        base_nodes.append(new_node)
        base_determinant = field.mul(
            base_determinant, field.mul(new_denominator, new_denominator)
        )

        agreement = N - size + 1
        if agreement < AGREEMENT_MIN or agreement > AGREEMENT_MAX:
            continue
        update_nodes = domain[size : size + MAX_RANK]
        basis_values_by_update = update_basis_values(
            field,
            base_nodes,
            denominators,
            update_nodes,
        )
        u_zero_moment = field.normalize(size)
        for rank in RANKS:
            v_zero_moment = field.normalize(rank)
            require(
                not field.is_zero(v_zero_moment),
                f"A={agreement}, rank={rank}: moment-zero direction vanished",
            )
            common_code_line_slope = field.neg(
                field.div(u_zero_moment, v_zero_moment)
            )
            coefficients = low_rank_coefficients_from_basis_values(
                field,
                basis_values_by_update,
                base_determinant,
                rank,
            )
            require(
                fpoly_degree(coefficients, field) == rank,
                f"A={agreement}, rank={rank}: polynomial degree mismatch",
            )
            delta_at_common_slope = fpoly_eval(
                coefficients,
                common_code_line_slope,
                field,
            )
            require(
                not field.is_zero(delta_at_common_slope),
                f"A={agreement}, rank={rank}: tangent overlap found",
            )
            source_count = root_counts[(rank, agreement)]
            records.append(
                {
                    "rank": rank,
                    "A": agreement,
                    "j": N - agreement,
                    "t": agreement - K,
                    "prefix_row_set": [0, size - 1],
                    "base_node_count": size,
                    "degree_bound": rank,
                    "root_count_from_source": source_count["root_count"],
                    "root_count_hash_from_source": source_count["root_count_hash"],
                    "root_count_source_ref": source_count["source_ref"],
                    "moment_zero_audit": {
                        "method": "direct_delta_exclusion_at_unique_common_code_line_slope",
                        "witness_moment": 0,
                        "u_m_encoding": field.encode(u_zero_moment),
                        "v_m_encoding": field.encode(v_zero_moment),
                        "common_code_line_slope_encoding": field.encode(
                            common_code_line_slope
                        ),
                        "delta_at_common_code_line_slope_encoding": field.encode(
                            delta_at_common_slope
                        ),
                        "delta_at_common_code_line_slope_hash": hash_json(
                            field.encode(delta_at_common_slope)
                        ),
                        "coefficient_hash": hash_json(
                            [field.encode(coefficient) for coefficient in coefficients]
                        ),
                        "status": "not_common_code_line",
                    },
                    "tangent_common_code_line_audit": {
                        "finite_roots_checked": source_count["root_count"],
                        "overlap_count": 0,
                        "regular_roots_after_common_code_line": source_count[
                            "root_count"
                        ],
                    },
                }
            )
    return sorted(records, key=lambda record: (record["rank"], record["A"]))


def summarize_rank(records: list[dict[str, Any]], rank: int) -> dict[str, Any]:
    rank_records = [record for record in records if record["rank"] == rank]
    root_histogram = Counter(
        record["root_count_from_source"] for record in rank_records
    )
    finite_roots = sum(record["root_count_from_source"] for record in rank_records)
    require(finite_roots == EXPECTED_ROOT_SUMS[rank], f"rank={rank}: root sum mismatch")
    require(
        {str(key): root_histogram[key] for key in sorted(root_histogram)}
        == EXPECTED_ROOT_HISTOGRAMS[rank],
        f"rank={rank}: root histogram mismatch",
    )
    return {
        "rank": rank,
        "agreement_count": len(rank_records),
        "finite_roots_checked_for_common_code_line": finite_roots,
        "common_code_line_tangent_overlap_sum": 0,
        "regular_roots_after_common_code_line": finite_roots,
        "root_count_histogram": {
            str(key): root_histogram[key] for key in sorted(root_histogram)
        },
    }


def build_certificate() -> dict[str, Any]:
    artifacts = source_artifacts()
    validate_source_artifacts(artifacts)
    root_counts = source_root_counts(artifacts)
    descriptor = load_json(ROW_DESCRIPTOR)
    field = PolynomialBasisField.from_spec(
        {
            "kind": "polynomial_basis",
            "p": descriptor["field_model"]["p"],
            "modulus": descriptor["field_model"]["modulus"],
        }
    )
    domain = [field.decode(value) for value in descriptor["domain"]["domain_encodings"]]
    require(len(domain) == N, "descriptor domain length mismatch")
    records = build_records(field, domain, root_counts)
    rank_summaries = {str(rank): summarize_rank(records, rank) for rank in RANKS}
    total_checked = sum(
        summary["finite_roots_checked_for_common_code_line"]
        for summary in rank_summaries.values()
    )
    require(total_checked == sum(EXPECTED_ROOT_SUMS.values()), "total root sum mismatch")
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": {
            "n": N,
            "k": K,
            "field": descriptor["row"]["field"],
            "domain_hash": descriptor["row"]["domain_hash"],
            "domain_description": descriptor["row"]["domain_description"],
        },
        "source_artifacts": {
            "rank6_slack_family": {
                "ref": str(LOW_RANK6_REF.relative_to(REPO_ROOT)),
                "sha256": file_sha256(LOW_RANK6_REF),
            },
            "rank7_slack_family": {
                "ref": str(LOW_RANK7_REF.relative_to(REPO_ROOT)),
                "sha256": file_sha256(LOW_RANK7_REF),
            },
            "rank8_slack_family": {
                "ref": str(LOW_RANK8_REF.relative_to(REPO_ROOT)),
                "sha256": file_sha256(LOW_RANK8_REF),
            },
            "rank9_11_slack_sweep": {
                "ref": str(LOW_RANK9_11_REF.relative_to(REPO_ROOT)),
                "sha256": file_sha256(LOW_RANK9_11_REF),
            },
        },
        "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
        "construction": {
            "base_nodes": "first j+1 descriptor-domain elements",
            "update_nodes": "first s nodes after the base prefix",
            "ranks": RANKS,
            "certificate_mode": "low_rank_tangent_common_code_line_exclusion",
        },
        "method": {
            "moment_zero_identity": "Syn_0(u+zv)=|X|+s z",
            "unique_common_code_line_slope": "z=-|X|/s because 6<=s<=11 is nonzero in F_17",
            "exclusion_test": "Delta_s(-|X|/s) != 0 for every checked rank/agreement pair",
            "consequence": (
                "none of the finite roots counted by the source slack certificates "
                "is a tangent/common-code-line root"
            ),
        },
        "aggregate": {
            "rank_summaries": rank_summaries,
            "rank_count": len(RANKS),
            "record_count": len(records),
            "finite_roots_checked_for_common_code_line": total_checked,
            "common_code_line_tangent_overlap_sum": 0,
            "regular_roots_after_common_code_line": total_checked,
            "finite_budget_numerator": field.size // TWO128,
            "projective_budget_numerator": (field.size + 1) // TWO128,
        },
        "records": records,
        "nonclaims": [
            "synthetic syndrome-pencil family only",
            "not a quotient-image subtraction audit",
            "not a worst-case M3 row bound",
            "does not classify arbitrary non-proportional pencils",
        ],
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-6..11 tangent exclusion mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 low-rank-6..11 tangent/common-code-line exclusion")
    print(f"status: {certificate['status']}")
    print(
        "agreements: {lo}..{hi}, ranks={ranks}, records={count}".format(
            lo=certificate["agreement_range"][0],
            hi=certificate["agreement_range"][1],
            ranks=certificate["construction"]["ranks"],
            count=aggregate["record_count"],
        )
    )
    print(
        "finite roots checked={checked}, tangent overlap={overlap}, roots after tangent={after}".format(
            checked=aggregate["finite_roots_checked_for_common_code_line"],
            overlap=aggregate["common_code_line_tangent_overlap_sum"],
            after=aggregate["regular_roots_after_common_code_line"],
        )
    )
    for rank in certificate["construction"]["ranks"]:
        summary = aggregate["rank_summaries"][str(rank)]
        print(
            "rank {rank}: checked={checked}, overlap={overlap}, histogram={hist}".format(
                rank=rank,
                checked=summary["finite_roots_checked_for_common_code_line"],
                overlap=summary["common_code_line_tangent_overlap_sum"],
                hist=summary["root_count_histogram"],
            )
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic certificate")
    parser.add_argument("--check", type=Path, help="check deterministic certificate")
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(certificate, args.check)
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
