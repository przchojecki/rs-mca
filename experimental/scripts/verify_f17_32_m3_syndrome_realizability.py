#!/usr/bin/env python3
"""Verify the F_17^32 M3 syndrome-realizability reduction.

In the M3 regular window for RS[F_17^32,H,256], every exact bucket uses the
first t+j = n-k = 256 syndrome moments.  Since |H|=512, the subgroup
inverse-Fourier section proves that every pair of length-256 syndrome vectors
(u,v) is realized by explicit line values (f,g) on H.  Thus the remaining
regular-window problem is a universal syndrome-pencil classification problem,
not a row-realizability problem.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-m3-syndrome-realizability-v1"
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
N = 512
K = 256
SYNDROME_LENGTH = N - K

ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
PLAN_REF = (
    "experimental/data/certificates/hankel-regular-window-f17-385-426/"
    "f17_32_n512_k256_regular_window_plan.json"
)
SUBGROUP_SECTION_REF = (
    "experimental/data/certificates/subgroup-syndrome-section/"
    "subgroup_syndrome_section_certificate.json"
)
OUTPUT_PATH = ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-syndrome-realizability/"
    "f17_32_n512_k256_m3_syndrome_realizability_certificate.json"
)


def load_json(ref: str) -> dict[str, Any]:
    return json.loads((ROOT / ref).read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_sources(
    descriptor: dict[str, Any],
    plan: dict[str, Any],
    subgroup_section: dict[str, Any],
) -> None:
    require(descriptor["row"]["n"] == N, "row descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "row descriptor k mismatch")
    require(len(descriptor["domain"]["domain_encodings"]) == N, "domain length mismatch")
    require(plan["row"]["n"] == N, "plan n mismatch")
    require(plan["row"]["k"] == K, "plan k mismatch")
    require(plan["window"]["A_min"] == AGREEMENT_MIN, "plan A_min mismatch")
    require(plan["window"]["A_max"] == AGREEMENT_MAX, "plan A_max mismatch")
    require(
        plan["row"]["domain_hash"] == descriptor["row"]["domain_hash"],
        "plan/domain hash mismatch",
    )
    require(
        subgroup_section["schema_version"] == "subgroup-syndrome-section-v1",
        "subgroup section schema mismatch",
    )
    require(subgroup_section["status"] == "PROVED / AUDIT", "subgroup section status mismatch")
    theorem = subgroup_section["theorem"]
    require("r <= |H|" in theorem["hypotheses"], "subgroup theorem does not state length hypothesis")
    cases = {case["name"]: case for case in subgroup_section["cases"]}
    require("F17_32_H512_fixed_top_window" in cases, "missing F17^32 subgroup-section replay")
    f17_case = cases["F17_32_H512_fixed_top_window"]
    require(f17_case["domain_hash"] == descriptor["row"]["domain_hash"], "subgroup replay domain mismatch")
    require(f17_case["u_section"]["syndrome_length"] == SYNDROME_LENGTH, "u-section length mismatch")
    require(f17_case["v_section"]["syndrome_length"] == SYNDROME_LENGTH, "v-section length mismatch")
    require(f17_case["u_section"]["subgroup_order"] == N, "u-section subgroup order mismatch")
    require(f17_case["v_section"]["subgroup_order"] == N, "v-section subgroup order mismatch")
    require(f17_case["u_section"]["section_replays_syndrome"] is True, "u-section replay failed")
    require(f17_case["v_section"]["section_replays_syndrome"] is True, "v-section replay failed")


def per_agreement(plan: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for item in plan["per_agreement"]:
        agreement = int(item["A"])
        if agreement < AGREEMENT_MIN or agreement > AGREEMENT_MAX:
            continue
        j = int(item["j"])
        t = int(item["t"])
        visible_length = t + j
        max_index = visible_length - 1
        require(j == N - agreement, f"A={agreement}: j mismatch")
        require(t == agreement - K, f"A={agreement}: t mismatch")
        require(visible_length == SYNDROME_LENGTH, f"A={agreement}: visible syndrome length mismatch")
        require(max_index == SYNDROME_LENGTH - 1, f"A={agreement}: max syndrome index mismatch")
        require(visible_length <= N, f"A={agreement}: section length exceeds subgroup order")
        out.append(
            {
                "A": agreement,
                "j": j,
                "t": t,
                "visible_syndrome_length": visible_length,
                "max_syndrome_index_used": max_index,
                "subgroup_order": N,
                "section_applies": True,
                "u_v_pencil_space": "all pairs in (F_17^32)^256 x (F_17^32)^256",
                "line_value_formula": {
                    "f_u": "f_u(x)=sum_{0<=m<256} u_m x^(-m-1)",
                    "g_v": "g_v(x)=sum_{0<=m<256} v_m x^(-m-1)",
                },
            }
        )
    require(len(out) == AGREEMENT_MAX - AGREEMENT_MIN + 1, "agreement count mismatch")
    return out


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    plan = load_json(PLAN_REF)
    subgroup_section = load_json(SUBGROUP_SECTION_REF)
    validate_sources(descriptor, plan, subgroup_section)
    records = per_agreement(plan)
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "field": "F_17^32",
            "n": N,
            "k": K,
            "domain_hash": descriptor["row"]["domain_hash"],
        },
        "source_artifacts": {
            "row_descriptor": {
                "ref": ROW_DESCRIPTOR_REF,
                "sha256": sha256_file(ROW_DESCRIPTOR_REF),
                "schema_version": descriptor["schema_version"],
            },
            "regular_window_plan": {
                "ref": PLAN_REF,
                "sha256": sha256_file(PLAN_REF),
                "schema_version": plan["schema_version"],
            },
            "subgroup_syndrome_section": {
                "ref": SUBGROUP_SECTION_REF,
                "sha256": sha256_file(SUBGROUP_SECTION_REF),
                "schema_version": subgroup_section["schema_version"],
            },
        },
        "theorem": {
            "statement": (
                "For every A in 385..426 and every length-256 syndrome pencil "
                "(u,v), there are explicit line values f,g:H->F_17^32 whose "
                "weighted syndromes are u and v.  Hence row-realizability "
                "imposes no extra constraint on the M3 regular-window "
                "syndrome-pencil classification."
            ),
            "reason": "t+j=(A-k)+(n-A)=n-k=256 <= |H|=512",
            "section_formula": "y_s(x)=sum_{0<=m<256} s_m x^(-m-1)",
            "uses": "subgroup-syndrome-section theorem",
        },
        "summary": {
            "regular_window": {"A_min": AGREEMENT_MIN, "A_max": AGREEMENT_MAX},
            "agreements": len(records),
            "visible_syndrome_length": SYNDROME_LENGTH,
            "subgroup_order": N,
            "pencil_realizability": "surjective onto all length-256 u,v syndrome pencils",
            "remaining_problem": (
                "classify arbitrary length-256 syndrome pencils after tangent, "
                "quotient, and extension-confined ledgers are removed"
            ),
        },
        "per_agreement": records,
        "nonclaims": [
            "does not prove a worst-case MCA bound",
            "does not compute root tables for arbitrary syndrome pencils",
            "does not remove tangent, quotient, or extension-confined branches",
            "does not classify singular pivot buckets",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"M3 syndrome-realizability certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 syndrome-realizability")
    print(
        "window: A={A_min}..{A_max}, agreements={agreements}".format(
            agreements=summary["agreements"],
            **summary["regular_window"],
        )
    )
    print(
        f"visible syndrome length={summary['visible_syndrome_length']}, "
        f"subgroup order={summary['subgroup_order']}"
    )
    print(f"pencil realizability: {summary['pencil_realizability']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic certificate JSON")
    parser.add_argument("--check", type=Path, help="check deterministic certificate JSON")
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
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
