#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

constexpr std::uint32_t P = 2147483647U;

std::uint32_t add_mod(std::uint32_t a, std::uint32_t b) {
    std::uint64_t value = static_cast<std::uint64_t>(a) + b;
    value = (value & P) + (value >> 31U);
    if (value >= P) {
        value -= P;
    }
    return static_cast<std::uint32_t>(value);
}

std::uint32_t sub_mod(std::uint32_t a, std::uint32_t b) {
    return a >= b ? a - b : static_cast<std::uint32_t>(static_cast<std::uint64_t>(a) + P - b);
}

std::uint32_t mul_mod(std::uint32_t a, std::uint32_t b) {
    std::uint64_t value = static_cast<std::uint64_t>(a) * b;
    value = (value & P) + (value >> 31U);
    value = (value & P) + (value >> 31U);
    if (value >= P) {
        value -= P;
    }
    return static_cast<std::uint32_t>(value);
}

std::uint32_t pow_mod(std::uint32_t base, std::uint32_t exponent) {
    std::uint32_t result = 1U;
    while (exponent != 0U) {
        if ((exponent & 1U) != 0U) {
            result = mul_mod(result, base);
        }
        base = mul_mod(base, base);
        exponent >>= 1U;
    }
    return result;
}

std::uint32_t inverse(std::uint32_t value) {
    if (value == 0U) {
        throw std::runtime_error("inverse of zero");
    }
    return pow_mod(value, P - 2U);
}

using Polynomial = std::vector<std::uint32_t>;

Polynomial locator(const std::vector<std::uint32_t>& roots) {
    Polynomial result{1U};
    for (const auto root : roots) {
        Polynomial next(result.size() + 1U, 0U);
        for (std::size_t index = 0; index < result.size(); ++index) {
            next[index] = sub_mod(next[index], mul_mod(root, result[index]));
            next[index + 1U] = add_mod(next[index + 1U], result[index]);
        }
        result = std::move(next);
    }
    return result;
}

std::uint32_t evaluate(const Polynomial& polynomial, std::uint32_t x) {
    std::uint32_t result = 0U;
    for (auto iterator = polynomial.rbegin(); iterator != polynomial.rend(); ++iterator) {
        result = add_mod(mul_mod(result, x), *iterator);
    }
    return result;
}

struct Fixture {
    std::vector<std::uint32_t> core;
    std::vector<std::vector<std::uint32_t>> branches;
    std::vector<std::unordered_set<std::uint32_t>> branch_sets;
};

Fixture read_fixture(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("cannot open fixture");
    }
    std::uint32_t field = 0U;
    std::size_t core_size = 0U;
    input >> field >> core_size;
    if (field != P || core_size != 509U) {
        throw std::runtime_error("fixture header");
    }
    Fixture fixture;
    fixture.core.resize(core_size);
    for (auto& value : fixture.core) {
        input >> value;
    }
    std::size_t branch_count = 0U;
    input >> branch_count;
    if (branch_count != 16U) {
        throw std::runtime_error("branch count");
    }
    fixture.branches.resize(branch_count);
    fixture.branch_sets.resize(branch_count);
    for (std::size_t branch = 0; branch < branch_count; ++branch) {
        std::uint32_t a = 0U;
        std::uint32_t b = 0U;
        std::size_t size = 0U;
        input >> a >> b >> size;
        (void)a;
        (void)b;
        if (size != 35U) {
            throw std::runtime_error("branch size");
        }
        fixture.branches[branch].resize(size);
        for (auto& value : fixture.branches[branch]) {
            input >> value;
            fixture.branch_sets[branch].insert(value);
        }
        if (fixture.branch_sets[branch].size() != size) {
            throw std::runtime_error("duplicate branch label");
        }
    }
    return fixture;
}

std::vector<std::uint32_t> set_union_for(
    const Fixture& fixture,
    const std::vector<int>& indices
) {
    std::set<std::uint32_t> values;
    for (const auto index : indices) {
        values.insert(fixture.branches[static_cast<std::size_t>(index)].begin(),
                      fixture.branches[static_cast<std::size_t>(index)].end());
    }
    return {values.begin(), values.end()};
}

std::vector<std::uint32_t> set_difference(
    const std::vector<std::uint32_t>& universe,
    const std::unordered_set<std::uint32_t>& removed
) {
    std::vector<std::uint32_t> result;
    for (const auto value : universe) {
        if (!removed.contains(value)) {
            result.push_back(value);
        }
    }
    return result;
}

struct Vec3 {
    std::uint32_t a = 0U;
    std::uint32_t b = 0U;
    std::uint32_t c = 0U;

    auto operator<=>(const Vec3&) const = default;
};

std::uint32_t coordinate(const Vec3& value, int index) {
    if (index == 0) {
        return value.a;
    }
    if (index == 1) {
        return value.b;
    }
    return value.c;
}

Vec3 scale(const Vec3& value, std::uint32_t factor) {
    return {mul_mod(value.a, factor), mul_mod(value.b, factor), mul_mod(value.c, factor)};
}

int first_nonzero(const Vec3& value) {
    if (value.a != 0U) {
        return 0;
    }
    if (value.b != 0U) {
        return 1;
    }
    if (value.c != 0U) {
        return 2;
    }
    return -1;
}

Vec3 cross(const Vec3& left, const Vec3& right) {
    return {
        sub_mod(mul_mod(left.b, right.c), mul_mod(left.c, right.b)),
        sub_mod(mul_mod(left.c, right.a), mul_mod(left.a, right.c)),
        sub_mod(mul_mod(left.a, right.b), mul_mod(left.b, right.a)),
    };
}

template <class Item, class Getter, class Setter>
void batch_projective_normalize(std::vector<Item>& items, Getter getter, Setter setter) {
    for (int pivot = 0; pivot < 3; ++pivot) {
        std::vector<std::size_t> indices;
        indices.reserve(items.size());
        for (std::size_t index = 0; index < items.size(); ++index) {
            if (first_nonzero(getter(items[index])) == pivot) {
                indices.push_back(index);
            }
        }
        if (indices.empty()) {
            continue;
        }
        std::vector<std::uint32_t> prefix(indices.size() + 1U, 1U);
        for (std::size_t index = 0; index < indices.size(); ++index) {
            prefix[index + 1U] = mul_mod(
                prefix[index], coordinate(getter(items[indices[index]]), pivot)
            );
        }
        std::uint32_t suffix = inverse(prefix.back());
        for (std::size_t reverse = indices.size(); reverse > 0U; --reverse) {
            const std::size_t local = reverse - 1U;
            const std::size_t item_index = indices[local];
            const auto value = getter(items[item_index]);
            const std::uint32_t pivot_inverse = mul_mod(suffix, prefix[local]);
            suffix = mul_mod(suffix, coordinate(value, pivot));
            setter(items[item_index], scale(value, pivot_inverse));
        }
    }
}

struct WeightedRow {
    Vec3 key;
    std::uint32_t weight = 1U;
};

struct CrossRecord {
    Vec3 key;
    std::uint32_t weight_sum = 0U;
};

std::uint32_t exact_line_count(std::uint64_t pair_count) {
    std::uint64_t low = 0U;
    std::uint64_t high = 2U;
    while (high * (high - 1U) / 2U < pair_count) {
        high *= 2U;
    }
    while (low + 1U < high) {
        const auto middle = (low + high) / 2U;
        if (middle * (middle - 1U) / 2U < pair_count) {
            low = middle;
        } else {
            high = middle;
        }
    }
    if (high * (high - 1U) / 2U != pair_count) {
        throw std::runtime_error("nontriangular concurrence bucket");
    }
    return static_cast<std::uint32_t>(high);
}

std::string histogram_json(const std::map<int, int>& histogram) {
    std::string result = "{";
    bool first = true;
    for (const auto& [key, value] : histogram) {
        if (!first) {
            result += ",";
        }
        first = false;
        result += "\"" + std::to_string(key) + "\":" + std::to_string(value);
    }
    result += "}";
    return result;
}

struct PairSummary {
    std::map<int, int> residual_degree_histogram;
    std::map<int, int> interior_root_histogram;
    std::map<int, int> degree_drop_root_histogram;
    int global_interior_maximum = 0;
    int global_degree_drop_maximum = 0;
};

PairSummary classify_pairs(const Fixture& fixture) {
    PairSummary summary;
    for (int left = 0; left < 16; ++left) {
        for (int right = left + 1; right < 16; ++right) {
            const auto union_values = set_union_for(fixture, {left, right});
            const auto left_roots = set_difference(
                union_values, fixture.branch_sets[static_cast<std::size_t>(left)]
            );
            const auto right_roots = set_difference(
                union_values, fixture.branch_sets[static_cast<std::size_t>(right)]
            );
            const int degree = static_cast<int>(left_roots.size());
            if (right_roots.size() != left_roots.size()) {
                throw std::runtime_error("pair residual degrees");
            }
            const auto left_polynomial = locator(left_roots);
            const auto right_polynomial = locator(right_roots);
            std::unordered_map<std::uint32_t, int> buckets;
            buckets.reserve(fixture.core.size() + union_values.size());
            int degree_drop_roots = 0;
            std::vector<std::uint32_t> allowed = fixture.core;
            allowed.insert(allowed.end(), union_values.begin(), union_values.end());
            for (const auto x : allowed) {
                const auto a = evaluate(left_polynomial, x);
                const auto b = evaluate(right_polynomial, x);
                if (a == b) {
                    ++degree_drop_roots;
                    continue;
                }
                const auto lambda = mul_mod(a, inverse(sub_mod(a, b)));
                ++buckets[lambda];
            }
            if (buckets[0U] != degree || buckets[1U] != degree) {
                throw std::runtime_error("pair endpoint root count");
            }
            int maximum = 0;
            for (const auto& [lambda, count] : buckets) {
                if (lambda != 0U && lambda != 1U) {
                    maximum = std::max(maximum, count);
                }
            }
            ++summary.residual_degree_histogram[degree];
            ++summary.interior_root_histogram[maximum];
            ++summary.degree_drop_root_histogram[degree_drop_roots];
            summary.global_interior_maximum = std::max(summary.global_interior_maximum, maximum);
            summary.global_degree_drop_maximum = std::max(
                summary.global_degree_drop_maximum, degree_drop_roots
            );
        }
    }
    return summary;
}

struct TripleSummary {
    std::map<int, int> residual_degree_histogram;
    std::map<int, int> interior_root_histogram;
    std::vector<std::array<int, 4>> maximum_three_triples;
    int global_interior_maximum = 0;
    int global_split_gap = 1000000;
};

TripleSummary classify_triples(const Fixture& fixture) {
    TripleSummary summary;
    for (int first = 0; first < 16; ++first) {
        for (int second = first + 1; second < 16; ++second) {
            for (int third = second + 1; third < 16; ++third) {
                const std::vector<int> indices{first, second, third};
                const auto union_values = set_union_for(fixture, indices);
                std::array<Polynomial, 3> residuals;
                for (int local = 0; local < 3; ++local) {
                    residuals[static_cast<std::size_t>(local)] = locator(set_difference(
                        union_values,
                        fixture.branch_sets[static_cast<std::size_t>(indices[static_cast<std::size_t>(local)])]
                    ));
                }
                const int degree = static_cast<int>(residuals[0].size() - 1U);
                if (residuals[1].size() != residuals[0].size()
                    || residuals[2].size() != residuals[0].size()) {
                    throw std::runtime_error("triple residual degrees");
                }

                std::vector<WeightedRow> rows;
                rows.reserve(fixture.core.size() + union_values.size());
                auto append_row = [&](std::uint32_t x) {
                    Vec3 row{
                        evaluate(residuals[0], x),
                        evaluate(residuals[1], x),
                        evaluate(residuals[2], x),
                    };
                    if (first_nonzero(row) < 0) {
                        throw std::runtime_error("zero residual row");
                    }
                    rows.push_back({row, 1U});
                };
                for (const auto x : fixture.core) {
                    append_row(x);
                }
                for (const auto x : union_values) {
                    append_row(x);
                }
                batch_projective_normalize(
                    rows,
                    [](const WeightedRow& row) { return row.key; },
                    [](WeightedRow& row, const Vec3& value) { row.key = value; }
                );
                std::sort(rows.begin(), rows.end(), [](const auto& left, const auto& right) {
                    return left.key < right.key;
                });
                std::vector<WeightedRow> classes;
                for (const auto& row : rows) {
                    if (!classes.empty() && classes.back().key == row.key) {
                        ++classes.back().weight;
                    } else {
                        classes.push_back(row);
                    }
                }
                int maximum = 0;
                for (const auto& row : classes) {
                    const int support = static_cast<int>(row.key.a != 0U)
                        + static_cast<int>(row.key.b != 0U)
                        + static_cast<int>(row.key.c != 0U);
                    const bool degree_drop_line = row.key.a == row.key.b
                        && row.key.b == row.key.c;
                    if (support >= 2 && !degree_drop_line) {
                        maximum = std::max(maximum, static_cast<int>(row.weight));
                    }
                }

                std::vector<CrossRecord> intersections;
                intersections.reserve(classes.size() * (classes.size() - 1U) / 2U);
                for (std::size_t left = 0; left < classes.size(); ++left) {
                    for (std::size_t right = left + 1U; right < classes.size(); ++right) {
                        const auto point = cross(classes[left].key, classes[right].key);
                        if (first_nonzero(point) < 0) {
                            throw std::runtime_error("proportional row classes");
                        }
                        intersections.push_back(
                            {point, classes[left].weight + classes[right].weight}
                        );
                    }
                }
                batch_projective_normalize(
                    intersections,
                    [](const CrossRecord& record) { return record.key; },
                    [](CrossRecord& record, const Vec3& value) { record.key = value; }
                );
                std::sort(
                    intersections.begin(), intersections.end(),
                    [](const auto& left, const auto& right) { return left.key < right.key; }
                );
                std::size_t cursor = 0U;
                while (cursor < intersections.size()) {
                    std::size_t end = cursor + 1U;
                    std::uint64_t weight_sum = intersections[cursor].weight_sum;
                    while (end < intersections.size()
                           && intersections[end].key == intersections[cursor].key) {
                        weight_sum += intersections[end].weight_sum;
                        ++end;
                    }
                    const auto alpha = intersections[cursor].key;
                    const bool full_support = alpha.a != 0U && alpha.b != 0U && alpha.c != 0U;
                    const bool full_degree = add_mod(add_mod(alpha.a, alpha.b), alpha.c) != 0U;
                    if (full_support && full_degree) {
                        const auto line_count = exact_line_count(end - cursor);
                        if (line_count < 2U || weight_sum % (line_count - 1U) != 0U) {
                            throw std::runtime_error("weighted concurrence identity");
                        }
                        const auto root_count = weight_sum / (line_count - 1U);
                        maximum = std::max(maximum, static_cast<int>(root_count));
                    }
                    cursor = end;
                }

                ++summary.residual_degree_histogram[degree];
                ++summary.interior_root_histogram[maximum];
                if (maximum == 3) {
                    summary.maximum_three_triples.push_back({first, second, third, degree});
                }
                summary.global_interior_maximum = std::max(summary.global_interior_maximum, maximum);
                summary.global_split_gap = std::min(summary.global_split_gap, degree - maximum);
                if (maximum >= degree) {
                    throw std::runtime_error("new support-three split locator");
                }
            }
        }
    }
    return summary;
}

void write_output(
    const std::string& path,
    const PairSummary& pairs,
    const TripleSummary& triples
) {
    std::ofstream output(path);
    if (!output) {
        throw std::runtime_error("cannot open output");
    }
    output << "{\n"
           << "  \"schema\": \"sp01zxa5-sparse-syndrome-locator-hull/v1\",\n"
           << "  \"claim_id\": \"SP01ZXA5_SPARSE_SYNDROME_LOCATOR_HULL_RIGIDITY\",\n"
           << "  \"status\": \"PASS_EXACT_SUPPORT_TWO_AND_THREE_CLASSIFICATION\",\n"
           << "  \"field\": " << P << ",\n"
           << "  \"pair_count\": 120,\n"
           << "  \"pair_residual_degree_histogram\": "
           << histogram_json(pairs.residual_degree_histogram) << ",\n"
           << "  \"pair_interior_root_histogram\": "
           << histogram_json(pairs.interior_root_histogram) << ",\n"
           << "  \"pair_global_interior_root_maximum\": "
           << pairs.global_interior_maximum << ",\n"
           << "  \"pair_degree_drop_root_histogram\": "
           << histogram_json(pairs.degree_drop_root_histogram) << ",\n"
           << "  \"pair_global_degree_drop_root_maximum\": "
           << pairs.global_degree_drop_maximum << ",\n"
           << "  \"triple_count\": 560,\n"
           << "  \"triple_residual_degree_histogram\": "
           << histogram_json(triples.residual_degree_histogram) << ",\n"
           << "  \"triple_interior_root_histogram\": "
           << histogram_json(triples.interior_root_histogram) << ",\n"
           << "  \"triple_global_interior_root_maximum\": "
           << triples.global_interior_maximum << ",\n"
           << "  \"triple_global_split_gap\": " << triples.global_split_gap << ",\n"
           << "  \"triple_maximum_three_cases\": [";
    for (std::size_t index = 0; index < triples.maximum_three_triples.size(); ++index) {
        if (index != 0U) {
            output << ",";
        }
        const auto& row = triples.maximum_three_triples[index];
        output << "{\"indices\":[" << row[0] << "," << row[1] << "," << row[2]
               << "],\"residual_degree\":" << row[3] << "}";
    }
    output << "],\n"
           << "  \"new_split_locator_with_coefficient_support_at_most_three\": false,\n"
           << "  \"scope_guard\": \"Classification inside the affine hull of the sixteen known syndrome locators for coefficient support at most three; denser combinations and arbitrary outsiders remain open.\"\n"
           << "}\n";
}

}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 3) {
            std::cerr << "usage: verifier FIXTURE OUTPUT\n";
            return 2;
        }
        const auto fixture = read_fixture(argv[1]);
        const auto pairs = classify_pairs(fixture);
        const auto triples = classify_triples(fixture);
        write_output(argv[2], pairs, triples);
        std::cout << "PASS SP01zxa5 sparse syndrome-locator hull rigidity\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "FAIL: " << error.what() << '\n';
        return 1;
    }
}
