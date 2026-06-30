# Proximity certificate scan

- Security target: `2^-128`
- Row: `n=512`, `k=256`, `rho=1/2`
- Fields: `q_gen=2367911594760467245844106297320951247361`, `q_line=2367911594760467245844106297320951247361`, `q_chal=2367911594760467245844106297320951247361`, `q_base=2367911594760467245844106297320951247361`
- Budgets: `floor(q_line/2^lambda)=6`, `floor(q_chal/2^lambda)=6`

## Agreement scans

| a | sigma | r | entropy margin bits | Qprof bits | line exact | list unique | combined verdict |
|---:|---:|---:|---:|---:|---|---|---|
| 257 | 1 | 255 | -376.369 | 250.673 | UNKNOWN outside r <= floor((n-k)/3) | UNKNOWN outside r <= floor((n-k)/2) | UNSAFE_BY_PROVED_LOWER_BOUND |
| 352 | 96 | 160 | 12102.632 | 1.585 | UNKNOWN outside r <= floor((n-k)/3) | UNKNOWN outside r <= floor((n-k)/2) | UNSAFE_BY_PROVED_LOWER_BOUND |
| 384 | 128 | 128 | 16331.493 | 0.000 | UNKNOWN outside r <= floor((n-k)/3) | PROVED exact list size 1 for every arity mu in high-agreement range | UNSAFE_BY_PROVED_LOWER_BOUND |
| 427 | 171 | 85 | 22038.961 | 0.000 | PROVED exact | PROVED exact list size 1 for every arity mu in high-agreement range | UNSAFE_BY_PROVED_LOWER_BOUND |
| 505 | 249 | 7 | 32518.263 | 0.000 | PROVED exact | PROVED exact list size 1 for every arity mu in high-agreement range | UNSAFE_BY_PROVED_LOWER_BOUND |
| 506 | 250 | 6 | 32655.237 | 0.000 | PROVED exact | PROVED exact list size 1 for every arity mu in high-agreement range | UNSAFE_BY_PROVED_LOWER_BOUND |
| 507 | 251 | 5 | 32792.437 | 0.000 | PROVED exact | PROVED exact list size 1 for every arity mu in high-agreement range | SAFE_BY_PROVED_UPPER_BOUND |
| 508 | 252 | 4 | 32929.902 | 0.000 | PROVED exact | PROVED exact list size 1 for every arity mu in high-agreement range | SAFE_BY_PROVED_UPPER_BOUND |
| 509 | 253 | 3 | 33067.693 | 0.000 | PROVED exact | PROVED exact list size 1 for every arity mu in high-agreement range | SAFE_BY_PROVED_UPPER_BOUND |
| 511 | 255 | 1 | 33344.697 | 0.000 | PROVED exact | PROVED exact list size 1 for every arity mu in high-agreement range | SAFE_BY_PROVED_UPPER_BOUND |
| 512 | 256 | 0 | 33484.496 | — | PROVED exact | PROVED exact list size 1 for every arity mu in high-agreement range | SAFE_BY_PROVED_UPPER_BOUND |

## Paper D universal cap scan

- Status: PROVED_PAPERD_V7_CAP
- Active caps: 1
- Strongest active cap: `N=512`, gap `1/256`, delta cap `127/256`, margin `253.553` bits

## Notes

- `SAFE_BY_PROVED_UPPER_BOUND` means all included protocol terms have theorem-backed upper numerators below the target.
- `UNSAFE_BY_PROVED_LOWER_BOUND` means theorem-backed lower numerators already exceed the target.
- `UNKNOWN_OR_CONDITIONAL` means at least one consumed term is outside a proved range, or only a conditional Paper B/C assumption is enabled.
- The scanner does not prove extension-line MCA, arbitrary-word locator local limits, or aperiodic Hankel-pencil packing; it flags those gaps.
