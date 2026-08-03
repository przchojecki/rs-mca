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
constexpr int SUPPORT = 5;
constexpr int GROUP_SIZE = 14;
constexpr int FULL_GROUPS = 36;

std::uint32_t add_mod(std::uint32_t a, std::uint32_t b) {
    std::uint64_t value = static_cast<std::uint64_t>(a) + b;
    value = (value & P) + (value >> 31U);
    return static_cast<std::uint32_t>(value >= P ? value - P : value);
}

std::uint32_t sub_mod(std::uint32_t a, std::uint32_t b) {
    return a >= b ? a - b : static_cast<std::uint32_t>(static_cast<std::uint64_t>(a) + P - b);
}

std::uint32_t neg_mod(std::uint32_t value) {
    return value == 0U ? 0U : P - value;
}

std::uint32_t mul_mod(std::uint32_t a, std::uint32_t b) {
    std::uint64_t value = static_cast<std::uint64_t>(a) * b;
    value = (value & P) + (value >> 31U);
    value = (value & P) + (value >> 31U);
    return static_cast<std::uint32_t>(value >= P ? value - P : value);
}

std::uint32_t power(std::uint32_t base, std::uint32_t exponent) {
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

struct Fixture {
    std::array<std::uint32_t, CORE_SIZE> core{};
    std::vector<std::uint32_t> outside;
    std::vector<std::uint16_t> masks;
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
        std::uint32_t ignored_a = 0U;
        std::uint32_t ignored_b = 0U;
        int size = 0;
        input >> ignored_a >> ignored_b >> size;
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
    for (const auto& [label, mask] : masks) {
        (void)mask;
        fixture.outside.push_back(label);
    }
    std::sort(fixture.outside.begin(), fixture.outside.end());
    if (fixture.outside.size() != 514U) {
        throw std::runtime_error("outside universe size");
    }
    for (const auto label : fixture.outside) {
        fixture.masks.push_back(masks.at(label));
    }
    return fixture;
}

using FullEvaluations = std::array<std::array<std::uint32_t, BRANCHES>, CORE_SIZE>;

FullEvaluations build_full_locator_evaluations(const Fixture& fixture) {
    FullEvaluations values{};
    for (int branch = 0; branch < BRANCHES; ++branch) {
        const auto bit = static_cast<std::uint16_t>(1U << branch);
        for (int core_index = 0; core_index < CORE_SIZE; ++core_index) {
            const auto x = fixture.core[static_cast<std::size_t>(core_index)];
            std::uint32_t result = 1U;
            for (std::size_t outside_index = 0; outside_index < fixture.outside.size(); ++outside_index) {
                if ((fixture.masks[outside_index] & bit) == 0U) {
                    result = mul_mod(result, sub_mod(x, fixture.outside[outside_index]));
                }
            }
            if (result == 0U) {
                throw std::runtime_error("full locator vanishes on core");
            }
            values[static_cast<std::size_t>(core_index)][static_cast<std::size_t>(branch)] = result;
        }
    }
    return values;
}

struct Vec5 {
    std::array<std::uint32_t, SUPPORT> coordinate{};
    auto operator<=>(const Vec5&) const = default;
};

Vec5 fraction_free_null_normal(const std::array<Vec5, 4>& input, bool& independent) {
    std::array<std::array<std::uint32_t, SUPPORT>, 4> matrix{};
    for (int row = 0; row < 4; ++row) {
        matrix[static_cast<std::size_t>(row)] = input[static_cast<std::size_t>(row)].coordinate;
    }
    std::array<int, SUPPORT> permutation{0, 1, 2, 3, 4};
    for (int pivot = 0; pivot < 4; ++pivot) {
        int selected_row = -1;
        int selected_column = -1;
        for (int row = pivot; row < 4 && selected_row < 0; ++row) {
            for (int column = pivot; column < SUPPORT; ++column) {
                if (matrix[static_cast<std::size_t>(row)][static_cast<std::size_t>(column)] != 0U) {
                    selected_row = row;
                    selected_column = column;
                    break;
                }
            }
        }
        if (selected_row < 0) {
            independent = false;
            return {};
        }
        if (selected_row != pivot) {
            std::swap(matrix[static_cast<std::size_t>(selected_row)], matrix[static_cast<std::size_t>(pivot)]);
        }
        if (selected_column != pivot) {
            for (auto& row : matrix) {
                std::swap(row[static_cast<std::size_t>(selected_column)], row[static_cast<std::size_t>(pivot)]);
            }
            std::swap(permutation[static_cast<std::size_t>(selected_column)],
                      permutation[static_cast<std::size_t>(pivot)]);
        }
        const auto diagonal = matrix[static_cast<std::size_t>(pivot)][static_cast<std::size_t>(pivot)];
        for (int row = pivot + 1; row < 4; ++row) {
            const auto multiplier = matrix[static_cast<std::size_t>(row)][static_cast<std::size_t>(pivot)];
            for (int column = pivot + 1; column < SUPPORT; ++column) {
                matrix[static_cast<std::size_t>(row)][static_cast<std::size_t>(column)] = sub_mod(
                    mul_mod(diagonal, matrix[static_cast<std::size_t>(row)][static_cast<std::size_t>(column)]),
                    mul_mod(multiplier, matrix[static_cast<std::size_t>(pivot)][static_cast<std::size_t>(column)])
                );
            }
            matrix[static_cast<std::size_t>(row)][static_cast<std::size_t>(pivot)] = 0U;
        }
    }
    independent = true;
    const auto d0 = matrix[0][0];
    const auto d1 = matrix[1][1];
    const auto d2 = matrix[2][2];
    const auto d3 = matrix[3][3];
    const auto a = sub_mod(mul_mod(matrix[2][3], matrix[3][4]),
                           mul_mod(matrix[2][4], d3));
    const auto x4_over_d0 = mul_mod(d1, mul_mod(d2, d3));
    const auto x3_over_d0 = neg_mod(mul_mod(matrix[3][4], mul_mod(d1, d2)));
    const auto x2_over_d0 = mul_mod(d1, a);
    const auto x1_over_d0 = neg_mod(add_mod(
        sub_mod(mul_mod(matrix[1][2], a),
                mul_mod(matrix[1][3], mul_mod(matrix[3][4], d2))),
        mul_mod(matrix[1][4], mul_mod(d2, d3))
    ));
    const auto x0 = neg_mod(add_mod(
        add_mod(mul_mod(matrix[0][1], x1_over_d0), mul_mod(matrix[0][2], x2_over_d0)),
        add_mod(mul_mod(matrix[0][3], x3_over_d0), mul_mod(matrix[0][4], x4_over_d0))
    ));
    const std::array<std::uint32_t, SUPPORT> permuted{
        x0,
        mul_mod(d0, x1_over_d0),
        mul_mod(d0, x2_over_d0),
        mul_mod(d0, x3_over_d0),
        mul_mod(d0, x4_over_d0),
    };
    Vec5 answer;
    for (int column = 0; column < SUPPORT; ++column) {
        answer.coordinate[static_cast<std::size_t>(permutation[static_cast<std::size_t>(column)])] =
            permuted[static_cast<std::size_t>(column)];
    }
    return answer;
}

std::uint32_t dot(const Vec5& left, const Vec5& right) {
    std::uint32_t answer = 0U;
    for (int index = 0; index < SUPPORT; ++index) {
        answer = add_mod(answer, mul_mod(
            left.coordinate[static_cast<std::size_t>(index)],
            right.coordinate[static_cast<std::size_t>(index)]
        ));
    }
    return answer;
}

bool admissible_normal(const Vec5& value) {
    std::uint32_t sum = 0U;
    for (const auto coordinate : value.coordinate) {
        if (coordinate == 0U) {
            return false;
        }
        sum = add_mod(sum, coordinate);
    }
    return sum != 0U;
}

void batch_projectivize(std::vector<Vec5>& values) {
    if (values.empty()) {
        return;
    }
    std::vector<std::uint32_t> prefix(values.size() + 1U, 1U);
    for (std::size_t index = 0; index < values.size(); ++index) {
        prefix[index + 1U] = mul_mod(prefix[index], values[index].coordinate[0]);
    }
    auto suffix = power(prefix.back(), P - 2U);
    for (std::size_t reverse = values.size(); reverse > 0U; --reverse) {
        const auto index = reverse - 1U;
        const auto old_pivot = values[index].coordinate[0];
        const auto factor = mul_mod(suffix, prefix[index]);
        suffix = mul_mod(suffix, old_pivot);
        for (auto& coordinate : values[index].coordinate) {
            coordinate = mul_mod(coordinate, factor);
        }
    }
}

std::uint64_t choose4(int value) {
    return value < 4 ? 0U
        : static_cast<std::uint64_t>(value) * (value - 1) * (value - 2) * (value - 3) / 24U;
}

struct Result {
    std::array<int, SUPPORT> branches{};
    int degree = 0;
    int overlap = 0;
    int required = 0;
    int dependent_quadruples = 0;
    int forced = 0;
    int observed = 0;
    int core_root_cap = 0;
    int normals = 0;
};

std::array<int, CORE_SIZE + 1> build_forced_table(
    const std::array<int, FULL_GROUPS + 1>& dependent
) {
    constexpr auto INF = std::numeric_limits<std::uint64_t>::max() / 4U;
    std::array<std::uint64_t, CORE_SIZE + 1> state{};
    state.fill(INF);
    state[0] = 0U;
    for (int group = 0; group <= FULL_GROUPS; ++group) {
        const int capacity = group < FULL_GROUPS ? GROUP_SIZE : CORE_SIZE - FULL_GROUPS * GROUP_SIZE;
        std::array<std::uint64_t, CORE_SIZE + 1> next{};
        next.fill(INF);
        for (int used = 0; used <= CORE_SIZE; ++used) {
            if (state[static_cast<std::size_t>(used)] == INF) {
                continue;
            }
            for (int load = 0; load <= capacity && used + load <= CORE_SIZE; ++load) {
                const auto independent_lower = choose4(load) > static_cast<std::uint64_t>(dependent[static_cast<std::size_t>(group)])
                    ? choose4(load) - static_cast<std::uint64_t>(dependent[static_cast<std::size_t>(group)])
                    : 0U;
                auto& target = next[static_cast<std::size_t>(used + load)];
                target = std::min(target, state[static_cast<std::size_t>(used)] + independent_lower);
            }
        }
        state = next;
    }
    std::array<int, CORE_SIZE + 1> answer{};
    for (int roots = 0; roots <= CORE_SIZE; ++roots) {
        if (state[static_cast<std::size_t>(roots)] > static_cast<std::uint64_t>(std::numeric_limits<int>::max())) {
            throw std::runtime_error("forced table overflow");
        }
        answer[static_cast<std::size_t>(roots)] = static_cast<int>(state[static_cast<std::size_t>(roots)]);
    }
    return answer;
}

Result process_support(
    const Fixture& fixture,
    const FullEvaluations& evaluations,
    const std::array<int, SUPPORT>& branches
) {
    Result result;
    result.branches = branches;
    std::uint16_t support_mask = 0U;
    for (const auto branch : branches) {
        support_mask = static_cast<std::uint16_t>(support_mask | static_cast<std::uint16_t>(1U << branch));
    }
    for (const auto mask : fixture.masks) {
        const auto active = static_cast<std::uint16_t>(mask & support_mask);
        if (active != 0U) {
            ++result.degree;
            if (std::popcount(active) >= 2) {
                ++result.overlap;
            }
        }
    }
    result.degree -= 35;
    result.required = result.degree - result.overlap;

    std::array<Vec5, CORE_SIZE> rows{};
    for (int core_index = 0; core_index < CORE_SIZE; ++core_index) {
        for (int local = 0; local < SUPPORT; ++local) {
            rows[static_cast<std::size_t>(core_index)].coordinate[static_cast<std::size_t>(local)] =
                evaluations[static_cast<std::size_t>(core_index)]
                           [static_cast<std::size_t>(branches[static_cast<std::size_t>(local)])];
        }
    }

    std::array<int, FULL_GROUPS + 1> dependent{};
    std::vector<Vec5> normals;
    normals.reserve(36041U);
    for (int group = 0; group <= FULL_GROUPS; ++group) {
        const int begin = group * GROUP_SIZE;
        const int end = std::min(begin + GROUP_SIZE, CORE_SIZE);
        for (int first = begin; first < end; ++first) {
            for (int second = first + 1; second < end; ++second) {
                for (int third = second + 1; third < end; ++third) {
                    for (int fourth = third + 1; fourth < end; ++fourth) {
                        const std::array<Vec5, 4> selected{
                            rows[static_cast<std::size_t>(first)],
                            rows[static_cast<std::size_t>(second)],
                            rows[static_cast<std::size_t>(third)],
                            rows[static_cast<std::size_t>(fourth)],
                        };
                        bool independent = false;
                        const auto normal = fraction_free_null_normal(selected, independent);
                        if (!independent) {
                            ++dependent[static_cast<std::size_t>(group)];
                            continue;
                        }
                        if (!admissible_normal(normal)) {
                            continue;
                        }
                        for (const auto& row : selected) {
                            if (dot(row, normal) != 0U) {
                                throw std::runtime_error("fraction-free null identity");
                            }
                        }
                        normals.push_back(normal);
                    }
                }
            }
        }
    }
    for (const auto count : dependent) {
        result.dependent_quadruples += count;
    }
    const auto forced_table = build_forced_table(dependent);
    result.forced = forced_table[static_cast<std::size_t>(result.required)];
    result.normals = static_cast<int>(normals.size());
    batch_projectivize(normals);
    std::sort(normals.begin(), normals.end());
    for (std::size_t begin = 0; begin < normals.size();) {
        std::size_t end = begin + 1U;
        while (end < normals.size() && normals[end] == normals[begin]) {
            ++end;
        }
        result.observed = std::max(result.observed, static_cast<int>(end - begin));
        begin = end;
    }
    for (int roots = 0; roots <= CORE_SIZE; ++roots) {
        if (forced_table[static_cast<std::size_t>(roots)] <= result.observed) {
            result.core_root_cap = roots;
        }
    }
    if (result.observed >= result.forced) {
        throw std::runtime_error("support-five candidate survives partition sieve");
    }
    return result;
}

std::vector<std::array<int, SUPPORT>> all_supports() {
    std::vector<std::array<int, SUPPORT>> answer;
    answer.reserve(4368U);
    for (int a = 0; a < BRANCHES; ++a) {
        for (int b = a + 1; b < BRANCHES; ++b) {
            for (int c = b + 1; c < BRANCHES; ++c) {
                for (int d = c + 1; d < BRANCHES; ++d) {
                    for (int e = d + 1; e < BRANCHES; ++e) {
                        answer.push_back({a, b, c, d, e});
                    }
                }
            }
        }
    }
    return answer;
}

std::string histogram_json(const std::map<int, int>& histogram) {
    std::string answer = "{";
    bool first = true;
    for (const auto& [key, count] : histogram) {
        if (!first) {
            answer += ",";
        }
        first = false;
        answer += "\"" + std::to_string(key) + "\":" + std::to_string(count);
    }
    return answer + "}";
}

void write_report(const std::string& path, const std::vector<Result>& results) {
    std::map<int, int> degree_histogram;
    std::map<int, int> overlap_histogram;
    std::map<int, int> required_histogram;
    std::map<int, int> dependent_histogram;
    std::map<int, int> forced_histogram;
    std::map<int, int> observed_histogram;
    std::map<int, int> core_cap_histogram;
    int minimum_bucket_margin = std::numeric_limits<int>::max();
    int minimum_residual_margin = std::numeric_limits<int>::max();
    int maximum_core_cap = 0;
    std::uint64_t normal_total = 0U;
    for (const auto& result : results) {
        ++degree_histogram[result.degree];
        ++overlap_histogram[result.overlap];
        ++required_histogram[result.required];
        ++dependent_histogram[result.dependent_quadruples];
        ++forced_histogram[result.forced];
        ++observed_histogram[result.observed];
        ++core_cap_histogram[result.core_root_cap];
        minimum_bucket_margin = std::min(minimum_bucket_margin, result.forced - result.observed);
        minimum_residual_margin = std::min(minimum_residual_margin, result.required - result.core_root_cap);
        maximum_core_cap = std::max(maximum_core_cap, result.core_root_cap);
        normal_total += static_cast<std::uint64_t>(result.normals);
    }
    std::ofstream output(path);
    output << "{\n"
           << "  \"schema\": \"sp01zxa7-support-five-partition-sieve/v1\",\n"
           << "  \"claim_id\": \"SP01ZXA7_EXACT_SUPPORT_FIVE_PARTITION_SIEVE\",\n"
           << "  \"status\": \"PASS_EXACT_SUPPORT_FIVE_EXCLUSION\",\n"
           << "  \"field\": " << P << ",\n"
           << "  \"support_count\": " << results.size() << ",\n"
           << "  \"partition_capacities\": [";
    for (int group = 0; group < FULL_GROUPS; ++group) {
        if (group != 0) {
            output << ",";
        }
        output << GROUP_SIZE;
    }
    output << "," << CORE_SIZE - FULL_GROUPS * GROUP_SIZE << "],\n"
           << "  \"residual_degree_histogram\": " << histogram_json(degree_histogram) << ",\n"
           << "  \"outside_overlap_upper_histogram\": " << histogram_json(overlap_histogram) << ",\n"
           << "  \"required_core_root_histogram\": " << histogram_json(required_histogram) << ",\n"
           << "  \"dependent_within_group_quadruple_histogram\": " << histogram_json(dependent_histogram) << ",\n"
           << "  \"forced_bucket_lower_histogram\": " << histogram_json(forced_histogram) << ",\n"
           << "  \"observed_bucket_histogram\": " << histogram_json(observed_histogram) << ",\n"
           << "  \"certified_core_root_cap_histogram\": " << histogram_json(core_cap_histogram) << ",\n"
           << "  \"maximum_certified_core_root_cap\": " << maximum_core_cap << ",\n"
           << "  \"minimum_rowwise_bucket_margin\": " << minimum_bucket_margin << ",\n"
           << "  \"minimum_residual_root_margin\": " << minimum_residual_margin << ",\n"
           << "  \"independent_quadruple_normals_generated\": " << normal_total << ",\n"
           << "  \"new_split_locator_with_exact_coefficient_support_five\": false,\n"
           << "  \"scope_guard\": \"Exact support-five classification inside the affine hull of the sixteen known syndrome locators. Support six or more and arbitrary syndrome-section split locators remain open.\"\n"
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
        const auto evaluations = build_full_locator_evaluations(fixture);
        const auto supports = all_supports();
        std::vector<Result> results(supports.size());
#pragma omp parallel for schedule(dynamic, 1)
        for (int index = 0; index < static_cast<int>(supports.size()); ++index) {
            results[static_cast<std::size_t>(index)] = process_support(
                fixture, evaluations, supports[static_cast<std::size_t>(index)]
            );
        }
        write_report(argv[2], results);
        std::cout << "PASS SP01zxa7 exact support-five partition sieve\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "FAIL: " << error.what() << '\n';
        return 1;
    }
}
