#!/usr/bin/env python3
"""Verify the KoalaBear m12 outer normal-form compiler."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from collections import defaultdict
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path
from typing import Any, Callable


if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-m12-outer-normal-form-compiler-v1"
    / "kb_mca_v4_m12_outer_normal_form_compiler_v1.json"
)
SCHEMA = "kb-mca-v4-m12-outer-normal-form-compiler-v1"
STATUS = "PROVED_M12_OUTER_NORMAL_FORM_COMPILER_ROW_OPEN"
PARENT_HEAD = "e368e5c8fc101ae0040b47265c2cd167e70dadd2"
PARENT_PATH = (
    "experimental/data/certificates/"
    "kb-mca-v4-m12-outer-subdegree-route-cut-v1/"
    "kb_mca_v4_m12_outer_subdegree_route_cut_v1.json"
)
PARENT_BLOB = "6ea55700f303869a850c79c66c331842e0eed385"
PARENT_PAYLOAD = (
    "4349f6ca07b991fe78b90c66feb1fdcb1df582ac19d34c50d354c3c91c9e6b63"
)
PARENT_TERMINAL = "M12_TRANSVERSE_TYPES_R2_R4_UNPAID"
ACTUAL_HEAD = "59c4449ca0f5cee929dd39fc7b5ae8b0a33877f4"
ACTUAL_PATH = (
    "experimental/notes/frontier-adjacent/"
    "kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.md"
)
ACTUAL_BLOB = "5d0ec0315fca34de80c22983b76bbafa12dd5661"

BRANCH_ROWS = [
    {"group_order": 60, "group": "A5", "finite_cycle_types": [[2, 2], [3]], "outer_genus": 0, "ordered_tuples": 10, "survives_genus_gate": True},
    {"group_order": 60, "group": "A5", "finite_cycle_types": [[3], [3]], "outer_genus": 1, "ordered_tuples": 5, "survives_genus_gate": True},
    {"group_order": 120, "group": "S5", "finite_cycle_types": [[2], [3, 2]], "outer_genus": 0, "ordered_tuples": 10, "survives_genus_gate": True},
    {"group_order": 120, "group": "S5", "finite_cycle_types": [[2], [4]], "outer_genus": 0, "ordered_tuples": 10, "survives_genus_gate": True},
    {"group_order": 120, "group": "S5", "finite_cycle_types": [[2], [2], [2, 2]], "outer_genus": 1, "ordered_tuples": 75, "survives_genus_gate": True},
    {"group_order": 120, "group": "S5", "finite_cycle_types": [[2], [2], [3]], "outer_genus": 2, "ordered_tuples": 75, "survives_genus_gate": False},
    {"group_order": 120, "group": "S5", "finite_cycle_types": [[2], [2], [2], [2]], "outer_genus": 3, "ordered_tuples": 125, "survives_genus_gate": False},
]
NORMAL_FORMS = [
    {"r": 2, "group": "D5", "finite_cycle_types": [[2, 2], [2, 2]], "form": "x^5-5*a*x^3+5*a^2*x", "parameter_condition": "a!=0", "rigid_affine_class": True},
    {"r": 4, "group": "A5", "finite_cycle_types": [[2, 2], [3]], "form": "x^3*(12*x^2-15*(1+t)*x+20*t)", "parameter_condition": "3*t^2+4*t+3=0", "rigid_affine_class": True},
    {"r": 4, "group": "A5", "finite_cycle_types": [[3], [3]], "form": "x^3*(6*x^2-15*x+10)", "parameter_condition": "none", "rigid_affine_class": True},
    {"r": 4, "group": "S5", "finite_cycle_types": [[2], [3, 2]], "form": "x^3*(x-1)^2", "parameter_condition": "none", "rigid_affine_class": True},
    {"r": 4, "group": "S5", "finite_cycle_types": [[2], [4]], "form": "x^4*(5-4*x)", "parameter_condition": "none", "rigid_affine_class": True},
    {"r": 4, "group": "S5", "finite_cycle_types": [[2], [2], [2, 2]], "form": "x^2*(x-1)^2*(2*x-5*t)", "parameter_condition": "open branch-profile locus", "rigid_affine_class": False},
]
NONCLAIMS = [
    "No normalizing affine map is silently descended to the challenge field.",
    "No family is deleted or realized by a supplied endpoint record.",
    "No parameter-to-carrier, received-data, explaining-polynomial, or slope bridge is proved.",
    "No inner-degree-twelve, u=2, K3, or KoalaBear row closure is claimed.",
    "No ledger quantity moves.",
]
EXPECTED_BINDINGS = [
    {"binding_id": "KB_M12_NORMAL_FORMS::parent_certificate", "commit": PARENT_HEAD, "path": PARENT_PATH, "blob_oid": PARENT_BLOB, "role": "surviving m12 transverse types and outer divisor profile"},
    {"binding_id": "KB_M12_NORMAL_FORMS::actual_curve_source", "commit": ACTUAL_HEAD, "path": ACTUAL_PATH, "blob_oid": ACTUAL_BLOB, "role": "bidegree-(2,4) actual component and birational endpoint lift"},
]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = dict(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json_text(text: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(text, object_pairs_hook=reject_duplicate_pairs)
    except (json.JSONDecodeError, VerificationError) as error:
        raise VerificationError(f"cannot parse {label}: {error}") from error
    require(isinstance(value, dict), f"{label} must be an object")
    return value


def load_json(path: Path) -> dict[str, Any]:
    try:
        return parse_json_text(path.read_text(), str(path))
    except OSError as error:
        raise VerificationError(f"cannot read {path}") from error


def git_output(*arguments: str) -> str:
    try:
        completed = subprocess.run(
            ["git", *arguments], cwd=REPO_ROOT, check=True,
            capture_output=True, text=True,
        )
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return completed.stdout.strip()


def exact_keys(value: Any, expected: set[str], label: str) -> None:
    require(isinstance(value, dict), f"{label} must be an object")
    require(set(value) == expected, f"{label} keys changed")


def exact_schema(data: dict[str, Any]) -> None:
    exact_keys(data, {
        "schema", "payload_sha256", "statement", "parent_stack",
        "actual_curve_genus_gate", "branch_cycle_ledger", "normal_forms",
        "dickson_divided_difference", "source_bindings", "conclusion",
        "nonclaims",
    }, "certificate")
    exact_keys(data["statement"], {
        "workboard_item", "row", "object", "inner_degree",
        "surviving_transverse_types", "status", "ledger_movement",
    }, "statement")
    exact_keys(data["parent_stack"], {
        "head_commit", "certificate_path", "certificate_blob_oid",
        "certificate_payload_sha256", "imported_terminal",
    }, "parent_stack")
    exact_keys(data["actual_curve_genus_gate"], {
        "source_bidegree", "birational_to_endpoint_component",
        "source_arithmetic_genus", "r4_map_degree",
        "outer_genus_upper_bound", "terminal",
    }, "actual_curve_genus_gate")
    exact_keys(data["branch_cycle_ledger"], {
        "infinity_cycle_type", "infinity_index", "finite_index_sum",
        "ordered_pair_degree", "ordered_pair_indices",
        "admissible_ordered_tuple_count", "rows", "AGL_1_5_occurs",
    }, "branch_cycle_ledger")
    for index, row in enumerate(data["branch_cycle_ledger"]["rows"]):
        exact_keys(row, {
            "group_order", "group", "finite_cycle_types", "outer_genus",
            "ordered_tuples", "survives_genus_gate",
        }, f"branch row {index}")
    for index, row in enumerate(data["normal_forms"]):
        exact_keys(row, {
            "r", "group", "finite_cycle_types", "form",
            "parameter_condition", "rigid_affine_class",
        }, f"normal form {index}")
    exact_keys(data["dickson_divided_difference"], {
        "sqrt_relation", "factor_one", "factor_two", "factor_bidegrees",
    }, "dickson_divided_difference")
    exact_keys(data["conclusion"], {
        "geometric_family_count", "rigid_affine_class_count",
        "one_parameter_family_count", "terminal",
        "challenge_field_classifier_proved", "family_deleted", "m12_closed",
        "u2_closed", "K3_closed", "row_closed",
    }, "conclusion")


IDENTITY = tuple(range(5))
INFINITY = (1, 2, 3, 4, 0)
S5 = list(permutations(range(5)))


def compose(left, right):
    return tuple(left[right[index]] for index in range(5))


def inverse(permutation):
    result = [0] * 5
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def cycles(permutation):
    seen = set()
    result = []
    for start in range(5):
        if start in seen:
            continue
        cycle = []
        point = start
        while point not in seen:
            seen.add(point)
            cycle.append(point)
            point = permutation[point]
        result.append(cycle)
    return result


def permutation_index(permutation):
    return 5 - len(cycles(permutation))


def cycle_type(permutation):
    values = sorted((len(cycle) for cycle in cycles(permutation) if len(cycle) > 1), reverse=True)
    return tuple(values) if values else (1,)


def generated_group(generators):
    generators = [*generators, *(inverse(item) for item in generators)]
    group = {IDENTITY}
    frontier = [IDENTITY]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            candidate = compose(generator, current)
            if candidate not in group:
                group.add(candidate)
                frontier.append(candidate)
    return group


def subdegrees(group):
    stabilizer = [item for item in group if item[0] == 0]
    unseen = set(range(5))
    result = []
    while unseen:
        seed = min(unseen)
        orbit = {item[seed] for item in stabilizer}
        result.append(len(orbit))
        unseen -= orbit
    return tuple(sorted(result))


def pair_index(permutation):
    unseen = {(i, j) for i in range(5) for j in range(5) if i != j}
    count = 0
    while unseen:
        current = next(iter(unseen))
        count += 1
        while current in unseen:
            unseen.remove(current)
            current = (permutation[current[0]], permutation[current[1]])
    return 20 - count


def compositions(total, prefix=()):
    if total == 0:
        yield prefix
    elif len(prefix) < 4:
        for part in range(1, total + 1):
            yield from compositions(total - part, prefix + (part,))


def verify_branch_ledger(data: dict[str, Any]) -> None:
    ledger = data["branch_cycle_ledger"]
    require(ledger["infinity_cycle_type"] == [5], "infinity type")
    require(ledger["infinity_index"] == 4, "infinity index")
    require(ledger["finite_index_sum"] == 4, "finite index sum")
    require(ledger["ordered_pair_degree"] == 20, "pair degree")
    require(ledger["ordered_pair_indices"] == {
        "2": 7, "2,2": 10, "3": 12, "3,2": 15, "4": 15, "5": 16,
    }, "pair index table")
    require(ledger["rows"] == BRANCH_ROWS, "branch rows")
    require(ledger["AGL_1_5_occurs"] is False, "AGL flag")

    by_index = {value: [item for item in S5 if permutation_index(item) == value] for value in range(1, 5)}
    summary = defaultdict(int)
    target = inverse(INFINITY)
    for composition in compositions(4):
        for finite_tuple in product(*(by_index[value] for value in composition)):
            finite_product = IDENTITY
            for item in finite_tuple:
                finite_product = compose(finite_product, item)
            if finite_product != target:
                continue
            group = generated_group([INFINITY, *finite_tuple])
            if subdegrees(group) != (1, 4):
                continue
            induced = sum(pair_index(item) for item in (INFINITY, *finite_tuple))
            genus = 1 - 20 + induced // 2
            profile = tuple(sorted(cycle_type(item) for item in finite_tuple))
            summary[(len(group), profile, genus)] += 1

    expected = {
        (row["group_order"], tuple(tuple(item) for item in row["finite_cycle_types"]), row["outer_genus"]): row["ordered_tuples"]
        for row in BRANCH_ROWS
    }
    require(dict(summary) == expected, "enumerated branch summary")
    require(sum(summary.values()) == ledger["admissible_ordered_tuple_count"] == 310, "tuple total")
    require(all(order != 20 for order, _, _ in summary), "AGL tuple found")


Q = Fraction


def poly_mul(left, right):
    result = [Q(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def derivative(polynomial):
    return [index * polynomial[index] for index in range(1, len(polynomial))]


def evaluate(polynomial, value):
    result = Q(0)
    for coefficient in reversed(polynomial):
        result = result * value + coefficient
    return result


def verify_normal_forms(data: dict[str, Any]) -> None:
    require(data["normal_forms"] == NORMAL_FORMS, "normal forms changed")
    require(sum(row["rigid_affine_class"] for row in NORMAL_FORMS) == 5, "rigid count")

    a5_33 = [Q(0), Q(0), Q(0), Q(10), Q(-15), Q(6)]
    require(derivative(a5_33) == poly_mul([Q(0), Q(0), Q(30)], [Q(1), Q(-2), Q(1)]), "A5 (3),(3)")
    require(evaluate(a5_33, 0) == 0 and evaluate(a5_33, 1) == 1, "A5 values")

    s5_32 = poly_mul([Q(0), Q(0), Q(0), Q(1)], [Q(1), Q(-2), Q(1)])
    require(derivative(s5_32) == poly_mul([Q(0), Q(0), Q(1)], poly_mul([Q(-1), Q(1)], [Q(-3), Q(5)])), "S5 (3,2)")
    require(evaluate(s5_32, 0) == evaluate(s5_32, 1) == 0, "S5 common value")

    s5_42 = [Q(0), Q(0), Q(0), Q(0), Q(5), Q(-4)]
    require(derivative(s5_42) == [Q(0), Q(0), Q(0), Q(20), Q(-20)], "S5 (4)")

    # The A5 parameter satisfies t^2=-1-(4/3)t. Evaluate the two critical values in this quadratic algebra.
    def add(left, right): return (left[0] + right[0], left[1] + right[1])
    def mul(left, right):
        return (left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0] - Q(4, 3) * left[1] * right[1])
    def scale(value, scalar): return (scalar * value[0], scalar * value[1])
    t = (Q(0), Q(1)); one = (Q(1), Q(0))
    coefficients = [(0, 0), (0, 0), (0, 0), scale(t, 20), scale(add(one, t), -15), (12, 0)]
    def qeval(value):
        result = (Q(0), Q(0))
        for coefficient in reversed(coefficients): result = add(mul(result, value), coefficient)
        return result
    require(qeval(one) == qeval(t), "A5 repeated critical value")

    # One-parameter derivative identity, checked at three exact parameters.
    for parameter in (Q(-2, 3), Q(1, 7), Q(11, 10)):
        p = poly_mul(poly_mul([0, 0, 1], [1, -2, 1]), [-5 * parameter, 2])
        expected = poly_mul([0, 2], poly_mul([-1, 1], [5 * parameter, -(10 * parameter + 3), 5]))
        require(derivative(p) == expected, "one-parameter derivative")
        require(evaluate(p, 0) == evaluate(p, 1) == 0, "one-parameter common value")

    factor = data["dickson_divided_difference"]
    require(factor == {
        "sqrt_relation": "s^2=5",
        "factor_one": "x^2+((1+s)/2)*x*y+y^2+((-5+s)/2)*a",
        "factor_two": "x^2+((1-s)/2)*x*y+y^2+((-5-s)/2)*a",
        "factor_bidegrees": [[2, 2], [2, 2]],
    }, "Dickson factors")
    A=(Q(1,2),Q(1,2)); C=(Q(1,2),Q(-1,2)); B=(Q(-5,2),Q(1,2)); D=(Q(-5,2),Q(-1,2))
    def s_add(x,y): return (x[0]+y[0],x[1]+y[1])
    def s_mul(x,y): return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
    require(s_add(A,C)==(1,0) and s_add(s_mul(A,C),(2,0))==(1,0), "Dickson quartic terms")
    require(s_add(B,D)==(-5,0) and s_add(s_mul(A,D),s_mul(B,C))==(-5,0) and s_mul(B,D)==(5,0), "Dickson a terms")


def verify_certificate(data: dict[str, Any], *, check_git: bool = True) -> None:
    exact_schema(data)
    require(data["schema"] == SCHEMA, "schema")
    digest = data["payload_sha256"]
    require(isinstance(digest, str) and len(digest) == 64 and all(c in "0123456789abcdef" for c in digest), "payload format")
    require(payload_hash(data) == digest, "payload hash")
    statement = data["statement"]
    require(statement == {
        "workboard_item": "K3", "row": "KoalaBear MCA at 2^-128",
        "object": "MCA", "inner_degree": 12,
        "surviving_transverse_types": [[2,24],[4,12]],
        "status": STATUS, "ledger_movement": 0,
    }, "statement")
    require(data["parent_stack"] == {
        "head_commit": PARENT_HEAD, "certificate_path": PARENT_PATH,
        "certificate_blob_oid": PARENT_BLOB,
        "certificate_payload_sha256": PARENT_PAYLOAD,
        "imported_terminal": PARENT_TERMINAL,
    }, "parent")
    genus = data["actual_curve_genus_gate"]
    require(genus == {
        "source_bidegree": [2,4], "birational_to_endpoint_component": True,
        "source_arithmetic_genus": 3, "r4_map_degree": 12,
        "outer_genus_upper_bound": 1,
        "terminal": "M12_R4_OUTER_GENUS_AT_MOST_ONE",
    }, "genus gate")
    require(2*3-2 < 12*(2*2-2), "genus arithmetic")
    verify_branch_ledger(data)
    verify_normal_forms(data)
    require(data["source_bindings"] == EXPECTED_BINDINGS, "bindings")
    conclusion = data["conclusion"]
    require(conclusion == {
        "geometric_family_count": 6, "rigid_affine_class_count": 5,
        "one_parameter_family_count": 1,
        "terminal": "M12_SIX_GEOMETRIC_OUTER_FAMILIES_UNPAID",
        "challenge_field_classifier_proved": False, "family_deleted": False,
        "m12_closed": False, "u2_closed": False, "K3_closed": False,
        "row_closed": False,
    }, "conclusion")
    require(data["nonclaims"] == NONCLAIMS, "nonclaims")
    if check_git:
        for binding in EXPECTED_BINDINGS:
            git_output("cat-file", "-e", f"{binding['commit']}^{{commit}}")
            require(git_output("rev-parse", f"{binding['commit']}:{binding['path']}") == binding["blob_oid"], f"binding {binding['binding_id']}")
        parent = parse_json_text(git_output("show", f"{PARENT_HEAD}:{PARENT_PATH}"), "parent")
        require(payload_hash(parent) == parent["payload_sha256"] == PARENT_PAYLOAD, "parent payload")
        require(parent["conclusion"]["terminal"] == PARENT_TERMINAL, "parent terminal")


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("genus", lambda x: x["actual_curve_genus_gate"].__setitem__("outer_genus_upper_bound", 2)),
        ("branch-row", lambda x: x["branch_cycle_ledger"]["rows"][0].__setitem__("outer_genus", 1)),
        ("restore-high-genus", lambda x: x["branch_cycle_ledger"]["rows"][5].__setitem__("survives_genus_gate", True)),
        ("AGL", lambda x: x["branch_cycle_ledger"].__setitem__("AGL_1_5_occurs", True)),
        ("tuple-count", lambda x: x["branch_cycle_ledger"].__setitem__("admissible_ordered_tuple_count", 309)),
        ("normal-form", lambda x: x["normal_forms"][2].__setitem__("form", "x^5")),
        ("rigid-count", lambda x: x["normal_forms"][5].__setitem__("rigid_affine_class", True)),
        ("Dickson-factor", lambda x: x["dickson_divided_difference"].__setitem__("sqrt_relation", "s^2=-5")),
        ("parent", lambda x: x["parent_stack"].__setitem__("certificate_payload_sha256", "0"*64)),
        ("binding", lambda x: x["source_bindings"][0].__setitem__("blob_oid", "0"*40)),
        ("field-claim", lambda x: x["conclusion"].__setitem__("challenge_field_classifier_proved", True)),
        ("delete-family", lambda x: x["conclusion"].__setitem__("family_deleted", True)),
        ("row-close", lambda x: x["conclusion"].__setitem__("row_closed", True)),
        ("drop-nonclaim", lambda x: x["nonclaims"].pop()),
        ("extra", lambda x: x.__setitem__("extra", 1)),
    ]
    passed = 0
    for name, mutation in mutations:
        candidate = copy.deepcopy(original); mutation(candidate); reseal(candidate)
        try: verify_certificate(candidate, check_git=False)
        except VerificationError: passed += 1
        else: raise VerificationError(f"tamper survived: {name}")
    bad = copy.deepcopy(original); bad["payload_sha256"] = "0"*64
    try: verify_certificate(bad, check_git=False)
    except VerificationError: passed += 1
    else: raise VerificationError("tamper survived: hash")
    try: parse_json_text('{"x":1,"x":2}', "duplicate")
    except VerificationError: passed += 1
    else: raise VerificationError("tamper survived: duplicate key")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    arguments = parser.parse_args()
    if not arguments.check and not arguments.tamper_selftest:
        parser.error("at least one mode is required")
    certificate = load_json(CERTIFICATE)
    verify_certificate(certificate)
    print("PASS: m12 survivors compiled to six geometric outer normal forms")
    if arguments.tamper_selftest:
        count = tamper_selftest(certificate)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
