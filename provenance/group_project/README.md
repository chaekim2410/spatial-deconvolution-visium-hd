# Group-project provenance

These scripts are retained to document how figures and comparisons were produced during the original group project. They may contain historical paths and should not be treated as the active reusable interface.

- `plots/g_truth_plot.py` contains the nine-cell-type digitized snRNA-seq composition values preserved in `data/reference/digitized_snrna_composition_reference.csv`.
- The reference follows the four-biological-replicate comparison framework in the original Spotless liver evaluation (`ABU11`, `ABU13`, `ABU17`, and `ABU20`).
- The underlying processed Liver Cell Atlas RDS files were not recovered and are therefore not redistributed here.

The group report states that the values were extracted with WebPlotDigitizer from a Spotless benchmark bar plot. The reference is therefore an approximate composition benchmark, not spot-level ground truth.

## Four-slide benchmark scope

The recovered repository contains full and split method outputs for `JB01`–`JB04`. The upstream [`3a_evaluate_liver_visium.R`](https://github.com/saeyslab/spotless-benchmark/blob/main/scripts/liver_analysis/3a_evaluate_liver_visium.R) script sets `datasets <- 1:4`, reads every slide/reference/method combination, calculates slide-level mean proportions, and averages the resulting metrics. The project notebooks then select `JB01` for the 1,293-spot full-versus-split case study shown in the group report.

## Historical execution files

- `execution/vis_hd_original.pbs` preserves the recovered PBS commands used to loop over split Visium HD RDS inputs and run RCTD through Nextflow; only trailing whitespace was normalized.
- `execution/nextflow_hpc_profile_changes.md` records the group's changes to the upstream Spotless HPC profile: local execution inside the PBS allocation, Apptainer configuration, and group storage paths.

These files intentionally retain retired university paths to document the original setup. Use the portable template in `execution/run_methods/` for a new run; do not submit the archival PBS file unchanged.
