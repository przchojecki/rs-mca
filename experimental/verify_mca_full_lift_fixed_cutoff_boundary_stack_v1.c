#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef __int128 i128;

enum {
    R = 1048576,
    D = 67448,
    K = 6,
    N = R + K,
    M = D + K,
    C = K - 1,
    BUDGET = 16777215,
    CUTOFF = 65200,
};

static int64_t caps[CUTOFF + 1];

static void reject(const char *what, int e, int h) {
    fprintf(stderr, "REJECT %s e=%d h=%d\n", what, e, h);
    exit(1);
}

static int64_t raw_cap(int e, int h) {
    int64_t n = N - e;
    int64_t agreement = M - h;
    int64_t johnson = agreement * agreement - n * C;
    if (johnson > 0) {
        return (int64_t)(((i128)n * (agreement - C)) / johnson);
    }
    int64_t gap = -johnson;
    int64_t balance = 2 * agreement * agreement - n * C;
    int64_t tangent = (n - agreement) * (n - agreement) - (n - 1) * gap;
    if (balance < 0 || tangent <= 0) reject("prefix cap", e, h);
    i128 numerator = (i128)(n - 1) * n * n * (agreement - C);
    i128 denominator = (i128)agreement * tangent;
    return (int64_t)(numerator / denominator);
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

static int64_t boundary_cap(int e, int h) {
    int64_t n = N - e;
    int64_t inside = 2LL * h - e;
    int64_t denominator = inside * inside - (int64_t)e * C;
    int64_t outside = M - h;
    if (2 * h <= e || inside <= 0 || denominator <= 0 ||
            !(n > outside && outside > C)) {
        reject("boundary cap", e, h);
    }
    int64_t classes = (int64_t)(((i128)e * (inside - C)) / denominator);
    int64_t line = (n - C) / (outside - C);
    return 1 + classes * (line - 1);
}

static void checkpoint(int e, int64_t p, int64_t stack, int64_t forcing,
                       int64_t threshold, int64_t core, int64_t low,
                       int64_t bound) {
    if (e == 98232 && !(p == 1381829 && stack == 391210 &&
            forcing == 1773039 && threshold == 15004177)) {
        reject("first checkpoint", e, 0);
    }
    if (e == 101149 && !(p == 1422377 && stack == 14327810 &&
            forcing == 15750187 && threshold == 1027029)) {
        reject("last direct checkpoint", e, 0);
    }
    if (e == 101150 && !(p == 1422391 && stack == 14530797 &&
            forcing == 15953188 && threshold == 824028 &&
            core == 67453 && low == 28 && bound == 3813329)) {
        reject("first absorption checkpoint", e, 0);
    }
    if (e == 101155 && !(p == 1422461 && stack == 15244572 &&
            forcing == 16667033 && threshold == 110183 &&
            core == 67446 && low == 28 && bound == 3813469)) {
        reject("endpoint checkpoint", e, 0);
    }
    if (e == 101156 && !(p == 1422475 && stack == 15528748 &&
            forcing == 16951223 && threshold == -174007)) {
        reject("adjacent checkpoint", e, 0);
    }
}

int main(void) {
    int direct = 0, absorption = 0, wall = 0;
    for (int e = 98232; e <= 101156; ++e) {
        int s = (e - K) / 3;
        int H = e - s - 1;
        int64_t p = prefix(e);
        int64_t stack = 0;
        for (int h = CUTOFF + 1; h <= H; ++h) {
            stack += boundary_cap(e, h);
        }
        int64_t forcing = p + stack;
        int64_t threshold = BUDGET - forcing + 1;
        int64_t core = -1, low = -1, bound = -1;

        if (forcing + (N - M + 1) <= BUDGET) {
            if (e > 101149) reject("late direct branch", e, H);
            ++direct;
        } else if (threshold >= 2) {
            core = (threshold * (int64_t)M - N + threshold - 2)
                   / (threshold - 1);
            int64_t inside = core - C;
            int64_t sync = e - inside + K;
            int64_t agreement = M - sync + 1;
            int64_t n = N - e;
            int64_t denominator = agreement * agreement - n * C;
            if (denominator <= 0) reject("low Johnson", e, H);
            low = (n * (agreement - C)) / denominator;
            bound = e * low + (N - M + 1);
            if (e > 101155 || bound >= BUDGET) {
                reject("absorption payment", e, H);
            }
            ++absorption;
        } else {
            if (e != 101156) reject("early wall", e, H);
            ++wall;
        }
        checkpoint(e, p, stack, forcing, threshold, core, low, bound);
    }
    if (direct != 2918 || absorption != 6 || wall != 1) {
        reject("branch census", 0, 0);
    }
    puts("MCA_FULL_LIFT_FIXED_CUTOFF_BOUNDARY_STACK_V1_SCAN_PASS "
         "paid=2924 direct=2918 absorption=6 adjacent_wall=1");
    return 0;
}
