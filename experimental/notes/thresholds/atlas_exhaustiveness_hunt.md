# Atlas exhaustiveness hunt (W56-M1, hard input a)

## Status
EXPERIMENTAL. **Rung: MEASURED-SUPPORT.**

## Phase 0 pastes (rule 1b)
```
1453:\label{def:first-match}
1441:\tag{2.2}\label{eq:realized-profile-scale}
1607:\label{thm:syndrome-secant-exact}
3609:\label{thm:exact-partial-occupancy}
3744:\label{thm:canonical-partial-occupancy-atlas}
433: first-match atlas is witness-exhaustive if its realized cells cover every witness
```

## Model
Bad slope = transverse syndrome-secant gamma (thm:syndrome-secant-exact).
Full atlas cells = all E with |E|<=t. Restricted = |E|=t only.

## Results
```text
n_instances = 13
missing_full_total = 0
missing_restricted_total = 265
routes_agree_all = true
```
Full secant atlas: exhaustive on sweep. Restricted sub-atlas: missing witnesses
(falsifiability of incomplete atlases).

## Dual routes
- generator: per-E gamma solve
- checker: brute gamma x E

## Reproducibility
payload_sha256: 0050a06b7b6fab7dbac945fcceb39f58d9cb57ada48c4c7a6f37b87160d97acf
