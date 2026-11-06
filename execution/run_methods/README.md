# Submit deconvolution jobs

`run_split_deconvolution.pbs` is the project-specific execution wrapper retained in this portfolio. It loops over the four split spatial inputs and submits one selected method through the upstream Spotless Nextflow pipeline.

The group used this PBS pattern with `METHOD=nnls`, `METHOD=rctd`, and `METHOD=cell2location`. It requests the HPC resources, configures the Apptainer cache, and passes the SC reference plus one split SP input to Nextflow.

The NNLS, RCTD, and cell2location implementations themselves are upstream software. They are intentionally linked rather than copied here: [Spotless benchmark](https://github.com/saeyslab/spotless-benchmark). My portfolio contribution is the execution setup, spatial splitting, result merging, comparison, and visualisation.

For traceability, the recovered Visium HD PBS commands and the group's HPC-profile changes are archived under `provenance/group_project/execution/`. Those files contain retired institutional paths and are historical records, not current submission templates.
