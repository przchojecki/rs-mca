#!/usr/bin/env python3
"""Deterministic replay for the M31 flatness keystone constant-shift obstruction.

Python is a replay/audit layer.  The mathematical proof is the degree argument
in the accompanying note.  This verifier reconstructs the explicit finite
field domain, checks the common locator prefix, and validates every deployed
integer and artifact hash.  It intentionally does not inspect agents.md,
PR_BODY.md, or any agents-log entry file.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable

PACKET_ID = "m31-flatness-keystone-constant-shift-obstruction-v1"
NOTE_REL = Path("experimental/notes/thresholds/m31_flatness_keystone_constant_shift_obstruction.md")
SCRIPT_REL = Path("experimental/scripts/verify_m31_flatness_keystone_constant_shift_obstruction.py")
CERT_REL = Path(
    "experimental/data/certificates/"
    "m31-flatness-keystone-constant-shift-obstruction/"
    "m31_flatness_keystone_constant_shift_obstruction.json"
)
LEAN_ROOT_REL = Path("experimental/lean/m31_alt_domain_fiber")
LEAN_MODULE_REL = LEAN_ROOT_REL / "M31AltDomainFiber.lean"
LEAN_CORRESPONDENCE_REL = LEAN_ROOT_REL / "CORRESPONDENCE.md"
LEAN_LAKEFILE_REL = LEAN_ROOT_REL / "lakefile.lean"
LEAN_TOOLCHAIN_REL = LEAN_ROOT_REL / "lean-toolchain"
LEAN_GITIGNORE_REL = LEAN_ROOT_REL / ".gitignore"
HASHED_ARTIFACTS = (
    NOTE_REL,
    SCRIPT_REL,
    LEAN_MODULE_REL,
    LEAN_CORRESPONDENCE_REL,
    LEAN_LAKEFILE_REL,
    LEAN_TOOLCHAIN_REL,
    LEAN_GITIGNORE_REL,
)

P = 2**31 - 1
G = 7
PREFIX_DEPTH = 32
BLOCK_DEGREE = PREFIX_DEPTH + 1
TOTAL_BLOCKS = 31
INTACT_BLOCKS = 30
SELECTED_BLOCKS = 14
CORE_SIZE = 17
SUPPORT_SIZE = SELECTED_BLOCKS * BLOCK_DEGREE + CORE_SIZE
BASE_DOMAIN_SIZE = 1024
PUNCTURE_COUNT = 2
DOMAIN_SIZE = BASE_DOMAIN_SIZE - PUNCTURE_COUNT
B_STAR = 2**24 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
ERRORS = 981_129

EXPECTED_TOP_KEYS = {
    "activity",
    "arithmetic",
    "artifact_hashes",
    "claims",
    "construction",
    "impact",
    "nonclaims",
    "packet_id",
    "provenance",
    "row",
    "schema_version",
    "scope_labels",
    "status",
}


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def digest_int_list(values: list[int]) -> str:
    payload = json.dumps(values, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    return sha256_bytes(payload)


def is_prime_trial(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def poly_mul_mod(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return out


def locator_mod(points: list[int], p: int) -> list[int]:
    """Ascending coefficients of the monic locator."""
    poly = [1]
    for x in points:
        poly = poly_mul_mod(poly, [(-x) % p, 1], p)
    return poly


def build_expected() -> dict[str, Any]:
    require(is_prime_trial(P), "p is not prime")
    require(N == 2_097_152 and K == 1_048_576, "deployed length/dimension drift")
    require(AGREEMENT + ERRORS == N, "agreement/error complement drift")
    require(P**4 // 2**100 == B_STAR, "deployed budget formula drift")

    factorization = {"2": 1, "3": 2, "7": 1, "11": 1, "31": 1, "151": 1, "331": 1}
    factor_product = math.prod(int(q) ** e for q, e in factorization.items())
    require(factor_product == P - 1, "factorization of p-1 is wrong")
    for q_text in factorization:
        q = int(q_text)
        require(pow(G, (P - 1) // q, P) != 1, f"g fails primitive-root gate q={q}")

    step = (P - 1) // BLOCK_DEGREE
    require(step * BLOCK_DEGREE == P - 1, "33 does not divide p-1")
    zeta = pow(G, step, P)
    require(pow(zeta, BLOCK_DEGREE, P) == 1, "zeta^33 != 1")
    require(pow(zeta, BLOCK_DEGREE // 3, P) != 1, "zeta order divides 11")
    require(pow(zeta, BLOCK_DEGREE // 11, P) != 1, "zeta order divides 3")

    cosets: list[list[int]] = []
    lambdas: list[int] = []
    for i in range(TOTAL_BLOCKS):
        a_i = pow(G, i, P)
        block = [(a_i * pow(zeta, j, P)) % P for j in range(BLOCK_DEGREE)]
        require(len(set(block)) == BLOCK_DEGREE, f"block {i} is not simple")
        lam = pow(a_i, BLOCK_DEGREE, P)
        require(all(pow(x, BLOCK_DEGREE, P) == lam for x in block), f"block {i} root law failed")
        cosets.append(block)
        lambdas.append(lam)

    union = [x for block in cosets for x in block]
    require(len(union) == TOTAL_BLOCKS * BLOCK_DEGREE, "wrong pre-puncture union size")
    require(len(set(union)) == len(union), "33-cosets overlap")
    require(len(set(lambdas)) == TOTAL_BLOCKS, "block constants are not distinct")

    punctured_point = pow(G, TOTAL_BLOCKS - 1, P)
    sentinel = pow(G, TOTAL_BLOCKS, P)
    require(punctured_point in cosets[-1], "chosen puncture not in last block")
    require(sentinel not in set(union), "sentinel lies in the 31-block union")

    base_domain = set(union)
    base_domain.add(sentinel)
    require(len(base_domain) == BASE_DOMAIN_SIZE, "base domain is not 1024 points")
    domain = sorted(base_domain - {punctured_point, sentinel})
    require(len(domain) == DOMAIN_SIZE, "punctured domain is not 1022 points")

    core = [
        (pow(G, TOTAL_BLOCKS - 1, P) * pow(zeta, j, P)) % P
        for j in range(1, CORE_SIZE + 1)
    ]
    require(len(set(core)) == CORE_SIZE, "core is not simple")
    require(set(core).issubset(domain), "core is not contained in the punctured domain")

    core_locator = locator_mod(core, P)
    require(len(core_locator) == CORE_SIZE + 1 and core_locator[-1] == 1, "bad core locator")
    common_prefix = list(reversed(core_locator[:-1])) + [0] * (PREFIX_DEPTH - CORE_SIZE)
    require(len(common_prefix) == PREFIX_DEPTH, "common prefix has wrong length")

    # Directly build two full support locators, one at each end of the block index range.
    # Each block locator is X^33-lambda_i.
    prefixes: list[list[int]] = []
    for selection in (tuple(range(SELECTED_BLOCKS)), tuple(range(INTACT_BLOCKS - SELECTED_BLOCKS, INTACT_BLOCKS))):
        support = list(core)
        for i in selection:
            support.extend(cosets[i])
        require(len(support) == SUPPORT_SIZE, "support size is not 479")
        require(len(set(support)) == SUPPORT_SIZE, "support has duplicate points")
        locator = locator_mod(support, P)
        require(len(locator) == SUPPORT_SIZE + 1 and locator[-1] == 1, "bad support locator")
        prefix = [locator[SUPPORT_SIZE - j] for j in range(1, PREFIX_DEPTH + 1)]
        prefixes.append(prefix)
    require(prefixes[0] == common_prefix == prefixes[1], "direct common-prefix check failed")

    # Symbolic degree gate: after the leading X^(14*33) term, the block product
    # has degree at most 13*33; multiplying by the degree-17 core gives 446.
    lower_tail_degree = CORE_SIZE + (SELECTED_BLOCKS - 1) * BLOCK_DEGREE
    require(lower_tail_degree == 446, "unexpected lower-tail degree")
    first_fixed_degree = SUPPORT_SIZE - PREFIX_DEPTH
    require(first_fixed_degree == 447, "unexpected fixed-prefix degree boundary")
    require(lower_tail_degree < first_fixed_degree, "degree argument does not cover 32 coefficients")

    family_size = math.comb(INTACT_BLOCKS, SELECTED_BLOCKS)
    target_count = P**PREFIX_DEPTH
    total_supports = math.comb(DOMAIN_SIZE, SUPPORT_SIZE)
    floor_average, remainder = divmod(total_supports, target_count)
    ceil_average = floor_average + (1 if remainder else 0)

    require(family_size == 145_422_675, "family count drift")
    require(ceil_average == 3_614_120, "ambient average drift")
    require(family_size - 8 * B_STAR == 11_204_955, "budget multiple arithmetic drift")
    require(family_size - 40 * ceil_average == 857_875, "average multiple arithmetic drift")
    require(B_STAR - 4 * ceil_average == 2_320_735, "four-average room drift")
    require(5 * ceil_average - B_STAR == 1_293_385, "five-average comparison drift")

    return {
        "schema_version": 1,
        "packet_id": PACKET_ID,
        "activity": "FALSIFY",
        "status": "PROVED",
        "impact": "ROUTE_CUT",
        "scope_labels": [
            "COUNTEREXAMPLE_TO_DOMAIN_AGNOSTIC_FLATNESS",
            "LOCAL_ONLY",
        ],
        "provenance": {
            "fork_base_sha": "d968e1cb9a3a6dbcfba35ecf9f448b4a373a35bb",
            "upstream_base_sha": "71f64349a8fa8cbf05678a6e9d4e00e8e06d7de5",
            "integrated_t64_t16_note_path": "experimental/notes/thresholds/m31_quotient_band_swap_census_t16_mixing.md",
            "integrated_t64_t16_note_git_blob_sha": "9f2756cd3225787d4990acca9474fffb7ccd7e9e",
            "steering_files_are_provenance_only": True,
        },
        "row": {
            "workboard_item": "M1",
            "name": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "target_epsilon": "2^-100",
            "length": N,
            "dimension": K,
            "agreement": AGREEMENT,
            "errors": ERRORS,
            "B_star": B_STAR,
            "projection_and_unit": "479-subsets per first-32 nonleading locator-coefficient target; support-level only",
        },
        "construction": {
            "p": P,
            "p_minus_1_factorization": factorization,
            "primitive_root": G,
            "block_degree": BLOCK_DEGREE,
            "coset_step": step,
            "zeta": zeta,
            "total_complete_blocks_before_puncture": TOTAL_BLOCKS,
            "intact_blocks_after_puncture": INTACT_BLOCKS,
            "base_domain_size": BASE_DOMAIN_SIZE,
            "puncture_count": PUNCTURE_COUNT,
            "punctured_block_index": TOTAL_BLOCKS - 1,
            "punctured_point": punctured_point,
            "sentinel_point": sentinel,
            "domain_size": DOMAIN_SIZE,
            "core_exponents": list(range(1, CORE_SIZE + 1)),
            "core_size": CORE_SIZE,
            "selected_blocks": SELECTED_BLOCKS,
            "support_size": SUPPORT_SIZE,
            "prefix_depth": PREFIX_DEPTH,
            "lower_tail_degree": lower_tail_degree,
            "first_fixed_degree": first_fixed_degree,
            "common_prefix32": common_prefix,
            "digests": {
                "complete_cosets_sha256": sha256_bytes(
                    json.dumps([sorted(block) for block in cosets], separators=(",", ":")).encode("ascii")
                ),
                "domain_sha256": digest_int_list(domain),
                "core_sha256": digest_int_list(sorted(core)),
                "block_constants_sha256": digest_int_list(lambdas),
                "common_prefix32_sha256": digest_int_list(common_prefix),
            },
        },
        "arithmetic": {
            "target_count_p_power_32": str(target_count),
            "total_479_subsets": str(total_supports),
            "floor_ambient_average": floor_average,
            "ambient_average_remainder": str(remainder),
            "ceil_ambient_average": ceil_average,
            "constant_shift_fiber_size": family_size,
            "fiber_minus_8_B_star": family_size - 8 * B_STAR,
            "fiber_minus_40_ceil_average": family_size - 40 * ceil_average,
            "B_star_minus_4_ceil_average": B_STAR - 4 * ceil_average,
            "five_ceil_average_minus_B_star": 5 * ceil_average - B_STAR,
        },
        "claims": [
            "An explicit two-puncture 1022-point domain over F_p has a depth-32 prefix fiber of 145422675 distinct 479-subsets.",
            "The certified fiber exceeds eight times B_star by 11204955 and forty times the ceiling ambient average by 857875.",
            "Therefore no theorem using only p, domain size, support size, prefix depth, and the ambient average can prove the M31 budget for all domains.",
        ],
        "nonclaims": [
            "No prefix-fiber upper or lower bound is proved for the deployed Chebyshev quotient domain.",
            "No received word, codeword, first-match survivor, or row-global list counterexample is constructed.",
            "No classification of constant-shift packets inside the deployed Chebyshev domain is claimed.",
        ],
        "artifact_hashes": {},
    }


def validate_loaded(data: dict[str, Any], root: Path, check_artifacts: bool) -> None:
    require(set(data) == EXPECTED_TOP_KEYS, f"top-level keys mismatch: {sorted(set(data) ^ EXPECTED_TOP_KEYS)}")
    expected = build_expected()
    expected_hashes = data.get("artifact_hashes")
    require(isinstance(expected_hashes, dict), "artifact_hashes must be an object")
    expected["artifact_hashes"] = expected_hashes
    require(data == expected, "certificate content differs from independent reconstruction")

    if check_artifacts:
        required_hash_paths = {path.as_posix() for path in HASHED_ARTIFACTS}
        require(set(expected_hashes) == required_hash_paths, "artifact hash path set mismatch")
        for rel_text, expected_sha in expected_hashes.items():
            path = root / rel_text
            require(path.is_file(), f"missing artifact: {rel_text}")
            require(sha256_file(path) == expected_sha, f"artifact hash mismatch: {rel_text}")


def load_certificate(root: Path) -> tuple[dict[str, Any], bytes]:
    cert_path = root / CERT_REL
    require(cert_path.is_file(), f"missing certificate: {CERT_REL}")
    raw = cert_path.read_bytes()
    data = json.loads(raw.decode("utf-8"))
    require(isinstance(data, dict), "certificate must be a JSON object")
    require(raw == canonical_json_bytes(data), "certificate JSON is not canonical")
    return data, raw


def run_check(root: Path) -> None:
    data, _ = load_certificate(root)
    validate_loaded(data, root, check_artifacts=True)
    arithmetic = data["arithmetic"]
    construction = data["construction"]
    print(f"PASS {PACKET_ID}")
    print(f"domain={construction['domain_size']} support={construction['support_size']} depth={construction['prefix_depth']}")
    print(f"fiber={arithmetic['constant_shift_fiber_size']} ceil_average={arithmetic['ceil_ambient_average']} B*={data['row']['B_star']}")
    print("verdict=COUNTEREXAMPLE_TO_DOMAIN_AGNOSTIC_FLATNESS")


def expect_reject(root: Path, base: dict[str, Any], label: str, mutate: Callable[[dict[str, Any]], None], *, artifacts: bool = False) -> None:
    candidate = copy.deepcopy(base)
    mutate(candidate)
    try:
        validate_loaded(candidate, root, check_artifacts=artifacts)
    except CheckError:
        return
    raise CheckError(f"tamper was accepted: {label}")


def run_tamper_selftest(root: Path) -> None:
    base, _ = load_certificate(root)
    validate_loaded(base, root, check_artifacts=True)

    tests: list[tuple[str, Callable[[dict[str, Any]], None], bool]] = [
        ("p", lambda d: d["construction"].__setitem__("p", P + 2), False),
        ("zeta", lambda d: d["construction"].__setitem__("zeta", d["construction"]["zeta"] + 1), False),
        ("domain size", lambda d: d["construction"].__setitem__("domain_size", 1021), False),
        ("block degree", lambda d: d["construction"].__setitem__("block_degree", 32), False),
        ("selected blocks", lambda d: d["construction"].__setitem__("selected_blocks", 15), False),
        ("support size", lambda d: d["construction"].__setitem__("support_size", 478), False),
        ("prefix depth", lambda d: d["construction"].__setitem__("prefix_depth", 31), False),
        ("prefix coefficient", lambda d: d["construction"]["common_prefix32"].__setitem__(0, (d["construction"]["common_prefix32"][0] + 1) % P), False),
        ("domain digest", lambda d: d["construction"]["digests"].__setitem__("domain_sha256", "0" * 64), False),
        ("family size", lambda d: d["arithmetic"].__setitem__("constant_shift_fiber_size", 145_422_674), False),
        ("average", lambda d: d["arithmetic"].__setitem__("ceil_ambient_average", 3_614_121), False),
        ("status", lambda d: d.__setitem__("status", "COMPUTED"), False),
        ("impact", lambda d: d.__setitem__("impact", "BANKABLE_ATOM"), False),
        ("note hash", lambda d: d["artifact_hashes"].__setitem__(NOTE_REL.as_posix(), "f" * 64), True),
        ("Lean hash", lambda d: d["artifact_hashes"].__setitem__(LEAN_MODULE_REL.as_posix(), "e" * 64), True),
        ("unknown key", lambda d: d.__setitem__("extra", 1), False),
    ]

    for label, mutate, artifacts in tests:
        expect_reject(root, base, label, mutate, artifacts=artifacts)
    print(f"PASS tamper-selftest: {len(tests)} mutations rejected")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate the packet")
    parser.add_argument("--tamper-selftest", action="store_true", help="run hostile certificate mutations")
    args = parser.parse_args(argv)
    if not args.check and not args.tamper_selftest:
        parser.error("select --check and/or --tamper-selftest")
    return args


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = Path(__file__).resolve().parents[2]
    try:
        if args.check:
            run_check(root)
        if args.tamper_selftest:
            run_tamper_selftest(root)
    except (CheckError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
