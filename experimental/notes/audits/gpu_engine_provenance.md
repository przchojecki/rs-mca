# GPU Engine Provenance Audit

Status: AUDIT

This note records the optional CUDA accelerator source files whose kernel
SHA-256 values can be checked without importing GPU modules. The verification
path remains CPU/stdlib: certificates are checked by their committed verifiers,
and `verify_gpu_engine_provenance.py` only confirms that recorded kernel hashes
resolve to inspectable source.

## Engines

```text
engine file                                      RAWKERNEL_SOURCE SHA-256
experimental/scripts/gpu/sigmac_gpu.py          e0f55cfeaa5527ab9204dbe6de2ce019bc3535f29284deaa5b6775b4cb20be33
experimental/scripts/gpu/staircase_gpu.py       07187e9d04bf445cc3a9271d7cc5c2017c89eb5982762fbdd58609170603ba52
```

The recorded host check used CuPy 14.1.1 on an NVIDIA GeForce RTX 3090. The
clients avoid cuBLAS and use modular integer RawKernel launches.

## Certificate References

At base `c87675e68065651857ef2eedbfdfac81a001d15c`, the repository contains
placeholder `gpu_run: null` fields in the sparse-census packets and no non-null
`gpu_run` or `gpu_runs` block. Therefore the provenance verifier reports zero
non-null certificate references on this branch.

The intended contract is forward-facing: when a certificate records a
`kernel_source_sha256` value under `gpu_run` or `gpu_runs`, the verifier parses
the optional engine files with `ast`, computes the corresponding kernel-string
hashes, and fails if any recorded hash is unknown.

## Reproducibility

```powershell
python experimental/scripts/verify_gpu_engine_provenance.py --check
```

Expected result on this base: `PASS`, with the two engine hashes above and
`gpu_blocks_checked = 0`.

```powershell
python experimental/scripts/verify_gpu_engine_provenance.py --self-test
```

Expected result on a CUDA host with CuPy installed: `SELF-TEST: PASS`. On a
host without CUDA or CuPy, the self-test exits 0 with `SELF-TEST: SKIP`.

## Non-Claims

This audit does not claim that GPU output is a proof path, does not add a new
mathematical certificate, and does not change the status of any sigma or
staircase row. GPU output must still be returned to exact CPU certificate
checks before it supports a recorded finite claim.
