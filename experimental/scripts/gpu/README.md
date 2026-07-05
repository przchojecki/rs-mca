# Optional CUDA Accelerators

This directory contains optional CUDA accelerator clients; nothing in the
repository depends on them, and every committed mathematical claim remains
checked by CPU/stdlib verifiers. The directory exists so the kernel-source
SHA-256 values recorded in certificate `gpu_run` blocks resolve to inspectable
code.

The sparse-census convention is the one recorded in
`experimental/notes/m1/sigma_c_sparse_census.md`: "Future GPU searches may use
only finite-slope-preserving upper-triangular reductions before returning
candidate witnesses to an exact verifier; full Mobius reductions are out of
scope because they can move finite slopes to the projective point at infinity."

The clients are optional tooling for finite census and staircase experiments.
They do not replace the certificate verifiers and do not upgrade any theorem
status.

The CUDA kernels are written to avoid cuBLAS. In particular, the clients use
RawKernel launches and plain modular integer arithmetic rather than matrix
products, `einsum`, or tensor contractions.

Check the recorded kernel provenance without importing these modules:

```powershell
python experimental/scripts/verify_gpu_engine_provenance.py --check
```

Optionally test CUDA availability on the current host:

```powershell
python experimental/scripts/verify_gpu_engine_provenance.py --self-test
```
