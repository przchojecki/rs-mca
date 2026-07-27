# KoalaBear post-first-gap full-histogram replay

This packet recomputes the full-histogram carrier-incidence compiler at the
exact seven-owner reserve `270,780,212,960,575,880`.

```text
  9,209.. 67,470   paid by full-histogram incidence
 67,471             paid by the first-gap source-pencil owner
 67,472..213,050   open
213,051..913,631   paid by full-histogram incidence
```

It emits and hashes an exact one-over-budget scalar route-cut packing at all
`145,579` open slacks. The replay adds no charge.

```bash
python3 experimental/scripts/verify_kb_mca_v4_post_first_gap_full_histogram_replay_v1.py --check
python3 experimental/scripts/verify_kb_mca_v4_post_first_gap_full_histogram_replay_v1.py --tamper-selftest
```

```text
payload            196d6b8946e668ce0872c0d12d151cb96d7a007cb213a47240cecdb81b13ca8d
scan digest        ce849fe77a42ff173e51820cbdc1c252691ba8614fe9050f4550a7e643694b34
route-cut digest   8e68bd0b8fe3381881324e76b5a92d56e4160bb60f27f5d530f7e1699e3bb2fc
partition digest   7a57fa877417920862ed2fe2e5c569852555f78b73b046d320d5e7a65d98ebaa
```
