# KoalaBear active carrier-incidence replay certificate

This certificate replays the full-outside carrier-sensitive one-cut compiler
at the six-owner active reserve.

```text
scan range     9209..913631
paid           9209..67466
open           67467..236112
paid           236113..913631
additional charge 0
```

Replay:

```sh
python3 experimental/scripts/verify_kb_mca_v4_active_carrier_incidence_replay_v1.py --check
python3 experimental/scripts/verify_kb_mca_v4_active_carrier_incidence_replay_v1.py --tamper-selftest
```

The certificate does not construct an RS selector in the open interval and
does not close the row.
