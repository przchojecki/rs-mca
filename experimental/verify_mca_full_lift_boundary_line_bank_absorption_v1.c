#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

/* Full constant-memory replay of the official paid interval and wall. */

typedef __int128 i128;

enum {
    R = 1048576, D = 67448, K = 6, N = R + K, M = D + K,
    C = K - 1, BUDGET = 16777215, LINE = N - M + 1,
    CUTOFF = 65272,
};

static int64_t caps[CUTOFF + 1];

static void reject(const char *what, int e, int h) {
    fprintf(stderr, "REJECT %s e=%d h=%d\n", what, e, h);
    exit(1);
}

static int64_t raw_cap(int e, int h) {
    int64_t n = N - e, agreement = M - h;
    int64_t johnson = agreement * agreement - n * C;
    if (johnson > 0) return n * (agreement - C) / johnson;
    int64_t gap = -johnson;
    int64_t balance = 2 * agreement * agreement - n * C;
    int64_t tangent = (n - agreement) * (n - agreement)
                      - (n - 1) * gap;
    if (balance < 0 || tangent <= 0) reject("prefix", e, h);
    return (int64_t)(((i128)(n - 1) * n * n * (agreement - C))
                     / ((i128)agreement * tangent));
}

static int64_t prefix(int e) {
    caps[0] = 0;
    for (int h = 1; h <= CUTOFF; ++h) caps[h] = raw_cap(e, h);
    for (int h = CUTOFF - 1; h >= 1; --h) {
        if (caps[h + 1] < caps[h]) caps[h] = caps[h + 1];
    }
    int64_t total = 0;
    for (int h = 1; h <= CUTOFF; ++h) {
        total += (caps[h] - caps[h - 1]) * (e / h);
    }
    return total;
}

struct row {
    int e, q, H, layers, groups, branch, failure;
    int64_t prefix, base, direct, threshold, core, inside;
    int64_t sync, agreement, low, bound, slack;
};

static struct row record(int e) {
    struct row x = {0};
    x.e = e;
    x.q = (e - K) % 3;
    int s = (e - K) / 3;
    x.H = e - s - 1;
    int upper = x.H < M ? x.H : M;
    if (CUTOFF >= upper) reject("empty line bank", e, upper);
    x.prefix = prefix(e);
    x.base = x.prefix;
    x.groups = x.H < M;
    for (int h = CUTOFF + 1; h <= upper; ++h) {
        int64_t inside = 2LL * h - e;
        int64_t denominator = inside * inside - (int64_t)e * C;
        if (2 * h <= e || inside <= C || denominator <= 0) {
            x.branch = 2;
            x.failure = 1;
            return x;
        }
        int64_t classes =
            (int64_t)(((i128)e * (inside - C)) / denominator);
        if (classes < 1) reject("class count", e, h);
        x.base += 1 - classes;
        x.groups += (int)classes;
        ++x.layers;
    }
    x.direct = x.base + (int64_t)x.groups * LINE;
    if (x.direct <= BUDGET) {
        x.branch = 0;
        x.bound = x.direct;
        x.slack = BUDGET - x.bound;
        return x;
    }
    int64_t required = BUDGET - x.base + 1;
    if (required <= 0 || x.groups == 0) {
        x.branch = 2;
        x.failure = 2;
        return x;
    }
    x.threshold = (required + x.groups - 1) / x.groups;
    if (x.threshold < 2) {
        x.branch = 2;
        x.failure = 3;
        return x;
    }
    x.core = (x.threshold * M - N + x.threshold - 2)
             / (x.threshold - 1);
    x.inside = x.core - C;
    x.sync = e - x.inside + K;
    x.agreement = M - x.sync + 1;
    int64_t n = N - e;
    int64_t denominator = x.agreement * x.agreement - n * C;
    if (denominator <= 0) {
        x.branch = 2;
        x.failure = 4;
        return x;
    }
    x.low = n * (x.agreement - C) / denominator;
    x.bound = (int64_t)e * x.low + LINE;
    x.slack = BUDGET - x.bound;
    x.branch = x.bound <= BUDGET ? 1 : 2;
    x.failure = x.branch == 1 ? 0 : 5;
    return x;
}

static void print_row(const char *name, const struct row *x) {
    printf("%s e=%d q=%d H=%d branch=%d failure=%d prefix=%lld "
           "layers=%d groups=%d base=%lld direct=%lld threshold=%lld "
           "core=%lld inside=%lld sync=%lld agreement=%lld low=%lld "
           "bound=%lld slack=%lld\n",
           name, x->e, x->q, x->H, x->branch, x->failure,
           (long long)x->prefix, x->layers, x->groups,
           (long long)x->base, (long long)x->direct,
           (long long)x->threshold, (long long)x->core,
           (long long)x->inside, (long long)x->sync,
           (long long)x->agreement, (long long)x->low,
           (long long)x->bound, (long long)x->slack);
}

int main(void) {
    struct row first = {0}, last = {0}, wall = {0};
    int paid = 0, direct = 0, absorption = 0;
    for (int e = 101157; e <= 140000; ++e) {
        struct row x = record(e);
        if (x.branch == 2) {
            wall = x;
            break;
        }
        if (!paid) first = x;
        last = x;
        ++paid;
        if (x.branch == 0) ++direct; else ++absorption;
    }
    if (!(paid == 23649 && direct == 0 && absorption == 23649 &&
          first.e == 101157 && first.prefix == 1502226 &&
          first.groups == 6502 && first.base == 1497892 &&
          first.threshold == 2350 && first.bound == 3813525 &&
          last.e == 124805 && last.prefix == 1636955 &&
          last.groups == 34560 && last.base == 1604577 &&
          last.threshold == 440 && last.core == 65220 &&
          last.low == 126 && last.bound == 16706559 &&
          wall.e == 124806 && wall.failure == 5 &&
          wall.groups == 34564 && wall.base == 1604586 &&
          wall.threshold == 439 && wall.low == 127 &&
          wall.bound == 16831491)) {
        reject("interval census", wall.e, wall.H);
    }
    print_row("FIRST", &first);
    print_row("LAST_PAID", &last);
    print_row("FIRST_WALL", &wall);
    printf("MCA_FULL_LIFT_BOUNDARY_LINE_BANK_ABSORPTION_V1_SCAN_PASS "
           "paid=%d direct=%d absorption=%d\n",
           paid, direct, absorption);
    return 0;
}
