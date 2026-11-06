#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(anndataR)
  library(Seurat)
})

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) {
  stop("Usage: Rscript execution/prepare_inputs/convert_h5ad_to_rds.R INPUT.h5ad OUTPUT.rds")
}

input_path <- normalizePath(args[[1]], mustWork = TRUE)
output_path <- args[[2]]

if (tolower(tools::file_ext(input_path)) != "h5ad") {
  stop("Input must be an .h5ad file")
}

output_parent <- dirname(output_path)
if (!dir.exists(output_parent)) {
  dir.create(output_parent, recursive = TRUE)
}

seurat_object <- read_h5ad(input_path, to = "Seurat")
saveRDS(seurat_object, file = output_path)
message("Saved Seurat object to ", normalizePath(output_path, mustWork = TRUE))
