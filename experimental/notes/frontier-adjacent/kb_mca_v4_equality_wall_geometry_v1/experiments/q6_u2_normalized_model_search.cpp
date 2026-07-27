#include <array>
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using U = std::uint64_t;
static constexpr U P = 2130706433ULL;

U add(U a, U b) { U c = a + b; return c >= P ? c - P : c; }
U sub(U a, U b) { return a >= b ? a - b : a + P - b; }
U mul(U a, U b) { return (a * b) % P; }
U power(U a, U e) {
    U r = 1;
    while (e) {
        if (e & 1) r = mul(r, a);
        a = mul(a, a);
        e >>= 1;
    }
    return r;
}
U inv(U a) { return power(a, P - 2); }

using V5 = std::array<U, 5>;

V5 from_roots(const std::array<U, 4>& roots) {
    V5 c{1, 0, 0, 0, 0};
    int degree = 0;
    for (U r : roots) {
        V5 n{};
        for (int i = 0; i <= degree; ++i) {
            n[i] = add(n[i], sub(0, mul(r, c[i])));
            n[i + 1] = add(n[i + 1], c[i]);
        }
        c = n;
        ++degree;
    }
    return c;
}

struct Option {
    V5 v;
    int edge_count;
    std::array<int, 4> root_indices;
    unsigned common_mask;
};

struct Key {
    std::array<U, 3> x;
    bool operator==(const Key& other) const { return x == other.x; }
};
struct KeyHash {
    std::size_t operator()(const Key& k) const {
        std::size_t h = 1469598103934665603ULL;
        for (U x : k.x) {
            h ^= static_cast<std::size_t>(x);
            h *= 1099511628211ULL;
        }
        return h;
    }
};

Key normalize(std::array<U, 3> x) {
    for (U a : x) {
        if (a != 0) {
            U z = inv(a);
            for (U& b : x) b = mul(b, z);
            return {x};
        }
    }
    return {{0, 0, 0}};
}

bool can_sum_four(const std::array<unsigned, 6>& masks) {
    unsigned reachable = 1;
    for (unsigned mask : masks) {
        unsigned next = 0;
        for (int total = 0; total <= 4; ++total) {
            if (!(reachable & (1U << total))) continue;
            for (int e = 0; e <= 2; ++e) {
                if ((mask & (1U << e)) && total + e <= 4)
                    next |= 1U << (total + e);
            }
        }
        reachable = next;
    }
    return reachable & (1U << 4);
}

struct Sig {
    int edges;
    unsigned common;
    const Option* witness;
};

bool grs_degree_two_valid(const std::vector<const Option*>& selected) {
    std::array<U, 6> x{};
    for (int row = 0; row < 6; ++row)
        x[row] = mul(6 + row, 6 + row);

    std::array<U, 6> dual{};
    for (int row = 0; row < 6; ++row) {
        U denominator = 1;
        for (int other = 0; other < 6; ++other)
            if (row != other)
                denominator = mul(denominator, sub(x[row], x[other]));
        dual[row] = inv(denominator);
    }

    // The quartics are monic. Their six row scalars must therefore be
    // evaluations S(x_j) of one quadratic S. For each of the other four
    // coefficients, the three dual GRS checks give a homogeneous equation
    // in the three coefficients of S.
    std::array<std::array<U, 3>, 12> matrix{};
    int equation = 0;
    for (int coefficient = 0; coefficient < 4; ++coefficient) {
        for (int moment = 0; moment < 3; ++moment) {
            for (int source_degree = 0; source_degree < 3;
                 ++source_degree) {
                U entry = 0;
                for (int row = 0; row < 6; ++row) {
                    entry = add(
                        entry,
                        mul(
                            mul(
                                dual[row],
                                power(x[row], moment + source_degree)),
                            selected[row]->v[coefficient]));
                }
                matrix[equation][source_degree] = entry;
            }
            ++equation;
        }
    }

    std::array<int, 3> pivot_row{};
    pivot_row.fill(-1);
    int rank = 0;
    for (int col = 0; col < 3 && rank < 12; ++col) {
        int pivot = -1;
        for (int row = rank; row < 12; ++row)
            if (matrix[row][col] != 0) { pivot = row; break; }
        if (pivot < 0) continue;
        std::swap(matrix[rank], matrix[pivot]);
        U scale = inv(matrix[rank][col]);
        for (int c = col; c < 3; ++c)
            matrix[rank][c] = mul(matrix[rank][c], scale);
        for (int row = 0; row < 12; ++row) {
            if (row == rank || matrix[row][col] == 0) continue;
            U factor = matrix[row][col];
            for (int c = col; c < 3; ++c)
                matrix[row][c] = sub(
                    matrix[row][c], mul(factor, matrix[rank][c]));
        }
        pivot_row[col] = rank++;
    }
    if (rank == 3) return false;

    std::vector<std::array<U, 3>> kernel_basis;
    for (int free_col = 0; free_col < 3; ++free_col) {
        if (pivot_row[free_col] >= 0) continue;
        std::array<U, 3> vector{};
        vector[free_col] = 1;
        for (int pivot_col = 0; pivot_col < 3; ++pivot_col) {
            int row = pivot_row[pivot_col];
            if (row >= 0)
                vector[pivot_col] = sub(0, matrix[row][free_col]);
        }
        kernel_basis.push_back(vector);
    }
    for (int source_row = 0; source_row < 6; ++source_row) {
        bool some_nonzero_scale = false;
        for (const auto& vector : kernel_basis) {
            U value = 0;
            for (int degree = 0; degree < 3; ++degree)
                value = add(
                    value,
                    mul(vector[degree], power(x[source_row], degree)));
            some_nonzero_scale |= value != 0;
        }
        if (!some_nonzero_scale) return false;
    }
    return true;
}

bool grs_degree_two_valid_direct(
    const std::vector<const Option*>& selected
) {
    std::array<U, 6> x{};
    for (int row = 0; row < 6; ++row)
        x[row] = mul(6 + row, 6 + row);

    std::array<U, 6> dual{};
    for (int row = 0; row < 6; ++row) {
        U denominator = 1;
        for (int other = 0; other < 6; ++other)
            if (row != other)
                denominator =
                    mul(denominator, sub(x[row], x[other]));
        dual[row] = inv(denominator);
    }

    std::array<std::array<U, 6>, 15> matrix{};
    int equation = 0;
    for (int coefficient = 0; coefficient < 5; ++coefficient) {
        for (int moment = 0; moment < 3; ++moment) {
            for (int row = 0; row < 6; ++row)
                matrix[equation][row] = mul(
                    mul(dual[row], power(x[row], moment)),
                    selected[row]->v[coefficient]);
            ++equation;
        }
    }

    std::array<int, 6> pivot_row{};
    pivot_row.fill(-1);
    int rank = 0;
    for (int col = 0; col < 6 && rank < 15; ++col) {
        int pivot = -1;
        for (int row = rank; row < 15; ++row)
            if (matrix[row][col] != 0) {
                pivot = row;
                break;
            }
        if (pivot < 0) continue;
        std::swap(matrix[rank], matrix[pivot]);
        U scale = inv(matrix[rank][col]);
        for (int c = col; c < 6; ++c)
            matrix[rank][c] = mul(matrix[rank][c], scale);
        for (int row = 0; row < 15; ++row) {
            if (row == rank || matrix[row][col] == 0) continue;
            U factor = matrix[row][col];
            for (int c = col; c < 6; ++c)
                matrix[row][c] =
                    sub(matrix[row][c],
                        mul(factor, matrix[rank][c]));
        }
        pivot_row[col] = rank++;
    }
    if (rank == 6) return false;

    std::vector<std::array<U, 6>> kernel_basis;
    for (int free_col = 0; free_col < 6; ++free_col) {
        if (pivot_row[free_col] >= 0) continue;
        std::array<U, 6> vector{};
        vector[free_col] = 1;
        for (int pivot_col = 0; pivot_col < 6; ++pivot_col) {
            int row = pivot_row[pivot_col];
            if (row >= 0)
                vector[pivot_col] =
                    sub(0, matrix[row][free_col]);
        }
        kernel_basis.push_back(vector);
    }
    for (int source_row = 0; source_row < 6; ++source_row) {
        bool coordinate_can_be_nonzero = false;
        for (const auto& vector : kernel_basis)
            coordinate_can_be_nonzero |= vector[source_row] != 0;
        if (!coordinate_can_be_nonzero) return false;
    }
    return true;
}

std::vector<const Option*> find_sum_four_with_empty_gcd(
    const std::array<std::vector<Sig>, 6>& choices
) {
    struct Prev {
        bool set = false;
        int previous_total = 0;
        unsigned previous_mask = 0;
        const Option* witness = nullptr;
    };
    std::array<std::array<bool, 1 << 10>, 5> current{};
    std::array<std::array<std::array<Prev, 1 << 10>, 5>, 6> previous{};
    current[0][(1 << 10) - 1] = true;
    for (int row = 0; row < 6; ++row) {
        std::array<std::array<bool, 1 << 10>, 5> next{};
        for (int total = 0; total <= 4; ++total)
        for (unsigned mask = 0; mask < (1U << 10); ++mask) {
            if (!current[total][mask]) continue;
            for (const Sig& choice : choices[row]) {
                int nt = total + choice.edges;
                unsigned nm = mask & choice.common;
                if (nt <= 4 && !next[nt][nm]) {
                    next[nt][nm] = true;
                    previous[row][nt][nm] = {
                        true, total, mask, choice.witness
                    };
                }
            }
        }
        current = next;
    }
    if (!current[4][0]) return {};
    std::vector<const Option*> out(6);
    int total = 4;
    unsigned mask = 0;
    for (int row = 5; row >= 0; --row) {
        const Prev& p = previous[row][total][mask];
        out[row] = p.witness;
        total = p.previous_total;
        mask = p.previous_mask;
    }
    return out;
}

std::vector<const Option*> find_with_quadratic_fiber_cap(
    const std::array<std::vector<Sig>, 6>& choices
) {
    std::vector<const Option*> selected(6, nullptr);
    std::array<int, 10> common_occurrences{};
    bool found = false;
    auto dfs = [&](auto&& self, int row, int edge_sum,
                   unsigned common_mask) -> void {
        if (found || edge_sum > 4) return;
        if (row == 6) {
            bool exact_common_fibers = true;
            for (int count : common_occurrences)
                exact_common_fibers &= count == 2;
            if (edge_sum == 4 && exact_common_fibers
                && common_mask == 0 && grs_degree_two_valid(selected))
                found = true;
            return;
        }
        for (const Sig& choice : choices[row]) {
            bool common_capacity_ok = true;
            for (int root = 0; root < 10; ++root)
                if ((choice.common & (1U << root))
                    && common_occurrences[root] >= 2)
                    common_capacity_ok = false;
            if (!common_capacity_ok) continue;
            int repeated = 0;
            for (int r = 0; r < row; ++r)
                if (selected[r]->v == choice.witness->v) ++repeated;
            if (repeated >= 2) continue;
            selected[row] = choice.witness;
            for (int root = 0; root < 10; ++root)
                if (choice.common & (1U << root))
                    ++common_occurrences[root];
            self(self, row + 1, edge_sum + choice.edges,
                 common_mask & choice.common);
            for (int root = 0; root < 10; ++root)
                if (choice.common & (1U << root))
                    --common_occurrences[root];
            if (found) return;
        }
    };
    dfs(dfs, 0, 0, (1U << 10) - 1);
    return found ? selected : std::vector<const Option*>{};
}

std::vector<const Option*> find_identical_zero_edge_fixture(
    const std::array<std::vector<Option>, 6>& options
) {
    auto in_span = [](const V5& a, const V5& b, const V5& v) {
        int p0 = -1, p1 = -1;
        U determinant = 0;
        for (int i = 0; i < 5 && p0 < 0; ++i)
        for (int j = i + 1; j < 5; ++j) {
            U candidate =
                sub(mul(a[i], b[j]), mul(a[j], b[i]));
            if (candidate != 0) {
                p0 = i;
                p1 = j;
                determinant = candidate;
                break;
            }
        }
        if (p0 < 0) return v == a;
        U inverse = inv(determinant);
        U coefficient_a = mul(
            sub(mul(v[p0], b[p1]), mul(v[p1], b[p0])),
            inverse);
        U coefficient_b = mul(
            sub(mul(a[p0], v[p1]), mul(a[p1], v[p0])),
            inverse);
        for (int coordinate = 0; coordinate < 5; ++coordinate)
            if (v[coordinate] != add(
                    mul(coefficient_a, a[coordinate]),
                    mul(coefficient_b, b[coordinate])))
                return false;
        return true;
    };

    std::vector<const Option*> selected(6, nullptr);
    std::array<int, 10> common_occurrences{};
    bool found = false;
    for (int zero_a = 0; zero_a < 6 && !found; ++zero_a)
    for (int zero_b = zero_a + 1; zero_b < 6 && !found; ++zero_b) {
        for (const Option& base : options[0]) {
            if (base.edge_count != 0) continue;
            const Option* base_a = nullptr;
            const Option* base_b = nullptr;
            for (const Option& candidate : options[zero_a])
                if (candidate.edge_count == 0
                    && candidate.v == base.v)
                    base_a = &candidate;
            for (const Option& candidate : options[zero_b])
                if (candidate.edge_count == 0
                    && candidate.v == base.v)
                    base_b = &candidate;
            if (base_a == nullptr || base_b == nullptr) continue;
            selected[zero_a] = base_a;
            selected[zero_b] = base_b;
            common_occurrences.fill(0);
            for (int root = 0; root < 10; ++root)
                if (base.common_mask & (1U << root))
                    common_occurrences[root] = 2;

            std::array<int, 4> active_rows{};
            int active_index = 0;
            for (int row = 0; row < 6; ++row)
                if (row != zero_a && row != zero_b)
                    active_rows[active_index++] = row;

            int first_row = active_rows[0];
            for (const Option& first : options[first_row]) {
                if (first.edge_count != 1
                    || (first.common_mask & base.common_mask) != 0)
                    continue;
                selected[first_row] = &first;
                for (int root = 0; root < 10; ++root)
                    if (first.common_mask & (1U << root))
                        ++common_occurrences[root];

            auto dfs = [&](auto&& self, int slot) -> void {
                if (found) return;
                if (slot == 4) {
                    bool exact_common_fibers = true;
                    for (int count : common_occurrences)
                        exact_common_fibers &= count == 2;
                    if (exact_common_fibers
                        && grs_degree_two_valid(selected))
                        found = true;
                    return;
                }
                int row = active_rows[slot];
                for (const Option& choice : options[row]) {
                    if (choice.edge_count != 1
                        || (choice.common_mask & base.common_mask) != 0)
                        continue;
                    if (!in_span(base.v, first.v, choice.v)) continue;
                    bool common_capacity_ok = true;
                    for (int root = 0; root < 10; ++root)
                        if ((choice.common_mask & (1U << root))
                            && common_occurrences[root] >= 2)
                            common_capacity_ok = false;
                    if (!common_capacity_ok) continue;
                    int repeated = 0;
                    for (int previous = 0; previous < row; ++previous)
                        if (selected[previous] != nullptr
                            && selected[previous]->v == choice.v)
                            ++repeated;
                    if (repeated >= 2) continue;
                    selected[row] = &choice;
                    for (int root = 0; root < 10; ++root)
                        if (choice.common_mask & (1U << root))
                            ++common_occurrences[root];
                    self(self, slot + 1);
                    for (int root = 0; root < 10; ++root)
                        if (choice.common_mask & (1U << root))
                            --common_occurrences[root];
                    selected[row] = nullptr;
                    if (found) return;
                }
            };
                dfs(dfs, 1);
                for (int root = 0; root < 10; ++root)
                    if (first.common_mask & (1U << root))
                        --common_occurrences[root];
                selected[first_row] = nullptr;
                if (found) return selected;
            }
            selected[zero_a] = nullptr;
            selected[zero_b] = nullptr;
        }
    }
    return {};
}

int main() {
    std::array<U, 10> common{};
    for (int i = 0; i < 5; ++i) {
        common[2 * i] = i + 1;
        common[2 * i + 1] = P - (i + 1);
    }
    std::array<std::array<U, 2>, 6> edges{};
    for (int j = 0; j < 6; ++j) {
        U current = 6 + j;
        U previous = 6 + ((j + 5) % 6);
        edges[j] = {P - current, previous};
    }

    std::vector<V5> common_forms;
    for (int a = 0; a < 10; ++a)
    for (int b = a + 1; b < 10; ++b)
    for (int c = b + 1; c < 10; ++c)
    for (int d = c + 1; d < 10; ++d)
        common_forms.push_back(from_roots(
            {common[a], common[b], common[c], common[d]}));

    std::array<std::vector<Option>, 6> options;
    for (int row = 0; row < 6; ++row) {
        std::array<U, 12> roots{};
        for (int i = 0; i < 10; ++i) roots[i] = common[i];
        roots[10] = edges[row][0];
        roots[11] = edges[row][1];
        for (int a = 0; a < 12; ++a)
        for (int b = a + 1; b < 12; ++b)
        for (int c = b + 1; c < 12; ++c)
        for (int d = c + 1; d < 12; ++d) {
            int ec = (a >= 10) + (b >= 10) + (c >= 10) + (d >= 10);
            options[row].push_back({
                from_roots({roots[a], roots[b], roots[c], roots[d]}),
                ec,
                {a, b, c, d},
                ((a < 10) ? (1U << a) : 0U)
                | ((b < 10) ? (1U << b) : 0U)
                | ((c < 10) ? (1U << c) : 0U)
                | ((d < 10) ? (1U << d) : 0U)
            });
        }
    }

    std::uint64_t lcg_state = 0x7d39a4c1ULL;
    for (int trial = 0; trial < 20000; ++trial) {
        std::vector<const Option*> selected(6);
        for (int row = 0; row < 6; ++row) {
            lcg_state =
                lcg_state * 6364136223846793005ULL
                + 1442695040888963407ULL;
            selected[row] =
                &options[row][lcg_state % options[row].size()];
        }
        if (grs_degree_two_valid(selected)
            != grs_degree_two_valid_direct(selected)) {
            std::cerr << "GRS reduction mismatch at trial "
                      << trial << "\n";
            return 2;
        }
    }

    auto identical_zero_edge =
        find_identical_zero_edge_fixture(options);
    if (!identical_zero_edge.empty()) {
        std::cout << "identical-zero-edge fixture\n";
        for (int row = 0; row < 6; ++row) {
            std::cout << "row=" << row
                      << " edge_count="
                      << identical_zero_edge[row]->edge_count
                      << " common_mask="
                      << identical_zero_edge[row]->common_mask
                      << " roots=";
            for (int x : identical_zero_edge[row]->root_indices)
                std::cout << x << ",";
            std::cout << "\n";
        }
        return 0;
    }

    std::uint64_t pairs = 0;
    for (std::size_t ia = 0; ia < common_forms.size(); ++ia) {
        for (std::size_t ib = ia + 1; ib < common_forms.size(); ++ib) {
            ++pairs;
            const V5& A = common_forms[ia];
            const V5& B = common_forms[ib];
            int p0 = -1, p1 = -1;
            U det = 0;
            for (int i = 0; i < 5 && p0 < 0; ++i)
            for (int j = i + 1; j < 5; ++j) {
                U d = sub(mul(A[i], B[j]), mul(A[j], B[i]));
                if (d != 0) { p0 = i; p1 = j; det = d; break; }
            }
            U idet = inv(det);
            std::array<int, 3> free{};
            int z = 0;
            for (int i = 0; i < 5; ++i)
                if (i != p0 && i != p1) free[z++] = i;

            std::array<unsigned, 6> zero_masks{};
            std::array<std::array<const Option*, 3>, 6> zero_witnesses{};
            std::array<std::vector<Sig>, 6> zero_signatures{};
            std::array<
                std::unordered_map<Key, std::vector<Sig>, KeyHash>, 6
            > maps;
            for (int row = 0; row < 6; ++row) {
                for (const Option& o : options[row]) {
                    U ca = mul(sub(mul(o.v[p0], B[p1]),
                                   mul(o.v[p1], B[p0])), idet);
                    U cb = mul(sub(mul(A[p0], o.v[p1]),
                                   mul(A[p1], o.v[p0])), idet);
                    std::array<U, 3> residual{};
                    for (int k = 0; k < 3; ++k) {
                        int col = free[k];
                        residual[k] = sub(
                            sub(o.v[col], mul(ca, A[col])),
                            mul(cb, B[col]));
                    }
                    Key key = normalize(residual);
                    unsigned bit = 1U << o.edge_count;
                    if (key.x == std::array<U, 3>{0, 0, 0}) {
                        zero_masks[row] |= bit;
                        if (zero_witnesses[row][o.edge_count] == nullptr)
                            zero_witnesses[row][o.edge_count] = &o;
                        zero_signatures[row].push_back(
                            {o.edge_count, o.common_mask, &o});
                    } else {
                        maps[row][key].push_back(
                            {o.edge_count, o.common_mask, &o});
                    }
                }
            }

            auto rank_two_witness =
                find_with_quadratic_fiber_cap(zero_signatures);
            if (!rank_two_witness.empty()) {
                std::cout << "rank-two fixture pair=" << ia << "," << ib
                          << " checked_pairs=" << pairs << "\n";
                int remaining = 4;
                for (int row = 0; row < 6; ++row) {
                    int chosen = -1;
                    for (int e = 0; e <= 2; ++e) {
                        if (e > remaining || !zero_witnesses[row][e]) continue;
                        std::array<unsigned, 6> suffix{};
                        for (int r = row + 1; r < 6; ++r)
                            suffix[r] = zero_masks[r];
                        unsigned reachable = 1;
                        for (int r = row + 1; r < 6; ++r) {
                            unsigned next = 0;
                            for (int total = 0; total <= 4; ++total)
                                if (reachable & (1U << total))
                                    for (int ee = 0; ee <= 2; ++ee)
                                        if ((suffix[r] & (1U << ee))
                                            && total + ee <= 4)
                                            next |= 1U << (total + ee);
                            reachable = next;
                        }
                        if (reachable & (1U << (remaining - e))) {
                            chosen = e;
                            break;
                        }
                    }
                    const Option* w = zero_witnesses[row][chosen];
                    std::cout << "row=" << row
                              << " edge_count=" << chosen
                              << " roots=";
                    for (int x : w->root_indices) std::cout << x << ",";
                    std::cout << "\n";
                    remaining -= chosen;
                }
                return 0;
            }
            std::unordered_set<Key, KeyHash> residual_directions;
            for (int row = 0; row < 6; ++row)
                for (const auto& [key, signatures] : maps[row])
                    residual_directions.insert(key);
            for (const Key& key : residual_directions) {
                std::array<std::vector<Sig>, 6> choices{};
                choices[0] = zero_signatures[0];
                auto first = maps[0].find(key);
                if (first != maps[0].end())
                    choices[0].insert(
                        choices[0].end(),
                        first->second.begin(), first->second.end());
                bool usable = true;
                for (int row = 1; row < 6; ++row) {
                    auto it = maps[row].find(key);
                    choices[row] = zero_signatures[row];
                    if (it != maps[row].end())
                        choices[row].insert(
                            choices[row].end(),
                            it->second.begin(),
                            it->second.end());
                    if (choices[row].empty()) { usable = false; break; }
                }
                auto witness = usable
                    ? find_with_quadratic_fiber_cap(choices)
                    : std::vector<const Option*>{};
                if (!witness.empty()) {
                    std::cout << "rank-three fixture pair=" << ia << "," << ib
                              << " checked_pairs=" << pairs << "\n";
                    for (int row = 0; row < 6; ++row) {
                        std::cout << "row=" << row
                                  << " edge_count="
                                  << witness[row]->edge_count
                                  << " common_mask="
                                  << witness[row]->common_mask
                                  << " roots=";
                        for (int x : witness[row]->root_indices)
                            std::cout << x << ",";
                        std::cout << "\n";
                    }
                    return 0;
                }
            }
        }
    }
    std::cout
        << "status=NO_FIXTURE\n"
        << "field=" << P << "\n"
        << "rows=6\n"
        << "common_poles=10\n"
        << "free_edge_poles=12\n"
        << "required_owned_edges=4\n"
        << "common_occurrence=2\n"
        << "grs_crosscheck_trials=20000\n"
        << "identical_zero_edge_branch=NO_FIXTURE\n"
        << "distinct_zero_edge_branch=NO_FIXTURE\n"
        << "distinct_common_pairs=" << pairs << "\n";
}
