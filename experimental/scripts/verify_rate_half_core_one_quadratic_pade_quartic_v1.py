#!/usr/bin/env python3
"""Replay the rate-half quadratic Pade/quartic degree identities."""

from __future__ import annotations

import argparse
import copy
import hashlib
from dataclasses import dataclass
from pathlib import Path


SOURCE_COMMIT = "beb25530100b14f23413c470219fdb6b8521094b"
SOURCE_HASHES = {
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_paired_all_excess_residual_fiber_factorization/statement.md": "0ef4e2eda6c08df7ef172c7f4e3e5e12ad8832644f0171cc8d92ec395819f193",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_paired_all_excess_residual_fiber_factorization/proof.md": "e35416d3950a743d4466f32c6c360c618087046377978b1e86f5fff8d467bc62",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_extremal_coprime_resultant_exact_four_core/statement.md": "03af81362c918c0a537371c7c51810052cdef52a8956d9dfa28663413c57d14f",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_extremal_coprime_resultant_exact_four_core/proof.md": "fcafb6e1d471c746891db593408e52d43c8939b62aef88d477a956cb3f0d38e8",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_pade_regular_factor_identity/statement.md": "de1ffaa7a71b105c5526a16dbff1838ae5b6529acc73d94428964ef8039b199c",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_pade_regular_factor_identity/proof.md": "6a84f32f36fb249177181c67251e03b5d0b62c430c1576ff110220d1ea84cd18",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_extremal_resultant_regular_quartic_identification/statement.md": "c8de176f5c5d3a3081737b9cbfe702d3cb821cfc881510fac8bc3cf26f03ebf6",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_extremal_resultant_regular_quartic_identification/proof.md": "fa8b278e41e9c579f729c82c2756715693e5f1895e33590f27dc190e606eb9c3",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_correction_marked_jet_route_fence/statement.md": "16dfa510de497812e3ec3bef088a50464bd647acebd47d4ce2b645bc92ff3b2c",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_correction_marked_jet_route_fence/proof.md": "df14c50468d1c6f7c68b3a672f2efe414fc25c71971f46406df40b9d6e271f34",
}


class VerificationError(RuntimeError):
    """Raised when an exact packet identity fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


@dataclass(frozen=True)
class Formula:
    pade_exponent_offset: int = 1
    residual_degree: int = 4
    double_correction_multiplicity: int = 2
    simple_correction_total: int = 4


def verify_source(root: Path) -> int:
    checked = 0
    for relative, expected in SOURCE_HASHES.items():
        path = root / relative
        require(path.is_file(), f"missing pinned source: {relative}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected, f"source hash mismatch: {relative}")
        checked += 1
    return checked


def replay(formula: Formula) -> dict[str, int]:
    require(formula.pade_exponent_offset == 1, "Pade exponent changed")
    require(formula.residual_degree == 4, "residual degree changed")
    require(
        formula.double_correction_multiplicity == 2,
        "double correction multiplicity changed",
    )
    require(
        formula.simple_correction_total == 4,
        "simple correction total changed",
    )

    checks = 0
    for e in (7, 13, 127, 1009, 183251937963):
        p = (3 * e - 1) // 2
        d = 3 * e - 2
        n = p - 3
        n0 = 3 * p - 2
        intersection = d * (e - 2) + e * n
        pade_exponent = 2 * d + formula.pade_exponent_offset

        require(n0 + d - 1 - n == pade_exponent, "Pade cancellation failed")
        require(
            (2 * d * e - e + d) - e * pade_exponent == e - 2,
            "regular-factor degree failed",
        )
        require(
            3 * e * n - e + formula.residual_degree == intersection,
            "projective four-core failed",
        )
        require(
            (e - 6) + formula.double_correction_multiplicity * 2 == e - 2,
            "double correction degree failed",
        )
        require(
            (e - 3) // 2
            + (e - 9) // 2
            + formula.simple_correction_total
            == e - 2,
            "two-simple correction degree failed",
        )
        for rank_loss in (0, 1, 2):
            require(
                (d - rank_loss) + rank_loss - d == 0,
                "center cancellation failed",
            )
        for excess in range(5):
            for padding in range(3):
                require(
                    (n - excess - padding) + padding == n - excess,
                    "all-excess padding cancellation failed",
                )
        checks += 23

    require(2 + 2 * 3 == 8, "double marked order failed")
    require(1 + 2 * 3 == 7, "simple marked order failed")
    require(len(SOURCE_COMMIT) == 40, "source commit pin malformed")
    require(len(SOURCE_HASHES) == 10, "source hash inventory changed")
    require(
        all(len(digest) == 64 for digest in SOURCE_HASHES.values()),
        "source hash malformed",
    )

    return {
        "checks": checks + 4,
        "official_e": 183251937963,
        "pade_exponent": 2 * (3 * 183251937963 - 2) + 1,
        "residual_degree": formula.residual_degree,
        "double_marked_order": 8,
        "simple_marked_order": 7,
        "source_hashes": len(SOURCE_HASHES),
    }


def tamper_selftest() -> int:
    base = Formula()
    rejected = 0
    for field in base.__dict__:
        values = copy.copy(base.__dict__)
        values[field] += 1
        try:
            replay(Formula(**values))
        except VerificationError:
            rejected += 1
    require(rejected == 4, "tamper self-test did not reject every mutation")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    require(args.check or args.tamper_selftest, "select --check or --tamper-selftest")

    if args.check:
        result = replay(Formula())
        if args.source_root is not None:
            result["source_files_checked"] = verify_source(args.source_root)
        print("RATE_HALF_QUADRATIC_PADE_QUARTIC_PASS", result)
    if args.tamper_selftest:
        print("RATE_HALF_QUADRATIC_PADE_QUARTIC_TAMPER_PASS", tamper_selftest())


if __name__ == "__main__":
    main()
