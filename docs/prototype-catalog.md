# Prototype Catalog

This document records reviewed prototypes and distinguishes exact duplicates from related but behaviorally different variants.

## Reviewed Experiments

| Path | Area | Review outcome |
|---|---|---|
| `dashboard.html`, `dashboard.js` | Cloud-connectivity dashboard | Browser dashboard concept with in-memory records and file-import interaction. |
| `DC` | AWS Direct Connect collection | Small boto3 collection experiment. |
| `three-csp` | Multi-cloud connectivity collection | Separate cloud connectivity collection sketch; not assumed equivalent to `DC`. |
| `DM-vis-1` | Browser impact visualization | Standalone browser visualization. |
| `DM-Vis-2` | Python impact analysis | Separate Python graph/configuration analysis prototype. |
| `Gem_Visual_1`, `Gem_Visual_2`, `Gem_Visual_3` | Configuration parsing and network impact | Same high-level function names, but different source contents and sizes. Retained as distinct historical iterations; no behavior-level equivalence established. |
| `prototypes/config-impact/gro_visualization.py` | Cisco network impact visualization | Canonical copy of the byte-identical `Gro-Vis-1` and `Gro_vis_2` files. |
| `Gro-Vis_3` | Hop-by-hop impact visualization | Distinct variant: its analysis signature and visualization function differ from the canonical Gro visualization. |
| `cald-vis-1`, `cald-vis-2` | Browser impact analysis | Related HTML applications with different source contents; retained. |
| `main-1`, `main-2`, `main-3` | Multi-cloud maintenance automation UI | Three different HTML iterations; retained pending feature-by-feature comparison. |
| `path` | Network path analysis | CLI-oriented network path analysis experiment. |
| `MSFT` | ExpressRoute architecture | Standalone architecture diagram. |
| `DM-Vis-2` | Network configuration analysis | Python model for routing, security policy and impact analysis. |

## Exact Duplicate Decision

- `Gro-Vis-1` and `Gro_vis_2` had the same Git blob SHA, confirming byte-identical contents.
- The content was copied to `prototypes/config-impact/gro_visualization.py`, fetched back, and verified byte-for-byte before both old root files were removed.
- No other exact duplicate blob groups were found among the 31 files in the reviewed tree at the time of comparison.

## Related Variants Not Merged

- The three `Gem_Visual` files expose the same top-level function names, but their content differs. Matching signatures alone do not establish equivalent parsing, impact analysis, or visualization behavior.
- `Gro-Vis_3` changes the analysis inputs and uses a hop-by-hop visualization path, so it remains separate.
- `cald-vis-1` and `cald-vis-2` are different browser implementations, not byte-identical files.
- `main-1`, `main-2`, and `main-3` are separate UI iterations. Their feature differences need a dedicated review before consolidation.
- `DC` and `three-csp` are related cloud-connectivity collectors but differ in scope and implementation.

## Review Limitations

This is a static source and repository-tree review. It does not prove runtime correctness, functional equivalence, cloud API behavior, or production readiness. Keep using synthetic data and least-privilege credentials for any local experiments.
