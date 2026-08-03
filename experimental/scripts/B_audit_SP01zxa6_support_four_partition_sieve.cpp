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
constexpr int GROUP_SIZE = 21;
constexpr int FULL_GROUPS = 24;

std::uint32_t add_mod(std::uint32_t a, std::uint32_t b) {
    std::uint64_t value = static_cast<std::uint64_t>(a) + b;
    value = (value & P) + (value >> 31U);
    return static_cast<std::uint32_t>(value >= P ? value - P : value);
}

std::uint32_t sub_mod(std::uint32_t a, std::uint32_t b) {
    return a >= b ? a - b : static_cast<std::uint32_t>(static_cast<std::uint64_t>(a) + P - b);
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
    for (auto& x : fixture.core) {
        input >> x;
    }
    int branch_count = 0;
    input >> branch_count;
    if (branch_count != BRANCHES) {
        throw std::runtime_error("branch count");
    }
    std::unordered_map<std::uint32_t, std::uint16_t> label_masks;
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
            label_masks[label] = static_cast<std::uint16_t>(
                label_masks[label] | static_cast<std::uint16_t>(1U << branch)
            );
        }
    }
    fixture.outside.reserve(label_masks.size());
    for (const auto& [label, mask] : label_masks) {
        (void)mask;
        fixture.outside.push_back(label);
    }
    std::sort(fixture.outside.begin(), fixture.outside.end());
    if (fixture.outside.size() != 514U) {
        throw std::runtime_error("outside universe size");
    }
    for (const auto label : fixture.outside) {
        fixture.masks.push_back(label_masks.at(label));
    }
    return fixture;
}

struct Vec4 {
    std::array<std::uint32_t, 4> coordinate{};
    auto operator<=>(const Vec4&) const = default;
};

std::uint32_t determinant3(
    std::uint32_t a, std::uint32_t b, std::uint32_t c,
    std::uint32_t d, std::uint32_t e, std::uint32_t f,
    std::uint32_t g, std::uint32_t h, std::uint32_t i
) {
    const auto positive = add_mod(add_mod(mul_mod(a, mul_mod(e, i)), mul_mod(b, mul_mod(f, g))),
                                  mul_mod(c, mul_mod(d, h)));
    const auto negative = add_mod(add_mod(mul_mod(c, mul_mod(e, g)), mul_mod(b, mul_mod(d, i))),
                                  mul_mod(a, mul_mod(f, h)));
    return sub_mod(positive, negative);
}

Vec4 cofactor_normal(const Vec4& x, const Vec4& y, const Vec4& z) {
    Vec4 answer;
    for (int omitted = 0; omitted < 4; ++omitted) {
        std::array<int, 3> columns{};
        int cursor = 0;
        for (int column = 0; column < 4; ++column) {
            if (column != omitted) {
                columns[static_cast<std::size_t>(cursor++)] = column;
            }
        }
        auto value = determinant3(
            x.coordinate[static_cast<std::size_t>(columns[0])],
            x.coordinate[static_cast<std::size_t>(columns[1])],
            x.coordinate[static_cast<std::size_t>(columns[2])],
            y.coordinate[static_cast<std::size_t>(columns[0])],
            y.coordinate[static_cast<std::size_t>(columns[1])],
            y.coordinate[static_cast<std::size_t>(columns[2])],
            z.coordinate[static_cast<std::size_t>(columns[0])],
            z.coordinate[static_cast<std::size_t>(columns[1])],
            z.coordinate[static_cast<std::size_t>(columns[2])]
        );
        if ((omitted & 1) != 0 && value != 0U) {
            value = P - value;
        }
        answer.coordinate[static_cast<std::size_t>(omitted)] = value;
    }
    return answer;
}

int pivot(const Vec4& value) {
    for (int index = 0; index < 4; ++index) {
        if (value.coordinate[static_cast<std::size_t>(index)] != 0U) {
            return index;
        }
    }
    return -1;
}

bool admissible(const Vec4& value) {
    std::uint32_t sum = 0U;
    for (const auto entry : value.coordinate) {
        if (entry == 0U) {
            return false;
        }
        sum = add_mod(sum, entry);
    }
    return sum != 0U;
}

void batch_projectivize(std::vector<Vec4>& values) {
    for (int selected_pivot = 0; selected_pivot < 4; ++selected_pivot) {
        std::vector<std::size_t> positions;
        for (std::size_t index = 0; index < values.size(); ++index) {
            if (pivot(values[index]) == selected_pivot) {
                positions.push_back(index);
            }
        }
        if (positions.empty()) {
            continue;
        }
        std::vector<std::uint32_t> prefix(positions.size() + 1U, 1U);
        for (std::size_t index = 0; index < positions.size(); ++index) {
            prefix[index + 1U] = mul_mod(
                prefix[index],
                values[positions[index]].coordinate[static_cast<std::size_t>(selected_pivot)]
            );
        }
        auto suffix = power(prefix.back(), P - 2U);
        for (std::size_t reverse = positions.size(); reverse > 0U; --reverse) {
            const auto local = reverse - 1U;
            auto& value = values[positions[local]];
            const auto old_pivot = value.coordinate[static_cast<std::size_t>(selected_pivot)];
            const auto factor = mul_mod(suffix, prefix[local]);
            suffix = mul_mod(suffix, old_pivot);
            for (auto& entry : value.coordinate) {
                entry = mul_mod(entry, factor);
            }
        }
    }
}

std::uint64_t choose2(int n) {
    return n < 2 ? 0U : static_cast<std::uint64_t>(n) * (n - 1) / 2U;
}

std::uint64_t choose3(int n) {
    return n < 3 ? 0U : static_cast<std::uint64_t>(n) * (n - 1) * (n - 2) / 6U;
}

std::array<int, CORE_SIZE + 1> forced_table() {
    constexpr auto INF = std::numeric_limits<std::uint64_t>::max() / 4U;
    std::array<std::uint64_t, CORE_SIZE + 1> state{};
    state.fill(INF);
    state[0] = 0U;
    std::array<int, FULL_GROUPS + 1> capacities{};
    capacities.fill(GROUP_SIZE);
    capacities.back() = CORE_SIZE - FULL_GROUPS * GROUP_SIZE;
    for (const auto capacity : capacities) {
        std::array<std::uint64_t, CORE_SIZE + 1> next{};
        next.fill(INF);
        for (int used = 0; used <= CORE_SIZE; ++used) {
            if (state[static_cast<std::size_t>(used)] == INF) {
                continue;
            }
            for (int load = 0; load <= capacity && used + load <= CORE_SIZE; ++load) {
                const auto independent = choose3(load) - choose2(load) / 3U;
                auto& target = next[static_cast<std::size_t>(used + load)];
                target = std::min(target, state[static_cast<std::size_t>(used)] + independent);
            }
        }
        state = next;
    }
    std::array<int, CORE_SIZE + 1> answer{};
    for (int roots = 0; roots <= CORE_SIZE; ++roots) {
        answer[static_cast<std::size_t>(roots)] = static_cast<int>(state[static_cast<std::size_t>(roots)]);
    }
    return answer;
}

struct Result {
    int degree = 0;
    int overlap = 0;
    int required = 0;
    int forced = 0;
    int observed = 0;
    int normals = 0;
};

Result audit_quadruple(
    const Fixture& fixture,
    const std::array<int, 4>& branches,
    const std::array<int, CORE_SIZE + 1>& lower_bound
) {
    std::uint16_t support = 0U;
    for (const auto branch : branches) {
        support = static_cast<std::uint16_t>(support | static_cast<std::uint16_t>(1U << branch));
    }
    Result result;
    for (const auto mask : fixture.masks) {
        const auto active = static_cast<std::uint16_t>(mask & support);
        if (active != 0U) {
            ++result.degree;
            if (std::popcount(active) >= 2) {
                ++result.overlap;
            }
        }
    }
    result.degree -= 35;
    result.required = result.degree - result.overlap;
    result.forced = lower_bound[static_cast<std::size_t>(result.required)];

    std::array<Vec4, CORE_SIZE> rows{};
    for (int core_index = 0; core_index < CORE_SIZE; ++core_index) {
        const auto x = fixture.core[static_cast<std::size_t>(core_index)];
        for (int local = 0; local < 4; ++local) {
            const auto branch_bit = static_cast<std::uint16_t>(1U << branches[static_cast<std::size_t>(local)]);
            std::uint32_t evaluation = 1U;
            for (std::size_t outside_index = 0; outside_index < fixture.outside.size(); ++outside_index) {
                const auto active = static_cast<std::uint16_t>(fixture.masks[outside_index] & support);
                if (active != 0U && (fixture.masks[outside_index] & branch_bit) == 0U) {
                    evaluation = mul_mod(evaluation, sub_mod(x, fixture.outside[outside_index]));
                }
            }
            rows[static_cast<std::size_t>(core_index)].coordinate[static_cast<std::size_t>(local)] = evaluation;
        }
    }

    std::vector<Vec4> normals;
    normals.reserve(31930U);
    for (int group = 0; group <= FULL_GROUPS; ++group) {
        const int begin = group * GROUP_SIZE;
        const int end = std::min(begin + GROUP_SIZE, CORE_SIZE);
        for (int first = begin; first < end; ++first) {
            for (int second = first + 1; second < end; ++second) {
                for (int third = second + 1; third < end; ++third) {
                    const auto normal = cofactor_normal(
                        rows[static_cast<std::size_t>(first)],
                        rows[static_cast<std::size_t>(second)],
                        rows[static_cast<std::size_t>(third)]
                    );
                    if (pivot(normal) >= 0 && admissible(normal)) {
                        normals.push_back(normal);
                    }
                }
            }
        }
    }
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
    if (result.observed >= result.forced) {
        throw std::runtime_error("support-four survivor in independent partition");
    }
    return result;
}

std::string histogram_json(const std::map<int, int>& histogram) {
    std::string output = "{";
    bool first = true;
    for (const auto& [key, count] : histogram) {
        if (!first) {
            output += ",";
        }
        first = false;
        output += "\"" + std::to_string(key) + "\":" + std::to_string(count);
    }
    return output + "}";
}

void write_report(
    const std::string& path,
    const std::vector<Result>& results,
    const std::array<int, CORE_SIZE + 1>& lower_bound
) {
    std::map<int, int> degrees;
    std::map<int, int> overlaps;
    std::map<int, int> required;
    std::map<int, int> forced;
    std::map<int, int> observed;
    int minimum_margin = std::numeric_limits<int>::max();
    int global_observed = 0;
    std::uint64_t normals = 0U;
    for (const auto& row : results) {
        ++degrees[row.degree];
        ++overlaps[row.overlap];
        ++required[row.required];
        ++forced[row.forced];
        ++observed[row.observed];
        minimum_margin = std::min(minimum_margin, row.forced - row.observed);
        global_observed = std::max(global_observed, row.observed);
        normals += static_cast<std::uint64_t>(row.normals);
    }
    int certified_core_root_cap = 0;
    for (int roots = 0; roots <= CORE_SIZE; ++roots) {
        if (lower_bound[static_cast<std::size_t>(roots)] <= global_observed) {
            certified_core_root_cap = roots;
        }
    }
    int residual_margin = std::numeric_limits<int>::max();
    for (const auto& row : results) {
        residual_margin = std::min(residual_margin, row.required - certified_core_root_cap);
    }
    std::ofstream output(path);
    output << "{\n"
           << "  \"schema\": \"sp01zxa6-independent-partition-audit/v1\",\n"
           << "  \"status\": \"PASS_INDEPENDENT_SUPPORT_FOUR_EXCLUSION\",\n"
           << "  \"representation\": \"direct residual locator products\",\n"
           << "  \"partition_capacities\": [";
    for (int index = 0; index < FULL_GROUPS; ++index) {
        if (index != 0) {
            output << ",";
        }
        output << GROUP_SIZE;
    }
    output << "," << CORE_SIZE - FULL_GROUPS * GROUP_SIZE << "],\n"
           << "  \"quadruple_count\": " << results.size() << ",\n"
           << "  \"residual_degree_histogram\": " << histogram_json(degrees) << ",\n"
           << "  \"outside_overlap_upper_histogram\": " << histogram_json(overlaps) << ",\n"
           << "  \"required_core_root_histogram\": " << histogram_json(required) << ",\n"
           << "  \"forced_bucket_lower_histogram\": " << histogram_json(forced) << ",\n"
           << "  \"observed_bucket_histogram\": " << histogram_json(observed) << ",\n"
           << "  \"minimum_rowwise_bucket_margin\": " << minimum_margin << ",\n"
           << "  \"certified_core_root_cap\": " << certified_core_root_cap << ",\n"
           << "  \"minimum_residual_root_margin\": " << residual_margin << ",\n"
           << "  \"independent_triple_normals_generated\": " << normals << ",\n"
           << "  \"verdict\": \"No exact-support-four split locator occurs in the affine hull.\"\n"
           << "}\n";
}

}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 3) {
            std::cerr << "usage: auditor FIXTURE OUTPUT\n";
            return 2;
        }
        const auto fixture = read_fixture(argv[1]);
        const auto lower_bound = forced_table();
        std::vector<std::array<int, 4>> quadruples;
        for (int a = 0; a < BRANCHES; ++a) {
            for (int b = a + 1; b < BRANCHES; ++b) {
                for (int c = b + 1; c < BRANCHES; ++c) {
                    for (int d = c + 1; d < BRANCHES; ++d) {
                        quadruples.push_back({a, b, c, d});
                    }
                }
            }
        }
        std::vector<Result> results(quadruples.size());
#pragma omp parallel for schedule(dynamic, 1)
        for (int index = 0; index < static_cast<int>(quadruples.size()); ++index) {
            results[static_cast<std::size_t>(index)] = audit_quadruple(
                fixture, quadruples[static_cast<std::size_t>(index)], lower_bound
            );
        }
        write_report(argv[2], results, lower_bound);
        std::cout << "PASS independent SP01zxa6 support-four audit\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "FAIL: " << error.what() << '\n';
        return 1;
    }
}
