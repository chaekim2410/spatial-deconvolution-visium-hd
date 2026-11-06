# Spatial splitting

`split_tissue_function.py` is the core project-specific function. Given a spatial AnnData object and spot-coordinate table, it divides the tissue into an `n × n` grid, writes one AnnData object per region, and records the spot-to-part mapping used to reassemble results.

`test_split_tissue_function.ipynb` is the original test/exploration notebook. For this study, `n = 2`, producing four spatially coherent partitions.
