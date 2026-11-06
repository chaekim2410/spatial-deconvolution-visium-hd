# Retained deconvolution proportions

This folder contains only small standard-Visium proportion matrices needed to reproduce the full-versus-split comparison.

- `nnls/`, `rctd/`, and `cell2location/` each contain the retained output for that method.
- `full.tsv` is a full-tissue result when it was recovered.
- `split/part_0.tsv` to `part_3.tsv` are independent results from the four spatial partitions.

These are deconvolution outputs, not expression counts. The full NNLS matrix was not recovered; its agreement value is kept as a paper-reported result in `results/reported_summary.csv`.

The retained RCTD and cell2location full/split matrices were generated with the `nuclei` / `annot_cd45` reference. The group project also ran `noEC`, `inVivo`, and `exVivo` reference conditions, but those sensitivity outputs are outside this focused portfolio comparison.
