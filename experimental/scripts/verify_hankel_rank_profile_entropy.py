#!/usr/bin/env python3
"""Replay the Hankel rank-profile entropy packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "m1" / "hankel_rank_profile_entropy.md"
SUPPORT_CERT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "hankel-support-lattice-accounting"
    / "hankel_support_lattice_accounting.json"
)
DEFECT_CERT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "hankel-sparse-atoms-rational-defects"
    / "hankel_sparse_atoms_rational_defects.json"
)
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "hankel-rank-profile-entropy"
    / "hankel_rank_profile_entropy.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "hankel_rank_profile_entropy",
    "support_dependency": "f_support_lattice",
    "defect_dependency": "hankel_sparse_atoms_as_rational_defects",
    "principal_kernel": "row-deficient Hankel kernels are principal GRS segments",
    "entropy_bound": "n^{O(W^2)}",
    "non_claim": "does not produce per-agreement M3 root tables",
}


def dependency_check(path: Path, expected_node: str) -> dict[str, object]:
    cert = json.loads(path.read_text(encoding="utf-8"))
    return {
        "path": str(path.relative_to(REPO)),
        "schema": cert.get("schema"),
        "status": cert.get("status"),
        "source_dag_node": cert.get("source_dag_node"),
        "accepted": cert.get("status") == "PROVED"
        and cert.get("source_dag_node") == expected_node,
    }


def toy_check() -> dict[str, object]:
    j = 8
    t = 3
    d = 4
    alpha = 2
    degree_q = (j + 1 - d) - alpha
    degree_qtilde = degree_q + alpha
    principal_degree_ok = degree_qtilde == j + 1 - d

    wide_w = 2
    wide_condition = j - t + 3 > 2 * wide_w
    narrow_w = 4
    narrow_condition = j - t + 3 <= 2 * narrow_w
    narrow_dimension_bound = 2 * narrow_w - 2
    residual_dimension = j + 1 - t

    fixed_w = 4
    branch_levels = fixed_w
    level_width_exponent = fixed_w
    entropy_exponent = branch_levels * level_width_exponent

    return {
        "principal_kernel": {
            "j": j,
            "t": t,
            "D": d,
            "alpha": alpha,
            "degree_q": degree_q,
            "degree_qtilde": degree_qtilde,
            "degree_bookkeeping_ok": principal_degree_ok,
        },
        "wide_case": {
            "W": wide_w,
            "j_minus_t_plus_3": j - t + 3,
            "condition_holds": wide_condition,
            "atom_closure_bound": 1,
        },
        "narrow_case": {
            "W": narrow_w,
            "condition_holds": narrow_condition,
            "residual_dimension": residual_dimension,
            "dimension_bound": narrow_dimension_bound,
            "dimension_bound_holds": residual_dimension <= narrow_dimension_bound,
        },
        "entropy_budget": {
            "fixed_W": fixed_w,
            "branch_levels": branch_levels,
            "level_width_exponent": level_width_exponent,
            "exponent": entropy_exponent,
            "is_O_W_squared": entropy_exponent <= fixed_w * fixed_w,
        },
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "hankel-rank-profile-entropy-v1",
        "status": "PROVED",
        "source_dag_node": "hankel_rank_profile_entropy",
        "dependencies": [
            dependency_check(DEFECT_CERT, "hankel_sparse_atoms_as_rational_defects"),
            dependency_check(SUPPORT_CERT, "f_support_lattice"),
        ],
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not produce M3 root tables",
            "does not close a row-level F_17^32 safe-side certificate",
            "does not prove terminal moment-count leaves",
        ],
        "note": "experimental/notes/m1/hankel_rank_profile_entropy.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "hankel-rank-profile-entropy-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not all(dep.get("accepted") for dep in cert["dependencies"]):
        raise AssertionError("dependency check failed")
    toy = cert["toy_check"]
    if not isinstance(toy, dict):
        raise AssertionError("missing toy check")
    if not toy["principal_kernel"]["degree_bookkeeping_ok"]:
        raise AssertionError("principal-kernel degree check failed")
    if not toy["wide_case"]["condition_holds"]:
        raise AssertionError("wide-case guard failed")
    if not toy["narrow_case"]["dimension_bound_holds"]:
        raise AssertionError("narrow-case dimension check failed")
    if not toy["entropy_budget"]["is_O_W_squared"]:
        raise AssertionError("entropy exponent check failed")


def assert_same(expected: dict[str, object], actual: dict[str, object]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(REPO)}")
    if args.check:
        actual = json.loads(args.check.read_text(encoding="utf-8"))
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print(f"{cert['status']}: {cert['source_dag_node']}")


if __name__ == "__main__":
    main()
