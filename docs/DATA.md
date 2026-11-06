# Data and file policy

## Public standard-Visium and snRNA-seq sources

The compact example uses the standard 10x Genomics Visium mouse liver sample `GSM5764414` from spatial series [GSE192741](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE192741). The method reference originated from the separate single-cell/single-nucleus series [GSE192740](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE192740). Both belong to the umbrella Liver Cell Atlas series [GSE192742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE192742) and the Guilliams et al. *Cell* paper, but they are different assay inputs.

This repository keeps only:

- the spot-to-part assignment table;
- small cell-type proportion matrices;
- generated comparison summaries and figures.

## Digitized snRNA-seq composition reference

`data/reference/digitized_snrna_composition_reference.csv` preserves the nine cell-type proportions used by the group analysis as an aggregate evaluation vector. Because the Spotless paper did not publish the numerical composition table, the group report states that the values were estimated from Figure 6—figure supplement 2 using WebPlotDigitizer. They were then stored as a hardcoded vector excluding `Others` in `provenance/group_project/plots/g_truth_plot.py`. The `normalized_within_nine_types` column is the corresponding JSD input vector.

The deconvolution methods instead used the processed object `liver_mouseStSt_nuclei_9celltypes_annot_cd45.rds`, derived upstream from GSE192740 with `annot_cd45` cell-type labels. I used this prepared object as an analysis input; I did not construct the atlas reference. It is not available locally. The included CSV is therefore only an approximate digitization—not a replacement for the method reference, a direct raw-data calculation, or spot-level ground truth. See `data/README.md` for source details.

## Restricted-access Visium HD analysis

The group project analyzed a Visium HD liver dataset at 16 micrometer resolution. No public download accession was identified in the project materials, and the complete source files were not recovered locally. The full count matrix, tissue images, SpatialData/Zarr objects, partition-level AnnData and RDS objects, and spot-level deconvolution matrices are not included.

The repository retains only:

- aggregate cell-type composition by method and partition;
- aggregate method-level spot usage;
- the JSD values reported for comparison with the digitized snRNA-seq composition reference;
- compact figures that do not allow reconstruction of the expression matrix;
- reusable code that can regenerate the summaries when authorized inputs are available.

## Files intentionally excluded

Large `.h5`, `.h5ad`, `.rds`, `.zarr`, trained model, and Nextflow work files are excluded. They are intermediate objects rather than useful portfolio artifacts and can exceed normal GitHub limits.

Because the Visium HD source data are not available as a public download in this project, neither its raw counts nor reconstructable processed objects are committed.

## Reproducibility note

The original proportion tables do not contain spot barcodes. Their row order is mapped back to spot identifiers using the saved `spots_and_parts.csv` assignment in the same way as the original analysis notebook. New method runs should export an explicit `spot_id` column to avoid relying on row order.

`results/derived_summaries/visium_hd_part_composition.csv` and `visium_hd_spot_usage.csv` are aggregate summaries created locally from group-project partition-level result files. The spot-level HD inputs remain outside the repository.
