# KoalaBear v4 K3 active-slice semantic bridge route cut v1

This is a zero-payment semantic route cut, not a K3 closure.  It repairs and
replays the #1139 tangent source pin, so `U_paid=981104` is again bankable on
the present source.  It then identifies the first still-missing K3 theorem:
an executable actual-slope predicate and a same-record
selector/reconstruction/projection from the active post-Q balanced-core
`m_in=2,r_out=4` slice to the supplied endpoint records used by the raw K3
workboard.

The packet includes an exact countermodel over the deployed KoalaBear base
field and its actual order-`2^21` carrier.  Thirty active and six source
degree-two fibers of `h(T)=T(1-T)` split completely on the carrier and satisfy
the printed source-pencil identities, but the displayed deck involution
`tau(T)=1-T` does not preserve the carrier: `1` lies in the carrier and
`tau(1)=0` does not.  This disproves only the direct-coordinate shortcut.  It
is not an actual MCA received-line counterexample.  The packet explicitly
records that conjugating by `T-1/2` sends `tau` to `-T`, which does preserve
the even-order subgroup; no claim against arbitrary conjugated same-record
folds is made.

The active MCA ledger remains

```text
U_paid = 981104
U_Q    = null
U_BC   = null
U_new  = null
```

All K3-local quantities remain `null`; ledger movement is zero.  The joint
reserve `274980728110413983` is not a K3 allocation.  The five-term
`U_list-int/U_ext` chronology belongs to LIST and is rejected here.

## Replay

From the repository root:

```bash
python3 -B experimental/scripts/verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1.py --check
python3 -B experimental/scripts/verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1.py --tamper-selftest
python3 -B -O experimental/scripts/verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1.py --check
python3 -B -O experimental/scripts/verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1.sage
~/math_code/.venv/bin/python experimental/scripts/verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1_flint.py
```

For the external public-DAG source bindings, add:

```bash
python3 -B experimental/scripts/verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1.py \
  --check --source-root /path/to/rs-mca-prize-dag
```

The primary checker uses strict duplicate-key-safe integer JSON, checks the
canonical payload seal and source bindings, reconstructs the complete
2,097,152-point subgroup and all 1,071 internal involution pairs, and rejects
hostile semantic mutations.  Sage and FLINT are independent implementations.
The companion Wolfram script was independently replayed through the connected
Wolfram evaluator.  When cloud credits are available, the local project
wrapper command is:

```bash
~/math_code/scripts/wm.sh -file \
  experimental/scripts/verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1.wl
```

The predecessor #1157 packet deliberately binds its historical stale tangent
gate.  Replay it only in an untouched checkout at exact #1157 head
`d7f0fd9370b3c13ff93293f08e03cadddb59b921`; this new packet binds #1157 by
hash rather than rewriting its historical verifier.
