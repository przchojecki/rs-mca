#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

namespace {

constexpr std::uint32_t P = 2147483647U;

std::uint32_t add(std::uint32_t a, std::uint32_t b) {
    std::uint64_t x = static_cast<std::uint64_t>(a) + b;
    x = (x & P) + (x >> 31U);
    if (x >= P) {
        x -= P;
    }
    return static_cast<std::uint32_t>(x);
}

std::uint32_t sub(std::uint32_t a, std::uint32_t b) {
    return a >= b ? a - b : static_cast<std::uint32_t>(static_cast<std::uint64_t>(a) + P - b);
}

std::uint32_t mul(std::uint32_t a, std::uint32_t b) {
    std::uint64_t x = static_cast<std::uint64_t>(a) * b;
    x = (x & P) + (x >> 31U);
    x = (x & P) + (x >> 31U);
    if (x >= P) {
        x -= P;
    }
    return static_cast<std::uint32_t>(x);
}

std::uint32_t power(std::uint32_t a, std::uint32_t e) {
    std::uint32_t answer = 1U;
    while (e != 0U) {
        if ((e & 1U) != 0U) {
            answer = mul(answer, a);
        }
        a = mul(a, a);
        e >>= 1U;
    }
    return answer;
}

std::uint32_t inv(std::uint32_t a) {
    if (a == 0U) {
        throw std::runtime_error("zero inverse");
    }
    return power(a, P - 2U);
}

struct Data {
    std::vector<std::uint32_t> core;
    std::array<std::vector<std::uint32_t>, 16> branch;
    std::array<std::unordered_set<std::uint32_t>, 16> branch_set;
};

Data load(const std::string& path) {
    std::ifstream input(path);
    std::uint32_t field = 0U;
    std::size_t core_size = 0U;
    input >> field >> core_size;
    if (!input || field != P || core_size != 509U) {
        throw std::runtime_error("fixture header");
    }
    Data data;
    data.core.resize(core_size);
    for (auto& value : data.core) {
        input >> value;
    }
    std::size_t count = 0U;
    input >> count;
    if (count != 16U) {
        throw std::runtime_error("branch count");
    }
    for (std::size_t index = 0; index < 16U; ++index) {
        std::uint32_t a = 0U;
        std::uint32_t b = 0U;
        std::size_t size = 0U;
        input >> a >> b >> size;
        (void)a;
        (void)b;
        if (size != 35U) {
            throw std::runtime_error("branch size");
        }
        data.branch[index].resize(size);
        for (auto& value : data.branch[index]) {
            input >> value;
            data.branch_set[index].insert(value);
        }
    }
    return data;
}

std::vector<std::uint32_t> union_of(const Data& data, const std::vector<int>& indices) {
    std::set<std::uint32_t> values;
    for (const auto index : indices) {
        values.insert(data.branch[static_cast<std::size_t>(index)].begin(),
                      data.branch[static_cast<std::size_t>(index)].end());
    }
    return {values.begin(), values.end()};
}

std::vector<std::uint32_t> difference(
    const std::vector<std::uint32_t>& values,
    const std::unordered_set<std::uint32_t>& removed
) {
    std::vector<std::uint32_t> answer;
    for (const auto value : values) {
        if (!removed.contains(value)) {
            answer.push_back(value);
        }
    }
    return answer;
}

std::uint32_t locator_value(std::uint32_t x, const std::vector<std::uint32_t>& roots) {
    std::uint32_t answer = 1U;
    for (const auto root : roots) {
        answer = mul(answer, sub(x, root));
    }
    return answer;
}

struct V3 {
    std::uint32_t x = 0U;
    std::uint32_t y = 0U;
    std::uint32_t z = 0U;
    auto operator<=>(const V3&) const = default;
};

int pivot(const V3& value) {
    if (value.x != 0U) {
        return 0;
    }
    if (value.y != 0U) {
        return 1;
    }
    if (value.z != 0U) {
        return 2;
    }
    return -1;
}

std::uint32_t at(const V3& value, int index) {
    return index == 0 ? value.x : (index == 1 ? value.y : value.z);
}

V3 scaled(const V3& value, std::uint32_t factor) {
    return {mul(value.x, factor), mul(value.y, factor), mul(value.z, factor)};
}

V3 cross(const V3& a, const V3& b) {
    return {
        sub(mul(a.y, b.z), mul(a.z, b.y)),
        sub(mul(a.z, b.x), mul(a.x, b.z)),
        sub(mul(a.x, b.y), mul(a.y, b.x)),
    };
}

void batch_normalize(std::vector<V3>& values) {
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
        std::vector<std::size_t> positions;
        for (std::size_t index = 0; index < values.size(); ++index) {
            if (pivot(values[index]) == coordinate) {
                positions.push_back(index);
            }
        }
        if (positions.empty()) {
            continue;
        }
        std::vector<std::uint32_t> prefix(positions.size() + 1U, 1U);
        for (std::size_t index = 0; index < positions.size(); ++index) {
            prefix[index + 1U] = mul(prefix[index], at(values[positions[index]], coordinate));
        }
        auto suffix = inv(prefix.back());
        for (std::size_t reverse = positions.size(); reverse > 0U; --reverse) {
            const auto local = reverse - 1U;
            const auto position = positions[local];
            const auto old = values[position];
            const auto inverse_value = mul(suffix, prefix[local]);
            suffix = mul(suffix, at(old, coordinate));
            values[position] = scaled(old, inverse_value);
        }
    }
}

bool valid_point(const V3& alpha) {
    return alpha.x != 0U && alpha.y != 0U && alpha.z != 0U
        && add(add(alpha.x, alpha.y), alpha.z) != 0U;
}

bool valid_single_line(const V3& row) {
    const int support = static_cast<int>(row.x != 0U)
        + static_cast<int>(row.y != 0U)
        + static_cast<int>(row.z != 0U);
    return support >= 2 && !(row.x == row.y && row.y == row.z);
}

std::string histogram(const std::map<int, int>& values) {
    std::string answer = "{";
    bool first = true;
    for (const auto& [key, value] : values) {
        if (!first) {
            answer += ",";
        }
        first = false;
        answer += "\"" + std::to_string(key) + "\":" + std::to_string(value);
    }
    return answer + "}";
}

struct Audit {
    std::map<int, int> pair_maximum_histogram;
    std::map<int, int> pair_degree_drop_histogram;
    int pair_global_maximum = 0;
    int pair_global_degree_drop_maximum = 0;
    int triple_global_valid_class_weight = 0;
    std::uint64_t triple_global_pair_bucket = 0U;
    int triple_global_class_count_bound = 0;
    int triple_global_root_upper_bound = 0;
    int triple_minimum_degree = 1000000;
};

Audit run(const Data& data) {
    Audit audit;
    for (int i = 0; i < 16; ++i) {
        for (int j = i + 1; j < 16; ++j) {
            const auto united = union_of(data, {i, j});
            const auto roots_i = difference(united, data.branch_set[static_cast<std::size_t>(i)]);
            const auto roots_j = difference(united, data.branch_set[static_cast<std::size_t>(j)]);
            std::vector<std::uint32_t> allowed = data.core;
            allowed.insert(allowed.end(), united.begin(), united.end());
            std::unordered_map<std::uint32_t, int> buckets;
            int degree_drop_roots = 0;
            for (const auto x : allowed) {
                const auto a = locator_value(x, roots_i);
                const auto b = locator_value(x, roots_j);
                if (a != b) {
                    ++buckets[mul(a, inv(sub(a, b)))];
                } else {
                    ++degree_drop_roots;
                }
            }
            int maximum = 0;
            for (const auto& [lambda, count] : buckets) {
                if (lambda != 0U && lambda != 1U) {
                    maximum = std::max(maximum, count);
                }
            }
            ++audit.pair_maximum_histogram[maximum];
            ++audit.pair_degree_drop_histogram[degree_drop_roots];
            audit.pair_global_maximum = std::max(audit.pair_global_maximum, maximum);
            audit.pair_global_degree_drop_maximum = std::max(
                audit.pair_global_degree_drop_maximum, degree_drop_roots
            );
        }
    }

    for (int i = 0; i < 16; ++i) {
        for (int j = i + 1; j < 16; ++j) {
            for (int k = j + 1; k < 16; ++k) {
                const std::vector<int> indices{i, j, k};
                const auto united = union_of(data, indices);
                std::array<std::vector<std::uint32_t>, 3> roots;
                for (int local = 0; local < 3; ++local) {
                    roots[static_cast<std::size_t>(local)] = difference(
                        united,
                        data.branch_set[static_cast<std::size_t>(indices[static_cast<std::size_t>(local)])]
                    );
                }
                const int degree = static_cast<int>(roots[0].size());
                audit.triple_minimum_degree = std::min(audit.triple_minimum_degree, degree);
                std::vector<V3> rows;
                rows.reserve(data.core.size() + united.size());
                auto append = [&](std::uint32_t x) {
                    V3 row{
                        locator_value(x, roots[0]),
                        locator_value(x, roots[1]),
                        locator_value(x, roots[2]),
                    };
                    if (pivot(row) < 0) {
                        throw std::runtime_error("zero row");
                    }
                    rows.push_back(row);
                };
                for (const auto x : data.core) {
                    append(x);
                }
                for (const auto x : united) {
                    append(x);
                }
                batch_normalize(rows);
                std::sort(rows.begin(), rows.end());
                std::vector<std::pair<V3, int>> classes;
                for (const auto& row : rows) {
                    if (!classes.empty() && classes.back().first == row) {
                        ++classes.back().second;
                    } else {
                        classes.emplace_back(row, 1);
                    }
                }
                int valid_class_weight = 0;
                for (const auto& [row, weight] : classes) {
                    if (valid_single_line(row)) {
                        valid_class_weight = std::max(valid_class_weight, weight);
                    }
                }
                audit.triple_global_valid_class_weight = std::max(
                    audit.triple_global_valid_class_weight, valid_class_weight
                );

                std::vector<V3> intersections;
                intersections.reserve(classes.size() * (classes.size() - 1U) / 2U);
                for (std::size_t left = 0; left < classes.size(); ++left) {
                    for (std::size_t right = left + 1U; right < classes.size(); ++right) {
                        intersections.push_back(cross(classes[left].first, classes[right].first));
                    }
                }
                batch_normalize(intersections);
                std::sort(intersections.begin(), intersections.end());
                std::size_t cursor = 0U;
                while (cursor < intersections.size()) {
                    std::size_t end = cursor + 1U;
                    while (end < intersections.size() && intersections[end] == intersections[cursor]) {
                        ++end;
                    }
                    if (valid_point(intersections[cursor])) {
                        audit.triple_global_pair_bucket = std::max<std::uint64_t>(
                            audit.triple_global_pair_bucket, end - cursor
                        );
                    }
                    cursor = end;
                }
            }
        }
    }

    int class_count = 1;
    while (static_cast<std::uint64_t>(class_count + 1) * class_count / 2U
           <= audit.triple_global_pair_bucket) {
        ++class_count;
    }
    audit.triple_global_class_count_bound = class_count;
    audit.triple_global_root_upper_bound = std::max(
        audit.triple_global_valid_class_weight,
        audit.triple_global_valid_class_weight * class_count
    );
    if (audit.pair_global_maximum != 1
        || audit.pair_global_degree_drop_maximum != 0
        || audit.triple_global_root_upper_bound >= audit.triple_minimum_degree) {
        throw std::runtime_error("independent exclusion failed");
    }
    return audit;
}

void save(const std::string& path, const Audit& audit) {
    std::ofstream output(path);
    output << "{\n"
           << "  \"schema\": \"sp01zxa5-sparse-locator-hull-independent-audit/v1\",\n"
           << "  \"status\": \"PASS_INDEPENDENT_SUPPORT_AT_MOST_THREE_EXCLUSION\",\n"
           << "  \"pair_count\": 120,\n"
           << "  \"pair_interior_root_histogram\": "
           << histogram(audit.pair_maximum_histogram) << ",\n"
           << "  \"pair_global_interior_root_maximum\": " << audit.pair_global_maximum << ",\n"
           << "  \"pair_degree_drop_root_histogram\": "
           << histogram(audit.pair_degree_drop_histogram) << ",\n"
           << "  \"pair_global_degree_drop_root_maximum\": "
           << audit.pair_global_degree_drop_maximum << ",\n"
           << "  \"triple_count\": 560,\n"
           << "  \"triple_global_valid_row_class_weight\": "
           << audit.triple_global_valid_class_weight << ",\n"
           << "  \"triple_global_projective_pair_bucket\": "
           << audit.triple_global_pair_bucket << ",\n"
           << "  \"triple_global_concurrent_class_count_bound\": "
           << audit.triple_global_class_count_bound << ",\n"
           << "  \"triple_global_root_upper_bound\": "
           << audit.triple_global_root_upper_bound << ",\n"
           << "  \"triple_minimum_required_split_roots\": "
           << audit.triple_minimum_degree << ",\n"
           << "  \"new_split_locator_with_coefficient_support_at_most_three\": false,\n"
           << "  \"scope_guard\": \"Independent product-evaluation and unweighted projective upper-bound audit; coefficient support four or more is not classified.\"\n"
           << "}\n";
}

}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 3) {
            std::cerr << "usage: audit FIXTURE OUTPUT\n";
            return 2;
        }
        const auto data = load(argv[1]);
        const auto result = run(data);
        save(argv[2], result);
        std::cout << "PASS independent SP01zxa5 sparse locator hull audit\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "FAIL: " << error.what() << '\n';
        return 1;
    }
}
