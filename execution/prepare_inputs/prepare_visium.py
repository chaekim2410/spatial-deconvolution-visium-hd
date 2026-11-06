#!/usr/bin/env python3
"""Prepare the standard Visium example for full and split deconvolution."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def normalize_spot_id(value: str) -> str:
    value = str(value)
    return value[:-2] if value.endswith("_1") else value


def load_visium(input_path: Path):
    """Load either an existing AnnData object or a Space Ranger directory."""
    import scanpy as sc

    if input_path.is_file() and input_path.suffix == ".h5ad":
        return sc.read_h5ad(input_path)
    if input_path.is_dir():
        return sc.read_visium(input_path)
    raise ValueError("--input must be a .h5ad file or Space Ranger Visium directory")


def prepare(
    input_path: Path,
    annotations_path: Path,
    output_path: Path,
    sample: str,
    sample_column: str,
    spot_column: str,
) -> None:
    adata = load_visium(input_path)
    annotations = pd.read_csv(annotations_path)
    required = {sample_column, spot_column}
    missing = required.difference(annotations.columns)
    if missing:
        raise ValueError(f"Annotation table is missing columns: {sorted(missing)}")

    annotations = annotations.loc[annotations[sample_column] == sample].copy()
    annotations["spot_id"] = annotations[spot_column].map(normalize_spot_id)
    annotation_ids = pd.Index(annotations["spot_id"])

    normalized_obs_names = pd.Index(map(normalize_spot_id, adata.obs_names))
    keep = normalized_obs_names.isin(annotation_ids)
    if not keep.any():
        raise ValueError(f"No spots for sample {sample!r} overlap the Visium object")
    adata = adata[keep].copy()
    adata.obs_names = normalized_obs_names[keep]

    annotation_frame = annotations.set_index("spot_id")
    shared_columns = [
        column
        for column in annotation_frame.columns
        if column not in adata.obs.columns and column not in {sample_column, spot_column}
    ]
    if shared_columns:
        adata.obs = adata.obs.join(annotation_frame[shared_columns], how="left")

    adata.obs["total_umi"] = adata.X.sum(axis=1).A1
    adata.obs["n_genes_by_counts"] = (adata.X > 0).sum(axis=1).A1
    adata.var["n_spots_by_counts"] = (adata.X > 0).sum(axis=0).A1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    adata.write_h5ad(output_path)
    adata.obs[["total_umi", "n_genes_by_counts"]].to_csv(
        output_path.with_suffix(".qc.csv"), index_label="spot_id"
    )
    print(f"Saved {adata.n_obs} spots and {adata.n_vars} genes to {output_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--annotations", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--sample", default="JBO1")
    parser.add_argument("--sample-column", default="sample")
    parser.add_argument("--spot-column", default="spot")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    prepare(
        args.input,
        args.annotations,
        args.output,
        args.sample,
        args.sample_column,
        args.spot_column,
    )


if __name__ == "__main__":
    main()
