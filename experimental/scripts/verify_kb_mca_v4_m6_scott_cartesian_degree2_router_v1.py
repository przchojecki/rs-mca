#!/usr/bin/env python3
"""Verify the KoalaBear m6 Scott-Cartesian degree-two router."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from collections import deque
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
CERTIFICATE = ROOT / "data" / "certificates" / "kb-mca-v4-m6-scott-cartesian-degree2-router-v1" / "kb_mca_v4_m6_scott_cartesian_degree2_router_v1.json"
SCHEMA = "kb-mca-v4-m6-scott-cartesian-degree2-router-v1"
COMPILER_COMMIT = "e287c54252c7872e1745c7594cfef62b74a65cf5"
COMPILER_PATH = "experimental/data/certificates/kb-mca-v4-degree60-source-pencil-rank-compiler-v1/kb_mca_v4_degree60_source_pencil_rank_compiler_v1.json"
COMPILER_BLOB = "5c16c7884b349d7e474b8dfc1267ab357ef0d477"
COMPILER_PAYLOAD = "6d4bc83e40e491f02f7d265b021628ffb7d52b1978c0655f83e5a9d3e0a9f4bb"
FRONTIER_COMMIT = "412bc68f1dcb6ac3924d6445146417f3c713ef89"
FRONTIER_PATH = "experimental/data/certificates/kb-mca-v4-m10-scott-strip-lower-degree-router-v1/kb_mca_v4_m10_scott_strip_lower_degree_router_v1.json"
FRONTIER_BLOB = "6e49093fdb9d9e55b45c55265eb3cc0c0e65e8c9"
FRONTIER_PAYLOAD = "66117d7ba207a66606fc4ae4770a2b314b3510066be7af734b4e579d028ce1d1"
DEGREE5_COMMIT = "a14a05d9ba80068133e93e2fa77d6d1dc8828829"
DEGREE5_PATH = "experimental/data/certificates/kb-mca-v4-degree60-decomposition-source-fiber-adapter-v1/kb_mca_v4_degree60_decomposition_source_fiber_adapter_v1.json"
DEGREE5_BLOB = "911bac3c1c5d1b4cd9822c59939d60e832b7ef23"
DEGREE5_PAYLOAD = "638190df24415e5609fa9c2f50dde8fd22bd150f60e7bef5cd1496cb22d75b4e"
M6_ROWS = [[1, 24], [2, 12], [3, 8], [4, 6], [6, 4], [8, 3]]
CATALOGUE = [
    {"group": "A5", "order": 60, "socle": "A5", "subdegrees": [1, 5]},
    {"group": "S5", "order": 120, "socle": "A5", "subdegrees": [1, 5]},
    {"group": "A6", "order": 360, "socle": "A6", "subdegrees": [1, 5]},
    {"group": "S6", "order": 720, "socle": "A6", "subdegrees": [1, 5]},
]
TRANSITIVE_ORDERS = (
    10,10,20,20,40,50,60,80,100,100,120,120,120,160,160,160,200,200,200,200,
    200,240,320,320,320,360,400,400,640,720,720,720,800,960,1440,1920,1920,1920,
    3840,7200,14400,14400,28800,1814400,3628800,
)
EXPECTED_NONCLAIMS = [
    "No degree-two destination is deleted or paid.",
    "No endpoint-record census or carrier, data, explaining-polynomial, or slope bridge is claimed.",
    "No u=2, K3, or KoalaBear row closure is claimed.",
    "No ledger quantity moves.",
]

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))

def payload_hash(value: dict[str, Any]) -> str:
    unhashed = dict(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()

def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result

def parse_json(text: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(text, object_pairs_hook=reject_duplicates)
    except (json.JSONDecodeError, VerificationError) as error:
        raise VerificationError(f"cannot parse {label}: {error}") from error
    require(isinstance(value, dict), f"{label} is not an object")
    return value

def load_json(path: Path) -> dict[str, Any]:
    return parse_json(path.read_text(), str(path))

def git_output(*arguments: str) -> str:
    try:
        result = subprocess.run(["git", *arguments], cwd=REPO_ROOT, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return result.stdout.strip()

def exact_keys(value: Any, expected: set[str], label: str) -> None:
    require(isinstance(value, dict), f"{label} is not an object")
    actual = set(value)
    require(actual == expected, f"{label} keys: {sorted(actual ^ expected)}")

def verify_schema(data: dict[str, Any]) -> None:
    exact_keys(data, {"schema","payload_sha256","statement","parent_compiler","incoming_frontier","degree_five_import","degree_six_catalogue","kernel_free_gate","scott_cartesian_route","external_source_custody","source_bindings","conclusion","nonclaims"}, "certificate")
    exact_keys(data["statement"], {"workboard_item","row","object","agreement","B_star","endpoint_degree","original_inner_degree","original_outer_degree","status","ledger_movement"}, "statement")
    exact_keys(data["parent_compiler"], {"commit","certificate_path","certificate_blob_oid","certificate_payload_sha256","imported_terminal","imported_m6_rows"}, "parent compiler")
    exact_keys(data["incoming_frontier"], {"commit","certificate_path","certificate_blob_oid","certificate_payload_sha256","imported_terminal","global_transverse_type_count","live_inner_degrees"}, "incoming frontier")
    exact_keys(data["degree_five_import"], {"commit","certificate_path","certificate_blob_oid","certificate_payload_sha256","quantifier","terminal"}, "degree five")
    for index, row in enumerate(data["degree_six_catalogue"]):
        exact_keys(row, {"group","order","socle","subdegrees"}, f"catalogue {index}")
    exact_keys(data["kernel_free_gate"], {"transitive_degree_ten_group_count","required_group_order_divisor","candidate_indices","large_candidates","large_candidates_survive","wreath_chains","terminal"}, "kernel-free gate")
    for index, row in enumerate(data["kernel_free_gate"]["wreath_chains"]):
        exact_keys(row, {"group","G_order","block_stabilizer_order","quotient","endpoint_stabilizer_order","intermediate_order","intermediate_index","subdegrees"}, f"wreath {index}")
    exact_keys(data["scott_cartesian_route"], {"derived_kernel","subdirect_coordinate_count","simple_socles","socle_subdegrees","compatibility_partition_G_invariant","compatible_class_sizes_supporting_delta","actual_suborbit_size","size_five_terminal","size_ten_column_contains_delta","primitive_degree_ten_nontrivial_subdegrees","subdegree_four_present","proper_right_factor_degrees","surviving_inner_degree","terminal"}, "Scott route")
    exact_keys(data["external_source_custody"], {"gap_primgrp_commit","gap_degree6_entry_bytes","gap_degree6_entry_sha256","gap_transgrp_commit","gap_trans10_file_bytes","gap_trans10_file_sha256","scott_doi","scott_lemma_page"}, "external custody")
    for index, row in enumerate(data["source_bindings"]):
        exact_keys(row, {"binding_id","commit","path","blob_oid","role"}, f"binding {index}")
    exact_keys(data["conclusion"], {"routed_m6_rows","m6_terminal_type_count","remaining_global_transverse_type_count","remaining_inner_degrees","terminal","m6_routed","degree_two_closed","u2_closed","K3_closed","row_closed"}, "conclusion")
    require(isinstance(data["nonclaims"], list), "nonclaims")

def verify_semantics(data: dict[str, Any]) -> None:
    require(data["schema"] == SCHEMA, "schema")
    require(data["statement"] == {"workboard_item":"K3","row":"KoalaBear MCA at 2^-128","object":"MCA","agreement":1116048,"B_star":"274980728111395087","endpoint_degree":60,"original_inner_degree":6,"original_outer_degree":10,"status":"PROVED_M6_ROUTED_TO_INNER_DEGREE_2_OR_EXCLUDED_M5_OTHER_K3_ROWS_OPEN","ledger_movement":0}, "statement changed")
    require(data["degree_six_catalogue"] == CATALOGUE, "catalogue")
    require(all(row["subdegrees"] == [1,5] for row in CATALOGUE), "degree-six subdegrees")
    candidates = [index + 1 for index, order in enumerate(TRANSITIVE_ORDERS) if order % 600 == 0]
    gate = data["kernel_free_gate"]
    require(len(TRANSITIVE_ORDERS) == gate["transitive_degree_ten_group_count"] == 45, "transitive count")
    require(gate["required_group_order_divisor"] == 600, "order divisor")
    require(gate["candidate_indices"] == candidates == [40,41,42,43,44,45], "candidate indices")
    require(gate["large_candidates"] == ["A10","S10"], "large candidates")
    require(gate["large_candidates_survive"] is False, "large exclusion")
    expected = [
        ("[A5^2]2",7200,720,"A5",120,600),
        ("parity wreath, split",14400,1440,"S5",240,1200),
        ("parity wreath, twist",14400,1440,"S5",240,1200),
        ("[S5^2]2",28800,2880,"S5",480,2400),
    ]
    actual = [(r["group"],r["G_order"],r["block_stabilizer_order"],r["quotient"],r["endpoint_stabilizer_order"],r["intermediate_order"]) for r in gate["wreath_chains"]]
    require(actual == expected, "wreath table")
    for row in gate["wreath_chains"]:
        require(row["G_order"] // row["block_stabilizer_order"] == 10, "outer index")
        require(row["block_stabilizer_order"] // row["endpoint_stabilizer_order"] == 6, "inner index")
        require(row["intermediate_order"] // row["endpoint_stabilizer_order"] == row["intermediate_index"] == 5, "middle index")
        require(row["subdegrees"] == [1,5], "wreath subdegrees")
    require(gate["terminal"] == "KERNEL_FREE_M6_ROUTES_TO_EXCLUDED_M5", "kernel terminal")
    route = data["scott_cartesian_route"]
    require(route["derived_kernel"] == "D=[N,N]", "derived kernel")
    require(route["subdirect_coordinate_count"] == 10, "coordinates")
    require(route["simple_socles"] == ["A5","A6"], "socles")
    require(route["socle_subdegrees"] == [1,5], "socle subdegrees")
    require(route["compatibility_partition_G_invariant"] is True, "compatibility")
    require(route["compatible_class_sizes_supporting_delta"] == [5,10], "class sizes")
    require(route["actual_suborbit_size"] == 4, "actual suborbit")
    require(route["size_five_terminal"] == "INNER_DEGREE_FIVE_EXCLUDED", "size five")
    require(route["size_ten_column_contains_delta"] is True, "column containment")
    require(route["primitive_degree_ten_nontrivial_subdegrees"] == [3,6,9], "m10 subdegrees")
    require(route["subdegree_four_present"] is False, "subdegree four")
    require(route["proper_right_factor_degrees"] == [2,5], "right factors")
    require(route["surviving_inner_degree"] == 2, "surviving degree")
    require(route["terminal"] == "NONTRIVIAL_KERNEL_M6_ROUTES_TO_M2_OR_EXCLUDED_M5", "Scott terminal")
    conclusion = data["conclusion"]
    require(conclusion["routed_m6_rows"] == M6_ROWS, "m6 rows")
    require(all(r*d == 24 for r,d in M6_ROWS), "row arithmetic")
    require(conclusion["m6_terminal_type_count"] == 0, "terminal count")
    require(conclusion["remaining_global_transverse_type_count"] == 12 == 18-len(M6_ROWS), "remaining count")
    require(conclusion["remaining_inner_degrees"] == [2,3,4], "remaining degrees")
    require(conclusion["terminal"] == "M6_NO_TERMINAL_PRODUCER_ROUTES_TO_M2_OR_EXCLUDED_M5", "conclusion terminal")
    require(conclusion["m6_routed"] is True, "routed flag")
    for key in ("degree_two_closed","u2_closed","K3_closed","row_closed"):
        require(conclusion[key] is False, f"forbidden close {key}")
    require(data["nonclaims"] == EXPECTED_NONCLAIMS, "nonclaims")

def verify_parents(data: dict[str, Any], *, check_git: bool) -> None:
    parent = data["parent_compiler"]
    require(parent == {"commit":COMPILER_COMMIT,"certificate_path":COMPILER_PATH,"certificate_blob_oid":COMPILER_BLOB,"certificate_payload_sha256":COMPILER_PAYLOAD,"imported_terminal":"TRANSVERSE_OUTER_CORRESPONDENCE_UNPAID","imported_m6_rows":M6_ROWS}, "parent compiler")
    frontier = data["incoming_frontier"]
    require(frontier == {"commit":FRONTIER_COMMIT,"certificate_path":FRONTIER_PATH,"certificate_blob_oid":FRONTIER_BLOB,"certificate_payload_sha256":FRONTIER_PAYLOAD,"imported_terminal":"M10_NO_TERMINAL_PRODUCER_ROUTES_TO_M2_M3_M6","global_transverse_type_count":18,"live_inner_degrees":[2,3,4,6]}, "incoming frontier")
    degree5 = data["degree_five_import"]
    require(degree5 == {"commit":DEGREE5_COMMIT,"certificate_path":DEGREE5_PATH,"certificate_blob_oid":DEGREE5_BLOB,"certificate_payload_sha256":DEGREE5_PAYLOAD,"quantifier":"every geometric decomposition of the residual degree-60 endpoint map","terminal":"INNER_DEGREE_FIVE_EXCLUDED"}, "degree-five import")
    expected_bindings = [
        {"binding_id":"KB_M6_ROUTER::compiler_certificate","commit":COMPILER_COMMIT,"path":COMPILER_PATH,"blob_oid":COMPILER_BLOB,"role":"terminal m6 transverse rows and actual quartic suborbit"},
        {"binding_id":"KB_M6_ROUTER::incoming_frontier_certificate","commit":FRONTIER_COMMIT,"path":FRONTIER_PATH,"blob_oid":FRONTIER_BLOB,"role":"18-type frontier after m12 close and m10 routing"},
        {"binding_id":"KB_M6_ROUTER::degree5_certificate","commit":DEGREE5_COMMIT,"path":DEGREE5_PATH,"blob_oid":DEGREE5_BLOB,"role":"universal challenge-field deletion of inner degree five"},
    ]
    require(data["source_bindings"] == expected_bindings, "bindings")
    if not check_git:
        return
    for row in data["source_bindings"]:
        require(git_output("rev-parse", f"{row['commit']}:{row['path']}") == row["blob_oid"], f"binding {row['binding_id']}")
    compiler = parse_json(git_output("show", f"{COMPILER_COMMIT}:{COMPILER_PATH}"), "compiler")
    require(payload_hash(compiler) == compiler["payload_sha256"] == COMPILER_PAYLOAD, "compiler payload")
    historical_m6 = next(row for row in compiler["transverse_outer_terminal"]["rows"] if row["m"] == 6)
    require(historical_m6["r_delta"] == M6_ROWS, "historical m6 rows")
    prior = parse_json(git_output("show", f"{FRONTIER_COMMIT}:{FRONTIER_PATH}"), "frontier")
    require(payload_hash(prior) == prior["payload_sha256"] == FRONTIER_PAYLOAD, "frontier payload")
    require(prior["conclusion"]["remaining_global_transverse_type_count"] == 18, "historical frontier")
    source5 = parse_json(git_output("show", f"{DEGREE5_COMMIT}:{DEGREE5_PATH}"), "degree five")
    require(payload_hash(source5) == source5["payload_sha256"] == DEGREE5_PAYLOAD, "degree-five payload")
    profile5 = next(row for row in source5["profiles"] if row["inner_degree"] == 5)
    require(profile5["terminal"] == "DELETED_CHALLENGE_FIELD_FIFTH_POWER_FIBER_CONTRADICTION", "degree-five terminal")

N = 10
ODD_BLOCK = frozenset((0,2,4,6,8))
IDENTITY = tuple(range(N))

def cycle(*cycles: tuple[int, ...]) -> tuple[int, ...]:
    result = list(IDENTITY)
    for points in cycles:
        for a,b in zip(points, points[1:]+points[:1]):
            result[a-1] = b-1
    return tuple(result)

def multiply(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[i]] for i in range(N))

def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0]*N
    for i,x in enumerate(permutation): result[x] = i
    return tuple(result)

def closure(generators: tuple[tuple[int, ...], ...]) -> set[tuple[int, ...]]:
    steps = generators + tuple(inverse(g) for g in generators)
    elements = {IDENTITY}
    queue = deque([IDENTITY])
    while queue:
        element = queue.popleft()
        for generator in steps:
            product = multiply(element, generator)
            if product not in elements:
                elements.add(product)
                queue.append(product)
    return elements

FIVE = cycle((2,4,6,8,10))
FIVE_GROUP = closure((FIVE,))
GROUP_CASES = (
    ((FIVE,cycle((2,4,10)),cycle((1,6),(2,7),(3,8),(4,9),(5,10))),7200,720,120,600,60),
    ((FIVE,cycle((2,10),(5,7)),cycle((1,6),(2,7),(3,8),(4,9),(5,10))),14400,1440,240,1200,120),
    ((FIVE,cycle((1,6),(2,5,10,7),(3,8),(4,9))),14400,1440,240,1200,120),
    ((FIVE,cycle((2,10)),cycle((1,6),(2,7),(3,8),(4,9),(5,10))),28800,2880,480,2400,120),
)

def normalizes_five(permutation: tuple[int, ...]) -> bool:
    return multiply(multiply(permutation,FIVE),inverse(permutation)) in FIVE_GROUP

def coset_quotient(group: set[tuple[int, ...]], subgroup: set[tuple[int, ...]]) -> tuple[int,list[int]]:
    unseen = set(group)
    reps = []
    owner = {}
    while unseen:
        rep = IDENTITY if IDENTITY in unseen else min(unseen)
        coset = {multiply(x,rep) for x in subgroup}
        index = len(reps)
        reps.append(rep)
        for x in coset: owner[x] = index
        unseen -= coset
    require(len(reps) == 6, "coset count")
    remaining = set(range(6))
    subdegrees = []
    while remaining:
        point = min(remaining)
        orbit = {owner[multiply(reps[point],a)] for a in subgroup}
        remaining -= orbit
        subdegrees.append(len(orbit))
    core = {a for a in subgroup if all(owner[multiply(rep,a)] == i for i,rep in enumerate(reps))}
    return len(group)//len(core), sorted(subdegrees)

def verify_groups() -> None:
    for generators,go,bo,ao,mo,qo in GROUP_CASES:
        group = closure(generators)
        block_kernel = {g for g in group if frozenset(g[i] for i in ODD_BLOCK) == ODD_BLOCK}
        stabilizer = {g for g in group if g[0] == 0}
        endpoint = {g for g in stabilizer if normalizes_five(g)}
        middle = {g for g in block_kernel if normalizes_five(g)}
        require((len(group),len(stabilizer),len(endpoint),len(middle)) == (go,bo,ao,mo), "group chain")
        require(endpoint <= middle <= group, "chain inclusion")
        quotient, subdegrees = coset_quotient(stabilizer, endpoint)
        require((quotient,subdegrees) == (qo,[1,5]), "quotient action")

def verify_custody(data: dict[str, Any]) -> None:
    require(data["external_source_custody"] == {"gap_primgrp_commit":"5612e113d50ac23a7d10945383936e20440b4e14","gap_degree6_entry_bytes":321,"gap_degree6_entry_sha256":"00bc5cdf6d0d833236953b9462c7c595a28960407ab2ee89e1b44ae11c16f5b7","gap_transgrp_commit":"165fc21ff497b24b7a5975582b331e6692ba04f1","gap_trans10_file_bytes":7059,"gap_trans10_file_sha256":"e7d8189cac31fa4f5a0f830234080fbddf0d741ca27921ffc7946c24b22f51d0","scott_doi":"10.1090/pspum/037/604599","scott_lemma_page":328}, "external custody")

def verify_certificate(data: dict[str, Any], *, check_git: bool=True, run_groups: bool=True) -> None:
    verify_schema(data)
    require(payload_hash(data) == data["payload_sha256"], "payload hash")
    verify_semantics(data)
    verify_parents(data, check_git=check_git)
    verify_custody(data)
    if run_groups:
        verify_groups()

def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)

def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str,Callable[[dict[str,Any]],None]]] = [
        ("drop-group", lambda v: v["degree_six_catalogue"].pop()),
        ("add-subdegree-four", lambda v: v["degree_six_catalogue"][0]["subdegrees"].append(4)),
        ("candidate", lambda v: v["kernel_free_gate"]["candidate_indices"].append(39)),
        ("large-survives", lambda v: v["kernel_free_gate"].__setitem__("large_candidates_survive",True)),
        ("middle-index", lambda v: v["kernel_free_gate"]["wreath_chains"][0].__setitem__("intermediate_index",4)),
        ("drop-wreath", lambda v: v["kernel_free_gate"]["wreath_chains"].pop()),
        ("compatibility", lambda v: v["scott_cartesian_route"].__setitem__("compatibility_partition_G_invariant",False)),
        ("class-size", lambda v: v["scott_cartesian_route"]["compatible_class_sizes_supporting_delta"].append(2)),
        ("column", lambda v: v["scott_cartesian_route"].__setitem__("size_ten_column_contains_delta",False)),
        ("m10-four", lambda v: v["scott_cartesian_route"].__setitem__("subdegree_four_present",True)),
        ("right-factor", lambda v: v["scott_cartesian_route"].__setitem__("proper_right_factor_degrees",[5])),
        ("surviving", lambda v: v["scott_cartesian_route"].__setitem__("surviving_inner_degree",5)),
        ("parent", lambda v: v["parent_compiler"].__setitem__("certificate_payload_sha256","0"*64)),
        ("frontier", lambda v: v["incoming_frontier"].__setitem__("global_transverse_type_count",19)),
        ("degree5", lambda v: v["degree_five_import"].__setitem__("quantifier","one decomposition")),
        ("binding", lambda v: v["source_bindings"][0].__setitem__("blob_oid","0"*40)),
        ("count", lambda v: v["conclusion"].__setitem__("remaining_global_transverse_type_count",13)),
        ("close-m2", lambda v: v["conclusion"].__setitem__("degree_two_closed",True)),
        ("ledger", lambda v: v["statement"].__setitem__("ledger_movement",1)),
        ("drop-nonclaim", lambda v: v["nonclaims"].pop()),
        ("extra", lambda v: v.__setitem__("extra",1)),
    ]
    passed = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(original)
        mutate(candidate)
        reseal(candidate)
        try:
            verify_certificate(candidate, check_git=False, run_groups=False)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"tamper survived: {name}")
    bad_hash = copy.deepcopy(original)
    bad_hash["payload_sha256"] = "0"*64
    try:
        verify_certificate(bad_hash, check_git=False, run_groups=False)
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: payload")
    try:
        parse_json('{"x":1,"x":2}', "duplicate test")
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("duplicate key survived")
    return passed

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    arguments = parser.parse_args()
    if not arguments.check and not arguments.tamper_selftest:
        parser.error("at least one action is required")
    data = load_json(CERTIFICATE)
    verify_certificate(data)
    print("PASS: m6 routes to inner degree two or the excluded degree-five row")
    if arguments.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
