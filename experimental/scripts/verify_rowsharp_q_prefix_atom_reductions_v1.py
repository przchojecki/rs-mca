#!/usr/bin/env python3
"""Verify the row-sharp Q-prefix atom reduction packet.

This verifier records the useful proved reductions around the KB-MCA
``A=1116048`` primitive Q-fin wall.  It deliberately does not claim the
row-sharp Q-prefix atom theorem is proved: the missing input is still a
support-level primitive full-rank signed-defect / generated-prefix
multiplicity certificate.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "rowsharp-q-prefix-atom-reductions-v1"
CERT_PATH = CERT_DIR / "rowsharp_q_prefix_atom_reductions_v1.json"
CERT_README_PATH = CERT_DIR / "README.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "rowsharp_q_prefix_atom_reductions_v1.report.md"
)
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "rowsharp_q_prefix_atom_reductions_v1.md"


P = 2**31 - 2**24 + 1
N = 2**21
K = 2**20
A = 1_116_048
J = N - A
T = A - K
W = T - 1
Q_LINE = P**6
B_STAR = (Q_LINE - 1) // 2**128
B_GEN = T * P
B_REM_AFTER_GEN = B_STAR - B_GEN
K_REM_EXPECTED = 4_805_007
K_RAW_EXPECTED = 4_807_520
RETAINED_EXACT_LIFT_BOUND = math.comb(16, 7)


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def log2_int(x: int) -> float:
    """Stable approximate log2 for large positive integers."""
    ensure(x > 0, "log2_int expects a positive integer")
    bits = x.bit_length()
    if bits <= 1024:
        return math.log2(x)
    shift = bits - 1024
    top = x >> shift
    return math.log2(top) + shift


def json_bytes(cert: dict[str, Any]) -> bytes:
    return (json.dumps(cert, indent=2, sort_keys=True) + "\n").encode("utf-8")


def provenance_block() -> list[dict[str, Any]]:
    return [
        {
            "name": "KB adjacent row constants and generated image-cell ledger",
            "source_path": "experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md",
            "source_pr_or_commit": "local main / prior KB-MCA 1116048 partial ledger packet",
            "status": "IMPORTED_PROVED_INPUT_WITH_CONDITIONAL_LEDGER_SCOPE",
            "consumed_statement": "p,n,k,agreement,j,t,w,B*,K_raw,K_rem and B_gen<=t*p image-cell arithmetic.",
        },
        {
            "name": "Exact-lift terminal-16 retained fiber bound",
            "source_path": "experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md",
            "source_pr_or_commit": "local main / prior KB-MCA 1116048 partial ledger packet",
            "status": "IMPORTED_PROVED_INPUT",
            "consumed_statement": "A retained exact lifted prefix class has size at most binom(16,7)=11440.",
        },
        {
            "name": "Q-fin / Route gamma strategy context",
            "source_path": "experimental/cap25_v13_missing_inputs_strategy.md",
            "source_pr_or_commit": "local main strategy note",
            "status": "STRATEGY_CONTEXT_NOT_CONSUMED_AS_PAYMENT",
            "consumed_statement": "Q-fin needs near-lossless recursion; Route gamma/folding defects are the aligned route.",
        },
        {
            "name": "Top-seam marked-incidence guardrail",
            "source_path": "experimental/notes/thresholds/rowsharp_q_prefix_atom_reductions_v1.md",
            "source_pr_or_commit": "this packet; conceptually adjacent to open PR #389",
            "status": "PROVED_LOCAL_LEMMA_DOES_NOT_SUPERSEDE_PR_389",
            "consumed_statement": "At e=w+1, coprime side locators U,V satisfy U-V=constant; common core G remains marked.",
        },
        {
            "name": "Composite-prefix gcd(e,N) descent context",
            "source_path": "experimental/notes/thresholds/rowsharp_q_prefix_atom_routes_v1.md",
            "source_pr_or_commit": "this packet; conceptually adjacent to open PR #394",
            "status": "EXPERIMENTAL_REGRESSION_NOT_CONSUMED_AS_PAYMENT",
            "consumed_statement": "Small-model regressions support c=gcd(e,N) quotient factorization.",
        },
        {
            "name": "BC-to-Q and shift-pair route context",
            "source_path": "experimental/notes/thresholds/rowsharp_q_prefix_atom_routes_v1.md",
            "source_pr_or_commit": "this packet; conceptually adjacent to open PRs #393/#395/#396",
            "status": "EXPERIMENTAL_CONTEXT_NOT_CONSUMED_AS_PAYMENT",
            "consumed_statement": "Toy chart decompositions motivate multiplicity accounting; no BC/SP upper payment is imported here.",
        },
    ]


def rim_counterexample() -> dict[str, Any]:
    """A small roots-of-unity RIM specialization singularity guardrail."""
    p = 17
    omega = 2
    domain = [pow(omega, i, p) for i in range(8)]

    def eval_poly(coeffs: tuple[int, ...], x: int) -> int:
        acc = 0
        power = 1
        for c in coeffs:
            acc = (acc + c * power) % p
            power = (power * x) % p
        return acc

    # u=(X-1)(X-2)=2+14X+X^2, v=3(X^2+1)=3+0X+3X^2.
    u = (2, 14, 1)
    v = (3, 0, 3)
    edges = {
        "13": [1, 2],
        "23": [4, 13],
        "12": [8, 16],
    }
    checks = {
        "u_zero_on_13": [eval_poly(u, x) == 0 for x in edges["13"]],
        "v_zero_on_23": [eval_poly(v, x) == 0 for x in edges["23"]],
        "u_minus_v_zero_on_12": [(eval_poly(u, x) - eval_poly(v, x)) % p == 0 for x in edges["12"]],
    }

    rows = [
        [1, 1, 1, 0, 0, 0],
        [1, 2, 4, 0, 0, 0],
        [0, 0, 0, 1, 4, 16],
        [0, 0, 0, 1, 13, 16],
        [1, 8, 13, -1, -8, -13],
        [1, 16, 1, -1, -16, -1],
    ]
    rows = [[x % p for x in row] for row in rows]
    kernel_vec = [2, 14, 1, 3, 0, 3]
    products = [sum(a * b for a, b in zip(row, kernel_vec)) % p for row in rows]

    # For k=3 and three vertices, k-weak partition connectivity inequalities.
    partition_crossing_weights = {
        "{1}|{2}|{3}": 6,
        "{1}|{2,3}": 4,
        "{2}|{1,3}": 4,
        "{3}|{1,2}": 4,
    }
    weak_partition_connected = (
        partition_crossing_weights["{1}|{2}|{3}"] >= 3 * (3 - 1)
        and partition_crossing_weights["{1}|{2,3}"] >= 3
        and partition_crossing_weights["{2}|{1,3}"] >= 3
        and partition_crossing_weights["{3}|{1,2}"] >= 3
    )

    ensure(all(all(vs) for vs in checks.values()), "RIM polynomial agreement checks failed")
    ensure(all(x == 0 for x in products), "RIM kernel vector check failed")
    ensure(weak_partition_connected, "RIM weak partition connectivity check failed")

    return {
        "status": "COUNTEREXAMPLE_TO_NAIVE_FIXED_SUBGROUP_RIM_NONSINGULARITY",
        "field": "F_17",
        "omega": omega,
        "domain_mu_8": domain,
        "dimension_k": 3,
        "edges": edges,
        "u_coefficients_constant_to_quadratic": list(u),
        "v_coefficients_constant_to_quadratic": list(v),
        "agreement_checks": checks,
        "rim_matrix_rows_mod_17": rows,
        "kernel_vector": kernel_vec,
        "matrix_times_kernel": products,
        "weak_partition_connected": weak_partition_connected,
        "meaning": (
            "Symbolic RIM full rank does not imply full rank after a fixed roots-of-unity "
            "specialization; a deterministic rank-drop/pivot first-match branch is necessary."
        ),
    }


def build_cert() -> dict[str, Any]:
    c = math.comb(N, J)
    p_to_w = pow(P, W)
    k_raw = (B_STAR * p_to_w) // c
    k_rem = (B_REM_AFTER_GEN * p_to_w) // c
    target_floor = (K_REM_EXPECTED * c) // p_to_w
    avg_floor = c // p_to_w
    paid_plus_retained = B_GEN + RETAINED_EXACT_LIFT_BOUND
    integer_slack = target_floor - paid_plus_retained

    ensure(k_raw == K_RAW_EXPECTED, "unexpected raw multiplier")
    ensure(k_rem == K_REM_EXPECTED, "unexpected remaining multiplier")
    ensure(RETAINED_EXACT_LIFT_BOUND == 11_440, "unexpected exact-lift retained bound")
    ensure(integer_slack > 0, "conditional closure inequality failed")
    ensure(W < P, "Newton identities are not invertible through depth w")

    odd_equations = (W + 1) // 2
    small_defect_lower_bound = odd_equations + 1
    one_sided_collision_distance = W + 1
    top_seam_degree_bound = one_sided_collision_distance - W - 1
    ensure(top_seam_degree_bound == 0, "top-seam constant-difference check failed")

    cert: dict[str, Any] = {
        "status": "REDUCED_NOT_PROVED",
        "claim_class": "ROW_SHARP_Q_PREFIX_ATOM_REDUCTION_PACKET",
        "not_a_safe_side_certificate": True,
        "does_not_prove": [
            "U(1116048) <= B*",
            "the KoalaBear MCA first-safe agreement",
            "row-sharp Q-prefix atom theorem",
            "primitive full-rank signed-defect support bound",
            "generated-prefix support payment",
        ],
        "row_packet": {
            "field": "KoalaBear sextic line field",
            "p": P,
            "n": N,
            "k": K,
            "agreement_a": A,
            "j": J,
            "t": T,
            "w": W,
            "q_line": Q_LINE,
            "B_star": B_STAR,
            "B_gen_image_cell_bound": B_GEN,
            "B_rem_after_generated_image_cells": B_REM_AFTER_GEN,
            "K_raw": k_raw,
            "K_rem": k_rem,
            "safe_certificate_status": "NOT_PROVED_BY_THIS_PACKET",
        },
        "target": {
            "statement": "max primitive Q-fin fiber <= 4805007 * binom(n,j) / p^w",
            "integer_form": "|R_prim(z)| * p^67471 <= 4805007 * binom(2097152,981104)",
            "target_floor": target_floor,
            "avg_floor": avg_floor,
            "avg_log2_approx": round(log2_int(c) - W * math.log2(P), 9),
        },
        "provenance": provenance_block(),
        "proved_reductions": {
            "newton_power_sum_equivalence": {
                "status": "PROVED",
                "condition": "w < p",
                "w": W,
                "p": P,
                "meaning": "Locator-prefix equality is triangularly equivalent to equality of the first w power sums.",
            },
            "q1_collision_distance": {
                "status": "PROVED",
                "one_sided_difference_at_least": one_sided_collision_distance,
                "symmetric_difference_at_least": 2 * one_sided_collision_distance,
                "proof_key": "deg(Lambda_S-Lambda_T)<=j-w-1 and Lambda_S-Lambda_T=G(U-V)",
            },
            "top_seam_constant_difference": {
                "status": "PROVED",
                "minimal_one_sided_difference": one_sided_collision_distance,
                "degree_bound_for_side_difference": top_seam_degree_bound,
                "conclusion": "At e=w+1, the coprime side locators U and V satisfy U-V=constant.",
                "guardrail": "The common core G must remain marked; unmarked side pairs can have many cores.",
            },
            "exact_lift_terminal_16_bound": {
                "status": "IMPORTED_PROVED_INPUT_FROM_KB_LEDGER",
                "retained_exact_lift_bound": RETAINED_EXACT_LIFT_BOUND,
                "reason": "w>=2^16 forces exact-lift mask divisibility by (X^n-1)/(X^16-1).",
            },
            "folding_identities": {
                "status": "PROVED",
                "even_power_sum": "P_{2a}(S)=sum_y u_y y^a",
                "odd_power_sum": "P_{2a+1}(S)=sum_y sigma_y x y^a",
            },
            "small_signed_defect_impossibility": {
                "status": "PROVED",
                "odd_equations": odd_equations,
                "nonzero_signed_defect_support_at_least": small_defect_lower_bound,
                "proof_key": "Vandermonde full column rank on any support of size <= number of odd equations.",
            },
            "rs_list_equivalence": {
                "status": "PROVED_REFORMULATION",
                "support_side_dimension": J - W,
                "complement_side_dimension": K + 1,
                "support_side_statement": (
                    "A prefix fiber is the list of h in F_p[X]_<913633 agreeing with "
                    "-F_z on at least 981104 points of D."
                ),
                "complement_side_statement": (
                    "Equivalently, after passing to D\\S, it is an RS_D(k+1) list "
                    "at agreement a=k+t."
                ),
            },
            "raw_constant_list_import_obstruction": {
                "status": "PROVED_BY_AVERAGE",
                "avg_floor": avg_floor,
                "meaning": "The raw prefix map has average fiber about 2^35.735, so no constant-list RS theorem can apply to raw fibers.",
            },
        },
        "rim_guardrail": rim_counterexample(),
        "conditional_closure": {
            "status": "PROVED_IF_SUPPORT_CERTIFICATE_SUPPLIED",
            "missing_support_certificate": "|G_gen_support(z)| + |D_full_rank_prim(z)| <= t*p",
            "t_times_p": B_GEN,
            "retained_exact_lift_bound": RETAINED_EXACT_LIFT_BOUND,
            "paid_plus_retained": paid_plus_retained,
            "target_floor": target_floor,
            "integer_slack": integer_slack,
            "slack_bits_approx": round(log2_int(target_floor) - math.log2(paid_plus_retained), 9),
        },
        "missing_certificate": {
            "name": "Primitive fixed-subgroup Boolean-coset / Route D support certificate",
            "sufficient_bound": B_GEN,
            "equivalent_forms": [
                "support-level primitive full-rank signed-defect theorem",
                "generated-prefix support multiplicity theorem",
                "deterministic fixed-subgroup RIM nonvanishing after first-match branch deletion",
                "marked-incidence injection into {0,...,67471} x F_p",
                "primitive Fourier phase-spread coefficient bound",
            ],
        },
        "supporting_experimental_packet": {
            "script": "experimental/scripts/experiment_rowsharp_q_prefix_atom_routes_v1.py",
            "json": "experimental/data/certificates/rowsharp-q-prefix-atom-routes-v1/rowsharp_q_prefix_atom_routes_v1.json",
            "report": "experimental/notes/thresholds/rowsharp_q_prefix_atom_routes_v1.md",
            "status": "EXPERIMENTAL_EVIDENCE_NOT_A_PROOF",
        },
    }
    return cert


def expected_payload_values() -> dict[str, int]:
    c = math.comb(N, J)
    p_to_w = pow(P, W)
    return {
        "target_floor": (K_REM_EXPECTED * c) // p_to_w,
        "avg_floor": c // p_to_w,
    }


def validate_cert_payload(cert: dict[str, Any], expected: dict[str, int] | None = None) -> None:
    if expected is None:
        expected = expected_payload_values()
    row = cert["row_packet"]
    target = cert["target"]
    closure = cert["conditional_closure"]
    reductions = cert["proved_reductions"]
    rim = cert["rim_guardrail"]
    expected_target_floor = expected["target_floor"]
    expected_avg_floor = expected["avg_floor"]

    ensure(row["p"] == P, "payload p mismatch")
    ensure(row["n"] == N, "payload n mismatch")
    ensure(row["k"] == K, "payload k mismatch")
    ensure(row["agreement_a"] == A, "payload agreement mismatch")
    ensure(row["B_gen_image_cell_bound"] == B_GEN, "payload B_gen mismatch")
    ensure(row["B_star"] == B_STAR, "payload B_star mismatch")
    ensure(row["K_raw"] == K_RAW_EXPECTED, "payload K_raw mismatch")
    ensure(row["K_rem"] == K_REM_EXPECTED, "payload K_rem mismatch")
    ensure(target["target_floor"] == expected_target_floor, "payload target_floor mismatch")
    ensure(target["avg_floor"] == expected_avg_floor, "payload avg_floor mismatch")
    ensure(
        reductions["exact_lift_terminal_16_bound"]["retained_exact_lift_bound"] == RETAINED_EXACT_LIFT_BOUND,
        "payload retained exact-lift bound mismatch",
    )
    ensure(
        reductions["top_seam_constant_difference"]["degree_bound_for_side_difference"] == 0,
        "payload top-seam degree bound mismatch",
    )
    ensure(
        reductions["small_signed_defect_impossibility"]["nonzero_signed_defect_support_at_least"] == 33_737,
        "payload small signed-defect lower bound mismatch",
    )
    ensure(closure["target_floor"] == expected_target_floor, "payload closure target mismatch")
    ensure(closure["t_times_p"] == B_GEN, "payload closure t*p mismatch")
    ensure(closure["retained_exact_lift_bound"] == RETAINED_EXACT_LIFT_BOUND, "payload closure retained mismatch")
    ensure(closure["integer_slack"] == expected_target_floor - closure["paid_plus_retained"], "payload integer slack mismatch")
    ensure(closure["integer_slack"] > 0, "payload conditional closure failed")

    matrix = rim["rim_matrix_rows_mod_17"]
    kernel = rim["kernel_vector"]
    products = [sum(a * b for a, b in zip(row, kernel)) % 17 for row in matrix]
    ensure(products == rim["matrix_times_kernel"], "payload RIM matrix/kernel mismatch")
    ensure(all(x == 0 for x in products), "payload RIM guardrail no longer singular")
    ensure(rim["weak_partition_connected"] is True, "payload RIM weak connectivity mismatch")


def tamper_selftest() -> None:
    base = build_cert()
    expected = expected_payload_values()
    validate_cert_payload(base, expected)

    mutations: list[tuple[str, Any]] = [
        ("K_rem", lambda c: c["row_packet"].__setitem__("K_rem", c["row_packet"]["K_rem"] + 1)),
        ("K_raw", lambda c: c["row_packet"].__setitem__("K_raw", c["row_packet"]["K_raw"] - 1)),
        ("B_gen", lambda c: c["row_packet"].__setitem__("B_gen_image_cell_bound", c["row_packet"]["B_gen_image_cell_bound"] + 1)),
        (
            "retained_exact_lift",
            lambda c: c["proved_reductions"]["exact_lift_terminal_16_bound"].__setitem__("retained_exact_lift_bound", 11_439),
        ),
        ("target_floor", lambda c: c["target"].__setitem__("target_floor", c["target"]["target_floor"] + 1)),
        (
            "RIM_kernel",
            lambda c: c["rim_guardrail"]["kernel_vector"].__setitem__(0, (c["rim_guardrail"]["kernel_vector"][0] + 1) % 17),
        ),
        (
            "RIM_matrix",
            lambda c: c["rim_guardrail"]["rim_matrix_rows_mod_17"][0].__setitem__(0, 2),
        ),
        (
            "top_seam_degree_bound",
            lambda c: c["proved_reductions"]["top_seam_constant_difference"].__setitem__("degree_bound_for_side_difference", 1),
        ),
    ]
    for name, mutate in mutations:
        bad = json.loads(json.dumps(base))
        mutate(bad)
        try:
            validate_cert_payload(bad, expected)
        except AssertionError:
            continue
        raise AssertionError(f"tamper self-test failed to detect mutation: {name}")
    print(f"tamper self-test passed: {len(mutations)} mutations detected")


def render_note(cert: dict[str, Any]) -> str:
    target = cert["target"]
    cc = cert["conditional_closure"]
    row = cert["row_packet"]
    text = f"""# Row-sharp Q prefix atom reductions v1

Status: `REDUCED_NOT_PROVED`.

This packet does not prove `U(1116048) <= B*`, does not certify the
KoalaBear MCA first-safe agreement, and does not prove the row-sharp Q-prefix
atom theorem.  It records the useful reductions from the failed proof attempts,
the exact conditional closure arithmetic, and the precise support certificate
that remains missing.

## Why this matters

This is not a closing theorem, but it is a high-value reduction packet for the
current row-sharp Q wall:

- it turns the KB-MCA `a=1116048` primitive target into a replayable
  support-certificate problem with exact constants;
- it proves the reusable structural lemmas needed by later attempts:
  Newton/power-sum equivalence, Q1 split distance, top-seam marked incidence,
  RS/list reformulations, dyadic folding identities, small signed-defect
  impossibility, and the fixed-subgroup RIM rank-drop guardrail;
- it records the exact conditional closure margin: a support-level Route D
  certificate bounded by `t*p` would imply the row-sharp atom inequality with
  about `10.9006675` bits of slack after the retained exact-lift `11440` term;
- it rules out several tempting but invalid shortcuts, including raw
  constant-list RS capacity import, generated-prefix image-cell support
  payment, zero-defect-only folding descent, and naive fixed-subgroup RIM
  nonsingularity.

## Deployed row

```text
p = {row['p']}
n = {row['n']}
k = {row['k']}
a = {row['agreement_a']}
j = {row['j']}
t = {row['t']}
w = {row['w']}
B* = {row['B_star']}
K_raw = {row['K_raw']}
K_rem = {row['K_rem']}
```

The remaining primitive target is

```text
max_z |R_prim(z)| <= 4805007 * binom(2097152,981104) / p^67471.
```

In integer form:

```text
|R_prim(z)| * p^67471 <= 4805007 * binom(2097152,981104).
```

The target floor is

```text
floor(4805007 * binom(2097152,981104) / p^67471)
  = {target['target_floor']}.
```

The raw average fiber floor is

```text
floor(binomial(n,j) / p^w) = {target['avg_floor']},
```

so a constant-list theorem cannot apply to the raw prefix map.

## Proved reductions

### Newton / power-sum equivalence

Since `w < p`, Newton identities are triangular and invertible through depth
`w`.  Equality of the first `w` locator coefficients is equivalent to equality
of the first `w` power sums.

### Q1 collision distance

If two distinct supports have the same first `w` prefixes, write

```text
Lambda_S = G U,
Lambda_T = G V,
deg U = deg V = e.
```

Then

```text
deg(Lambda_S - Lambda_T) <= j-w-1,
Lambda_S - Lambda_T = G(U-V),
deg G = j-e.
```

Thus

```text
e >= w+1 = {cert['proved_reductions']['q1_collision_distance']['one_sided_difference_at_least']}.
```

### Top-seam marked incidence

The same degree bound gives

```text
deg(U-V) <= e-w-1.
```

At the minimal seam `e=w+1`, this becomes

```text
deg(U-V) <= 0,
```

so

```text
U-V = constant.
```

The common core `G` must remain marked; unmarked side-pair counting can have
many common cores and is not a valid replacement.

### Exact-lift terminal-16 retained class

The imported exact-lift Q2 input gives a retained exact-lift class bound

```text
|E_ret(z)| <= binom(16,7) = {cc['retained_exact_lift_bound']}.
```

### Folding identities

For an antipodal pair `{{x,-x}}` with `y=x^2`, define

```text
u_y     = 1_S(x) + 1_S(-x),
sigma_y = 1_S(x) - 1_S(-x).
```

Then

```text
P_{{2a}}(S)   = sum_y u_y y^a,
P_{{2a+1}}(S) = sum_y sigma_y x y^a.
```

There are `{cert['proved_reductions']['small_signed_defect_impossibility']['odd_equations']}` odd equations, so a nonzero homogeneous signed defect
satisfying all of them has support at least

```text
{cert['proved_reductions']['small_signed_defect_impossibility']['nonzero_signed_defect_support_at_least']}.
```

This excludes small signed defects only; it does not pay large full-rank
signed defects.

### RS/list reformulations

On the support-locator side, the prefix fiber is exactly the list of
polynomials

```text
h in F_p[X]_<913633
```

that agree with the received word `-F_z` on at least `981104` points of `D`.
On the complementary MCA side it is an `RS_D(k+1)` list at agreement
`a=k+t`.  These are exact reformulations, not imported capacity theorems.

## Provenance

This packet consumes or references the following local sources and open-PR
context.  Experimental sources listed here are not imported as payments.

"""
    for source in cert["provenance"]:
        text += (
            f"- `{source['name']}`: `{source['status']}` from "
            f"`{source['source_path']}` ({source['source_pr_or_commit']}). "
            f"{source['consumed_statement']}\n"
        )
    text += f"""

## RIM guardrail

The packet includes a small `F_17`, `mu_8`, `k=3` counterexample to the naive
claim that symbolic RIM full rank always survives roots-of-unity
specialization.  Therefore the correct deterministic RIM result is a
first-match routing theorem: if the canonical pivot minor vanishes after
specialization, the packet must enter a rank-drop/pivot branch.  Surviving
packets have full specialized rank by definition of that branch.

This does not pay the rank-drop/pivot branch.

## Conditional closure

If the missing support certificate proves

```text
|G_gen_support(z)| + |D_full_rank_prim(z)| <= t*p
```

for every primitive finite prefix target `z`, then

```text
t*p = {cc['t_times_p']},
|E_ret(z)| <= {cc['retained_exact_lift_bound']},
t*p + |E_ret(z)| = {cc['paid_plus_retained']}.
```

Since

```text
{cc['paid_plus_retained']} < {cc['target_floor']},
```

the row-sharp Q-prefix atom inequality follows with integer slack

```text
{cc['integer_slack']}
```

and about `{cc['slack_bits_approx']}` bits of slack.

## Missing theorem

The remaining theorem is a support-level primitive fixed-subgroup certificate:

```text
For every primitive finite prefix target z, after first-match deletion of
generated_field, quotient_planted, sparse_pade_hankel, m1_window_shadow,
rank_drop_pivot, bc_chart, sp_shift_pair, and extension_slope branches,
the remaining generated-prefix / primitive full-rank signed-defect support
mass is at most t*p = 143763024447376.
```

Equivalent forms include deterministic fixed-subgroup RIM nonvanishing after
branch deletion, marked-incidence injection into `{{0,...,67471}} x F_p`, and a
primitive Fourier phase-spread coefficient bound.

## Related experiment packet

The companion evidence packet is:

```text
experimental/scripts/experiment_rowsharp_q_prefix_atom_routes_v1.py
experimental/data/certificates/rowsharp-q-prefix-atom-routes-v1/rowsharp_q_prefix_atom_routes_v1.json
experimental/notes/thresholds/rowsharp_q_prefix_atom_routes_v1.md
```

It is experimental evidence only.  It supports Route D and marked incidence,
while showing that generated-prefix image labels and zero-defect descent do
not pay support multiplicity.
"""
    return text


def render_cert_readme(cert: dict[str, Any]) -> str:
    return f"""# rowsharp-q-prefix-atom-reductions-v1

Status: `{cert['status']}`.

This certificate records the proved reductions and exact conditional arithmetic
around the KB-MCA `a=1116048` row-sharp Q-prefix atom wall.  It does not prove
the row safe and does not prove the primitive Q-fin theorem.

Contribution summary:

- packages the row-sharp Q wall as a precise support-certificate target;
- proves and verifies the main structural reductions needed by Route D;
- records the exact conditional closure slack if the missing support payment is
  supplied;
- includes provenance and tamper gates so later packets can safely consume the
  constants and nonclaims.

Replay:

```bash
python3 experimental/scripts/verify_rowsharp_q_prefix_atom_reductions_v1.py --check
```
"""


def render_report(cert: dict[str, Any]) -> str:
    row = cert["row_packet"]
    cc = cert["conditional_closure"]
    return f"""# rowsharp_q_prefix_atom_reductions_v1 report

Status: `{cert['status']}`.

## Row constants

- `p = {row['p']}`
- `n = {row['n']}`
- `j = {row['j']}`
- `w = {row['w']}`
- `K_rem = {row['K_rem']}`

## Verified reductions

- Newton/power-sum equivalence: `{cert['proved_reductions']['newton_power_sum_equivalence']['status']}`
- Q1 one-sided collision distance: `{cert['proved_reductions']['q1_collision_distance']['one_sided_difference_at_least']}`
- top-seam `U-V=constant`: `{cert['proved_reductions']['top_seam_constant_difference']['status']}`
- retained exact-lift bound: `{cc['retained_exact_lift_bound']}`
- small signed-defect support lower bound: `{cert['proved_reductions']['small_signed_defect_impossibility']['nonzero_signed_defect_support_at_least']}`

## Conditional closure

```text
t*p + 11440 = {cc['paid_plus_retained']}
target floor = {cc['target_floor']}
integer slack = {cc['integer_slack']}
slack bits ~= {cc['slack_bits_approx']}
```

## Missing input

`{cert['missing_certificate']['name']}` with bound
`<= {cert['missing_certificate']['sufficient_bound']}`.
"""


def bytes_map(cert: dict[str, Any]) -> dict[Path, bytes]:
    return {
        CERT_PATH: json_bytes(cert),
        CERT_README_PATH: (render_cert_readme(cert)).encode("utf-8"),
        REPORT_PATH: (render_report(cert)).encode("utf-8"),
        NOTE_PATH: (render_note(cert)).encode("utf-8"),
    }


def write_artifacts(cert: dict[str, Any]) -> None:
    for path, data in bytes_map(cert).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(f"wrote {path}")


def check_artifacts(cert: dict[str, Any]) -> None:
    validate_cert_payload(cert)
    expected = bytes_map(cert)
    for path, data in expected.items():
        ensure(path.exists(), f"missing artifact: {path}")
        actual = path.read_bytes()
        ensure(actual == data, f"artifact mismatch: {path}")
    print(f"artifact check passed: {len(expected)} files")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write deterministic artifacts")
    parser.add_argument("--check", action="store_true", help="check deterministic artifacts")
    parser.add_argument("--tamper-selftest", action="store_true", help="run mutation checks for critical certificate fields")
    parser.add_argument("--json", action="store_true", help="print the certificate JSON")
    args = parser.parse_args()

    if args.tamper_selftest:
        tamper_selftest()
        return

    cert = build_cert()
    validate_cert_payload(cert)

    if args.write:
        write_artifacts(cert)
    if args.check:
        check_artifacts(cert)
    if args.json:
        print(json.dumps(cert, indent=2, sort_keys=True))
    if not (args.write or args.check or args.json):
        print(f"STATUS: {cert['status']}")
        print("RESULT: PASS")


if __name__ == "__main__":
    main()
