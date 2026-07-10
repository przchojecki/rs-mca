
# Audit: #444 C9 absorption into profile-envelope revision

## Claim
Verdict **NO ISSUE**: #444 k=5 numbers recompute exactly; the paper absorbs Sidon-heavy residual fibers via `def:sidon-paid` / `thm:primitive-q` (not by equating #444 to the paper's smooth-square obstruction). `thm:polynomial-obstruction` is a **distinct** construction.

## Status
EXPERIMENTAL / AUDIT.

## Key numbers (k=5)
A_k=120, heavy=32, M=152, L=121, E=7776, Delta=243/1024.

## Dual routes
A_k multinomial vs factorial (gen) / falling-factorial (check); energy 6^k.

## Reproducibility
```
py -3.13 experimental/scripts/verify_counterexample_absorption.py --emit --check
py -3.13 experimental/scripts/verify_counterexample_absorption_check.py --check
```
