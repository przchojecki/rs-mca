# Experimental Scripts

Run scripts from the repository root, for example:

```sh
python3 experimental/scripts/verify_l1_prefix_divisor_count.py
python3 experimental/scripts/verify_l1_prefix_dual_d3_subgroup_twisted_collision_bound.py
python3 experimental/scripts/verify_l1_monomial_dyadic_descent_local16.py
python3 experimental/scripts/verify_f1_arbitrary_anchor_split.py
python3 experimental/scripts/verify_m1_tangent_floor_gate_ladder.py
python3 experimental/scripts/verify_m1_depth_two_line_conic_resonance_reduction.py
python3 experimental/scripts/verify_q17_locator_mca.py \
  --check experimental/data/certificates/q17-locator-mca/q17_locator_mca_certificate.json
python3 experimental/scripts/f1_deep_point_list_to_ca_mca_sanity.py
python3 experimental/scripts/verify_l1_fourier_orbit_cancellation.py
python3 experimental/scripts/verify_l1_coset_chart_residue_bridge_v1.py --check
python3 experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py --check
python3 experimental/scripts/verify_m1_half_turn_pair_core_13_v1.py --check
python3 experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py --check
python3 experimental/scripts/verify_m1_nonconsecutive_window_normal_form_v1.py --check
python3 experimental/scripts/verify_rowsharp_q_prefix_atom_reductions_v1.py --check
python3 experimental/scripts/verify_rowsharp_q_prefix_atom_reductions_v1.py --tamper-selftest
python3 experimental/scripts/experiment_rowsharp_q_prefix_atom_routes_v1.py --check
python3 experimental/scripts/experiment_rowsharp_q_prefix_atom_routes_v1.py --tamper-selftest
python3 experimental/scripts/verify_rowsharp_q_singleton_topseam_v1.py --check
python3 experimental/scripts/verify_rowsharp_q_singleton_topseam_v1.py --tamper-selftest
```

`experiment_rowsharp_q_prefix_atom_routes_v1.py --check` is a fast artifact
replay. Use `--full --write --check` only when regenerating the route evidence,
or `--case P N J W` for a single small-model case.

The active Python scripts are intentionally flat in this directory. Several M1
and L1 verifiers import local helpers by module name, so scattering them into
topic subdirectories would require a package rewrite without improving the
research content.

Locator-fiber packet tools live under `scripts/locator/`.
