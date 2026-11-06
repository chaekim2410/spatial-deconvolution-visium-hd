# Recovered source audit

The portfolio was checked against the recovered group repository at commit `8810ca1` (`DRIESASTER/spotless-benchmark`, 1 June 2025). The goal was to retain the code that supports the project story without copying the entire 549 MB working tree.

## Retained from the group project

| Recovered material | Portfolio location | Audit result |
|---|---|---|
| tissue-splitting function | `execution/split/split_tissue_function.py` | byte-for-byte identical |
| splitting test notebook | `execution/split/test_split_tissue_function.ipynb` | code cells preserved |
| three standard-Visium notebooks | `exploration/visium/` | code cells preserved; notebook outputs cleared |
| Visium HD SpatialData creation notebook | `exploration/visium_hd/Creation_sdata_object_Visium_HD.ipynb` | code cells preserved; outputs cleared |
| partition merge notebook | `execution/merge/merge_partition_results.ipynb` | code cells preserved; renamed for clarity |
| original Visium HD PBS submission | `provenance/group_project/execution/vis_hd_original.pbs` | recovered commands preserved; trailing whitespace normalized |
| group-specific Nextflow HPC changes | `provenance/group_project/execution/nextflow_hpc_profile_changes.md` | focused record of the substantive changes against the pre-project upstream state |
| six plotting scripts used for comparison/provenance | `provenance/group_project/plots/` | byte-for-byte identical |
| selected full/split proportion matrices | `data/proportions/` | byte-for-byte matches for the retained nuclei/JB01 result files; narrowed to the main story |

The retained HD sparsity notebook is the more complete local analysis copy supplied separately during curation. It contains substantially more QC, Sankey, spot-usage, and distribution analysis than the shorter `Visium_HD_sparsity.ipynb` found in the recovered Git repository.

## Retained in portable form

- The recovered HD PBS file used hard-coded university storage and cache paths. `execution/run_methods/run_split_deconvolution.pbs` preserves its method loop, Nextflow call, reference annotation, and Apptainer setup while replacing retired paths with explicit environment variables.
- The recovered H5AD-to-RDS helper contained one contributor's Windows paths. `execution/prepare_inputs/convert_h5ad_to_rds.R` preserves the conversion operation but accepts input and output paths as command-line arguments.

## Linked instead of copied

The full Spotless `main.nf`, Dockerfiles, and NNLS/RCTD/cell2location implementations are upstream benchmark software rather than group-authored method implementations. The portfolio links to the upstream repository and retains only the group-specific execution layer and HPC-profile patch.

## Intentionally excluded

- raw or processed RDS/H5AD/Zarr objects and tissue images;
- Nextflow work directories, Apptainer caches, model checkpoints, `.out`/`.err` logs, and temporary test files;
- `.DS_Store`, the duplicate ZIP archive, and IDE project metadata;
- failed test PBS scripts and experimental cell2location edits that did not contribute to the final analysis;
- redundant `uncover`/`zonation` scripts that were not used in the report's core split-versus-full conclusion;
- the complete NNLS/reference-sensitivity result grid, because the portfolio focuses on the selected nuclei reference and retains only compact evidence needed for that story.

The omitted `JB02`–`JB04` matrices are not missing experiments: they remain in the recovered group repository and were used by the upstream four-slide benchmark evaluation. They are outside the report's `JB01` full-versus-split case study retained here.

This audit supports a hybrid portfolio: historical implementation remains visible, while the top-level workflow stays small enough to review.
