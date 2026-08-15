#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

/* Full constant-memory replay of recursive M31 affine-line peeling. */

typedef __int128 i128;

enum {
    R = 1048576, D = 67448, K = 6, N = R + K, M = D + K,
    C = K - 1, BUDGET = 16777215, LINE = N - M + 1,
    INITIAL_CUTOFF = 65304, ADAPTIVE_MARGIN = 2, MAX_LINES = 32,
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

static int prefix(int e, int cutoff, int64_t *out) {
    if (cutoff < 1 || cutoff > M) return 0;
    caps[0] = 0;
    for (int h = 1; h <= cutoff; ++h) {
        if (!raw_cap(e, h, &caps[h])) return 0;
    }
    for (int h = cutoff - 1; h >= 1; --h) {
        if (caps[h + 1] < caps[h]) caps[h] = caps[h + 1];
    }
    int64_t total = 0;
    for (int h = 1; h <= cutoff; ++h) {
        total += (caps[h] - caps[h - 1]) * (e / h);
    }
    *out = total;
    return 1;
}

static int choose_cutoff(int e) {
    int cutoff = INITIAL_CUTOFF;
    while (cutoff < M) {
        int h = cutoff + 1;
        int64_t agreement = 2LL * h - e;
        if (2 * h > e && agreement > C &&
                agreement * agreement > (int64_t)e * C) break;
        ++cutoff;
    }
    if (cutoff > INITIAL_CUTOFF && cutoff < M) {
        cutoff += ADAPTIVE_MARGIN;
        if (cutoff > M) cutoff = M;
    }
    return cutoff;
}

struct row {
    int e, failure, finish, cutoff, lines, upper;
    int first_threshold, last_threshold;
    int64_t piece, bound, slack, inside_sum, packing;
    int64_t groups, base, target;
};

static struct row record(int e) {
    struct row x = {0};
    x.e = e;
    int H = e - (e - K) / 3 - 1;
    if (H < M) { x.failure = 1; return x; }
    x.cutoff = choose_cutoff(e);
    int64_t bank_prefix;
    if (x.cutoff >= M || !prefix(e, x.cutoff, &bank_prefix)) {
        x.failure = 2;
        return x;
    }
    int upper = M;
    while (x.lines < MAX_LINES) {
        int64_t target = BUDGET - (int64_t)x.lines * LINE;
        if (target < 0) { x.failure = 3; return x; }
        int64_t whole_prefix;
        if (prefix(e, upper, &whole_prefix) && whole_prefix <= target) {
            x.finish = 1;
            x.upper = upper;
            x.piece = whole_prefix;
            x.bound = (int64_t)x.lines * LINE + whole_prefix;
            x.slack = BUDGET - x.bound;
            return x;
        }

        int64_t groups = 0;
        for (int h = x.cutoff + 1; h <= upper; ++h) {
            int64_t agreement = 2LL * h - e;
            int64_t denominator = agreement * agreement - (int64_t)e * C;
            if (2 * h <= e || agreement <= C || denominator <= 0) {
                x.failure = 4;
                return x;
            }
            groups += (int64_t)(((i128)e * (agreement - C)) / denominator);
        }
        int64_t base = bank_prefix + upper - x.cutoff - groups;
        int64_t required = target - base + 1;
        if (required <= 0) {
            x.failure = 5;
            x.upper = upper;
            x.groups = groups;
            x.base = base;
            x.target = target;
            return x;
        }
        if (groups < 1) { x.failure = 6; return x; }
        int64_t threshold = (required + groups - 1) / groups;
        if (threshold < 2 || threshold > LINE) {
            x.failure = 7;
            return x;
        }
        if (!x.lines) x.first_threshold = (int)threshold;
        x.last_threshold = (int)threshold;
        int64_t numerator = threshold * M - N;
        int64_t core = numerator <= 0 ? 0
            : (numerator + threshold - 2) / (threshold - 1);
        int64_t inside = core > C ? core - C : 0;
        int64_t sync = e - inside + K;
        x.inside_sum += inside;
        ++x.lines;
        x.packing = x.inside_sum
            - (int64_t)x.lines * (x.lines - 1) * C / 2;
        if (x.packing > e) {
            x.finish = 2;
            x.upper = upper;
            return x;
        }
        if (sync - 1 < upper) upper = (int)sync - 1;
    }
    x.failure = 8;
    return x;
}

static void print_row(const char *name, const struct row *x) {
    printf("%s e=%d failure=%d finish=%d cutoff=%d lines=%d upper=%d "
           "piece=%lld bound=%lld slack=%lld inside=%lld packing=%lld "
           "first_threshold=%d last_threshold=%d groups=%lld base=%lld "
           "target=%lld\n",
           name, x->e, x->failure, x->finish, x->cutoff, x->lines,
           x->upper, (long long)x->piece, (long long)x->bound,
           (long long)x->slack, (long long)x->inside_sum,
           (long long)x->packing, x->first_threshold, x->last_threshold,
           (long long)x->groups, (long long)x->base,
           (long long)x->target);
}

int main(void) {
    struct row first = {0}, first_packing = {0}, last = {0}, wall = {0};
    int paid = 0, profile = 0, packing = 0, max_lines = 0;
    int line_count[MAX_LINES + 1] = {0};
    for (int e = 124806; e <= 130199; ++e) {
        struct row x = record(e);
        if (x.failure) { wall = x; break; }
        if (!paid) first = x;
        if (x.finish == 2 && !first_packing.e) first_packing = x;
        last = x;
        ++paid;
        ++line_count[x.lines];
        if (x.lines > max_lines) max_lines = x.lines;
        if (x.finish == 1) ++profile;
        else if (x.finish == 2) ++packing;
        else reject("finish", e, x.finish);
    }
    if (!(paid == 5393 && profile == 3837 && packing == 1556 &&
          max_lines == 5 && line_count[1] == 3534 &&
          line_count[2] == 397 && line_count[3] == 1397 &&
          line_count[4] == 59 && line_count[5] == 6 &&
          first.e == 124806 && first.bound == 2603990 &&
          first.first_threshold == 433 &&
          first_packing.e == 128340 && first_packing.lines == 2 &&
          first_packing.packing == 129391 &&
          last.e == 130198 && last.cutoff == 65504 && last.lines == 5 &&
          last.packing == 133160 && last.first_threshold == 34 &&
          last.last_threshold == 19 &&
          wall.e == 130199 && wall.failure == 5 && wall.lines == 9 &&
          wall.groups == 269019 && wall.base == 8154082 &&
          wall.target == 7947054 && wall.inside_sum == 126232 &&
          wall.packing == 126052)) {
        reject("census", wall.e, paid);
    }
    print_row("FIRST", &first);
    print_row("FIRST_PACKING", &first_packing);
    print_row("LAST_PAID", &last);
    print_row("FIRST_WALL", &wall);
    printf("MCA_FULL_LIFT_RECURSIVE_LINE_PEELING_CORE_PACKING_V1_SCAN_PASS "
           "paid=%d profile=%d packing=%d max_lines=%d "
           "line_counts=1:%d,2:%d,3:%d,4:%d,5:%d\n",
           paid, profile, packing, max_lines, line_count[1], line_count[2],
           line_count[3], line_count[4], line_count[5]);
    return 0;
}
