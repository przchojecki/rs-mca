#!/usr/bin/env python3
"""Verify the KoalaBear actual-record dimension-sensitivity audit.

This checker deliberately validates an actual MCA witness and exact
noninvariance under the two printed dimension conventions. It does not
promote profile membership to a frozen Q/BC owner or treat schema parsing as
a proof of K3.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "experimental/data/certificates/kb-mca-v4-k3-actual-record-source-dimension-route-cut-v1/manifest.json"
SCHEMA_PATH = ROOT / "experimental/data/schemas/kb_mca_v4_k3_actual_record_source_dimension_route_cut_v1.schema.json"

P = 2_130_706_433
N = 2_097_152
K_CODE = 1_048_576
M = 1_116_048
OMEGA = N - M
K_EFF = K_CODE + 1
W_CODE = M - K_CODE
W_EFF = M - K_EFF
E = 67_473
ZETA = 1_213_133_211
Q = P**6
B_STAR = Q // 2**128
U_PAID = N - M
RESERVE = B_STAR - U_PAID
MODULUS = [6, 1, 0, 0, 0, 0, 1]
COMB_MODS = (P, 1_000_000_007, 4_294_967_291)
BASE_HEAD = "5145fc8e0abca6325b8226294cdc2661e0891dcc"
UPSTREAM_MAIN_AT_REFRESH = "93fba1be3f3299b0ba4708d88715377bbb656e45"
PR1157_HEAD = "d7f0fd9370b3c13ff93293f08e03cadddb59b921"
PUBLIC_DAG_HEAD = "3edb8b31b6735a0a2302a578a21dc6e50bd64046"
ARCHITECTURE = "GRANDE_FINALE_V4_KB_MCA_TANGENT_SOURCE_ADAPTER_V1"
PARTITION = "4fade91abc408264989babcff6f8f9bbd80bcec52545a5db15ac376bf17d88fc"
SOURCE_BINDINGS_SHA256 = "85e68bb4cca383b134b30b302c5c04277c8608cf5e5af5edb4c34227beef2cba"
PACKET_BINDING_ROLES = {
    "experimental/notes/thresholds/kb_mca_v4_k3_actual_record_source_dimension_route_cut_v1.md": "MATHEMATICAL_STATEMENT_AND_SCOPE",
    "experimental/data/certificates/kb-mca-v4-k3-actual-record-source-dimension-route-cut-v1/README.md": "REPLAY_CONTRACT",
    "experimental/data/schemas/kb_mca_v4_k3_actual_record_source_dimension_route_cut_v1.schema.json": "STRICT_CERTIFICATE_SCHEMA",
    "experimental/scripts/verify_kb_mca_v4_k3_actual_record_source_dimension_route_cut_v1.py": "PRIMARY_VERIFIER",
    "experimental/scripts/verify_kb_mca_v4_k3_actual_record_source_dimension_route_cut_v1.sage": "INDEPENDENT_SAGE_REPLAY",
    "experimental/scripts/verify_kb_mca_v4_k3_actual_record_source_dimension_route_cut_v1_flint.py": "INDEPENDENT_FLINT_REPLAY",
    "experimental/scripts/verify_kb_mca_v4_k3_actual_record_source_dimension_route_cut_v1.wl": "INDEPENDENT_WOLFRAM_REPLAY",
}


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise CheckError(f"duplicate JSON key: {key}")
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


def strict_load(path: Path) -> Any:
    return strict_load_text(path.read_text())


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def payload_hash(manifest: dict[str, Any]) -> str:
    payload = copy.deepcopy(manifest)
    payload.pop("payload_sha256", None)
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_show(root: Path, commit: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(root), "show", f"{commit}:{path}"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(proc.returncode == 0, f"cannot read pinned source {commit}:{path}")
    return proc.stdout


def verify_line_ranges(binding: dict[str, Any], data: bytes) -> None:
    if "line_ranges" not in binding:
        return
    line_count = len(data.decode("utf-8").splitlines())
    for item in binding["line_ranges"]:
        match = re.fullmatch(r"([0-9]+)-([0-9]+)", item)
        require(match is not None, f"invalid line range {binding['binding_id']}")
        lo, hi = map(int, match.groups())
        require(1 <= lo <= hi <= line_count, f"out-of-range pin {binding['binding_id']}")


def ensure_no_floats(value: Any, path: str = "$") -> None:
    if isinstance(value, float):
        raise CheckError(f"float forbidden at {path}")
    if isinstance(value, dict):
        for key, child in value.items():
            ensure_no_floats(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            ensure_no_floats(child, f"{path}[{index}]")


def is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def schema_validate(
    value: Any,
    rule: dict[str, Any],
    root_schema: dict[str, Any],
    path: str = "$",
) -> None:
    """Validate the strict JSON-Schema subset used by this packet."""

    if "$ref" in rule:
        ref = rule["$ref"]
        require(ref.startswith("#/$defs/"), f"unsupported schema reference at {path}")
        name = ref.removeprefix("#/$defs/")
        require(name in root_schema["$defs"], f"missing schema definition {name}")
        schema_validate(value, root_schema["$defs"][name], root_schema, path)
        return

    if "const" in rule:
        require(type(value) is type(rule["const"]) and value == rule["const"], f"schema const at {path}")
    if "enum" in rule:
        require(value in rule["enum"], f"schema enum at {path}")

    allowed_types = rule.get("type")
    if isinstance(allowed_types, str):
        allowed_types = [allowed_types]
    if allowed_types is not None:
        matches = False
        for kind in allowed_types:
            if kind == "object":
                matches |= isinstance(value, dict)
            elif kind == "array":
                matches |= isinstance(value, list)
            elif kind == "string":
                matches |= isinstance(value, str)
            elif kind == "integer":
                matches |= is_int(value)
            elif kind == "boolean":
                matches |= isinstance(value, bool)
            elif kind == "null":
                matches |= value is None
            else:
                raise CheckError(f"unsupported schema type {kind} at {path}")
        require(matches, f"schema type at {path}")

    if isinstance(value, dict):
        required = set(rule.get("required", []))
        require(required <= set(value), f"schema required keys at {path}")
        properties = rule.get("properties", {})
        if rule.get("additionalProperties") is False:
            require(set(value) <= set(properties), f"schema additional key at {path}")
        for key, child in value.items():
            if key in properties:
                schema_validate(child, properties[key], root_schema, f"{path}.{key}")
    elif isinstance(value, list):
        if "minItems" in rule:
            require(len(value) >= rule["minItems"], f"schema minItems at {path}")
        if "maxItems" in rule:
            require(len(value) <= rule["maxItems"], f"schema maxItems at {path}")
        if rule.get("uniqueItems"):
            canonical = [canonical_bytes(item) for item in value]
            require(len(canonical) == len(set(canonical)), f"schema uniqueItems at {path}")
        if "items" in rule:
            for index, child in enumerate(value):
                schema_validate(child, rule["items"], root_schema, f"{path}[{index}]")
    elif isinstance(value, str):
        if "minLength" in rule:
            require(len(value) >= rule["minLength"], f"schema minLength at {path}")
        if "pattern" in rule:
            require(re.fullmatch(rule["pattern"], value) is not None, f"schema pattern at {path}")
    elif is_int(value):
        if "minimum" in rule:
            require(value >= rule["minimum"], f"schema minimum at {path}")


# Small polynomial arithmetic over F_p for an independent irreducibility test.
def poly_trim(a: list[int]) -> list[int]:
    a = [x % P for x in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def poly_sub(a: list[int], b: list[int]) -> list[int]:
    length = max(len(a), len(b))
    out = [0] * length
    for i in range(length):
        out[i] = ((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % P
    return poly_trim(out)


def poly_mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % P
    return poly_trim(out)


def poly_divmod(a: list[int], b: list[int]) -> tuple[list[int], list[int]]:
    a = poly_trim(a[:])
    b = poly_trim(b[:])
    require(b != [0], "polynomial division by zero")
    if len(a) < len(b):
        return [0], a
    q = [0] * (len(a) - len(b) + 1)
    inv = pow(b[-1], P - 2, P)
    while a != [0] and len(a) >= len(b):
        shift = len(a) - len(b)
        coeff = a[-1] * inv % P
        q[shift] = coeff
        for i, value in enumerate(b):
            a[i + shift] = (a[i + shift] - coeff * value) % P
        a = poly_trim(a)
    return poly_trim(q), a


def poly_mod(a: list[int], modulus: list[int] = MODULUS) -> list[int]:
    return poly_divmod(a, modulus)[1]


def poly_gcd(a: list[int], b: list[int]) -> list[int]:
    a, b = poly_trim(a), poly_trim(b)
    while b != [0]:
        _, r = poly_divmod(a, b)
        a, b = b, r
    inv = pow(a[-1], P - 2, P)
    return [(x * inv) % P for x in a]


def poly_pow_x(exponent: int) -> list[int]:
    result = [1]
    base = [0, 1]
    while exponent:
        if exponent & 1:
            result = poly_mod(poly_mul(result, base))
        base = poly_mod(poly_mul(base, base))
        exponent >>= 1
    return poly_trim(result)


def verify_irreducible() -> None:
    x = [0, 1]
    require(poly_pow_x(P**6) == x, "extension modulus fails x^(p^6)=x")
    for exponent in (P**2, P**3):
        g = poly_gcd(MODULUS, poly_sub(poly_pow_x(exponent), x))
        require(g == [1], f"extension modulus has a proper factor at {exponent}")


def exact_comb_fingerprint() -> dict[str, Any]:
    value = math.comb(N - E, M)
    raw = value.to_bytes((value.bit_length() + 7) // 8, "big")
    return {
        "formula": f"binomial({N-E},{M})",
        "bit_length": value.bit_length(),
        "big_endian_byte_length": len(raw),
        "big_endian_sha256": hashlib.sha256(raw).hexdigest(),
        "residues": {
            f"mod_{modulus}": value % modulus for modulus in COMB_MODS
        },
    }


def verify_local_binding(binding: dict[str, Any]) -> None:
    path = ROOT / binding["path"]
    require(path.is_file(), f"missing bound local source {binding['path']}")
    data = path.read_bytes()
    committed = git_show(ROOT, binding["commit"], binding["path"])
    require(data == committed, f"working source differs from pin {binding['binding_id']}")
    verify_line_ranges(binding, committed)
    if binding["hash_kind"] == "GIT_BLOB_SHA1":
        require(git_blob_sha1(committed) == binding["hash"], f"blob mismatch {binding['binding_id']}")
        require(sha256(committed) == binding["sha256"], f"sha256 mismatch {binding['binding_id']}")
    elif binding["hash_kind"] == "SHA256":
        require(sha256(committed) == binding["hash"], f"sha256 mismatch {binding['binding_id']}")
    else:
        raise CheckError(f"unexpected local hash kind {binding['hash_kind']}")


def verify_dag_binding(binding: dict[str, Any], dag_root: Path) -> None:
    data = git_show(dag_root, binding["commit"], binding["path"])
    verify_line_ranges(binding, data)
    require(git_blob_sha1(data) == binding["hash"], f"DAG blob mismatch {binding['binding_id']}")
    require(sha256(data) == binding["sha256"], f"DAG sha256 mismatch {binding['binding_id']}")


def verify_packet_bindings(bindings: list[dict[str, Any]]) -> None:
    require(len(bindings) == len(PACKET_BINDING_ROLES), "packet binding count")
    by_path = {item["path"]: item for item in bindings}
    require(len(by_path) == len(bindings), "duplicate packet binding path")
    require(set(by_path) == set(PACKET_BINDING_ROLES), "packet binding path set")
    for path, role in PACKET_BINDING_ROLES.items():
        item = by_path[path]
        require(item["role"] == role, f"packet binding role {path}")
        file_path = ROOT / path
        require(file_path.is_file(), f"missing packet file {path}")
        require(sha256(file_path.read_bytes()) == item["sha256"], f"packet hash {path}")


def validate(
    manifest: dict[str, Any],
    *,
    schema: dict[str, Any] | None = None,
    check_payload: bool = True,
    check_sources: bool = True,
    dag_root: Path | None = None,
    comb_fingerprint: dict[str, Any] | None = None,
) -> None:
    ensure_no_floats(manifest)
    if schema is not None:
        schema_validate(manifest, schema, schema)
    expected_top = {
        "schema", "artifact_kind", "base_repository", "source_bindings",
        "deployed_row", "actual_record_witness", "dimension_noninvariance",
        "public_dag_audit", "missing_theorem", "ledger", "conclusion",
        "packet_bindings",
        "payload_sha256",
    }
    require(set(manifest) == expected_top, "top-level key set")
    require(manifest["schema"] == "rs-mca-kb-v4-k3-actual-record-source-dimension-route-cut-v1", "schema id")
    require(manifest["artifact_kind"] == "ACTUAL_RECORD_K_SHIFT_DIMENSION_SENSITIVITY_AUDIT", "artifact kind")
    if check_payload:
        require(payload_hash(manifest) == manifest["payload_sha256"], "payload seal")

    base = manifest["base_repository"]
    require(base == {
        "repository": "przchojecki/rs-mca",
        "base_head": BASE_HEAD,
        "base_is_exact_pr1158_head": True,
        "upstream_main_at_refresh": UPSTREAM_MAIN_AT_REFRESH,
        "pr1157_head": PR1157_HEAD,
        "pr1158_head": BASE_HEAD,
        "public_dag_repository": "AllenGrahamHart/rs-mca-prize-dag",
        "public_dag_head_at_refresh": PUBLIC_DAG_HEAD,
        "reconciled_prs": {
            "1130": "a14a05d9ba80068133e93e2fa77d6d1dc8828829",
            "1132": "543db66f570e066c0c14976b72b27bb873307111",
            "1139": "8d43c6fa3a6ff04ea369ba7046fced6ae133b097",
            "1143": "1646bbba7f3c5d52e1f4ed109c651053ef2e3d8c",
            "1152": "ed4877cce5f227f33311fa93f5ff5e5f4150ae63",
            "1155": "1cf13bb4058da19c5108bf79472394a598217bca",
            "1156": "7c0e45eb4d5352b4e55bf70a48023fb60c7ce7fd",
            "1157": PR1157_HEAD,
            "1158": BASE_HEAD,
        },
    }, "base repository snapshot")

    bindings = manifest["source_bindings"]
    require(len(bindings) == 11, "source binding count")
    ids = [item["binding_id"] for item in bindings]
    require(len(ids) == len(set(ids)), "duplicate source binding")
    require(sha256(canonical_bytes(bindings)) == SOURCE_BINDINGS_SHA256, "source binding inventory")
    if check_sources:
        require(dag_root is not None, "--dag-root is required for fail-closed source replay")
        require(dag_root.is_dir(), "DAG root is not a directory")
        for binding in bindings:
            if binding["repository"] == "przchojecki/rs-mca":
                verify_local_binding(binding)
            elif binding["repository"] == "AllenGrahamHart/rs-mca-prize-dag":
                verify_dag_binding(binding, dag_root)
            else:
                raise CheckError(f"unrecognized source repository {binding['repository']}")

        ancestor = subprocess.run(
            ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", BASE_HEAD, "HEAD"],
            check=False,
        )
        require(ancestor.returncode == 0, "packet HEAD is not based on exact PR #1158 head")

        conjectures = (ROOT / "experimental/Conjectures_and_Barriers_RS_MCA_v4_1.tex").read_text()
        finale = (ROOT / "experimental/grande_finale.tex").read_text()
        foundation = (ROOT / "tex/cs25_cap_v13_2.tex").read_text()
        require("\\deg h<k" in conjectures, "actual degree-k witness source token")
        require("K=2^{20}+1$ on the MCA route" in finale, "effective K source token")
        require("K$ is the code dimension of the census ($K=k$ for the deployed rows)" in foundation, "code K source token")
        require("boundary delegated to \\textup{(Q)}" in foundation, "boundary-Q source token")

    verify_packet_bindings(manifest["packet_bindings"])

    row = manifest["deployed_row"]
    expected_ints = {
        "base_prime": P,
        "extension_degree": 6,
        "n": N,
        "code_dimension_k": K_CODE,
        "agreement_m": M,
        "locator_degree_omega": OMEGA,
        "actual_lattice_K": K_CODE,
        "actual_lattice_w": W_CODE,
        "prefix_effective_K": K_EFF,
        "prefix_effective_w": W_EFF,
        "B_star": B_STAR,
        "U_paid": U_PAID,
        "joint_unpaid_reserve": RESERVE,
    }
    for key, expected in expected_ints.items():
        require(is_int(row[key]) and row[key] == expected, f"row integer {key}")
    require(row["row"] == "KoalaBear MCA at 2^-128", "row name")
    require(row["object"] == "MCA", "row object")
    require(row["field_cardinality"] == str(Q), "field cardinality")
    require(row["architecture_id"] == ARCHITECTURE, "row architecture")
    require(row["partition_sha256"] == PARTITION, "row partition")
    require(row["unit"] == "DISTINCT_BAD_FINITE_SLOPES_PER_RECEIVED_LINE", "row unit")

    if check_sources:
        row_manifest = strict_load(
            ROOT / "experimental/data/certificates/kb-mca-v4-tangent-source-adapter-v1/row_manifest.json"
        )
        row_payload = copy.deepcopy(row_manifest)
        row_seal = row_payload.pop("payload_sha256")
        require(sha256(canonical_bytes(row_payload)) == row_seal, "bound row-manifest seal")
        partition = row_manifest["partition"]
        contract = row_manifest["row_contract"]
        require(row_manifest["architecture_id"] == ARCHITECTURE, "bound architecture")
        require(partition["architecture_id"] == ARCHITECTURE, "bound partition architecture")
        require(partition["partition_sha256"] == PARTITION, "bound partition digest")
        require(partition["atom_order"] == ["U_paid", "U_Q", "U_BC", "U_new"], "bound atom order")
        require(partition["owner_order"] == [
            "SOURCE_COORDINATE_TANGENT_IMAGE",
            "ACTIVE_V4_BOUNDARY_PREFIX_Q",
            "ACTIVE_V4_BALANCED_CORE",
            "UNPAID_V4_COMPLEMENT",
        ], "bound owner order")
        require(partition["unit"] == row["unit"], "bound row unit")
        require(partition["same_partition_for_all_atoms"] is True, "bound partition scope")
        require(contract["row"] == row["row"] and contract["object"] == row["object"], "bound row identity")
        require(contract["B_star"] == B_STAR and contract["agreement"] == M, "bound row target")
        require(contract["code"]["dimension"] == K_CODE, "bound code dimension")
        require(contract["domain"]["cardinality"] == N, "bound domain size")
        require(contract["field"]["base_prime"] == P, "bound base field")
        require(contract["field"]["extension_degree"] == 6, "bound extension degree")

    record = manifest["actual_record_witness"]
    require(record["record_id"] == "KB_SPARSE_BOUNDARY_ACTUAL_RECORD_V1", "record id")
    carrier = record["carrier"]
    require(carrier["description"] == "D=<zeta> inside F_p^x", "carrier description")
    require(carrier["primitive_generator"] == 3, "primitive generator")
    require(pow(3, (P - 1) // 2, P) != 1, "generator missing 2-primary order")
    require(pow(3, (P - 1) // 127, P) != 1, "generator missing 127-primary order")
    require(carrier["carrier_index"] == (P - 1) // N == 1016, "carrier index")
    require(carrier["zeta"] == ZETA == pow(3, (P - 1) // N, P), "carrier generator")
    require(carrier["order"] == N, "declared carrier order")
    require(carrier["exact_order_checks"] == ["zeta^n=1", "zeta^(n/2)=-1"], "carrier check inventory")
    require(pow(ZETA, N, P) == 1, "zeta^n")
    require(pow(ZETA, N // 2, P) == P - 1, "exact carrier order")
    field = record["challenge_field"]
    require(field["model"] == "F_p[alpha]/(alpha^6+alpha+6)", "challenge field model")
    require(field["modulus_coefficients_low_to_high"] == MODULUS, "extension modulus")
    require(field["modulus_irreducible"] is True, "irreducibility claim")
    require(field["alpha_degree_over_F_p"] == 6 and field["alpha_not_in_base_field"] is True, "alpha degree")

    require(record["error_size_e"] == E, "error size")
    require(record["error_set"] == "E={zeta^i:0<=i<67473}", "error-set definition")
    require(record["witness_support"] == "S={zeta^i:67473<=i<1183521}", "support definition")
    require(record["witness_support_size"] == M, "witness support size")
    require(E + M == 1_183_521 < N, "support interval")
    line = record["received_line"]
    require(line["r0"] == "indicator_E + alpha/(x-alpha)", "received r0")
    require(line["r1"] == "-1/(x-alpha)", "received r1")
    require(line["affine_slope"] == "alpha", "actual slope")
    require(line["received_word_at_slope"] == "indicator_E", "slope cancellation")
    require(line["explaining_polynomial"] == "0" and line["explaining_polynomial_degree_lt_k"] is True, "explainer")
    for key in (
        "actual_MCA_witness", "pair_not_simultaneously_explained_on_S",
        "column_far", "tangent_image_empty", "direction_unexplained_for_degree_lt_k",
        "direction_unexplained_for_degree_lt_k_plus_one", "full_extension_degree_slope",
    ):
        require(record[key] is True, f"actual record flag {key}")
    require(M > K_CODE + 1, "pole nonexplanation root bound")
    require(
        record["direction_nonexplanation_reason"]
        == "If -1/(x-alpha)=g(x) on m points then (x-alpha)g(x)+1 has m roots but degree at most k (actual) or k+1 (effective), both below m",
        "direction nonexplanation statement",
    )

    require(record["lattice_vector"] == "(Lambda_E,0)", "lattice vector")
    require(record["minimal_shifted_degree_actual_K"] == E, "actual d1")
    require(record["minimal_shifted_degree_effective_K"] == E, "effective d1")
    bound = record["minimality_root_bound"]
    require(bound["off_E_root_count"] == N - E, "off-E roots")
    require(bound["actual_K_max_degree_N_below_e"] == K_CODE + E - 2, "actual N degree")
    require(bound["effective_K_max_degree_N_below_e"] == K_CODE + E - 1, "effective N degree")
    require(bound["max_degree_W_below_e"] == E - 1, "W degree")
    require(
        bound["proof"]
        == "Any lower shifted-degree (W,N) has N=0 from off-E roots, then W=0 from the e nonzero error positions",
        "minimality proof statement",
    )
    require(N - E > K_CODE + E - 1, "root bound beats both N degrees")

    actual = record["actual_code_dimension_classification"]
    effective = record["effective_prefix_classification"]
    require(actual == {
        "w": W_CODE,
        "boundary_profile_value": W_CODE + 1,
        "d1_eq_boundary_profile": True,
        "frozen_Q_membership_proved": False,
        "frozen_BC_membership_proved": False,
    }, "actual profile classification")
    require(effective == {
        "w": W_EFF,
        "boundary_profile_value": W_EFF + 1,
        "first_interior_profile_value": W_EFF + 2,
        "d1_eq_first_interior_profile": True,
        "frozen_Q_membership_proved": False,
        "frozen_BC_membership_proved": False,
    }, "effective profile classification")

    profiles = record["row_degree_profiles"]
    code_profile = profiles["code_dimension"]
    eff_profile = profiles["effective_dimension"]
    require(code_profile == {
        "d1": E, "d2": OMEGA, "d1_plus_d2": N - K_CODE + 1,
        "m_prime": M, "degree_cap_B": 0, "profile": "BOUNDARY_NUMERICAL_PROFILE",
    }, "code row-degree profile")
    require(eff_profile == {
        "d1": E, "d2": OMEGA - 1, "d1_plus_d2": N - K_EFF + 1,
        "m_prime": M + 1, "degree_cap_B": 1, "profile": "FIRST_INTERIOR_NUMERICAL_PROFILE",
    }, "effective row-degree profile")
    require(profiles["difference"] == "K_PLUS_ONE_CREATES_EXACTLY_ONE_ADDITIONAL_B_COEFFICIENT", "profile difference")

    ray = record["pure_ray_scope"]
    require(ray == {
        "weak_popov_g1": "(Lambda_E,0)",
        "weak_popov_g2": "(L_{D_minus_E} mod Lambda_E,L_{D_minus_E})",
        "determinant": "Lambda_D",
        "zero_codeword_supports_have_B": 0,
        "primitive_r_out_4_membership_proved": False,
        "endpoint_route_membership_proved": False,
        "role": "PRE_REC_2_4_DIMENSION_SENSITIVITY_CONTROL_ONLY",
    }, "pure-ray scope")

    if comb_fingerprint is None:
        comb_fingerprint = exact_comb_fingerprint()
    require(record["zero_codeword_exact_m_supports"] == comb_fingerprint, "exact support fingerprint")

    noninv = manifest["dimension_noninvariance"]
    require(noninv["same_actual_record"] is True, "same actual record")
    require(noninv["code_dimension_profile"] == {
        "K": K_CODE,
        "w": W_CODE,
        "d1": E,
        "classification": "BOUNDARY_PROFILE",
        "frozen_owner_membership_entailed": False,
    }, "code-dimension profile")
    require(noninv["effective_dimension_profile"] == {
        "K": K_EFF,
        "w": W_EFF,
        "d1": E,
        "classification": "FIRST_INTERIOR_PROFILE",
        "frozen_owner_membership_entailed": False,
    }, "effective-dimension profile")
    require(noninv["d1_invariant"] is True, "d1 invariance")
    for key in ("w_drop", "d2_drop", "m_prime_increase", "degree_cap_B_increase"):
        require(is_int(noninv[key]) and noninv[key] == 1, f"dimension delta {key}")
    for key in (
        "literal_profile_classification_invariant_under_K_plus_one",
        "K_plus_one_semantics_preserving_adapter_proved",
        "explicit_priority_map_supplied_by_bound_sources",
        "frozen_Q_membership_proved_for_record",
        "frozen_BC_membership_proved_for_record",
        "frozen_U_new_membership_proved_for_record",
    ):
        require(noninv[key] is False, f"forbidden semantic promotion {key}")
    require(noninv["actual_owner_status"] == "NOT_ESTABLISHED_BY_PINNED_SOURCES", "actual owner status")

    audit = manifest["public_dag_audit"]
    require(audit == {
        "node_id": "rate_half_kb_active_balanced_core_witness_compiler",
        "declared_status": "PROVED",
        "selector_lemma_after_relation_is_supplied": True,
        "source_bound_equivalence_to_frozen_BC_proved": False,
        "typed_actual_certificate_validator_present": False,
        "actual_received_pair_equations_checked": False,
        "actual_MCA_noncontainment_checked": False,
        "degree_lt_k_explanation_checked": False,
        "Q_exclusion_executable": False,
        "Q_exclusion_scope": "STRING_TAG_ON_CERTIFICATE_NOT_SLOPE_GLOBAL_EXISTENTIAL_EXCLUSION",
        "code_dimension_to_effective_dimension_adapter_proved": False,
        "support_ge_m_to_exact_m_normalization_proved": False,
        "verifier_scope": "INTEGER_STRING_AND_PROOF_TOKEN_STRUCTURE_ONLY",
        "downstream_order32_adapter_inherits_gap": True,
        "downstream_component_bridge_remains_conditional": True,
    }, "public DAG audit")

    missing = manifest["missing_theorem"]
    require(missing["theorem_id"] == "SEM_QBC_BEFORE_REC_2_4", "missing theorem id")
    required_clauses = {
        "ACTUAL_WITNESS_SOUNDNESS", "FROZEN_Q_PROJECTION_EQUIVALENCE",
        "FROZEN_BC_PROJECTION_EQUIVALENCE", "SLOPE_GLOBAL_Q_EXCLUSION_ACROSS_ALL_WITNESSES",
        "CODE_DIMENSION_OR_K_PLUS_ONE_ADAPTER", "SUPPORT_AT_LEAST_M_NORMALIZATION",
        "ALL_Z_BC_COMPLEMENT_FENCE",
    }
    require(set(missing["required_clauses"]) == required_clauses, "SEM-QBC clauses")
    require(missing["Rec_2_4_may_begin_after_this"] is True, "Rec ordering")
    require(missing["endpoint_realization_current_status"] == "UNPROVED", "endpoint status")
    require(missing["thirteen_route_replay_current_status"] == "RAW_ONLY", "route replay status")
    require(
        missing["weakest_required_statement"]
        == "Give explicit algebraic P_Q(r,w) and P_BC(r,w) on actual MCA witnesses; prove their slope projections equal the frozen Q and BC sets in both directions after slope-global first match; prove which K and shift govern P_BC; preserve original support and degree-<k explanation; and prove an all-witness complement fence.",
        "missing theorem statement",
    )

    ledger = manifest["ledger"]
    require(ledger["U_paid"] == U_PAID, "ledger U_paid")
    for key in ("U_Q", "U_BC", "U_new", "U_remaining", "U_positive", "U_sourcecover", "U_K3", "U_K3_allocation", "signed_slack"):
        require(ledger[key] is None, f"ledger {key} must be null")
    require(ledger["ledger_movement"] == 0, "ledger movement")

    conclusion = manifest["conclusion"]
    require(conclusion["outcome"] == "OPEN_MISSING_ADAPTER_GAP", "audit outcome")
    require(conclusion["actual_record_constructed"] is True, "actual record conclusion")
    require(conclusion["K_shift_profile_noninvariance_proved"] is True, "K-shift conclusion")
    require(conclusion["SEM_QBC_required"] is True, "SEM-QBC conclusion")
    for key in (
        "public_DAG_source_bound_K_adapter_proved",
        "actual_owner_collision_proved",
        "frozen_owner_membership_proved",
    ):
        require(conclusion[key] is False, f"forbidden conclusion promotion {key}")
    for key in ("ActiveRec_2_4_defined", "Rec_2_4_compiler_proved", "K3_closed", "KoalaBear_row_closed", "universal_smooth_domain_result"):
        require(conclusion[key] is False, f"forbidden promotion {key}")
    require(conclusion["ledger_movement"] == 0, "conclusion movement")
    require(conclusion == {
        "outcome": "OPEN_MISSING_ADAPTER_GAP",
        "actual_record_constructed": True,
        "K_shift_profile_noninvariance_proved": True,
        "public_DAG_source_bound_K_adapter_proved": False,
        "actual_owner_collision_proved": False,
        "frozen_owner_membership_proved": False,
        "SEM_QBC_required": True,
        "first_false_or_unproved_bridge": "CODE_DIMENSION_TO_EFFECTIVE_DIMENSION_AND_PRIORITY_MAP_BEFORE_REC_2_4",
        "ActiveRec_2_4_defined": False,
        "Rec_2_4_compiler_proved": False,
        "K3_closed": False,
        "KoalaBear_row_closed": False,
        "universal_smooth_domain_result": False,
        "ledger_movement": 0,
        "proof_tier": "RIGOROUS_DIMENSION_SENSITIVITY_AND_MISSING_ADAPTER_AUDIT",
    }, "conclusion scope")


def reseal(manifest: dict[str, Any]) -> None:
    manifest["payload_sha256"] = payload_hash(manifest)


def mutation_cases() -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    return [
        ("wrong-p", lambda m: m["deployed_row"].__setitem__("base_prime", P + 1)),
        ("wrong-n", lambda m: m["deployed_row"].__setitem__("n", N // 2)),
        ("wrong-k", lambda m: m["deployed_row"].__setitem__("code_dimension_k", K_CODE + 1)),
        ("wrong-m", lambda m: m["deployed_row"].__setitem__("agreement_m", M - 1)),
        ("wrong-omega", lambda m: m["deployed_row"].__setitem__("locator_degree_omega", OMEGA + 1)),
        ("collapse-K", lambda m: m["deployed_row"].__setitem__("actual_lattice_K", K_EFF)),
        ("wrong-w-code", lambda m: m["deployed_row"].__setitem__("actual_lattice_w", W_CODE - 1)),
        ("wrong-B", lambda m: m["deployed_row"].__setitem__("B_star", B_STAR + 1)),
        ("wrong-reserve", lambda m: m["deployed_row"].__setitem__("joint_unpaid_reserve", RESERVE + 1)),
        ("wrong-architecture", lambda m: m["deployed_row"].__setitem__("architecture_id", "OTHER")),
        ("wrong-partition", lambda m: m["deployed_row"].__setitem__("partition_sha256", "0" * 64)),
        ("wrong-upstream-main", lambda m: m["base_repository"].__setitem__("upstream_main_at_refresh", BASE_HEAD)),
        ("wrong-pr1157-head", lambda m: m["base_repository"].__setitem__("pr1157_head", BASE_HEAD)),
        ("source-binding-commit", lambda m: m["source_bindings"][0].__setitem__("commit", PR1157_HEAD)),
        ("source-binding-range", lambda m: m["source_bindings"][0]["line_ranges"].__setitem__(0, "1-1")),
        ("source-binding-repository", lambda m: m["source_bindings"][0].__setitem__("repository", "other/repo")),
        ("source-binding-hash", lambda m: m["source_bindings"][0].__setitem__("hash", "0" * 40)),
        ("wrong-zeta", lambda m: m["actual_record_witness"]["carrier"].__setitem__("zeta", ZETA + 1)),
        ("wrong-primitive-generator", lambda m: m["actual_record_witness"]["carrier"].__setitem__("primitive_generator", 4)),
        ("wrong-carrier-order", lambda m: m["actual_record_witness"]["carrier"].__setitem__("order", N // 2)),
        ("reducible-modulus", lambda m: m["actual_record_witness"]["challenge_field"].__setitem__("modulus_irreducible", False)),
        ("wrong-error-size", lambda m: m["actual_record_witness"].__setitem__("error_size_e", E - 1)),
        ("wrong-support-definition", lambda m: m["actual_record_witness"].__setitem__("witness_support", "S=D")),
        ("wrong-support-size", lambda m: m["actual_record_witness"].__setitem__("witness_support_size", M - 1)),
        ("base-slope", lambda m: m["actual_record_witness"]["received_line"].__setitem__("affine_slope", 0)),
        ("wrong-direction", lambda m: m["actual_record_witness"]["received_line"].__setitem__("r1", "x^k")),
        ("not-actual", lambda m: m["actual_record_witness"].__setitem__("actual_MCA_witness", False)),
        ("common-pair", lambda m: m["actual_record_witness"].__setitem__("pair_not_simultaneously_explained_on_S", False)),
        ("not-column-far", lambda m: m["actual_record_witness"].__setitem__("column_far", False)),
        ("tangent-nonempty", lambda m: m["actual_record_witness"].__setitem__("tangent_image_empty", False)),
        ("wrong-d1-code", lambda m: m["actual_record_witness"].__setitem__("minimal_shifted_degree_actual_K", E - 1)),
        ("wrong-d1-eff", lambda m: m["actual_record_witness"].__setitem__("minimal_shifted_degree_effective_K", E + 1)),
        ("wrong-root-count", lambda m: m["actual_record_witness"]["minimality_root_bound"].__setitem__("off_E_root_count", N - E - 1)),
        ("wrong-N-degree", lambda m: m["actual_record_witness"]["minimality_root_bound"].__setitem__("effective_K_max_degree_N_below_e", K_CODE + E)),
        ("false-minimality-proof", lambda m: m["actual_record_witness"]["minimality_root_bound"].__setitem__("proof", "false")),
        ("claim-code-Q", lambda m: m["actual_record_witness"]["actual_code_dimension_classification"].__setitem__("frozen_Q_membership_proved", True)),
        ("claim-effective-BC", lambda m: m["actual_record_witness"]["effective_prefix_classification"].__setitem__("frozen_BC_membership_proved", True)),
        ("wrong-code-d2", lambda m: m["actual_record_witness"]["row_degree_profiles"]["code_dimension"].__setitem__("d2", OMEGA - 1)),
        ("wrong-eff-B-cap", lambda m: m["actual_record_witness"]["row_degree_profiles"]["effective_dimension"].__setitem__("degree_cap_B", 0)),
        ("owner-profile-label", lambda m: m["actual_record_witness"]["row_degree_profiles"]["code_dimension"].__setitem__("profile", "Q_BOUNDARY")),
        ("promote-primitive-route", lambda m: m["actual_record_witness"]["pure_ray_scope"].__setitem__("primitive_r_out_4_membership_proved", True)),
        ("change-ray-B", lambda m: m["actual_record_witness"]["pure_ray_scope"].__setitem__("zero_codeword_supports_have_B", 1)),
        ("wrong-comb-hash", lambda m: m["actual_record_witness"]["zero_codeword_exact_m_supports"].__setitem__("big_endian_sha256", "0" * 64)),
        ("claim-profile-invariance", lambda m: m["dimension_noninvariance"].__setitem__("literal_profile_classification_invariant_under_K_plus_one", True)),
        ("claim-K-adapter-exists", lambda m: m["dimension_noninvariance"].__setitem__("K_plus_one_semantics_preserving_adapter_proved", True)),
        ("claim-Q-owner", lambda m: m["dimension_noninvariance"].__setitem__("frozen_Q_membership_proved_for_record", True)),
        ("claim-BC-owner", lambda m: m["dimension_noninvariance"].__setitem__("frozen_BC_membership_proved_for_record", True)),
        ("claim-new-owner", lambda m: m["dimension_noninvariance"].__setitem__("frozen_U_new_membership_proved_for_record", True)),
        ("wrong-profile-class", lambda m: m["dimension_noninvariance"]["effective_dimension_profile"].__setitem__("classification", "BOUNDARY_PROFILE")),
        ("claim-source-equivalence", lambda m: m["public_dag_audit"].__setitem__("source_bound_equivalence_to_frozen_BC_proved", True)),
        ("wrong-DAG-node", lambda m: m["public_dag_audit"].__setitem__("node_id", "other")),
        ("claim-Q-executable", lambda m: m["public_dag_audit"].__setitem__("Q_exclusion_executable", True)),
        ("claim-K-adapter", lambda m: m["public_dag_audit"].__setitem__("code_dimension_to_effective_dimension_adapter_proved", True)),
        ("drop-SEM-clause", lambda m: m["missing_theorem"]["required_clauses"].pop()),
        ("bank-K3-zero", lambda m: m["ledger"].__setitem__("U_K3", 0)),
        ("move-ledger", lambda m: m["ledger"].__setitem__("ledger_movement", 1)),
        ("claim-success-B", lambda m: m["conclusion"].__setitem__("outcome", "B")),
        ("close-K3", lambda m: m["conclusion"].__setitem__("K3_closed", True)),
        ("close-row", lambda m: m["conclusion"].__setitem__("KoalaBear_row_closed", True)),
        ("packet-hash-drift", lambda m: m["packet_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("packet-role-drift", lambda m: m["packet_bindings"][0].__setitem__("role", "OTHER")),
        ("unknown-nested-key", lambda m: m["actual_record_witness"].__setitem__("invented_owner", "Q")),
    ]


def run_tamper_selftest(
    manifest: dict[str, Any],
    schema: dict[str, Any],
    comb_fingerprint: dict[str, Any],
) -> int:
    accepted: list[str] = []
    for name, mutate in mutation_cases():
        candidate = copy.deepcopy(manifest)
        mutate(candidate)
        reseal(candidate)
        try:
            validate(
                candidate,
                schema=schema,
                check_payload=True,
                check_sources=False,
                comb_fingerprint=comb_fingerprint,
            )
        except CheckError:
            continue
        accepted.append(name)
    require(not accepted, f"semantic mutations accepted: {accepted}")

    parser_mutations = [
        '{"x":1,"x":2}',
        '{"x":1.5}',
        '{"x":NaN}',
    ]
    parser_accepted = []
    for raw in parser_mutations:
        try:
            strict_load_text(raw)
        except CheckError:
            continue
        parser_accepted.append(raw)
    require(not parser_accepted, "parser mutations accepted")
    return len(mutation_cases())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--dag-root", type=Path)
    args = parser.parse_args()
    require(args.check or args.tamper_selftest, "request --check and/or --tamper-selftest")

    manifest = strict_load(MANIFEST_PATH)
    schema = strict_load(SCHEMA_PATH)
    require(schema["$id"] == manifest["schema"], "schema sidecar id")
    verify_irreducible()
    comb_fingerprint = exact_comb_fingerprint()

    if args.check:
        validate(
            manifest,
            schema=schema,
            check_payload=True,
            check_sources=True,
            dag_root=args.dag_root,
            comb_fingerprint=comb_fingerprint,
        )
        external = 6 if args.dag_root is not None else 0
        print(
            "PASS K3 ACTUAL-RECORD DIMENSION-SENSITIVITY AUDIT "
            f"d1={E} code_profile=boundary effective_profile=first-interior actual_owner=not-established actual_record=1 "
            f"local_sources=5 external_sources={external} ledger_movement=0"
        )

    if args.tamper_selftest:
        count = run_tamper_selftest(manifest, schema, comb_fingerprint)
        print(f"PASS tamper-selftest: {count} semantic and 3 parser mutations rejected")


if __name__ == "__main__":
    try:
        main()
    except CheckError as exc:
        raise SystemExit(f"FAIL: {exc}")
