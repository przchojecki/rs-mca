#!/usr/bin/env python3
"""Replay the rate-half core-one quadratic pair-floor arithmetic."""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass


SOURCE_COMMIT = "04179c43ac45b7c53a03d2441487971da72f3069"
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
}


class VerificationError(RuntimeError):
    """Raised when an exact profile identity fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


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

    official_N = 1 << 41
    official_rho = official_N // 4
    official_e = (official_rho + 1) // 3
    require(official_rho == 549755813888, "official rho mismatch")
    require(official_e == 183251937963, "official e mismatch")
    require(3 * official_e - 1 == official_rho, "official divisibility failed")
    require(2 * official_e - 9 == 366503875917, "official gap mismatch")

    require(len(SOURCE_COMMIT) == 40, "source commit pin malformed")
    require(len(SOURCE_HASHES) == 4, "source hash inventory changed")
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
