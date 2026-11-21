# Cloud Network Visualization Lab

**Created:** 2025-05-05  
**Project type:** Network engineering prototypes and visualization experiments

A collection of interactive and code-based experiments for exploring cloud connectivity, network configuration, topology relationships, routing paths, VRF concepts, and network operations dashboards.

## Purpose

This repository is a lab for prototyping network visualization and analysis ideas. It brings together exploratory implementations that may later be developed into standalone tools.

## Areas of Exploration

- Cloud and data-center connectivity dashboards
- VRF and network relationship visualization
- Configuration parsing and impact analysis
- Network path exploration
- Connectivity inventory and service-provider concepts
- Notifications and dashboard interaction patterns
- Python-based graph visualization and analysis

## Repository Contents

The repository currently contains experimental scripts and standalone prototypes with historical filenames. A reviewed subset includes:


| File | Description |
|---|---|
| `dashboard.html` | Browser dashboard concept for tracking cloud connectivity records |
| `dashboard.js` | Client-side dashboard logic and sample connectivity record handling |
| `DC` | Python experiment for collecting AWS Direct Connect details |
| `DM-vis-1` | Browser-based network configuration impact visualization |
| `DM-Vis-2` | Python graph and network configuration analysis prototype |
| `Gem_Visual_1`, `Gem_Visual_2`, `Gem_Visual_3` | Configuration parsing and network graph experiments |
| `Gro-Vis-1`, `Gro_vis_2`, `Gro-Vis_3` | Cisco configuration parsing and network visualization experiments |
| `path` | Network path analysis CLI experiment |
| `three-csp` | Cloud connectivity data collection prototype |

Other files represent additional experiments and are catalogued progressively. Filenames and implementations may change as prototypes are reviewed and consolidated.

## Technology Areas

- Python
- JavaScript and HTML
- Network configuration parsing
- Graph modeling and visualization
- AWS connectivity APIs
- Interactive dashboards

Specific dependencies vary by experiment. Refer to the imports within individual files before installing dependencies.

## Getting Started

1. Clone the repository.
2. Review the experiment you intend to run.
3. Install only the dependencies required by that experiment.
4. Use synthetic configuration, account, network, and connectivity data.
5. Run the prototype in a sandbox or local development environment.

These experiments are not yet packaged as one application. Some may require additional dependencies, API permissions, data inputs, or implementation work.

## Safety and Data Handling

- Use synthetic or sanitized data only.
- Do not commit credentials, cloud account identifiers, private IP plans, customer data, or real network configurations.
- Review API permissions and data access before running cloud collection scripts.
- Treat these prototypes as local development tools until they have been reviewed and tested.

## Limitations

- Experiments have different levels of maturity.
- There is no unified application entry point or shared dependency management yet.
- Some scripts may be incomplete or require modification.
- Automated testing and runtime verification have not been performed across the repository.

## Roadmap

- Review and classify all prototypes.
- Identify duplicate or overlapping implementations.
- Consolidate related experiments into clearly named modules.
- Standardize filenames and dependency declarations.
- Add sample sanitized datasets and usage notes.
- Add tests and CI checks as prototypes mature.
- Develop selected experiments into independently documented tools.

## License

No license has been added yet. Until a license is selected, reuse and redistribution are not explicitly granted.
