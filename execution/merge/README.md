# Merge partition-level outputs

`merge_partition_results.ipynb` is the original notebook used to combine CSV outputs from the four spatial partitions after a method run. The merged table is then used by `analysis/summarize_visium_hd.py` for aggregate composition and spot-usage summaries.

This is an execution step, not exploratory analysis: it connects four independent split runs back into one tissue-level result table.
