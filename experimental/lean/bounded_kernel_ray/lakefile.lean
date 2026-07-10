import Lake
open Lake DSL

package «bounded_kernel_ray» where

@[default_target]
lean_lib «BoundedKernelRay» where
  roots := #[`BoundedKernelRay]
