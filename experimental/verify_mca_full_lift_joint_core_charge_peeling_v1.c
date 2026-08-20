#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

/* Full constant-memory replay of the M31 joint-core charge interval. */

typedef __int128 i128;

enum {
    R = 1048576, D = 67448, K = 6, N = R + K, M = D + K,
    C = K - 1, BUDGET = 16777215, Q = N - M + 1,
    INITIAL_CUTOFF = 65304, MAX_LINES = 256,
};

static int64_t caps[M + 1];

static void reject(const char *what, int e, int value) {
    fprintf(stderr, "REJECT %s e=%d value=%d\n", what, e, value);
    exit(1);
}

static int raw_cap(int e, int h, int64_t *out) {
    int64_t shortened = N - e, agreement = M - h;
    if (agreement <= C) return 0;
    int64_t johnson = agreement * agreement - shortened * C;
    if (johnson > 0) {
        *out = shortened * (agreement - C) / johnson;
        return 1;
    }
    int64_t gap = -johnson;
    int64_t balance = 2 * agreement * agreement - shortened * C;
    int64_t tangent = (shortened - agreement) * (shortened - agreement)
                      - (shortened - 1) * gap;
    if (balance < 0 || tangent <= 0) return 0;
    *out = (int64_t)(((i128)(shortened - 1) * shortened * shortened
                      * (agreement - C))
                     / ((i128)agreement * tangent));
    return 1;
}

static int64_t prefix(int e, int cutoff) {
    caps[0] = 0;
    for (int h = 1; h <= cutoff; ++h) {
        if (!raw_cap(e, h, &caps[h])) reject("prefix", e, h);
    }
    for (int h = cutoff - 1; h >= 1; --h) {
        if (caps[h + 1] < caps[h]) caps[h] = caps[h + 1];
    }
    int64_t total = 0;
    for (int h = 1; h <= cutoff; ++h) {
        total += (caps[h] - caps[h - 1]) * (e / h);
    }
    return total;
}

static int choose_cutoff(int e) {
    int cutoff = INITIAL_CUTOFF;
    while (cutoff < M) {
        int h = cutoff + 1;
        int64_t overlap = 2LL * h - e;
        if (2 * h > e && overlap > C &&
                overlap * overlap > (int64_t)e * C) break;
        ++cutoff;
    }
    if (cutoff > INITIAL_CUTOFF && cutoff < M) cutoff += 2;
    if (cutoff >= M) reject("cutoff", e, cutoff);
    return cutoff;
}

struct charge {
    int64_t value, core_budget, full, remainder;
};

static struct charge joint_charge(int e, int lines) {
    struct charge x = {0};
    if (!lines) return x;
    int64_t pair_budget = e + (int64_t)lines * (lines + 1) * C / 2;
    int64_t trivial = (int64_t)lines * (M - 1);
    x.core_budget = pair_budget < trivial ? pair_budget : trivial;
    x.full = x.core_budget / (M - 1);
    if (x.full > lines) x.full = lines;
    x.remainder = x.core_budget - x.full * (M - 1);
    if (x.full == lines) {
        x.value = (int64_t)lines * Q;
        return x;
    }
    int64_t left = lines - x.full;
    i128 denominator = (i128)(M - x.remainder) * M;
    i128 numerator = (i128)(N - x.remainder) * M
                     + (i128)(left - 1) * N * (M - x.remainder);
    x.value = x.full * Q + (int64_t)(numerator / denominator);
    return x;
}

struct row {
    int e, failure, cutoff, lines, first_threshold, middle_threshold;
    int last_threshold, positive;
    int64_t prefix, groups, base, target, charge, core_budget;
    int64_t full, remainder, packing;
};

static struct row record(int e) {
    struct row x = {0};
    x.e = e;
    x.cutoff = choose_cutoff(e);
    x.prefix = prefix(e, x.cutoff);
    for (int h = x.cutoff + 1; h <= M; ++h) {
        int64_t overlap = 2LL * h - e;
        int64_t denominator = overlap * overlap - (int64_t)e * C;
        if (2 * h <= e || overlap <= C || denominator <= 0) {
            x.failure = 1;
            return x;
        }
        x.groups += (int64_t)(((i128)e * (overlap - C)) / denominator);
    }
    x.base = x.prefix + M - x.cutoff - x.groups;
    int64_t inside_sum = 0;
    for (int removed = 0; removed < MAX_LINES; ++removed) {
        struct charge q = joint_charge(e, removed);
        x.target = BUDGET - q.value;
        int64_t required = x.target - x.base + 1;
        if (required <= 0) {
            x.failure = 2;
            return x;
        }
        int64_t threshold = (required + x.groups - 1) / x.groups;
        if (threshold < 2) {
            x.failure = 3;
            return x;
        }
        if (!removed) x.first_threshold = (int)threshold;
        else if (removed == 1) x.middle_threshold = (int)threshold;
        x.last_threshold = (int)threshold;
        int64_t numerator = threshold * M - N;
        int64_t core = numerator <= 0 ? 0
            : (numerator + threshold - 2) / (threshold - 1);
        int64_t inside = core > C ? core - C : 0;
        ++x.lines;
        if (inside > 0) {
            inside_sum += inside;
            ++x.positive;
        }
        x.packing = inside_sum
            - (int64_t)x.positive * (x.positive - 1) * C / 2;
        x.charge = q.value;
        x.core_budget = q.core_budget;
        x.full = q.full;
        x.remainder = q.remainder;
        if (x.packing > e) return x;
        if (inside == 0) {
            x.failure = 4;
            return x;
        }
    }
    x.failure = 5;
    return x;
}

static void print_row(const char *name, const struct row *x) {
    printf("%s e=%d failure=%d cutoff=%d prefix=%lld groups=%lld base=%lld "
           "lines=%d positive=%d thresholds=%d,%d,%d packing=%lld "
           "charge=%lld target=%lld core_budget=%lld full=%lld rem=%lld\n",
           name, x->e, x->failure, x->cutoff, (long long)x->prefix,
           (long long)x->groups, (long long)x->base, x->lines, x->positive,
           x->first_threshold, x->middle_threshold, x->last_threshold,
           (long long)x->packing, (long long)x->charge,
           (long long)x->target, (long long)x->core_budget,
           (long long)x->full, (long long)x->remainder);
}

int main(void) {
    struct row first = {0}, last = {0}, wall = {0};
    int paid = 0, max_lines = 0;
    int line_count[MAX_LINES + 1] = {0};
    for (int e = 130199; e <= 130220; ++e) {
        struct row x = record(e);
        if (x.failure) {
            wall = x;
            break;
        }
        if (!paid) first = x;
        last = x;
        ++paid;
        ++line_count[x.lines];
        if (x.lines > max_lines) max_lines = x.lines;
    }
    if (!(paid == 21 && max_lines == 13 &&
          line_count[4] == 2 && line_count[5] == 10 &&
          line_count[6] == 3 && line_count[7] == 2 &&
          line_count[8] == 1 && line_count[10] == 1 &&
          line_count[13] == 2 &&
          first.e == 130199 && first.cutoff == 65504 &&
          first.prefix == 8421151 && first.groups == 269019 &&
          first.base == 8154082 && first.lines == 4 &&
          first.first_threshold == 33 && first.middle_threshold == 29 &&
          first.last_threshold == 29 && first.packing == 133986 &&
          first.charge == 981355 &&
          last.e == 130219 && last.cutoff == 65514 &&
          last.prefix == 11445963 && last.groups == 269400 &&
          last.base == 11178503 && last.lines == 13 &&
          last.first_threshold == 21 && last.middle_threshold == 18 &&
          last.last_threshold == 18 && last.packing == 134835 &&
          last.charge == 981513 &&
          wall.e == 130220 && wall.failure == 4 && wall.lines == 44 &&
          wall.positive == 43 && wall.cutoff == 65515 &&
          wall.prefix == 11904256 && wall.groups == 260559 &&
          wall.base == 11645636 && wall.first_threshold == 20 &&
          wall.middle_threshold == 16 && wall.last_threshold == 13 &&
          wall.packing == 97018 && wall.charge == 1962895 &&
          wall.target == 14814320 && wall.core_budget == 134950 &&
          wall.full == 2 && wall.remainder == 44)) {
        reject("census", wall.e, paid);
    }
    print_row("FIRST", &first);
    print_row("LAST_PAID", &last);
    print_row("FIRST_WALL", &wall);
    printf("RATE_HALF_MCA_M31_JOINT_CORE_CHARGE_PEELING_SCAN_PASS "
           "paid=%d max_lines=%d line_counts=4:%d,5:%d,6:%d,7:%d,8:%d,10:%d,13:%d\n",
           paid, max_lines, line_count[4], line_count[5], line_count[6],
           line_count[7], line_count[8], line_count[10], line_count[13]);
    return 0;
}
