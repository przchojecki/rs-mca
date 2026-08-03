#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>

#ifndef P06_DOMAIN_ORDER
#define P06_DOMAIN_ORDER 32
#endif
#ifndef P06_FIELD_PRIME
#define P06_FIELD_PRIME 97
#endif

namespace {
constexpr uint32_t N = P06_DOMAIN_ORDER;
uint32_t modulus = P06_FIELD_PRIME;
static_assert(N >= 8 && (N & (N - 1)) == 0);

uint64_t mod_pow(uint64_t a, uint64_t e) {
  uint64_t result = 1;
  while (e != 0) {
    if ((e & 1U) != 0) result = result * a % modulus;
    e >>= 1U;
    if (e != 0) a = a * a % modulus;
  }
  return result;
}

bool is_prime(uint32_t value) {
  if (value < 2) return false;
  if ((value & 1U) == 0) return value == 2;
  for (uint32_t d = 3; uint64_t{d} * d <= value; d += 2) {
    if (value % d == 0) return false;
  }
  return true;
}

uint32_t inverse(uint32_t a) {
  if (a == 0) throw std::runtime_error("division by zero");
  return static_cast<uint32_t>(mod_pow(a, modulus - 2));
}

uint32_t mod_add(uint32_t a, uint32_t b) {
  return static_cast<uint32_t>((uint64_t{a} + b) % modulus);
}

uint32_t mod_sub(uint32_t a, uint32_t b) {
  return static_cast<uint32_t>((uint64_t{a} + modulus - b) % modulus);
}

uint32_t mod_mul(uint32_t a, uint32_t b) {
  return static_cast<uint32_t>(uint64_t{a} * b % modulus);
}

uint32_t root_of_order_n() {
  if ((modulus - 1) % N != 0) throw std::runtime_error("n does not divide p-1");
  for (uint32_t a = 2; a < modulus; ++a) {
    const uint32_t z = static_cast<uint32_t>(mod_pow(a, (modulus - 1) / N));
    if (mod_pow(z, N) == 1 && mod_pow(z, N / 2) != 1) return z;
  }
  throw std::runtime_error("no element of exact order n");
}

bool canonical_gap_rotation(const std::array<uint16_t, 4>& gap) {
  for (uint32_t shift = 1; shift < 4; ++shift) {
    for (uint32_t i = 0; i < 4; ++i) {
      const uint16_t lhs = gap[(i + shift) & 3U];
      const uint16_t rhs = gap[i];
      if (lhs < rhs) return false;
      if (lhs > rhs) break;
    }
  }
  return true;
}

struct Record {
  uint32_t type = 0;
  uint32_t key0 = 0;
  uint32_t key1 = 0;
  uint32_t key2 = 0;
  uint32_t e1 = 0;
  uint32_t e2 = 0;
  uint32_t e3 = 0;
  uint32_t product_exponent = 0;
  std::array<uint16_t, 4> exponent{};
};

bool key_less(const Record& a, const Record& b) {
  return std::tie(a.type, a.key0, a.key1, a.key2) <
         std::tie(b.type, b.key0, b.key1, b.key2);
}

bool same_key(const Record& a, const Record& b) {
  return a.type == b.type && a.key0 == b.key0 && a.key1 == b.key1 &&
         a.key2 == b.key2;
}

std::array<uint32_t, 3> elementary(const std::array<uint16_t, 4>& exponent,
                                   const std::vector<uint32_t>& roots) {
  std::array<uint32_t, 4> x{};
  for (uint32_t i = 0; i < 4; ++i) x[i] = roots[exponent[i]];
  uint64_t e1 = 0;
  uint64_t e2 = 0;
  uint64_t e3 = 0;
  for (uint32_t i = 0; i < 4; ++i) {
    e1 += x[i];
    for (uint32_t j = i + 1; j < 4; ++j) {
      e2 += uint64_t{x[i]} * x[j] % modulus;
      for (uint32_t k = j + 1; k < 4; ++k) {
        e3 += (uint64_t{x[i]} * x[j] % modulus) * x[k] % modulus;
      }
    }
  }
  return {static_cast<uint32_t>(e1 % modulus),
          static_cast<uint32_t>(e2 % modulus),
          static_cast<uint32_t>(e3 % modulus)};
}

bool smooth(uint32_t e1, uint32_t e2, uint32_t e3) {
  const uint32_t m = uint64_t{e1} * inverse(4) % modulus;
  const uint32_t m2 = uint64_t{m} * m % modulus;
  const uint32_t sigma =
      uint64_t{(6 * uint64_t{m2} + modulus - e2) % modulus} * inverse(2) %
      modulus;
  const uint32_t m3 = uint64_t{m2} * m % modulus;
  const uint32_t rho = uint64_t{
      static_cast<uint32_t>((uint64_t{e3} + modulus -
                             (4 * uint64_t{m3}) % modulus +
                             (4 * uint64_t{m} * sigma) % modulus) % modulus)} *
      inverse(8) % modulus;
  if (rho == 0) return false;
  return uint64_t{sigma} * sigma % modulus * sigma % modulus !=
         27 * (uint64_t{rho} * rho % modulus) % modulus;
}

Record make_record(const std::array<uint16_t, 4>& exponent,
                   const std::vector<uint32_t>& roots) {
  const auto e = elementary(exponent, roots);
  Record r;
  r.e1 = e[0];
  r.e2 = e[1];
  r.e3 = e[2];
  r.exponent = exponent;
  for (uint16_t x : exponent) r.product_exponent = (r.product_exponent + x) % N;
  if (r.e1 != 0) {
    r.type = 1;
    const uint32_t inv = inverse(r.e1);
    const uint32_t inv2 = uint64_t{inv} * inv % modulus;
    r.key0 = static_cast<uint32_t>(mod_pow(r.e1, N));
    r.key1 = uint64_t{r.e2} * inv2 % modulus;
    r.key2 = uint64_t{r.e3} * inv2 % modulus * inv % modulus;
  } else if (r.e2 != 0) {
    r.type = 2;
    const uint32_t inv = inverse(r.e2);
    const uint32_t inv2 = uint64_t{inv} * inv % modulus;
    r.key0 = static_cast<uint32_t>(mod_pow(r.e2, N / 2));
    r.key1 = uint64_t{r.e3} * r.e3 % modulus * inv2 % modulus * inv % modulus;
  } else if (r.e3 != 0) {
    r.type = 3;
    r.key0 = static_cast<uint32_t>(mod_pow(r.e3, N));
  } else {
    r.type = 4;
  }
  return r;
}

uint32_t shifted(uint32_t value, uint32_t degree, uint32_t shift,
                 const std::vector<uint32_t>& roots) {
  return uint64_t{value} * roots[(degree * shift) % N] % modulus;
}

bool disjoint_after_shift(const Record& a, const Record& b, uint32_t shift) {
  for (uint16_t x : a.exponent) {
    for (uint16_t y : b.exponent) {
      if (x == (y + shift) % N) return false;
    }
  }
  return true;
}

uint32_t product_signature(uint32_t alpha, uint32_t beta) {
  const uint32_t d = (beta + N - alpha) % N;
  const uint32_t forward = (alpha & 3U) * N + d;
  const uint32_t reverse = (beta & 3U) * N + ((N - d) % N);
  return std::min(forward, reverse);
}
}  // namespace

int main(int argc, char** argv) {
  if (argc > 2) throw std::runtime_error("usage: probe [prime]");
  if (argc == 2) modulus = static_cast<uint32_t>(std::stoul(argv[1]));
  if (!is_prime(modulus) || modulus <= 3) throw std::runtime_error("bad prime");

  const uint32_t zeta = root_of_order_n();
  std::vector<uint32_t> roots(N);
  std::unordered_map<uint32_t, uint32_t> logarithm;
  roots[0] = 1;
  logarithm.emplace(1, 0);
  for (uint32_t i = 1; i < N; ++i) {
    roots[i] = uint64_t{roots[i - 1]} * zeta % modulus;
    logarithm.emplace(roots[i], i);
  }

  std::vector<Record> records;
  for (uint32_t g0 = 1; g0 <= N - 3; ++g0) {
    for (uint32_t g1 = 1; g1 <= N - g0 - 2; ++g1) {
      for (uint32_t g2 = 1; g2 <= N - g0 - g1 - 1; ++g2) {
        const uint32_t g3 = N - g0 - g1 - g2;
        const std::array<uint16_t, 4> gap{
            static_cast<uint16_t>(g0), static_cast<uint16_t>(g1),
            static_cast<uint16_t>(g2), static_cast<uint16_t>(g3)};
        if (!canonical_gap_rotation(gap)) continue;
        const std::array<uint16_t, 4> exponent{
            0, static_cast<uint16_t>(g0), static_cast<uint16_t>(g0 + g1),
            static_cast<uint16_t>(g0 + g1 + g2)};
        Record r = make_record(exponent, roots);
        if (smooth(r.e1, r.e2, r.e3)) records.push_back(r);
      }
    }
  }
  std::sort(records.begin(), records.end(), key_less);

  uint64_t trade_orbits = 0;
  uint64_t decorated_product_line_records = 0;
  uint64_t product_line_left_degenerate = 0;
  uint64_t product_line_right_degenerate = 0;
  std::map<uint32_t, uint64_t> product_multiplicity;
  std::map<uint64_t, uint64_t> normalized_product_cell_multiplicity;
  std::vector<uint64_t> cross_ratio_incidence(N, 0);
  for (size_t begin = 0; begin < records.size();) {
    size_t end = begin + 1;
    while (end < records.size() && same_key(records[begin], records[end])) ++end;
    for (size_t i = begin; i < end; ++i) {
      for (size_t j = i + 1; j < end; ++j) {
        const Record& a = records[i];
        const Record& b = records[j];
        std::array<uint32_t, 2> candidates{};
        uint32_t count = 0;
        if (a.type == 1) {
          const auto it = logarithm.find(uint64_t{a.e1} * inverse(b.e1) % modulus);
          if (it != logarithm.end()) candidates[count++] = it->second;
        } else if (a.type == 2) {
          const auto it = logarithm.find(uint64_t{a.e2} * inverse(b.e2) % modulus);
          if (it != logarithm.end() && (it->second & 1U) == 0) {
            candidates[count++] = it->second / 2;
            candidates[count++] = it->second / 2 + N / 2;
          }
        } else if (a.type == 3) {
          const auto it = logarithm.find(uint64_t{a.e3} * inverse(b.e3) % modulus);
          if (it != logarithm.end()) {
            const uint32_t inv3 = N % 3 == 1 ? (2 * N + 1) / 3 : (N + 1) / 3;
            candidates[count++] = it->second * inv3 % N;
          }
        }
        for (uint32_t k = 0; k < count; ++k) {
          const uint32_t shift = candidates[k] % N;
          if (shifted(b.e1, 1, shift, roots) != a.e1 ||
              shifted(b.e2, 2, shift, roots) != a.e2 ||
              shifted(b.e3, 3, shift, roots) != a.e3 ||
              !disjoint_after_shift(a, b, shift)) {
            continue;
          }
          ++trade_orbits;
          const uint32_t alpha = a.product_exponent;
          const uint32_t beta = (b.product_exponent + 4 * shift) % N;
          ++product_multiplicity[product_signature(alpha, beta)];

          const auto add_oriented_cells = [&](uint32_t first_product,
                                              uint32_t second_product,
                                              const Record& second,
                                              uint32_t second_shift) {
            for (uint16_t y0 : second.exponent) {
              const uint32_t y = (y0 + second_shift) % N;
              const uint32_t normalized_first =
                  (first_product + N - (4 * y) % N) % N;
              const uint32_t normalized_second =
                  (second_product + N - (4 * y) % N) % N;
              const uint64_t cell = uint64_t{normalized_first} * N +
                                    normalized_second;
              ++normalized_product_cell_multiplicity[cell];
            }
          };
          add_oriented_cells(alpha, beta, b, shift);
          add_oriented_cells(beta, alpha, a, 0);

          // Both orientations are counted. Each unordered trade orbit has
          // exactly 32 normalized ordered cross-pair incidences.
          for (uint16_t x : a.exponent) {
            for (uint16_t y0 : b.exponent) {
              const uint32_t y = (y0 + shift) % N;
              ++cross_ratio_incidence[(x + N - y) % N];
              ++cross_ratio_incidence[(y + N - x) % N];

              const auto count_decorations = [&](const Record& left,
                                                   uint32_t left_shift,
                                                   uint16_t left_anchor,
                                                   const Record& right,
                                                   uint32_t right_shift,
                                                   uint16_t right_anchor,
                                                   uint32_t normalizer) {
                const uint32_t anchor_left =
                    (left_anchor + left_shift + N - normalizer) % N;
                const uint32_t anchor_right =
                    (right_anchor + right_shift + N - normalizer) % N;
                const uint32_t r_value = roots[anchor_left];
                if (anchor_right != 0) {
                  throw std::runtime_error("product-line normalization drift");
                }
                for (uint16_t a0 : left.exponent) {
                  const uint32_t a_exp =
                      (a0 + left_shift + N - normalizer) % N;
                  if (a_exp == anchor_left) continue;
                  const uint32_t av = roots[a_exp];
                  for (uint16_t t0 : right.exponent) {
                    const uint32_t t_exp =
                        (t0 + right_shift + N - normalizer) % N;
                    if (t_exp == 0) continue;
                    const uint32_t tv = roots[t_exp];
                    uint32_t left_coefficient = 0;
                    left_coefficient = mod_add(left_coefficient, mod_mul(av, tv));
                    left_coefficient = mod_add(left_coefficient, av);
                    left_coefficient = mod_add(left_coefficient, mod_mul(r_value, tv));
                    left_coefficient = mod_add(left_coefficient, r_value);
                    left_coefficient = mod_sub(left_coefficient, mod_mul(av, r_value));
                    left_coefficient = mod_sub(left_coefficient, mod_mul(tv, tv));
                    left_coefficient = mod_sub(left_coefficient, tv);
                    left_coefficient = mod_sub(left_coefficient, 1);

                    uint32_t right_coefficient = 0;
                    right_coefficient = mod_add(right_coefficient, mod_mul(av, av));
                    right_coefficient = mod_add(right_coefficient, mod_mul(av, r_value));
                    right_coefficient = mod_add(right_coefficient, mod_mul(r_value, r_value));
                    right_coefficient = mod_add(right_coefficient, tv);
                    right_coefficient = mod_sub(right_coefficient, mod_mul(av, tv));
                    right_coefficient = mod_sub(right_coefficient, av);
                    right_coefficient = mod_sub(right_coefficient, mod_mul(r_value, tv));
                    right_coefficient = mod_sub(right_coefficient, r_value);
                    if (left_coefficient == 0 && right_coefficient == 0) {
                      throw std::runtime_error("both product-line coefficients vanish");
                    }
                    ++decorated_product_line_records;
                    product_line_left_degenerate += left_coefficient == 0;
                    product_line_right_degenerate += right_coefficient == 0;
                  }
                }
              };
              count_decorations(a, 0, x, b, shift, y0, y);
              count_decorations(b, shift, y0, a, 0, x, x);
            }
          }
        }
      }
    }
    begin = end;
  }

  uint64_t max_product_multiplicity = 0;
  uint32_t max_product_signature = 0;
  for (const auto& [signature, count] : product_multiplicity) {
    if (count > max_product_multiplicity) {
      max_product_multiplicity = count;
      max_product_signature = signature;
    }
  }
  uint64_t max_cross_ratio_incidence = 0;
  uint32_t max_cross_ratio = 0;
  uint64_t cross_ratio_total = 0;
  for (uint32_t r = 0; r < N; ++r) {
    cross_ratio_total += cross_ratio_incidence[r];
    if (cross_ratio_incidence[r] > max_cross_ratio_incidence) {
      max_cross_ratio_incidence = cross_ratio_incidence[r];
      max_cross_ratio = r;
    }
  }
  uint64_t normalized_product_cell_total = 0;
  uint64_t max_normalized_product_cell_multiplicity = 0;
  uint64_t max_normalized_product_cell = 0;
  for (const auto& [cell, count] : normalized_product_cell_multiplicity) {
    normalized_product_cell_total += count;
    if (count > max_normalized_product_cell_multiplicity) {
      max_normalized_product_cell_multiplicity = count;
      max_normalized_product_cell = cell;
    }
  }

  std::cout << "n=" << N << " p=" << modulus
            << " smooth_necklaces=" << records.size()
            << " trade_orbits=" << trade_orbits
            << " product_signatures=" << product_multiplicity.size()
            << " max_product_multiplicity=" << max_product_multiplicity
            << " max_product_signature=" << max_product_signature
            << " normalized_product_cells="
            << normalized_product_cell_multiplicity.size()
            << " normalized_product_cell_total="
            << normalized_product_cell_total
            << " expected_normalized_product_cell_total=" << 8 * trade_orbits
            << " max_normalized_product_cell_multiplicity="
            << max_normalized_product_cell_multiplicity
            << " max_normalized_product_cell=" << max_normalized_product_cell
            << " decorated_product_line_records="
            << decorated_product_line_records
            << " expected_decorated_product_line_records="
            << 288 * trade_orbits
            << " product_line_left_degenerate="
            << product_line_left_degenerate
            << " product_line_right_degenerate="
            << product_line_right_degenerate
            << " cross_ratio_total=" << cross_ratio_total
            << " expected_cross_ratio_total=" << 32 * trade_orbits
            << " max_cross_ratio_incidence=" << max_cross_ratio_incidence
            << " max_cross_ratio=" << max_cross_ratio << '\n';
  if (cross_ratio_total != 32 * trade_orbits) {
    throw std::runtime_error("cross-ratio incidence accounting failed");
  }
  if (normalized_product_cell_total != 8 * trade_orbits) {
    throw std::runtime_error("normalized product-cell accounting failed");
  }
  if (decorated_product_line_records != 288 * trade_orbits) {
    throw std::runtime_error("decorated product-line accounting failed");
  }
  std::cout << "PASS_P06B3V_PRODUCT_PAIR_AND_CROSS_RATIO_PROBE\n";
  return 0;
}
