#!/usr/bin/env sage
"""Independent Sage replay of the maximal M31 rank-seven route cut."""

import hashlib
import json
from collections import deque
from functools import lru_cache
from math import comb, isqrt


def canonical(value):
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
            default=int,
        )
        + "\n"
    ).encode("ascii")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


p = 2^31 - 1
n = 2^21
K = 2^20
a = 1116023
R0 = n - a
w = a - K
B_star = 2^24 - 1
shallow_L = B_star - 1001282
g = 354972
d = g - w
q0 = 26144
h0 = g - q0


def B6(Q):
    return comb(R0 - g + w + 6, 6) // comb(w - Q + 6, 6)


def Hcap(Q):
    return R0*B6(Q) // (g - Q)


def Phi(Q):
    inner = comb(R0 - g + w + 5, 5) // comb(w - Q + 5, 5)
    return R0*inner // (g - Q)


def Fcap(q):
    c = min(q, w)
    t = max(q, w)
    inner = comb(R0 - g + q + w + 5, 5) // comb(t + 5, 5)
    return R0*inner // (g - c)


def two_stage(Q):
    v = w - Q
    A_gap = R0 - d
    caps = [1]
    nus = [-1]
    for r in range(1, 7):
        B = comb(A_gap + r - 1, r - 1) // comb(v + r - 1, r - 1)
        best = -1
        best_nu = -1
        for nu in range(r, d):
            C = (A_gap + nu)*B // (v + nu)
            den = (v + nu)^2 - (A_gap + nu)*(nu - 1)
            candidate = C
            if den > 0:
                J = (A_gap + nu)*(v + 1) // den
                candidate = min(C, J)
            if candidate > best:
                best = candidate
                best_nu = nu
        caps.append(best)
        nus.append(best_nu)
    M = max(caps)
    return M, caps.index(M), nus[caps.index(M)], caps, nus, R0*M // (g - Q)


def generic_cap(rank, dimension, excess):
    A_gap = R0 - d
    B = comb(A_gap + rank - 1, rank - 1) // comb(
        excess + rank - 1, rank - 1
    )
    value = (A_gap + dimension)*B // (excess + dimension)
    den = (excess + dimension)^2 - (A_gap + dimension)*(dimension - 1)
    if den > 0:
        value = min(value, (A_gap + dimension)*(excess + 1) // den)
    return value


def recursive_arrays(Q, max_rank=7):
    excess = w - Q
    A_gap = R0 - d
    arrays = {}
    base = [0]*(d + 1)
    for dimension in range(1, d + 1):
        base[dimension] = (A_gap + dimension) // (excess + dimension)
    arrays[1] = base
    traces = []
    for rank in range(2, max_rank + 1):
        child = arrays[rank - 1]
        U = max(child[rank - 1:])
        U_arg = next(
            dimension
            for dimension in range(rank - 1, d + 1)
            if child[dimension] == U
        )
        current = list(child)
        exact = [0]*(d + 1)
        window = deque()
        for dimension in range(rank - 1, d + 1):
            added = dimension - 1
            if added >= rank - 1:
                while window and child[window[-1]] <= child[added]:
                    window.pop()
                window.append(added)
            lower = dimension - (dimension - 1) // (rank - 1)
            while window and window[0] < lower:
                window.popleft()
            if dimension < rank:
                continue
            two_tier = (
                (dimension - 1)*U + (A_gap + 1)*child[window[0]]
            ) // (excess + dimension)
            exact[dimension] = min(
                two_tier, generic_cap(rank, dimension, excess)
            )
            current[dimension] = max(child[dimension], exact[dimension])
        assert min(
            exact[dimension] - child[dimension]
            for dimension in range(rank, d + 1)
        ) >= 0
        arrays[rank] = current
        traces.append(
            (
                rank,
                U,
                U_arg,
                max(current),
                current.index(max(current)),
                exact[d],
                current[d],
            )
        )
    return arrays, traces


def coupled_rank7(Q):
    arrays, traces = recursive_arrays(Q, 6)
    child = arrays[6]
    D_top = d - 1
    largest = d - 6
    f = [0] + [child[d - size] for size in range(1, largest + 1)]
    prefix = [0]*(largest + 1)
    prefix_arg = [0]*(largest + 1)
    for size in range(1, largest + 1):
        if f[size] > prefix[size - 1]:
            prefix[size] = f[size]
            prefix_arg[size] = size
        else:
            prefix[size] = prefix[size - 1]
            prefix_arg[size] = prefix_arg[size - 1]
    best = None
    for size in range(1, largest + 1):
        B = D_top - size
        u = min(size, B - 4)
        b = min(size, B // 5)
        if u < 1 or b < 1:
            continue
        numerator = (
            size*f[size] + B*prefix[u] + (R0 - D_top)*prefix[b]
        )
        record = (
            numerator,
            size,
            f[size],
            B,
            u,
            prefix[u],
            prefix_arg[u],
            b,
            prefix[b],
            prefix_arg[b],
        )
        if best is None or record[0] > best[0]:
            best = record
    return best[0] // (g - Q), best, traces, f


def planted_cap(Q, residual_dimension):
    if residual_dimension > Q:
        return None
    return (
        comb(g - residual_dimension + 6, 6)
        // comb(Q - residual_dimension + 6, 6)
    )


def source_lifted_coupled_rank7(Q):
    arrays, traces = recursive_arrays(Q, 6)
    child = arrays[6]
    D_top = d - 1
    largest = d - 6
    old = [0]*(largest + 1)
    planted = [None]*(largest + 1)
    cap = [0]*(largest + 1)
    prefix = [0]*(largest + 1)
    prefix_arg = [0]*(largest + 1)
    for size in range(1, largest + 1):
        residual = d - size
        old[size] = child[residual]
        planted[size] = planted_cap(Q, residual)
        cap[size] = (
            old[size]
            if planted[size] is None
            else min(old[size], planted[size])
        )
        if cap[size] > prefix[size - 1]:
            prefix[size] = cap[size]
            prefix_arg[size] = size
        else:
            prefix[size] = prefix[size - 1]
            prefix_arg[size] = prefix_arg[size - 1]
    best = None
    for size in range(1, largest + 1):
        B = D_top - size
        u = min(size, B - 4)
        b = min(size, B // 5)
        if u < 1 or b < 1:
            continue
        numerator = (
            size*cap[size] + B*prefix[u] + (R0 - D_top)*prefix[b]
        )
        record = (
            numerator,
            size,
            d - size,
            old[size],
            planted[size],
            cap[size],
            B,
            u,
            prefix[u],
            prefix_arg[u],
            b,
            prefix[b],
            prefix_arg[b],
        )
        if best is None or record[0] > best[0]:
            best = record
    return best[0] // (g - Q), best, traces


def parameterized_cap(rank, dimension, ambient_gap, excess):
    rank = int(rank)
    dimension = int(dimension)
    ambient_gap = int(ambient_gap)
    excess = int(excess)
    inner = (
        comb(ambient_gap + rank - 1, rank - 1)
        // comb(excess + rank - 1, rank - 1)
    )
    value = (ambient_gap + dimension)*inner // (excess + dimension)
    den = (
        (excess + dimension)^2
        - (ambient_gap + dimension)*(dimension - 1)
    )
    if den > 0:
        value = min(
            value,
            (ambient_gap + dimension)*(excess + 1) // den,
        )
    return value


def local_prefix_caps(ambient_gap, excess, max_dimension, top_rank=6):
    ambient_gap = int(ambient_gap)
    excess = int(excess)
    max_dimension = int(max_dimension)
    child = [0]*(max_dimension + 1)
    for dimension in range(1, max_dimension + 1):
        child[dimension] = (
            ambient_gap + dimension
        ) // (excess + dimension)
    for rank in range(2, int(top_rank) + 1):
        current = list(child)
        prefix = -1
        window = deque()
        for dimension in range(rank, max_dimension + 1):
            added = dimension - 1
            prefix = max(prefix, child[added])
            while window and child[window[-1]] <= child[added]:
                window.pop()
            window.append(added)
            lower = dimension - (dimension - 1) // (rank - 1)
            while window and window[0] < lower:
                window.popleft()
            exact = (
                (dimension - 1)*prefix
                + (ambient_gap + 1)*child[window[0]]
            ) // (excess + dimension)
            exact = min(
                exact,
                parameterized_cap(
                    rank, dimension, ambient_gap, excess
                ),
            )
            current[dimension] = max(child[dimension], exact)
        child = current
    return child


@lru_cache(maxsize=None)
def local_cap6(ambient_gap, excess, dimension):
    return local_prefix_caps(
        int(ambient_gap), int(excess), int(dimension), 6
    )[int(dimension)]


def scan_outer(Q, class_caps):
    largest = int(d - 6)
    prefix = [0]*(largest + 1)
    prefix_arg = [0]*(largest + 1)
    for size in range(1, largest + 1):
        if class_caps[size] > prefix[size - 1]:
            prefix[size] = class_caps[size]
            prefix_arg[size] = size
        else:
            prefix[size] = prefix[size - 1]
            prefix_arg[size] = prefix_arg[size - 1]
    agreement = int(g - Q)
    target_numerator = int(shallow_L - 1)*agreement
    best = None
    survivors = []
    for size in range(1, largest + 1):
        B = int(d - 1 - size)
        u = min(size, B - 4)
        b = min(size, B // 5)
        if u < 1 or b < 1:
            continue
        numerator = (
            size*class_caps[size]
            + B*prefix[u]
            + int(R0 - (d - 1))*prefix[b]
        )
        if numerator > target_numerator:
            survivors.append(size)
        record = (
            numerator,
            size,
            int(d - size),
            class_caps[size],
            B,
            u,
            prefix[u],
            prefix_arg[u],
            b,
            prefix[b],
            prefix_arg[b],
        )
        if best is None or record[0] > best[0]:
            best = record
    return best[0] // agreement, best, survivors


def linear_schedule(k):
    return 44835 - (67*int(k)) // 10


def tangent_schedule(k):
    k = int(k)
    return max(
        k - 1,
        int(w) + k - isqrt((int(R0 - d) + k)*(k - 1)) - 11,
    )


def dual_class(Q, k, split, old):
    low = local_cap6(int(R0 - d), int(w - split), int(k))
    planted = local_cap6(int(g - k), int(split + 1 - k), int(k))
    phi = int(Phi(Q))
    dual = low + max(phi, planted)
    return min(int(old), dual), low, planted, dual


def dual_scan(Q, schedule):
    child = local_prefix_caps(int(R0 - d), int(w - Q), int(d), 6)
    largest = int(d - 6)
    coarse = [0] + [
        child[int(d - size)] for size in range(1, largest + 1)
    ]
    coarse_head, coarse_best, survivors = scan_outer(Q, coarse)
    refined = list(coarse)
    raw = []
    for size in survivors:
        k = int(d - size)
        split = schedule(k)
        value, low, planted, dual = dual_class(
            Q, k, split, coarse[size]
        )
        refined[size] = value
        raw.append((k, split, dual))
    head, best, remaining = scan_outer(Q, refined)
    raw.sort()
    violations = sum(
        raw[index][2] > raw[index + 1][2]
        for index in range(len(raw) - 1)
    )
    return (
        head,
        best,
        len(survivors),
        len(remaining),
        raw[0],
        raw[-1],
        violations,
        coarse_head,
        coarse_best,
    )


# Reject the old H-saturated histogram with the exact weighted theorem.
old_hist = []
previous = 0
for q in range(15187):
    current = Hcap(q)
    old_hist.append(current - previous)
    previous = current
old_hist.append(shallow_L - previous)
assert sum(old_hist) == shallow_L
old_margins = {}
for Q in [0, 1, 2463, 15186]:
    lhs = sum((g - j)*old_hist[j] for j in range(Q + 1))
    old_margins[str(int(Q))] = R0*B6(Q) - lhs
assert old_margins == {
    "0": 279531,
    "1": -3193224,
    "2463": -9044103237,
    "15186": -116880365780,
}
stage_15187 = two_stage(15187)
stage_15838 = two_stage(15838)
stage_15839 = two_stage(15839)
assert stage_15187[:3] == (5052479, 6, 4638)
assert stage_15187[5] == 14589030
assert stage_15838[5] == 15774764
assert stage_15839[:3] == (5453288, 6, 4513)
assert stage_15839[3] == [1, 13, 162, 2240, 30191, 405788, 5453288]
assert stage_15839[4] == [-1, 1, 4136, 4486, 4511, 4513, 4513]
assert stage_15839[5] == 15776639

arrays_26052, trace_26052 = recursive_arrays(26052, 7)
arrays_26053, _ = recursive_arrays(26053, 7)
assert arrays_26052[7][d] == 15775392
assert arrays_26053[7][d] == 15776368
assert [record[1] for record in trace_26052] == [
    16, 253, 3987, 62817, 989693, 15592472
]
assert [record[2] for record in trace_26052] == [
    1, 2620, 2795, 2806, 2807, 2808
]

coupled_26143 = coupled_rank7(26143)
coupled_26144 = coupled_rank7(26144)
assert coupled_26143[0] == 15775194
assert coupled_26143[1] == (
    5187341399069,
    284730,
    15737600,
    2794,
    2790,
    1014691,
    2783,
    558,
    1014323,
    553,
)
assert coupled_26144[0] == 15776151
top_six = [284730, 614, 545, 545, 545, 545]
assert all(sum(top_six[:k]) <= d - 7 + k for k in range(1, 7))
assert sum(top_six) == d - 1
f_26144 = coupled_26144[3]
top_caps = [f_26144[size] for size in top_six]
assert top_caps == [15738557, 1014371, 1014361, 1014361, 1014361, 1014361]
tail_mass = R0 - (d - 1)
tail_full, tail_remainder = divmod(tail_mass, 545)
assert (tail_full, tail_remainder) == (1272, 365)
exact_relaxation_numerator = (
    sum(size*cap for size, cap in zip(top_six, top_caps))
    + tail_full*545*f_26144[545]
    + tail_remainder*f_26144[tail_remainder]
)
assert f_26144[365] == 1014344
assert exact_relaxation_numerator == 5187639320584
assert exact_relaxation_numerator // h0 == 15776148
dominant_planted_cap = (
    comb(g - 2795 + 6, 6) // comb(q0 - 2795 + 6, 6)
)
assert dominant_planted_cap == 11764989
coarse_other_capacity = coupled_26144[1][0] - 284730*15738557
required_big_slice = (
    shallow_L*h0 - coarse_other_capacity + 284730 - 1
) // 284730
assert required_big_slice == 15738305
assert dominant_planted_cap < required_big_slice

source_lifted_26144 = source_lifted_coupled_rank7(26144)
assert source_lifted_26144[0] == 15345533
assert source_lifted_26144[1] == (
    5046040936511,
    283663,
    3862,
    15294703,
    15295049,
    15294703,
    3861,
    3857,
    1014887,
    3846,
    772,
    1014383,
    757,
)
assert source_lifted_26144[1][0] % h0 == 11187
assert shallow_L - 1 - source_lifted_26144[0] == 430399
planted_values = [planted_cap(q0, k) for k in range(q0 + 1)]
planted_increments = [
    planted_values[k + 1] - planted_values[k] for k in range(q0)
]
assert min(planted_increments) == 1331

dual_26193 = dual_scan(26193, linear_schedule)
assert dual_26193[0] == 15775776
assert dual_26193[1] == (
    5186744182280,
    284498,
    3027,
    15738077,
    3026,
    3022,
    1018564,
    3012,
    605,
    1018174,
    601,
)
assert dual_26193[2:4] == (239, 0)
assert dual_26193[4] == (2788, 26156, 7899882)
assert dual_26193[5] == (3026, 24561, 12277361)
assert dual_26193[6] == 0
assert (shallow_L - 1) - dual_26193[0] == 156

dual_26194 = dual_scan(26194, tangent_schedule)
assert dual_26194[0] == 15800402
assert dual_26194[1] == (
    5194824788248,
    284380,
    3145,
    15762647,
    3144,
    3140,
    1022657,
    3136,
    628,
    1022236,
    613,
)
assert dual_26194[2] == 431

route_intervals = [
    (3144, 23768, 18, 15764297, 15764315),
    (23769, 23775, 16772, 15746404, 15763176),
    (23776, 23778, 26254, 15736663, 15762917),
    (23779, 23780, 34649, 15732593, 15767242),
    (23781, 23785, 44038, 15718801, 15762839),
    (23786, 23816, 136553, 15627111, 15763664),
    (23817, 26193, 11031141, 8136412, 19167553),
]
route_rows = []
for start, end, expected_low, expected_high, expected_sum in route_intervals:
    low = local_cap6(int(R0 - d), int(w - start), 3145)
    planted = local_cap6(int(g - 3145), int(end + 1 - 3145), 3145)
    high = max(int(Phi(26194)), planted)
    assert (low, high, low + high) == (
        expected_low, expected_high, expected_sum
    )
    route_rows.append([start, end, low, high, low + high])
assert route_rows[0][0] == 3144
assert route_rows[-1][1] == 26193
assert all(
    route_rows[index][1] + 1 == route_rows[index + 1][0]
    for index in range(len(route_rows) - 1)
)
assert min(row[-1] for row in route_rows) == 15762839
assert min(row[-1] for row in route_rows) - 15762647 == 192

v_26193 = int(w - 26193)
generic_t_23729 = (
    comb(int(R0 - d) + 7, 7) // comb(v_26193 + 23729 + 7, 7)
)
generic_t_23730 = (
    comb(int(R0 - d) + 7, 7) // comb(v_26193 + 23730 + 7, 7)
)
assert (generic_t_23729, generic_t_23730) == (15776593, 15774894)
small_t_K_min = int(d - 23729)
two_active_lower = 2*(small_t_K_min - 26193)
top_two_cap = small_t_K_min - 5
assert (small_t_K_min, two_active_lower - top_two_cap) == (263796, 211415)


# Exact scalar-feasible but source-impossible one-level marginal.
hist = [0]*q0 + [shallow_L]
assert digest(hist) == (
    "c393b083f7b71a8b03c8823153cae6e4c81044cd3924bfae002f8dd257a853d5"
)
first = shallow_L*q0
second = shallow_L*q0^2
assert first == 412445992352
assert second == 10782988024050688
assert g*first - second == 135623790773123456
assert B6(q0) == 22416731
assert Hcap(q0) == 66885134
assert R0*B6(q0) - shallow_L*h0 == 16806136372775
assert Phi(q0) == 3983444
assert g*Phi(q0) - first == 1001565091216
assert g*Phi(q0) // q0 == 54085491


# Proper fixed-G moderate caps and exact 39-slice cofactor marginal.
values = [Fcap(q) for q in range(1, d)]
assert max(values) == 624046
assert values.index(max(values)) + 1 == w
assert Fcap(1) == 317828
assert Fcap(q0) == 412817
assert Fcap(100000) == 107399
assert Fcap(d - 1) == 1576

slice_counts = [412817]*38 + [88887]
assert sum(slice_counts) == shallow_L
assert gcd(q0, g) == 4
root_loads = [0]*g
root_word_loads = [0]*g
for j, count in enumerate(slice_counts):
    start = (j*q0) % g
    for offset in range(q0):
        root = (start + offset) % g
        root_loads[root] += 1
        root_word_loads[root] += count
assert root_loads.count(2) == 45300
assert root_loads.count(3) == 309672
assert min(root_loads) == 2
assert max(root_loads) == 3
assert max(root_word_loads) <= 1238451 < Phi(q0)


# Independent deployed interlaced construction arithmetic.
unique_sizes = [33973]*4 + [33972]*3
extra_pairs = {(1, 2), (3, 4), (5, 6), (6, 7), (5, 7)}
pair_degrees = [0]*7
pair_total = 0
for i in range(1, 8):
    for j in range(i + 1, 8):
        size = 5579 + ((i, j) in extra_pairs)
        pair_degrees[i - 1] += size
        pair_degrees[j - 1] += size
        pair_total += size
assert pair_degrees == [33475]*4 + [33476]*3
assert [unique_sizes[i] + pair_degrees[i] for i in range(7)] == [67448]*7
assert sum(unique_sizes) + pair_total == g
assert 887*1090 + 137*1089 == a
assert 887*958 + 137*959 == R0
assert 7*(67448 - 65536) == 13384
assert R0 - 7*65536 == 522377
assert 6*R0 == 5886774 < p - 1
assert g <= 6*65536
assert g <= 1048576


# Direct finite-field realization of the complete source mechanism.
F = GF(101)
PR.<X> = PolynomialRing(F)
D_toy = [F(i) for i in range(80)]
S0 = [F(8*k + offset) for k in range(10) for offset in range(4)]
E0 = [F(8*k + offset) for k in range(10) for offset in range(4, 8)]
A0 = prod(X - x for x in S0)
L0 = prod(X - x for x in E0)

core = S0[:5]
unique = [S0[5 + 6*i: 11 + 6*i] for i in range(3)]
G_polys = [prod(X - x for x in core + unique[i]) for i in range(3)]
assert all(Gi.degree() == 11 for Gi in G_polys)
P_toy = lcm(lcm(G_polys[0], G_polys[1]), G_polys[2])
assert P_toy.degree() == 23

H_supports = []
for i in range(3):
    support = [F(8*k + 4 + i) for k in range(10)]
    support.append(F(8*i + 7))
    H_supports.append(support)
assert all(len(set(support)) == 11 for support in H_supports)
assert len(set().union(*[set(support) for support in H_supports])) == 33
H_polys = [prod(X - x for x in support) for support in H_supports]

labels = [F(1)]
for j in range(1, 3):
    forbidden = {F(0)}
    for i in range(j):
        for x in E0:
            forbidden.add(labels[i]*G_polys[j](x)/G_polys[i](x))
    labels.append(next(value for value in F if value not in forbidden))
assert all(
    (G_polys[i]*labels[j] - G_polys[j]*labels[i])(x) != 0
    for i in range(3)
    for j in range(i)
    for x in E0
)

value_table = {}
for i in range(3):
    for x in H_supports[i]:
        value_table[x] = G_polys[i](x)/labels[i]
for x in E0:
    if x in value_table:
        continue
    forbidden_values = {F(0)} | {
        G_polys[i](x)/labels[i] for i in range(3)
    }
    value_table[x] = next(value for value in F if value not in forbidden_values)
V = PR.lagrange_polynomial([(x, value_table[x]) for x in E0])
assert gcd(V, L0) == 1
assert all(
    gcd(L0, G_polys[i] - labels[i]*V) == H_polys[i]
    for i in range(3)
)
H0 = V.inverse_mod(L0)
U = A0*H0

codewords = [(A0 // G_polys[i])*labels[i] for i in range(3)]
assert matrix(F, [[c[j] for j in range(30)] for c in codewords]).rank() == 3
agreement_counts = []
agreement_full_blocks = []
error_full_blocks = []
for c in codewords:
    agreements = {int(x) for x in D_toy if c(x) == U(x)}
    errors = {int(x) for x in D_toy if c(x) != U(x)}
    agreement_counts.append(len(agreements))
    agreement_full_blocks.append(
        any(set(range(8*k, 8*k + 8)) <= agreements for k in range(10))
    )
    error_full_blocks.append(
        any(set(range(8*k, 8*k + 8)) <= errors for k in range(10))
    )
assert agreement_counts == [40, 40, 40]
assert agreement_full_blocks == [False, False, False]
assert error_full_blocks == [False, False, False]

Y = P_toy*H0
M_toy = P_toy*L0
f_polys = [(P_toy // G_polys[i])*labels[i] for i in range(3)]
assert all(f.degree() == 12 < 13 for f in f_polys)
assert all(
    gcd(M_toy, Y - f_polys[i]) == (P_toy // G_polys[i])*H_polys[i]
    for i in range(3)
)
assert gcd(gcd(f_polys[0], f_polys[1]), f_polys[2]) == 1


# No-second-cofactor-pivot structural control.
Q_toy = prod(X - F(i) for i in range(6))
witness_basis = [PR(1)] + [Q_toy*X^j for j in range(6)]
assert matrix(F, [[f[j] for j in range(12)] for f in witness_basis]).rank() == 7
for alpha in [F(i) for i in range(6)]:
    assert [f(alpha) for f in witness_basis] == [F(1)] + [F(0)]*6


transport = [[j, 0, 0] for j in range(q0)]
transport.append([q0, 10411669, 5364264])
sparse = {
    "delta": q0,
    "count": shallow_L,
    "b_zero": 10411669,
    "b_layer": 5364264,
}
assert digest(transport) == (
    "e4fd2bbef5e5f983a9c6edeb75baf592c4f3c8aa1157816b998e978f5e29c2ae"
)
assert digest(sparse) == (
    "8bd18793245255c785979c0f447ac0cfeb7f3057c5504e6ffa38cbb49261ea20"
)

record = {
    "schema": "m31-rank7-weighted-head-interlaced-source-sage-v1",
    "scope": "INDEPENDENT_WEIGHTED_ARITHMETIC_AND_DIRECT_TOY_SOURCE",
    "weighted": {
        "old_margins": old_margins,
        "two_stage_Q15187": {
            "M": stage_15187[0],
            "rank": stage_15187[1],
            "nu": stage_15187[2],
            "head": stage_15187[5],
        },
        "two_stage_Q15838_head": stage_15838[5],
        "two_stage_Q15839": {
            "M": stage_15839[0],
            "rank": stage_15839[1],
            "nu": stage_15839[2],
            "rank_caps": stage_15839[3],
            "rank_nu": stage_15839[4],
            "head": stage_15839[5],
        },
        "B6": B6(q0),
        "weighted_margin": R0*B6(q0) - shallow_L*h0,
        "Phi": Phi(q0),
        "cofactor_margin": g*Phi(q0) - first,
        "F_endpoint_cutoff": Fcap(q0),
        "F_max": max(values),
    },
    "recursive_full_line": {
        "two_tier_Q26052_head": arrays_26052[7][d],
        "two_tier_Q26053_head": arrays_26053[7][d],
        "coupled_Q26143_head": coupled_26143[0],
        "coupled_Q26143_numerator": coupled_26143[1][0],
        "coupled_Q26144_coarse_head": coupled_26144[0],
        "Q26144_exact_relaxation_head": exact_relaxation_numerator // h0,
        "Q26144_exact_relaxation_numerator": exact_relaxation_numerator,
        "Q26144_source_lifted_head": source_lifted_26144[0],
        "Q26144_source_lifted_numerator": source_lifted_26144[1][0],
        "Q26144_source_lifted_optimizer": list(source_lifted_26144[1][1:]),
        "Q26144_target_margin": shallow_L - 1 - source_lifted_26144[0],
        "common_zero_reduction": {
            "state_map": "(R,D,v)->(R-t,D-t,v+t)",
            "partition_map": "ADD_T_TO_LARGEST_CLASS",
            "planted_dimensions_checked": [0, q0],
            "planted_min_increment": min(planted_increments),
            "conclusion": "T_ZERO_IS_WORST_CASE",
        },
    },
    "dual_domain": {
        "Q26193_schedule": "x(k)=44835-floor(67*k/10)",
        "Q26193_head": dual_26193[0],
        "Q26193_numerator": dual_26193[1][0],
        "Q26193_optimizer": list(dual_26193[1][1:]),
        "Q26193_coarse_survivors": dual_26193[2],
        "Q26193_remaining_survivors": dual_26193[3],
        "Q26193_first_raw": list(dual_26193[4]),
        "Q26193_last_raw": list(dual_26193[5]),
        "Q26193_monotonicity_violations": dual_26193[6],
        "Q26194_schedule": (
            "x(k)=max(k-1,w+k-isqrt((A_E+k)(k-1))-11)"
        ),
        "Q26194_head": dual_26194[0],
        "Q26194_numerator": dual_26194[1][0],
        "Q26194_optimizer": list(dual_26194[1][1:]),
        "Q26194_Phi": Phi(26194),
        "Q26194_route_intervals": route_rows,
        "Q26194_minimum_sum": min(row[-1] for row in route_rows),
        "Q26194_minimum_excess": (
            min(row[-1] for row in route_rows) - 15762647
        ),
        "E0_zero_branch": {
            "t_23729_cap": generic_t_23729,
            "t_23730_cap": generic_t_23730,
            "small_t_K_min": small_t_K_min,
            "unique_active_line_margin": two_active_lower - top_two_cap,
        },
    },
    "cyclic_marginal": {
        "slice_count": len(slice_counts),
        "root_load_2": root_loads.count(2),
        "root_load_3": root_loads.count(3),
        "max_word_load": max(root_word_loads),
    },
    "toy": {
        "field": 101,
        "n": 80,
        "K": 30,
        "agreement": 40,
        "rank": 3,
        "companions": 3,
        "master_degree": P_toy.degree(),
        "message_dimension": 13,
        "cofactor_degree": 12,
        "agreement_counts": agreement_counts,
        "complete_agreement_blocks": agreement_full_blocks,
        "complete_error_blocks": error_full_blocks,
        "full_gcd": True,
        "exact_lcm": True,
    },
    "no_second_pivot": {
        "rank": 7,
        "Q_roots": 6,
        "evaluation_column_rank": 1,
    },
}
record["payload_sha256"] = hashlib.sha256(canonical(record)).hexdigest()
print(canonical(record).decode("ascii"), end="")
