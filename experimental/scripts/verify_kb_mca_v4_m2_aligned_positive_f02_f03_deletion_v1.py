#!/usr/bin/env python3
"""Fail-closed verifier for the exact aligned-positive F02/F03 deletion.

The Sage compiler performs the load-bearing algebra.  This Python verifier
independently binds its sources, validates the exhaustive branch/point
certificate, checks every stored nonzero norm and literal-transport record,
and runs semantic mutation tests.  It intentionally uses ``require`` rather
than Python ``assert`` so ``python -O`` cannot disable a check.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "data/certificates/"
    "kb-mca-v4-m2-aligned-positive-f02-f03-deletion-v1/"
    "kb_mca_v4_m2_aligned_positive_f02_f03_deletion_v1.json"
)
COMPILER = (
    ROOT
    / "scripts/"
    "compile_kb_mca_v4_m2_aligned_positive_f02_f03_deletion_v1.sage"
)
ATLAS_COMPILER = (
    ROOT
    / "scripts/compile_kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.sage"
)
ATLAS_CERTIFICATE = (
    ROOT
    / "data/certificates/kb-mca-v4-m2-aligned-positive-qslice-atlas-v1"
    / "kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.json"
)

SCHEMA = "kb-mca-v4-m2-aligned-positive-f02-f03-deletion-v1"
PRIME = 2130706433
COMPILER_SHA256 = (
    "e65439765b029443f8f309da74e4195ba7cd96db9f1d0c89145d3582e3d04061"
)
ATLAS_COMPILER_SHA256 = (
    "c382adee5be3b72dcb675b4932a681f65ae958f58e24c3f5fdb8163d4d1508b7"
)
ATLAS_COMPILER_BLOB = "946308dbc014ce952c0c1cc583cc3d579a61aecf"
ATLAS_CERTIFICATE_SHA256 = (
    "91b3df40ec8721b2e95ef8170ff58cb0a68a4ef17be0f8c7dbe9f6a0291c8ac4"
)
ATLAS_CERTIFICATE_BLOB = "017bc1447f6114ae91182560ad0c7ca708919b6b"
ATLAS_PAYLOAD = (
    "127a4574077d213b188c9e8a9fde93a5a1a4b6121e9f37f84fc01f66c313d990"
)
EXPECTED_PAYLOAD = (
    "51572f4d190a3bceb31494ae7ee48f6b026346413ae398d2da4f7b1da1402438"
)
EXPECTED_LOCALIZER_FACTORS = [
    "2*b - 1",
    "2*c - 1",
    "2*d - 1",
    "2*w - 1",
    "4*c*d*w - c*d - 2*c*w - 2*d*w + 2*c + 2*d + w - 4",
    "5*c*d - 4*c - 4*d + 5",
    "b",
    "b + 1",
    "b - 1",
    "b - 2",
    "b - c",
    "b - d",
    "b - w",
    "b*c - 1",
    "b*d - 1",
    "b*w - 1",
    "c",
    "c + 1",
    "c - 1",
    "c - 2",
    "c - d",
    "c - w",
    "c*d - 1",
    "c*w - 1",
    "d",
    "d + 1",
    "d - 1",
    "d - 2",
    "d - w",
    "d*w - 1",
    "w",
    "w + 1",
    "w - 1",
    "w - 2",
]
EXPECTED_FACTOR_HASHES = {
    "F02-R02": {
        "c_constant": [
            "6487d12fbfc00b7544e53d11f779ce3a7f1b79c13ade210eac801791fb2d6fec",
            "94431ebab5b5b7bfd716d4e0aa979fac66ed82c8c460fa114e055e5cd97a6382",
        ],
        "d_constant": [
            "732b0dbe4af1f439da74223bb233b495f708fbc8f7248ea6eeaad0b35b497189",
            "31712bb6b3aec9b79ef350922ade01f95f5158ddf9cc332bb3d96c4106263d45",
        ],
    },
    "F02-R11": {
        "c_constant": [
            "1de6e2699de59b642e44d00a81a1f122360b48702193bf78b86c0cb2b9d5a5bf",
        ],
        "d_constant": [
            "38ff5656e2ff6fc3b2788618b501a4bef37e45230064ad0a337574e2443852d2",
        ],
    },
    "F02-R20": {
        "c_constant": [
            "d8d960cecb0c9da47f87606ee1c9e87f97b0f60ce4472a92d0a12d489dc88e3e",
            "716c2b0d3648d895929962d432de5de5c8230ad1d31a6e05317879d3f4d195de",
        ],
        "d_constant": [
            "6c0568b42b56834467a4b476fb38490dc52fea6cd2292f06f9ff76fbd42f9f77",
            "f91f47efcdd9cf39c85923d75550ed09137b9f557a4e9b185ae47cc9d8fa9f85",
        ],
    },
}
UNIT_BASIS_SHA256 = (
    "43de3a417d75f4818c5a553268b80ce3a5805109a3bbc6b605e9fb0b8f50b485"
)
EXPECTED_NONUNIT_BASIS_SHA256 = {
    "F02-R02": "17cc25e32b90ec69e80451e92ccc83fa1dc573b10181c8f1c877f05d36a448b7",
    "F02-R20": "0c3fc1de68d19ccb906add3eb0018415aaa89e9a09594a00d5741e9f963c227a",
}
EXPECTED_LEX = {
    "F02-R02": [
        ("tt", "7ac4aabb0ca5bb9863733fa2237b75a7dd379b6764b368862a843873775c3747"),
        ("bb", "dc407d56d0fe4b0b4a63f3d154d99537e2cf5a53ec34e7338250416338366d71"),
        ("cc", "45d63f61b744707a36ee1beacc1956c9173989453e999268752161dd7d1a18fd"),
        ("dd^2", "3d436ff8bc3c3b7a40265f2ec72b8b5af1ae2076a3cfa3a8023183f1ca57b78e"),
        ("ww^2", "7cde15d55391b27235c61cb58a44276da0ec8b4bd8ea168d1b9b9258e00d927d"),
    ],
    "F02-R20": [
        ("tt", "5367c0172597800b03fe3b2af860efe94b648519b2d8c62799bc848cbc28eb06"),
        ("bb", "e283350a7fe6d52a6eaf429ecd965bebd2f6e773bf6dfa068a371882d2394b9c"),
        ("cc", "10fbc4c5535c9f8dc8c108001224cd3f167cfe28bef74536ce6cfb7cde2fa3fb"),
        ("dd^2", "530783b9c0f8786529e2073f96991203e8d703e97fb044a60edf8cce09ba454e"),
        ("ww^4", "ad549bf01263be37875f44b8e06ced4bcacf14ad0588819173d733750df17693"),
    ],
}
EXPECTED_REMAINDERS = {
    "F02-R02": {
        940017546: {
            "J": (317112865, 1161791022, 627736383),
            "I": (462252474, 145305698, 1796550960),
        },
    },
    "F02-R20": {
        584912723: {
            "J": (1671616282, 297746731, 555560394),
            "I": (134663927, 1672091025, 1334100861),
        },
        1190675975: {
            "J": (309729886, 1997957961, 2008265187),
            "I": (1042061214, 2038553966, 1196113770),
        },
    },
}
B_INVERSION = {
    "F00": "F01",
    "F01": "F00",
    "F02": "F03",
    "F03": "F02",
    "F04": "F05",
    "F05": "F04",
    "F06": "F07",
    "F07": "F06",
    "M00": "M00",
    "M01": "M02",
    "M02": "M01",
    "M03": "M03",
}
EXPECTED_SIGNS = {
    key: (-1 if key in {"M00", "M03"} else 1) for key in B_INVERSION
}
EXPECTED_OPEN = {
    f"{assignment}-{target}"
    for assignment in (
        "F00", "F01", "F04", "F05", "F06", "F07",
        "M00", "M01", "M02", "M03",
    )
    for target in ("R02", "R11", "R20")
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_sha(data: dict[str, Any]) -> str:
    copy_data = dict(data)
    copy_data.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(copy_data).encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def git_blob_sha1(path: Path) -> str:
    value = path.read_bytes()
    return hashlib.sha1(f"blob {len(value)}\0".encode() + value).hexdigest()


def norm_quadratic(a: int, slope: int, constant: int) -> int:
    """Norm of slope*w+constant modulo w^2+a*w+1."""
    return (
        constant * constant
        - a * slope * constant
        + slope * slope
    ) % PRIME


def verify_source_pins(data: dict[str, Any]) -> None:
    require(sha256(COMPILER) == COMPILER_SHA256, "compiler SHA-256")
    require(sha256(ATLAS_COMPILER) == ATLAS_COMPILER_SHA256, "atlas SHA-256")
    require(git_blob_sha1(ATLAS_COMPILER) == ATLAS_COMPILER_BLOB, "atlas blob")
    require(
        sha256(ATLAS_CERTIFICATE) == ATLAS_CERTIFICATE_SHA256,
        "atlas certificate SHA-256",
    )
    require(
        git_blob_sha1(ATLAS_CERTIFICATE) == ATLAS_CERTIFICATE_BLOB,
        "atlas certificate blob",
    )
    atlas = json.loads(ATLAS_CERTIFICATE.read_text())
    require(atlas["payload_sha256"] == ATLAS_PAYLOAD, "atlas payload recorded")
    require(payload_sha(atlas) == ATLAS_PAYLOAD, "atlas payload recomputed")
    pins = data["source_pins"]
    require(
        pins["atlas_compiler"]["sha256"] == ATLAS_COMPILER_SHA256,
        "certificate atlas compiler pin",
    )
    require(
        pins["atlas_certificate"]["payload_sha256"] == ATLAS_PAYLOAD,
        "certificate atlas payload pin",
    )


def verify_coordinate_pair(value: Any, context: str) -> None:
    require(isinstance(value, list) and len(value) == 2, f"{context} shape")
    require(
        all(isinstance(item, int) and 0 <= item < PRIME for item in value),
        f"{context} range",
    )


def factor_hashes(cell: dict[str, Any], side: str) -> list[str]:
    return [
        item["metric"]["sha256"]
        for item in cell["factor_first"][side]
    ]


def verify_cell(cell: dict[str, Any]) -> None:
    cell_id = cell["cell_id"]
    target = cell_id[-3:]
    expected_count = 1 if target == "R11" else 4
    expected_factor_count = 1 if target == "R11" else 2
    branch_info = cell["branch_exhaustivity"]
    require(
        branch_info == {
            "c_factor_count": expected_factor_count,
            "d_factor_count": expected_factor_count,
            "cartesian_branch_count": expected_count,
            "all_cartesian_branches_present_once": True,
        },
        f"{cell_id} branch exhaustivity",
    )
    require(
        factor_hashes(cell, "c_constant")
        == EXPECTED_FACTOR_HASHES[cell_id]["c_constant"],
        f"{cell_id} c factor hashes",
    )
    require(
        factor_hashes(cell, "d_constant")
        == EXPECTED_FACTOR_HASHES[cell_id]["d_constant"],
        f"{cell_id} d factor hashes",
    )
    branches = cell["branches"]
    require(len(branches) == expected_count, f"{cell_id} branch count")
    branch_keys = [tuple(item["branch"]) for item in branches]
    require(len(set(branch_keys)) == len(branch_keys), f"{cell_id} duplicate branch")
    require(
        set(branch_keys)
        == {
            (left, right)
            for left in range(expected_factor_count)
            for right in range(expected_factor_count)
        },
        f"{cell_id} Cartesian branches",
    )
    nonunits = [
        item for item in branches
        if not item["localized_groebner"]["unit"]
    ]
    for branch in branches:
        groebner = branch["localized_groebner"]
        require(groebner["size"] == len(groebner["basis"]), "basis size")
        expressions = [item["expression"] for item in groebner["basis"]]
        require(
            hashlib.sha256(canonical_json(expressions).encode()).hexdigest()
            == groebner["basis_sha256"],
            f"{cell_id} basis digest",
        )
        for item in groebner["basis"]:
            require(
                sha_text(item["expression"]) == item["metric"]["sha256"],
                f"{cell_id} basis expression hash",
            )
        c_index, d_index = branch["branch"]
        require(
            branch["selected_factor_sha256"]["c_constant"]
            == EXPECTED_FACTOR_HASHES[cell_id]["c_constant"][c_index],
            f"{cell_id} selected c factor link",
        )
        require(
            branch["selected_factor_sha256"]["d_constant"]
            == EXPECTED_FACTOR_HASHES[cell_id]["d_constant"][d_index],
            f"{cell_id} selected d factor link",
        )
        if groebner["unit"]:
            require(groebner["size"] == 1, f"{cell_id} unit basis size")
            require(
                groebner["basis_sha256"] == UNIT_BASIS_SHA256,
                f"{cell_id} unit basis hash",
            )
            require(
                branch["classification"] == "EMPTY_LOCALIZED_UNIT_IDEAL",
                f"{cell_id} unit classification",
            )
        else:
            require(
                groebner["basis_sha256"]
                == EXPECTED_NONUNIT_BASIS_SHA256[cell_id],
                f"{cell_id} nonunit basis hash",
            )
            require(
                branch["classification"] == "ZERO_DIMENSIONAL_QSLICE_SURVIVOR",
                f"{cell_id} survivor branch classification",
            )

    if target == "R11":
        require(not nonunits, "R11 must be a unit ideal")
        require(cell["survivor"] is None, "R11 survivor must be null")
        require(cell["conclusion"] == "EMPTY_LOCALIZED_QSLICE", "R11 conclusion")
        require(cell["proof_mode"] == "DIRECT_UNIT_IDEAL", "R11 proof mode")
        return

    require(len(nonunits) == 1, f"{cell_id} unique survivor")
    require(tuple(nonunits[0]["branch"]) == (0, 0), f"{cell_id} survivor branch")
    survivor = cell["survivor"]
    require(survivor is not None, f"{cell_id} survivor record")
    require(tuple(survivor["branch"]) == (0, 0), f"{cell_id} survivor link")
    require(
        survivor["classification"] == "EMPTY_AFTER_FULL_QUOTIENT_IDENTITIES",
        f"{cell_id} survivor classification",
    )
    lex_basis = survivor["lex_groebner"]["basis"]
    require(
        [
            (item["leading_monomial"], item["metric"]["sha256"])
            for item in lex_basis
        ]
        == EXPECTED_LEX[cell_id],
        f"{cell_id} lex basis pins",
    )
    require(
        all(sha_text(item["expression"]) == item["metric"]["sha256"]
            for item in lex_basis),
        f"{cell_id} lex expression hashes",
    )
    census = survivor["point_census"]
    expected_points = 4 if target == "R02" else 8
    require(
        census["standard_monomial_dimension"] == expected_points,
        f"{cell_id} quotient dimension",
    )
    require(census["point_count_over_Fp2"] == expected_points, "point census")
    require(census["all_points_lie_in_Fp2_subfield_of_Fp6"], "subfield audit")
    require(census["full_J_identity_false_at_every_point"], "J mismatch coverage")
    require(census["full_I_identity_false_at_every_point"], "I mismatch coverage")
    components = census["components"]
    require(
        len(components) == len(EXPECTED_REMAINDERS[cell_id]),
        f"{cell_id} component count",
    )
    total_points = 0
    middles: set[int] = set()
    for component in components:
        middle = component["w_minimal_polynomial_middle"]
        middles.add(middle)
        require(
            component["w_minimal_polynomial_coefficients"] == [1, middle, 1],
            f"{cell_id} reciprocal minimal polynomial",
        )
        require(component["irreducible_degree"] == 2, "component degree")
        require(component["point_count"] == len(component["points"]), "point list")
        require(component["point_count"] == 4, "four points per quadratic")
        require(
            len({canonical_json(point) for point in component["points"]})
            == component["point_count"],
            f"{cell_id} distinct component points",
        )
        total_points += component["point_count"]
        for point_index, point in enumerate(component["points"]):
            require(set(point) == {"b", "c", "d", "w", "z"}, "point fields")
            for name, value in point.items():
                verify_coordinate_pair(
                    value, f"{cell_id} component {middle} point {point_index} {name}"
                )
        for identity in ("J", "I"):
            mismatch = component["full_quotient_mismatches"][identity]
            require(mismatch["coefficient_index"] == 1, "mismatch coefficient")
            require(mismatch["nonzero"], "mismatch nonzero flag")
            require(
                mismatch["uniform_over_d_roots_and_w_conjugates"],
                "mismatch uniformity",
            )
            remainder = mismatch["remainder_mod_w_factor"]
            observed = (
                remainder["w_coefficient"],
                remainder["constant"],
                mismatch["norm_to_prime_field"],
            )
            expected = EXPECTED_REMAINDERS[cell_id][middle][identity]
            require(observed == expected, f"{cell_id} {middle} {identity} constants")
            require(
                norm_quadratic(middle, observed[0], observed[1]) == observed[2],
                f"{cell_id} {middle} {identity} norm replay",
            )
            require(observed[2] != 0, f"{cell_id} {middle} {identity} nonzero norm")
    require(total_points == expected_points, f"{cell_id} total points")
    require(middles == set(EXPECTED_REMAINDERS[cell_id]), "component coverage")
    require(cell["conclusion"] == "EMPTY_FULL_SOURCE", f"{cell_id} conclusion")
    require(
        cell["proof_mode"]
        == "FULL_J_AND_I_QUOTIENT_MISMATCH_ON_EXACT_POINT_CENSUS",
        f"{cell_id} proof mode",
    )


def verify(
    data: dict[str, Any],
    *,
    sources: bool = True,
    pinned_payload: bool = True,
) -> None:
    require(data["schema"] == SCHEMA, "schema")
    require(data["payload_sha256"] == payload_sha(data), "payload recomputation")
    if pinned_payload:
        require(data["payload_sha256"] == EXPECTED_PAYLOAD, "pinned payload")
    if sources:
        verify_source_pins(data)
    require(data["field"]["prime"] == PRIME, "deployed prime")
    require(data["field"]["challenge_extension_degree"] == 6, "challenge degree")
    require(
        data["scope"] == {
            "direct_assignment": "F02",
            "transported_assignment": "F03",
            "targets": ["R02", "R11", "R20"],
            "direct_cells_deleted": 3,
            "transported_cells_deleted": 3,
            "ledger_movement": 0,
        },
        "scope",
    )
    localizer = data["localizer"]
    require(
        localizer["raw"] == {
            "degree": 54,
            "terms": 34112,
            "sha256": (
                "21d38166362e101d6505bdee2edc2373c27c9d6905bb6eb55d845043c133844e"
            ),
        },
        "raw localizer",
    )
    require(localizer["rabinowitsch"]["degree"] == 55, "Rabinowitsch degree")
    require(localizer["rabinowitsch"]["terms"] == 34113, "Rabinowitsch terms")
    radical = localizer["radical"]
    require(radical["factor_count"] == 34, "localizer factor count")
    require(radical["degree"] == 43, "localizer radical degree")
    require(radical["terms"] == 12312, "localizer radical terms")
    require(
        radical["sha256"]
        == "a5a4eb686175c86d5cd6f4a04dba92c9b8063cbbaf37856be6d28d5e1b1b36e1",
        "localizer radical hash",
    )
    require(radical["factors"] == EXPECTED_LOCALIZER_FACTORS, "localizer factors")

    cells = data["cells"]
    require(len(cells) == 3, "three direct cells")
    require(
        [item["cell_id"] for item in cells]
        == ["F02-R02", "F02-R11", "F02-R20"],
        "cell order and coverage",
    )
    require(len({item["cell_id"] for item in cells}) == 3, "unique cells")
    for cell in cells:
        require(cell["ledger_movement"] == 0, "cell ledger movement")
        verify_cell(cell)

    inversion = data["literal_b_inversion"]
    require(inversion["map"] == B_INVERSION, "inversion map")
    require(inversion["proved_for_all_twelve_assignments"], "inversion coverage flag")
    require(
        inversion["imported_conclusion"] == "F02_EMPTY_IMPLIES_F03_EMPTY",
        "transported conclusion",
    )
    require(inversion["other_conclusions_imported"] == [], "extra imports")
    records = inversion["records"]
    require(len(records) == 12, "twelve inversion records")
    require(len({record["source"] for record in records}) == 12, "unique records")
    for record in records:
        source = record["source"]
        require(record["target"] == B_INVERSION[source], f"{source} partner")
        require(record["U_global_sign"] == EXPECTED_SIGNS[source], f"{source} U sign")
        for key in (
            "V_exact",
            "z_exact",
            "q_exact",
            "G_equals_U2_minus_WV2_exact",
            "full_J_identity_exact_by_factor_transport",
            "full_I_identity_exact_by_factor_transport",
        ):
            require(record[key] is True, f"{source} {key}")
        require(
            record["label_factor_multisets_exact"]
            == {"J": True, "I": True, "K": True, "R": True},
            f"{source} label multisets",
        )
    require(
        data["conclusions"] == {
            "F02-R02": "EMPTY",
            "F02-R11": "EMPTY",
            "F02-R20": "EMPTY",
            "F03-R02": "EMPTY_BY_LITERAL_INVERSION",
            "F03-R11": "EMPTY_BY_LITERAL_INVERSION",
            "F03-R20": "EMPTY_BY_LITERAL_INVERSION",
        },
        "conclusions",
    )
    require(set(data["open_cells"]) == EXPECTED_OPEN, "open-cell fence")
    require(len(data["open_cells"]) == 30, "open-cell count")
    require(
        data["evidence_level"] == {
            "F02_F03_local_lemma": "PROVED_EXACT_GREEN",
            "K3_row": "OPEN",
            "global_ledger": "UNCHANGED",
        },
        "evidence level",
    )
    require(len(data["nonclaims"]) == 6, "nonclaim count")


def repayload(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_sha(data)


def mutation_cases() -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    def mutate(path: tuple[Any, ...], value: Any) -> Callable[[dict[str, Any]], None]:
        def apply(data: dict[str, Any]) -> None:
            cursor: Any = data
            for key in path[:-1]:
                cursor = cursor[key]
            cursor[path[-1]] = value
        return apply

    return [
        ("schema", mutate(("schema",), "wrong")),
        ("prime", mutate(("field", "prime"), PRIME - 2)),
        ("scope-direct", mutate(("scope", "direct_assignment"), "F04")),
        ("scope-ledger", mutate(("scope", "ledger_movement"), 1)),
        ("raw-localizer", mutate(("localizer", "raw", "degree"), 53)),
        ("radical-hash", mutate(("localizer", "radical", "sha256"), "0" * 64)),
        ("factor-delete", lambda data: data["localizer"]["radical"]["factors"].pop()),
        ("cell-delete", lambda data: data["cells"].pop()),
        ("cell-duplicate", lambda data: data["cells"].append(copy.deepcopy(data["cells"][0]))),
        ("branch-delete", lambda data: data["cells"][0]["branches"].pop()),
        (
            "branch-duplicate",
            lambda data: data["cells"][0]["branches"].append(
                copy.deepcopy(data["cells"][0]["branches"][0])
            ),
        ),
        (
            "unit-flip",
            mutate(("cells", 1, "branches", 0, "localized_groebner", "unit"), False),
        ),
        ("r11-survivor", mutate(("cells", 1, "survivor"), {})),
        (
            "point-count",
            mutate(("cells", 0, "survivor", "point_census", "point_count_over_Fp2"), 3),
        ),
        (
            "norm-zero",
            mutate(
                (
                    "cells", 0, "survivor", "point_census", "components", 0,
                    "full_quotient_mismatches", "J", "norm_to_prime_field",
                ),
                0,
            ),
        ),
        (
            "remainder",
            mutate(
                (
                    "cells", 0, "survivor", "point_census", "components", 0,
                    "full_quotient_mismatches", "I",
                    "remainder_mod_w_factor", "constant",
                ),
                1,
            ),
        ),
        (
            "point-coordinate",
            mutate(
                (
                    "cells", 0, "survivor", "point_census",
                    "components", 0, "points", 0, "b", 0,
                ),
                PRIME,
            ),
        ),
        (
            "point-duplicate",
            lambda data: data["cells"][0]["survivor"]["point_census"][
                "components"
            ][0]["points"].__setitem__(
                1,
                copy.deepcopy(
                    data["cells"][0]["survivor"]["point_census"][
                        "components"
                    ][0]["points"][0]
                ),
            ),
        ),
        ("inversion-delete", lambda data: data["literal_b_inversion"]["records"].pop()),
        (
            "inversion-map",
            mutate(("literal_b_inversion", "map", "F02"), "F05"),
        ),
        (
            "U-sign",
            mutate(("literal_b_inversion", "records", 2, "U_global_sign"), -1),
        ),
        (
            "V-exact",
            mutate(("literal_b_inversion", "records", 2, "V_exact"), False),
        ),
        (
            "label-factor",
            mutate(
                (
                    "literal_b_inversion", "records", 2,
                    "label_factor_multisets_exact", "J",
                ),
                False,
            ),
        ),
        (
            "extra-import",
            mutate(("literal_b_inversion", "other_conclusions_imported"), ["F04"]),
        ),
        ("open-delete", lambda data: data["open_cells"].pop()),
        (
            "K3-green",
            mutate(("evidence_level", "K3_row"), "CLOSED"),
        ),
    ]


def run_mutations(data: dict[str, Any]) -> int:
    count = 0
    for name, mutation in mutation_cases():
        candidate = copy.deepcopy(data)
        mutation(candidate)
        repayload(candidate)
        try:
            verify(candidate, sources=False, pinned_payload=False)
        except (AssertionError, KeyError, IndexError, TypeError, ValueError):
            count += 1
            continue
        raise AssertionError(f"mutation survived: {name}")
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    require(args.check or args.tamper_selftest, "choose --check and/or --tamper-selftest")
    data = json.loads(CERTIFICATE.read_text())
    if args.check:
        verify(data)
        print(
            "PASS: F02/F03 deletion "
            f"cells={len(data['cells'])} payload={data['payload_sha256']}"
        )
    if args.tamper_selftest:
        count = run_mutations(data)
        print(f"PASS: fail-closed semantic mutations {count}/{count}")


if __name__ == "__main__":
    main()
