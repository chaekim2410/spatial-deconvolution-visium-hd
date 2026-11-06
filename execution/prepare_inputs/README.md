# Data preparation helpers

- `prepare_visium.py` loads a public standard-Visium Space Ranger directory or `.h5ad`, matches it to the annotation table, adds basic QC columns, and saves a prepared `.h5ad`.
- `convert_h5ad_to_rds.R` converts a prepared AnnData `.h5ad` object to a Seurat `.rds` object for R-based methods.

These are preparation helpers, not a data download script. Download locations for public source data are documented in `data/README.md`; the HD source data are not included.
