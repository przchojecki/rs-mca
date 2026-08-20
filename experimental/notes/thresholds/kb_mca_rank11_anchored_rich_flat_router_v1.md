# KoalaBear rank-eleven anchored rich-flat router

Status: **proved direct branch payment / structural route cut**.  Zero
active-v4 ledger movement; no rank-eleven or KoalaBear closure.

For cutoff `tau=1547`, anchor one actual low-margin record and let
`G_0` be the portion of its exact size-`m` support on which its minimizing
pair equals the received pair.  Then

```text
A = m-tau = 1,114,501
|G_0| <= m
c = 2A-n = 131,850.
```

Every represented pair-difference row space of rank one or two annihilates at
least `c` labeled evaluation columns from `G_0`.

Call a row space `h`-transverse if no proper flat of its annihilator contains
more than `h` of those labels.  Greedy ordered-basis selection gives at least
`(c-h)^(s-r)` determining tuples.  Uniformly over explanation dimension
`s<=10`, the numbers of transverse row spaces are bounded by

```text
N_1 <= floor(m_fall_9/(c-h)^9),
N_2 <= floor(m_fall_8/(c-h)^8).
```

Rank-one groups cost at most `8,147,918` slopes by PR #1171.  Rank-two groups
have at most `252` pair types and cost at most `247,628,052` slopes.  At
`h=42,452`, the complete low/high/near sum is

```text
274,978,720,888,758,363 < B*
```

with slack `2,007,222,636,724`.

Therefore every unsafe survivor contains a proper annihilator flat on at least
`42,453` actual coordinates.  Orthogonal complementation yields a direction
subspace `W` strictly larger than the represented row space `U`, and all
polynomials in `W` share the squarefree locator of those coordinates.  Thus:

```text
rank(U)=1  => dim(W)>=2 and deg common factor >=42,453;
rank(U)=2  => dim(W)>=3 and deg common factor >=42,453.
```

In the second case `U` itself retains at least `131,850` common anchor zeros.
The next task is factor synchronization or chronology-safe shortening across
these emitted higher-dimensional spaces.
