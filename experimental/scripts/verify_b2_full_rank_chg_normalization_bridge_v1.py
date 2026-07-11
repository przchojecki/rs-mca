#!/usr/bin/env python3
"""Finite exact checks for the full-rank CHG normalization bridge.

The verifier checks rank duality, determinant reciprocity, the -4 inverse
coordinate change, complementary projector/phase identity, explicit z_Z(v),
termwise Gaussian correspondence, centering, Fourier pairing, Salie
factorization, and the deployed exponent arithmetic.

Status: PROVED FULL-RANK NORMALIZATION BRIDGE / OPEN SIGNED ESTIMATE.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import random
import tempfile
from pathlib import Path
from typing import Any, Sequence

import verify_b2_twisted_hankel_transform_v1 as core


THEOREM_ID = "b2-full-rank-chg-normalization-bridge-v1"
STATUS = "PROVED FULL-RANK NORMALIZATION BRIDGE / OPEN SIGNED ESTIMATE"
SEED = 20260711
CERT = Path(
    "experimental/data/certificates/b2-twisted-hankel-transform-v1/"
    "b2_full_rank_chg_normalization_bridge_v1.json"
)
NOTE = Path("experimental/notes/roadmaps/b2_full_rank_chg_normalization_bridge_v1.md")
TRANSFORM_NOTE = Path("experimental/notes/roadmaps/b2_twisted_hankel_transform_v1.md")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def normalize(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 12)
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]
    return value


def payload_hash(payload: dict[str, Any]) -> str:
    clean = copy.deepcopy(payload)
    clean.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(clean, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def transpose(matrix: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(matrix[row][column] for row in range(len(matrix))) for column in range(len(matrix[0])))


def matmul(
    left: Sequence[Sequence[int]], right: Sequence[Sequence[int]], p: int
) -> tuple[tuple[int, ...], ...]:
    right_t = transpose(right)
    return tuple(
        tuple(sum(a * b for a, b in zip(row, column)) % p for column in right_t)
        for row in left
    )


def matadd(
    left: Sequence[Sequence[int]], right: Sequence[Sequence[int]], p: int, sign: int = 1
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple((left[i][j] + sign * right[i][j]) % p for j in range(len(left[0])))
        for i in range(len(left))
    )


def diagonal(values: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(value if row == column else 0 for column in range(len(values)))
        for row, value in enumerate(values)
    )


def identity(size: int) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(1 if row == column else 0 for column in range(size)) for row in range(size))


def matrix_scale(matrix: Sequence[Sequence[int]], scalar: int, p: int) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(scalar * value % p for value in row) for row in matrix)


def matrix_vector(
    matrix: Sequence[Sequence[int]], vector: Sequence[int], p: int
) -> tuple[int, ...]:
    return tuple(sum(a * b for a, b in zip(row, vector)) % p for row in matrix)


def vector_matrix_vector(
    vector: Sequence[int], matrix: Sequence[Sequence[int]], p: int
) -> int:
    return sum(a * b for a, b in zip(vector, matrix_vector(matrix, vector, p))) % p


def product(values: Sequence[int], p: int) -> int:
    result = 1
    for value in values:
        result = result * value % p
    return result


def l_z_value(Z: Sequence[int], point: int, p: int) -> int:
    return product(tuple((point - z) % p for z in Z), p)


def locator_coefficients(points: Sequence[int], p: int) -> tuple[int, ...]:
    return core.locator(points, p)


def bridge_data(
    p: int,
    n: int,
    w: int,
    m: int,
    Z: Sequence[int],
    xi: Sequence[int],
    v: Sequence[int],
) -> dict[str, Any]:
    H = core.roots_of_unity(p, n)
    Z_set = set(Z)
    T = tuple(point for point in H if point not in Z_set)
    c = w + 1
    d = n - c
    q = len(T) - d
    if q <= 0:
        raise ValueError("bridge_data requires q>=1")
    if len(xi) != len(T) or any(value % p == 0 for value in xi):
        raise ValueError("xi must be nonzero on T")

    inverse_n = pow(n, -1, p)
    inverse_four = pow(4, -1, p)
    kappa = tuple((l_z_value(Z, point, p) * inverse_n) ** 2 % p for point in T)
    lam = tuple((-4 * kappa[index] * pow(xi[index], -1, p)) % p for index in range(len(T)))
    d_inv = diagonal(tuple(pow(value, -1, p) for value in lam))
    d_lam = diagonal(lam)

    E = tuple(tuple(pow(point, exponent, p) for exponent in range(1, d + 1)) for point in T)
    W = tuple(
        tuple(l_z_value(Z, point, p) * inverse_n * pow(point, r, p) % p for r in range(q))
        for point in T
    )
    if matmul(transpose(E), W, p) != tuple(tuple(0 for _ in range(q)) for _ in range(d)):
        raise AssertionError("E^T W != 0")

    A = matmul(matmul(transpose(E), d_lam, p), E, p)
    B0 = matmul(matmul(transpose(W), d_inv, p), W, p)
    Bz = matrix_scale(B0, -4, p)
    Bz_moment = tuple(
        tuple(sum(xi[index] * pow(T[index], r + u, p) for index in range(len(T))) % p for u in range(q))
        for r in range(q)
    )
    if Bz != Bz_moment:
        raise AssertionError("-4 complementary Hankel normalization failed")

    det_a = core.matrix_det(A, p)
    det_b0 = core.matrix_det(B0, p)
    det_bz = core.matrix_det(Bz, p)
    if not det_a or not det_b0 or not det_bz:
        raise ValueError("sample is not full rank")

    U = tuple(
        tuple(E[row]) + tuple(matmul(d_inv, W, p)[row])
        for row in range(len(T))
    )
    det_u = core.matrix_det(U, p)
    determinant_identity = det_a * det_b0 % p == det_u * det_u * product(lam, p) % p
    if not determinant_identity:
        raise AssertionError("determinant identity failed")
    character_identity = (
        core.legendre(det_a, p) * core.legendre(det_bz, p)
        == core.legendre(pow(-1, d, p), p)
        * math.prod(core.legendre(value, p) for value in xi)
    )
    if not character_identity:
        raise AssertionError("determinant character reciprocity failed")

    fixed_values = []
    h_values = []
    for point in T:
        rv = (m + sum(v[j - 1] * pow(point, -j, p) for j in range(1, w + 1))) * inverse_n % p
        fixed_values.append(rv)
        h_values.append((2 * rv - 1) % p)
    h = tuple(h_values)
    ell = matrix_vector(matmul(transpose(E), d_lam, p), h, p)
    gamma = inverse_four * (
        sum(lam[index] * (h[index] * h[index] - 1) for index in range(len(T))) % p
    ) % p
    z_direct = matrix_vector(transpose(W), h, p)

    lz_coeff = locator_coefficients(Z, p)
    beta = ((m - n * pow(2, -1, p)) % p,) + tuple(v)
    z_explicit = tuple(
        2
        * inverse_n
        * sum(
            lz_coeff[k] * beta[k + r]
            for k in range(len(lz_coeff))
            if k + r < len(beta)
        )
        % p
        for r in range(q)
    )
    if z_direct != z_explicit:
        raise AssertionError(("explicit z formula failed", z_direct, z_explicit))

    a_inv = core.matrix_inverse(A, p)
    b0_inv = core.matrix_inverse(B0, p)
    bz_inv = core.matrix_inverse(Bz, p)
    lhs_projector = matadd(
        d_lam,
        matmul(matmul(matmul(d_lam, E, p), a_inv, p), matmul(transpose(E), d_lam, p), p),
        p,
        sign=-1,
    )
    rhs_projector = matmul(matmul(W, b0_inv, p), transpose(W), p)
    if lhs_projector != rhs_projector:
        raise AssertionError("complementary projector identity failed")

    phase_left = (gamma - inverse_four * vector_matrix_vector(ell, a_inv, p)) % p
    phase_right = (
        sum(kappa[index] * pow(xi[index], -1, p) for index in range(len(T)))
        - vector_matrix_vector(z_direct, bz_inv, p)
    ) % p
    if phase_left != phase_right:
        raise AssertionError(("phase identity failed", phase_left, phase_right))

    gauss_power = core.cyc_pow(core.gauss_cyclotomic(p), d)
    g_left = core.cyc_shift(core.cyc_scale(gauss_power, core.legendre(det_a, p)), phase_left)
    right_character = (
        core.legendre(pow(-1, d, p), p)
        * math.prod(core.legendre(value, p) for value in xi)
        * core.legendre(det_bz, p)
    )
    g_right = core.cyc_shift(core.cyc_scale(gauss_power, right_character), phase_right)
    if not core.cyc_equal(g_left, g_right):
        raise AssertionError("termwise bridge failed")

    return {
        "T": T,
        "Z": tuple(Z),
        "q": q,
        "d": d,
        "xi": tuple(xi),
        "lambda": lam,
        "A": A,
        "B0": B0,
        "Bz": Bz,
        "z": z_direct,
        "phase": phase_left,
        "ell": ell,
        "gamma": gamma,
        "kappa": kappa,
        "determinant_identity": determinant_identity,
        "character_identity": character_identity,
        "termwise_exact": True,
    }


def direct_gaussian_sum(
    p: int, A: Sequence[Sequence[int]], ell: Sequence[int], gamma: int
) -> tuple[int, ...]:
    total = core.cyc_zero(p)
    for u in core.vectors(p, len(ell)):
        exponent = (
            vector_matrix_vector(u, A, p)
            + sum(ell[index] * u[index] for index in range(len(ell)))
            + gamma
        ) % p
        total = core.cyc_add(total, core.cyc_monomial(p, exponent))
    return total


def f_value_vector(p: int, B: Sequence[Sequence[int]], z: Sequence[int]) -> tuple[int, ...]:
    determinant = core.matrix_det(B, p)
    if not determinant:
        return core.cyc_zero(p)
    inverse = core.matrix_inverse(B, p)
    phase = -vector_matrix_vector(z, inverse, p)
    return core.cyc_monomial(p, phase, core.legendre(determinant, p))


def check_centering(
    p: int, n: int, w: int, m: int, row: dict[str, Any]
) -> dict[str, Any]:
    q = row["q"]
    Z = row["Z"]
    B = row["Bz"]
    xi = row["xi"]
    summed = core.cyc_zero(p)
    for eta in core.vectors(p, w):
        eta_row = bridge_data(p, n, w, m, Z, xi, eta)
        summed = core.cyc_add(summed, f_value_vector(p, B, eta_row["z"]))
    gauss_q = core.cyc_pow(core.gauss_cyclotomic(p), q)
    left = core.cyc_mul(gauss_q, summed)
    if Z:
        right = core.cyc_monomial(p, 0, p**w)
        kind = "non-full-support constant center"
    else:
        a_m = (2 * m - n) * pow(n, -1, p) % p
        b0 = B[0][0]
        scalar_sum = core.cyc_zero(p)
        for t in range(p):
            scalar_sum = core.cyc_add(
                scalar_sum, core.cyc_monomial(p, b0 * t * t + 2 * a_m * t)
            )
        right = core.cyc_scale(scalar_sum, p**w)
        kind = "full-support scalar line center"
    if not core.cyc_equal(left, right):
        raise AssertionError(("centering identity failed", kind))
    return {"kind": kind, "exact": True}


def salie_factorization_check(
    p: int, row: dict[str, Any], P: Sequence[int]
) -> bool:
    T = row["T"]
    kappa = row["kappa"]
    q = row["q"]
    direct = core.cyc_zero(p)
    for xi in itertools.product(range(1, p), repeat=len(T)):
        moments = tuple(
            sum(xi[index] * pow(T[index], degree, p) for index in range(len(T))) % p
            for degree in range(2 * q - 1)
        )
        exponent = (
            core.dot(P, moments, p)
            + sum(kappa[index] * pow(xi[index], -1, p) for index in range(len(T)))
        ) % p
        coefficient = math.prod(core.legendre(value, p) for value in xi)
        direct = core.cyc_add(direct, core.cyc_monomial(p, exponent, coefficient))

    factored = core.cyc_monomial(p, 0)
    for index, point in enumerate(T):
        local = core.cyc_zero(p)
        p_at_a = sum(P[degree] * pow(point, degree, p) for degree in range(len(P))) % p
        for value in range(1, p):
            exponent = kappa[index] * pow(value, -1, p) + p_at_a * value
            local = core.cyc_add(local, core.cyc_monomial(p, exponent, core.legendre(value, p)))
        factored = core.cyc_mul(factored, local)
    if not core.cyc_equal(direct, factored):
        raise AssertionError("Salie product factorization failed")
    return True


def sample_full_rank_row(
    p: int,
    n: int,
    w: int,
    m: int,
    Z: Sequence[int],
    v: Sequence[int],
    rng: random.Random,
) -> dict[str, Any]:
    H = core.roots_of_unity(p, n)
    T = tuple(point for point in H if point not in set(Z))
    for _ in range(5000):
        xi = tuple(rng.randrange(1, p) for _ in T)
        try:
            return bridge_data(p, n, w, m, Z, xi, v)
        except ValueError:
            continue
    raise AssertionError("failed to sample a full-rank row")


def check_case(p: int, n: int, w: int, m: int, rng: random.Random) -> dict[str, Any]:
    H = core.roots_of_unity(p, n)
    c = w + 1
    rows = []
    center_rows = []
    endpoint_rows = []
    direct_gaussian_rows = 0
    salie_rows = 0
    salie_q: set[int] = set()
    for q in range(1, c + 1):
        z_size = c - q
        z_choices = list(itertools.combinations(H, z_size))
        selected_z = z_choices if len(z_choices) <= 3 else rng.sample(z_choices, 3)
        for Z in selected_z:
            for v in [(0,) * w, tuple(rng.randrange(p) for _ in range(w))]:
                row = sample_full_rank_row(p, n, w, m, Z, v, rng)
                rows.append(row)
                if v == (0,) * w:
                    endpoint_supported = all(value == 0 for value in row["z"][1:])
                    beta_zero = (m - n * pow(2, -1, p)) % p == 0
                    scalar_condition = row["z"][0] == 0 if beta_zero else row["z"][0] != 0
                    if not endpoint_supported or not scalar_condition:
                        raise AssertionError(("zero-fiber endpoint identification failed", row["z"], Z))
                    endpoint_rows.append(
                        {
                            "Z_size": len(Z),
                            "q": q,
                            "z": list(row["z"]),
                            "classification": "balanced zero twist" if beta_zero else "nonzero endpoint twist",
                        }
                    )
                center_rows.append(check_centering(p, n, w, m, row))

                if direct_gaussian_rows < 4:
                    A = row["A"]
                    d = row["d"]
                    det_a = core.matrix_det(A, p)
                    gauss_value = core.cyc_shift(
                        core.cyc_scale(core.cyc_pow(core.gauss_cyclotomic(p), d), core.legendre(det_a, p)),
                        row["phase"],
                    )
                    direct_value = direct_gaussian_sum(p, A, row["ell"], row["gamma"])
                    if not core.cyc_equal(direct_value, gauss_value):
                        raise AssertionError("direct Gaussian sum mismatch")
                    direct_gaussian_rows += 1

                if q not in salie_q and len(row["T"]) <= 6:
                    P = tuple(rng.randrange(p) for _ in range(2 * q - 1))
                    salie_factorization_check(p, row, P)
                    salie_rows += 1
                    salie_q.add(q)

    return {
        "parameters": {"p": p, "n": n, "w": w, "m": m, "c": c, "d": n - c},
        "full_rank_bridge_rows": len(rows),
        "determinant_phase_termwise_mismatches": 0,
        "direct_gaussian_rows": direct_gaussian_rows,
        "direct_gaussian_mismatches": 0,
        "centering_rows": len(center_rows),
        "centering_mismatches": 0,
        "zero_fiber_endpoint_rows": endpoint_rows,
        "zero_fiber_endpoint_mismatches": 0,
        "salie_factorization_rows": salie_rows,
        "salie_factorization_mismatches": 0,
    }


def deployed_arithmetic() -> dict[str, Any]:
    p = 2130706433
    n = 2097152
    c = 67472
    d = n - c
    m = n // 2 - c
    target_t = n + 2 - c // 2
    target_h = n // 2 + 2
    checks = {
        "p_mod_4_is_1": p % 4 == 1,
        "d_even": d % 2 == 0,
        "d": d == 2029680,
        "m": m == 981104,
        "gauss_prefactor_exponent": d // 2 == 1014840,
        "T_target_exponent": target_t == 2063418,
        "H_target_exponent": target_h == 1048578,
        "normalization_equivalence": target_t - d // 2 == target_h,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    return {
        "p": p,
        "n": n,
        "c": c,
        "d": d,
        "m": m,
        "beta_0": -c,
        "a_m": f"-{2*c}/{n}",
        "T_d_prefactor": "p^1014840",
        "T_d_target": "p^2063418",
        "H_d_target": "p^1048578",
        "checks": checks,
    }


def note_contract(root: Path) -> dict[str, bool]:
    note = (root / NOTE).read_text(encoding="utf-8")
    transform = (root / TRANSFORM_NOTE).read_text(encoding="utf-8")
    checks = {
        "status": "FULL-RANK CHG NORMALIZATION BRIDGE: PROVED" in note,
        "rank_bridge": "rank A_lambda=d iff det B^0_(Z,lambda)!=0" in note,
        "minus_four": "xi_a=-4 kappa_(Z,a)/lambda_a" in note,
        "z_formula": "z_(Z,r)(v)=(2/n)" in note,
        "endpoint_corollary": "DEPLOYED ZERO-FIBER ENDPOINT IDENTIFICATION: PROVED" in note
        and "balanced `m=n/2` zero-twist exception" in note,
        "centering_split": "non-full-support center" in note and "full-support center" in note,
        "pairing_guard": "not the matrix trace pairing" in note,
        "salie": "Salie" in note,
        "normalization": "|H_d(v)| <= p^(n/2+2)" in note,
        "signed_estimate_open": "SIGNED HANKEL--SALIE ESTIMATE: OPEN" in note,
        "transform_note_consumes_bridge": "FULL-RANK CHG NORMALIZATION BRIDGE: PROVED" in transform,
    }
    if not all(checks.values()):
        raise AssertionError({key: value for key, value in checks.items() if not value})
    return checks


def build_payload(root: Path) -> dict[str, Any]:
    rng = random.Random(SEED)
    payload: dict[str, Any] = {
        "theorem_id": THEOREM_ID,
        "status": STATUS,
        "seed": SEED,
        "toy_cases": [
            check_case(7, 6, 1, 3, rng),
            check_case(11, 5, 1, 2, rng),
        ],
        "deployed_arithmetic": deployed_arithmetic(),
        "note_contract": note_contract(root),
        "claims": [
            "full-rank complementary Hankel rank and determinant bridge",
            "canonical -4 inverse-variable normalization",
            "explicit z_Z(v) and deployed zero-fiber endpoint identification",
            "exact non-full and full-support centering",
            "coefficient Fourier pairing and Salie factorization",
            "T_d=chi((-1)^d) g^d H_d normalization",
        ],
        "nonclaims": [
            "signed Hankel-Salie aggregate estimate",
            "lower-rank pseudodeterminant strata",
            "N(0) <= n^3 or max_v N(v) <= n^3",
            "LS or SV* closure",
        ],
    }
    payload = normalize(payload)
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def validate(actual: dict[str, Any], expected: dict[str, Any]) -> None:
    if actual.get("payload_sha256") != payload_hash(actual):
        raise AssertionError("payload hash mismatch")
    if normalize(actual) != normalize(expected):
        raise AssertionError("certificate does not match recomputed bridge checks")


def write_payload(root: Path, payload: dict[str, Any]) -> None:
    path = root / CERT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def tamper_selftest(root: Path, expected: dict[str, Any]) -> int:
    source = json.loads((root / CERT).read_text(encoding="utf-8"))
    mutations = []
    changed = copy.deepcopy(source)
    changed["status"] = "PROVED SIGNED ESTIMATE"
    mutations.append(changed)
    changed = copy.deepcopy(source)
    changed["toy_cases"][0]["zero_fiber_endpoint_mismatches"] = 1
    mutations.append(changed)
    changed = copy.deepcopy(source)
    changed["deployed_arithmetic"]["H_d_target"] = "p^1048577"
    mutations.append(changed)
    changed = copy.deepcopy(source)
    changed["nonclaims"] = []
    mutations.append(changed)
    changed = copy.deepcopy(source)
    changed["payload_sha256"] = "0" * 64
    mutations.append(changed)

    rejected = 0
    with tempfile.TemporaryDirectory() as directory:
        for index, mutation in enumerate(mutations):
            path = Path(directory) / f"mutation_{index}.json"
            path.write_text(json.dumps(mutation), encoding="utf-8")
            try:
                validate(json.loads(path.read_text(encoding="utf-8")), expected)
            except AssertionError:
                rejected += 1
    if rejected != len(mutations):
        raise AssertionError("tamper self-test failed")
    return rejected


def print_summary(payload: dict[str, Any]) -> None:
    print(f"theorem_id: {payload['theorem_id']}")
    print(f"status: {payload['status']}")
    for row in payload["toy_cases"]:
        parameters = row["parameters"]
        print(
            "toy: "
            f"p={parameters['p']} n={parameters['n']} rows={row['full_rank_bridge_rows']} "
            f"endpoint_mismatches={row['zero_fiber_endpoint_mismatches']} "
            f"centering_mismatches={row['centering_mismatches']}"
        )
    arithmetic = payload["deployed_arithmetic"]
    print(
        "deployed: "
        f"T_d={arithmetic['T_d_prefactor']} H_d, "
        f"target={arithmetic['H_d_target']}"
    )
    print("result: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if not (args.write or args.check or args.tamper_selftest):
        args.check = True
    root = repo_root()
    expected = build_payload(root)
    if args.write:
        write_payload(root, expected)
        print(f"wrote: {CERT.as_posix()}")
    if args.check:
        actual = json.loads((root / CERT).read_text(encoding="utf-8"))
        validate(actual, expected)
    if args.tamper_selftest:
        print(f"tamper_mutations_rejected: {tamper_selftest(root, expected)}")
    print_summary(expected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
