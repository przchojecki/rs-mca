# Floor-Budget Retarget Slack Scan

Status: AUDIT / replayable arithmetic guardrail.

This note vendors the smooth-RS prize DAG node `floor_budget_slack_scan` into
the current finite-adjacent certificate vocabulary.  It asks whether several
safe-side floor constants can be weakened by spending slack that appears later
in the consumer arithmetic.

The answer is mixed and useful:

- the split-pencil / balanced-core small-core floor is essentially binding;
- the petal floor has real standing room at the official maximal rows; and
- the worst-word envelope has no free uniform slack unless the QA.22
  attribution convention is changed.

Replay:

```bash
python3 experimental/scripts/verify_floor_budget_retarget_slack_scan.py
```

## Scope

The script checks the arithmetic consequences of already banked compiler
outputs.  It does not replay those compiler outputs themselves.  In particular,
it treats the following as cited inputs:

- the clean-rate poly-forcing compiler, which consumes a uniform `16 n^3`
  small-core residual and is prize-row tight at about `29 n^3`;
- the petal floor-window calculation, whose saturated paid family is the
  degree-six binomial column `binom(n+6,6)`;
- the QA.22 four-column worst-word gate, whose within-column slack and
  aggregate-vs-budget convention are recorded elsewhere.

The value of this packet is negative information: it prevents the finite row
program from softening a hard primitive target by spending slack that is not
actually available at the certificate boundary.

## Balanced-Core / Split-Pencil Small-Core Floor

The clean-rate consumer chain uses a uniform small-core residual of shape

```text
16 n^3.
```

At the binding prize-max row in that chain, the available budget is only about

```text
29 n^3 = 2^127.86...
```

Thus the largest uniform retune of the constant is

```text
16 -> 29,
```

which is less than one bit:

```text
log2(29/16) = 0.858...
```

Consequence: the `n^3` primitive split-pencil / residual-ray count has to be
proved essentially at the stated scale.  There is no material consumer slack
to weaken it.

## Petal Floor

For the petal floor, the saturated paid family is the degree-six column

```text
binom(n+6, 6).
```

At the four official maximal rows `n = 2^41, 2^42, 2^43, 2^44`, the effective
exponents are about

```text
5.7685, 5.7740, 5.7793, 5.7843.
```

So the printed `n^6` budget has roughly `9.5` bits of room at every row.  The
same remains true for the checked excess sweep through `c = 14`, since the
column remains degree six.

Consequence: the petal floor is not the binding retarget obstruction.  Any
attempt to push beyond exponent `6` is gated by the codegree/image-fiber to
list-safe conversion, not by this paid family.

## Worst-Word Envelope

The QA.22 worst-word gate has large within-column staircase room at the prize
rows, but the aggregate line under the conservative convention is only about
`0.9` bits below the row budget.

Consequence: this is not free arithmetic slack.  Spending the within-column
room on the challenger envelope would be a cross-column re-attribution decision
under the QA.22 convention, and should stay explicit in any finite adjacent
certificate.

## Certificate-Program Consequence

The retarget tactic pays only in the petal lane.  It is dead for the
balanced-core/split-pencil small-core residual and blocked by convention for
the worst-word envelope.  For the current frontiers-paper vocabulary, this is a
profile-envelope / lower-reserve guardrail: the primitive residual-ray and
small-core targets should not be silently relaxed by downstream budget slack.
