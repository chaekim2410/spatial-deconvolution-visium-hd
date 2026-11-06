# Obtaining inputs for a new run

The deconvolution methods require two different biological inputs:

1. **SP (spatial):** the standard-Visium mouse liver count matrix plus spatial positions/images. In this study, the spatial benchmark sample is `GSM5764414`.
2. **SC/snRNA (method reference):** a single-nucleus liver expression object with cell-type annotations from GEO [GSE192740](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE192740), restricted to the nine retained cell types after upstream preprocessing.

They come from the same primary study—Guilliams et al., [“Spatial proteogenomics reveals distinct and evolutionarily conserved hepatic macrophage niches”](https://doi.org/10.1016/j.cell.2021.12.018), *Cell* (2022)—but they are not the same data: SP measures expression at tissue locations, whereas SC/snRNA measures isolated nuclei and supplies the cell-type reference.

The retained portfolio comparison specifically uses the `nuclei` reference with the `annot_cd45` nine-cell-type annotation. Separately, the digitized composition CSV retained in this repository is only an aggregate JSD comparison target; it must not be confused with the complete expression object supplied to each deconvolution method. The original group project also tested `noEC`, `inVivo`, and `exVivo` reference variants; these were sensitivity conditions, not the selected reference for the compact split comparison.

## Public standard-Visium and snRNA-seq sources

The public records are organized as two distinct GEO subseries under umbrella series [GSE192742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE192742):

- **Spatial Visium:** [GSE192741](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE192741), including sample `GSM5764414`.
- **Single-cell/single-nucleus reference source:** [GSE192740](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE192740).

The same study is also documented through the [Liver Cell Atlas download page](https://livercellatlas.org/download.php). Download and prepare the relevant spatial and nuclei objects outside this repository, then use:

- `execution/prepare_inputs/prepare_visium.py` to prepare a standard-Visium `.h5ad` or Space Ranger directory;
- `execution/prepare_inputs/convert_h5ad_to_rds.R` when an R/Seurat object is required by a method;
- the reference's cell-type annotation column used by the selected method.

The original [Spotless liver-reference preprocessing script](https://github.com/saeyslab/spotless-benchmark/blob/main/scripts/liver_analysis/1_preprocess_liver_ref.R) used the Liver Cell Atlas `mouseStSt_allcells` 10x count matrix, `mouseStSt_annot.csv`, and the refined CD45-negative annotation file `annot_mouseStStCD45neg.csv`. It created a Seurat object, assigned the refined `annot_cd45` labels, retained cell types represented by more than 50 cells in each of the three protocols, and saved separate reference objects by protocol. The selected project input was named `liver_mouseStSt_nuclei_9celltypes_annot_cd45.rds`. This preprocessing belonged to the upstream Spotless workflow; I used the resulting reference for deconvolution rather than generating the atlas reference myself.

The exact processed `.rds` reference object used in the original group run was not recovered, so this repository cannot recreate the group run byte-for-byte from a single download command. It documents the source study, samples, processing helpers, methods, and comparisons needed to repeat the workflow with newly obtained public inputs.

## Visium HD

The project’s HD source object is not available from a public download link in the recovered materials. It is therefore not possible to reproduce the exact HD run from this repository alone. The public repository retains the workflow code and non-reconstructive summaries only.
