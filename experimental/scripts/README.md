# Experimental Scripts

Run scripts from the repository root, for example:

```sh
python3 experimental/scripts/verify_l1_prefix_divisor_count.py
python3 experimental/scripts/verify_m1_depth_two_line_conic_resonance_reduction.py
python3 experimental/scripts/verify_q17_locator_mca.py \
  --check experimental/data/certificates/q17-locator-mca/q17_locator_mca_certificate.json
python3 experimental/scripts/f1_deep_point_list_to_ca_mca_sanity.py
python3 experimental/scripts/verify_l1_fourier_orbit_cancellation.py
```

The active Python scripts are intentionally flat in this directory. Several M1
and L1 verifiers import local helpers by module name, so scattering them into
topic subdirectories would require a package rewrite without improving the
research content.

Locator-fiber packet tools live under `scripts/locator/`.
