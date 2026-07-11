# Experimental Scripts

Run scripts from the repository root, for example:

```sh
python3 experimental/scripts/verify_asymptotic_c9_parseval_split_prime_descent.py --check
python3 experimental/scripts/verify_asymptotic_c9_endpoint_shortened_plotkin.py --check
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
python3 experimental/scripts/verify_asymptotic_primitive_profile_character_frame_v1.py --check
python3 experimental/scripts/verify_asymptotic_primitive_profile_character_frame_v1.py --tamper-selftest
python3 experimental/scripts/verify_asymptotic_packed_flatness_converse_v1.py --check
python3 experimental/scripts/verify_asymptotic_packed_flatness_converse_v1.py --tamper-selftest
python3 experimental/scripts/verify_b2_twisted_hankel_transform_v1.py --check
python3 experimental/scripts/verify_b2_twisted_hankel_transform_v1.py --tamper-selftest
python3 experimental/scripts/verify_b2_full_rank_chg_normalization_bridge_v1.py --check
python3 experimental/scripts/verify_b2_full_rank_chg_normalization_bridge_v1.py --tamper-selftest
python3 experimental/scripts/experiment_b2_twisted_hankel_cancellation_v1.py --artifact-check
```

`experiment_rowsharp_q_prefix_atom_routes_v1.py --check` is a fast artifact
replay. Use `--full --write --check` only when regenerating the route evidence,
or `--case P N J W` for a single small-model case.

`verify_asymptotic_primitive_profile_character_frame_v1.py` checks a proved
finite character-frame implication, the five existing elementary-prefix toys,
and an exact block-parabola product where global absolute Fourier summation is
exponential but the packed multiplier is one.  Its source-specific semantic
residual packing hypothesis remains open; the script does not prove
primitive-profile Q, effective MI/MA, or the direct Sidon payment.

`verify_asymptotic_packed_flatness_converse_v1.py` checks the corrected finite
converse: the scaled full-dual infimum is exactly the max-atom multiplier, while
MSS Corollary 1.5 supplies the nontrivial image-scale family with raw Gram norm
at most `(3+2*sqrt(2))` times that multiplier.  The finite regression does not
prove MSS or the open source many-shell max-atom/large-sieve theorem.  The
regression covers cyclic and noncyclic product groups and includes a symbolic
family where a full-slice heavy atom forces exponential packed norm while its
semantic residual is uniformly flat under the same full-slice normalization.

`verify_b2_twisted_hankel_transform_v1.py` checks the exact zero-fiber divisor
normal forms, uniform subset-Fourier identity, nonsingular twisted Hankel
transform, and abstract polar/endpoint cancellation on deterministic small
fields.  It protects the Fourier sign, projective-divisor normalization, and
claim boundary.  It does not prove `N(0)<=n^3`, CHG, the lower-rank transform,
or the open signed aggregate estimate.

`verify_b2_full_rank_chg_normalization_bridge_v1.py` checks the proved
full-rank bridge from centered `T_d(v)` to the normalized Hankel--Salie
aggregate: rank duality, determinant reciprocity, canonical `-4` variables,
complete scalar phase, explicit `z_Z(v)`, deployed zero-fiber endpoint,
support-wise centering, coefficient Fourier pairing, Salie factorization, and
the deployed exponent conversion.  It does not prove the signed aggregate
bound or cover lower-rank pseudodeterminant strata.

`experiment_b2_twisted_hankel_cancellation_v1.py` supplies a CHG-linked toy
census.  It checks the ordinary-Hankel transform at the same `(p,c)` as two
integrated CHG toys, finds an explicit `(p,c)=(11,2)` case where the termwise
absolute transformed bound is `374 > n^3=125` but the signed value is about
`31.31`, measures polar-incidence reduction, and reconstructs the
original-coordinate Gaussian completion twists.  Those original-coordinate
twists are not substituted directly for the complementary-Hankel `z(v)`; the
bridge verifier checks the exact change of coordinates.  Use
`--artifact-check` for fast review; `--check` recomputes the full deterministic
census and takes roughly one minute on the reference machine.

The active Python scripts are intentionally flat in this directory. Several M1
and L1 verifiers import local helpers by module name, so scattering them into
topic subdirectories would require a package rewrite without improving the
research content.

Locator-fiber packet tools live under `scripts/locator/`.
