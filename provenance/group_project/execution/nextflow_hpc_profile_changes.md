# Group-specific Nextflow HPC profile changes

This is a focused record of the substantive changes made to the upstream `nextflow.config` during the group project. It is historical provenance, not a complete or current Nextflow configuration.

## Executor

```diff
- executor = "slurm"
+ executor = "local"
```

The PBS scheduler allocated the node first, after which Nextflow launched tasks inside that allocation.

## Apptainer

```groovy
apptainer {
    enabled = true
    libraryDir = "$VSC_SCRATCH"
    pullTimeout = "60 min"
}
```

The earlier Singularity block was replaced with Apptainer settings suitable for the university environment.

## GPU process labels

```diff
- clusterOptions = "--gres=gpu:1 --mail-type FAIL --mail-user <upstream-email>"
+ clusterOptions = "--gres=gpu:1"
  containerOptions = "--nv"
```

## Project storage

The `workDir` and `params.rootdir` values were changed from upstream user-scoped variables to the Design Project group storage area under:

```text
/kyukon/data/gent/courses/2024/design_project_C003698/groups/group05/
```

For a portable replacement without retired institutional paths, see `execution/run_methods/run_split_deconvolution.pbs`.
