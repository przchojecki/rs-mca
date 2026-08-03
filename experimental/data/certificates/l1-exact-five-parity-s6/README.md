# Exact-five parity S6 certificate

**Author:** Manuel E. Rey-Álvarez Zafiria

The six JSON files record the two characteristic filters, their modular
terminals, and the complete terminal spectra. The independent auditor uses
scalar arithmetic, reconstructs every event witness, checks both norm
factorization manifests, recomputes 483 unique profiles, and verifies the
original even-support transport directly.

From the repository root:

```text
python experimental/scripts/audit_p04cw_parity_uniform_S6_theorem.py
```

The expected final line is:

```text
PASS_P04CW_INDEPENDENT_PARITY_UNIFORM_S6_AUDIT
```

The primary stages can be replayed separately with the paths in
`REPLAY.txt`. The primary stages require SymPy; the line-profile classifier
also requires NumPy. The package-level `SHA256SUMS` file authenticates the
note, sources and recorded certificates.
