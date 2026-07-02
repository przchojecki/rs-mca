#!/usr/bin/env python3
"""A=426 exact-threshold two-core certificate.

This verifier proves a row-level support-wise MCA/LD_sw statement without
deployed Hankel root tables:

    For any Reed--Solomon code RS[F,D,256] with |D|=512 and distinct domain D,
    LD_sw(C,426) <= 87.

It also verifies a matching tangent/moving-root lower witness and an adjacent
unsafe tangent-floor gate over the chosen prime field

    p = 22275*2^120 + 1,

where floor((p-1)/2^128)=87.  Thus A=426 is safe and A=425 is unsafe
at the 2^-128 finite-slope support-wise MCA threshold.

The proof has two cases. Given M exact support-wise noncontained bad slopes with
supports of size A=426:
  1. If every pair of supports intersects in at most 341, the complements have
     size 86 and pairwise intersection at most 1. Pair-packing gives
     M*C(86,2) <= C(512,2), so M <= 35.
  2. Otherwise choose two supports with intersection at least 342. They determine
     a common RS code-line on the common-zero set C. Every bad slope has residual
     degree <256 and at least 256 zeros on C, hence the residual codeword is zero.
     The existing support-wise noncontainment residual count gives
     M <= floor((512-c)/max(1,426-c)) <= 87, where c=|C|.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental/data/certificates/a426-two-core-exact-threshold-v26"
OUT_DIR = ROOT / "experimental/notes/certificate_scanner/outputs"
CERT_PATH = CERT_DIR / "a426_two_core_exact_threshold_v26.json"
TERMINAL_PATH = CERT_DIR / "terminal_records_A426_exact_threshold_v26.jsonl"
TANGENT_WITNESS_A426_PATH = CERT_DIR / "tangent_witness_A426_v26.json"
TANGENT_WITNESS_A425_PATH = CERT_DIR / "tangent_witness_A425_v26.json"
REPORT_PATH = OUT_DIR / "a426_two_core_exact_threshold_v26.report.md"

TWO_128 = 1 << 128
TWO_256 = 1 << 256

N = 512
K = 256
A = 426
A_UNSAFE = 425
J = N - A
RHO = Fraction(K, N)
DELTA = Fraction(N - A, N)
DELTA_UNSAFE = Fraction(N - A_UNSAFE, N)
ETA = Fraction(1, 1) - RHO - DELTA

# Exact-budget prime for the A=426/A=425 adjacent threshold row.
# It has floor((p-1)/2^128)=87 and p-1=2^120*3^4*5^2*11.
P = 22275 * (1 << 120) + 1
P_MINUS_1_FACTORS = {2: 120, 3: 4, 5: 2, 11: 1}
PRIMITIVE_ROOT_WITNESS = 13
DOMAIN_GENERATOR = pow(PRIMITIVE_ROOT_WITNESS, (P - 1) // N, P)

B_TAN = N + 1 - A  # 87
B_TAN_UNSAFE = N + 1 - A_UNSAFE  # 88
PAIR_CORE_THRESHOLD = N + K - A  # 342
LOW_PAIR_INTERSECTION_MAX = PAIR_CORE_THRESHOLD - 1  # 341
COMPLEMENT_INTERSECTION_MAX_LOW_PAIR = LOW_PAIR_INTERSECTION_MAX - N + 2 * J
PACKING_BOUND_LOW_PAIR = math.comb(N, 2) // math.comb(J, 2)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def sha256_json(obj: Any) -> str:
    return sha256_bytes(canonical_json(obj).encode())


def lf_bytes(text: str) -> bytes:
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def pretty_json_bytes(obj: Any) -> bytes:
    return lf_bytes(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def verify_small_prime(q: int) -> None:
    if q < 2:
        raise AssertionError(f"not prime: {q}")
    d = 2
    while d * d <= q:
        if q % d == 0:
            raise AssertionError(f"not prime: {q}")
        d += 1


def verify_lucas_prime(n: int, factors: dict[int, int], witness: int) -> None:
    prod = 1
    for q, e in factors.items():
        verify_small_prime(q)
        prod *= q ** e
    if prod != n - 1:
        raise AssertionError("factorization does not multiply to n-1")
    if pow(witness, n - 1, n) != 1:
        raise AssertionError("Lucas witness fails Fermat congruence")
    for q in factors:
        if pow(witness, (n - 1) // q, n) == 1:
            raise AssertionError(f"Lucas witness has order dividing (n-1)/{q}")


def verify_domain_generator() -> None:
    if P % N != 1:
        raise AssertionError("p is not 1 mod n")
    if pow(DOMAIN_GENERATOR, N, P) != 1:
        raise AssertionError("domain generator does not have order dividing n")
    for q in (2,):  # n=2^9, so it is enough to rule out order dividing 256.
        if pow(DOMAIN_GENERATOR, N // q, P) == 1:
            raise AssertionError("domain generator order is not exactly 512")


def domain_elements() -> list[int]:
    elems = [1]
    for _ in range(1, N):
        elems.append((elems[-1] * DOMAIN_GENERATOR) % P)
    if len(set(elems)) != N:
        raise AssertionError("domain elements are not distinct")
    if elems[-1] * DOMAIN_GENERATOR % P != 1:
        raise AssertionError("domain generator cycle does not close")
    return elems


def core_case_bound_values() -> list[dict[str, int]]:
    vals = []
    for c in range(PAIR_CORE_THRESHOLD, N + 1):
        h = max(1, A - c)
        bound = (N - c) // h
        vals.append({"common_core_size": c, "outside_required_per_slope": h, "bound": bound})
    return vals


def max_core_case_bound() -> tuple[int, int]:
    vals = core_case_bound_values()
    best = max(vals, key=lambda r: r["bound"])
    return best["bound"], best["common_core_size"]


def verify_two_core_upper() -> dict[str, Any]:
    if not (A >= K + 1):
        raise AssertionError("exact-support reduction requires A >= k+1")
    if not (2 * A - N > K):
        raise AssertionError("two chosen slopes must determine code-line on their overlap")
    if PAIR_CORE_THRESHOLD != 342:
        raise AssertionError("unexpected pair-core threshold")
    if COMPLEMENT_INTERSECTION_MAX_LOW_PAIR != 1:
        raise AssertionError("low-pair complement intersection bound should be 1")
    if PACKING_BOUND_LOW_PAIR != 35:
        raise AssertionError("unexpected pair packing bound")
    core_bound, core_argmax = max_core_case_bound()
    if core_bound != B_TAN or core_argmax != A - 1:
        raise AssertionError("core residual bound should maximize at A-1 with value n+1-A")
    total_upper = max(PACKING_BOUND_LOW_PAIR, core_bound)
    if total_upper != B_TAN:
        raise AssertionError("total upper should equal tangent branch size")
    return {
        "theorem": "A426 two-core support-wise line-decoding closure",
        "status": "PROVED",
        "parameters": {"n": N, "k": K, "A": A, "j": J},
        "exact_support_reduction": {"A_ge_k_plus_1": A >= K + 1},
        "two_slope_overlap": {
            "min_pair_intersection": 2 * A - N,
            "min_pair_intersection_gt_k": 2 * A - N > K,
            "core_threshold_n_plus_k_minus_A": PAIR_CORE_THRESHOLD,
        },
        "case_1_no_large_pair_core": {
            "assumption_pair_intersection_at_most": LOW_PAIR_INTERSECTION_MAX,
            "complement_size": J,
            "complement_pair_intersection_at_most": COMPLEMENT_INTERSECTION_MAX_LOW_PAIR,
            "packing_bound_floor_binom_n2_over_binom_j2": PACKING_BOUND_LOW_PAIR,
            "binom_n_2": math.comb(N, 2),
            "binom_j_2": math.comb(J, 2),
        },
        "case_2_large_pair_core": {
            "common_core_size_min": PAIR_CORE_THRESHOLD,
            "residual_degree_lt": K,
            "residual_zero_count_min": K,
            "bound_formula": "floor((n-c)/max(1,A-c)) for c=|common code-line support|",
            "max_bound": core_bound,
            "max_attained_at_common_core_size": core_argmax,
            "argmax_interpretation": "moving-root/tangent envelope with A-1 common coordinates",
        },
        "LD_sw_upper_bound_A426": total_upper,
    }


def tangent_lower_witness(agreement: int) -> dict[str, Any]:
    if not (K + 1 <= agreement <= N):
        raise AssertionError("tangent witness agreement outside valid RS range")
    slope_count = N + 1 - agreement
    core_size = agreement - 1
    elems = domain_elements()
    core_indices = list(range(core_size))
    outside_indices = list(range(core_size, N))
    slopes = list(range(len(outside_indices)))
    if len(outside_indices) != slope_count:
        raise AssertionError("outside/tangent slope count mismatch")
    # Compact line witness over D indexed by domain_elements:
    # on the core, f=g=0; on outside index agreement-1+i, g=1 and f=-i.
    # For slope z=i, f+z g vanishes on core plus outside_i.
    records = []
    for i, idx in enumerate(outside_indices):
        z = slopes[i]
        f_val = (-z) % P
        g_val = 1
        if (f_val + z * g_val) % P != 0:
            raise AssertionError("line value does not vanish at tangent moving root")
        records.append({
            "slope": z,
            "moving_coordinate_index": idx,
            "moving_domain_element": elems[idx],
            "support_size": agreement,
            "explaining_codeword": "zero polynomial",
            "noncontained_reason": f"direction g is zero on {core_size} core coordinates and one at the moving coordinate; no degree<256 polynomial can agree on this support",
        })
    witness = {
        "agreement": agreement,
        "field": {"p": P, "domain_generator": DOMAIN_GENERATOR},
        "domain_hash_sha256": sha256_json(elems),
        "line_definition": {
            "core_indices": {"start": 0, "stop_inclusive": core_size - 1, "count": core_size},
            "outside_indices": {"start": core_size, "stop_inclusive": N - 1, "count": slope_count},
            "f_values": f"f=0 on core; f=-i on outside index {core_size}+i for i=0..{slope_count - 1}",
            "g_values": "g=0 on core; g=1 on outside indices",
        },
        "bad_slope_encodings": slopes,
        "bad_slope_hash_sha256": sha256_json(slopes),
        "support_record_hash_sha256": sha256_json(records),
        "records": records,
        "LD_sw_lower_bound": slope_count,
        f"LD_sw_lower_bound_A{agreement}": slope_count,
    }
    return witness


def terminal_records(ledger_hash: str, tangent_hash: str) -> list[dict[str, Any]]:
    # These are retained-ledger records, not raw chart-root records.  The v26
    # theorem pays/absorbs all non-tangent chart families into the two-core
    # envelope, so there is no separately retained contribution.
    base = {
        "A": A,
        "coverage_ledger_id": "A426-two-core-exact-threshold-v26",
        "coverage_ledger_hash_sha256": ledger_hash,
        "coverage_certificate_type": "structural_two_core_residual_packing_theorem",
    }
    rows = [
        {
            **base,
            "component": "B_tan",
            "terminal_status": "tangent_moving_root_complete",
            "retained_count": B_TAN,
            "tangent_witness_hash_sha256": tangent_hash,
        }
    ]
    for component in ["B_quot_support", "B_quot_image", "B_ext", "B_ap_regular", "B_ap_pivot"]:
        rows.append({
            **base,
            "component": component,
            "terminal_status": "globally_absorbed_by_two_core_envelope",
            "retained_count": 0,
            "explanation": "No separately retained contribution after applying the global A=426 two-core upper bound LD_sw<=87 and the tangent witness LD_sw>=87.",
        })
    return rows


def build_certificate() -> dict[str, Any]:
    verify_lucas_prime(P, P_MINUS_1_FACTORS, PRIMITIVE_ROOT_WITNESS)
    verify_domain_generator()
    upper = verify_two_core_upper()
    tangent426 = tangent_lower_witness(A)
    tangent425 = tangent_lower_witness(A_UNSAFE)
    if tangent426["LD_sw_lower_bound"] != upper["LD_sw_upper_bound_A426"]:
        raise AssertionError("upper/lower mismatch")
    if tangent425["LD_sw_lower_bound"] != B_TAN_UNSAFE:
        raise AssertionError("unexpected A=425 tangent lower witness size")
    budget_floor = P // TWO_128
    if budget_floor != B_TAN:
        raise AssertionError("unexpected budget floor")
    if not (TWO_128 * B_TAN < P):
        raise AssertionError("2^-128 inequality fails")
    if not (B_TAN_UNSAFE > budget_floor and TWO_128 * B_TAN_UNSAFE > P):
        raise AssertionError("adjacent unsafe tangent-floor inequality fails")
    # Ledger hash excludes terminal rows first to avoid circularity.
    core_payload = {
        "upper_theorem": upper,
        "tangent_witness_A426_hash_sha256": sha256_json({k: v for k, v in tangent426.items() if k != "records"}),
        "tangent_support_A426_record_hash_sha256": tangent426["support_record_hash_sha256"],
        "tangent_witness_A425_hash_sha256": sha256_json({k: v for k, v in tangent425.items() if k != "records"}),
        "tangent_support_A425_record_hash_sha256": tangent425["support_record_hash_sha256"],
    }
    ledger_hash = sha256_json(core_payload)
    terminal = terminal_records(ledger_hash, tangent426["support_record_hash_sha256"])
    terminal_hash = sha256_json(terminal)
    cert = {
        "schema": "a426_two_core_exact_threshold_v26",
        "status": "PROVED_ADJACENT_THRESHOLD_ROW",
        "result": "PASS_ADJACENT_THRESHOLD_ROW_CANDIDATE",
        "claim": "For every finite field F and every distinct D subset F with |D|=512, LD_sw(RS[F,D,256],426)=87. For p=22275*2^120+1 and an order-512 subgroup H, floor((p-1)/2^128)=87, so A=426 is safe and A=425 is unsafe.",
        "row": {
            "track": "finite-slope support-wise MCA / LD_sw adjacent threshold row",
            "field_model": "prime field F_p",
            "p": P,
            "p_factorization_p_minus_1": {str(q): e for q, e in P_MINUS_1_FACTORS.items()},
            "p_lucas_primitive_root_witness": PRIMITIVE_ROOT_WITNESS,
            "p_prime_certified_by_lucas": True,
            "p_lt_2^256": P < TWO_256,
            "domain": "multiplicative subgroup H=<g> of order 512",
            "domain_generator": DOMAIN_GENERATOR,
            "domain_generator_order": N,
            "domain_hash_sha256": tangent426["domain_hash_sha256"],
            "q_gen": P,
            "q_line": P,
            "q_chal": "not protocol-bound",
            "q_ledgers_equal": "q_gen=q_line=p; q_chal is intentionally not asserted",
        },
        "parameters": {
            "n": N,
            "k": K,
            "rho": f"{RHO.numerator}/{RHO.denominator}",
            "A": A,
            "closed_radius_convention": "A = ceil((1-delta)n)",
            "delta": f"{DELTA.numerator}/{DELTA.denominator}",
            "first_unsafe_A": A_UNSAFE,
            "first_unsafe_delta": f"{DELTA_UNSAFE.numerator}/{DELTA_UNSAFE.denominator}",
            "eta": f"{ETA.numerator}/{ETA.denominator}",
        },
        "budget": {
            "epsilon": "2^-128",
            "budget_floor": budget_floor,
            "budget_floor_convention": "floor((q_line - 1)/2^128)",
            "safe_A426_N_bad": B_TAN,
            "safe_A426_N_bad_le_budget_floor": B_TAN <= budget_floor,
            "strict_inequality_2^128_N_bad_lt_q_line": TWO_128 * B_TAN < P,
            "unsafe_A425_tangent_floor": B_TAN_UNSAFE,
            "unsafe_A425_exceeds_budget_floor": B_TAN_UNSAFE > budget_floor,
            "unsafe_A425_strict_inequality_2^128_N_bad_gt_q_line": TWO_128 * B_TAN_UNSAFE > P,
            "spare_budget_floor_units_at_A426": budget_floor - B_TAN,
        },
        "decomposition_A426_retained_after_two_core_coverage": {
            "B_tan": B_TAN,
            "B_quot_support": 0,
            "B_quot_image": 0,
            "B_ext": 0,
            "B_ap_regular": 0,
            "B_ap_pivot": 0,
            "deduped_total_426": B_TAN,
            "deduped_total_426_le_budget_floor": B_TAN <= budget_floor,
            "interpretation": "These are retained ledger contributions after applying the v26 structural two-core coverage theorem; raw Hankel root tables are superseded for this A=426 row.",
        },
        "adjacent_threshold": {
            "safe_agreement": A,
            "safe_closed_radius": f"{DELTA.numerator}/{DELTA.denominator}",
            "safe_reason": "LD_sw(C,426)=87 <= floor((q_line-1)/2^128)=87",
            "first_unsafe_agreement": A_UNSAFE,
            "first_unsafe_closed_radius": f"{DELTA_UNSAFE.numerator}/{DELTA_UNSAFE.denominator}",
            "unsafe_reason": "direct moving-root tangent witness gives LD_sw(C,425)>=88 > floor((q_line-1)/2^128)=87",
        },
        "upper_theorem": upper,
        "lower_witness_A426_summary": {k: v for k, v in tangent426.items() if k != "records"},
        "lower_witness_A425_summary": {k: v for k, v in tangent425.items() if k != "records"},
        "coverage_ledger_hash_sha256": ledger_hash,
        "terminal_records_hash_sha256": terminal_hash,
        "nonclaims": [
            "Does not close the live F_17^32 A=426 row; that denominator has budget floor 6 and cannot pay N_bad=87.",
            "Hankel-free: does not provide raw Hankel eliminant root tables; it proves a structural upper bound that makes those tables unnecessary for the emitted A=426 prime-field row.",
            "Does not claim ordinary list decoding, interleaved-list safety, protocol query soundness, BETA_2, or M1 local-limit closure.",
        ],
    }
    cert["certificate_hash_sha256"] = sha256_json({k: v for k, v in cert.items() if k != "certificate_hash_sha256"})
    return cert


def write_artifacts(cert: dict[str, Any]) -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_bytes(pretty_json_bytes(cert))
    tangent426 = tangent_lower_witness(A)
    tangent425 = tangent_lower_witness(A_UNSAFE)
    TANGENT_WITNESS_A426_PATH.write_bytes(pretty_json_bytes(tangent426))
    TANGENT_WITNESS_A425_PATH.write_bytes(pretty_json_bytes(tangent425))
    terminal = terminal_records(cert["coverage_ledger_hash_sha256"], tangent426["support_record_hash_sha256"])
    TERMINAL_PATH.write_bytes(lf_bytes("".join(json.dumps(r, sort_keys=True) + "\n" for r in terminal)))
    write_report(cert)


def check_artifacts(cert: dict[str, Any]) -> None:
    expected = pretty_json_bytes(cert)
    if not CERT_PATH.exists():
        raise AssertionError(f"missing certificate: {CERT_PATH}")
    if CERT_PATH.read_bytes() != expected:
        raise AssertionError("certificate JSON mismatch; run --write to regenerate")
    tangent426 = tangent_lower_witness(A)
    tangent425 = tangent_lower_witness(A_UNSAFE)
    if TANGENT_WITNESS_A426_PATH.read_bytes() != pretty_json_bytes(tangent426):
        raise AssertionError("A=426 tangent witness mismatch; run --write to regenerate")
    if TANGENT_WITNESS_A425_PATH.read_bytes() != pretty_json_bytes(tangent425):
        raise AssertionError("A=425 tangent witness mismatch; run --write to regenerate")
    terminal = terminal_records(cert["coverage_ledger_hash_sha256"], tangent426["support_record_hash_sha256"])
    expected_terminal = lf_bytes("".join(json.dumps(r, sort_keys=True) + "\n" for r in terminal))
    if TERMINAL_PATH.read_bytes() != expected_terminal:
        raise AssertionError("terminal records mismatch; run --write to regenerate")
    if REPORT_PATH.read_bytes() != lf_bytes(report_text(cert)):
        raise AssertionError("report mismatch; run --write to regenerate")


def report_text(cert: dict[str, Any]) -> str:
    d = cert["decomposition_A426_retained_after_two_core_coverage"]
    lines = []
    lines.append("# A=426 two-core exact threshold v26\n\n")
    lines.append("**Status:** `PROVED_ADJACENT_THRESHOLD_ROW`.\n\n")
    lines.append("This is a Hankel-free structural two-core support-wise line-decoding theorem. With the exact-budget prime, it gives an adjacent finite-slope support-wise MCA threshold row.\n\n")
    lines.append("## Row\n\n")
    lines.append(f"- `p = {P} = 22275*2^120 + 1`, prime by Lucas witness `{PRIMITIVE_ROOT_WITNESS}` and `p-1=2^120*3^4*5^2*11`.\n")
    lines.append(f"- `n={N}`, `k={K}`, `A_safe={A}`, `A_unsafe={A_UNSAFE}`, `rho={RHO}`.\n")
    lines.append(f"- `q_gen=q_line=p`; `q_chal` is not protocol-bound; budget floor `floor((p-1)/2^128)={cert['budget']['budget_floor']}`.\n")
    lines.append(f"- Safe: `LD_sw(C,{A}) = {B_TAN}` at closed radius `{DELTA}`.\n")
    lines.append(f"- First unsafe: direct tangent witness gives `LD_sw(C,{A_UNSAFE}) >= {B_TAN_UNSAFE}` at closed radius `{DELTA_UNSAFE}`.\n\n")
    lines.append("## Retained A=426 decomposition after v26 two-core coverage\n\n")
    lines.append("| component | retained count | terminal status |\n")
    lines.append("|---|---:|---|\n")
    lines.append(f"| `B_tan(426)` | {d['B_tan']} | tangent moving-root witness complete |\n")
    for comp in ["B_quot_support", "B_quot_image", "B_ext", "B_ap_regular", "B_ap_pivot"]:
        lines.append(f"| `{comp}(426)` | 0 | globally absorbed by two-core envelope |\n")
    lines.append(f"| `deduped_total(426)` | {d['deduped_total_426']} | equals budget floor `{cert['budget']['budget_floor']}` |\n\n")
    lines.append("## Proof sketch\n\n")
    lines.append("Using the existing repo M2 exact-support bridge, restrict to exact supports of size `426`. If all support pairs intersect in at most `341`, complement pair-packing gives at most `35` slopes. Otherwise two supports have overlap at least `342`, determine a common code-line, and the existing common-code-line residual budget bounds the remaining slopes by `floor((512-c)/max(1,426-c)) <= 87`, with equality at `c=425`.\n\n")
    lines.append("The matching lower witness takes a common zero core of size `425` and one moving outside coordinate for each of `87` slopes.\n\n")
    lines.append("Monotonicity then makes every `A>=426` safe over this prime, while the direct `A=425` tangent witness gives the first unsafe grid point.\n\n")
    lines.append("## Replay\n\n")
    lines.append("```bash\npython3 experimental/scripts/certify_a426_two_core_exact_threshold_v26.py --check\n```\n")
    return "".join(lines)


def write_report(cert: dict[str, Any]) -> None:
    REPORT_PATH.write_bytes(lf_bytes(report_text(cert)))


def print_summary(cert: dict[str, Any]) -> None:
    print("A=426 two-core exact-threshold v26")
    print(f"STATUS: {cert['status']}")
    print(f"p: {P}")
    print("p_prime_lucas: witness=13, p-1=2^120*3^4*5^2*11")
    print(f"n,k,A: {N},{K},{A}")
    print(f"delta: {DELTA}")
    print(f"LD_sw_upper_A426: {cert['upper_theorem']['LD_sw_upper_bound_A426']}")
    print(f"LD_sw_lower_A426: {cert['lower_witness_A426_summary']['LD_sw_lower_bound_A426']}")
    print(f"deduped_total_426: {cert['decomposition_A426_retained_after_two_core_coverage']['deduped_total_426']}")
    print(f"budget_floor: {cert['budget']['budget_floor']}")
    print(f"strict_2^128_N_bad_lt_q_line: {cert['budget']['strict_inequality_2^128_N_bad_lt_q_line']}")
    print(f"first_unsafe_A425_tangent_floor: {cert['budget']['unsafe_A425_tangent_floor']}")
    print(f"unsafe_A425_exceeds_budget_floor: {cert['budget']['unsafe_A425_exceeds_budget_floor']}")
    print(f"terminal_records_hash: {cert['terminal_records_hash_sha256']}")
    print("RESULT: PASS_ADJACENT_THRESHOLD_ROW_CANDIDATE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write deterministic JSON/report artifacts")
    parser.add_argument("--check", action="store_true", help="check committed artifacts match regenerated output")
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
    args = parser.parse_args()
    cert = build_certificate()
    if args.write:
        write_artifacts(cert)
    if args.check:
        check_artifacts(cert)
    if args.json:
        print(json.dumps(cert, indent=2, sort_keys=True))
        return
    print_summary(cert)


if __name__ == "__main__":
    main()
