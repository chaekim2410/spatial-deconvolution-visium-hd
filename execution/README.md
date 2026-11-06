# Execution workflow

This folder follows the actual processing order:

1. `prepare_inputs/`: prepare the public spatial input and convert it to the format required by R methods.
2. `split/`: divide the tissue into a 2 × 2 spatial grid and save four inputs plus the spot-to-part map.
3. `run_methods/`: submit NNLS, RCTD, or cell2location on each partition through the portable PBS template.
4. `merge/`: combine four partition-level outputs for downstream summaries and visualisation.

## PBS/Nextflow submission

`run_methods/run_split_deconvolution.pbs` is a cleaned, portable version of the PBS submission pattern used in the group project. It loops over the four split spatial inputs and runs one method at a time through Nextflow.

It deliberately does **not** contain retired university paths, cache directories, account names, or project data paths. Set the required environment variables when submitting the job:

```bash
qsub -v PIPELINE_ROOT=/path/to/spotless-benchmark,SP_DATA_DIR=/path/to/split_rds,SC_DATA_FILE=/path/to/reference.rds,METHOD=rctd execution/run_methods/run_split_deconvolution.pbs
```

Use `METHOD=nnls`, `METHOD=rctd`, or `METHOD=cell2location`. The group used the same PBS template and changed this method parameter for the three deconvolution methods.

The full `main.nf` dispatcher and method implementations remain in the upstream [Spotless benchmark](https://github.com/saeyslab/spotless-benchmark), so `PIPELINE_ROOT` should point to a compatible checkout of that pipeline. They are intentionally not copied into this portfolio because the project contribution was running and analysing the methods, not implementing NNLS, RCTD, or cell2location themselves.
