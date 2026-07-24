import M31SelectorSpectrum.Atlas
import M31SelectorSpectrum.SpectrumGenerator
import M31SelectorSpectrum.DeficiencyLaw

/-!
Public entry point for the M31 depth-32 selector-spectrum structural generator.

The package is self-contained and stdlib-only.  It proves that the exhaustive
68,896-edge selector-atlas maximum spectrum equals the pointwise maximum of one
central binomial law and four irredundant atlas-sourced coefficient laws, in
both block- and point-deficiency form.  It is support-selector level only; the
deployed interpretation of this spectrum is outside its scope.
-/
