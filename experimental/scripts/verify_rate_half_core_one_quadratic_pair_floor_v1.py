#!/usr/bin/env python3
"""Replay the rate-half core-one quadratic pair-floor arithmetic."""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass


SOURCE_COMMIT = "cd318d6155d9f96ff986926dfec5a0b58f54a408"
SOURCE_HASHES = {
    "localization_statement": (
        "fafe03c21890127aeef952a4e6282da6319f20a6c224d80338ce8e8529be22c8"
    ),
    "localization_proof": (
        "0e471cfc4abbf4d825cc73c4a3271b03c7b69ac197fbce8c1996cd078c9b719b"
    ),
    "exclusion_statement": (
        "09a93f1e8a2fdc283fc424b21217323d5ec8ce6c0e429086f62c1d3f50e1edcd"
    ),
    "exclusion_proof": (
        "a916c434e1ab321f9f731e5a62c70b670bb02964fcae4448a34f008333ac1742"
    ),
    "macroscopic_statement": (
        "e1aea2dd47ced41f1b2be847846147d8df54730752232c5325d5dd62fbbeafcf"
    ),
    "macroscopic_proof": (
        "ceaa9fae989d4b54652937993ab60aa61aa8dffb5078b3ca7acfb69e242b3954"
    ),
    "source_partition_statement": (
        "fd23ed6e8d238cd56b2f553857e64e1c902b9c6f66a2a7b5541acb88568ae637"
    ),
    "source_partition_proof": (
        "4f0db5ad2e68d2e2028dd91ec6e03e077543d31b53f1c3d70e6b25cd0196e932"
    ),
    "forney_gate_statement": (
        "a8be024011bda2fcbecac762324b0ac86b5090ab876dd267f4a187ae9d2785b7"
    ),
    "forney_gate_proof": (
        "a3a42cd173eaa41e66a4362fe9a46764610964b874384173c8081f3080a9da0d"
    ),
    "dual_biform_statement": (
        "bfc301188ff4d08086fcbd9acceedb6f886b26f1f0fcb337c0e2cfff3d0e3b05"
    ),
    "dual_biform_proof": (
        "03cbd1b1dfc702bb79b9974a76104bceba00758595bb78af706fa75b1261a857"
    ),
    "strict_minword_statement": (
        "80ad5e3e4817fa0508a7ec738c285edff38925a349e2592edcb87a71e9381798"
    ),
    "strict_minword_proof": (
        "b301134e650c60337bca20586540de9dd3bf76d8a3bce6632b2cbcad621f8d27"
    ),
    "strict_biform_statement": (
        "61c0bd1bd1f75493d8a872c9aefabd73c45b1ca5ba361d23fa73ed0737560022"
    ),
    "strict_biform_proof": (
        "518be4020bb33547e5530df6877e69b36b06f64b76ec3f1772b6f2edbe74368b"
    ),
    "coefficient_gate_statement": (
        "6116d6040d5e45691046001fc0929d5a6924c2f088c84c7e3cf6173d34f77289"
    ),
    "coefficient_gate_proof": (
        "16efedbadab999696cc438e07de4da83c51a2311a1c664805ea45cbbfe1d3433"
    ),
    "coefficient_gate_probe": (
        "508d0d0bcc0888c4170a121f458ac2c0618b32cdcf99b88b0ad78586ef8a43e9"
    ),
    "padded_fiber_statement": (
        "ac80fea6eddd99a7733f72a4743aa0a982a34ba0ce15043975848f31239dff84"
    ),
    "padded_fiber_proof": (
        "6a2ab5b579dccecb018b5bb3ab35ce31690745014a4a75a1a4f2e422f988e437"
    ),
    "parameter_gate_statement": (
        "c1261184526f38bc36dbad4706f1ba4ffbe1e2276190702b0c80bbd45378690b"
    ),
    "parameter_gate_proof": (
        "3539a0b726e761836e9224132b6503e96ed99e3058eab44d7c92e9461cd1353a"
    ),
}


class VerificationError(RuntimeError):
    """Raised when an exact profile identity fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def obstruction(e: int, j: int) -> int:
    return (
        3 * e * e * j
        - 9 * e * e
        - 2 * e * j * j
        + 5 * e * j
        + 6 * e
        - 2 * j * j
        - 2 * j
    )


@dataclass(frozen=True)
class Formula:
    rho_multiplier: int = 3
    rho_offset: int = -1
    supported_offset: int = 4
    packet_deficit_offset: int = 6
    line_charge: int = 4


def replay(formula: Formula) -> dict[str, int]:
    require(formula.rho_multiplier == 3, "rho multiplier changed")
    require(formula.rho_offset == -1, "rho offset changed")
    require(formula.supported_offset == 4, "supported-slope offset changed")
    require(
        formula.packet_deficit_offset == 6,
        "packet deficit offset changed",
    )
    require(formula.line_charge == 4, "line charge changed")

    for e in (7, 13, 127, 1009, 183251937963):
        rho = formula.rho_multiplier * e + formula.rho_offset
        T = rho + formula.supported_offset
        require(T == 3 * e + 3, "supported-slope total mismatch")

        for R in range(5):
            common_light = rho - R - 4
            difference_rows = R + 6
            require(
                common_light + difference_rows == rho + 2,
                "endpoint-union partition mismatch",
            )

            for q in range(2, min(e, 32) + 1):
                g = e - q
                slack = (R + 5) * g - (R + 3) * e + 2
                demand_gap = common_light * (q - 1) - slack
                require(
                    demand_gap == e * (3 * q - 5) + R + 3,
                    "pre-maximal gcd gap identity failed",
                )
                require(demand_gap > 0, "pre-maximal gcd branch survived")

            g = e - 1
            slack = (R + 5) * g - (R + 3) * e + 2
            require(slack == 2 * e - R - 3, "maximal-gcd slack mismatch")
            for d_line in (0, 1):
                missing_common = 3 * e - R - 6 + d_line
                positive_slack = e - formula.packet_deficit_offset - d_line
                zero_slack = slack - positive_slack
                require(
                    zero_slack == e - R + 3 + d_line,
                    "zero-deficit slack mismatch",
                )
                require(
                    missing_common - zero_slack == 2 * e - 9,
                    "terminal contradiction gap mismatch",
                )
                require(
                    missing_common > zero_slack,
                    "rho+3 profile was not excluded",
                )

        for endpoint_deficit in range(5):
            expansion = T - ((rho + 4 - endpoint_deficit) // 4)
            closed = ceil_div(3 * rho + 12 + endpoint_deficit, 4)
            require(expansion == closed, "expansion ceiling identity failed")

        j0 = rho // 2 - 1
        require(j0 == (3 * e - 3) // 2, "macroscopic floor mismatch")
        require(
            obstruction(e, 4) == 3 * e * e - 6 * e - 40 > 0,
            "left obstruction endpoint failed",
        )
        require(
            obstruction(e, j0 - 1) == (3 * e * e - 14 * e - 15) // 2 > 0,
            "right obstruction endpoint failed",
        )
        if e <= 1009:
            require(
                all(obstruction(e, j) > 0 for j in range(4, j0)),
                "interior concavity replay failed",
            )
        require((rho + j0 - 1) // j0 == 3, "three-center cap failed")
        require(4 * j0 > rho + j0 - 1, "four-center exclusion failed")

        p = rho // 2
        require(2 * e <= 3 * e, "zero-excess count exceeded off-line slopes")
        require(e + 6 <= 2 * e, "clean split-fiber lower bound failed")
        require(3 * p - 3 == (9 * e - 9) // 2, "split-row floor mismatch")
        require(p - 3 == (3 * e - 7) // 2, "domain biform degree mismatch")

        off_line_strict = 3 * e + 1
        strict_excess = p
        strict_zero = off_line_strict - strict_excess
        require(strict_zero == p + 2, "strict zero-excess count mismatch")
        for line_deficit in range(min(e - 6, 4) + 1):
            off_deficit = e - 6 - line_deficit
            strict_clean = strict_zero - off_deficit
            require(
                strict_clean == (e + 15) // 2 + line_deficit,
                "strict clean-fiber count mismatch",
            )
            strict_columns = 2 * p + line_deficit
            strict_checks = strict_columns - ((p - 2) + 1)
            require(
                strict_checks == p + 1 + line_deficit,
                "strict coefficient-MDS check count mismatch",
            )

        for line_deficit in (0, 1):
            ext_columns = 3 * p - 3 + line_deficit
            ext_checks = ext_columns - ((p - 3) + 1)
            require(
                ext_checks == 2 * p - 1 + line_deficit,
                "extremal coefficient-MDS check count mismatch",
            )

        ext_parameter_columns = 2 * e
        ext_parameter_checks = ext_parameter_columns - ((e - 2) + 1)
        require(
            ext_parameter_checks == e + 1,
            "extremal parameter-fiber check count mismatch",
        )
        require(
            (p - 2) * ext_parameter_checks
            == (p - 2) * (e + 1),
            "extremal parameter-fiber matrix rows mismatch",
        )

        strict_parameter_columns = p + 2
        strict_parameter_checks = strict_parameter_columns - ((e - 1) + 1)
        require(
            strict_parameter_checks == p + 2 - e,
            "strict parameter-fiber check count mismatch",
        )
        require(
            (p - 1) * strict_parameter_checks
            == (p - 1) * (p + 2 - e),
            "strict parameter-fiber matrix rows mismatch",
        )

    official_N = 1 << 41
    official_rho = official_N // 4
    official_e = (official_rho + 1) // 3
    require(official_rho == 549755813888, "official rho mismatch")
    require(official_e == 183251937963, "official e mismatch")
    require(3 * official_e - 1 == official_rho, "official divisibility failed")
    require(2 * official_e - 9 == 366503875917, "official gap mismatch")

    require(len(SOURCE_COMMIT) == 40, "source commit pin malformed")
    require(len(SOURCE_HASHES) == 23, "source hash inventory changed")
    require(
        all(len(value) == 64 for value in SOURCE_HASHES.values()),
        "source hash malformed",
    )
    return {
        "N": official_N,
        "rho": official_rho,
        "e": official_e,
        "T": official_rho + 4,
        "terminal_gap": 2 * official_e - 9,
        "pair_union_floor": 3 * official_rho // 2 - 1,
        "center_line_max": 3,
        "expanding_thirds": official_rho + 1,
        "zero_excess_slopes": 2 * official_e,
        "clean_split_fibers": official_e + 6,
        "split_rows": 3 * (official_rho // 2) - 3,
        "biform_parameter_degree": official_e - 2,
        "biform_domain_degree": official_rho // 2 - 3,
        "strict_zero_excess_slopes": official_rho // 2 + 2,
        "strict_clean_split_fibers": (official_e + 15) // 2,
        "strict_split_rows": official_rho,
        "strict_biform_parameter_degree": official_e - 1,
        "strict_biform_domain_degree": official_rho // 2 - 2,
        "extremal_coefficient_matrix_rows": (
            (official_e - 1) * (official_rho - 1)
        ),
        "strict_coefficient_matrix_rows": (
            official_e * (official_rho // 2 + 1)
        ),
        "extremal_parameter_matrix_rows": (
            (official_rho // 2 - 2) * (official_e + 1)
        ),
        "extremal_parameter_matrix_columns": 2 * official_e,
        "strict_parameter_matrix_rows": (
            (official_rho // 2 - 1)
            * (official_rho // 2 + 2 - official_e)
        ),
        "strict_parameter_matrix_columns": official_rho // 2 + 2,
    }


def tamper_selftest() -> int:
    base = Formula()
    rejected = 0
    for field in (
        "rho_multiplier",
        "rho_offset",
        "supported_offset",
        "packet_deficit_offset",
        "line_charge",
    ):
        values = copy.copy(base.__dict__)
        values[field] += 1
        try:
            replay(Formula(**values))
        except VerificationError:
            rejected += 1
    require(rejected == 5, "tamper self-test did not reject every mutation")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    require(args.check or args.tamper_selftest, "select --check or --tamper-selftest")

    if args.check:
        result = replay(Formula())
        print("RATE_HALF_CORE_ONE_QUADRATIC_PAIR_FLOOR_PASS", result)
    if args.tamper_selftest:
        print("RATE_HALF_CORE_ONE_QUADRATIC_PAIR_FLOOR_TAMPER_PASS", tamper_selftest())


if __name__ == "__main__":
    main()
