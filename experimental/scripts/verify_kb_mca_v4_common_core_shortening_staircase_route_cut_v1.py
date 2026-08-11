#!/usr/bin/env python3
"""Verify the KoalaBear v4 common-core shortening staircase route cut.

The checker uses exact integers throughout.  It binds the active-v4 source,
checks the cancellation/staircase contract, rejects chronology or unit drift,
and deliberately records zero global-ledger movement.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
BASE_HEAD = "c5f4ea7a0c78828c901ae5f3428894a8b2e2806b"
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-v4-common-core-shortening-staircase-route-cut-v1/manifest.json"


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_load_text(text: str) -> Any:
    try:
        return json.loads(
            text,
            object_pairs_hook=strict_pairs,
            parse_float=lambda value: (_ for _ in ()).throw(
                CheckError(f"floating JSON number forbidden: {value}")
            ),
            parse_constant=lambda value: (_ for _ in ()).throw(
                CheckError(f"non-finite JSON number forbidden: {value}")
            ),
        )
    except json.JSONDecodeError as exc:
        raise CheckError(f"invalid JSON: {exc}") from exc


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()


def payload_hash(manifest: dict[str, Any]) -> str:
    value = copy.deepcopy(manifest)
    value.pop("payload_sha256", None)
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode() + b"\0" + data
    ).hexdigest()


def git_show(commit: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{commit}:{path}"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(proc.returncode == 0, f"cannot read pinned source {commit}:{path}")
    return proc.stdout


def exact_keys(value: Any, keys: tuple[str, ...], label: str) -> None:
    require(type(value) is dict, f"{label} must be an object")
    require(tuple(value) == keys, f"{label} exact ordered key set")


def exact_equal(actual: Any, expected: Any, label: str) -> None:
    require(type(actual) is type(expected), f"{label} exact JSON type")
    if isinstance(expected, dict):
        exact_keys(actual, tuple(expected), label)
        for key in expected:
            exact_equal(actual[key], expected[key], f"{label}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"{label} list length")
        for index, (a, e) in enumerate(zip(actual, expected)):
            exact_equal(a, e, f"{label}[{index}]")
    else:
        require(actual == expected, f"{label} exact value")


def r_floor(n: int, m: int, c: int, order: int = 32) -> int:
    return (order * (m - c) + (n - c) - 1) // (n - c)


def affine_span_bound(R: int, d: int, s: int) -> int:
    value = Fraction(1, 1)
    for i in range(s + 1):
        value *= Fraction(R + i, d + i)
    return value.numerator // value.denominator


def cell_bound(R: int, d: int, s: int) -> int:
    return min(math.comb(R + s, d + s), math.comb(R + s, s + 1))


EXPECTED_CONTRACT = {
    "schema": "rs-mca-kb-v4-common-core-shortening-staircase-route-cut-v1",
    "artifact_kind": "SOURCE_BOUND_LOCAL_THEOREM_AND_MAXIMAL_ROUTE_CUT",
    "base": {
        "repository": "przchojecki/rs-mca",
        "head": BASE_HEAD,
        "head_is_exact_pr1160_head": True,
        "upstream_main_at_refresh": "93fba1be3f3299b0ba4708d88715377bbb656e45",
        "public_dag_head_at_refresh": "3edb8b31b6735a0a2302a578a21dc6e50bd64046",
    },
    "row": {
        "name": "KoalaBear MCA at 2^-128",
        "unit": "DISTINCT_FINITE_AFFINE_BAD_SLOPES_PER_ACTUAL_RECEIVED_LINE",
        "n": 2097152,
        "k": 1048576,
        "m": 1116048,
        "d": 67472,
        "R": 1048576,
        "t": 981104,
        "B_star": 274980728111395087,
    },
    "theorem": {
        "compiler": "REVERSIBLE_COMMON_CORE_SHORTENING_ADAPTER",
        "parameter_map": "(n,k,m)->(n-c,k-c,m-c)",
        "preserved_invariants": ["m-k", "n-k", "n-m"],
        "preserves_identical_slope": True,
        "preserves_same_support_noncontainment": True,
        "inverse_exists": True,
        "reverse_denominator_guard_required_on_deleted_core": True,
        "converse_requires_compatible_domain_extension": True,
        "chronology_preserved_globally": False,
    },
    "exact_boundaries": {
        "last_core_with_degree_at_least_18": 4130,
        "first_core_with_degree_17": 4131,
        "degree_at_core_k_minus_1": 3,
        "last_generic_cell_s": 2,
        "first_generic_failure_s": 3,
        "last_direction_separated_s": 13,
        "first_direction_separated_failure_s": 14,
        "J_13": 47876303026096432,
        "J_14": 743896698428332665,
        "J_13_slack": 227104425085298655,
        "J_14_slack": -468915970316937578,
        "jo_c_4131_ceiling_bit_length": 3765,
        "jo_c_4131_ceiling_decimal_digits": 1134,
        "jo_c_4131_multiplier_alone_exceeds_B_star": True,
    },
    "terminals": [
        "GLOBAL_AFFINE_PAID",
        "FIXED_CORE_GENERIC_PAID_S_LE_2",
        "DIRECTION_SEPARATED_PAID_3_LE_S_LE_13",
        "DIRECTION_LIST_SHORTENED_s",
        "COMMON_CORE_SHORTENED_s_GE_14",
    ],
    "chronology": {
        "first_missing_bridge": "STAIRCASE_ROUTE_LINE_LEVEL_DISJOINT_SELECTOR_FOR_VARYING_LOCAL_32_TUPLE_CORES",
        "U_S_movement": 0,
        "U_A_movement": 0,
        "U_E_movement": 0,
        "global_ledger_movement": 0,
        "KoalaBear_closed": False,
    },
}


SOURCE_EXPECTED = [
    {
        "binding_id": "ACTIVE_V4_SAE_AND_COMMON_CORE_SOURCE",
        "commit": BASE_HEAD,
        "path": "experimental/grande_finale.tex",
        "line_ranges": ["132-149", "1395-1426", "4724-4735", "5744-5781", "6040-6135", "6622-6651", "7082-7110", "7585-7617"],
        "git_blob_sha1": "5e0cb1bad6b40c4db39f6b4cb3e5316aebeafe2f",
        "sha256": "03b8806c5e71ebd41a97012fbdcc6442dabd4c8bf9383b7d832a48b0c55ce5ab",
    },
    {
        "binding_id": "COMMON_CORE_COVER_OBSTRUCTION",
        "commit": BASE_HEAD,
        "path": "experimental/notes/thresholds/common_core_cover_obstruction.md",
        "line_ranges": ["1-280"],
        "git_blob_sha1": "9cff201c7ebb424cdfb44958d768946707f7687e",
        "sha256": "550e4f8565dfde78fbbb6d0db871aae5fdbf057bd6d88aa814a0f3779fd029c1",
    },
    {
        "binding_id": "PR1160_NEAR_RATIONAL_CONTROL",
        "commit": BASE_HEAD,
        "path": "experimental/notes/thresholds/kb_mca_supportwise_near_rational_two_anchor_repair_v1.md",
        "line_ranges": ["57-164", "189-241"],
        "git_blob_sha1": "12bc4a0f06189829a9490928e4855d1aa958f940",
        "sha256": "7e75d67420f4ed37add3b4f6ea3aa45e043a782a6396f328b1e34ce659938989",
    },
    {
        "binding_id": "CAP25_SUPPORTWISE_MCA_DEFINITION",
        "commit": BASE_HEAD,
        "path": "tex/cs25_cap_v13_2.tex",
        "line_ranges": ["215-226"],
        "git_blob_sha1": "001c3898b6317911e487ee0199adcce701aaae57",
        "sha256": "009dd3221e7b70182242cc25e82c2451e3ef2f7d4970fa325c7e96a96adbe7c7",
    },
    {
        "binding_id": "JO_SHORTENING_TRANSFER_AND_TELESCOPING_FENCE",
        "commit": BASE_HEAD,
        "path": "RS_MCA_Paving_v9.2.tex",
        "line_ranges": ["2255-2309", "2365-2397"],
        "git_blob_sha1": "3381e130c691561974f645d4d832173784db2108",
        "sha256": "8e89be94dd6291dc5563897e72ae34b49880512cd37f72287b4288ff030cbbc0",
    },
]


def verify_math(contract: dict[str, Any]) -> None:
    row = contract["row"]
    n, k, m = row["n"], row["k"], row["m"]
    d, R, t, B = row["d"], row["R"], row["t"], row["B_star"]
    require(m - k == d, "d=m-k")
    require(n - k == R, "R=n-k")
    require(n - m == t, "t=n-m")

    last = max(c for c in range(k) if r_floor(n, m, c) >= 18)
    require(last == 4130, "exact degree-18 core boundary")
    require(r_floor(n, m, 4131) == 17, "c=4131 degree floor")
    require(r_floor(n, m, k - 1) == 3, "c=k-1 degree floor")
    require(32 * d - 2 * R == 61952, "order-32 invariant surplus")

    expected_cells = {
        1: (549756338176, 274980178355056911),
        2: (192154133857304576, 82826594254090511),
        3: (50372197381489643749376, -50371922400761532354289),
    }
    for s, (bound, slack) in expected_cells.items():
        actual = cell_bound(R, d, s)
        require(actual == bound, f"cell bound s={s}")
        require(B - actual == slack, f"cell slack s={s}")

    j13, j14 = affine_span_bound(R, d, 13), affine_span_bound(R, d, 14)
    require(j13 == 47876303026096432, "J_13")
    require(j14 == 743896698428332665, "J_14")
    require(B - j13 == 227104425085298655, "J_13 slack")
    require(B - j14 == -468915970316937578, "J_14 slack")

    c = 4131
    numerator, denominator = math.comb(n, c), math.comb(m, c)
    ceiling = (numerator + denominator - 1) // denominator
    require(numerator > B * denominator, "Jo cross-product budget obstruction")
    require(ceiling.bit_length() == 3765, "Jo ceiling bit length")
    require(len(str(ceiling)) == 1134, "Jo ceiling decimal digits")


def verify_sources(bindings: list[dict[str, Any]]) -> None:
    exact_equal(bindings, SOURCE_EXPECTED, "source_bindings")
    for item in bindings:
        pinned = git_show(item["commit"], item["path"])
        current = (ROOT / item["path"]).read_bytes()
        require(current == pinned, f"current bytes equal pin: {item['path']}")
        require(git_blob_sha1(pinned) == item["git_blob_sha1"], "git blob pin")
        require(sha256(pinned) == item["sha256"], "sha256 pin")
        line_count = len(pinned.decode().splitlines())
        for line_range in item["line_ranges"]:
            match = re.fullmatch(r"([0-9]+)-([0-9]+)", line_range)
            require(match is not None, f"invalid line range: {line_range}")
            lo, hi = map(int, match.groups())
            require(1 <= lo <= hi <= line_count, f"out-of-range pin: {line_range}")


def verify_manifest(manifest: dict[str, Any], check_files: bool = True) -> None:
    keys = tuple(EXPECTED_CONTRACT) + (
        "source_bindings",
        "packet_files",
        "packet_file_sha256",
        "payload_sha256",
    )
    exact_keys(manifest, keys, "manifest")
    exact_equal(
        {key: manifest[key] for key in EXPECTED_CONTRACT},
        EXPECTED_CONTRACT,
        "semantic_contract",
    )
    verify_math(manifest)
    verify_sources(manifest["source_bindings"])
    require(type(manifest["packet_files"]) is list, "packet_files list")
    require(len(set(manifest["packet_files"])) == len(manifest["packet_files"]), "unique packet files")
    require(
        tuple(manifest["packet_file_sha256"]) == tuple(manifest["packet_files"]),
        "packet hash keys and order",
    )
    if check_files:
        for relpath in manifest["packet_files"]:
            require(".." not in Path(relpath).parts, "packet path traversal")
            require(
                sha256((ROOT / relpath).read_bytes())
                == manifest["packet_file_sha256"][relpath],
                f"packet hash: {relpath}",
            )
    require(payload_hash(manifest) == manifest["payload_sha256"], "payload hash")


def mutation_tests(manifest: dict[str, Any]) -> int:
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda m: m["row"].__setitem__("unit", "WITNESSES"),
        lambda m: m["row"].__setitem__("B_star", m["row"]["B_star"] + 1),
        lambda m: m["theorem"].__setitem__("preserves_identical_slope", False),
        lambda m: m["theorem"].__setitem__("chronology_preserved_globally", True),
        lambda m: m["exact_boundaries"].__setitem__("last_core_with_degree_at_least_18", 4131),
        lambda m: m["exact_boundaries"].__setitem__("first_direction_separated_failure_s", 15),
        lambda m: m["exact_boundaries"].__setitem__("J_14", m["exact_boundaries"]["J_14"] - 1),
        lambda m: m["exact_boundaries"].__setitem__("jo_c_4131_ceiling_bit_length", 3764),
        lambda m: m["chronology"].__setitem__("U_E_movement", 1),
        lambda m: m["chronology"].__setitem__("KoalaBear_closed", True),
        lambda m: m["terminals"].append("SILENTLY_PAID_PRIMITIVE"),
        lambda m: m["source_bindings"][0].__setitem__("sha256", "0" * 64),
        lambda m: m["source_bindings"][1].__setitem__("path", "experimental/grande_finale.tex"),
        lambda m: m["packet_files"].append(m["packet_files"][0]),
        lambda m: m.__setitem__("silent_global_claim", True),
    ]
    rejected = 0
    for mutate in mutations:
        changed = copy.deepcopy(manifest)
        mutate(changed)
        changed["payload_sha256"] = payload_hash(changed)
        try:
            verify_manifest(changed, check_files=False)
        except CheckError:
            rejected += 1
    require(rejected == len(mutations), "all semantic mutations rejected")
    duplicate = MANIFEST.read_text().replace(
        '"schema": "rs-mca-kb-v4-common-core-shortening-staircase-route-cut-v1",',
        '"schema": "duplicate",\n  "schema": "rs-mca-kb-v4-common-core-shortening-staircase-route-cut-v1",',
        1,
    )
    try:
        strict_load_text(duplicate)
    except CheckError:
        rejected += 1
    require(rejected == len(mutations) + 1, "duplicate key rejected")
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    manifest = strict_load_text(MANIFEST.read_text())
    verify_manifest(manifest)
    rejected = mutation_tests(manifest) if args.tamper_selftest else 0
    row = manifest["row"]
    print("PASS kb-mca-v4-common-core-shortening-staircase-route-cut-v1")
    print(f"row={(row['n'], row['k'], row['m'])} B_star={row['B_star']}")
    print("degree18_last_core=4130 first_degree17_core=4131")
    print("generic_last_s=2 direction_separated_last_s=13 first_unpaid_s=14")
    print("Jo_c4131_ceiling_bits=3765 global_ledger_movement=0")
    if args.tamper_selftest:
        print(f"mutations_rejected={rejected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
