# Wolfram exact replay

Wolfram Language independently evaluated the selected integer cell at
`tau=1547`, `h=42452`.

```text
A                         1114501
c                          131850
d                           65925
multiplicity               982651
M2                            252
rank2 group cap         247628052
high tail        68875044016173272
N1                    7365150514
N2                     589969647
rank1 total      60010642445729852
rank2 total     146093034425737644
total           274978720888758363
slack                2007222636724
next-h over       17108854816460
```

The replay used exact integers only.  The exhaustive all-cutoff maximization is
performed twice by the shipped Python implementations; Wolfram is an
independent selected-cell arithmetic control rather than a proof dependency.
