# Special-case proofs for image-normalized Sidon payment (W50-M2)

## Status
EXPERIMENTAL. **Rung: PROVED-SPECIAL** (subclasses only; full C9 open).

## Phase 0
`image_scale_mi_ma` cube3: **E=216**, Δ=**27/64** (reproduced).

## Lemma I — injective folding (PROVED)
If Φ is injective, then L=|Ω|, barN=1, f_s=1 for all s, hence
Gsid ≤ 1 and rate ≤ 0 ≤ τ.

Toy certificate: ≥5 injective power-sum instances with Gsid≤1.

**Discharges:** near-injective / exact-injective charts (bounded fold, barN=1).

## Lemma II — max-fiber control (PROVED)
Gsid ≤ (max_s f_s / barN)^q, so rate ≤ log(max_f/barN)/N.
If max_f ≤ exp(η N) barN with η≤τ, payment holds.

Toy certificate: inequality holds on all enumerated sweep toys.

**Discharges:** any chart with proved exponential max-fiber control.
**Open:** proving that control for low-energy fibers on deep charts.

## Lemma III — singleton low-energy fibers (PROVED)
If every low-energy fiber has f_s≤1, then Gsid≤1.

## REDUCED open core
Prove: on deep power-sum charts (R√p not o(N)), no low-energy fiber satisfies
f_s ≥ exp(η N)·barN for fixed η,σ>0. Equivalently low-energy max-fiber ratio is
exp(o(N)). This is Lemma II's missing analytic input (true C9 content).

## Dual routes
- **generator:** elementary inequalities + exact toy enumeration
- **checker:** four-tuple energy Gsid recompute + injective re-enum + Lemma II check

## Nonclaims
- Not a full proof of `ass:image-normalized-sidon-input` / C9.
- Injective subclass is real but narrow.

## Reproducibility
```text
py -3.13 experimental/scripts/verify_sidon_special_case_proof.py --check
payload_sha256: a017e945632ee4cbf8c434193405e539fdc531baf2dc8062e8c2cb1558e1b9ce
```
