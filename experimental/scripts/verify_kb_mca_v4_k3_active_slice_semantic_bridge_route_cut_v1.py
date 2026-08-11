#!/usr/bin/env python3
"""Verify the KoalaBear K3 active-slice semantic bridge route cut.

The proved negative statement is narrow: the printed degree-two source-pencil
and rational-deck identities do not imply that the displayed endpoint
coordinate preserves the deployed evaluation carrier.  The active
``Z_BC^(m_in=2,r_out=4)`` domain is not executable in the pinned source, so
this checker deliberately does not manufacture an actual MCA counterexample
or a K3 payment.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable


sys.set_int_max_str_digits(2_500_000)

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-kb-v4-k3-active-slice-semantic-bridge-route-cut-v1"
STATUS = "PROVED_DEFINITION_LEVEL_ROUTE_CUT_OPEN_GAP"
ARTIFACT_KIND = (
    "SOURCE_BOUND_DEFINITION_ROUTE_CUT_AND_DIRECT_COORDINATE_COUNTERMODEL"
)
THEOREM_KIND = "DIRECT_ENDPOINT_COORDINATE_CARRIER_INFERENCE_COUNTERMODEL"

P = 2_130_706_433
EXTENSION_DEGREE = 6
FIELD_SIZE = P**EXTENSION_DEGREE
N = 2_097_152
K = 1_048_576
AGREEMENT = 1_116_048
B_STAR = 274_980_728_111_395_087
U_PAID = 981_104
RESERVE = B_STAR - U_PAID
PRIMITIVE_GENERATOR = 3
SUBGROUP_GENERATOR = 1_213_133_211

ARCHITECTURE = "GRANDE_FINALE_V4_KB_MCA_TANGENT_SOURCE_ADAPTER_V1"
PARTITION = "4fade91abc408264989babcff6f8f9bbd80bcec52545a5db15ac376bf17d88fc"
HISTORICAL_ARCHITECTURE = (
    "GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_"
    "FROBENIUS_9208_FIRST_GAP_PENCIL_IMAGE_ADAPTER_V1"
)
HISTORICAL_PARTITION = (
    "7a57fa877417920862ed2fe2e5c569852555f78b73b046d320d5e7a65d98ebaa"
)
UNIT = "DISTINCT_BAD_FINITE_SLOPES_PER_RECEIVED_LINE"
QUANTIFIER = "UNIFORM_OVER_ALL_ADMISSIBLE_RECEIVED_LINES"

BASE_HEAD = "d7f0fd9370b3c13ff93293f08e03cadddb59b921"
PARENT_HEAD = "ed4877cce5f227f33311fa93f5ff5e5f4150ae63"
PIN_REPAIR_HEAD = "8d43c6fa3a6ff04ea369ba7046fced6ae133b097"
PUBLIC_DAG_COMMIT = "48a7de3c2d0d092b1899b1bb18d62bb4bf8861ce"
HISTORICAL_OWNER_COMMIT = "702cd8e16673f2971ac1e7898603de2d7d087dfa"
HISTORICAL_EQUALITY_COMMIT = "065f347a96c91ade7d80df8bf324f646329c623e"

MANIFEST_REL = Path(
    "experimental/data/certificates/"
    "kb-mca-v4-k3-active-slice-semantic-bridge-route-cut-v1/manifest.json"
)
PRIMARY_REL = Path(
    "experimental/scripts/"
    "verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1.py"
)

# Exact first 36 unordered carrier two-cycles for tau(x)=1-x, sorted by the
# smaller/first coordinate.  The first 30 are active and the last six source.
SELECTED_PAIRS = [
    [106253, 2130600181],
    [1369722, 2129336712],
    [3779040, 2126927394],
    [8509390, 2122197044],
    [10074554, 2120631880],
    [10557358, 2120149076],
    [12609353, 2118097081],
    [14292086, 2116414348],
    [14535750, 2116170684],
    [15465656, 2115240778],
    [15916705, 2114789729],
    [16063573, 2114642861],
    [17060445, 2113645989],
    [18308266, 2112398168],
    [18560217, 2112146217],
    [19146956, 2111559478],
    [23803083, 2106903351],
    [24600315, 2106106119],
    [24695656, 2106010778],
    [25420300, 2105286134],
    [26886517, 2103819917],
    [32424981, 2098281453],
    [33558404, 2097148030],
    [33587235, 2097119199],
    [33762591, 2096943843],
    [33877430, 2096829004],
    [34423271, 2096283163],
    [35880750, 2094825684],
    [37630638, 2093075796],
    [37955085, 2092751349],
    [38255910, 2092450524],
    [38823503, 2091882931],
    [41058570, 2089647864],
    [41999211, 2088707223],
    [42650444, 2088055990],
    [42971510, 2087734924],
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_noninteger(token: str) -> Any:
    raise AssertionError(f"noninteger/nonstandard JSON number: {token}")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(),
        object_pairs_hook=strict_object,
        parse_float=reject_noninteger,
        parse_constant=reject_noninteger,
    )
    require(isinstance(value, dict), f"JSON root is not an object: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest_object(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def payload_digest(value: dict[str, Any]) -> str:
    payload = copy.deepcopy(value)
    payload.pop("payload_sha256", None)
    return digest_object(payload)


def seal(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result["payload_sha256"] = payload_digest(result)
    return result


def promote_booleans_to_integers(value: Any) -> None:
    """Hostile in-place JSON type promotion used by the tamper suite."""
    if isinstance(value, dict):
        for key, child in value.items():
            if isinstance(child, bool):
                value[key] = int(child)
            else:
                promote_booleans_to_integers(child)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            if isinstance(child, bool):
                value[index] = int(child)
            else:
                promote_booleans_to_integers(child)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_show(root: Path, commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(root), "show", f"{commit}:{path}"],
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


def git_blob(root: Path, commit: str, path: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), "rev-parse", f"{commit}:{path}"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    ).stdout.strip()


def is_prime_64(n: int) -> bool:
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for q in small:
        if n % q == 0:
            return n == q
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


# Polynomials use constant-first coefficient lists over F_p.
def trim(poly: list[int]) -> list[int]:
    out = [x % P for x in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(a: list[int], b: list[int]) -> list[int]:
    out = [0] * max(len(a), len(b))
    for i in range(len(a)):
        out[i] += a[i]
    for i in range(len(b)):
        out[i] += b[i]
    return trim(out)


def poly_sub(a: list[int], b: list[int]) -> list[int]:
    out = [0] * max(len(a), len(b))
    for i in range(len(a)):
        out[i] += a[i]
    for i in range(len(b)):
        out[i] -= b[i]
    return trim(out)


def poly_mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % P
    return trim(out)


def poly_pow(a: list[int], exponent: int) -> list[int]:
    out = [1]
    base = trim(a)
    e = exponent
    while e:
        if e & 1:
            out = poly_mul(out, base)
        base = poly_mul(base, base)
        e //= 2
    return out


def poly_eval(a: list[int], x: int) -> int:
    out = 0
    for coefficient in reversed(a):
        out = (out * x + coefficient) % P
    return out


def poly_compose(a: list[int], h: list[int]) -> list[int]:
    out = [0]
    for coefficient in reversed(a):
        out = poly_add(poly_mul(out, h), [coefficient])
    return out


def poly_derivative(a: list[int]) -> list[int]:
    return trim([(i * a[i]) % P for i in range(1, len(a))] or [0])


def poly_divmod(a: list[int], b: list[int]) -> tuple[list[int], list[int]]:
    dividend = trim(a)
    divisor = trim(b)
    require(divisor != [0], "polynomial division by zero")
    if len(dividend) < len(divisor):
        return [0], dividend
    quotient = [0] * (len(dividend) - len(divisor) + 1)
    inverse = pow(divisor[-1], P - 2, P)
    while dividend != [0] and len(dividend) >= len(divisor):
        shift = len(dividend) - len(divisor)
        factor = dividend[-1] * inverse % P
        quotient[shift] = factor
        for i, coefficient in enumerate(divisor):
            dividend[i + shift] = (
                dividend[i + shift] - factor * coefficient
            ) % P
        dividend = trim(dividend)
    return trim(quotient), dividend


def poly_gcd(a: list[int], b: list[int]) -> list[int]:
    left, right = trim(a), trim(b)
    while right != [0]:
        _, remainder = poly_divmod(left, right)
        left, right = right, remainder
    inverse = pow(left[-1], P - 2, P)
    return trim([(inverse * x) % P for x in left])


def product_linear(roots: list[int]) -> list[int]:
    out = [1]
    for root in roots:
        out = poly_mul(out, [(-root) % P, 1])
    return out


def derive_countermodel() -> dict[str, Any]:
    require(is_prime_64(P), "deployed base prime")
    require(P - 1 == N * 1016, "carrier index")
    require(pow(PRIMITIVE_GENERATOR, (P - 1) // 2, P) != 1, "primitive 2-part")
    require(pow(PRIMITIVE_GENERATOR, (P - 1) // 127, P) != 1, "primitive 127-part")
    require(
        pow(PRIMITIVE_GENERATOR, (P - 1) // N, P) == SUBGROUP_GENERATOR,
        "subgroup generator",
    )
    require(pow(SUBGROUP_GENERATOR, N, P) == 1, "subgroup generator power")
    require(pow(SUBGROUP_GENERATOR, N // 2, P) == P - 1, "exact subgroup order")

    carrier: set[int] = set()
    current = 1
    for _ in range(N):
        carrier.add(current)
        current = current * SUBGROUP_GENERATOR % P
    require(current == 1 and len(carrier) == N, "complete deployed carrier")

    pairs = []
    for x in sorted(carrier):
        y = (1 - x) % P
        if x < y and y in carrier:
            pairs.append([x, y])
    require(len(pairs) == 1071, "carrier internal tau-pair census")
    require(pairs[:36] == SELECTED_PAIRS, "canonical selected pairs")

    selected_roots = [x for pair in SELECTED_PAIRS for x in pair]
    require(len(set(selected_roots)) == 72, "selected root distinctness")
    require(all(x in carrier for x in selected_roots), "selected roots in carrier")
    require(all((1 - x) % P == y for x, y in SELECTED_PAIRS), "tau pairing")
    inverse_two = pow(2, P - 2, P)
    require(inverse_two not in selected_roots, "unramified selected fibers")

    outer_values = [(x * (1 - x)) % P for x, _ in SELECTED_PAIRS]
    require(len(set(outer_values)) == 36, "outer values distinct")
    active_values = outer_values[:30]
    source_values = outer_values[30:]
    require(set(active_values).isdisjoint(source_values), "active/source disjoint")

    outer_active = product_linear(active_values)
    outer_source = product_linear(source_values)
    h = [0, 1, P - 1]
    v_active = poly_compose(outer_active, h)
    source_locator = poly_compose(outer_source, h)
    direct_active = product_linear(selected_roots[:60])
    direct_source = product_linear(selected_roots[60:])
    require(v_active == direct_active, "active complete-fiber identity")
    require(source_locator == direct_source, "source complete-fiber identity")
    require(len(v_active) - 1 == 60 and v_active[-1] == 1, "active degree/monic")
    require(
        len(source_locator) - 1 == 12 and source_locator[-1] == 1,
        "source degree/monic",
    )
    require(poly_gcd(v_active, poly_derivative(v_active)) == [1], "active squarefree")
    require(
        poly_gcd(source_locator, poly_derivative(source_locator)) == [1],
        "source squarefree",
    )
    require(poly_gcd(v_active, source_locator) == [1], "active/source coprime")
    require(
        all(poly_eval(v_active, x) == 0 for x in selected_roots[:60]),
        "active roots",
    )
    require(
        all(poly_eval(source_locator, x) == 0 for x in selected_roots[60:]),
        "source roots",
    )
    require(
        poly_mul(v_active, poly_pow(source_locator, 5))
        == poly_mul(poly_compose(outer_active, h), poly_pow(poly_compose(outer_source, h), 5)),
        "rational composition cross-product",
    )
    require(
        all(poly_sub(h, [value]) == [(-value) % P, 1, P - 1] for value in source_values),
        "source locators lie in W=<1,h>",
    )

    # Direct carrier failure and the disclosed conjugacy.
    require(1 in carrier and 0 not in carrier, "literal carrier witness")
    require((1 - 1) % P == 0, "tau witness")
    require(N % P != 0, "coefficient contradiction")
    require(pow(SUBGROUP_GENERATOR, N // 2, P) == P - 1, "minus one in carrier")

    return {
        "base_prime": P,
        "extension_degree": EXTENSION_DEGREE,
        "ambient_field_cardinality": str(FIELD_SIZE),
        "carrier_order": N,
        "carrier_index_in_base_multiplicative_group": 1016,
        "primitive_generator": PRIMITIVE_GENERATOR,
        "subgroup_generator": SUBGROUP_GENERATOR,
        "subgroup_generator_order": N,
        "inner_map": "h(T)=T*(1-T)",
        "deck_involution": "tau(T)=1-T",
        "deck_order": 2,
        "deck_defined_over": "F_p subset F_(p^6)",
        "inner_map_invariant": True,
        "carrier_internal_tau_pair_count": 1071,
        "selected_pairs": SELECTED_PAIRS,
        "active_pair_count": 30,
        "source_pair_count": 6,
        "selected_root_count": 72,
        "active_root_count": 60,
        "source_root_count": 12,
        "selected_roots_all_in_carrier": True,
        "selected_fibers_unramified": True,
        "outer_values_distinct": True,
        "active_source_disjoint": True,
        "V_act_degree": 60,
        "A_degree": 12,
        "V_act_monic_squarefree": True,
        "A_monic_squarefree": True,
        "gcd_V_act_A": "1",
        "source_pencil": "W=<1,h>",
        "complete_source_locators_in_W": True,
        "V_act_in_Sym30_W": True,
        "composition": "V_act/A^5=(P/Q^5) composed with h",
        "composition_verified": True,
        "outer_active_coefficients_sha256": digest_object(outer_active),
        "outer_source_coefficients_sha256": digest_object(outer_source),
        "V_act_coefficients_sha256": digest_object(v_active),
        "A_coefficients_sha256": digest_object(source_locator),
        "direct_carrier_witness": {"x": 1, "tau_x": 0, "x_in_D": True, "tau_x_in_D": False},
        "tau_preserves_D": False,
        "coefficient_contradiction": {
            "D_root_polynomial": "X^n-1",
            "tau_D_root_polynomial": "(1-X)^n-1",
            "X^(n-1)_coefficients": [0, (-N) % P],
            "p_divides_n": False,
        },
        "map_class": "DISPLAYED_ENDPOINT_COORDINATE_ONLY",
        "conjugacy_disclosure": {
            "g": "g(T)=T-1/2",
            "conjugated_involution": "g*tau*g^-1(T)=-T",
            "minus_one_in_D": True,
            "conjugated_involution_preserves_D": True,
            "no_carrier_compatible_conjugate_claimed": False,
            "record_level_conjugacy_proved": False,
        },
        "actual_received_line_constructed": False,
        "actual_MCA_witness_constructed": False,
        "actual_endpoint_record_constructed": False,
        "actual_slice_counterexample": False,
    }


# These hashes are filled from the reviewed source tree.  The verifier treats
# all listed local sources as load-bearing and the two DAG statements as
# optional external bindings when --source-root is supplied.
SOURCE_BINDINGS = [
    {
        "binding_id": "KB_K3_SEM::primary_verifier",
        "kind": "LOCAL_SHA256",
        "path": str(PRIMARY_REL),
        "sha256": sha256_file(ROOT / PRIMARY_REL),
    },
    {
        "binding_id": "KB_K3_SEM::schema",
        "kind": "LOCAL_SHA256",
        "path": "experimental/data/schemas/kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1.schema.json",
        "sha256": "d3a4dd8d136af2f1c9a7f7a463096723f9128c9934c78966ebe26aab2d1f5605",
    },
    {
        "binding_id": "KB_K3_SEM::note",
        "kind": "LOCAL_SHA256",
        "path": "experimental/notes/thresholds/kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1.md",
        "sha256": "9aef3fdfbbf43028d726c8837dd4032eaa9c4b86c88f32be6f00e197870c39c3",
    },
    {
        "binding_id": "KB_K3_SEM::readme",
        "kind": "LOCAL_SHA256",
        "path": "experimental/data/certificates/kb-mca-v4-k3-active-slice-semantic-bridge-route-cut-v1/README.md",
        "sha256": "d43c3fa991a386b37dd49ec61ccad090538f789cb5e9520e45d4b0b068ed3245",
    },
    {
        "binding_id": "KB_K3_SEM::tangent_row_repaired",
        "kind": "LOCAL_SHA256",
        "path": "experimental/data/certificates/kb-mca-v4-tangent-source-adapter-v1/row_manifest.json",
        "sha256": "c416511796e3a196bf43f6a9f7155f499a6bf7c63dbbf52e2a64b4437e248a05",
        "internal_payload_sha256": "36e9d69aaf6deeb4fe123358e8bb8d5bbbdcb40c9315b4316f0c6a1189a270e1",
    },
    {
        "binding_id": "KB_K3_SEM::tangent_manifest_repaired",
        "kind": "LOCAL_SHA256",
        "path": "experimental/data/certificates/kb-mca-v4-tangent-source-adapter-v1/manifest.json",
        "sha256": "e21f3a454ff9e66b21dfd152d920713c1e0a61392b488c57ae8309137a887587",
        "internal_payload_sha256": "ffd1e427f53db3d2dbfd13e69a05d173d2f2aa1f03c152aead73fcc821094acb",
    },
    {
        "binding_id": "KB_K3_SEM::tangent_readme_repaired",
        "kind": "LOCAL_SHA256",
        "path": "experimental/data/certificates/kb-mca-v4-tangent-source-adapter-v1/README.md",
        "sha256": "b63faa7e06358404bf35101cbc68b65f995a9160c4a4413e7c5498086f2cc8fa",
    },
    {
        "binding_id": "KB_K3_SEM::tangent_verifier",
        "kind": "LOCAL_SHA256",
        "path": "experimental/scripts/verify_kb_mca_v4_tangent_source_adapter_v1.py",
        "sha256": "5d3fa1b34393c5c4534babd50fea4ebcc73283ab6619521b849fecef07ff6f5a",
    },
    {
        "binding_id": "KB_K3_SEM::active_v4",
        "kind": "LOCAL_SHA256",
        "path": "experimental/grande_finale.tex",
        "sha256": "336ba3c9a6d9483d0eab74677d6224aae23adf15d84891c6099f6d2f45cf226d",
        "git_blob_sha1": "6b21d6ea937a8a9f85fc7ade6032d73efd4c7222",
    },
    {
        "binding_id": "KB_K3_SEM::mca_witness_source",
        "kind": "LOCAL_SHA256",
        "path": "experimental/Conjectures_and_Barriers_RS_MCA_v4_1.tex",
        "sha256": "a26464d28d5c10284b73882ab081a04fa791659f94cbf22232055be05c59e66d",
        "git_blob_sha1": "f50d296131b471ec1e986bc0a28d81d6e0af0b11",
    },
    {
        "binding_id": "KB_K3_SEM::predecessor_1157_manifest",
        "kind": "GIT_COMMIT_SHA256",
        "commit": BASE_HEAD,
        "path": "experimental/data/certificates/kb-mca-v4-k3-source-bound-compiler-route-cut-v1/manifest.json",
        "sha256": "fec032b358fe8ef0038dec3caa8c0c20b4f5891b5a927744feef1a58b8727a29",
        "internal_payload_sha256": "5f7ae16ce2a94a02cbef0e602251686aa50d1ea4af84ed413538fabc3d9f696b",
    },
    {
        "binding_id": "KB_K3_SEM::predecessor_1157_note",
        "kind": "GIT_COMMIT_SHA256",
        "commit": BASE_HEAD,
        "path": "experimental/notes/thresholds/kb_mca_v4_k3_source_bound_compiler_route_cut_v1.md",
        "sha256": "bf90c7ddcd1671fa77b6da39cb4383702414fd0ec497fe036786719643e33c62",
    },
    {
        "binding_id": "KB_K3_SEM::historical_owner_manifest",
        "kind": "GIT_COMMIT_SHA256",
        "commit": HISTORICAL_OWNER_COMMIT,
        "path": "experimental/data/certificates/kb-mca-v4-first-gap-source-pencil-image-owner-v1/manifest.json",
        "sha256": "741681ff61a41a5c43f88fe7362839bb361b60be8ad19b1d3c59f292a8bf79e6",
        "internal_payload_sha256": "0ba2155dea1a337b17fe23d7da303b5fa3b13d4958777b977a9e768842072bf5",
    },
    {
        "binding_id": "KB_K3_SEM::historical_fixed_domain_normalization",
        "kind": "GIT_COMMIT_SHA256",
        "commit": HISTORICAL_EQUALITY_COMMIT,
        "path": "experimental/data/certificates/kb-mca-v4-equality-wall-fixed-domain-rank16-normalization-v1/certificate.json",
        "sha256": "823319e88230ee45cf5c718a0a2eba5cc88969d951d9ddcd90e57dc549a4e8e9",
        "internal_payload_sha256": "706fc1aaef763890b3ffbfbba1f750fb926ad412f2f0c66515ead393fb3318b0",
    },
    {
        "binding_id": "KB_K3_SEM::historical_source_fiber_reduction",
        "kind": "GIT_COMMIT_SHA256",
        "commit": HISTORICAL_EQUALITY_COMMIT,
        "path": "experimental/data/certificates/kb-mca-v4-rank-one-split-scroll-source-fiber-reduction-v1/certificate.json",
        "sha256": "13f662f66a353b22f8678c7021d502facd23ebe2ac2e8aae1325842de9f6fde5",
    },
    {
        "binding_id": "KB_K3_SEM::historical_residue_line_reduction",
        "kind": "GIT_COMMIT_SHA256",
        "commit": HISTORICAL_EQUALITY_COMMIT,
        "path": "experimental/data/certificates/kb-mca-v4-equality-wall-residue-line-partition-reduction-v1/certificate.json",
        "sha256": "8df41484112cb64a423f0043aa041af51ca6fdae4540b527d5b0a2733adcfab6",
        "internal_payload_sha256": "e2f3159960425614b6cb6e3bf849b2d737a6f6525e8aeb37d266804acfb9ef17",
    },
    {
        "binding_id": "KB_K3_SEM::independent_sage",
        "kind": "LOCAL_SHA256",
        "path": "experimental/scripts/verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1.sage",
        "sha256": "0e5530fbc78b950595b1766e9b184de8cbe943e93c7b6cebf40565cbda3f319c",
    },
    {
        "binding_id": "KB_K3_SEM::independent_flint",
        "kind": "LOCAL_SHA256",
        "path": "experimental/scripts/verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1_flint.py",
        "sha256": "abf4fcec275a5eaea10568ed741ce6f5ea3fe6ad359cec95c01dfa04be2e24e3",
    },
    {
        "binding_id": "KB_K3_SEM::independent_wolfram",
        "kind": "LOCAL_SHA256",
        "path": "experimental/scripts/verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1.wl",
        "sha256": "4b6ea20e6948ecd64c650b8fd2b2919fa64115bc5c9c4df29d5b75cf599f6e9b",
    },
    {
        "binding_id": "KB_K3_SEM::source_pencil_public_dag",
        "kind": "EXTERNAL_GIT_COMMIT_SHA256",
        "commit": PUBLIC_DAG_COMMIT,
        "path": "background/nodes/rate_half_kb_decomposition_source_pencil_compiler/statement.md",
        "sha256": "54b2879737b8d9f381678e35f18460ed51f092a7c2ab808aea9bf6ea9454b776",
    },
    {
        "binding_id": "KB_K3_SEM::transverse_public_dag",
        "kind": "EXTERNAL_GIT_COMMIT_SHA256",
        "commit": PUBLIC_DAG_COMMIT,
        "path": "background/nodes/rate_half_kb_source_pencil_rank_transverse_compiler/statement.md",
        "sha256": "0c1756ccf94e7b4503bf7b9aa5a39cebf16abaf1a200ec9496dd8bcf6b6f664f",
    },
]


def expected_payload(countermodel: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "theorem_kind": THEOREM_KIND,
        "base_repository": {
            "repository": "przchojecki/rs-mca",
            "base_head": BASE_HEAD,
            "parent_head": PARENT_HEAD,
            "base_is_exact_pr1157_head": True,
            "tangent_pin_repair_source_commit": PIN_REPAIR_HEAD,
            "tangent_repair_import_mode": "EXACT_THREE_FILE_PATCH_ONLY",
            "duplicate_pr1156_scalar_locator_repair": False,
        },
        "active_contract": {
            "architecture_id": ARCHITECTURE,
            "partition_sha256": PARTITION,
            "row": "KoalaBear MCA at 2^-128",
            "object": "MCA",
            "base_prime": P,
            "extension_degree": EXTENSION_DEGREE,
            "n": N,
            "k": K,
            "agreement": AGREEMENT,
            "B_star": B_STAR,
            "challenge_denominator": "FIELD_CARDINALITY",
            "unit": UNIT,
            "quantifier": QUANTIFIER,
            "first_match": True,
            "owner_order": [
                "SOURCE_COORDINATE_TANGENT_IMAGE",
                "ACTIVE_V4_BOUNDARY_PREFIX_Q",
                "ACTIVE_V4_BALANCED_CORE",
                "UNPAID_V4_COMPLEMENT",
            ],
            "atom_order": ["U_paid", "U_Q", "U_BC", "U_new"],
            "list_atom_import_forbidden": ["U_list-int", "U_ext"],
            "set_difference_equations": [
                "Z_paid=Z intersect T",
                "R1=Z setminus Z_paid",
                "Z_Q=R1 intersect Q",
                "R2=R1 setminus Z_Q",
                "Z_BC=R2 intersect BC",
                "Z_new=R2 setminus Z_BC",
            ],
        },
        "definition_inventory": [
            {
                "object": "MCA_WITNESS_RELATION",
                "defined": True,
                "executable_source_predicate": True,
                "source_bound": True,
            },
            {
                "object": "GENERIC_BALANCED_QUOTIENT_CORE",
                "defined": True,
                "executable_source_predicate": False,
                "source_bound": True,
            },
            {
                "object": "ACTIVE_V4_Q_SET",
                "defined": "SYMBOLIC_ENGLISH_LABEL_ONLY",
                "row_manifest_predicate_available_flag": True,
                "executable_source_predicate": False,
                "source_bound": False,
            },
            {
                "object": "ACTIVE_V4_BC_SET",
                "defined": "SYMBOLIC_ENGLISH_LABEL_ONLY",
                "row_manifest_predicate_available_flag": True,
                "executable_source_predicate": False,
                "source_bound": False,
            },
            {
                "object": "Z_BC^(m_in=2,r_out=4)",
                "defined": False,
                "executable_source_predicate": False,
                "source_bound": False,
            },
            {
                "object": "SUPPLIED_ENDPOINT_SOURCE_PENCIL_RECORD",
                "defined": True,
                "executable_source_predicate": True,
                "source_bound": "PER_SUPPLIED_RECORD_ONLY",
            },
            {
                "object": "THIRTEEN_ROUTE_RAW_WORKBOARD",
                "defined": True,
                "executable_source_predicate": True,
                "source_bound": False,
            },
        ],
        "required_compiler": {
            "relation_name": "Rec_2_4",
            "membership_predicate_proved": False,
            "earlier_owner_projection_proved": False,
            "total_canonical_selector_proved": False,
            "deterministic_tie_break_proved": False,
            "actual_endpoint_record_producer_proved": False,
            "reconstruction_proved": False,
            "projection_proved": False,
            "exact_projection_fiber_bound": None,
            "all_Z_BC_complement_fence_proved": False,
            "must_preserve": [
                "received_line",
                "affine_slope",
                "support",
                "explaining_polynomial_and_data",
                "balanced_core_witness",
                "source_line",
                "orientation",
                "source_cover_and_passport",
                "first_match_owner",
                "add_back_chronology",
                "field_of_definition",
                "distinctness_and_nonvanishing_guards",
            ],
        },
        "first_failed_bridge": {
            "bridge_id": "ACTIVE_M2_R4_SLICE_TO_CARRIER_SELECTOR_RECONSTRUCTION_AND_PROJECTION",
            "status": "UNDEFINED_DOMAIN_PREDICATE_AND_UNPROVEN_MAP",
            "first_false_shortcut": "DISPLAYED_ENDPOINT_PARAMETER_COORDINATE_IS_THE_EVALUATION_CARRIER",
            "actual_counterexample_available": False,
            "reason_actual_counterexample_unavailable": "THE_DECLARED_ACTIVE_SLICE_HAS_NO_EXECUTABLE_ANTECEDENT",
            "direct_coordinate_countermodel_available": True,
            "unpaid_primitive_declared": False,
        },
        "direct_coordinate_countermodel": countermodel,
        "architecture_comparison": {
            "current_architecture": ARCHITECTURE,
            "current_partition_sha256": PARTITION,
            "historical_architecture": HISTORICAL_ARCHITECTURE,
            "historical_partition_sha256": HISTORICAL_PARTITION,
            "historical_owner_count_before_Q_BC": 7,
            "historical_U_paid": 4_200_515_150_819_207,
            "historical_line_cap_68_status": "OPEN",
            "historical_primitive_69_point_exclusion_status": "OPEN",
            "historical_delta_floor": 3_912,
            "historical_half_degree_c": 67_472,
            "historical_pencil_degree_e": 134_944,
            "historical_excluded_integer_delta_interval": [3_912, 118_076],
            "historical_proved_splitting_degrees": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            "historical_open_splitting_degrees": [12, 13, 14, 15, 16],
            "historical_surviving_low_excess_h_windows": [
                {"splitting_degree": 12, "h_interval": [118_077, 132_382]},
                {"splitting_degree": 13, "h_interval": [119_375, 134_943]},
                {"splitting_degree": 14, "h_interval": [120_487, 134_943]},
                {"splitting_degree": 15, "h_interval": [121_451, 134_943]},
                {"splitting_degree": 16, "h_interval": [122_294, 134_943]},
            ],
            "historical_general_excess_delta_floor": 134_944,
            "historical_general_excess_status": "OPEN",
            "historical_69_objects_are_affine_slopes": False,
            "historical_counted_object": "DISTINCT_SOURCE_MAP_EQUIVALENCE_CLASSES_PER_TRANSVERSAL_PROJECTIVE_RESIDUE_LINE",
            "historical_image_cap_per_projective_direction": 1_894_736,
            "historical_same_map_directions_globally_deduplicated": True,
            "historical_remaining_budget": 270_780_212_960_575_880,
            "historical_cap_68_source_map_charge": 270_487_454_459_300_144,
            "historical_cap_68_reserve_margin": 292_758_501_275_736,
            "historical_cap_69_source_map_charge": 274_524_580_645_231_568,
            "historical_cap_69_reserve_deficit": 3_744_367_684_655_688,
            "current_to_historical_partition_adapter_proved": False,
            "historical_bypass_bankable": False,
        },
        "pr_reconciliation": [
            {"pr": 1130, "role": "SUPPLIED_RECORD_SOURCE_PENCIL_COMPILER", "pays_K3": False},
            {"pr": 1132, "role": "TRANSVERSE_FRONTIER_AND_ORDER_TWO_INTERFACES", "pays_K3": False},
            {"pr": 1139, "role": "CONDITIONAL_ANY69_ROUTE_CUT_AND_IMPORTED_TANGENT_PIN_REPAIR", "pays_K3": False},
            {"pr": 1143, "role": "NECESSARY_THIRTEEN_ROUTE_RAW_WORKBOARD", "pays_K3": False},
            {"pr": 1152, "role": "RAW_433_1B_TO_O0A_EXCLUSION", "pays_K3": False},
            {"pr": 1155, "role": "VALID_GUARD_TRANSPLANT_ROUTE_CUT", "pays_K3": False},
            {"pr": 1156, "role": "UNRELATED_DENOMINATOR_ROOT_AND_COORDINATE_CLONE_ROUTING", "pays_K3": False},
            {"pr": 1157, "role": "PREDECESSOR_SELECTOR_AND_UNIT_ROUTE_CUT", "pays_K3": False},
        ],
        "tangent_source_repair": {
            "source_pin_refresh": True,
            "new_payment": False,
            "transitive_source_revalidated": True,
            "lean_build_passed": True,
            "lean_correspondence_empty_axiom_census_accurate": False,
            "standard_lean_axioms_observed": ["propext", "Quot.sound"],
            "user_declared_axioms_observed": [],
            "preexisting_axiom_documentation_drift_invalidates_payment": False,
            "U_paid": U_PAID,
            "joint_remaining_reserve": RESERVE,
            "joint_reserve_is_K3_allocation": False,
            "normal_check_passed": True,
            "optimized_check_passed": True,
            "normal_tamper_selftest_passed": True,
            "optimized_tamper_selftest_passed": True,
        },
        "imported_census": {
            "predecessor_1157_bound_by_hash": True,
            "thirteen_route_count": 13,
            "raw_zero_route_count": 2,
            "open_raw_route_count": 11,
            "actual_active_slice_slope_count": None,
            "actual_endpoint_record_count": None,
            "actual_projection_fiber_bound": None,
            "raw_zero_is_slope_payment": False,
            "replayed_as_new_algebra": False,
        },
        "exact_ledger_outputs": {
            "chronology": ["U_paid", "U_Q", "U_BC", "U_new"],
            "U_paid": U_PAID,
            "U_Q": None,
            "U_BC": None,
            "U_new": None,
            "known_sum": U_PAID,
            "joint_remaining_reserve": RESERVE,
            "U_remaining": None,
            "U_positive": None,
            "U_sourcecover": None,
            "U_K3": None,
            "U_K3_allocation": None,
            "signed_slack": None,
            "inequality_evaluable": False,
            "ledger_movement": 0,
            "row_closed": False,
        },
        "source_bindings": SOURCE_BINDINGS,
        "conclusion": {
            "K3_closed": False,
            "KoalaBear_row_closed": False,
            "all_Z_BC_covered": False,
            "active_slice_bridge_proved": False,
            "direct_coordinate_carrier_inference_refuted": True,
            "arbitrary_conjugated_fold_refuted": False,
            "actual_MCA_counterexample": False,
            "official_endpoint_changed": False,
            "ledger_movement": 0,
        },
        "nonclaims": [
            "NO_ACTUAL_RECEIVED_PAIR",
            "NO_ACTUAL_RECEIVED_LINE",
            "NO_MCA_WITNESS",
            "NO_ACTIVE_Q_MEMBERSHIP",
            "NO_ACTIVE_BC_MEMBERSHIP",
            "NO_ACTIVE_M2_R4_SLICE_MEMBERSHIP",
            "NO_ACTUAL_ENDPOINT_RECORD",
            "NO_ACTUAL_IRREDUCIBLE_4_4_COMPONENT",
            "NO_K3_ORIENTATION_REALIZATION",
            "NO_EXPLAINING_DATA_DESCENT",
            "NO_FIRST_MATCH_OWNER_DESCENT",
            "NO_PROJECTION_FIBER_BOUND",
            "NO_ALL_Z_BC_COMPLEMENT_FENCE",
            "NO_UNPAID_PRIMITIVE_DECLARATION",
            "NO_ACTUAL_RECORD_COUNTEREXAMPLE",
            "NO_CLAIM_AGAINST_ARBITRARY_CONJUGACY",
            "NO_K3_ALLOCATION",
            "NO_K3_PAYMENT",
            "NO_ROW_CLOSURE",
            "NO_OFFICIAL_ENDPOINT_CHANGE",
            "NO_LIST_CHRONOLOGY_IMPORT",
            "NO_NEW_TANGENT_PAYMENT",
        ],
    }


def verify_source_bindings(source_root: Path | None) -> tuple[int, int]:
    local = 0
    external = 0
    for binding in SOURCE_BINDINGS:
        kind = binding["kind"]
        path = binding["path"]
        if kind == "LOCAL_SHA256":
            file_path = ROOT / path
            require(file_path.is_file(), f"missing local source: {path}")
            require(sha256_file(file_path) == binding["sha256"], f"source hash: {path}")
            if "git_blob_sha1" in binding:
                require(
                    subprocess.run(
                        ["git", "-C", str(ROOT), "hash-object", path],
                        check=True,
                        stdout=subprocess.PIPE,
                        text=True,
                    ).stdout.strip()
                    == binding["git_blob_sha1"],
                    f"source blob: {path}",
                )
            if "internal_payload_sha256" in binding:
                require(
                    load_json(file_path)["payload_sha256"]
                    == binding["internal_payload_sha256"],
                    f"internal source payload: {path}",
                )
            local += 1
        elif kind == "GIT_COMMIT_SHA256":
            content = git_show(ROOT, binding["commit"], path)
            require(hashlib.sha256(content).hexdigest() == binding["sha256"], f"git source hash: {path}")
            if "internal_payload_sha256" in binding:
                obj = json.loads(content, object_pairs_hook=strict_object)
                require(obj["payload_sha256"] == binding["internal_payload_sha256"], f"git internal payload: {path}")
            local += 1
        elif kind == "EXTERNAL_GIT_COMMIT_SHA256":
            if source_root is None:
                continue
            content = git_show(source_root, binding["commit"], path)
            require(hashlib.sha256(content).hexdigest() == binding["sha256"], f"external source hash: {path}")
            external += 1
        else:
            raise AssertionError(f"unknown source-binding kind: {kind}")
    return local, external


def validate_manifest(
    manifest: dict[str, Any],
    countermodel: dict[str, Any],
    *,
    check_sources: bool,
    source_root: Path | None,
) -> tuple[int, int]:
    expected = expected_payload(countermodel)
    expected_keys = set(expected) | {"payload_sha256"}
    require(set(manifest) == expected_keys, "top-level manifest keys")
    require(manifest["payload_sha256"] == payload_digest(manifest), "canonical payload seal")
    payload = copy.deepcopy(manifest)
    payload.pop("payload_sha256")
    # Canonical JSON comparison is deliberately type-strict: Python's native
    # equality would otherwise accept ``true == 1`` and ``false == 0``.
    require(canonical_bytes(payload) == canonical_bytes(expected), "manifest semantic payload")
    if check_sources:
        return verify_source_bindings(source_root)
    return 0, 0


def mutation_tests(manifest: dict[str, Any], countermodel: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("claim-slice-defined", lambda m: m["definition_inventory"][4].__setitem__("defined", True)),
        ("claim-q-executable", lambda m: m["definition_inventory"][2].__setitem__("executable_source_predicate", True)),
        ("claim-bc-executable", lambda m: m["definition_inventory"][3].__setitem__("executable_source_predicate", True)),
        ("claim-selector", lambda m: m["required_compiler"].__setitem__("total_canonical_selector_proved", True)),
        ("claim-reconstruction", lambda m: m["required_compiler"].__setitem__("reconstruction_proved", True)),
        ("claim-projection-fiber", lambda m: m["required_compiler"].__setitem__("exact_projection_fiber_bound", 1)),
        ("claim-all-zbc", lambda m: m["required_compiler"].__setitem__("all_Z_BC_complement_fence_proved", True)),
        ("claim-actual-counterexample", lambda m: m["first_failed_bridge"].__setitem__("actual_counterexample_available", True)),
        ("promote-unpaid-primitive", lambda m: m["first_failed_bridge"].__setitem__("unpaid_primitive_declared", True)),
        ("tau-preserves-D", lambda m: m["direct_coordinate_countermodel"].__setitem__("tau_preserves_D", True)),
        ("witness-not-in-D", lambda m: m["direct_coordinate_countermodel"]["direct_carrier_witness"].__setitem__("x_in_D", False)),
        ("witness-image-in-D", lambda m: m["direct_coordinate_countermodel"]["direct_carrier_witness"].__setitem__("tau_x_in_D", True)),
        ("claim-no-compatible-conjugate", lambda m: m["direct_coordinate_countermodel"]["conjugacy_disclosure"].__setitem__("no_carrier_compatible_conjugate_claimed", True)),
        ("delete-conjugacy-disclosure", lambda m: m["direct_coordinate_countermodel"].pop("conjugacy_disclosure")),
        ("wrong-map-class", lambda m: m["direct_coordinate_countermodel"].__setitem__("map_class", "ARBITRARY_PGL2_CONJUGACY")),
        ("wrong-prime", lambda m: m["direct_coordinate_countermodel"].__setitem__("base_prime", P + 2)),
        ("wrong-extension", lambda m: m["direct_coordinate_countermodel"].__setitem__("extension_degree", 5)),
        ("wrong-carrier-order", lambda m: m["direct_coordinate_countermodel"].__setitem__("carrier_order", N // 2)),
        ("wrong-generator", lambda m: m["direct_coordinate_countermodel"].__setitem__("subgroup_generator", SUBGROUP_GENERATOR + 1)),
        ("wrong-pair-count", lambda m: m["direct_coordinate_countermodel"].__setitem__("carrier_internal_tau_pair_count", 1070)),
        ("duplicate-selected-pair", lambda m: m["direct_coordinate_countermodel"]["selected_pairs"].__setitem__(1, m["direct_coordinate_countermodel"]["selected_pairs"][0])),
        ("wrong-active-count", lambda m: m["direct_coordinate_countermodel"].__setitem__("active_pair_count", 29)),
        ("wrong-source-count", lambda m: m["direct_coordinate_countermodel"].__setitem__("source_pair_count", 7)),
        ("claim-ramification", lambda m: m["direct_coordinate_countermodel"].__setitem__("selected_fibers_unramified", False)),
        ("claim-overlap", lambda m: m["direct_coordinate_countermodel"].__setitem__("active_source_disjoint", False)),
        ("wrong-degree", lambda m: m["direct_coordinate_countermodel"].__setitem__("V_act_degree", 59)),
        ("corrupt-composition", lambda m: m["direct_coordinate_countermodel"].__setitem__("composition_verified", False)),
        ("source-not-in-W", lambda m: m["direct_coordinate_countermodel"].__setitem__("complete_source_locators_in_W", False)),
        ("V-not-in-sym", lambda m: m["direct_coordinate_countermodel"].__setitem__("V_act_in_Sym30_W", False)),
        ("historical-cap-green", lambda m: m["architecture_comparison"].__setitem__("historical_line_cap_68_status", "PROVED")),
        ("historical-objects-slopes", lambda m: m["architecture_comparison"].__setitem__("historical_69_objects_are_affine_slopes", True)),
        ("wrong-architecture", lambda m: m["active_contract"].__setitem__("architecture_id", HISTORICAL_ARCHITECTURE)),
        ("wrong-partition", lambda m: m["active_contract"].__setitem__("partition_sha256", HISTORICAL_PARTITION)),
        ("import-list-atom", lambda m: m["active_contract"]["atom_order"].append("U_ext")),
        ("move-U-BC", lambda m: m["exact_ledger_outputs"].__setitem__("U_BC", 0)),
        ("move-U-K3", lambda m: m["exact_ledger_outputs"].__setitem__("U_K3", 0)),
        ("reserve-as-allocation", lambda m: m["exact_ledger_outputs"].__setitem__("U_K3_allocation", RESERVE)),
        ("hide-lean-documentation-drift", lambda m: m["tangent_source_repair"].__setitem__("lean_correspondence_empty_axiom_census_accurate", True)),
        ("ledger-movement", lambda m: m["exact_ledger_outputs"].__setitem__("ledger_movement", 1)),
        ("row-close", lambda m: m["conclusion"].__setitem__("KoalaBear_row_closed", True)),
        ("source-binding-drift", lambda m: m["source_bindings"][3].__setitem__("sha256", "0" * 64)),
        ("promote-all-booleans-to-integers", promote_booleans_to_integers),
        ("drop-nonclaim", lambda m: m["nonclaims"].pop()),
    ]
    caught: list[str] = []
    for name, mutate in mutations:
        candidate = copy.deepcopy(manifest)
        mutate(candidate)
        candidate = seal(candidate)
        try:
            validate_manifest(candidate, countermodel, check_sources=False, source_root=None)
        except (AssertionError, KeyError, TypeError):
            caught.append(name)
        else:
            raise AssertionError(f"semantic mutation escaped: {name}")
    require(len(caught) == len(mutations), "all semantic mutations caught")

    raw = MANIFEST_REL.read_text() if MANIFEST_REL.is_absolute() else (ROOT / MANIFEST_REL).read_text()
    parser_cases = {
        "duplicate-key": raw.replace('"schema":', '"schema":"duplicate",\n  "schema":', 1),
        "float": raw.replace(f'"base_prime": {P}', f'"base_prime": {P}.0', 1),
        "nan": raw.replace(f'"base_prime": {P}', '"base_prime": NaN', 1),
    }
    for name, serialized in parser_cases.items():
        try:
            json.loads(
                serialized,
                object_pairs_hook=strict_object,
                parse_float=reject_noninteger,
                parse_constant=reject_noninteger,
            )
        except AssertionError:
            caught.append("parser-" + name)
        else:
            raise AssertionError(f"parser mutation escaped: {name}")
    return caught


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()

    countermodel = derive_countermodel()
    manifest = load_json(ROOT / MANIFEST_REL)

    if args.check:
        local, external = validate_manifest(
            manifest,
            countermodel,
            check_sources=True,
            source_root=args.source_root,
        )
        print(
            "PASS K3 ACTIVE-SLICE SEMANTIC ROUTE CUT "
            f"carrier={N} tau_pairs=1071 selected=36 local_sources={local} "
            f"external_sources={external} U_paid={U_PAID} movement=0"
        )
        return 0

    validate_manifest(manifest, countermodel, check_sources=False, source_root=None)
    caught = mutation_tests(manifest, countermodel)
    semantic = len(caught) - 3
    print(
        "PASS tamper-selftest: "
        f"{semantic} semantic and 3 parser mutations rejected"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
