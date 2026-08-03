#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

#include <omp.h>

namespace {

constexpr std::uint32_t P = 2147483647U;
constexpr int BRANCHES = 16;
constexpr int CORE_SIZE = 509;
constexpr int GROUP_SIZE = 20;
constexpr int FULL_GROUPS = 25;

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

struct Fixture {
    std::array<std::uint32_t, CORE_SIZE> core{};
    std::vector<std::uint32_t> outside;
    std::vector<std::uint16_t> incidence_masks;
};

Fixture read_fixture(const std::string& path) {
    std::ifstream input(path);
    std::uint32_t field = 0U;
    int core_size = 0;
    input >> field >> core_size;
    if (!input || field != P || core_size != CORE_SIZE) {
        throw std::runtime_error("fixture header");
    }
    Fixture fixture;
    for (auto& value : fixture.core) {
        input >> value;
    }
    int branch_count = 0;
    input >> branch_count;
    if (branch_count != BRANCHES) {
        throw std::runtime_error("branch count");
    }
    std::unordered_map<std::uint32_t, std::uint16_t> masks;
    masks.reserve(600U);
    for (int branch = 0; branch < BRANCHES; ++branch) {
        std::uint32_t a = 0U;
        std::uint32_t b = 0U;
        int size = 0;
        input >> a >> b >> size;
        (void)a;
        (void)b;
        if (size != 35) {
            throw std::runtime_error("branch size");
        }
        for (int index = 0; index < size; ++index) {
            std::uint32_t label = 0U;
            input >> label;
            masks[label] = static_cast<std::uint16_t>(
                masks[label] | static_cast<std::uint16_t>(1U << branch)
            );
        }
    }
    fixture.outside.reserve(masks.size());
    for (const auto& [label, mask] : masks) {
        (void)mask;
        fixture.outside.push_back(label);
    }
    std::sort(fixture.outside.begin(), fixture.outside.end());
    if (fixture.outside.size() != 514U) {
        throw std::runtime_error("outside size");
    }
    fixture.incidence_masks.reserve(fixture.outside.size());
    for (const auto label : fixture.outside) {
        fixture.incidence_masks.push_back(masks.at(label));
    }
    return fixture;
}

using Evaluations = std::array<std::array<std::uint32_t, BRANCHES>, CORE_SIZE>;

Evaluations build_locator_evaluations(const Fixture& fixture) {
    Evaluations values{};
    for (int branch = 0; branch < BRANCHES; ++branch) {
        const auto bit = static_cast<std::uint16_t>(1U << branch);
        for (int core_index = 0; core_index < CORE_SIZE; ++core_index) {
            std::uint32_t result = 1U;
            const auto x = fixture.core[static_cast<std::size_t>(core_index)];
            for (std::size_t outside_index = 0; outside_index < fixture.outside.size(); ++outside_index) {
                if ((fixture.incidence_masks[outside_index] & bit) == 0U) {
                    result = mul_mod(result, sub_mod(x, fixture.outside[outside_index]));
                }
            }
            if (result == 0U) {
                throw std::runtime_error("outside locator vanishes on core");
            }
            values[static_cast<std::size_t>(core_index)][static_cast<std::size_t>(branch)] = result;
        }
    }
    return values;
}

struct Vec4 {
    std::uint32_t a = 0U;
    std::uint32_t b = 0U;
    std::uint32_t c = 0U;
    std::uint32_t d = 0U;
    auto operator<=>(const Vec4&) const = default;
};

int first_nonzero(const Vec4& value) {
    if (value.a != 0U) {
        return 0;
    }
    if (value.b != 0U) {
        return 1;
    }
    if (value.c != 0U) {
        return 2;
    }
    if (value.d != 0U) {
        return 3;
    }
    return -1;
}

std::uint32_t coordinate(const Vec4& value, int index) {
    if (index == 0) {
        return value.a;
    }
    if (index == 1) {
        return value.b;
    }
    if (index == 2) {
        return value.c;
    }
    return value.d;
}

Vec4 scale(const Vec4& value, std::uint32_t factor) {
    return {
        mul_mod(value.a, factor),
        mul_mod(value.b, factor),
        mul_mod(value.c, factor),
        mul_mod(value.d, factor),
    };
}

std::uint32_t determinant3(
    std::uint32_t a00, std::uint32_t a01, std::uint32_t a02,
    std::uint32_t a10, std::uint32_t a11, std::uint32_t a12,
    std::uint32_t a20, std::uint32_t a21, std::uint32_t a22
) {
    const auto positive = add_mod(
        add_mod(mul_mod(a00, mul_mod(a11, a22)), mul_mod(a01, mul_mod(a12, a20))),
        mul_mod(a02, mul_mod(a10, a21))
    );
    const auto negative = add_mod(
        add_mod(mul_mod(a02, mul_mod(a11, a20)), mul_mod(a01, mul_mod(a10, a22))),
        mul_mod(a00, mul_mod(a12, a21))
    );
    return sub_mod(positive, negative);
}

Vec4 null_normal(const Vec4& x, const Vec4& y, const Vec4& z) {
    const auto n0 = determinant3(x.b, x.c, x.d, y.b, y.c, y.d, z.b, z.c, z.d);
    const auto n1 = determinant3(x.a, x.c, x.d, y.a, y.c, y.d, z.a, z.c, z.d);
    const auto n2 = determinant3(x.a, x.b, x.d, y.a, y.b, y.d, z.a, z.b, z.d);
    const auto n3 = determinant3(x.a, x.b, x.c, y.a, y.b, y.c, z.a, z.b, z.c);
    return {n0, n1 == 0U ? 0U : P - n1, n2, n3 == 0U ? 0U : P - n3};
}

std::uint32_t dot(const Vec4& left, const Vec4& right) {
    return add_mod(
        add_mod(mul_mod(left.a, right.a), mul_mod(left.b, right.b)),
        add_mod(mul_mod(left.c, right.c), mul_mod(left.d, right.d))
    );
}

bool valid_support_four_normal(const Vec4& value) {
    return value.a != 0U && value.b != 0U && value.c != 0U && value.d != 0U
        && add_mod(add_mod(value.a, value.b), add_mod(value.c, value.d)) != 0U;
}

void batch_normalize(std::vector<Vec4>& values) {
    for (int pivot = 0; pivot < 4; ++pivot) {
        std::vector<std::size_t> indices;
        indices.reserve(values.size());
        for (std::size_t index = 0; index < values.size(); ++index) {
            if (first_nonzero(values[index]) == pivot) {
                indices.push_back(index);
            }
        }
        if (indices.empty()) {
            continue;
        }
        std::vector<std::uint32_t> prefix(indices.size() + 1U, 1U);
        for (std::size_t index = 0; index < indices.size(); ++index) {
            prefix[index + 1U] = mul_mod(
                prefix[index], coordinate(values[indices[index]], pivot)
            );
        }
        auto suffix = inverse(prefix.back());
        for (std::size_t reverse = indices.size(); reverse > 0U; --reverse) {
            const auto local = reverse - 1U;
            const auto item = indices[local];
            const auto old = values[item];
            const auto old_pivot = coordinate(old, pivot);
            const auto pivot_inverse = mul_mod(suffix, prefix[local]);
            suffix = mul_mod(suffix, old_pivot);
            values[item] = scale(old, pivot_inverse);
        }
    }
}

std::uint64_t choose2(int value) {
    return value < 2 ? 0U : static_cast<std::uint64_t>(value) * (value - 1) / 2U;
}

std::uint64_t choose3(int value) {
    return value < 3 ? 0U
        : static_cast<std::uint64_t>(value) * (value - 1) * (value - 2) / 6U;
}

std::array<int, 510> build_forced_bucket_table() {
    constexpr std::uint64_t INF = std::numeric_limits<std::uint64_t>::max() / 4U;
    std::array<std::uint64_t, 510> dynamic{};
    dynamic.fill(INF);
    dynamic[0] = 0U;
    std::array<int, 26> capacities{};
    capacities.fill(GROUP_SIZE);
    capacities.back() = CORE_SIZE - FULL_GROUPS * GROUP_SIZE;
    for (const auto capacity : capacities) {
        std::array<std::uint64_t, 510> next{};
        next.fill(INF);
        for (int total = 0; total <= CORE_SIZE; ++total) {
            if (dynamic[static_cast<std::size_t>(total)] == INF) {
                continue;
            }
            for (int load = 0; load <= capacity && total + load <= CORE_SIZE; ++load) {
                const auto dependent_upper = choose2(load) / 3U;
                const auto independent_lower = choose3(load) - dependent_upper;
                auto& target = next[static_cast<std::size_t>(total + load)];
                target = std::min(target, dynamic[static_cast<std::size_t>(total)] + independent_lower);
            }
        }
        dynamic = next;
    }
    std::array<int, 510> answer{};
    for (int roots = 0; roots <= CORE_SIZE; ++roots) {
        if (dynamic[static_cast<std::size_t>(roots)] > static_cast<std::uint64_t>(std::numeric_limits<int>::max())) {
            throw std::runtime_error("forced bucket overflow");
        }
        answer[static_cast<std::size_t>(roots)] = static_cast<int>(dynamic[static_cast<std::size_t>(roots)]);
    }
    return answer;
}

struct QuadrupleResult {
    std::array<int, 4> indices{};
    int residual_degree = 0;
    int outside_overlap_upper = 0;
    int required_core_roots = 0;
    int forced_bucket_lower = 0;
    int observed_bucket_maximum = 0;
    int independent_triples_generated = 0;
};

std::vector<std::array<int, 4>> all_quadruples() {
    std::vector<std::array<int, 4>> result;
    result.reserve(1820U);
    for (int a = 0; a < BRANCHES; ++a) {
        for (int b = a + 1; b < BRANCHES; ++b) {
            for (int c = b + 1; c < BRANCHES; ++c) {
                for (int d = c + 1; d < BRANCHES; ++d) {
                    result.push_back({a, b, c, d});
                }
            }
        }
    }
    return result;
}

QuadrupleResult process_quadruple(
    const Fixture& fixture,
    const Evaluations& evaluations,
    const std::array<int, 4>& indices,
    const std::array<int, 510>& forced_table
) {
    QuadrupleResult result;
    result.indices = indices;
    std::uint16_t support_mask = 0U;
    for (const auto index : indices) {
        support_mask = static_cast<std::uint16_t>(support_mask | (1U << index));
    }
    int union_size = 0;
    int overlap = 0;
    for (const auto mask : fixture.incidence_masks) {
        const auto active = static_cast<std::uint16_t>(mask & support_mask);
        if (active != 0U) {
            ++union_size;
            if (std::popcount(active) >= 2) {
                ++overlap;
            }
        }
    }
    result.residual_degree = union_size - 35;
    result.outside_overlap_upper = overlap;
    result.required_core_roots = result.residual_degree - overlap;
    result.forced_bucket_lower = forced_table[static_cast<std::size_t>(result.required_core_roots)];

    std::array<Vec4, CORE_SIZE> rows{};
    for (int core_index = 0; core_index < CORE_SIZE; ++core_index) {
        rows[static_cast<std::size_t>(core_index)] = {
            evaluations[static_cast<std::size_t>(core_index)][static_cast<std::size_t>(indices[0])],
            evaluations[static_cast<std::size_t>(core_index)][static_cast<std::size_t>(indices[1])],
            evaluations[static_cast<std::size_t>(core_index)][static_cast<std::size_t>(indices[2])],
            evaluations[static_cast<std::size_t>(core_index)][static_cast<std::size_t>(indices[3])],
        };
    }

    std::vector<Vec4> normals;
    normals.reserve(28584U);
    for (int group = 0; group <= FULL_GROUPS; ++group) {
        const int begin = group * GROUP_SIZE;
        const int end = std::min(begin + GROUP_SIZE, CORE_SIZE);
        for (int first = begin; first < end; ++first) {
            for (int second = first + 1; second < end; ++second) {
                for (int third = second + 1; third < end; ++third) {
                    const auto normal = null_normal(
                        rows[static_cast<std::size_t>(first)],
                        rows[static_cast<std::size_t>(second)],
                        rows[static_cast<std::size_t>(third)]
                    );
                    if (first_nonzero(normal) < 0 || !valid_support_four_normal(normal)) {
                        continue;
                    }
                    if (dot(rows[static_cast<std::size_t>(first)], normal) != 0U
                        || dot(rows[static_cast<std::size_t>(second)], normal) != 0U
                        || dot(rows[static_cast<std::size_t>(third)], normal) != 0U) {
                        throw std::runtime_error("cofactor normal identity");
                    }
                    normals.push_back(normal);
                }
            }
        }
    }
    result.independent_triples_generated = static_cast<int>(normals.size());
    batch_normalize(normals);
    std::sort(normals.begin(), normals.end());
    int maximum = 0;
    std::size_t cursor = 0U;
    while (cursor < normals.size()) {
        std::size_t end = cursor + 1U;
        while (end < normals.size() && normals[end] == normals[cursor]) {
            ++end;
        }
        maximum = std::max(maximum, static_cast<int>(end - cursor));
        cursor = end;
    }
    result.observed_bucket_maximum = maximum;
    return result;
}

std::string histogram_json(const std::map<int, int>& histogram) {
    std::string answer = "{";
    bool first = true;
    for (const auto& [key, value] : histogram) {
        if (!first) {
            answer += ",";
        }
        first = false;
        answer += "\"" + std::to_string(key) + "\":" + std::to_string(value);
    }
    return answer + "}";
}

void write_output(const std::string& path, const std::vector<QuadrupleResult>& results) {
    std::map<int, int> degree_histogram;
    std::map<int, int> overlap_histogram;
    std::map<int, int> required_histogram;
    std::map<int, int> forced_histogram;
    std::map<int, int> observed_histogram;
    int global_forced_minimum = std::numeric_limits<int>::max();
    int global_observed_maximum = 0;
    int global_bucket_margin = std::numeric_limits<int>::max();
    std::uint64_t generated_total = 0U;
    std::vector<QuadrupleResult> tight;
    const auto forced_table = build_forced_bucket_table();
    for (const auto& result : results) {
        ++degree_histogram[result.residual_degree];
        ++overlap_histogram[result.outside_overlap_upper];
        ++required_histogram[result.required_core_roots];
        ++forced_histogram[result.forced_bucket_lower];
        ++observed_histogram[result.observed_bucket_maximum];
        global_forced_minimum = std::min(global_forced_minimum, result.forced_bucket_lower);
        global_observed_maximum = std::max(global_observed_maximum, result.observed_bucket_maximum);
        global_bucket_margin = std::min(
            global_bucket_margin,
            result.forced_bucket_lower - result.observed_bucket_maximum
        );
        generated_total += static_cast<std::uint64_t>(result.independent_triples_generated);
        if (result.forced_bucket_lower - result.observed_bucket_maximum == global_bucket_margin) {
            tight.push_back(result);
        }
        if (result.observed_bucket_maximum >= result.forced_bucket_lower) {
            throw std::runtime_error("support-four candidate survives partition sieve");
        }
    }
    std::erase_if(tight, [global_bucket_margin](const auto& result) {
        return result.forced_bucket_lower - result.observed_bucket_maximum != global_bucket_margin;
    });
    int certified_core_root_cap = 0;
    for (int roots = 0; roots <= CORE_SIZE; ++roots) {
        if (forced_table[static_cast<std::size_t>(roots)] <= global_observed_maximum) {
            certified_core_root_cap = roots;
        }
    }
    int certified_residual_root_margin = std::numeric_limits<int>::max();
    for (const auto& result : results) {
        certified_residual_root_margin = std::min(
            certified_residual_root_margin,
            result.required_core_roots - certified_core_root_cap
        );
    }

    std::ofstream output(path);
    if (!output) {
        throw std::runtime_error("cannot open output");
    }
    output << "{\n"
           << "  \"schema\": \"sp01zxa6-support-four-partition-sieve/v1\",\n"
           << "  \"claim_id\": \"SP01ZXA6_SUPPORT_FOUR_PARTITION_SIEVE\",\n"
           << "  \"status\": \"PASS_EXACT_SUPPORT_FOUR_EXCLUSION\",\n"
           << "  \"field\": " << P << ",\n"
           << "  \"quadruple_count\": " << results.size() << ",\n"
           << "  \"partition_capacities\": [";
    for (int group = 0; group < FULL_GROUPS; ++group) {
        if (group != 0) {
            output << ",";
        }
        output << GROUP_SIZE;
    }
    output << "," << CORE_SIZE - FULL_GROUPS * GROUP_SIZE << "],\n"
           << "  \"projective_root_line_cap\": 3,\n"
           << "  \"residual_degree_histogram\": " << histogram_json(degree_histogram) << ",\n"
           << "  \"outside_overlap_upper_histogram\": " << histogram_json(overlap_histogram) << ",\n"
           << "  \"required_core_root_histogram\": " << histogram_json(required_histogram) << ",\n"
           << "  \"forced_bucket_lower_histogram\": " << histogram_json(forced_histogram) << ",\n"
           << "  \"observed_bucket_histogram\": " << histogram_json(observed_histogram) << ",\n"
           << "  \"global_forced_bucket_minimum\": " << global_forced_minimum << ",\n"
           << "  \"global_observed_bucket_maximum\": " << global_observed_maximum << ",\n"
           << "  \"minimum_rowwise_bucket_margin\": " << global_bucket_margin << ",\n"
           << "  \"certified_core_root_cap\": " << certified_core_root_cap << ",\n"
           << "  \"minimum_residual_root_margin\": " << certified_residual_root_margin << ",\n"
           << "  \"independent_triple_normals_generated\": " << generated_total << ",\n"
           << "  \"tight_cases\": [";
    for (std::size_t index = 0; index < tight.size(); ++index) {
        if (index != 0U) {
            output << ",";
        }
        const auto& row = tight[index];
        output << "{\"indices\":[" << row.indices[0] << "," << row.indices[1] << ","
               << row.indices[2] << "," << row.indices[3] << "],"
               << "\"degree\":" << row.residual_degree << ","
               << "\"required_core_roots\":" << row.required_core_roots << ","
               << "\"forced\":" << row.forced_bucket_lower << ","
               << "\"observed\":" << row.observed_bucket_maximum << "}";
    }
    output << "],\n"
           << "  \"new_split_locator_with_exact_coefficient_support_four\": false,\n"
           << "  \"scope_guard\": \"Exact support-four classification inside the affine hull of the sixteen known syndrome locators. Support five or more and arbitrary syndrome-section split locators remain open.\"\n"
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
        const auto evaluations = build_locator_evaluations(fixture);
        const auto forced_table = build_forced_bucket_table();
        const auto quadruples = all_quadruples();
        std::vector<QuadrupleResult> results(quadruples.size());
#pragma omp parallel for schedule(dynamic, 1)
        for (int index = 0; index < static_cast<int>(quadruples.size()); ++index) {
            results[static_cast<std::size_t>(index)] = process_quadruple(
                fixture,
                evaluations,
                quadruples[static_cast<std::size_t>(index)],
                forced_table
            );
        }
        write_output(argv[2], results);
        std::cout << "PASS SP01zxa6 exact support-four partition sieve\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "FAIL: " << error.what() << '\n';
        return 1;
    }
}
