#!/usr/bin/env python3
"""Independent verifier for the KoalaBear tangent-rooted Q conditional packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.set_int_max_str_digits(0)

PACKET = "kb-uq-boundary-prefix-tangent-rooted-shell-v1"
SCRIPT_REL = Path("experimental/scripts/verify_kb_uq_boundary_prefix_tangent_rooted_shell_v1.py")
NOTE_REL = Path("experimental/notes/frontier-adjacent/kb_uq_boundary_prefix_tangent_rooted_shell_v1.md")
CERT_REL = Path("experimental/data/certificates") / PACKET
MANIFEST_REL = CERT_REL / "manifest.json"
HASHES_REL = CERT_REL / "hashes.json"
ROUND1_ROW_REL = CERT_REL / "round1_row_manifest.json"
LEAN_REL = Path("experimental/lean/kb_uq_boundary_prefix/KbUqBoundaryPrefix.lean")
# Transport-only files: carried by the PR bundle, deliberately never imported
# upstream.  `hashes.json` still records them, so the in-repo gate checks every
# retained artifact and requires the omissions to be exactly this set.
TRANSPORT_ONLY = frozenset({
    "PR_BODY.md",
    "experimental/agents-log-entry-gptpro-kb-uq-boundary-prefix.md",
    "experimental/agents-log-kb-uq-boundary-prefix.patch",
})
# Upstream steering files are recorded for provenance, not gated.  `agents.md` is
# rewritten by governance commits -- fb6d955 replaced the blob this packet froze --
# so drift there must report, never fail.
STEERING_SOURCES = frozenset({"agents.md"})

EXPECTED = {
    "p": 2_130_706_433,
    "extension_degree": 6,
    "n": 2_097_152,
    "k": 1_048_576,
    "a": 1_116_048,
    "t": 981_104,
    "w": 67_471,
    "e_min": 67_473,
    "sparse_shell_count": 913_632,
    "B_star": 274_980_728_111_395_087,
    "paid": 981_104,
    "reserve": 274_980_728_110_413_983,
    "floor_xq": 57_198_030_365,
    "ceil_xq": 57_198_030_366,
    "floor_7xq": 400_386_212_557,
    "sparse_cap": 400_388_953_453,
    "uniform_cap": 400_389_155_870,
    "pruning_dividend": 202_417,
    "partial_total": 400_390_136_974,
    "remaining": 274_980_327_721_258_113,
    "bmax_c0": 280_276_839_265,
    "cmax_b0": 4_807_520,
    "bmax_cmax": 54_192,
    "corner_cap": 274_980_728_110_019_048,
    "corner_remaining": 394_935,
    "next_b_cap": 274_980_728_111_000_152,
    "next_b_excess": 586_169,
    "next_c_cap": 274_980_732_140_061_446,
    "next_c_excess": 4_029_647_463,
    "prime_count": 155_611,
    "factor_count": 105_726,
    "x_bits": 2_090_874,
    "q_bits": 2_090_838,
    "h_bits": 721_939,
    "margin": 953_462_079_457,
    "x_hash": "e2a3e4a63e81ffc3388cf4f33a6592b7ced29f14219b74d5c6d67e9b5036e066",
    "q_hash": "f3cd891754f52acf2ea27de139afeccf396336284d1bb321a9a8bf4b6af9406f",
    "rem_hash": "eab3fa93125841b71210ec5881d434852033524e3e72ea9fed7aab3a91c8c465",
    "h_hash": "a3d7f5cb854cdbf23260eac5d24bf2c8223a9176011d08ec89590b7b537ef90b",
    "partition": "4fade91abc408264989babcff6f8f9bbd80bcec52545a5db15ac376bf17d88fc",
    "architecture": "GRANDE_FINALE_V4_KB_MCA_TANGENT_SOURCE_ADAPTER_V1",
}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_decimal(value: int) -> str:
    return sha256_bytes(str(value).encode("ascii"))


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise VerificationError(f"cannot read JSON {path}: {exc}") from exc


def sieve_primes(limit: int) -> list[int]:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for q in range(2, math.isqrt(limit) + 1):
        if flags[q]:
            start = q * q
            flags[start : limit + 1 : q] = b"\x00" * (((limit - start) // q) + 1)
    return [q for q, flag in enumerate(flags) if flag]


def vp_factorial(n: int, q: int) -> int:
    total = 0
    while n:
        n //= q
        total += n
    return total


def binomial_from_primes(n: int, r: int, primes: list[int]) -> tuple[int, int]:
    value = 1
    nonzero = 0
    for q in primes:
        exponent = vp_factorial(n, q) - vp_factorial(r, q) - vp_factorial(n - r, q)
        if exponent:
            nonzero += 1
            value *= q**exponent
    return value, nonzero


def product_binomials_from_primes(
    n1: int, r1: int, n2: int, r2: int, primes: list[int]
) -> int:
    value = 1
    for q in primes:
        exponent = (
            vp_factorial(n1, q)
            - vp_factorial(r1, q)
            - vp_factorial(n1 - r1, q)
            + vp_factorial(n2, q)
            - vp_factorial(r2, q)
            - vp_factorial(n2 - r2, q)
        )
        if exponent:
            value *= q**exponent
    return value


def square_and_multiply(base: int, exponent: int) -> int:
    result = 1
    x = base
    e = exponent
    while e:
        if e & 1:
            result *= x
        x *= x
        e >>= 1
    return result


def validate_manifest(root: Path) -> dict[str, Any]:
    manifest = load_json(root / MANIFEST_REL)
    rc = manifest["row_contract"]
    comp = manifest["compiler"]
    window = manifest["viable_window"]
    replay = manifest["independent_replay"]
    hyp = manifest["conditional_hypothesis"]
    round1 = manifest["round1"]

    require(manifest["schema"] == "rs-mca-kb-uq-boundary-prefix-tangent-rooted-shell-v1", "schema")
    require(manifest["status"] == "CONDITIONAL", "status")
    require(manifest["impact"] == "BANKABLE_ATOM", "impact")
    require(manifest["workboard_item"] == "K2", "workboard")
    require(manifest["architecture_id"] == EXPECTED["architecture"], "architecture")
    require(manifest["partition_sha256"] == EXPECTED["partition"], "partition")
    require(
        manifest["owner_order"]
        == [
            "SOURCE_COORDINATE_TANGENT_IMAGE",
            "ACTIVE_V4_BOUNDARY_PREFIX_Q",
            "ACTIVE_V4_BALANCED_CORE",
            "UNPAID_V4_COMPLEMENT",
        ],
        "owner order",
    )
    for key, expected in [
        ("base_prime", EXPECTED["p"]),
        ("extension_degree", EXPECTED["extension_degree"]),
        ("n", EXPECTED["n"]),
        ("k", EXPECTED["k"]),
        ("agreement", EXPECTED["a"]),
        ("t", EXPECTED["t"]),
        ("B_star", EXPECTED["B_star"]),
    ]:
        require(rc[key] == expected, f"row_contract.{key}")
    require(rc["quantifier"] == "UNIFORM_OVER_ALL_ADMISSIBLE_RECEIVED_LINES", "quantifier")
    require(rc["unit"] == "DISTINCT_BAD_FINITE_SLOPES_PER_RECEIVED_LINE", "unit")
    require(round1["U_paid"] == EXPECTED["paid"], "round1 paid")
    require(round1["reserve"] == EXPECTED["reserve"], "round1 reserve")
    require(hyp["name"] == "KB_TANGENT_ROOTED_Q_SHELL", "hypothesis name")
    require((hyp["b"], hyp["c"]) == (3, 7), "hypothesis constants")
    require(hyp["prefix_depth_w"] == EXPECTED["w"], "prefix depth")
    require(hyp["non_column_far_shell_range"] == [EXPECTED["e_min"], EXPECTED["t"]], "sparse range")
    require(hyp["column_far_shell_range"] == [1, EXPECTED["t"]], "far range")

    manifest_checks = {
        "sparse_shell_count": EXPECTED["sparse_shell_count"],
        "floor_X_over_Q": EXPECTED["floor_xq"],
        "ceil_X_over_Q": EXPECTED["ceil_xq"],
        "floor_7X_over_Q": EXPECTED["floor_7xq"],
        "floor_7Xm1_over_Q": EXPECTED["floor_7xq"],
        "U_Q_sparse": EXPECTED["sparse_cap"],
        "U_Q_uniform": EXPECTED["uniform_cap"],
        "pruning_dividend": EXPECTED["pruning_dividend"],
        "partial_total": EXPECTED["partial_total"],
        "remaining_reserve": EXPECTED["remaining"],
    }
    for key, expected in manifest_checks.items():
        require(comp[key] == expected, f"compiler.{key}")

    window_checks = {
        "b_max_at_c0": EXPECTED["bmax_c0"],
        "c_max_at_b0": EXPECTED["cmax_b0"],
        "b_max_at_c_max": EXPECTED["bmax_cmax"],
        "corner_cap": EXPECTED["corner_cap"],
        "corner_remaining": EXPECTED["corner_remaining"],
        "next_b_cap": EXPECTED["next_b_cap"],
        "next_b_excess": EXPECTED["next_b_excess"],
        "next_c_cap": EXPECTED["next_c_cap"],
        "next_c_excess": EXPECTED["next_c_excess"],
    }
    for key, expected in window_checks.items():
        require(window[key] == expected, f"viable_window.{key}")

    replay_checks = {
        "prime_count_to_n": EXPECTED["prime_count"],
        "nonzero_binomial_prime_factors": EXPECTED["factor_count"],
        "X_bit_length": EXPECTED["x_bits"],
        "Q_bit_length": EXPECTED["q_bits"],
        "H_w1_bit_length": EXPECTED["h_bits"],
        "shell_monotonicity_margin": EXPECTED["margin"],
        "X_decimal_sha256": EXPECTED["x_hash"],
        "Q_decimal_sha256": EXPECTED["q_hash"],
        "remainder_decimal_sha256": EXPECTED["rem_hash"],
        "H_w1_decimal_sha256": EXPECTED["h_hash"],
    }
    for key, expected in replay_checks.items():
        require(replay[key] == expected, f"independent_replay.{key}")

    require(len(manifest["source_bindings"]) == 8, "source binding count")
    require("A1_UNCONDITIONAL_Q" in manifest["nonclaims"], "nonclaim A1")
    require("ROW_CLOSURE" in manifest["nonclaims"], "nonclaim row closure")
    return manifest



def validate_frozen_row_manifest(root: Path, manifest: dict[str, Any]) -> None:
    path = root / ROUND1_ROW_REL
    data_bytes = path.read_bytes()
    require(git_blob_sha1(data_bytes) == manifest["round1"]["row_manifest_blob"], "round1 row-manifest blob")
    row = load_json(path)
    require(row["architecture_id"] == EXPECTED["architecture"], "round1 architecture")
    partition = row["partition"]
    require(partition["partition_sha256"] == EXPECTED["partition"], "round1 partition pin")
    digest_object = dict(partition)
    digest_object.pop("partition_sha256")
    digest_object.pop("partition_digest_method")
    canonical = json.dumps(digest_object, sort_keys=True, separators=(",", ":")).encode("utf-8")
    require(sha256_bytes(canonical) == EXPECTED["partition"], "round1 partition digest replay")
    require(partition["owner_order"] == manifest["owner_order"], "round1 owner order")
    require(partition["quantifier"] == manifest["row_contract"]["quantifier"], "round1 quantifier")
    require(partition["unit"] == manifest["row_contract"]["unit"], "round1 unit")
    require(partition["canonical_translation"]["alternative_translation_union_forbidden"], "round1 translation prohibition")
    require(partition["canonical_translation"]["column_far_case"] == "EMPTY_SOURCE_COORDINATE_TANGENT_IMAGE", "round1 column-far branch")
    require(row["row_contract"]["B_star"] == EXPECTED["B_star"], "round1 B_star")
    require(row["row_contract"]["agreement"] == EXPECTED["a"], "round1 agreement")

def validate_source_pins(root: Path, manifest: dict[str, Any]) -> tuple[int, int]:
    checked = 0
    external = 0
    for binding in manifest["source_bindings"]:
        path = root / binding["path"]
        if path.is_file():
            actual = git_blob_sha1(path.read_bytes())
            if binding["path"] in STEERING_SOURCES:
                if actual != binding["blob"]:
                    print(
                        f"NOTE steering source drifted: {binding['path']} "
                        f"recorded {binding['blob']}, observed {actual}"
                    )
                checked += 1
                continue
            require(actual == binding["blob"], f"source blob drift: {binding['path']}")
            checked += 1
        else:
            external += 1
    return checked, external


def validate_text_contract(root: Path) -> None:
    note = (root / NOTE_REL).read_text(encoding="utf-8")
    required_note = [
        "workboard_item: K2",
        "status: CONDITIONAL",
        "impact: BANKABLE_ATOM",
        "KB_TANGENT_ROOTED_Q_SHELL(3,7)",
        "Z_Q=(Z\\setminus\\mathcal T(r))\\cap Q",
        "thm:exact-sparsification",
        "mcaBad_sub_mem_iff",
        "thm:canonical-partial-occupancy-atlas",
        "def:primitive-q",
        "eq:exact-power-sum-map",
        "prop:q-boundary-divisor",
        "conj:q-active",
        "400{,}389{,}155{,}870",
        "274{,}980{,}327{,}721{,}258{,}113",
        "Mandatory adversarial epilogue",
        "Column-far branch",
        "No unconditional A2 integer is claimed",
        "No admissible family with certified active-Q membership",
        "# CONDITIONAL",
    ]
    for token in required_note:
        require(token in note, f"note missing: {token}")
    require("422{,}354{,}730{,}332" not in note, "legacy M1 integer imported")
    require("alternative translation" not in note.lower(), "alternative translation wording")

    lean = (root / LEAN_REL).read_text(encoding="utf-8")
    for token in [
        "theorem shellCompilerNoRoot",
        "theorem shellCompilerWithRoot",
        "theorem deployed_uniform_cap",
        "theorem deployed_window_corner",
        "import Std",
    ]:
        require(token in lean, f"Lean missing: {token}")
    forbidden_patterns = [r"(?m)^\s*axiom\b", r"\bsorry\b", r"\badmit\b", r"Mathlib"]
    for pattern in forbidden_patterns:
        require(re.search(pattern, lean) is None, f"forbidden Lean marker: {pattern}")

    require(not (root / ".github").exists(), "packet modifies .github")
    for path in root.rglob(".lake"):
        require(not path.exists(), f"forbidden .lake directory: {path}")


def validate_pr_body(root: Path) -> None:
    lines = (root / PR_BODY_REL).read_text(encoding="utf-8").splitlines()
    require(len(lines) == 7, "PR_BODY must have exactly 7 lines")
    require(1 <= len(lines[0].split()) <= 6, "PR title word count")
    require(lines[1] == "STATUS: CONDITIONAL / BANKABLE_ATOM / ROW OPEN", "PR status line")
    prefixes = ["- Claim:", "- Status:", "- Verifier:", "- Consumers:", "- Risk-limits:"]
    for line, prefix in zip(lines[2:], prefixes, strict=True):
        require(line.startswith(prefix), f"PR bullet prefix {prefix}")
        words = re.findall(r"\S+", line[len(prefix) :])
        require(len(words) <= 50, f"PR bullet over 50 words: {prefix}")
    body_lower = "\n".join(lines).lower()
    for forbidden in ["branch", "draft", "session", "tool link"]:
        require(forbidden not in body_lower, f"process wording in PR_BODY: {forbidden}")


def validate_log_entry(root: Path) -> None:
    text = (root / LOG_ENTRY_REL).read_text(encoding="utf-8")
    for token in [
        "### 2026-07-22 - KoalaBear tangent-rooted Q conditional cap",
        "- **Agent/model:** GPT-5.6 Pro",
        "- **Files added or changed:**",
        "- **Status:** CONDITIONAL / BANKABLE_ATOM / ROW OPEN.",
        "- **What is being added:**",
        "- **How it is useful:**",
        "- **What to do next:**",
    ]:
        require(token in text, f"agents-log entry missing: {token}")
    patch = (root / LOG_PATCH_REL).read_text(encoding="utf-8")
    require("@@" in patch and "KoalaBear tangent-rooted Q conditional cap" in patch, "log patch")


def validate_artifact_hashes(root: Path) -> None:
    data = load_json(root / HASHES_REL)
    require(data["algorithm"] == "sha256", "hash algorithm")
    require(data["excluded"] == [str(HASHES_REL)], "hash exclusion")
    files = data["files"]
    require(isinstance(files, dict) and files, "hash file inventory")
    # In-repo replay: `root` is the repository, not a standalone bundle, so an
    # inventory-equality test is meaningless.  Gate every RETAINED artifact and
    # require the omissions to be exactly the declared transport-only set -- that
    # keeps full integrity coverage without re-importing PR transport files.
    missing = {rel for rel in files if not (root / rel).is_file()}
    require(
        missing <= TRANSPORT_ONLY,
        f"missing non-transport artifacts: {sorted(missing - TRANSPORT_ONLY)}",
    )
    retained = [rel for rel in files if rel not in missing]
    require(retained, "no retained artifacts to gate")
    for rel in retained:
        actual_hash = sha256_bytes((root / rel).read_bytes())
        require(actual_hash == files[rel], f"artifact hash mismatch: {rel}")


def validate_math(manifest: dict[str, Any]) -> None:
    p = EXPECTED["p"]
    n = EXPECTED["n"]
    a = EXPECTED["a"]
    k = EXPECTED["k"]
    t = n - a
    w = a - (k + 1)
    e_min = a - k + 1
    reserve = EXPECTED["reserve"]

    require(t == EXPECTED["t"], "route A t")
    require(w == EXPECTED["w"], "route A w")
    require(e_min == EXPECTED["e_min"], "route A e_min")
    sparse_shell_count = t - e_min + 1
    require(sparse_shell_count == EXPECTED["sparse_shell_count"], "route A shell count")

    # Route A: direct exact combinatorics and built-in exponentiation.
    x_a = math.comb(n, a)
    q_a = pow(p, w)

    # Route B: independent sieve/Legendre reconstruction and custom exponentiation.
    primes = sieve_primes(n)
    require(len(primes) == EXPECTED["prime_count"], "route B prime count")
    x_b, factor_count = binomial_from_primes(n, a, primes)
    require(factor_count == EXPECTED["factor_count"], "route B factor count")
    q_b = square_and_multiply(p, w)
    require(x_a == x_b, "independent X mismatch")
    require(q_a == q_b, "independent Q mismatch")

    require(x_a.bit_length() == EXPECTED["x_bits"], "X bit length")
    require(q_a.bit_length() == EXPECTED["q_bits"], "Q bit length")
    require(sha256_decimal(x_a) == EXPECTED["x_hash"], "X decimal hash")
    require(sha256_decimal(q_a) == EXPECTED["q_hash"], "Q decimal hash")
    require(sha256_decimal(x_a % q_a) == EXPECTED["rem_hash"], "remainder hash")

    floor_xq = x_a // q_a
    ceil_xq = (x_a + q_a - 1) // q_a
    floor_7xq = 7 * x_a // q_a
    floor_7xm1q = 7 * (x_a - 1) // q_a
    require(floor_xq == EXPECTED["floor_xq"], "floor X/Q")
    require(ceil_xq == EXPECTED["ceil_xq"], "ceil X/Q")
    require(floor_7xq == EXPECTED["floor_7xq"], "floor 7X/Q")
    require(floor_7xm1q == EXPECTED["floor_7xq"], "floor 7(X-1)/Q")

    sparse_cap = 3 * sparse_shell_count + floor_7xq
    uniform_cap = 1 + 3 * t + floor_7xm1q
    require(sparse_cap == EXPECTED["sparse_cap"], "sparse cap")
    require(uniform_cap == EXPECTED["uniform_cap"], "uniform cap")
    require(uniform_cap - sparse_cap == EXPECTED["pruning_dividend"], "pruning dividend")
    require(EXPECTED["paid"] + uniform_cap == EXPECTED["partial_total"], "partial total")
    require(reserve - uniform_cap == EXPECTED["remaining"], "remaining reserve")

    # Exact viable-window arithmetic.
    m = x_a - 1
    bmax_c0 = (reserve - 1) // t
    cmax_b0 = (reserve * q_a - 1) // m
    c_floor = cmax_b0 * m // q_a
    bmax_cmax = (reserve - 1 - c_floor) // t
    corner_cap = 1 + bmax_cmax * t + c_floor
    next_b_cap = 1 + (bmax_cmax + 1) * t + c_floor
    next_c_cap = 1 + (cmax_b0 + 1) * m // q_a
    require(bmax_c0 == EXPECTED["bmax_c0"], "bmax at c=0")
    require(cmax_b0 == EXPECTED["cmax_b0"], "cmax at b=0")
    require(bmax_cmax == EXPECTED["bmax_cmax"], "bmax at cmax")
    require(corner_cap == EXPECTED["corner_cap"], "corner cap")
    require(reserve - corner_cap == EXPECTED["corner_remaining"], "corner remaining")
    require(next_b_cap == EXPECTED["next_b_cap"], "next b cap")
    require(next_b_cap - reserve == EXPECTED["next_b_excess"], "next b excess")
    require(next_c_cap == EXPECTED["next_c_cap"], "next c cap")
    require(next_c_cap - reserve == EXPECTED["next_c_excess"], "next c excess")

    # Independent shell endpoint reconstruction and the exact pruning sanity gate.
    e = w + 1
    h_a = math.comb(a, e) * math.comb(t, e)
    h_b = product_binomials_from_primes(a, e, t, e, primes)
    require(h_a == h_b, "independent H_{w+1} mismatch")
    require(h_a.bit_length() == EXPECTED["h_bits"], "H bit length")
    require(sha256_decimal(h_a) == EXPECTED["h_hash"], "H decimal hash")
    margin = (a - w) * (t - w) - (w + 1) ** 2
    require(margin == EXPECTED["margin"] and margin > 0, "shell monotonicity margin")
    require(EXPECTED["cmax_b0"] * (w + 2) * h_a < q_a, "low-shell bound below Q")

    # Direct recurrence checks that the deleted low shells do not change the c=7 floor.
    h = 1
    low_sum = 1
    for shell in range(0, w + 1):
        h = h * (a - shell) * (t - shell) // ((shell + 1) ** 2)
        low_sum += h
    require(h == h_a, "shell recurrence endpoint")
    require(7 * low_sum < q_a, "c=7 low-shell mass")
    require(7 * (x_a - low_sum) // q_a == floor_7xq, "exact pruned-tail floor")

    # Field budget, independently by built-in power and repeated multiplication.
    field_a = p**EXPECTED["extension_degree"]
    field_b = 1
    for _ in range(EXPECTED["extension_degree"]):
        field_b *= p
    require(field_a == field_b, "field cardinality routes")
    require(field_a // (1 << 128) == EXPECTED["B_star"], "B_star")
    require(str(field_a) == manifest["row_contract"]["field_cardinality"], "field decimal")


def run_check(root: Path, *, with_math: bool = True, with_hashes: bool = True) -> None:
    manifest = validate_manifest(root)
    validate_frozen_row_manifest(root, manifest)
    checked, external = validate_source_pins(root, manifest)
    validate_text_contract(root)
    if with_math:
        validate_math(manifest)
    if with_hashes:
        validate_artifact_hashes(root)
    print(
        "PASS",
        json.dumps(
            {
                "packet": PACKET,
                "status": "CONDITIONAL",
                "U_Q": EXPECTED["uniform_cap"],
                "remaining_reserve": EXPECTED["remaining"],
                "source_files_checked": checked,
                "external_source_pins": external,
                "math_routes": 2 if with_math else 0,
                "hashes": with_hashes,
            },
            sort_keys=True,
        ),
    )


def rewrite_hash_for(root: Path, rel: Path) -> None:
    data = load_json(root / HASHES_REL)
    data["files"][str(rel)] = sha256_bytes((root / rel).read_bytes())
    (root / HASHES_REL).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def tamper_selftest(root: Path) -> None:
    run_check(root, with_math=True, with_hashes=True)

    # Artifact-integrity branch: mutate a retained artifact and require the
    # hash gate to reject it.  The transport-only files stay absent throughout.
    with tempfile.TemporaryDirectory(prefix="kb-uq-tamper-") as tmp:
        tmp_root = Path(tmp) / "packet"
        shutil.copytree(root, tmp_root)
        with (tmp_root / NOTE_REL).open("a", encoding="utf-8") as handle:
            handle.write("\nTAMPERED\n")
        failed = False
        try:
            validate_artifact_hashes(tmp_root)
        except VerificationError:
            failed = True
        require(failed, "artifact tamper was not detected")

    with tempfile.TemporaryDirectory(prefix="kb-uq-semantic-tamper-") as tmp:
        tmp_root = Path(tmp) / "packet"
        shutil.copytree(root, tmp_root)
        manifest = load_json(tmp_root / MANIFEST_REL)
        manifest["compiler"]["U_Q_uniform"] += 1
        (tmp_root / MANIFEST_REL).write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        failed = False
        try:
            validate_manifest(tmp_root)
        except VerificationError:
            failed = True
        require(failed, "semantic manifest tamper was not detected")
    print("PASS tamper-selftest: artifact hash and decisive integer mutations rejected")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="repository/packet root",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    try:
        if args.check:
            run_check(root)
        else:
            tamper_selftest(root)
    except VerificationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
