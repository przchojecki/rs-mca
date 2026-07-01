#!/usr/bin/env python3
"""Verify the split-locator filter for the barycentric boundary root."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import K, N, P  # noqa: E402


SCHEMA_VERSION = "f17-32-m3-rank6-barycentric-split-filter-v1"
Q_LINE = 17**32
RANK = 6
A_VALUES = [385, 386, 387]
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
BOUNDARY_OBSTRUCTION_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-barycentric-obstruction/"
    "f17_32_n512_k256_m3_rank6_boundary_barycentric_obstruction.json"
)
NULLPOLY_SPLIT_GATE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/"
    "f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json"
)


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


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    m_value = j_value + 1
    support_size = m_value + RANK
    defect = support_size - t_value

    require(defect > 0, f"A={agreement}: no boundary defect")
    require(defect < j_value, f"A={agreement}: low-degree kernel not below split degree")
    require(support_size > j_value, f"A={agreement}: interpolation root count too small")
    require(t_value == support_size - defect, f"A={agreement}: defect mismatch")

    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "m": m_value,
        "direction_rank": RANK,
        "combined_support_size": support_size,
        "boundary_defect": defect,
        "ambient_root": "z=1",
        "barycentric_kernel_description": {
            "kernel_polynomial_space": f"polynomials Q with deg Q < {defect}",
            "kernel_dimension": defect,
            "proof": (
                "If L has degree <m and H(u+v)L=0, then the weighted values "
                "omega_s L(s) lie in the nullspace of the first t Vandermonde "
                "rows on S.  That nullspace is {omega_s Q(s): deg Q<|S|-t}. "
                "Thus L and Q agree on all |S| nodes; since deg(L-Q)<=j<|S|, "
                "L=Q."
            ),
        },
        "split_locator_filter": {
            "split_locator_required_degree": j_value,
            "split_locator_roots_in_H": j_value,
            "max_kernel_degree": defect - 1,
            "contains_degree_j_split_locator": False,
            "reason": f"all kernel polynomials have degree < {defect}, while a split locator has degree {j_value}",
        },
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    obstruction = load_json(BOUNDARY_OBSTRUCTION_REF)
    split_gate = load_json(NULLPOLY_SPLIT_GATE_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        obstruction["schema_version"]
        == "f17-32-m3-rank6-boundary-barycentric-obstruction-v1",
        "boundary obstruction schema mismatch",
    )
    require(obstruction["window"]["agreements"] == A_VALUES, "obstruction agreement mismatch")
    require(
        obstruction["summary"]["support_weight_uniform_empty_finite_table_refuted"],
        "obstruction summary mismatch",
    )
    require(
        split_gate["schema_version"] == "f17-32-m3-nullpolynomial-split-locator-gate-v1",
        "null-polynomial split gate schema mismatch",
    )
    require(
        split_gate["summary"]["split_locator_gate_available"],
        "split-locator gate requirement missing",
    )
    require(N % P != 0, "X^512-1 is not separable in this characteristic")

    records = [agreement_record(agreement) for agreement in A_VALUES]
    require(
        [record["boundary_defect"] for record in records]
        == obstruction["summary"]["boundary_deficits"],
        "defect mismatch with obstruction packet",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "split-locator filter for the rank-6 barycentric boundary root",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "q_line": Q_LINE,
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "boundary_barycentric_obstruction": {
                "ref": BOUNDARY_OBSTRUCTION_REF,
                "sha256": sha256_file(BOUNDARY_OBSTRUCTION_REF),
            },
            "nullpolynomial_split_locator_gate": {
                "ref": NULLPOLY_SPLIT_GATE_REF,
                "sha256": sha256_file(NULLPOLY_SPLIT_GATE_REF),
            },
        },
        "window": {
            "agreements": A_VALUES,
            "agreement_count": len(A_VALUES),
        },
        "theorem": {
            "statement": (
                "For the barycentric-residue boundary construction at A=385,386,387, "
                "the finite ambient root z=1 has no degree-j split-locator witness."
            ),
            "vandermonde_dual_kernel": (
                "For S of size d and barycentric residues omega_s, the nullspace "
                "of the first t Vandermonde rows on weighted values is exactly "
                "{omega_s Q(s): deg Q<d-t}."
            ),
            "interpolation_step": (
                "A kernel polynomial L of degree <m=j+1 must agree on S with a "
                "polynomial Q of degree <d-t.  Since |S|=j+7>j, L-Q has too many "
                "roots unless L=Q."
            ),
            "split_filter": (
                "The null-polynomial split-locator gate requires a monic degree-j "
                "divisor of X^512-1.  The z=1 barycentric kernel contains only "
                "polynomials of degree <d-t in {1,3,5}, hence no such locator."
            ),
            "consequence": (
                "The barycentric packet is a sharpness obstruction for ambient "
                "empty finite-root tables, but its displayed root is filtered out "
                "before becoming a support-wise split-locator witness."
            ),
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "ambient_finite_root": 1,
            "boundary_defects": [record["boundary_defect"] for record in records],
            "kernel_dimensions": [record["boundary_defect"] for record in records],
            "degree_j_split_locator_present_at_z1": False,
            "barycentric_root_filtered_by_split_locator_gate": True,
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "boundary obstruction packet has agreements A=385,386,387",
            "null-polynomial split-locator gate is available",
            "boundary defects are 5,3,1",
            "kernel degrees are strictly below the required split-locator degree j",
            "X^512-1 is separable in characteristic 17",
        ],
        "nonclaims": [
            "does not classify every finite root of the barycentric weights",
            "does not classify arbitrary boundary rank-6 pencils",
            "does not close overlapping-support strata",
            "does not prove endpoint payment",
            "does not remove the need for exact root tables or paid-root audits in other boundary families",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-6 barycentric split-filter certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 barycentric split-locator filter")
    print("A={}".format(",".join(str(value) for value in certificate["window"]["agreements"])))
    print(
        "ambient z={ambient_finite_root}, split locator present={degree_j_split_locator_present_at_z1}".format(
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
        check_certificate(args.check, certificate)
    print_summary(certificate)


if __name__ == "__main__":
    main()
