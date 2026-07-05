#!/usr/bin/env python3
"""Growing-dimensional d=3 Conjecture-F finite census.

Status: EXPERIMENTAL / AUDIT. This script records exact incidence counts for
structured and seeded projective flats on the requested mu_16 toy rows. It is a
finite census, not a proof or refutation of Conjecture-F.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from math import comb, gcd
from pathlib import Path
from typing import Any


STATUS = "EXPERIMENTAL"
THEOREM_PROBLEM_ID = "rem:v13-conjf-open; prob:band; thm:v13-dim2"
SCHEMA_VERSION = "growing-dim-conjf-d3-v2"
DEFAULT_OUTPUT = Path(
    "experimental/data/certificates/growing-dim-conjf-d3/"
    "growing_dim_conjf_d3.json"
)
ROWS = (97, 113, 241)
N = 16
J = 4
RANDOM_FLATS_PER_DIM = 48
DIRECTED_NORMAL_SAMPLES = 60_000
SEED = 2026070509


def primitive_root(p: int) -> int:
    factors: list[int] = []
    value = p - 1
    d = 2
    while d * d <= value:
        if value % d == 0:
            factors.append(d)
            while value % d == 0:
                value //= d
        d += 1 if d == 2 else 2
    if value > 1:
        factors.append(value)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise ValueError(f"no primitive root for F_{p}")


def subgroup(p: int, n: int) -> tuple[int, ...]:
    if (p - 1) % n:
        raise ValueError("n must divide p-1")
    omega = pow(primitive_root(p), (p - 1) // n, p)
    values = tuple(pow(omega, i, p) for i in range(n))
    assert len(set(values)) == n
    return values


def trim(poly: tuple[int, ...]) -> tuple[int, ...]:
    out = list(poly)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def poly_eval(poly: tuple[int, ...], x: int, p: int) -> int:
    acc = 0
    for coeff in reversed(poly):
        acc = (acc * x + coeff) % p
    return acc


def locator(domain: tuple[int, ...], support: tuple[int, ...], p: int) -> tuple[int, ...]:
    coeffs = [1]
    for index in support:
        root = domain[index]
        nxt = [0] * (len(coeffs) + 1)
        for i, coeff in enumerate(coeffs):
            nxt[i] = (nxt[i] - coeff * root) % p
            nxt[i + 1] = (nxt[i + 1] + coeff) % p
        coeffs = nxt
    return tuple(coeffs)


def matrix_rank(rows: list[list[int]], p: int) -> int:
    if not rows:
        return 0
    work = [[x % p for x in row] for row in rows]
    rank = 0
    width = len(work[0])
    for col in range(width):
        pivot = None
        for row in range(rank, len(work)):
            if work[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inv = pow(work[rank][col], -1, p)
        work[rank] = [(inv * value) % p for value in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][col] % p:
                factor = work[row][col]
                work[row] = [
                    (work[row][i] - factor * work[rank][i]) % p
                    for i in range(width)
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def rank_polys(polys: list[tuple[int, ...]], width: int, p: int) -> int:
    return matrix_rank(
        [[poly[i] % p if i < len(poly) else 0 for i in range(width)] for poly in polys],
        p,
    )


def in_span(poly: tuple[int, ...], basis: list[tuple[int, ...]], width: int, p: int) -> bool:
    return rank_polys(basis + [poly], width, p) == rank_polys(basis, width, p)


def stabilizer_size(support: tuple[int, ...], n: int) -> int:
    S = set(support)
    return sum(1 for shift in range(n) if {(x + shift) % n for x in S} == S)


def gcd_trivial_space(basis: list[tuple[int, ...]], domain: tuple[int, ...], p: int) -> bool:
    return all(any(poly_eval(poly, point, p) != 0 for poly in basis) for point in domain)


def canonical_basis(basis: list[tuple[int, ...]], width: int, p: int) -> list[tuple[int, ...]]:
    rows = [[poly[i] % p if i < len(poly) else 0 for i in range(width)] for poly in basis]
    rank = 0
    pivots: list[int] = []
    for col in range(width):
        pivot = None
        for row in range(rank, len(rows)):
            if rows[row][col]:
                pivot = row
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, p)
        rows[rank] = [(inv * x) % p for x in rows[rank]]
        for row in range(len(rows)):
            if row != rank and rows[row][col]:
                factor = rows[row][col]
                rows[row] = [(rows[row][i] - factor * rows[rank][i]) % p for i in range(width)]
        pivots.append(col)
        rank += 1
        if rank == len(rows):
            break
    return [tuple(row) for row in rows[:rank]]


def canonical_vector(vector: tuple[int, ...], p: int) -> tuple[int, ...]:
    for value in vector:
        if value % p:
            inv = pow(value, -1, p)
            return tuple((inv * item) % p for item in vector)
    raise ValueError("zero vector has no projective representative")


def null_normal(rows: list[tuple[int, ...]], p: int) -> tuple[int, ...] | None:
    work = [[x % p for x in row] for row in rows]
    width = len(work[0])
    rank = 0
    pivots: list[int] = []
    for col in range(width):
        pivot = None
        for row in range(rank, len(work)):
            if work[row][col]:
                pivot = row
                break
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inv = pow(work[rank][col], -1, p)
        work[rank] = [(inv * value) % p for value in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][col]:
                factor = work[row][col]
                work[row] = [(work[row][i] - factor * work[rank][i]) % p for i in range(width)]
        pivots.append(col)
        rank += 1
        if rank == len(work):
            break
    if rank != width - 1:
        return None
    free_cols = [col for col in range(width) if col not in pivots]
    normal = [0] * width
    normal[free_cols[0]] = 1
    for row_index, col in reversed(list(enumerate(pivots))):
        normal[col] = (-sum(work[row_index][i] * normal[i] for i in range(col + 1, width))) % p
    return canonical_vector(tuple(normal), p)


def evaluation_normal(point: int, width: int, p: int) -> tuple[int, ...]:
    return canonical_vector(tuple(pow(point, degree, p) for degree in range(width)), p)


def normal_is_evaluation(normal: tuple[int, ...], domain: tuple[int, ...], p: int) -> bool:
    width = len(normal)
    return any(normal == evaluation_normal(point, width, p) for point in domain)


def hyperplane_basis_from_normal(normal: tuple[int, ...], p: int) -> list[tuple[int, ...]]:
    width = len(normal)
    pivot = next(index for index, value in enumerate(normal) if value % p)
    inv = pow(normal[pivot], -1, p)
    basis: list[tuple[int, ...]] = []
    for free_col in range(width):
        if free_col == pivot:
            continue
        row = [0] * width
        row[free_col] = 1
        row[pivot] = (-normal[free_col] * inv) % p
        basis.append(tuple(row))
    return canonical_basis(basis, width, p)


def fraction_text(numerator: int, denominator: int) -> str:
    factor = gcd(numerator, denominator)
    return f"{numerator // factor}/{denominator // factor}"


def std_basis(width: int, keep: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [tuple(1 if i == col else 0 for i in range(width)) for col in keep]


def random_basis(rng: random.Random, dim: int, width: int, p: int) -> list[tuple[int, ...]]:
    basis: list[tuple[int, ...]] = []
    while len(basis) < dim + 1:
        candidate = tuple(rng.randrange(p) for _ in range(width))
        if any(candidate) and rank_polys(basis + [candidate], width, p) == len(basis) + 1:
            basis.append(candidate)
    return basis


def locator_span_basis(locators: list[tuple[int, ...]], dim: int, width: int, p: int) -> list[tuple[int, ...]]:
    basis: list[tuple[int, ...]] = []
    for loc in locators:
        if rank_polys(basis + [loc], width, p) == len(basis) + 1:
            basis.append(loc)
        if len(basis) == dim + 1:
            break
    if len(basis) != dim + 1:
        raise AssertionError("not enough independent locators")
    return basis


def build_candidates(p: int, domain: tuple[int, ...], locators: list[tuple[tuple[int, ...], tuple[int, ...]]],
                     dim: int) -> list[dict[str, Any]]:
    width = J + 1
    candidates: list[dict[str, Any]] = []

    def append_candidate(family: str, tag: str, basis: list[tuple[int, ...]]) -> None:
        canonical = canonical_basis(basis, width, p)
        if len(canonical) != dim + 1:
            return
        if not gcd_trivial_space(canonical, domain, p):
            return
        if any(existing["basis"] == canonical for existing in candidates):
            return
        candidates.append({"family": family, "tag": tag, "basis": canonical})

    omitted_count = width - (dim + 1)
    for omitted in itertools.combinations(range(width), omitted_count):
        keep = tuple(i for i in range(width) if i not in omitted)
        append_candidate("coefficient_flat", "omit_" + "_".join(map(str, omitted)), std_basis(width, keep))
    ordered_locs = [poly for _support, poly in locators]
    for start in range(0, min(80, len(ordered_locs)), 7):
        append_candidate(
            "locator_span_window",
            f"window_{start}",
            locator_span_basis(ordered_locs[start:] + ordered_locs[:start], dim, width, p),
        )
    spread = ordered_locs[:: max(1, len(ordered_locs) // 40)]
    if len(spread) >= dim + 1:
        for start in range(min(8, len(spread))):
            append_candidate(
                "locator_span_spread",
                f"spread_{start}",
                locator_span_basis(spread[start:] + spread[:start], dim, width, p),
            )
    rng = random.Random(SEED + p * 10 + dim)
    accepted = 0
    attempts = 0
    while accepted < RANDOM_FLATS_PER_DIM and attempts < RANDOM_FLATS_PER_DIM * 20:
        attempts += 1
        basis = random_basis(rng, dim, width, p)
        before = len(candidates)
        append_candidate("seeded_random", f"seed_{accepted}", basis)
        if len(candidates) > before:
            accepted += 1
    return candidates


def count_hits(candidate: dict[str, Any], locators: list[tuple[tuple[int, ...], tuple[int, ...]]],
               domain: tuple[int, ...], p: int) -> dict[str, Any]:
    basis = [tuple(row) for row in candidate["basis"]]
    width = J + 1
    if rank_polys(basis, width, p) != len(basis):
        raise AssertionError("candidate basis is not independent")
    if not gcd_trivial_space(basis, domain, p):
        raise AssertionError("candidate basis has a common domain root")
    hits = []
    periodic_hits = []
    for support, poly in locators:
        if in_span(poly, basis, width, p):
            scale = stabilizer_size(support, N)
            item = {"support": list(support), "periodicity_scale": scale}
            if scale == 1:
                hits.append(item)
            else:
                periodic_hits.append(item)
    return {
        "family": candidate["family"],
        "tag": candidate["tag"],
        "basis": [list(row) for row in basis],
        "aperiodic_hit_count": len(hits),
        "periodic_hit_count": len(periodic_hits),
        "aperiodic_hits": hits[:24],
        "periodic_hits": periodic_hits[:24],
        "hits_truncated": len(hits) > 24 or len(periodic_hits) > 24,
    }


def count_normal_hits(normal: tuple[int, ...], locators: list[tuple[tuple[int, ...], tuple[int, ...]]],
                      p: int) -> dict[str, Any]:
    hits = []
    periodic_hits = []
    for support, poly in locators:
        if sum(normal[index] * poly[index] for index in range(len(normal))) % p:
            continue
        scale = stabilizer_size(support, N)
        item = {"support": list(support), "periodicity_scale": scale}
        if scale == 1:
            hits.append(item)
        else:
            periodic_hits.append(item)
    return {
        "aperiodic_hit_count": len(hits),
        "periodic_hit_count": len(periodic_hits),
        "aperiodic_hits": hits[:24],
        "periodic_hits": periodic_hits[:24],
        "hits_truncated": len(hits) > 24 or len(periodic_hits) > 24,
    }


def evaluation_hyperplane_calibration(domain: tuple[int, ...],
                                      locators: list[tuple[tuple[int, ...], tuple[int, ...]]],
                                      p: int) -> dict[str, Any]:
    point_rows = []
    for point_index, point in enumerate(domain):
        normal = evaluation_normal(point, J + 1, p)
        normal_counts = count_normal_hits(normal, locators, p)
        through_total = 0
        through_aperiodic = 0
        through_periodic = 0
        for support, _poly in locators:
            if point_index not in support:
                continue
            through_total += 1
            if stabilizer_size(support, N) == 1:
                through_aperiodic += 1
            else:
                through_periodic += 1
        if through_total != normal_counts["aperiodic_hit_count"] + normal_counts["periodic_hit_count"]:
            raise AssertionError("evaluation normal count mismatch")
        if through_aperiodic != normal_counts["aperiodic_hit_count"]:
            raise AssertionError("evaluation aperiodic count mismatch")
        if through_periodic != normal_counts["periodic_hit_count"]:
            raise AssertionError("evaluation periodic count mismatch")
        point_rows.append(
            {
                "point_index": point_index,
                "point": point,
                "normal": list(normal),
                "total_through_point": through_total,
                "aperiodic_through_point": through_aperiodic,
                "periodic_through_point": through_periodic,
            }
        )
    expected_total = comb(N - 1, J - 1)
    periodic_through = point_rows[0]["periodic_through_point"]
    expected_aperiodic = expected_total - periodic_through
    if any(row["total_through_point"] != expected_total for row in point_rows):
        raise AssertionError("evaluation total is not uniform")
    if any(row["aperiodic_through_point"] != expected_aperiodic for row in point_rows):
        raise AssertionError("evaluation aperiodic count is not uniform")
    if expected_aperiodic != 448:
        raise AssertionError("unexpected mu_16,j=4 evaluation aperiodic count")
    return {
        "object": "excluded evaluation hyperplanes normal to (1,a,a^2,a^3,a^4)",
        "point_count": len(point_rows),
        "total_through_point": expected_total,
        "periodic_through_point": periodic_through,
        "aperiodic_through_point": expected_aperiodic,
        "identity": "C(15,3) - 7 = 448",
        "dim3_envelope_binom_n_3": comb(N, 3),
        "aperiodic_to_envelope": fraction_text(expected_aperiodic, comb(N, 3)),
        "point_rows": point_rows,
    }


def directed_common_normal_search(p: int, domain: tuple[int, ...],
                                  locators: list[tuple[tuple[int, ...], tuple[int, ...]]]) -> dict[str, Any]:
    rng = random.Random(SEED + p * 1000)
    aperiodic_locators = [
        (support, poly) for support, poly in locators if stabilizer_size(support, N) == 1
    ]
    seen_normals: set[tuple[int, ...]] = set()
    duplicate_normals = 0
    dependent_samples = 0
    skipped_evaluation = 0
    accepted_normals = 0
    over_envelope_count = 0
    best_witness: dict[str, Any] | None = None
    best_count = -1
    last_improvement_sample = -1
    envelope = comb(N, 3)
    for sample_index in range(DIRECTED_NORMAL_SAMPLES):
        sample = rng.sample(aperiodic_locators, J)
        normal = null_normal([poly for _support, poly in sample], p)
        if normal is None:
            dependent_samples += 1
            continue
        if normal in seen_normals:
            duplicate_normals += 1
            continue
        seen_normals.add(normal)
        if normal_is_evaluation(normal, domain, p):
            skipped_evaluation += 1
            continue
        counts = count_normal_hits(normal, locators, p)
        accepted_normals += 1
        if counts["aperiodic_hit_count"] > envelope:
            over_envelope_count += 1
        if counts["aperiodic_hit_count"] > best_count:
            basis = hyperplane_basis_from_normal(normal, p)
            if not gcd_trivial_space(basis, domain, p):
                raise AssertionError("directed candidate is not gcd-trivial")
            best_count = counts["aperiodic_hit_count"]
            last_improvement_sample = sample_index
            best_witness = {
                "family": "directed_common_normal",
                "tag": f"sample_{sample_index}",
                "normal": list(normal),
                "sample_supports": [list(support) for support, _poly in sample],
                "basis": [list(row) for row in basis],
                "aperiodic_hit_count": counts["aperiodic_hit_count"],
                "periodic_hit_count": counts["periodic_hit_count"],
                "aperiodic_hits": counts["aperiodic_hits"],
                "periodic_hits": counts["periodic_hits"],
                "hits_truncated": counts["hits_truncated"],
            }
    if best_witness is None:
        raise AssertionError("directed search found no admissible hyperplane")
    return {
        "method": "common normal of random 4-subsets of aperiodic locators",
        "samples_requested": DIRECTED_NORMAL_SAMPLES,
        "sampled_locator_class": "aperiodic Dloc_4 only",
        "unique_normals_seen": len(seen_normals),
        "accepted_gcd_trivial_normals": accepted_normals,
        "skipped_evaluation_hyperplanes": skipped_evaluation,
        "dependent_samples": dependent_samples,
        "duplicate_normals": duplicate_normals,
        "over_envelope_count": over_envelope_count,
        "max_aperiodic_incidence": best_witness["aperiodic_hit_count"],
        "max_periodic_hits_in_candidate": best_witness["periodic_hit_count"],
        "last_improvement_sample": last_improvement_sample,
        "samples_after_last_improvement": DIRECTED_NORMAL_SAMPLES - last_improvement_sample - 1,
        "max_to_envelope": fraction_text(best_witness["aperiodic_hit_count"], envelope),
        "max_witness": best_witness,
    }


def row_payload(p: int) -> dict[str, Any]:
    domain = subgroup(p, N)
    locs = [
        (support, locator(domain, support, p))
        for support in itertools.combinations(range(N), J)
    ]
    evaluation_calibration = evaluation_hyperplane_calibration(domain, locs, p)
    dim_rows = {}
    for dim in (2, 3):
        candidates = build_candidates(p, domain, locs, dim)
        checked = [count_hits(candidate, locs, domain, p) for candidate in candidates]
        structured_max = max(item["aperiodic_hit_count"] for item in checked)
        structured_witnesses = [
            item for item in checked if item["aperiodic_hit_count"] == structured_max
        ][:5]
        max_count = structured_max
        max_periodic = max(item["periodic_hit_count"] for item in checked)
        witnesses = structured_witnesses
        dim_record: dict[str, Any] = {
            "projective_dimension": dim,
            "candidates_checked": len(checked),
            "structured_candidates_checked": len(checked),
            "structured_max_aperiodic_incidence": structured_max,
            "max_aperiodic_incidence": max_count,
            "max_periodic_hits_in_candidate": max_periodic,
            "dim2_comparison_binom_j_2": comb(J, 2) if dim == 2 else None,
            "dim3_envelope_binom_n_3": comb(N, 3) if dim == 3 else None,
            "exceeds_dim2_comparison": dim == 2 and max_count > comb(J, 2),
            "exceeds_dim3_envelope": dim == 3 and max_count > comb(N, 3),
            "max_witnesses": witnesses,
        }
        if dim == 3:
            directed = directed_common_normal_search(p, domain, locs)
            max_count = max(structured_max, directed["max_aperiodic_incidence"])
            max_periodic = max(max_periodic, directed["max_periodic_hits_in_candidate"])
            witnesses = [directed["max_witness"]]
            if structured_max == max_count:
                witnesses.extend(structured_witnesses[:2])
            dim_record.update(
                {
                    "candidates_checked": len(checked) + directed["accepted_gcd_trivial_normals"],
                    "directed_search": directed,
                    "max_aperiodic_incidence": max_count,
                    "max_periodic_hits_in_candidate": max_periodic,
                    "exceeds_dim3_envelope": max_count > comb(N, 3) or directed["over_envelope_count"] > 0,
                    "max_witnesses": witnesses,
                }
            )
        dim_rows[str(dim)] = dim_record
    return {
        "label": f"f{p}_mu{N}_j{J}",
        "p": p,
        "q_gen": p,
        "q_line": p,
        "q_chal": p,
        "n": N,
        "j": J,
        "domain": list(domain),
        "total_Dloc_j": len(locs),
        "aperiodic_Dloc_j": sum(1 for support, _poly in locs if stabilizer_size(support, N) == 1),
        "periodic_Dloc_j": sum(1 for support, _poly in locs if stabilizer_size(support, N) != 1),
        "evaluation_hyperplane_calibration": evaluation_calibration,
        "dimension_rows": dim_rows,
    }


def payload_hash(payload: dict[str, Any]) -> str:
    clone = {key: value for key, value in payload.items() if key != "payload_sha256"}
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def build_certificate() -> dict[str, Any]:
    rows = [row_payload(p) for p in ROWS]
    named = []
    for row in rows:
        dim2 = row["dimension_rows"]["2"]
        dim3 = row["dimension_rows"]["3"]
        if dim2["exceeds_dim2_comparison"]:
            named.append(
                {
                    "row": row["label"],
                    "dimension": 2,
                    "max_aperiodic_incidence": dim2["max_aperiodic_incidence"],
                    "comparison": dim2["dim2_comparison_binom_j_2"],
                }
            )
        if dim3["exceeds_dim3_envelope"]:
            named.append(
                {
                    "row": row["label"],
                    "dimension": 3,
                    "max_aperiodic_incidence": dim3["max_aperiodic_incidence"],
                    "comparison": dim3["dim3_envelope_binom_n_3"],
                }
            )
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "proof_status": STATUS,
        "claim": "finite exact incidence counts for recorded d=2 and d=3 aperiodic Conjecture-F candidate flats",
        "row_rule": "mu_16, j=4, projective dimensions 2 and 3, structured flats plus 60k directed common-normal samples per row",
        "seed": SEED,
        "directed_normal_samples_per_row": DIRECTED_NORMAL_SAMPLES,
        "evaluation_hyperplane_identity": "C(15,3) - 7 = 448 aperiodic locators in each excluded evaluation hyperplane",
        "non_claims": [
            "No growing-dimensional incidence theorem is claimed.",
            "No proof or refutation of Conjecture-F is claimed.",
            "The max values are over the recorded candidate flats, not the full Grassmannian.",
        ],
        "rows": rows,
        "named_over_envelope_findings": named,
    }
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--emit-defaults", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cert = build_certificate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(cert, indent=2, sort_keys=True))
    else:
        print(
            "growing_dim_conjf_d3: "
            f"status={STATUS} result=PASS rows={len(cert['rows'])} "
            f"findings={len(cert['named_over_envelope_findings'])}"
        )
        print(args.output.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
