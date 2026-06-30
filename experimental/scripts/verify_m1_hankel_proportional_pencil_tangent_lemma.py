#!/usr/bin/env python3
"""Verify the v9 proportional-pencil tangent lemma certificate.

The lemma is the reusable form of the scalar-multiple packet check: if
``u=c v`` then the Hankel pencil satisfies ``H(u)+Z H(v)=(c+Z)H(v)``.  Hence
regular roots and affine pivot slopes from this branch are tangent/common-code
line roots, not aperiodic roots.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from hashlib import sha256
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.extract_regular_hankel_minors import (  # noqa: E402
    determinant_mod,
    determinant_polynomial_by_interpolation,
    linear_power_mod,
    poly_eval,
    poly_scale,
)


SCHEMA_VERSION = "m1-hankel-proportional-pencil-tangent-lemma-v1"
PRIME = 17
SCALAR = 5
TANGENT_ROOT = (-SCALAR) % PRIME
SIZE = 3
T = 5
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/"
    "hankel_proportional_pencil_tangent_lemma_certificate.json"
)
SCALAR_INPUT_REF = (
    "experimental/data/hankel-regular-minor-inputs/"
    "f17_32_n512_k256_a426_scalar5_rank_witness_input.json"
)
SCALAR_PACKET_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-proportional-a426/"
    "f17_32_n512_k256_a426_scalar5_packet.json"
)
SCALAR_SUBTRACTION_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-proportional-a426/"
    "f17_32_n512_k256_a426_scalar5_subtraction.json"
)
SCHEMA_CHECKER = REPO_ROOT / "scripts/check_aperiodic_eliminant_packet.py"
SCHEMA = REPO_ROOT / "scripts/aperiodic_eliminant_schema.json"


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else REPO_ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((REPO_ROOT / ref).read_bytes()).hexdigest()


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


def regular_matrix(values: list[int], row_set: list[int], size: int) -> list[list[int]]:
    return [[values[row + col] % PRIME for col in range(size)] for row in row_set]


def regular_case(
    name: str,
    v: list[int],
    row_set: list[int],
) -> dict[str, Any]:
    u = [(SCALAR * value) % PRIME for value in v]
    det_v = determinant_mod(regular_matrix(v, row_set, SIZE), PRIME)
    actual = determinant_polynomial_by_interpolation(u, v, row_set, SIZE, PRIME)
    expected = poly_scale(linear_power_mod(SCALAR, SIZE, PRIME), det_v, PRIME)
    require(actual == expected, f"{name}: determinant identity failed")
    roots = [
        root for root in range(PRIME) if poly_eval(actual, root, PRIME) == 0
    ]
    if det_v:
        require(roots == [TANGENT_ROOT], f"{name}: wrong nonzero-minor roots")
    else:
        require(all(value == 0 for value in actual), f"{name}: expected zero minor")
    return {
        "name": name,
        "field": f"F_{PRIME}",
        "scalar_c": SCALAR,
        "row_set": row_set,
        "minor_size": SIZE,
        "det_Hv": det_v,
        "determinant_coefficients_mod_17": actual,
        "expected_shape": (
            "det(H(v)_R)*(Z+c)^3"
            if det_v
            else "zero determinant; proportional branch is still tangent-confined"
        ),
        "roots_mod_17": roots if det_v else "all_slopes_for_this_zero_minor",
        "tangent_slope_mod_17": TANGENT_ROOT,
    }


def pivot_case() -> dict[str, Any]:
    b_vectors = [
        [0, 3, 7, 11],
        [5, 0, 0, 9],
        [0, 0, 0, 0],
    ]
    records = []
    for b_vec in b_vectors:
        a_vec = [(SCALAR * value) % PRIME for value in b_vec]
        slopes = set()
        contained = True
        for a_i, b_i in zip(a_vec, b_vec):
            if b_i:
                slopes.add((-a_i * pow(b_i, -1, PRIME)) % PRIME)
                contained = False
            else:
                require(a_i == 0, "proportional pivot vector broke containment")
        require(slopes in ({TANGENT_ROOT}, set()), "pivot slope was not tangent")
        records.append(
            {
                "B_vector": b_vec,
                "A_vector": a_vec,
                "status": "contained" if contained else "finite_tangent_slope",
                "slope_mod_17": None if contained else TANGENT_ROOT,
            }
        )
    return {
        "field": f"F_{PRIME}",
        "identity": "A_T=c B_T for every locator/co-support T",
        "checked_vectors": records,
    }


def check_f17_32_artifacts() -> dict[str, Any]:
    checker = load_schema_checker()
    checker.check_path(REPO_ROOT / SCALAR_PACKET_REF, SCHEMA)
    input_data = load_json(SCALAR_INPUT_REF)
    packet = load_json(SCALAR_PACKET_REF)
    subtraction = load_json(SCALAR_SUBTRACTION_REF)
    require(input_data["certificate_mode"] == "scalar_multiple_roots", "bad scalar input mode")
    require(input_data["line_syndrome"]["scalar_multiple_u_over_v"] == SCALAR, "bad scalar")
    require(input_data["line_syndrome"]["tangent_root"] == TANGENT_ROOT, "bad tangent root")
    require(packet["root_union"] == [TANGENT_ROOT], "bad F17^32 root union")
    require(
        subtraction["summary"]["deduped_aperiodic_numerator_after_removed_ledgers"] == 0,
        "subtraction did not remove proportional root",
    )
    return {
        "input_ref": SCALAR_INPUT_REF,
        "input_sha256": sha256_file(SCALAR_INPUT_REF),
        "packet_ref": SCALAR_PACKET_REF,
        "packet_sha256": sha256_file(SCALAR_PACKET_REF),
        "subtraction_ref": SCALAR_SUBTRACTION_REF,
        "subtraction_sha256": sha256_file(SCALAR_SUBTRACTION_REF),
        "checked_root_union": packet["root_union"],
        "checked_residual_after_tangent": [],
    }


def build_certificate() -> dict[str, Any]:
    regular_v = [2, 7, 4, 13, 6, 15, 5, 9]
    singular_v = [1 for _ in range(8)]
    regular_checks = [
        regular_case("nonzero_prefix_minor", regular_v, [0, 1, 2]),
        regular_case("nonzero_shifted_minor", regular_v, [0, 1, 3]),
        regular_case("singular_rank_one_minor", singular_v, [0, 1, 2]),
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "theorem": {
            "name": "Hankel proportional-pencil tangent lemma",
            "statement": (
                "For any field F, scalar c, syndrome vector v, and u=c v, "
                "the v9 Hankel pencil satisfies H(u)+Z H(v)=(c+Z)H(v). "
                "Thus every nonzero regular maximal minor has root set {-c}; "
                "every affine pivot slope with B_T nonzero is also -c; and "
                "B_T=0 implies A_T=0, hence contained.  After the "
                "tangent/common-code-line ledger removes Z=-c, the proportional "
                "branch contributes no aperiodic roots."
            ),
            "proof_status": "algebraic identity plus machine replay",
            "v9_residual_label": "tangent",
        },
        "formal_identities": {
            "regular_minor": "det((H(u)+Z H(v))_R)=det(H(v)_R)*(Z+c)^(j+1)",
            "pivot_chart": "A_T=H(u) ell_T=c H(v) ell_T=c B_T",
            "removed_slope": "Z=-c makes u+Z v=0, a common-code-line syndrome",
        },
        "prime_field_checks": {
            "regular_minor_checks": regular_checks,
            "pivot_slope_checks": pivot_case(),
        },
        "f17_32_replay": check_f17_32_artifacts(),
        "consequence_for_packets": {
            "if_regular_minor_nonzero": "root_union={-c}; charge it to tangent",
            "if_regular_bucket_singular": (
                "proportionality alone is a tangent residual, not a new "
                "aperiodic obstruction"
            ),
            "claim_scope": "not threshold-pinning unless embedded in an actual-row packet",
        },
        "nonclaims": [
            "does not prove actual M3 row root tables",
            "does not bound non-proportional aperiodic pencils",
            "does not replace quotient/tangent deduplication for arbitrary packets",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"proportional-pencil lemma certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    theorem = certificate["theorem"]
    print(theorem["name"])
    print(f"status: {certificate['status']}")
    print("v9 residual label:", theorem["v9_residual_label"])
    print("F17^32 replay root union:", certificate["f17_32_replay"]["checked_root_union"])


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
