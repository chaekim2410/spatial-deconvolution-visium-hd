#!/usr/bin/env python3
"""Summarize gene and UMI counts for a Visium HD AnnData object."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import scanpy as sc


def values_from_anndata(adata) -> tuple[np.ndarray, np.ndarray]:
    if {"n_genes_by_counts", "total_counts"}.issubset(adata.obs.columns):
        return (
            adata.obs["n_genes_by_counts"].to_numpy(),
            adata.obs["total_counts"].to_numpy(),
        )

    matrix = adata.X
    total_counts = np.asarray(matrix.sum(axis=1)).ravel()
    detected_genes = np.asarray((matrix > 0).sum(axis=1)).ravel()
    return detected_genes, total_counts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--gene-threshold", type=int, default=500)
    parser.add_argument("--umi-threshold", type=int, default=500)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    adata = sc.read_h5ad(args.input)
    detected_genes, total_counts = values_from_anndata(adata)
    total_spots = len(adata)
    low_gene = int((detected_genes < args.gene_threshold).sum())
    low_umi = int((total_counts < args.umi_threshold).sum())
    summary = pd.DataFrame(
        [
            {
                "total_spots": total_spots,
                "gene_threshold": args.gene_threshold,
                "spots_below_gene_threshold": low_gene,
                "percent_below_gene_threshold": 100 * low_gene / total_spots,
                "umi_threshold": args.umi_threshold,
                "spots_below_umi_threshold": low_umi,
                "percent_below_umi_threshold": 100 * low_umi / total_spots,
            }
        ]
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output, index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
