# Full-lift exact-layer slot-core packing

## Scope

This packet restores the exact-layer owner of every affine-line slot in the
Mersenne full-lift recursive bank.  It pays
`130226<=e<=130236`; it does not certify the adjacent support unsafe or close
the full Mersenne row.

## Exact-layer incidence

Let a selected affine explanation line contain `lambda>=2` members of one
exact layer `h`, and let `u` be its inside common core.  At an inside
coordinate outside that core, the line equation

```text
r_0+gamma*r_1 = a+gamma*b
```

holds for at most one line parameter `gamma`.  Every member has at least `h`
inside agreements, so incidence counting in the fixed `e`-coordinate support
gives

```text
lambda*h <= e+(lambda-1)u,
u >= ceil((lambda*h-e)/(lambda-1)).                 (EL1)
```

This is directly an inside-core lower bound; it spends none of the outside
zero allowance.  In this support interval the parent ceiling satisfies
`H>=m`, so every recursive-bank slot has one exact-layer owner and no
cross-layer top slot is present.

## Eleven support payments

Retain the core-dichotomy absorption cutoff `65450`.  In its complementary
branch each selected line has total-core cap

```text
G_e=e+9-65450.
```

Use the capped lower-aware convex charge, now with (EL1) as the selected
line's lower bound.  The following legal cutoffs force the same threshold on
each of the first three selected lines:

```text
e                 cutoff  lambda  EL1 lower u
130226             65516      14        60540
130227             65516       5        49340
130228             65517      13        60126
130229             65517       4        43948
130230             65518      11        59048
130231             65518       4        43949
130232             65519       9        57431
130233,130234      65520       7        54736
130235,130236      65521       4        43951
```

Here the printed `lambda` is the forced minimum slot size and `h=cutoff+1`
is the minimum possible exact layer.  In this range the right side of (EL1)
is nondecreasing in both variables, so using those minima is conservative.

Distinct selected lines have pairwise inside-core intersection at most
`c=5`.  Hence three selected lines violate support-size packing on every
printed row.  The smallest printed lower bound is

```text
3*43948-C(3,2)*5=131829>130229.
```

The high-core branch remains exhaustive and is at most `5161243`, so all
eleven supports are safe under the full-lift route.

## Adjacent shift-pair wall

At `e=130237`, cutoff `65521` is legal and has

```text
prefix=15893203, groups=1933560, base=13961576.
```

It forces only size-two affine explanation slots, the shift-pair stratum of
this line bank.  Formula (EL1) gives `u=807`, while

```text
max_s {s*807-C(s,2)*5}=65529<e.
```

After 7583 such lower bounds, the capped convex envelope has core budget
`143903917`, charge `882245`, residual target `15894970`, and next threshold
one.  No further actual line is forced.  This is a method wall, not an unsafe
certificate.  The Mersenne full-lift residual is therefore

```text
130237<=e<=1044241.
```

The next structural task is primitive shift-pair control, or a stronger
global coupling between these size-two exact-layer slots.

## Replay

```bash
python3 experimental/verify_mca_full_lift_exact_layer_slot_core_packing_v1.py
python3 experimental/audit_mca_full_lift_exact_layer_slot_core_packing_v1.py
```
