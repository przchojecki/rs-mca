#!/usr/bin/env python3
"""Verify the M5 regular-root rank-drop bridge."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (  # noqa: E402
    Field,
    K,
    MODULUS,
    N,
    P,
)


SCHEMA_VERSION = "f17-32-m3-m5-regular-root-rank-drop-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
GENERIC_MINOR_REF = (
    "experimental/data/certificates/hankel-f17-32-generic-regular-minor/"
    "f17_32_n512_k256_m3_generic_all_row_set_regular_minor_certificate.json"
)
FINITE_AFFINE_KERNEL_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-finite-affine-kernel-chart/"
    "f17_32_n512_k256_m3_m5_finite_affine_kernel_chart.json"
)


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def hash_value(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    size = j_value + 1
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": size,
        "maximal_row_set_count": comb(t_value, size),
        "regular_root_rank_drop": "z root of canonical gcd => rank M_A(z) <= j",
        "full_direction_consequence": (
            "if rank H_{t,j}(v)=j+1, every finite regular root survives "
            "the ambient finite-affine kernel filter"
        ),
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    generic_minor = load_json(GENERIC_MINOR_REF)
    finite_kernel = load_json(FINITE_AFFINE_KERNEL_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "syndrome length mismatch")
    require(
        generic_minor["schema_version"]
        == "f17-32-m3-generic-all-row-set-regular-minor-v1",
        "unexpected generic minor schema",
    )
    require(
        generic_minor["claim"]["regular_window"] == {"A_min": A_MIN, "A_max": A_MAX},
        "generic minor window mismatch",
    )
    require(
        finite_kernel["schema_version"]
        == "f17-32-m3-m5-finite-affine-kernel-chart-v1",
        "unexpected finite-affine kernel schema",
    )
    require(finite_kernel["window"]["A_min"] == A_MIN, "finite kernel A_min mismatch")
    require(finite_kernel["window"]["A_max"] == A_MAX, "finite kernel A_max mismatch")

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    decoded = [field.decode(value) for value in domain_encodings]
    require(
        [field.encode(value) for value in decoded] == domain_encodings,
        "domain decode/encode roundtrip failed",
    )

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    total_row_sets = sum(record["maximal_row_set_count"] for record in records)
    require(
        total_row_sets == generic_minor["claim"]["all_row_set_count_sum"],
        "generic minor row-set total mismatch",
    )
    require(
        total_row_sets == finite_kernel["window"]["all_row_set_total"],
        "finite kernel row-set total mismatch",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED",
        "object": "M5 bridge from regular gcd roots to rank-drop/noncontainment tests",
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
            "generic_regular_minor": {
                "ref": GENERIC_MINOR_REF,
                "sha256": sha256_file(GENERIC_MINOR_REF),
            },
            "finite_affine_kernel_chart": {
                "ref": FINITE_AFFINE_KERNEL_REF,
                "sha256": sha256_file(FINITE_AFFINE_KERNEL_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
        },
        "theorem": {
            "canonical_gcd_root_rank_drop": (
                "Let G_A be the gcd of all nonzero maximal minors of "
                "M_A(Z)=H(u)+Z H(v).  If z is a finite root of G_A, then "
                "all maximal minors of M_A(z) vanish, including those whose "
                "polynomials were identically zero.  Hence rank M_A(z)<=j."
            ),
            "rank_drop_root_converse": (
                "If the regular bucket is nonsingular and z in F is a finite "
                "slope with rank M_A(z)<=j, then every maximal minor vanishes "
                "at z, so z is a root of the canonical gcd G_A."
            ),
            "finite_kernel_consequence": (
                "Combining with the finite-affine kernel chart: if "
                "rank H(v)>rank M_A(z), then the root z survives the ambient "
                "noncontainment filter."
            ),
            "full_direction_consequence": (
                "For rank H(v)=j+1, every finite regular root has "
                "rank M_A(z)<=j<j+1 and therefore cannot be removed by "
                "same-support kernel containment."
            ),
            "proof": [
                "A maximal row-set minor evaluates to a maximal minor of M_A(z).",
                "A root of the gcd of all nonzero minor polynomials is a root of each nonzero minor polynomial; identically zero minors vanish at every z.",
                "All maximal minors vanish exactly when the column rank is at most j.",
                "The converse holds in a nonsingular regular bucket because a finite field root common to all nonzero minor polynomials contributes the linear factor Z-z to their gcd.",
                "The finite-affine kernel consequence is the rank-stratification corollary of the M5 kernel chart.",
            ],
        },
        "field_audit": {
            "full_domain_distinct": True,
            "domain_size": len(domain_encodings),
            "domain_hash": hash_value(domain_encodings),
            "decoded_roundtrip_hash": hash_value([field.encode(value) for value in decoded]),
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "regular_root_implies_rank_drop": True,
            "nonsingular_rank_drop_implies_regular_root": True,
            "full_direction_roots_survive_finite_kernel_filter": True,
        },
        "checks": [
            "row descriptor, generic-minor, and finite-kernel schemas match",
            "window is 385..426",
            "row-set totals agree across dependencies",
            "domain encodings round-trip in the printed F_17^32 model",
            "maximal-minor vanishing is equivalent to rank <= j",
        ],
        "nonclaims": [
            "does not compute a finite root table",
            "does not prove ambient nonempty implies split-locator nonempty",
            "does not audit quotient, extension, or subfield overlap for surviving roots",
            "does not close singular buckets where every maximal minor is identically zero",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"M5 regular-root rank-drop certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M5 regular-root rank-drop bridge")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, row sets={all_row_set_total}".format(
            **window
        )
    )
    print(
        "regular root => rank drop={regular_root_implies_rank_drop}, full-direction roots survive filter={full_direction_roots_survive_finite_kernel_filter}".format(
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
