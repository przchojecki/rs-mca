#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <string>
#include <tuple>
#include <vector>

using i64 = std::int64_t;

static constexpr int ELL = 11;
static constexpr int TERMS = 5;

i64 mod_pow(i64 base, i64 exponent, int prime) {
    i64 output = 1;
    while (exponent != 0) {
        if ((exponent & 1) != 0) output = output * base % prime;
        base = base * base % prime;
        exponent >>= 1;
    }
    return output;
}

bool is_prime(int value) {
    if (value < 2) return false;
    for (int divisor = 2; i64(divisor) * divisor <= value; ++divisor) {
        if (value % divisor == 0) return false;
    }
    return true;
}

std::vector<int> prime_factors(int value) {
    std::vector<int> output;
    for (int divisor = 2; i64(divisor) * divisor <= value; ++divisor) {
        if (value % divisor != 0) continue;
        output.push_back(divisor);
        while (value % divisor == 0) value /= divisor;
    }
    if (value > 1) output.push_back(value);
    return output;
}

int primitive_root(int prime) {
    const auto factors = prime_factors(prime - 1);
    for (int candidate = 2; candidate < prime; ++candidate) {
        bool valid = true;
        for (int factor : factors) {
            if (mod_pow(candidate, (prime - 1) / factor, prime) == 1) {
                valid = false;
                break;
            }
        }
        if (valid) return candidate;
    }
    return -1;
}

std::vector<std::array<int, TERMS>> root_translation_representatives() {
    std::set<std::array<int, TERMS>> representatives;
    for (int a = 0; a < ELL; ++a) {
        for (int b = a + 1; b < ELL; ++b) {
            for (int c = b + 1; c < ELL; ++c) {
                for (int d = c + 1; d < ELL; ++d) {
                    for (int e = d + 1; e < ELL; ++e) {
                        const std::array<int, TERMS> roots = {a, b, c, d, e};
                        std::array<int, TERMS> best = {ELL, ELL, ELL, ELL, ELL};
                        for (int shift = 0; shift < ELL; ++shift) {
                            std::array<int, TERMS> candidate{};
                            for (int index = 0; index < TERMS; ++index) {
                                candidate[index] = (roots[index] + shift) % ELL;
                            }
                            std::sort(candidate.begin(), candidate.end());
                            best = std::min(best, candidate);
                        }
                        representatives.insert(best);
                    }
                }
            }
        }
    }
    return {representatives.begin(), representatives.end()};
}

std::vector<std::array<int, 4>> four_root_translation_representatives() {
    std::set<std::array<int, 4>> representatives;
    for (int a = 0; a < ELL; ++a) {
        for (int b = a + 1; b < ELL; ++b) {
            for (int c = b + 1; c < ELL; ++c) {
                for (int d = c + 1; d < ELL; ++d) {
                    const std::array<int, 4> roots = {a, b, c, d};
                    std::array<int, 4> best = {ELL, ELL, ELL, ELL};
                    for (int shift = 0; shift < ELL; ++shift) {
                        std::array<int, 4> candidate{};
                        for (int index = 0; index < 4; ++index) {
                            candidate[index] = (roots[index] + shift) % ELL;
                        }
                        std::sort(candidate.begin(), candidate.end());
                        best = std::min(best, candidate);
                    }
                    representatives.insert(best);
                }
            }
        }
    }
    return {representatives.begin(), representatives.end()};
}

using Matrix = std::array<std::array<int, TERMS>, TERMS - 1>;

int matrix_rank(Matrix matrix, int prime) {
    int rank = 0;
    for (int column = 0; column < TERMS && rank < TERMS - 1; ++column) {
        int pivot = rank;
        while (pivot < TERMS - 1 && matrix[pivot][column] == 0) ++pivot;
        if (pivot == TERMS - 1) continue;
        std::swap(matrix[pivot], matrix[rank]);
        const int inverse = int(mod_pow(matrix[rank][column], prime - 2, prime));
        for (int target = column; target < TERMS; ++target) {
            matrix[rank][target] =
                int(i64(matrix[rank][target]) * inverse % prime);
        }
        for (int row = 0; row < TERMS - 1; ++row) {
            if (row == rank || matrix[row][column] == 0) continue;
            const int factor = matrix[row][column];
            for (int target = column; target < TERMS; ++target) {
                i64 value = matrix[row][target]
                    - i64(factor) * matrix[rank][target];
                value %= prime;
                if (value < 0) value += prime;
                matrix[row][target] = int(value);
            }
        }
        ++rank;
    }
    return rank;
}

int determinant4(std::array<std::array<int, 4>, 4> matrix, int prime) {
    i64 determinant = 1;
    for (int column = 0; column < 4; ++column) {
        int pivot = column;
        while (pivot < 4 && matrix[pivot][column] == 0) ++pivot;
        if (pivot == 4) return 0;
        if (pivot != column) {
            std::swap(matrix[pivot], matrix[column]);
            determinant = prime - determinant;
        }
        const int pivot_value = matrix[column][column];
        determinant = determinant * pivot_value % prime;
        const int inverse = int(mod_pow(pivot_value, prime - 2, prime));
        for (int row = column + 1; row < 4; ++row) {
            const int factor = int(i64(matrix[row][column]) * inverse % prime);
            for (int target = column; target < 4; ++target) {
                i64 value = matrix[row][target]
                    - i64(factor) * matrix[column][target];
                value %= prime;
                if (value < 0) value += prime;
                matrix[row][target] = int(value);
            }
        }
    }
    return int(determinant);
}

std::array<int, TERMS> kernel(const Matrix& matrix, int prime) {
    std::array<int, TERMS> output{};
    for (int omitted = 0; omitted < TERMS; ++omitted) {
        std::array<std::array<int, 4>, 4> minor{};
        for (int row = 0; row < 4; ++row) {
            int target = 0;
            for (int column = 0; column < TERMS; ++column) {
                if (column != omitted) minor[row][target++] = matrix[row][column];
            }
        }
        int value = determinant4(minor, prime);
        if ((omitted & 1) != 0 && value != 0) value = prime - value;
        output[omitted] = value;
    }
    return output;
}

struct Nullspace2 {
    int rank = 0;
    std::array<std::array<int, TERMS>, 2> basis{};
};

Nullspace2 nullspace_3x5(
    std::array<std::array<int, TERMS>, 3> matrix, int prime) {
    Nullspace2 output;
    std::array<int, 3> pivots = {-1, -1, -1};
    for (int column = 0; column < TERMS && output.rank < 3; ++column) {
        int pivot = output.rank;
        while (pivot < 3 && matrix[pivot][column] == 0) ++pivot;
        if (pivot == 3) continue;
        std::swap(matrix[pivot], matrix[output.rank]);
        const int inverse =
            int(mod_pow(matrix[output.rank][column], prime - 2, prime));
        for (int target = column; target < TERMS; ++target) {
            matrix[output.rank][target] =
                int(i64(matrix[output.rank][target]) * inverse % prime);
        }
        for (int row = 0; row < 3; ++row) {
            if (row == output.rank || matrix[row][column] == 0) continue;
            const int factor = matrix[row][column];
            for (int target = column; target < TERMS; ++target) {
                i64 value = matrix[row][target]
                    - i64(factor) * matrix[output.rank][target];
                value %= prime;
                if (value < 0) value += prime;
                matrix[row][target] = int(value);
            }
        }
        pivots[output.rank] = column;
        ++output.rank;
    }
    if (output.rank != 3) return output;
    std::array<int, 2> free_columns = {-1, -1};
    int free_count = 0;
    for (int column = 0; column < TERMS; ++column) {
        if (std::find(pivots.begin(), pivots.end(), column) == pivots.end()) {
            free_columns[free_count++] = column;
        }
    }
    if (free_count != 2) {
        output.rank = -1;
        return output;
    }
    for (int basis_index = 0; basis_index < 2; ++basis_index) {
        const int free_column = free_columns[basis_index];
        output.basis[basis_index][free_column] = 1;
        for (int row = 0; row < 3; ++row) {
            const int value = matrix[row][free_column];
            output.basis[basis_index][pivots[row]] = value == 0 ? 0 : prime - value;
        }
    }
    return output;
}

struct State {
    std::array<int, TERMS> support{};
    std::array<int, TERMS> gamma{};

    bool operator<(const State& other) const {
        return std::tie(support, gamma) < std::tie(other.support, other.gamma);
    }
};

struct Spectrum {
    std::vector<int> sorted;
    std::map<int, int> histogram;
    std::array<int, 4> top_sums{};
};

Spectrum spectrum(
    const State& state, int prime, int generator, int quotient_size,
    const std::array<int, ELL>& zeta_power) {
    Spectrum output;
    output.sorted.reserve(quotient_size);
    auto coefficients = state.gamma;
    std::array<int, TERMS> steps{};
    for (int index = 0; index < TERMS; ++index) {
        steps[index] = int(mod_pow(generator, state.support[index], prime));
    }
    for (int label = 0; label < quotient_size; ++label) {
        std::array<int, ELL> values{};
        for (int root = 0; root < ELL; ++root) {
            i64 value = 0;
            for (int index = 0; index < TERMS; ++index) {
                value += i64(coefficients[index])
                    * zeta_power[(root * state.support[index]) % ELL];
            }
            values[root] = int(value % prime);
        }
        std::sort(values.begin(), values.end());
        int maximum = 1;
        int run = 1;
        for (int index = 1; index < ELL; ++index) {
            if (values[index] == values[index - 1]) {
                maximum = std::max(maximum, ++run);
            } else {
                run = 1;
            }
        }
        output.sorted.push_back(maximum);
        ++output.histogram[maximum];
        for (int index = 0; index < TERMS; ++index) {
            coefficients[index] =
                int(i64(coefficients[index]) * steps[index] % prime);
        }
    }
    std::sort(output.sorted.begin(), output.sorted.end(), std::greater<int>());
    int running = 0;
    for (int h = 1; h <= 9; ++h) {
        if (h <= int(output.sorted.size())) running += output.sorted[h - 1];
        if (h >= 6) output.top_sums[h - 6] = running;
    }
    return output;
}

int run_four_state_census(int prime) {
    if (!is_prime(prime) || prime % ELL != 1) return 10;
    const int quotient_size = (prime - 1) / ELL;
    if (quotient_size < 6) return 11;
    const int generator = primitive_root(prime);
    const int zeta = int(mod_pow(generator, quotient_size, prime));
    std::array<int, ELL> zeta_power{};
    zeta_power[0] = 1;
    for (int index = 1; index < ELL; ++index) {
        zeta_power[index] = int(i64(zeta_power[index - 1]) * zeta % prime);
    }
    const auto root_sets = four_root_translation_representatives();
    if (root_sets.size() != 30) return 12;

    i64 projective_rows = 0;
    i64 exact_states_evaluated = 0;
    int rank_deficient = 0;
    std::array<int, 4> maxima = {18, 21, 24, 27};
    int maximum_labels_ge_three = 0;
    int maximum_labels_ge_four = 0;
    int maximum_labels_ge_five = 0;
    int maximum_fibre = 3;
    State maximum_high_label_state{};
    Spectrum maximum_high_label_spectrum;
    State maximum_fibre_state{};
    Spectrum maximum_fibre_spectrum;
    std::array<std::array<int, 4>, 2> gcd_class_maxima = {
        std::array<int, 4>{18, 21, 24, 27},
        std::array<int, 4>{18, 21, 24, 27},
    };
    std::array<int, 2> gcd_class_maximum_high_labels = {0, 0};
    State best_state{};
    Spectrum best_spectrum;
    bool have_best = false;

    for (int a = 1; a < ELL; ++a) {
        for (int b = a + 1; b < ELL; ++b) {
            for (int c = b + 1; c < ELL; ++c) {
                for (int d = c + 1; d < ELL; ++d) {
                    for (int e = d + 1; e < ELL; ++e) {
                        const std::array<int, TERMS> support = {a, b, c, d, e};
                        int support_gcd = 0;
                        for (int index = 1; index < TERMS; ++index) {
                            support_gcd = std::gcd(
                                support_gcd, support[index] - support[0]);
                        }
                        const int gcd_class = support_gcd == 1 ? 0 : 1;
                        for (const auto& roots : root_sets) {
                            std::array<std::array<int, TERMS>, 3> matrix{};
                            for (int row = 1; row < 4; ++row) {
                                for (int column = 0; column < TERMS; ++column) {
                                    matrix[row - 1][column] = (
                                        zeta_power[(roots[row] * support[column]) % ELL]
                                        - zeta_power[(roots[0] * support[column]) % ELL]
                                        + prime) % prime;
                                }
                            }
                            const auto nullspace = nullspace_3x5(matrix, prime);
                            if (nullspace.rank != 3) {
                                ++rank_deficient;
                                continue;
                            }
                            for (int parameter = 0; parameter <= prime; ++parameter) {
                                ++projective_rows;
                                std::array<int, TERMS> gamma{};
                                if (parameter == prime) {
                                    gamma = nullspace.basis[1];
                                } else {
                                    for (int index = 0; index < TERMS; ++index) {
                                        gamma[index] = int((
                                            nullspace.basis[0][index]
                                            + i64(parameter) * nullspace.basis[1][index]
                                        ) % prime);
                                    }
                                }
                                if (std::any_of(
                                        gamma.begin(), gamma.end(),
                                        [](int value) { return value == 0; })) {
                                    continue;
                                }
                                const int inverse =
                                    int(mod_pow(gamma[0], prime - 2, prime));
                                for (int index = 0; index < TERMS; ++index) {
                                    gamma[index] =
                                        int(i64(gamma[index]) * inverse % prime);
                                }
                                ++exact_states_evaluated;
                                const State state{support, gamma};
                                const auto current = spectrum(
                                    state, prime, generator, quotient_size, zeta_power);
                                for (int index = 0; index < 4; ++index) {
                                    maxima[index] =
                                        std::max(maxima[index], current.top_sums[index]);
                                    gcd_class_maxima[gcd_class][index] = std::max(
                                        gcd_class_maxima[gcd_class][index],
                                        current.top_sums[index]);
                                }
                                int labels_ge_three = 0;
                                int labels_ge_four = 0;
                                int labels_ge_five = 0;
                                if (current.sorted[0] > maximum_fibre) {
                                    maximum_fibre = current.sorted[0];
                                    maximum_fibre_state = state;
                                    maximum_fibre_spectrum = current;
                                }
                                for (const auto& [value, count] : current.histogram) {
                                    if (value >= 3) labels_ge_three += count;
                                    if (value >= 4) labels_ge_four += count;
                                    if (value >= 5) labels_ge_five += count;
                                }
                                maximum_labels_ge_three =
                                    std::max(maximum_labels_ge_three, labels_ge_three);
                                if (labels_ge_four > maximum_labels_ge_four) {
                                    maximum_labels_ge_four = labels_ge_four;
                                    maximum_high_label_state = state;
                                    maximum_high_label_spectrum = current;
                                }
                                maximum_labels_ge_five =
                                    std::max(maximum_labels_ge_five, labels_ge_five);
                                gcd_class_maximum_high_labels[gcd_class] = std::max(
                                    gcd_class_maximum_high_labels[gcd_class],
                                    labels_ge_four);
                                if (!have_best
                                    || current.top_sums[0] > best_spectrum.top_sums[0]) {
                                    have_best = true;
                                    best_state = state;
                                    best_spectrum = current;
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    std::cout << "P04CU_FOUR_STATE_CENSUS_V1\n"
              << "p=" << prime << " q=" << quotient_size
              << " projective_rows=" << projective_rows
              << " exact_states_evaluated=" << exact_states_evaluated
              << " rank_deficient=" << rank_deficient
              << " max_labels_ge3=" << maximum_labels_ge_three
              << " max_labels_ge4=" << maximum_labels_ge_four
              << " max_labels_ge5=" << maximum_labels_ge_five
              << " max_fibre=" << maximum_fibre
              << " maxima=";
    for (int value : maxima) std::cout << value << ',';
    if (have_best) {
        std::cout << " best_support=";
        for (int value : best_state.support) std::cout << value << ',';
        std::cout << " best_gamma=";
        for (int value : best_state.gamma) std::cout << value << ',';
        std::cout << " best_hist=";
        for (const auto& [value, count] : best_spectrum.histogram) {
            std::cout << value << '^' << count << ',';
        }
        std::cout << " max_high_support=";
        for (int value : maximum_high_label_state.support) std::cout << value << ',';
        std::cout << " max_high_gamma=";
        for (int value : maximum_high_label_state.gamma) std::cout << value << ',';
        std::cout << " max_high_hist=";
        for (const auto& [value, count] : maximum_high_label_spectrum.histogram) {
            std::cout << value << '^' << count << ',';
        }
        std::cout << " gcd1_maxima=";
        for (int value : gcd_class_maxima[0]) std::cout << value << ',';
        std::cout << " gcd1_max_high=" << gcd_class_maximum_high_labels[0];
        std::cout << " gcd2_maxima=";
        for (int value : gcd_class_maxima[1]) std::cout << value << ',';
        std::cout << " gcd2_max_high=" << gcd_class_maximum_high_labels[1];
        std::cout << " max_fibre_support=";
        for (int value : maximum_fibre_state.support) std::cout << value << ',';
        std::cout << " max_fibre_gamma=";
        for (int value : maximum_fibre_state.gamma) std::cout << value << ',';
        std::cout << " max_fibre_hist=";
        for (const auto& [value, count] : maximum_fibre_spectrum.histogram) {
            std::cout << value << '^' << count << ',';
        }
    }
    std::cout << "\nPASS_P04CU_FOUR_STATE_CENSUS\n";
    return 0;
}

int main(int argc, char** argv) {
    if (argc == 3 && std::string(argv[1]) == "--four-state") {
        return run_four_state_census(std::stoi(argv[2]));
    }
    const int limit = argc > 1 ? std::stoi(argv[1]) : 1000;
    const auto root_sets = root_translation_representatives();
    if (root_sets.size() != 42) return 2;
    std::cout << "P04CU_EXACT_FIVE_PROBE_V1\n";
    for (int prime = 23; prime <= limit; prime += ELL) {
        if (!is_prime(prime)) continue;
        const int quotient_size = (prime - 1) / ELL;
        if (quotient_size < 12) continue;
        const int generator = primitive_root(prime);
        const int zeta = int(mod_pow(generator, quotient_size, prime));
        std::array<int, ELL> zeta_power{};
        zeta_power[0] = 1;
        for (int index = 1; index < ELL; ++index) {
            zeta_power[index] = int(i64(zeta_power[index - 1]) * zeta % prime);
        }

        std::set<State> states;
        int rank_deficient = 0;
        int nonexact_support = 0;
        for (int a = 1; a < ELL; ++a) {
            for (int b = a + 1; b < ELL; ++b) {
                for (int c = b + 1; c < ELL; ++c) {
                    for (int d = c + 1; d < ELL; ++d) {
                        for (int e = d + 1; e < ELL; ++e) {
                            const std::array<int, TERMS> support = {a, b, c, d, e};
                            for (const auto& roots : root_sets) {
                                Matrix matrix{};
                                for (int row = 1; row < TERMS; ++row) {
                                    for (int column = 0; column < TERMS; ++column) {
                                        matrix[row - 1][column] = (
                                            zeta_power[(roots[row] * support[column]) % ELL]
                                            - zeta_power[(roots[0] * support[column]) % ELL]
                                            + prime) % prime;
                                    }
                                }
                                const int rank = matrix_rank(matrix, prime);
                                if (rank != TERMS - 1) {
                                    ++rank_deficient;
                                    continue;
                                }
                                auto gamma = kernel(matrix, prime);
                                if (std::any_of(gamma.begin(), gamma.end(),
                                                [](int value) { return value == 0; })) {
                                    ++nonexact_support;
                                    continue;
                                }
                                const int inverse =
                                    int(mod_pow(gamma[0], prime - 2, prime));
                                for (int index = 0; index < TERMS; ++index) {
                                    gamma[index] = int(i64(gamma[index]) * inverse % prime);
                                }
                                states.insert(State{support, gamma});
                            }
                        }
                    }
                }
            }
        }

        std::array<int, 4> maxima = {24, 28, 32, 36};
        State best_state{};
        Spectrum best_spectrum;
        bool have_best = false;
        for (const auto& state : states) {
            const auto current = spectrum(
                state, prime, generator, quotient_size, zeta_power);
            for (int index = 0; index < 4; ++index) {
                maxima[index] = std::max(maxima[index], current.top_sums[index]);
            }
            if (!have_best || current.top_sums[0] > best_spectrum.top_sums[0]) {
                have_best = true;
                best_state = state;
                best_spectrum = current;
            }
        }

        std::cout << "ROW p=" << prime << " q=" << quotient_size
                  << " states=" << states.size()
                  << " rank_deficient=" << rank_deficient
                  << " nonexact=" << nonexact_support
                  << " maxima=";
        for (int value : maxima) std::cout << value << ',';
        if (have_best) {
            std::cout << " best_support=";
            for (int value : best_state.support) std::cout << value << ',';
            std::cout << " best_gamma=";
            for (int value : best_state.gamma) std::cout << value << ',';
            std::cout << " best_hist=";
            for (const auto& [value, count] : best_spectrum.histogram) {
                std::cout << value << '^' << count << ',';
            }
        }
        std::cout << '\n';
    }
    std::cout << "PASS_P04CU_EXACT_FIVE_PROBE\n";
    return 0;
}
