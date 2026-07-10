# w35-sidon-direct-payment

## Status
EXPERIMENTAL / AUDIT. **Verdict: OPEN GAP**.

## Dual routes
- generator: Counter r(d)^2 energy per fiber + (f/barN)**q Sidon-heavy sum
- checker: 4-fold a-b=c-d energy + successive-multiply (f/barN)^q

## Reproducibility
```
py -3.13 experimental/scripts/verify_sidon_direct_payment.py --emit-defaults --check
py -3.13 experimental/scripts/verify_sidon_direct_payment_check.py --check
```
