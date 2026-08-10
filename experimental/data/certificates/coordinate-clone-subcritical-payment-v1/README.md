# Coordinate-clone subcritical-payment certificate

This packet corroborates the theorem in
`experimental/notes/m2/coordinate_clone_subcritical_payment.md`.

Run from the repository root:

```bash
python3 experimental/scripts/verify_coordinate_clone_subcritical_payment.py --check
python3 -O experimental/scripts/verify_coordinate_clone_subcritical_payment.py --check
python3 experimental/scripts/verify_coordinate_clone_subcritical_payment.py --tamper-selftest
python3 -O experimental/scripts/verify_coordinate_clone_subcritical_payment.py --tamper-selftest
```

The checker uses only the Python standard library. It pins the current
owner-pencil source, checks the deployed inequalities and budgets, replays
affine-chart bidegree intersection seams over three fields, exhausts a small
integer grid, and rejects hostile metadata mutations.

The checker does not pay the unique large clone component, any fixed-owner
branch, complete `(E)`, or an adjacent row.
