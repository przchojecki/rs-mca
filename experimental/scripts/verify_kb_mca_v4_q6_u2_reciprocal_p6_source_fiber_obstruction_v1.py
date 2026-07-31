#!/usr/bin/env python3
"""Verify the active source-fiber obstruction for the PR #1126 witness.

For an actual outgoing component H dividing the endpoint producer

    M(T,X) = sum_i kappa_i L_i(T) B(X)/z_i(X),

specialization at every source alpha_i forces H(alpha_i,X) to divide
B(X).  The exact local reciprocal-P6 witness from PR #1126 fails this
necessary gate at six of its twelve source labels.

The finite-field arithmetic in this verifier is inherited from, and first
revalidates, the exact parent verifier.  A separate Sage script reconstructs
the obstruction independently.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


if not __debug__:
    raise RuntimeError(
        "Verifier refuses optimized execution; rerun without Python -O."
    )


class VerificationError(RuntimeError):
    """Raised when an exact certificate condition fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


ROOT = Path(__file__).resolve().parents[1]
PARENT_SCRIPT = (
    ROOT
    / "scripts"
    / "verify_kb_mca_v4_q6_u2_reciprocal_p6_local_survivor_v1.py"
)
PARENT_CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-q6-u2-reciprocal-p6-local-survivor-v1"
    / "kb_mca_v4_q6_u2_reciprocal_p6_local_survivor_v1.json"
)
CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-q6-u2-reciprocal-p6-source-fiber-obstruction-v1"
    / "kb_mca_v4_q6_u2_reciprocal_p6_source_fiber_obstruction_v1.json"
)

PARENT_COMMIT = "0f6c23f5c4f02ee9f9e8f340f833abc0096cf254"
PARENT_PAYLOAD = (
    "a3231f7903e255b254b202a269aca1740aec666cd04c13940711e83d29e8ce1b"
)
SOURCE_REDUCTION_COMMIT = "44542e91e459364a521870ed2ebde7f6fe5055bf"
MANUAL_INTEGRATION_COMMIT = "0f7476f0fcbc5d1a1d3eed0c03221aaa48f5767d"

# Canonical roots, in F_p + omega F_p coordinates, of the parent source
# quintic.  The first root is -1 and each following adjacent pair is Galois
# conjugate.  These values are independently reconstructed by the Sage replay.
COMMON_SOURCE_ROOTS = [
    [2_130_706_432, 0],
    [657_937_426, 1_329_463_970],
    [657_937_426, 801_242_463],
    [39_550_247, 1_475_945_685],
    [39_550_247, 654_760_748],
]


def load_module() -> Any:
    spec = importlib.util.spec_from_file_location(
        "kb_reciprocal_p6_parent_verifier", PARENT_SCRIPT
    )
    require(spec is not None and spec.loader is not None, "parent import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


PARENT = load_module()
P = PARENT.P
Fp2 = PARENT.Fp2


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(data: dict[str, Any]) -> str:
    unsigned = {
        key: value for key, value in data.items() if key != "payload_sha256"
    }
    return hashlib.sha256(canonical_json(unsigned).encode()).hexdigest()


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def decode(value: list[int]) -> Any:
    require(
        isinstance(value, list)
        and len(value) == 2
        and all(isinstance(entry, int) for entry in value),
        "invalid F_p2 encoding",
    )
    return Fp2(value[0], value[1])


def encode(value: object) -> list[int]:
    element = Fp2.coerce(value)
    require(element is not NotImplemented, "cannot encode non-F_p2 value")
    return [element.a, element.b]


def encode_polynomial(polynomial: list[object]) -> list[list[int]]:
    return [encode(value) for value in polynomial]


def load_parent() -> dict[str, Any]:
    with PARENT_CERTIFICATE.open(encoding="utf-8") as handle:
        data = json.load(handle, object_pairs_hook=reject_duplicate_keys)
    PARENT.validate(data)
    require(data["payload_sha256"] == PARENT_PAYLOAD, "parent payload drift")
    return data


def polynomial_degree(polynomial: list[object]) -> int:
    return len(PARENT.poly_trim(polynomial, P)) - 1


def evaluate_bivariate_row(
    source: object,
    s_coefficients: list[object],
    p_coefficients: list[object],
) -> list[object]:
    s_value = PARENT.poly_eval(s_coefficients, source, P)
    p_value = PARENT.poly_eval(p_coefficients, source, P)
    return [
        Fp2(1),
        -s_value % P,
        (Fp2(2) + p_value) % P,
        -s_value % P,
        Fp2(1),
    ]


def source_records(parent: dict[str, Any]) -> list[dict[str, object]]:
    witness = parent["witness"]
    common = [
        {
            "role": "COMMON_INVARIANT_SOURCE",
            "label": root,
        }
        for root in COMMON_SOURCE_ROOTS
    ]
    extra = [
        {
            "role": "EXTRA_INVARIANT_SOURCE_ETA",
            "label": [witness["invariant_extra_label"], 0],
        }
    ]
    noninvariant = [
        {
            "role": "NONINVARIANT_ROW_SOURCE",
            "row": index,
            "label": [value, 0],
        }
        for index, value in enumerate(witness["alpha_noninvariant"])
    ]
    return [*common, *extra, *noninvariant]


def build_payload() -> dict[str, Any]:
    parent = load_parent()
    witness = parent["witness"]
    sources = source_records(parent)
    source_values = [decode(record["label"]) for record in sources]

    require(len(source_values) == 12, "complete source count")
    require(len(set(source_values)) == 12, "complete sources not distinct")

    common_locator = [
        Fp2(value)
        for value in witness["common_source_locator_coefficients"]
    ]
    common_values = [decode(root) for root in COMMON_SOURCE_ROOTS]
    require(
        all(PARENT.poly_eval(common_locator, value, P) == 0
            for value in common_values),
        "declared common source root is not on the quintic",
    )
    require(len(set(common_values)) == 5, "common source roots collide")
    require(
        PARENT.poly_gcd(
            common_locator, PARENT.poly_derivative(common_locator, P), P
        )
        == [Fp2(1)],
        "common source locator not reduced",
    )

    complete_source_polynomial: list[object] = [Fp2(1)]
    for source in source_values:
        complete_source_polynomial = PARENT.poly_mul(
            complete_source_polynomial,
            [-source % P, Fp2(0), Fp2(1)],
            P,
        )
    require(
        polynomial_degree(complete_source_polynomial) == 24,
        "complete source polynomial degree",
    )
    # The extra invariant label is eta=0, so its coordinate quadratic is
    # X^2.  Repeated roots within one z_i are allowed by the producer; the
    # other eleven coordinate quadratics are reduced and pairwise disjoint.
    require(
        PARENT.poly_gcd(
            complete_source_polynomial,
            PARENT.poly_derivative(complete_source_polynomial, P),
            P,
        )
        == [Fp2(0), Fp2(1)],
        "unexpected complete-source repeated-root locus",
    )

    s_coefficients = [
        Fp2(0, value)
        for value in witness["S_coefficient_multipliers"]
    ]
    p_coefficients = [
        Fp2(value) for value in witness["P_coefficients"]
    ]

    # Reconstruct the six committed rows from their exact pole factors.  This
    # binds the obstruction to the parent H rather than to an unrelated
    # quartic interpolation.
    factor_sequence = [
        Fp2(0, value)
        for value in witness["factor_sequence_multipliers"]
    ]
    path = parent["scope"]["signature_path"]
    row_factors: dict[int, tuple[object, object]] = {}
    for position, row in enumerate(path):
        row_factors[row] = (
            factor_sequence[position],
            factor_sequence[position + 1],
        )

    rows: list[dict[str, object]] = []
    for record, source in zip(sources, source_values, strict=True):
        h_row = evaluate_bivariate_row(
            source, s_coefficients, p_coefficients
        )
        require(polynomial_degree(h_row) == 4, "H row lost degree")
        gcd = PARENT.poly_gcd(h_row, complete_source_polynomial, P)
        degree = polynomial_degree(gcd)

        output = dict(record)
        output.update(
            {
                "H_row_coefficients": encode_polynomial(h_row),
                "gcd_with_complete_source_polynomial_coefficients":
                    encode_polynomial(gcd),
                "gcd_degree": degree,
                "passes_necessary_source_fiber_gate": degree == 4,
            }
        )
        rows.append(output)

        if record["role"] == "NONINVARIANT_ROW_SOURCE":
            row = int(record["row"])
            expected = PARENT.poly_mul(
                PARENT.quadratic(row_factors[row][0], P),
                PARENT.quadratic(row_factors[row][1], P),
                P,
            )
            require(h_row == expected, f"parent row {row} mismatch")

    histogram: dict[str, int] = {}
    for row in rows:
        key = str(row["gcd_degree"])
        histogram[key] = histogram.get(key, 0) + 1
    require(histogram == {"0": 6, "4": 6}, "gcd histogram")

    fatal_indices = [
        index
        for index, row in enumerate(rows)
        if not row["passes_necessary_source_fiber_gate"]
    ]
    require(fatal_indices == list(range(6)), "fatal source set")
    require(
        all(rows[index]["role"] != "NONINVARIANT_ROW_SOURCE"
            for index in fatal_indices),
        "a committed row unexpectedly fails",
    )

    data: dict[str, Any] = {
        "format":
            "kb-mca-v4-q6-u2-reciprocal-p6-source-fiber-obstruction-v1",
        "status":
            "PROVED_WITNESS_SPECIFIC_ACTIVE_SOURCE_FIBER_DELETION",
        "row": {
            "field_characteristic": P,
            "field_extension_degree": 6,
            "agreement": 1_116_048,
            "B_star": 274_980_728_111_395_087,
            "object": "MCA",
            "workboard_item": "K3",
        },
        "dependency": {
            "parent_pr": 1126,
            "parent_commit": PARENT_COMMIT,
            "parent_format": parent["format"],
            "parent_payload_sha256": parent["payload_sha256"],
            "source_reduction_commit": SOURCE_REDUCTION_COMMIT,
            "manual_integration_commit": MANUAL_INTEGRATION_COMMIT,
        },
        "producer_gate": {
            "producer":
                "M(T,X)=sum_i kappa_i L_i(T) B(X)/z_i(X)",
            "component_hypothesis": "H divides F_out divides M",
            "source_specialization":
                "M(alpha_i,X)=kappa_i B(X)/z_i(X)",
            "necessary_divisibility":
                "H(alpha_i,X) divides B(X) for every source alpha_i",
            "complete_source_divisor_model":
                "B(X)~prod_beta(X^2-beta) over all 12 source labels",
            "individual_noninvariant_coordinate_warning":
                "an individual z_i need not be one complete deck fiber",
            "complete_source_polynomial_degree": 24,
            "complete_source_polynomial_squarefree": False,
            "only_repeated_root": "[0:1] from z_eta(X)=X^2",
            "H_bidegree": [2, 4],
            "H_is_monic_in_X": True,
            "affine_gcd_is_complete_projective_test": True,
        },
        "field": {
            "quadratic_subfield_generator": "omega",
            "omega_square": witness["quadratic_subfield"]["omega_square"],
            "encoding": "[constant_coefficient,omega_coefficient]",
        },
        "H": {
            "S_coefficient_multipliers":
                witness["S_coefficient_multipliers"],
            "P_coefficients": witness["P_coefficients"],
            "formula":
                "X^4-S(T)X^3+(2+P(T))X^2-S(T)X+1",
        },
        "complete_source_polynomial_coefficients":
            encode_polynomial(complete_source_polynomial),
        "source_rows": rows,
        "obstruction": {
            "gcd_degree_histogram": histogram,
            "fatal_source_indices": fatal_indices,
            "fatal_source_roles": [
                "COMMON_INVARIANT_SOURCE",
                "EXTRA_INVARIANT_SOURCE_ETA",
            ],
            "passing_source_count": 6,
            "failing_source_count": 6,
            "terminal":
                "DELETED_BY_ACTIVE_SOURCE_FIBER_DIVISIBILITY",
            "witness_lifts_to_active_producer": False,
            "owner_id": None,
            "ledger_movement": 0,
            "active_ledger": {
                "U_paid": None,
                "U_Q": None,
                "U_BC": None,
                "U_new": None,
            },
        },
        "claims": {
            "parent_local_survivor_remains_valid": True,
            "parent_witness_is_active_producer_component": False,
            "all_twelve_source_fibers_checked": True,
            "source_fiber_gate_is_assignment_independent": True,
            "source_fiber_gate_is_scale_independent": True,
            "source_fiber_gate_is_projectively_invariant": True,
            "all_reciprocal_P6_components_eliminated": False,
            "same_record_owner_supplied": False,
            "row_payment": False,
        },
        "nonclaims": [
            "elimination of every reciprocal P6 component",
            "received-line witness",
            "bad-slope witness",
            "survival or deletion of every earlier first-match cell",
            "active owner payment",
            "cap-68 proof or refutation",
            "KoalaBear MCA row closure",
        ],
        "upstream_prs_checked": [1121, 1122, 1123, 1124, 1125, 1126],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def validate(data: dict[str, Any]) -> dict[str, Any]:
    expected = build_payload()
    require(data["payload_sha256"] == payload_hash(data), "payload hash")
    require(data == expected, "certificate differs from exact reconstruction")

    rows = data["source_rows"]
    require(len(rows) == 12, "source row count")
    require(
        all(
            row["gcd_degree"] == 0
            and not row["passes_necessary_source_fiber_gate"]
            for row in rows[:6]
        ),
        "fatal invariant-source rows",
    )
    require(
        all(
            row["gcd_degree"] == 4
            and row["passes_necessary_source_fiber_gate"]
            for row in rows[6:]
        ),
        "passing noninvariant rows",
    )
    obstruction = data["obstruction"]
    require(
        obstruction["terminal"]
        == "DELETED_BY_ACTIVE_SOURCE_FIBER_DIVISIBILITY",
        "terminal drift",
    )
    require(
        obstruction["witness_lifts_to_active_producer"] is False,
        "lift verdict drift",
    )
    require(obstruction["owner_id"] is None, "owner must remain null")
    require(obstruction["ledger_movement"] == 0, "ledger movement")
    return {
        "prime": P,
        "sources": len(rows),
        "passing": obstruction["passing_source_count"],
        "failing": obstruction["failing_source_count"],
        "histogram": obstruction["gcd_degree_histogram"],
        "terminal": obstruction["terminal"],
        "ledger_movement": obstruction["ledger_movement"],
    }


def mutate(
    data: dict[str, Any], path: tuple[object, ...], value: object
) -> dict[str, Any]:
    result = copy.deepcopy(data)
    target: Any = result
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    result["payload_sha256"] = payload_hash(result)
    return result


def tamper_selftest(data: dict[str, Any]) -> tuple[int, int]:
    tests = [
        ("status", ("status",), "OPEN"),
        ("prime", ("row", "field_characteristic"), P + 2),
        ("agreement", ("row", "agreement"), 1_116_047),
        ("budget", ("row", "B_star"), 274_980_728_111_395_086),
        ("object", ("row", "object"), "LIST"),
        ("parent-pr", ("dependency", "parent_pr"), 1125),
        ("parent-commit", ("dependency", "parent_commit"), "0" * 40),
        (
            "parent-payload",
            ("dependency", "parent_payload_sha256"),
            "0" * 64,
        ),
        (
            "source-commit",
            ("dependency", "source_reduction_commit"),
            "0" * 40,
        ),
        (
            "producer",
            ("producer_gate", "producer"),
            "candidate supplied producer",
        ),
        (
            "component",
            ("producer_gate", "component_hypothesis"),
            "H may not divide M",
        ),
        (
            "divisibility",
            ("producer_gate", "necessary_divisibility"),
            "H(alpha_i,X) divides B for some sources",
        ),
        (
            "omega-square",
            ("field", "omega_square"),
            1_923_159_405,
        ),
        (
            "S",
            ("H", "S_coefficient_multipliers", 0),
            190_235_002,
        ),
        ("P", ("H", "P_coefficients", 0), 1_619_401_243),
        (
            "B-coefficient",
            ("complete_source_polynomial_coefficients", 0, 0),
            1,
        ),
        ("source-label", ("source_rows", 0, "label", 0), 0),
        ("source-role", ("source_rows", 0, "role"), "NONINVARIANT"),
        (
            "H-row",
            ("source_rows", 0, "H_row_coefficients", 1, 1),
            1,
        ),
        (
            "gcd-coefficient",
            (
                "source_rows",
                0,
                "gcd_with_complete_source_polynomial_coefficients",
                0,
                0,
            ),
            0,
        ),
        ("gcd-degree", ("source_rows", 0, "gcd_degree"), 4),
        (
            "gate-verdict",
            ("source_rows", 0, "passes_necessary_source_fiber_gate"),
            True,
        ),
        (
            "histogram",
            ("obstruction", "gcd_degree_histogram", "0"),
            5,
        ),
        (
            "fatal-indices",
            ("obstruction", "fatal_source_indices", 5),
            6,
        ),
        (
            "passing-count",
            ("obstruction", "passing_source_count"),
            7,
        ),
        (
            "terminal",
            ("obstruction", "terminal"),
            "UNPAID_PRIMITIVE",
        ),
        (
            "lift",
            ("obstruction", "witness_lifts_to_active_producer"),
            True,
        ),
        ("owner", ("obstruction", "owner_id"), "FAKE_OWNER"),
        ("movement", ("obstruction", "ledger_movement"), 1),
        (
            "ledger",
            ("obstruction", "active_ledger", "U_paid"),
            0,
        ),
        (
            "parent-validity",
            ("claims", "parent_local_survivor_remains_valid"),
            False,
        ),
        (
            "global-elimination",
            ("claims", "all_reciprocal_P6_components_eliminated"),
            True,
        ),
        (
            "owner-claim",
            ("claims", "same_record_owner_supplied"),
            True,
        ),
        ("nonclaim", ("nonclaims", 0), "all P6 eliminated"),
        ("upstream-pr", ("upstream_prs_checked", 5), 1125),
    ]
    passed = 0
    for name, path, value in tests:
        candidate = mutate(data, path, value)
        try:
            validate(candidate)
        except (VerificationError, PARENT.VerificationError):
            passed += 1
        else:
            raise VerificationError(f"tamper survived: {name}")

    stale = copy.deepcopy(data)
    stale["status"] = "OPEN"
    try:
        validate(stale)
    except (VerificationError, PARENT.VerificationError):
        passed += 1
    else:
        raise VerificationError("tamper survived: stale payload hash")
    return passed, len(tests) + 1


def load_certificate() -> dict[str, Any]:
    with CERTIFICATE.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def write_certificate() -> None:
    data = build_payload()
    CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATE.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(CERTIFICATE)
    print(data["payload_sha256"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--print-hash", action="store_true")
    arguments = parser.parse_args()
    require(
        arguments.write
        or arguments.check
        or arguments.tamper_selftest
        or arguments.print_hash,
        "choose --write, --check, --tamper-selftest, or --print-hash",
    )
    if arguments.write:
        write_certificate()
    if arguments.check or arguments.tamper_selftest or arguments.print_hash:
        data = load_certificate()
        if arguments.print_hash:
            print(payload_hash(data))
        if arguments.check:
            summary = validate(data)
            print(
                "status="
                "PROVED_WITNESS_SPECIFIC_ACTIVE_SOURCE_FIBER_DELETION"
            )
            print(f"field=F_{summary['prime']}^2<=F_{summary['prime']}^6")
            print(f"source_rows={summary['sources']}")
            print(f"passing_source_rows={summary['passing']}")
            print(f"failing_source_rows={summary['failing']}")
            print(f"gcd_degree_histogram={summary['histogram']}")
            print(f"terminal={summary['terminal']}")
            print(f"ledger_movement={summary['ledger_movement']}")
        if arguments.tamper_selftest:
            passed, total = tamper_selftest(data)
            print(f"tamper_selftest={passed}/{total}")


if __name__ == "__main__":
    main()
