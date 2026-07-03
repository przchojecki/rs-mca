#!/usr/bin/env python3
"""E18/E19 actual-pair XR scanner and globalness telemetry.

This verifier attaches the E11 stripped XR candidate idea to actual alignment
sets

    A_{u,v} = {T in D_j : H_u l_T is parallel to H_v l_T and H_v l_T != 0}

on the subgroup row.  The committed exact case is J(16,8) over F_97 with
window length t=2.  It scans a deterministic finite corpus of actual word-pair
orbits: delta/delta distances, delta/Fourier-character pairs,
Fourier-character pairs, and deterministic random projective pairs.  The same
code also records sampled J(32,16) telemetry.

The output is experimental evidence, not a proof of c_xr_content or a complete
enumeration of all F_p^{2n} word pairs.  Its value is that the post-strip
objects are genuine A_{u,v} sets rather than dictionary families.  The n=16
E_3 values and all reported n=16 post-strip link densities are exact; the n=32
case never materializes J(32,16) and is sample-only telemetry.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / (
    "experimental/data/certificates/xr-pair-orbit-globalness/"
    "xr_pair_orbit_globalness.json"
)

SCHEMA_VERSION = "xr-pair-orbit-globalness-v1"
P = 97
T_WINDOW = 2
N16_RANDOM_PAIRS = 96
N32_RANDOM_PAIRS = 16
N32_SUPPORT_SAMPLES = 1024
N32_WALK_SAMPLES = 1024
TOP_RECORD_LIMIT = 40
TOP_DECILE_NUMERATOR = 1
TOP_DECILE_DENOMINATOR = 10
LINK_RADII = (1, 2, 3, 4)
TANGENT_LINK_LEAK_THRESHOLD = Fraction(9, 10)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def sha256_json(obj: Any) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def render(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=True) + "\n"


def fraction_record(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "float": float(value),
    }


def primitive_root(p: int) -> int:
    factors = []
    m = p - 1
    q = 2
    while q * q <= m:
        if m % q == 0:
            factors.append(q)
            while m % q == 0:
                m //= q
        q += 1
    if m > 1:
        factors.append(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise AssertionError("no primitive root found")


def subgroup_generator(p: int, n: int) -> int:
    require((p - 1) % n == 0, "field does not contain mu_n")
    gen = pow(primitive_root(p), (p - 1) // n, p)
    require(pow(gen, n, p) == 1, "subgroup generator is not n-torsion")
    for q in prime_divisors(n):
        require(pow(gen, n // q, p) != 1, "subgroup generator has smaller order")
    return gen


def prime_divisors(value: int) -> list[int]:
    out = []
    q = 2
    m = value
    while q * q <= m:
        if m % q == 0:
            out.append(q)
            while m % q == 0:
                m //= q
        q += 1
    if m > 1:
        out.append(m)
    return out


def locator_coefficients(indices: Iterable[int], points: list[int], p: int) -> tuple[int, ...]:
    coeff = [1]
    for index in indices:
        root = points[index]
        new = [0] * (len(coeff) + 1)
        for degree, value in enumerate(coeff):
            new[degree] = (new[degree] - value * root) % p
            new[degree + 1] = (new[degree + 1] + value) % p
        coeff = new
    return tuple(coeff)


def word_syndromes(word: tuple[int, ...], points: list[int], upto: int, p: int) -> tuple[int, ...]:
    return tuple(
        sum(word[index] * pow(points[index], exponent, p) for index in range(len(points))) % p
        for exponent in range(upto + 1)
    )


def hankel_product(syndromes: tuple[int, ...], locator: tuple[int, ...], t: int, p: int) -> tuple[int, ...]:
    degree = len(locator) - 1
    return tuple(
        sum(locator[c] * syndromes[row + c] for c in range(degree + 1)) % p
        for row in range(t)
    )


def parallel_noncontained(
    locator: tuple[int, ...],
    syndromes_u: tuple[int, ...],
    syndromes_v: tuple[int, ...],
    t: int,
    p: int,
) -> bool:
    a = hankel_product(syndromes_u, locator, t, p)
    b = hankel_product(syndromes_v, locator, t, p)
    if all(entry == 0 for entry in b):
        return False
    return all(
        (a[r] * b[s] - a[s] * b[r]) % p == 0
        for r in range(t)
        for s in range(r + 1, t)
    )


class JohnsonCase:
    def __init__(self, n: int, j: int, p: int = P, t: int = T_WINDOW) -> None:
        self.n = n
        self.j = j
        self.p = p
        self.t = t
        self.generator = subgroup_generator(p, n)
        self.points = [pow(self.generator, index, p) for index in range(n)]
        self.vertices = [tuple(v) for v in combinations(range(n), j)]
        self.vertex_index = {vertex: idx for idx, vertex in enumerate(self.vertices)}
        self.locators = [
            locator_coefficients(vertex, self.points, p) for vertex in self.vertices
        ]
        self.degree = j * (n - j)
        self.neighbors = self._neighbors()

    def _neighbors(self) -> list[list[int]]:
        neighbors = []
        universe = set(range(self.n))
        for vertex in self.vertices:
            support = set(vertex)
            missing = sorted(universe - support)
            row = []
            for old in vertex:
                base = support - {old}
                for new in missing:
                    row.append(self.vertex_index[tuple(sorted(base | {new}))])
            require(len(row) == self.degree, "Johnson degree mismatch")
            neighbors.append(row)
        return neighbors

    def random_support(self, rng: random.Random) -> tuple[int, ...]:
        return tuple(sorted(rng.sample(range(self.n), self.j)))

    def random_neighbor(self, support: tuple[int, ...], rng: random.Random) -> tuple[int, ...]:
        present = set(support)
        old = rng.choice(support)
        missing = [index for index in range(self.n) if index not in present]
        new = rng.choice(missing)
        return tuple(sorted((present - {old}) | {new}))


class SampledJohnsonCase:
    """A Johnson row interface that never enumerates the vertex set."""

    def __init__(self, n: int, j: int, p: int = P, t: int = T_WINDOW) -> None:
        self.n = n
        self.j = j
        self.p = p
        self.t = t
        self.generator = subgroup_generator(p, n)
        self.points = [pow(self.generator, index, p) for index in range(n)]
        self.degree = j * (n - j)

    def random_support(self, rng: random.Random) -> tuple[int, ...]:
        return tuple(sorted(rng.sample(range(self.n), self.j)))

    def random_neighbor(self, support: tuple[int, ...], rng: random.Random) -> tuple[int, ...]:
        present = set(support)
        old = rng.choice(support)
        missing = [index for index in range(self.n) if index not in present]
        new = rng.choice(missing)
        return tuple(sorted((present - {old}) | {new}))


def delta_word(n: int, index: int) -> tuple[int, ...]:
    return tuple(1 if i == index else 0 for i in range(n))


def character_word(points: list[int], exponent: int, p: int) -> tuple[int, ...]:
    return tuple(pow(point, exponent, p) for point in points)


def normalize_projective_pair(u: tuple[int, ...], v: tuple[int, ...], p: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    data = list(u) + list(v)
    pivot = next((value for value in data if value % p), 1)
    inv = pow(pivot, -1, p)
    return (
        tuple((value * inv) % p for value in u),
        tuple((value * inv) % p for value in v),
    )


def pair_corpus(case: JohnsonCase, random_pairs: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add(pair_id: str, family: str, u: tuple[int, ...], v: tuple[int, ...], parameters: dict[str, Any]) -> None:
        u_norm, v_norm = normalize_projective_pair(u, v, case.p)
        digest = sha256_json({"u": u_norm, "v": v_norm})
        if digest in seen:
            return
        seen.add(digest)
        records.append(
            {
                "pair_id": pair_id,
                "family": family,
                "parameters": parameters,
                "u": u_norm,
                "v": v_norm,
                "pair_hash_sha256": digest,
            }
        )

    for distance in range(case.n):
        add(
            f"delta_delta_distance_{distance}",
            "delta_delta_cyclic_orbit",
            delta_word(case.n, 0),
            delta_word(case.n, distance),
            {"cyclic_distance": distance},
        )
    for exponent in range(case.n):
        add(
            f"delta_character_{exponent}",
            "delta_character_orbit",
            delta_word(case.n, 0),
            character_word(case.points, exponent, case.p),
            {"character_exponent": exponent},
        )
    for left in range(case.n):
        for right in range(left + 1, case.n):
            add(
                f"character_pair_{left}_{right}",
                "character_pair_orbit",
                character_word(case.points, left, case.p),
                character_word(case.points, right, case.p),
                {"left_character": left, "right_character": right},
            )

    rng = random.Random(20260703 + 1000 * case.n + case.j)
    for index in range(random_pairs):
        u = tuple(rng.randrange(case.p) for _ in range(case.n))
        v = tuple(rng.randrange(case.p) for _ in range(case.n))
        add(
            f"random_projective_pair_{index}",
            "deterministic_random_projective_pair",
            u,
            v,
            {"seed": 20260703 + 1000 * case.n + case.j, "index": index},
        )
    return records


def aligned_indices(case: JohnsonCase, pair: dict[str, Any]) -> list[int]:
    upto = case.j + case.t - 1
    syndromes_u = word_syndromes(pair["u"], case.points, upto, case.p)
    syndromes_v = word_syndromes(pair["v"], case.points, upto, case.p)
    return [
        index
        for index, locator in enumerate(case.locators)
        if parallel_noncontained(locator, syndromes_u, syndromes_v, case.t, case.p)
    ]


def e3_exact(case: JohnsonCase, aligned: set[int]) -> Fraction:
    if not aligned:
        return Fraction(0, 1)
    if len(aligned) == len(case.vertices):
        return Fraction(1, 1)
    active = aligned
    walk_counts: dict[int, int] = {index: 1 for index in active}
    for _ in range(3):
        next_counts = {}
        for vertex in active:
            count = sum(walk_counts.get(neighbor, 0) for neighbor in case.neighbors[vertex])
            if count:
                next_counts[vertex] = count
        walk_counts = next_counts
        if not walk_counts:
            break
    return Fraction(sum(walk_counts.values()), len(case.vertices) * case.degree**3)


def is_quotient_periodic(support: tuple[int, ...], n: int) -> bool:
    support_set = set(support)
    for shift in range(1, n):
        if shift == n:
            continue
        orbit_size = n // math.gcd(n, shift)
        if orbit_size == n:
            continue
        if {(index + shift) % n for index in support_set} == support_set:
            return True
    return False


def link_stats_exact(case: JohnsonCase, aligned: list[int], density: Fraction) -> list[dict[str, Any]]:
    if not aligned:
        return [
            {
                "r": r,
                "max_count": 0,
                "link_size": math.comb(case.n - r, case.j - r),
                "max_link_density": fraction_record(Fraction(0, 1)),
                "boost_over_global_density": None,
                "kllm_proxy_threshold": fraction_record(Fraction(0, 1)),
                "below_kllm_proxy": True,
                "max_core": [],
            }
            for r in LINK_RADII
            if r <= case.j
        ]

    if len(aligned) == len(case.vertices):
        return [
            {
                "r": r,
                "max_count": math.comb(case.n - r, case.j - r),
                "link_size": math.comb(case.n - r, case.j - r),
                "max_link_density": fraction_record(Fraction(1, 1)),
                "boost_over_global_density": fraction_record(Fraction(1, 1) / density),
                "kllm_proxy_threshold": fraction_record(Fraction(1, 1)),
                "below_kllm_proxy": True,
                "max_core": [],
            }
            for r in LINK_RADII
            if r <= case.j
        ]

    out = []
    aligned_vertices = [case.vertices[index] for index in aligned]
    for r in LINK_RADII:
        if r > case.j:
            continue
        counts: Counter[tuple[int, ...]] = Counter()
        for vertex in aligned_vertices:
            counts.update(combinations(vertex, r))
        max_core, max_count = max(counts.items(), key=lambda item: (item[1], item[0]))
        link_size = math.comb(case.n - r, case.j - r)
        max_density = Fraction(max_count, link_size)
        proxy = min(Fraction(1, 1), density * (case.n**r))
        out.append(
            {
                "r": r,
                "max_count": max_count,
                "link_size": link_size,
                "max_link_density": fraction_record(max_density),
                "boost_over_global_density": (
                    fraction_record(max_density / density) if density else None
                ),
                "paid_tangent_leak_proxy_threshold": fraction_record(
                    TANGENT_LINK_LEAK_THRESHOLD
                ),
                "above_paid_tangent_leak_proxy": max_density
                >= TANGENT_LINK_LEAK_THRESHOLD,
                "kllm_proxy_threshold": fraction_record(proxy),
                "below_kllm_proxy": max_density <= proxy,
                "max_core": list(max_core),
            }
        )
    return out


def classify_alignment(case: JohnsonCase, aligned: list[int], link_stats: list[dict[str, Any]]) -> dict[str, Any]:
    if not aligned:
        return {
            "classification": "empty",
            "post_quotient_strip": True,
            "common_core_size": 0,
            "common_hole_size": case.n,
            "all_supports_quotient_periodic": False,
        }

    supports = [set(case.vertices[index]) for index in aligned]
    common_core = set.intersection(*supports)
    common_hole = set(range(case.n)) - set.union(*supports)
    periodic_flags = [is_quotient_periodic(case.vertices[index], case.n) for index in aligned]
    density = Fraction(len(aligned), len(case.vertices))
    max_link = max(
        Fraction(row["max_link_density"]["numerator"], row["max_link_density"]["denominator"])
        for row in link_stats
    )

    if len(aligned) == len(case.vertices) or density >= Fraction(9, 10):
        classification = "paid_global_rank_one_or_degenerate"
        post_strip = False
    elif all(periodic_flags):
        classification = "paid_quotient_periodic_supports"
        post_strip = False
    elif common_core:
        classification = "fixed_core_tangent_shape"
        post_strip = True
    elif common_hole:
        classification = "fixed_hole_first_eigenspace_shape"
        post_strip = True
    elif max_link >= TANGENT_LINK_LEAK_THRESHOLD:
        classification = "post_strip_tangent_link_leak_candidate"
        post_strip = True
    elif len(aligned) <= 2 * case.n and max_link <= min(Fraction(1, 1), density * case.n):
        classification = "post_strip_sparse_global"
        post_strip = True
    else:
        classification = "post_strip_unclassified"
        post_strip = True

    return {
        "classification": classification,
        "post_quotient_strip": post_strip,
        "common_core_size": len(common_core),
        "common_hole_size": len(common_hole),
        "all_supports_quotient_periodic": all(periodic_flags),
        "some_support_quotient_periodic": any(periodic_flags),
    }


def classify_paid_global_exact(case: JohnsonCase, aligned: list[int]) -> dict[str, Any] | None:
    density = Fraction(len(aligned), len(case.vertices))
    if len(aligned) == len(case.vertices) or density >= Fraction(9, 10):
        return {
            "classification": "paid_global_rank_one_or_degenerate",
            "post_quotient_strip": False,
            "common_core_size": 0,
            "common_hole_size": 0,
            "all_supports_quotient_periodic": False,
            "some_support_quotient_periodic": False,
        }
    return None


def summarize_exact_pair(case: JohnsonCase, pair: dict[str, Any]) -> dict[str, Any]:
    aligned = aligned_indices(case, pair)
    aligned_set = set(aligned)
    density = Fraction(len(aligned), len(case.vertices))
    classification = classify_paid_global_exact(case, aligned)
    if classification is None:
        links: list[dict[str, Any]] | str = link_stats_exact(case, aligned, density)
        classification = classify_alignment(case, aligned, links)
    else:
        links = "skipped_for_paid_global_density_ge_9_over_10"
    e3 = e3_exact(case, aligned_set)
    return {
        "pair_id": pair["pair_id"],
        "family": pair["family"],
        "parameters": pair["parameters"],
        "pair_hash_sha256": pair["pair_hash_sha256"],
        "aligned_count": len(aligned),
        "vertex_count": len(case.vertices),
        "density": fraction_record(density),
        "E_3": fraction_record(e3),
        "classification": classification,
        "link_stats": links,
        "aligned_support_hash_sha256": sha256_json(aligned),
    }


def summarize_exact_case() -> dict[str, Any]:
    case = JohnsonCase(n=16, j=8)
    pairs = pair_corpus(case, N16_RANDOM_PAIRS)
    records = [summarize_exact_pair(case, pair) for pair in pairs]
    records.sort(
        key=lambda row: (
            Fraction(row["E_3"]["numerator"], row["E_3"]["denominator"]),
            row["aligned_count"],
            row["pair_id"],
        ),
        reverse=True,
    )
    post_strip = [row for row in records if row["classification"]["post_quotient_strip"]]
    top_decile_count = max(
        1,
        math.ceil(len(post_strip) * TOP_DECILE_NUMERATOR / TOP_DECILE_DENOMINATOR),
    )
    top_decile = post_strip[:top_decile_count]
    class_counts = Counter(row["classification"]["classification"] for row in records)
    top_class_counts = Counter(row["classification"]["classification"] for row in top_decile)
    link_leaks = [
        {
            "pair_id": row["pair_id"],
            "classification": row["classification"]["classification"],
            "kllm_proxy_leaking_radii": [
                link["r"] for link in row["link_stats"] if not link["below_kllm_proxy"]
            ],
            "paid_tangent_proxy_leaking_radii": [
                link["r"]
                for link in row["link_stats"]
                if link.get("above_paid_tangent_leak_proxy")
            ],
        }
        for row in post_strip
        if isinstance(row["link_stats"], list)
        if any(
            not link["below_kllm_proxy"]
            for link in row["link_stats"]
        )
        or row["classification"]["classification"]
        == "post_strip_tangent_link_leak_candidate"
    ]
    strict_top_unclassified = [
        row["pair_id"]
        for row in top_decile
        if row["classification"]["classification"]
        not in {"fixed_core_tangent_shape", "fixed_hole_first_eigenspace_shape"}
    ]
    exact_payload = {
        "case": {
            "field": "F_97",
            "n": case.n,
            "j": case.j,
            "window_t": case.t,
            "domain_generator": case.generator,
            "vertex_count": len(case.vertices),
            "johnson_degree": case.degree,
        },
        "pair_corpus": {
            "pair_count": len(records),
            "families": dict(Counter(row["family"] for row in records)),
            "random_pair_count": N16_RANDOM_PAIRS,
            "scope": (
                "exact over this finite actual-word-pair corpus; not exhaustive "
                "over all projective pairs in F_97^{2n}"
            ),
        },
        "summary": {
            "classification_counts": dict(class_counts),
            "post_strip_record_count": len(post_strip),
            "top_decile_count": top_decile_count,
            "top_decile_classification_counts": dict(top_class_counts),
            "post_strip_kllm_proxy_link_leak_count": sum(
                1
                for row in post_strip
                if isinstance(row["link_stats"], list)
                and any(not link["below_kllm_proxy"] for link in row["link_stats"])
            ),
            "post_strip_paid_tangent_link_leak_candidate_count": sum(
                1
                for row in post_strip
                if row["classification"]["classification"]
                == "post_strip_tangent_link_leak_candidate"
            ),
            "strict_fixed_core_hole_top_decile_holds": not strict_top_unclassified,
            "strict_fixed_core_hole_top_decile_counterexamples": strict_top_unclassified[:20],
            "interpretation": (
                "The strict 'top actual sets are only fixed-core/fixed-hole' reading "
                "fails for this t=2 actual-pair corpus.  Several delta-character "
                "post-strip records are not exactly fixed-core/fixed-hole and have "
                "near-full density on fixed-core links, so they are reported as "
                "paid-tangent leak candidates or an incomplete strip/taxonomy."
            ),
        },
        "top_records": records[:TOP_RECORD_LIMIT],
        "top_post_strip_records": post_strip[:TOP_RECORD_LIMIT],
        "top_decile_post_strip_records": top_decile,
        "link_leaks": link_leaks[:TOP_RECORD_LIMIT],
        "all_record_digest_sha256": sha256_json(records),
    }
    return exact_payload


def estimate_sampled_pair(case: JohnsonCase, pair: dict[str, Any]) -> dict[str, Any]:
    rng_seed = int(hashlib.sha256(pair["pair_hash_sha256"].encode("utf-8")).hexdigest()[:12], 16)
    rng = random.Random(rng_seed)
    upto = case.j + case.t - 1
    syndromes_u = word_syndromes(pair["u"], case.points, upto, case.p)
    syndromes_v = word_syndromes(pair["v"], case.points, upto, case.p)

    def aligned_support(support: tuple[int, ...]) -> bool:
        locator = locator_coefficients(support, case.points, case.p)
        return parallel_noncontained(locator, syndromes_u, syndromes_v, case.t, case.p)

    aligned_supports = []
    link_observed: dict[int, Counter[tuple[int, ...]]] = {r: Counter() for r in LINK_RADII}
    link_totals: dict[int, Counter[tuple[int, ...]]] = {r: Counter() for r in LINK_RADII}
    for _ in range(N32_SUPPORT_SAMPLES):
        support = case.random_support(rng)
        is_aligned = aligned_support(support)
        if is_aligned:
            aligned_supports.append(support)
        for r in LINK_RADII:
            for core in combinations(support, r):
                link_totals[r][core] += 1
                if is_aligned:
                    link_observed[r][core] += 1

    walk_hits = 0
    for _ in range(N32_WALK_SAMPLES):
        support = case.random_support(rng)
        ok = aligned_support(support)
        for _step in range(3):
            support = case.random_neighbor(support, rng)
            ok = ok and aligned_support(support)
        if ok:
            walk_hits += 1

    density = Fraction(len(aligned_supports), N32_SUPPORT_SAMPLES)
    link_rows = []
    for r in LINK_RADII:
        best_core: tuple[int, ...] = ()
        best_density = Fraction(0, 1)
        best_count = 0
        best_total = 0
        for core, total in link_totals[r].items():
            count = link_observed[r][core]
            value = Fraction(count, total)
            if value > best_density:
                best_core = core
                best_density = value
                best_count = count
                best_total = total
        proxy = min(Fraction(1, 1), density * (case.n**r))
        link_rows.append(
            {
                "r": r,
                "max_observed_core": list(best_core),
                "aligned_count_on_observed_core": best_count,
                "sample_count_on_observed_core": best_total,
                "max_observed_link_density": fraction_record(best_density),
                "kllm_proxy_threshold": fraction_record(proxy),
                "below_kllm_proxy": best_density <= proxy,
            }
        )

    return {
        "pair_id": pair["pair_id"],
        "family": pair["family"],
        "pair_hash_sha256": pair["pair_hash_sha256"],
        "support_samples": N32_SUPPORT_SAMPLES,
        "walk_samples": N32_WALK_SAMPLES,
        "aligned_support_sample_count": len(aligned_supports),
        "estimated_density": fraction_record(density),
        "estimated_E_3": fraction_record(Fraction(walk_hits, N32_WALK_SAMPLES)),
        "observed_link_stats": link_rows,
        "observed_kllm_proxy_link_leak": any(
            not row["below_kllm_proxy"] for row in link_rows
        ),
        "aligned_support_sample_hash_sha256": sha256_json(aligned_supports),
    }


def summarize_sampled_case() -> dict[str, Any]:
    case = SampledJohnsonCase(n=32, j=16)
    pairs = pair_corpus(case, N32_RANDOM_PAIRS)
    # Keep all structured small families plus the requested random sample, but
    # cap the character-character block to a deterministic prefix for runtime.
    structured = [
        pair
        for pair in pairs
        if pair["family"] in {"delta_delta_cyclic_orbit", "delta_character_orbit"}
    ]
    character_prefix = [
        pair for pair in pairs if pair["family"] == "character_pair_orbit"
    ][:16]
    random_block = [
        pair for pair in pairs if pair["family"] == "deterministic_random_projective_pair"
    ]
    selected = structured + character_prefix + random_block
    records = [estimate_sampled_pair(case, pair) for pair in selected]
    records.sort(
        key=lambda row: (
            Fraction(row["estimated_E_3"]["numerator"], row["estimated_E_3"]["denominator"]),
            row["aligned_support_sample_count"],
            row["pair_id"],
        ),
        reverse=True,
    )
    return {
        "case": {
            "field": "F_97",
            "n": case.n,
            "j": case.j,
            "window_t": case.t,
            "domain_generator": case.generator,
            "johnson_degree": case.degree,
        },
        "sampling": {
            "pair_count": len(records),
            "support_samples_per_pair": N32_SUPPORT_SAMPLES,
            "walk_samples_per_pair": N32_WALK_SAMPLES,
            "families": dict(Counter(row["family"] for row in records)),
        },
        "summary": {
            "observed_kllm_proxy_link_leak_count": sum(
                1 for row in records if row["observed_kllm_proxy_link_leak"]
            ),
            "nonzero_estimated_E_3_count": sum(
                1 for row in records if row["estimated_E_3"]["numerator"] != 0
            ),
            "interpretation": (
                "Monte Carlo telemetry only.  It exercises the same actual-pair "
                "predicate at n=32 and records whether sampled fixed-core links "
                "violate the polynomial globalness proxy."
            ),
        },
        "top_records": records[:TOP_RECORD_LIMIT],
        "all_record_digest_sha256": sha256_json(records),
    }


def build_certificate() -> dict[str, Any]:
    exact = summarize_exact_case()
    sampled = summarize_sampled_case()
    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": "EXPERIMENTAL_EVIDENCE / EXACT_N16_CORPUS / SAMPLED_N32",
        "evidence_ids": ["E18", "E19"],
        "targets": ["c_xr_content", "xr_inverse", "xr_globalness_from_ledger"],
        "alignment_predicate": (
            "A_{u,v}={T in D_j : H_u l_T parallel H_v l_T and H_v l_T != 0}"
        ),
        "energy": "E_3^J(A)=Pr[T_0,T_1,T_2,T_3 in A] for a 3-step Johnson walk",
        "globalness_proxy": {
            "link_radii": list(LINK_RADII),
            "measured_quantity": "max fixed-core link density at each radius r",
            "paid_tangent_leak_proxy": "flag any non-fixed-core/hole post-strip row with max link density >= 9/10",
            "proxy_threshold": "min(1, n^r * global_density(A))",
            "reason_for_proxy": (
                "E20/QX.10 has not yet pinned the imported KLLM constants in this "
                "repository.  The polynomial proxy saturates on dense toy sets, so "
                "the paid-tangent leak flag is reported separately."
            ),
        },
        "exact_n16": exact,
        "sampled_n32": sampled,
        "overall_interpretation": {
            "e18": (
                "The scanner now works on genuine actual-pair alignment sets.  In "
                "the exact n=16 corpus, high raw E_3 comes from paid global/"
                "degenerate structures, but the post-strip top decile contains "
                "delta-character link-dense rows outside the fixed-core/fixed-hole "
                "classifier.  This is a falsifier candidate for the narrow C_XR "
                "content statement at t=2."
            ),
            "e19": (
                "The exact n=16 corpus contains paid-tangent link-leak candidates.  "
                "The polynomial KLLM proxy itself does not fire because it saturates "
                "on dense toy sets; the paid-ledger/taxonomy issue is therefore the "
                "actionable E19 readout."
            ),
        },
        "nonclaims": [
            "does not enumerate all projective word pairs over F_97",
            "does not prove c_xr_content or xr_inverse",
            "does not import or prove the KLLM global hypercontractivity theorem",
            "does not replace the E20 KMS/KLLM loss-exponent table",
            "n=32 data are Monte Carlo telemetry, not exhaustive",
        ],
    }
    payload["payload_sha256"] = sha256_json(payload)
    return payload


def check_certificate(path: Path, expected: dict[str, Any]) -> None:
    actual = json.loads(path.read_text(encoding="utf-8"))
    if actual != expected:
        raise AssertionError(f"certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    exact = certificate["exact_n16"]["summary"]
    sampled = certificate["sampled_n32"]["summary"]
    print("XR pair-orbit globalness evidence")
    print(f"status: {certificate['status']}")
    print(
        "n=16 exact corpus: post-strip={post_strip_record_count}, "
        "top-decile={top_decile_count}, KLLM-proxy leaks={post_strip_kllm_proxy_link_leak_count}, "
        "paid-tangent leak candidates={post_strip_paid_tangent_link_leak_candidate_count}".format(
            **exact
        )
    )
    print(
        "n=16 strict fixed-core/hole top-decile holds:",
        exact["strict_fixed_core_hole_top_decile_holds"],
    )
    print(
        "n=32 sampled: proxy leaks={observed_kllm_proxy_link_leak_count}, "
        "nonzero E3 samples={nonzero_estimated_E_3_count}".format(**sampled)
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        nargs="?",
        const=OUTPUT,
        type=Path,
        help="write deterministic certificate JSON, optionally to PATH",
    )
    parser.add_argument(
        "--check",
        nargs="?",
        const=OUTPUT,
        type=Path,
        help="check deterministic certificate JSON, optionally at PATH",
    )
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check, certificate)
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
