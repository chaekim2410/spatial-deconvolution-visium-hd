#!/usr/bin/env python3
"""Summarize partition-level Visium HD deconvolution outputs.

The unavailable spot-level matrices are read from the group's local project files. Only aggregate cell-type
compositions and method-level spot usage are written, so the compact outputs
can be shared without publishing the underlying Visium HD dataset.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


METHODS = ("NNLS", "RCTD", "cell2location")


def read_proportions(path: Path) -> pd.DataFrame:
    table = pd.read_csv(path, sep="\t")
    unnamed = [column for column in table if column.startswith("Unnamed:")]
    if unnamed:
        table = table.drop(columns=unnamed)
    table = table.apply(pd.to_numeric, errors="coerce").dropna(how="all")
    row_totals = table.sum(axis=1)
    table = table.loc[row_totals.gt(0)].div(row_totals[row_totals.gt(0)], axis=0)
    return table


def summarize(
    patterns: dict[str, str], parts: list[int]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    tables: dict[tuple[str, int], pd.DataFrame] = {}
    for method, pattern in patterns.items():
        for part in parts:
            path = Path(pattern.format(part=part))
            if not path.exists():
                raise FileNotFoundError(path)
            tables[(method, part)] = read_proportions(path)

    composition_rows: list[dict[str, object]] = []
    usage_rows: list[dict[str, object]] = []
    for part in parts:
        expected_spots = max(len(tables[(method, part)]) for method in METHODS)
        for method in METHODS:
            table = tables[(method, part)]
            usage_rows.append(
                {
                    "method": method,
                    "part": part,
                    "input_spots": expected_spots,
                    "used_spots": len(table),
                    "rejected_spots": expected_spots - len(table),
                }
            )
            for cell_type, value in table.mean(axis=0).items():
                composition_rows.append(
                    {
                        "method": method,
                        "part": part,
                        "cell_type": cell_type,
                        "mean_proportion": float(value),
                    }
                )

    return pd.DataFrame(composition_rows), pd.DataFrame(usage_rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--nnls-pattern", required=True, help="NNLS path containing {part}"
    )
    parser.add_argument(
        "--rctd-pattern", required=True, help="RCTD path containing {part}"
    )
    parser.add_argument(
        "--cell2location-pattern",
        required=True,
        help="cell2location path containing {part}",
    )
    parser.add_argument("--parts", nargs="+", type=int, default=[0, 1, 2, 3])
    parser.add_argument("--composition-output", required=True, type=Path)
    parser.add_argument("--usage-output", required=True, type=Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    composition, usage = summarize(
        {
            "NNLS": args.nnls_pattern,
            "RCTD": args.rctd_pattern,
            "cell2location": args.cell2location_pattern,
        },
        args.parts,
    )
    args.composition_output.parent.mkdir(parents=True, exist_ok=True)
    args.usage_output.parent.mkdir(parents=True, exist_ok=True)
    composition.to_csv(args.composition_output, index=False)
    usage.to_csv(args.usage_output, index=False)
    print(usage.to_string(index=False))


if __name__ == "__main__":
    main()
