# M1 nonconsecutive coefficient-window normal form v1 certificate

Status: `PROVED`.

## Regeneration

```bash
python3 experimental/scripts/verify_m1_nonconsecutive_window_normal_form_v1.py --write
python3 experimental/scripts/verify_m1_nonconsecutive_window_normal_form_v1.py --check
python3 -m json.tool experimental/data/certificates/m1-nonconsecutive-window-normal-form-v1/m1_nonconsecutive_window_normal_form_v1.json
```

## Claim

Every printed two-row coefficient window `W={1,r}` satisfies the normal-form
identity `sum_h b_h theta_{r-2h}(R)=0` after half-turn decomposition.
The packet routes survivors into generated collision, honest half-turn,
recursive lower-core affine slice, or pair-deficient residual branches.

## Nonclaim

The pair-deficient residual branch is named but not paid by this packet.
