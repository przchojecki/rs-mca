#!/usr/bin/env python3
"""Synthesize the full affine-hull theorem from the public certificates."""

import hashlib
import json
import math
import pathlib
import sys


def load(directory: pathlib.Path, name: str) -> dict:
    return json.loads((directory / name).read_text(encoding="ascii"))


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: verifier CERTIFICATE_DIRECTORY OUTPUT")
    directory = pathlib.Path(sys.argv[1])
    output_path = pathlib.Path(sys.argv[2])

    sparse_primary = load(directory, "SP01zxa5_sparse_locator_hull.json")
    sparse_audit = load(
        directory, "SP01zxa5_sparse_locator_hull_independent_audit.json"
    )
    assert sparse_primary["pair_count"] == sparse_audit["pair_count"] == math.comb(16, 2)
    assert sparse_primary["triple_count"] == sparse_audit["triple_count"] == math.comb(16, 3)
    assert not sparse_primary["new_split_locator_with_coefficient_support_at_most_three"]
    assert not sparse_audit["new_split_locator_with_coefficient_support_at_most_three"]

    names = {
        4: "SP01zxa6_support_four_partition_sieve",
        5: "SP01zxa7_support_five_partition_sieve",
        6: "SP01zxa8_support_six_partition_sieve",
        7: "SP01zxa9_support_seven_partition_sieve",
        8: "SP01zxaa_support_eight_partition_sieve",
    }
    imported_reports = []
    for support, stem in names.items():
        primary = load(directory, stem + ".json")
        audit = load(directory, stem + "_independent_audit.json")
        count_key = "quadruple_count" if support == 4 else "support_count"
        assert primary[count_key] == audit[count_key] == math.comb(16, support)
        assert primary["minimum_residual_root_margin"] > 0
        assert audit["minimum_residual_root_margin"] > 0
        imported_reports.append(
            {
                "support": support,
                "support_count": primary[count_key],
                "primary_margin": primary["minimum_residual_root_margin"],
                "audit_margin": audit["minimum_residual_root_margin"],
            }
        )

    dense_reports = []
    primary_normals = 0
    audit_normals = 0
    source_paths = []
    for support in range(9, 17):
        primary_path = directory / f"SP01zxab_support_{support:02d}_partition_sieve.json"
        audit_path = directory / (
            f"SP01zxab_support_{support:02d}_partition_sieve_independent_audit.json"
        )
        primary = json.loads(primary_path.read_text(encoding="ascii"))
        audit = json.loads(audit_path.read_text(encoding="ascii"))
        source_paths.extend((primary_path, audit_path))
        for key in (
            "support_count",
            "residual_degree_histogram",
            "outside_overlap_upper_histogram",
            "required_core_root_histogram",
        ):
            assert primary[key] == audit[key]
        count = math.comb(16, support)
        assert primary["support_count"] == count
        assert primary["dependent_within_group_row_set_histogram"] == {"0": count}
        assert audit["dependent_within_group_row_set_histogram"] == {"0": count}
        assert primary["minimum_residual_root_margin"] > 0
        assert audit["minimum_residual_root_margin"] > 0
        assert not primary["new_split_locator_at_this_support"]
        assert not audit["new_split_locator_at_this_support"]
        primary_normals += primary["independent_row_normals_generated"]
        audit_normals += audit["independent_row_normals_generated"]
        dense_reports.append(
            {
                "support": support,
                "support_count": count,
                "primary_core_cap": primary["maximum_certified_core_root_cap"],
                "audit_core_cap": audit["maximum_certified_core_root_cap"],
                "primary_margin": primary["minimum_residual_root_margin"],
                "audit_margin": audit["minimum_residual_root_margin"],
            }
        )

    all_nonempty_supports = sum(math.comb(16, support) for support in range(1, 17))
    dense_supports = sum(item["support_count"] for item in dense_reports)
    assert all_nonempty_supports == 65535
    assert dense_supports == 26333

    digest = hashlib.sha256()
    for path in sorted(
        source_paths,
        key=lambda item: ("independent_audit" in item.name, item.name),
    ):
        digest.update(path.name.encode("ascii"))
        digest.update(path.read_bytes())

    report = {
        "schema": "sp01zxab-full-affine-hull-synthesis/v1",
        "status": "PASS_EXACT_FULL_AFFINE_HULL_RIGIDITY",
        "field": 2147483647,
        "vertex_count": 16,
        "affine_dimension": 15,
        "all_nonempty_coefficient_supports": all_nonempty_supports,
        "dense_supports_9_through_16": dense_supports,
        "dense_primary_normals": primary_normals,
        "dense_audit_normals": audit_normals,
        "supports_4_through_8": imported_reports,
        "supports_9_through_16": dense_reports,
        "split_affine_hull_members": "exactly_the_sixteen_vertices",
        "dense_json_bundle_sha256": digest.hexdigest(),
        "scope_guard": (
            "Complete classification inside the affine hull of the sixteen "
            "known syndrome locators. It does not exclude split locators "
            "outside this affine hull or prove the complete fixture list."
        ),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="ascii"
    )
    print("PASS SP01zxab exact full affine-hull synthesis")


if __name__ == "__main__":
    main()
