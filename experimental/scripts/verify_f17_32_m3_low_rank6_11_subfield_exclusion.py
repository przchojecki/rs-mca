#!/usr/bin/env python3
"""Verify proper-subfield exclusion for M3 low-rank ranks 6..11.

This audit consumes the exact finite-root certificates for the nested
low-rank families at ranks 6, 7, 8 and the compact rank-9..11 sweep.  It then
checks whether any counted finite root lies in a proper subfield of
F_17^32.  Since the proper subfields are exactly F_17^d for
d in {1,2,4,8,16}, this is the Frobenius fixedness test

    z^(17^d) = z.

Listed roots are checked directly.  Count-only root-gcd rows are intersected
with Z^(17^d)-Z.  The rank-9..11 count-only rows only store compact hashes, so
the verifier reconstructs the corresponding compressed regular-minor
polynomial and checks the stored coefficient hash before running the same
subfield-gcd tests.
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
    fpoly_gcd,
    fpoly_trim,
    hash_json,
    render,
)
from experimental.scripts.verify_f17_32_m3_low_rank3_family import (
    monic_polynomial,
    multiply_mod_monic,
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


SCHEMA_VERSION = "f17-32-m3-low-rank6-11-subfield-exclusion-v1"
RANKS = [6, 7, 8, 9, 10, 11]
PROPER_SUBFIELD_DEGREES = [1, 2, 4, 8, 16]
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
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-subfield-exclusion/"
    "f17_32_n512_k256_m3_low_rank6_11_subfield_exclusion_certificate.json"
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


def source_root_records(
    artifacts: dict[int, tuple[Path, dict[str, Any]]]
) -> dict[tuple[int, int], dict[str, Any]]:
    records: dict[tuple[int, int], dict[str, Any]] = {}
    for rank in [6, 7, 8]:
        source_ref = str(artifacts[rank][0].relative_to(REPO_ROOT))
        for record in artifacts[rank][1]["records"]:
            records[(rank, int(record["A"]))] = {
                "rank": rank,
                "A": int(record["A"]),
                "root_count": int(record["root_count"]),
                "root_count_hash": record["root_count_hash"],
                "source_ref": source_ref,
                "listed_roots": record.get("listed_roots"),
                "listed_roots_status": record["linear_root_count_certificate"][
                    "listed_roots_status"
                ],
                "linear_root_gcd_coefficients": record[
                    "linear_root_count_certificate"
                ].get("linear_root_gcd_coefficients_ascending"),
            }
    sweep_ref = str(LOW_RANK9_11_REF.relative_to(REPO_ROOT))
    for record in artifacts[9][1]["records"]:
        rank = int(record["rank"])
        records[(rank, int(record["A"]))] = {
            "rank": rank,
            "A": int(record["A"]),
            "root_count": int(record["root_count"]),
            "root_count_hash": record["root_count_hash"],
            "source_ref": sweep_ref,
            "listed_roots": record.get("listed_roots"),
            "listed_roots_status": record["linear_root_count_certificate"][
                "listed_roots_status"
            ],
            "coefficient_hash": record["coefficient_hash"],
        }
    require(
        len(records) == len(RANKS) * (AGREEMENT_MAX - AGREEMENT_MIN + 1),
        "source root-record map size mismatch",
    )
    return records


def polynomial_power_mod_monic(
    base: list[tuple[int, ...]],
    exponent: int,
    modulus: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    result = [field.one]
    current = fpoly_trim(base, field)
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = multiply_mod_monic(result, current, modulus, field)
        remaining >>= 1
        if remaining:
            current = multiply_mod_monic(current, current, modulus, field)
    return fpoly_trim(result, field)


def proper_subfield_counts_from_polynomial(
    coefficients: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> dict[str, int]:
    if fpoly_degree(coefficients, field) <= 0:
        return {str(degree): 0 for degree in PROPER_SUBFIELD_DEGREES}
    monic = monic_polynomial(coefficients, field)
    current = [field.zero, field.one]
    requested = set(PROPER_SUBFIELD_DEGREES)
    counts: dict[str, int] = {}
    for degree in range(1, max(PROPER_SUBFIELD_DEGREES) + 1):
        current = polynomial_power_mod_monic(current, field.p, monic, field)
        if degree not in requested:
            continue
        remainder = list(current)
        if len(remainder) < 2:
            remainder += [field.zero] * (2 - len(remainder))
        remainder[1] = field.sub(remainder[1], field.one)
        remainder = fpoly_trim(remainder, field)
        counts[str(degree)] = fpoly_degree(fpoly_gcd(monic, remainder, field), field)
    return counts


def proper_subfield_counts_from_listed_roots(
    roots: list[int],
    field: PolynomialBasisField,
) -> dict[str, int]:
    counts = Counter({str(degree): 0 for degree in PROPER_SUBFIELD_DEGREES})
    requested = set(PROPER_SUBFIELD_DEGREES)
    for encoded_root in roots:
        root = field.decode(int(encoded_root))
        current = root
        for degree in range(1, max(PROPER_SUBFIELD_DEGREES) + 1):
            current = field.pow(current, field.p)
            if degree in requested and current == root:
                counts[str(degree)] += 1
    return {str(degree): counts[str(degree)] for degree in PROPER_SUBFIELD_DEGREES}


def reconstruct_coefficients_for_count_only_sweep_records(
    field: PolynomialBasisField,
    domain: list[tuple[int, ...]],
    source_records: dict[tuple[int, int], dict[str, Any]],
) -> dict[tuple[int, int], list[tuple[int, ...]]]:
    targets = {
        key: record
        for key, record in source_records.items()
        if key[0] in [9, 10, 11] and record["listed_roots_status"] == "count_only"
    }
    reconstructed: dict[tuple[int, int], list[tuple[int, ...]]] = {}
    if not targets:
        return reconstructed

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
        ranks_here = [rank for rank, item_a in targets if item_a == agreement]
        if not ranks_here:
            continue
        update_nodes = domain[size : size + max(ranks_here)]
        basis_values_by_update = update_basis_values(
            field,
            base_nodes,
            denominators,
            update_nodes,
        )
        for rank in ranks_here:
            coefficients = low_rank_coefficients_from_basis_values(
                field,
                basis_values_by_update,
                base_determinant,
                rank,
            )
            source = targets[(rank, agreement)]
            coefficient_hash = hash_json(
                [field.encode(coefficient) for coefficient in coefficients]
            )
            require(
                coefficient_hash == source["coefficient_hash"],
                f"A={agreement}, rank={rank}: coefficient hash mismatch",
            )
            reconstructed[(rank, agreement)] = coefficients

    require(
        set(reconstructed) == set(targets),
        "count-only rank-9..11 reconstruction coverage mismatch",
    )
    return reconstructed


def record_subfield_counts(
    record: dict[str, Any],
    field: PolynomialBasisField,
    reconstructed_coefficients: dict[tuple[int, int], list[tuple[int, ...]]],
) -> tuple[dict[str, int], str, str | None]:
    key = (record["rank"], record["A"])
    if record["listed_roots_status"] == "listed":
        listed_roots = record["listed_roots"] or []
        require(
            len(listed_roots) == record["root_count"],
            f"A={record['A']}, rank={record['rank']}: listed root count mismatch",
        )
        return (
            proper_subfield_counts_from_listed_roots(listed_roots, field),
            "listed_root_frobenius_fixedness",
            None,
        )

    if record.get("linear_root_gcd_coefficients") is not None:
        root_gcd = [
            field.decode(int(coefficient))
            for coefficient in record["linear_root_gcd_coefficients"]
        ]
        require(
            fpoly_degree(root_gcd, field) == record["root_count"],
            f"A={record['A']}, rank={record['rank']}: source root-gcd degree mismatch",
        )
        return (
            proper_subfield_counts_from_polynomial(root_gcd, field),
            "source_linear_root_gcd_intersection",
            hash_json([field.encode(coefficient) for coefficient in root_gcd]),
        )

    coefficients = reconstructed_coefficients[key]
    return (
        proper_subfield_counts_from_polynomial(coefficients, field),
        "reconstructed_delta_intersection",
        hash_json([field.encode(coefficient) for coefficient in coefficients]),
    )


def build_records(
    field: PolynomialBasisField,
    source_records: dict[tuple[int, int], dict[str, Any]],
    reconstructed_coefficients: dict[tuple[int, int], list[tuple[int, ...]]],
) -> list[dict[str, Any]]:
    records = []
    for rank in RANKS:
        for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1):
            source = source_records[(rank, agreement)]
            counts, method, witness_hash = record_subfield_counts(
                source,
                field,
                reconstructed_coefficients,
            )
            require(
                all(count == 0 for count in counts.values()),
                f"A={agreement}, rank={rank}: proper subfield root found",
            )
            base_node_count = N - agreement + 1
            audit: dict[str, Any] = {
                "method": method,
                "proper_subfield_degrees": PROPER_SUBFIELD_DEGREES,
                "proper_subfield_root_counts": counts,
                "proper_subfield_overlap_count": 0,
                "roots_after_proper_subfield_exclusion": source["root_count"],
                "listed_roots_status": source["listed_roots_status"],
                "status": "no_proper_subfield_roots",
            }
            if witness_hash is not None:
                if method == "source_linear_root_gcd_intersection":
                    audit["source_linear_root_gcd_hash"] = witness_hash
                else:
                    audit["reconstructed_delta_coefficient_hash"] = witness_hash
            records.append(
                {
                    "rank": rank,
                    "A": agreement,
                    "j": N - agreement,
                    "t": agreement - K,
                    "prefix_row_set": [0, base_node_count - 1],
                    "base_node_count": base_node_count,
                    "degree_bound": rank,
                    "root_count_from_source": source["root_count"],
                    "root_count_hash_from_source": source["root_count_hash"],
                    "root_count_source_ref": source["source_ref"],
                    "subfield_confinement_audit": audit,
                }
            )
    return records


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
    subfield_counts = {
        str(degree): sum(
            record["subfield_confinement_audit"]["proper_subfield_root_counts"][
                str(degree)
            ]
            for record in rank_records
        )
        for degree in PROPER_SUBFIELD_DEGREES
    }
    require(
        all(count == 0 for count in subfield_counts.values()),
        f"rank={rank}: proper subfield overlap found",
    )
    return {
        "rank": rank,
        "agreement_count": len(rank_records),
        "finite_roots_checked_for_proper_subfield": finite_roots,
        "proper_subfield_root_counts": subfield_counts,
        "proper_subfield_overlap_sum": 0,
        "regular_roots_after_proper_subfield_exclusion": finite_roots,
        "root_count_histogram": {
            str(key): root_histogram[key] for key in sorted(root_histogram)
        },
    }


def build_certificate() -> dict[str, Any]:
    artifacts = source_artifacts()
    validate_source_artifacts(artifacts)
    source_records = source_root_records(artifacts)
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
    reconstructed_coefficients = reconstruct_coefficients_for_count_only_sweep_records(
        field,
        domain,
        source_records,
    )
    records = build_records(field, source_records, reconstructed_coefficients)
    rank_summaries = {str(rank): summarize_rank(records, rank) for rank in RANKS}
    total_checked = sum(
        summary["finite_roots_checked_for_proper_subfield"]
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
            "certificate_mode": "low_rank_proper_subfield_exclusion",
        },
        "method": {
            "proper_subfield_degrees": PROPER_SUBFIELD_DEGREES,
            "subfield_criterion": "z lies in F_17^d iff z^(17^d)=z",
            "listed_root_test": "direct Frobenius fixedness on listed source roots",
            "count_only_test": "gcd(source root-gcd or reconstructed Delta_s, Z^(17^d)-Z)",
            "reconstructed_count_only_delta_records": [
                {"rank": rank, "A": agreement}
                for rank, agreement in sorted(reconstructed_coefficients)
            ],
            "consequence": (
                "none of the finite roots counted by the source slack certificates "
                "is confined to a proper subfield of F_17^32"
            ),
        },
        "aggregate": {
            "rank_summaries": rank_summaries,
            "rank_count": len(RANKS),
            "record_count": len(records),
            "proper_subfield_degrees": PROPER_SUBFIELD_DEGREES,
            "finite_roots_checked_for_proper_subfield": total_checked,
            "proper_subfield_overlap_sum": 0,
            "regular_roots_after_proper_subfield_exclusion": total_checked,
            "finite_budget_numerator": field.size // TWO128,
            "projective_budget_numerator": (field.size + 1) // TWO128,
        },
        "records": records,
        "nonclaims": [
            "synthetic syndrome-pencil family only",
            "not a quotient-image subtraction audit",
            "not a worst-case M3 row bound",
            "does not classify arbitrary extension-valued or non-proportional pencils",
        ],
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-6..11 subfield exclusion mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 low-rank-6..11 proper-subfield exclusion")
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
        "finite roots checked={checked}, proper-subfield overlap={overlap}, roots after exclusion={after}".format(
            checked=aggregate["finite_roots_checked_for_proper_subfield"],
            overlap=aggregate["proper_subfield_overlap_sum"],
            after=aggregate["regular_roots_after_proper_subfield_exclusion"],
        )
    )
    for rank in certificate["construction"]["ranks"]:
        summary = aggregate["rank_summaries"][str(rank)]
        print(
            "rank {rank}: checked={checked}, overlap={overlap}, subfield_counts={counts}".format(
                rank=rank,
                checked=summary["finite_roots_checked_for_proper_subfield"],
                overlap=summary["proper_subfield_overlap_sum"],
                counts=summary["proper_subfield_root_counts"],
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
