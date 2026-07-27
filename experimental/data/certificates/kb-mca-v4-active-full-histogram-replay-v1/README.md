# KoalaBear active full-histogram replay certificate

This certificate replays the complete selected-slope incidence bound at the
six-owner active reserve.

```text
scan range     9209..913631
paid           9209..67470
open           67471..209568
paid           209569..913631
additional charge 0
```

Replay:

```sh
python3 experimental/scripts/verify_kb_mca_v4_active_full_histogram_replay_v1.py --check
python3 experimental/scripts/verify_kb_mca_v4_active_full_histogram_replay_v1.py --tamper-selftest
```

The open scalar witnesses are route cuts, not deployed RS selectors.
