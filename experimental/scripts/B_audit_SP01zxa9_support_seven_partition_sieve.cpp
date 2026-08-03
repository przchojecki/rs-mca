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
constexpr int SUPPORT = 7;
constexpr int ROWS = SUPPORT - 1;
constexpr int GROUP_SIZE = 16;
constexpr int FULL_GROUPS = 31;
constexpr int CORE_PERMUTATION_MULTIPLIER = 137;
constexpr int CORE_PERMUTATION_OFFSET = 17;

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

struct Vec7 {
    std::array<std::uint32_t, SUPPORT> coordinate{};
    auto operator<=>(const Vec7&) const = default;
};

Vec7 fraction_free_null_normal(const std::array<Vec7, ROWS>& input, bool& independent) {
    std::array<std::array<std::uint32_t, SUPPORT>, ROWS> matrix{};
    for (int row = 0; row < ROWS; ++row) {
        matrix[static_cast<std::size_t>(row)] = input[static_cast<std::size_t>(row)].coordinate;
    }
    std::array<int, SUPPORT> permutation{0, 1, 2, 3, 4, 5, 6};
    std::array<std::uint32_t, ROWS> diagonal{};
    for (int pivot = 0; pivot < ROWS; ++pivot) {
        int selected_row = -1;
        int selected_column = -1;
        for (int row = pivot; row < ROWS && selected_row < 0; ++row) {
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
        diagonal[static_cast<std::size_t>(pivot)] =
            matrix[static_cast<std::size_t>(pivot)][static_cast<std::size_t>(pivot)];
        for (int row = pivot + 1; row < ROWS; ++row) {
            const auto multiplier = matrix[static_cast<std::size_t>(row)][static_cast<std::size_t>(pivot)];
            for (int column = pivot + 1; column < SUPPORT; ++column) {
                matrix[static_cast<std::size_t>(row)][static_cast<std::size_t>(column)] = sub_mod(
                    mul_mod(diagonal[static_cast<std::size_t>(pivot)],
                            matrix[static_cast<std::size_t>(row)][static_cast<std::size_t>(column)]),
                    mul_mod(multiplier,
                            matrix[static_cast<std::size_t>(pivot)][static_cast<std::size_t>(column)])
                );
            }
            matrix[static_cast<std::size_t>(row)][static_cast<std::size_t>(pivot)] = 0U;
        }
    }
    independent = true;
    std::array<std::uint32_t, SUPPORT> scaled{};
    scaled[SUPPORT - 1] = 1U;
    for (int row = ROWS - 1; row >= 0; --row) {
        std::uint32_t sum = 0U;
        std::uint32_t interval_product = 1U;
        for (int column = row + 1; column < SUPPORT; ++column) {
            if (column > row + 1) {
                interval_product = mul_mod(
                    interval_product, diagonal[static_cast<std::size_t>(column - 1)]
                );
            }
            sum = add_mod(sum, mul_mod(
                matrix[static_cast<std::size_t>(row)][static_cast<std::size_t>(column)],
                mul_mod(interval_product, scaled[static_cast<std::size_t>(column)])
            ));
        }
        scaled[static_cast<std::size_t>(row)] = neg_mod(sum);
    }
    Vec7 answer;
    std::uint32_t prefix = 1U;
    for (int column = 0; column < ROWS; ++column) {
        answer.coordinate[static_cast<std::size_t>(permutation[static_cast<std::size_t>(column)])] =
            mul_mod(prefix, scaled[static_cast<std::size_t>(column)]);
        prefix = mul_mod(prefix, diagonal[static_cast<std::size_t>(column)]);
    }
    answer.coordinate[static_cast<std::size_t>(permutation[SUPPORT - 1])] = prefix;
    return answer;
}

std::uint32_t dot(const Vec7& left, const Vec7& right) {
    std::uint32_t answer = 0U;
    for (int index = 0; index < SUPPORT; ++index) {
        answer = add_mod(answer, mul_mod(
            left.coordinate[static_cast<std::size_t>(index)],
            right.coordinate[static_cast<std::size_t>(index)]
        ));
    }
    return answer;
}

bool admissible(const Vec7& value) {
    std::uint32_t sum = 0U;
    for (const auto entry : value.coordinate) {
        if (entry == 0U) {
            return false;
        }
        sum = add_mod(sum, entry);
    }
    return sum != 0U;
}

void batch_projectivize(std::vector<Vec7>& values) {
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
        const auto old = values[index].coordinate[0];
        const auto factor = mul_mod(suffix, prefix[index]);
        suffix = mul_mod(suffix, old);
        for (auto& entry : values[index].coordinate) {
            entry = mul_mod(entry, factor);
        }
    }
}

std::uint64_t choose6(int value) {
    return value < 6 ? 0U
        : static_cast<std::uint64_t>(value) * (value - 1) * (value - 2)
          * (value - 3) * (value - 4) * (value - 5) / 720U;
}

std::array<int, CORE_SIZE + 1> forced_table(
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
                const auto all = choose6(load);
                const auto bad = static_cast<std::uint64_t>(dependent[static_cast<std::size_t>(group)]);
                const auto lower = all > bad ? all - bad : 0U;
                auto& target = next[static_cast<std::size_t>(used + load)];
                target = std::min(target, state[static_cast<std::size_t>(used)] + lower);
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

struct Result {
    std::array<int, SUPPORT> branches{};
    int degree = 0;
    int overlap = 0;
    int required = 0;
    int dependent = 0;
    int forced = 0;
    int observed = 0;
    int core_cap = 0;
    int repeated_normal_core_roots = 0;
    int repeated_normal_outside_roots = 0;
    Vec7 repeated_normal{};
    int normals = 0;
};

Result process_support(
    const Fixture& fixture,
    const std::array<int, SUPPORT>& branches
) {
    std::uint16_t support_mask = 0U;
    for (const auto branch : branches) {
        support_mask = static_cast<std::uint16_t>(support_mask | static_cast<std::uint16_t>(1U << branch));
    }
    Result result;
    result.branches = branches;
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

    std::array<Vec7, CORE_SIZE> rows{};
    for (int row_index = 0; row_index < CORE_SIZE; ++row_index) {
        const int core_index = (CORE_PERMUTATION_MULTIPLIER * row_index
                                + CORE_PERMUTATION_OFFSET) % CORE_SIZE;
        const auto x = fixture.core[static_cast<std::size_t>(core_index)];
        for (int local = 0; local < SUPPORT; ++local) {
            const auto branch_bit = static_cast<std::uint16_t>(
                1U << branches[static_cast<std::size_t>(local)]
            );
            std::uint32_t evaluation = 1U;
            for (std::size_t outside_index = 0; outside_index < fixture.outside.size(); ++outside_index) {
                const auto active = static_cast<std::uint16_t>(fixture.masks[outside_index] & support_mask);
                if (active != 0U && (fixture.masks[outside_index] & branch_bit) == 0U) {
                    evaluation = mul_mod(evaluation, sub_mod(x, fixture.outside[outside_index]));
                }
            }
            rows[static_cast<std::size_t>(row_index)].coordinate[static_cast<std::size_t>(local)] = evaluation;
        }
    }

    std::array<int, FULL_GROUPS + 1> dependent{};
    std::vector<Vec7> normals;
    normals.reserve(249964U);
    for (int group = 0; group <= FULL_GROUPS; ++group) {
        const int begin = group * GROUP_SIZE;
        const int end = std::min(begin + GROUP_SIZE, CORE_SIZE);
        for (int a = begin; a < end; ++a) {
            for (int b = a + 1; b < end; ++b) {
                for (int c = b + 1; c < end; ++c) {
                    for (int d = c + 1; d < end; ++d) {
                        for (int e = d + 1; e < end; ++e) {
                            for (int f = e + 1; f < end; ++f) {
                                const std::array<Vec7, ROWS> selected{
                                    rows[static_cast<std::size_t>(a)], rows[static_cast<std::size_t>(b)],
                                    rows[static_cast<std::size_t>(c)], rows[static_cast<std::size_t>(d)],
                                    rows[static_cast<std::size_t>(e)], rows[static_cast<std::size_t>(f)]
                                };
                                bool independent = false;
                                const auto normal = fraction_free_null_normal(selected, independent);
                                if (!independent) {
                                    ++dependent[static_cast<std::size_t>(group)];
                                    continue;
                                }
                                if (!admissible(normal)) {
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
        }
    }
    for (const auto count : dependent) {
        result.dependent += count;
    }
    const auto lower = forced_table(dependent);
    result.forced = lower[static_cast<std::size_t>(result.required)];
    result.normals = static_cast<int>(normals.size());
    batch_projectivize(normals);
    std::sort(normals.begin(), normals.end());
    for (std::size_t begin = 0; begin < normals.size();) {
        std::size_t end = begin + 1U;
        while (end < normals.size() && normals[end] == normals[begin]) {
            ++end;
        }
        const auto bucket = static_cast<int>(end - begin);
        if (bucket > result.observed) {
            result.observed = bucket;
            result.repeated_normal = normals[begin];
        }
        begin = end;
    }
    if (result.observed > 1) {
        for (const auto& row : rows) {
            if (dot(row, result.repeated_normal) == 0U) {
                ++result.repeated_normal_core_roots;
            }
        }
        for (std::size_t label_index = 0; label_index < fixture.outside.size(); ++label_index) {
            if ((fixture.masks[label_index] & support_mask) == 0U) {
                continue;
            }
            const auto x = fixture.outside[label_index];
            Vec7 row;
            for (int local = 0; local < SUPPORT; ++local) {
                const auto branch_bit = static_cast<std::uint16_t>(
                    1U << branches[static_cast<std::size_t>(local)]
                );
                if ((fixture.masks[label_index] & branch_bit) == 0U) {
                    row.coordinate[static_cast<std::size_t>(local)] = 0U;
                    continue;
                }
                std::uint32_t evaluation = 1U;
                for (std::size_t root_index = 0; root_index < fixture.outside.size(); ++root_index) {
                    const auto active = static_cast<std::uint16_t>(fixture.masks[root_index] & support_mask);
                    if (active != 0U && (fixture.masks[root_index] & branch_bit) == 0U) {
                        evaluation = mul_mod(evaluation, sub_mod(x, fixture.outside[root_index]));
                    }
                }
                row.coordinate[static_cast<std::size_t>(local)] = evaluation;
            }
            if (dot(row, result.repeated_normal) == 0U) {
                ++result.repeated_normal_outside_roots;
            }
        }
    }
    for (int roots = 0; roots <= CORE_SIZE; ++roots) {
        if (lower[static_cast<std::size_t>(roots)] <= result.observed) {
            result.core_cap = roots;
        }
    }
    if (result.observed >= result.forced) {
        throw std::runtime_error("support-seven candidate survives partition sieve");
    }
    return result;
}

std::vector<std::array<int, SUPPORT>> all_supports() {
    std::vector<std::array<int, SUPPORT>> answer;
    answer.reserve(11440U);
    for (int a = 0; a < BRANCHES; ++a) {
        for (int b = a + 1; b < BRANCHES; ++b) {
            for (int c = b + 1; c < BRANCHES; ++c) {
                for (int d = c + 1; d < BRANCHES; ++d) {
                    for (int e = d + 1; e < BRANCHES; ++e) {
                        for (int f = e + 1; f < BRANCHES; ++f) {
                            for (int g = f + 1; g < BRANCHES; ++g) {
                                answer.push_back({a, b, c, d, e, f, g});
                            }
                        }
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
    std::map<int, int> degree;
    std::map<int, int> overlap;
    std::map<int, int> required;
    std::map<int, int> dependent;
    std::map<int, int> forced;
    std::map<int, int> observed;
    std::map<int, int> core_cap;
    int bucket_margin = std::numeric_limits<int>::max();
    int residual_margin = std::numeric_limits<int>::max();
    int maximum_core_cap = 0;
    std::uint64_t normal_total = 0U;
    for (const auto& row : results) {
        ++degree[row.degree];
        ++overlap[row.overlap];
        ++required[row.required];
        ++dependent[row.dependent];
        ++forced[row.forced];
        ++observed[row.observed];
        ++core_cap[row.core_cap];
        bucket_margin = std::min(bucket_margin, row.forced - row.observed);
        residual_margin = std::min(residual_margin, row.required - row.core_cap);
        maximum_core_cap = std::max(maximum_core_cap, row.core_cap);
        normal_total += static_cast<std::uint64_t>(row.normals);
    }
    std::ofstream output(path);
    output << "{\n"
           << "  \"schema\": \"sp01zxa9-independent-support-seven-audit/v1\",\n"
           << "  \"claim_id\": \"SP01ZXA9_EXACT_SUPPORT_SEVEN_PARTITION_SIEVE\",\n"
           << "  \"status\": \"PASS_INDEPENDENT_EXACT_SUPPORT_SEVEN_EXCLUSION\",\n"
           << "  \"representation\": \"direct residual products with permuted core partition\",\n"
           << "  \"core_permutation\": \"index -> 137*index+17 mod 509\",\n"
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
           << "  \"residual_degree_histogram\": " << histogram_json(degree) << ",\n"
           << "  \"outside_overlap_upper_histogram\": " << histogram_json(overlap) << ",\n"
           << "  \"required_core_root_histogram\": " << histogram_json(required) << ",\n"
           << "  \"dependent_within_group_six_row_histogram\": " << histogram_json(dependent) << ",\n"
           << "  \"forced_bucket_lower_histogram\": " << histogram_json(forced) << ",\n"
           << "  \"observed_bucket_histogram\": " << histogram_json(observed) << ",\n"
           << "  \"certified_core_root_cap_histogram\": " << histogram_json(core_cap) << ",\n"
           << "  \"maximum_certified_core_root_cap\": " << maximum_core_cap << ",\n"
           << "  \"minimum_rowwise_bucket_margin\": " << bucket_margin << ",\n"
           << "  \"minimum_residual_root_margin\": " << residual_margin << ",\n"
           << "  \"independent_six_row_normals_generated\": " << normal_total << ",\n"
           << "  \"repeated_normal_cases\": [";
    bool first_case = true;
    for (const auto& row : results) {
        if (row.observed <= 1) {
            continue;
        }
        if (!first_case) {
            output << ",";
        }
        first_case = false;
        output << "{\"branches\":[";
        for (int index = 0; index < SUPPORT; ++index) {
            if (index != 0) {
                output << ",";
            }
            output << row.branches[static_cast<std::size_t>(index)];
        }
        output << "],\"bucket\":" << row.observed
               << ",\"exact_core_roots\":" << row.repeated_normal_core_roots
               << ",\"exact_outside_roots\":" << row.repeated_normal_outside_roots
               << ",\"exact_residual_roots\":"
               << row.repeated_normal_core_roots + row.repeated_normal_outside_roots
               << ",\"residual_degree\":" << row.degree
               << ",\"normal\":[";
        for (int index = 0; index < SUPPORT; ++index) {
            if (index != 0) {
                output << ",";
            }
            output << row.repeated_normal.coordinate[static_cast<std::size_t>(index)];
        }
        output << "]}";
    }
    output << "],\n"
           << "  \"new_split_locator_with_exact_coefficient_support_seven\": false,\n"
           << "  \"scope_guard\": \"Exact support-seven classification inside the affine hull of the sixteen known syndrome locators. Support eight or more and arbitrary syndrome-section split locators remain open.\"\n"
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
        const auto supports = all_supports();
        std::vector<Result> results(supports.size());
#pragma omp parallel for schedule(dynamic, 1)
        for (int index = 0; index < static_cast<int>(supports.size()); ++index) {
            results[static_cast<std::size_t>(index)] = process_support(
                fixture, supports[static_cast<std::size_t>(index)]
            );
        }
        write_report(argv[2], results);
        std::cout << "PASS independent SP01zxa9 support-seven audit\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "FAIL: " << error.what() << '\n';
        return 1;
    }
}
