#!/usr/bin/env python3
"""Compare full-tissue and reassembled split deconvolution results."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def normalize_spot_id(value: str) -> str:
    value = str(value)
    return value[:-2] if value.endswith("_1") else value


def read_assignments(path: Path) -> pd.DataFrame:
    assignments = pd.read_csv(path)
    if "part" not in assignments:
        raise ValueError("Assignment table must contain a 'part' column")

    spot_column = "spot_id" if "spot_id" in assignments else assignments.columns[0]
    assignments = assignments[[spot_column, "part"]].rename(columns={spot_column: "spot_id"})
    assignments["spot_id"] = assignments["spot_id"].map(normalize_spot_id)
    assignments["part"] = assignments["part"].astype(int)
    if assignments["spot_id"].duplicated().any():
        raise ValueError("Assignment table contains duplicated spot identifiers")
    return assignments


def read_proportions(path: Path) -> pd.DataFrame:
    table = pd.read_csv(path, sep="\t")
    unnamed = [column for column in table if column.startswith("Unnamed:")]
    if unnamed:
        table = table.drop(columns=unnamed)
    if "spot_id" in table:
        table = table.set_index(table.pop("spot_id").map(normalize_spot_id))
    return table.apply(pd.to_numeric, errors="raise")


def attach_full_spot_ids(full: pd.DataFrame, assignments: pd.DataFrame) -> pd.DataFrame:
    if full.index.name == "spot_id":
        return full
    if len(full) != len(assignments):
        raise ValueError(
            f"Full result has {len(full)} rows but assignments contain {len(assignments)} spots"
        )
    full = full.copy()
    full.index = pd.Index(assignments["spot_id"], name="spot_id")
    return full


def load_split_results(
    pattern: str,
    assignments: pd.DataFrame,
    parts: list[int],
) -> pd.DataFrame:
    tables: list[pd.DataFrame] = []
    for part in parts:
        path = Path(pattern.format(part=part))
        table = read_proportions(path)
        expected_ids = assignments.loc[assignments["part"] == part, "spot_id"]
        if table.index.name != "spot_id":
            if len(table) != len(expected_ids):
                raise ValueError(
                    f"{path} has {len(table)} rows; part {part} has {len(expected_ids)} assigned spots"
                )
            table.index = pd.Index(expected_ids, name="spot_id")
        table["part"] = part
        tables.append(table)
    return pd.concat(tables, axis=0)


def compare(full: pd.DataFrame, split: pd.DataFrame, method: str) -> pd.DataFrame:
    parts = split.pop("part")
    missing_columns = set(full.columns).symmetric_difference(split.columns)
    if missing_columns:
        raise ValueError(f"Cell-type columns differ: {sorted(missing_columns)}")

    common_ids = full.index.intersection(split.index)
    full = full.loc[common_ids, split.columns]
    split = split.loc[common_ids]
    if len(common_ids) == 0:
        raise ValueError("No common spot identifiers were found")

    full_dominant = full.idxmax(axis=1)
    split_dominant = split.idxmax(axis=1)
    matches = full_dominant.eq(split_dominant)
    absolute_error = (full - split).abs()
    flattened_correlation = np.corrcoef(full.to_numpy().ravel(), split.to_numpy().ravel())[0, 1]

    return pd.DataFrame(
        [
            {
                "method": method,
                "parts": ",".join(map(str, sorted(parts.unique()))),
                "evaluated_spots": len(common_ids),
                "dominant_matches": int(matches.sum()),
                "dominant_mismatches": int((~matches).sum()),
                "dominant_agreement": float(matches.mean()),
                "mean_absolute_error": float(absolute_error.to_numpy().mean()),
                "median_absolute_error": float(np.median(absolute_error.to_numpy())),
                "flattened_pearson_correlation": float(flattened_correlation),
            }
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--method", required=True)
    parser.add_argument("--assignments", required=True, type=Path)
    parser.add_argument("--full", required=True, type=Path)
    parser.add_argument(
        "--split-pattern",
        required=True,
        help="Path pattern containing the literal placeholder {part}",
    )
    parser.add_argument("--parts", nargs="+", type=int, default=[0, 1, 2, 3])
    parser.add_argument("--output", required=True, type=Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    assignments = read_assignments(args.assignments)
    full = attach_full_spot_ids(read_proportions(args.full), assignments)
    split = load_split_results(args.split_pattern, assignments, args.parts)
    metrics = compare(full, split, args.method)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(args.output, index=False)
    print(metrics.to_string(index=False))


if __name__ == "__main__":
    main()
