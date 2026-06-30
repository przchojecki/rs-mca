#!/usr/bin/env python3
"""Verify the rank-at-nodes regular-bucket audit certificate.

The theorem is the small linear-algebra gate used by the regular Hankel-minor
extractor: a maximal minor has degree at most j+1, so j+2 distinct failed
rank tests prove every maximal minor is identically zero; one full-rank
specialization supplies a nonzero maximal minor.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_aperiodic_eliminant_packet import (
    PolynomialBasisField,
    parse_prime_field,
)


SCHEMA_VERSION = "rank-at-nodes-regular-bucket-audit-v1"
PACKET_SCHEMA_VERSION = "aperiodic-hankel-eliminant-v1"
CERTIFICATE_PATH = ROOT / (
    "experimental/data/certificates/rank-at-nodes-regular-bucket/"
    "rank_at_nodes_regular_bucket_audit.json"
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def sha256_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def repo_ref(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def field_size(packet: dict[str, Any]) -> int:
    extension_field = PolynomialBasisField.from_packet(packet)
    if extension_field is not None:
        return extension_field.size
    prime = parse_prime_field(packet["row"]["field"])
    require(prime is not None, "rank_at_nodes packet needs a finite field size")
    return prime


def rank_at_nodes_items(path: Path) -> list[tuple[int, dict[str, Any]]]:
    data = load_json(path)
    if not isinstance(data, dict) or data.get("schema_version") != PACKET_SCHEMA_VERSION:
        return []
    out = []
    for index, item in enumerate(data.get("exact_agreements", [])):
        audit = item.get("extractor_audit")
        if isinstance(audit, dict) and audit.get("row_set_source") == "rank_at_nodes":
            out.append((index, item))
    return out


def packet_paths() -> list[Path]:
    out = []
    for path in (ROOT / "experimental/data/certificates").glob("**/*.json"):
        if path.name.startswith("invalid_"):
            continue
        if rank_at_nodes_items(path):
            out.append(path)
    return sorted(out)


def validate_rank_at_nodes_item(
    packet: dict[str, Any],
    path: Path,
    item_index: int,
    item: dict[str, Any],
) -> dict[str, Any]:
    agreement = item["A"]
    j_value = item["j"]
    size = j_value + 1
    required_nodes = size + 1
    audit = item["extractor_audit"]
    tested = audit.get("rank_pivot_nodes_tested")
    test_nodes = audit.get("rank_pivot_test_nodes")
    field_order = field_size(packet)

    require(
        field_order > size,
        f"{repo_ref(path)} A={agreement}: field has too few nodes for rank_at_nodes",
    )
    require(
        audit.get("rank_pivot_nodes_required") == required_nodes,
        f"{repo_ref(path)} A={agreement}: rank_pivot_nodes_required mismatch",
    )
    require(
        isinstance(tested, int) and 1 <= tested <= required_nodes,
        f"{repo_ref(path)} A={agreement}: bad tested count",
    )
    require(
        isinstance(test_nodes, list) and len(test_nodes) == tested,
        f"{repo_ref(path)} A={agreement}: bad test node list",
    )
    require(
        test_nodes == list(range(tested)),
        f"{repo_ref(path)} A={agreement}: test nodes are not deterministic prefix nodes",
    )

    status = item["status"]
    if status == "regular_minor":
        minor = item["regular_minor"]
        row_set = minor["row_set"]
        require(
            len(row_set) == size,
            f"{repo_ref(path)} A={agreement}: row_set size mismatch",
        )
        require(
            minor["degree"] <= size,
            f"{repo_ref(path)} A={agreement}: degree exceeds j+1",
        )
        require(
            audit.get("rank_pivot_node") == test_nodes[-1],
            f"{repo_ref(path)} A={agreement}: pivot node is not final tested node",
        )
        theorem_outcome = "nonzero_maximal_minor"
    elif status == "residual_obstruction":
        require(
            audit.get("rank_pivot_node") is None,
            f"{repo_ref(path)} A={agreement}: singular declaration names pivot node",
        )
        require(
            tested == required_nodes,
            f"{repo_ref(path)} A={agreement}: singular declaration underchecked",
        )
        reason = item.get("residual_reason")
        require(
            isinstance(reason, str) and "size+1 distinct slopes" in reason,
            f"{repo_ref(path)} A={agreement}: missing singularity proof reason",
        )
        theorem_outcome = "all_maximal_minors_identically_zero"
    else:
        raise AssertionError(
            f"{repo_ref(path)} A={agreement}: unsupported rank_at_nodes status {status}"
        )

    return {
        "packet_ref": repo_ref(path),
        "packet_sha256": sha256_file(path),
        "item_index": item_index,
        "A": agreement,
        "j": j_value,
        "t": item["t"],
        "field_size": field_order,
        "minor_size": size,
        "degree_bound": size,
        "nodes_required_for_singularity_proof": required_nodes,
        "rank_pivot_test_nodes": test_nodes,
        "rank_pivot_node": audit.get("rank_pivot_node"),
        "packet_status": status,
        "theorem_outcome": theorem_outcome,
    }


def build_certificate() -> dict[str, Any]:
    records = []
    for path in packet_paths():
        packet = load_json(path)
        for item_index, item in rank_at_nodes_items(path):
            records.append(validate_rank_at_nodes_item(packet, path, item_index, item))

    regular_count = sum(
        record["theorem_outcome"] == "nonzero_maximal_minor" for record in records
    )
    singular_count = sum(
        record["theorem_outcome"] == "all_maximal_minors_identically_zero"
        for record in records
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "theorem": {
            "name": "rank_at_nodes_regular_bucket_dichotomy",
            "statement": (
                "For a t by (j+1) affine-linear matrix pencil M(Z), every "
                "maximal minor has degree at most j+1.  A full-rank "
                "specialization at one tested node gives a nonzero maximal "
                "minor; if all maximal minors vanish at j+2 distinct tested "
                "nodes, then all maximal minors vanish identically."
            ),
            "paper_d_v9_role": (
                "regular overdetermined bucket decision before pivot charts"
            ),
            "required_distinct_nodes": "j+2",
        },
        "audit_summary": {
            "rank_at_nodes_packet_items": len(records),
            "regular_minor_items": regular_count,
            "singular_or_residual_items": singular_count,
            "audited_packet_refs": sorted(
                {record["packet_ref"] for record in records}
            ),
        },
        "audited_instances": records,
        "nonclaims": [
            "does not enumerate roots for large fields",
            "does not prove an actual F_17^32 M3 row bound",
            "does not close singular pivot charts",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-at-nodes audit mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["audit_summary"]
    print("rank-at-nodes regular-bucket audit")
    print(
        "items={rank_at_nodes_packet_items}, regular={regular_minor_items}, "
        "singular_or_residual={singular_or_residual_items}".format(**summary)
    )
    for ref in summary["audited_packet_refs"]:
        print(f"- {ref}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic audit JSON")
    parser.add_argument("--check", type=Path, help="check deterministic audit JSON")
    parser.add_argument("--json", action="store_true", help="print audit JSON")
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
