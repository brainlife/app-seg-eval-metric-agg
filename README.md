# Segmentation evaluation metric aggregation

A Brainlife app that combines one complete batch of `neuro/seg-eval-metrics`
datasets into `neuro/seg-eval-metric-agg` (`aggregate/aggregate.json`). Requires
Python 3.8 or later; no third-party Python packages are needed.

The app averages every numeric metric in `raw` and
`target_informed_neighbor_corrected` separately. Each image has equal weight.
Standard deviation is population SD (`ddof=0`); a single image has SD zero. Every
metric includes its contributing count `n`; missing/null values are excluded,
not replaced by zero. Other groups such as topology and components remain in
individual input metrics and are not pooled into these two score groups.

Example `config.json` (the engine supplies real staged paths and IDs):

```json
{
  "metrics": ["../stage-a/a/metrics.json", "../stage-b/b/metrics.json"],
  "team": "ExampleTeam",
  "batch_id": "BATCH_ID",
  "input_dataset_ids": "[\"DATASET_A\",\"DATASET_B\"]"
}
```

`python3 aggregate.py` reads that config in the working directory and writes
`aggregate/aggregate.json`. `main` is the executable Brainlife entrypoint. Run
`python3 -m unittest discover -s . -p 'test_*.py'` for the numeric/validation tests.

The registered output datatype is `neuro/seg-eval-metric-agg`
(`6ada73fa1e6d29036a18edcc`). `manifest.json` contains that datatype ID and the
GitHub repository identity for Brainlife registration. Preserve input `metrics` (multi-input, file ID `metrics`)
and output `aggregate` (file ID `aggregate`, filename `aggregate.json`). Enable
Python 3.8+ and this app on slurm24; configure its app/datatype IDs and pinned Git
commit in Warehouse. Do not place user tokens or private reference mappings here.

The worker archives the original output privately, validates its identities and
arithmetic against private evaluations, and publishes a copy with public input
IDs. It adds team/description/batch annotations to both aggregate datasets.

Input schema was checked against the public evaluation implementation:
https://github.com/gamorosino/app-seg-eval-metrics/blob/main/metrics.py
