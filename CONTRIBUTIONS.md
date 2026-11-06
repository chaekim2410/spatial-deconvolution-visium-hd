# Contributions

## Group project

The original study was completed by Sarah Verschuere, Chaeyoung Kim, Hyojun Bae, and Dries Huybens.

According to the paper's Author Contribution section, Chaeyoung Kim:

- benchmarked RCTD and cell2location on the standard Visium dataset;
- visualized and qualitatively compared those results with ground truth, together with Dries Huybens;
- co-developed the tissue-splitting procedure with Sarah Verschuere;
- independently applied and visualized RCTD and cell2location on split Visium;
- ran RCTD on Visium HD;
- performed data-sparsity analyses and summary visualizations.

Sarah Verschuere implemented the tissue-splitting strategy on Visium and Visium HD, generated reusable SpatialData objects, and produced dominant-cell-type maps and other interpretation plots.

Dries Huybens benchmarked RCTD and cell2location on Visium with Chaeyoung Kim, ran cell2location on Visium HD, performed JSD comparisons, and contributed visualizations.

Hyojun Bae performed NNLS estimation across Visium, split Visium, and Visium HD, compared method outputs with the benchmark, generated JSD visualizations, and derived ground-truth proportions from snRNA-seq samples.

## Portfolio reconstruction

The cleaned repository layout, explicit provenance notes, validation checks, and comparison interface are a reconstruction of the original analysis materials for clarity and reproducibility. They do not erase or replace the contribution record above.
