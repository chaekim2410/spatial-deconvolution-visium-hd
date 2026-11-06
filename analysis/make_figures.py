#!/usr/bin/env python3
"""Generate the compact figure set used in the portfolio README."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from compare_full_vs_split import (
    attach_full_spot_ids,
    load_split_results,
    read_assignments,
    read_proportions,
)


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "results" / "figures"
COLORS = {0: "#4C78A8", 1: "#F58518", 2: "#54A24B", 3: "#E45756"}
CELL_TYPE_COLORS = {
    "Bcells": "#FF9D76",
    "CentralVeinEndothelialcells": "#4C78A8",
    "Cholangiocytes": "#F58518",
    "Hepatocytes": "#72B7B2",
    "Kupffercells": "#E45756",
    "LSECs": "#54A24B",
    "Mesothelialcells": "#FFB6C1",
    "PortalVeinEndothelialcells": "#8CD17D",
    "Tcells": "#B279A2",
}


def save_figure(figure: plt.Figure, name: str) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    # Keep README figures readable without making them dominate a GitHub page.
    figure.savefig(FIGURE_DIR / name, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(figure)


def plot_study_workflow() -> None:
    """Summarize the validation-first study design used in this project."""
    figure, axis = plt.subplots(figsize=(13.2, 4.3))
    axis.set_xlim(0, 13.2)
    axis.set_ylim(0, 4.3)
    axis.axis("off")

    boxes = [
        (0.25, 1.45, 2.0, 1.35, "Standard Visium\n1,293 spots", "#E8F1FA"),
        (2.75, 2.35, 2.0, 1.15, "Full tissue\nrun", "#F3F3F3"),
        (2.75, 0.65, 2.0, 1.15, "2 × 2 spatial\nsplit", "#F3F3F3"),
        (5.25, 1.45, 2.2, 1.35, "NNLS · RCTD\ncell2location", "#EAF5EC"),
        (7.95, 1.45, 2.0, 1.35, "Full vs split\nvalidation", "#FFF1DC"),
        (10.45, 2.35, 2.3, 1.15, "Visium HD\n115,975 spots", "#F2EAF8"),
        (10.45, 0.65, 2.3, 1.15, "2 × 2 split only\n+ 3 methods", "#F2EAF8"),
    ]
    for x, y, width, height, label, color in boxes:
        patch = plt.Rectangle(
            (x, y), width, height, facecolor=color, edgecolor="#667085", linewidth=1.2
        )
        axis.add_patch(patch)
        axis.text(x + width / 2, y + height / 2, label, ha="center", va="center", fontsize=11)

    arrows = [
        ((2.25, 2.12), (2.75, 2.92)),
        ((2.25, 2.12), (2.75, 1.22)),
        ((4.75, 2.92), (5.25, 2.12)),
        ((4.75, 1.22), (5.25, 2.12)),
        ((7.45, 2.12), (7.95, 2.12)),
        ((9.95, 2.12), (10.45, 2.92)),
        ((11.60, 2.35), (11.60, 1.80)),
    ]
    for start, end in arrows:
        axis.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops={"arrowstyle": "->", "color": "#667085", "lw": 1.5},
        )

    axis.text(
        11.60,
        0.20,
        "Compare aggregate compositions and JSD",
        ha="center",
        va="center",
        fontsize=10,
        color="#344054",
    )
    axis.set_title("Validation-first workflow for scalable spatial deconvolution", pad=12)
    save_figure(figure, "00_study_workflow.png")


def load_cell2location_part0() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    assignments = read_assignments(ROOT / "data/assignments/jbo1_spots_and_parts.csv")
    full = attach_full_spot_ids(
        read_proportions(ROOT / "data/proportions/cell2location/full.tsv"), assignments
    )
    split = load_split_results(
        str(ROOT / "data/proportions/cell2location/split/part_{part}.tsv"),
        assignments,
        [0],
    )
    split = split.drop(columns="part")
    full = full.loc[split.index, split.columns]
    return assignments, full, split


def plot_partition_map(assignments: pd.DataFrame) -> None:
    coordinates = pd.read_csv(
        ROOT / "data/coordinates/jbo1_tissue_positions.csv",
        header=None,
        names=["spot_id", "in_tissue", "array_row", "array_col", "pixel_y", "pixel_x"],
    )
    coordinates = coordinates.merge(assignments, on="spot_id", how="inner", validate="one_to_one")

    figure, axis = plt.subplots(figsize=(7.2, 5.4))
    for part, group in coordinates.groupby("part"):
        axis.scatter(
            group["pixel_x"],
            group["pixel_y"],
            s=11,
            alpha=0.9,
            color=COLORS[int(part)],
            label=f"Part {part} (n={len(group)})",
            linewidths=0,
        )
    axis.invert_yaxis()
    axis.set(title="Spatially coherent 2 x 2 partition", xlabel="Pixel x", ylabel="Pixel y")
    axis.legend(frameon=False, ncol=2)
    axis.spines[["top", "right"]].set_visible(False)
    save_figure(figure, "01_spatial_partitions.png")


def plot_cell2location_scatter(full: pd.DataFrame, split: pd.DataFrame) -> None:
    cell_types = ["Cholangiocytes", "Hepatocytes", "Tcells"]
    figure, axes = plt.subplots(1, 3, figsize=(12, 3.8))
    for axis, cell_type in zip(axes, cell_types):
        x = full[cell_type]
        y = split[cell_type]
        limit = max(float(x.max()), float(y.max())) * 1.05
        axis.scatter(x, y, s=16, alpha=0.58, color="#4C78A8", linewidths=0)
        axis.plot([0, limit], [0, limit], linestyle="--", color="#666666", linewidth=1)
        axis.set(
            xlim=(0, limit),
            ylim=(0, limit),
            title=cell_type,
            xlabel="Full tissue proportion",
            ylabel="Split part 0 proportion",
        )
        axis.spines[["top", "right"]].set_visible(False)
    figure.suptitle("cell2location: full tissue versus spatial split", fontsize=14)
    figure.tight_layout()
    save_figure(figure, "02_cell2location_full_vs_split.png")


def plot_cell2location_mismatches(
    assignments: pd.DataFrame, full: pd.DataFrame, split: pd.DataFrame
) -> None:
    coordinates = pd.read_csv(
        ROOT / "data/coordinates/jbo1_tissue_positions.csv",
        header=None,
        names=["spot_id", "in_tissue", "array_row", "array_col", "pixel_y", "pixel_x"],
    ).set_index("spot_id")
    matches = full.idxmax(axis=1).eq(split.idxmax(axis=1)).rename("match")
    evaluated = coordinates.loc[matches.index].join(matches)

    figure, axis = plt.subplots(figsize=(6.2, 5.0))
    background = coordinates.loc[assignments["spot_id"]]
    axis.scatter(background["pixel_x"], background["pixel_y"], s=8, color="#D9D9D9", linewidths=0)
    for label, color, display in [(True, "#4C78A8", "Match"), (False, "#E45756", "Mismatch")]:
        group = evaluated[evaluated["match"] == label]
        axis.scatter(
            group["pixel_x"],
            group["pixel_y"],
            s=18 if label else 30,
            color=color,
            label=f"{display} (n={len(group)})",
            linewidths=0,
        )
    axis.invert_yaxis()
    axis.set(
        title="Dominant cell type agreement in part 0",
        xlabel="Pixel x",
        ylabel="Pixel y",
    )
    axis.legend(frameon=False)
    axis.spines[["top", "right"]].set_visible(False)
    save_figure(figure, "03_cell2location_dominant_matches.png")


def plot_reported_agreement() -> None:
    summary = pd.read_csv(ROOT / "results/reported_summary.csv")
    summary = summary[summary["method"].isin(["NNLS", "RCTD", "cell2location"])].copy()
    summary["agreement_percent"] = summary["agreement"] * 100

    summary["mismatch_percent"] = 100 - summary["agreement_percent"]

    figure, axis = plt.subplots(figsize=(5.6, 3.2))
    matches = axis.barh(
        summary["method"], summary["agreement_percent"], color="#4C78A8", label="Match"
    )
    axis.barh(
        summary["method"],
        summary["mismatch_percent"],
        left=summary["agreement_percent"],
        color="#E45756",
        label="Mismatch",
    )
    axis.set(
        xlim=(0, 100),
        xlabel="Spots (%)",
        title="Dominant cell type was largely preserved after splitting",
    )
    labels = [
        f"{int(row.dominant_matches)}/{int(row.evaluated_spots)} "
        f"({row.agreement_percent:.1f}%)"
        for row in summary.itertuples()
    ]
    axis.bar_label(matches, labels=labels, label_type="center", color="white", fontsize=10)
    axis.invert_yaxis()
    axis.legend(frameon=False, ncol=2, loc="lower center", bbox_to_anchor=(0.5, -0.28))
    axis.spines[["top", "right"]].set_visible(False)
    axis.grid(axis="x", alpha=0.2)
    save_figure(figure, "04_reported_dominant_agreement.png")


def plot_visium_hd_digitized_reference_jsd() -> None:
    summary = pd.read_csv(ROOT / "results/visium_vs_hd_digitized_reference_jsd.csv")
    x = np.arange(len(summary))
    width = 0.34

    figure, axis = plt.subplots(figsize=(5.6, 3.4))
    visium = axis.bar(
        x - width / 2,
        summary["visium_jsd"],
        width,
        color="#4C78A8",
        label="Visium",
    )
    visium_hd = axis.bar(
        x + width / 2,
        summary["visium_hd_jsd"],
        width,
        color="#F58518",
        label="Visium HD",
    )
    axis.set(
        xticks=x,
        xticklabels=summary["method"],
        ylabel="Jensen-Shannon divergence",
        title="JSD to digitized snRNA-seq composition",
        ylim=(0, 0.70),
    )
    axis.bar_label(visium, fmt="%.3f", padding=3)
    axis.bar_label(visium_hd, fmt="%.3f", padding=3)
    axis.legend(frameon=False)
    axis.grid(axis="y", alpha=0.2)
    axis.spines[["top", "right"]].set_visible(False)
    save_figure(figure, "05_visium_vs_hd_digitized_reference_jsd.png")


def plot_visium_hd_composition() -> None:
    summary = pd.read_csv(ROOT / "results/derived_summaries/visium_hd_part_composition.csv")
    methods = ["NNLS", "RCTD", "cell2location"]
    cell_types = list(CELL_TYPE_COLORS)
    figure, axes = plt.subplots(1, 3, figsize=(13.2, 4.6), sharex=True, sharey=True)

    for axis, method in zip(axes, methods):
        subset = summary[summary["method"].eq(method)]
        table = subset.pivot(index="part", columns="cell_type", values="mean_proportion")
        table = table.reindex(index=[0, 1, 2, 3], columns=cell_types, fill_value=0)
        left = np.zeros(len(table))
        for cell_type in cell_types:
            values = table[cell_type].fillna(0).to_numpy()
            axis.barh(
                [f"Part {part}" for part in table.index],
                values,
                left=left,
                color=CELL_TYPE_COLORS[cell_type],
                label=cell_type,
            )
            left += values
        axis.set(title=method, xlim=(0, 1), xlabel="Mean proportion")
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(axis="x", alpha=0.15)

    handles, labels = axes[-1].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        frameon=False,
        ncol=3,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.17),
    )
    figure.suptitle("Visium HD: cell-type composition across spatial partitions", fontsize=14)
    figure.tight_layout()
    save_figure(figure, "06_visium_hd_partition_composition.png")


def main() -> None:
    plot_study_workflow()
    assignments, full, split = load_cell2location_part0()
    plot_partition_map(assignments)
    plot_cell2location_scatter(full, split)
    plot_cell2location_mismatches(assignments, full, split)
    plot_reported_agreement()
    plot_visium_hd_digitized_reference_jsd()
    plot_visium_hd_composition()
    print(f"Saved figures to {FIGURE_DIR}")


if __name__ == "__main__":
    main()
