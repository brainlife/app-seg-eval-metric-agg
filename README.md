<h1 align="center">Segmentation evaluation metric aggregation</h1>

<p align="center">
  Per-metric means, population standard deviations and counts from one batch of segmentation evaluation metrics, written as a single <code>aggregate.json</code>.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.990"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.990-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="MIT license"></a>
</p>

## 🧠 At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

**Aggregates a batch of CONNECTS segmentation evaluation metrics into per-metric means and population standard deviations, written as aggregate.json.**

Averages every numeric metric in the raw and target_informed_neighbor_corrected groups across all input metrics files with equal weight per image, reports population standard deviation (ddof=0) and the count n per metric, and excludes missing values. Use it on one complete batch of seg-eval-metrics datasets; other metric groups are not pooled.

Run it on brainlife.io: [https://doi.org/10.25663/brainlife.app.990](https://doi.org/10.25663/brainlife.app.990)

| Input | Datatype | Required | Description |
|---|---|---|---|
| `metrics` | `neuro/seg-eval-metrics` | yes | Segmentation evaluation metrics (metrics.json) for each image in the batch. |

| Output | Datatype | Description |
|---|---|---|
| `aggregate` | `neuro/seg-eval-metric-agg` | aggregate.json with per-metric mean, population standard deviation and n, plus team, batch and input dataset IDs. |

| Parameter | Type | Default | Description |
|---|---|---|---|
| `team` | string |  | Team name recorded in the aggregate output. |
| `batch_id` | string |  | Batch identifier recorded in the aggregate output. |
| `input_dataset_ids` | string | `[]` | JSON array of dataset IDs, one unique ID per metrics file, in the same order. |

<!-- brainlife-app:end -->

## 🚀 Running the App

### ☁️ On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.990](https://doi.org/10.25663/brainlife.app.990), select every `neuro/seg-eval-metrics` dataset of one complete batch as the (multi) `metrics` input, fill in `team`, `batch_id` and `input_dataset_ids`, and press **Execute**. The result is archived to your project as a `neuro/seg-eval-metric-agg` dataset (`aggregate/aggregate.json`).

How the metrics are pooled:

- Every numeric metric in the `raw` and `target_informed_neighbor_corrected` groups is averaged separately; each image has equal weight.
- The standard deviation is the population SD (`ddof=0`), so a single image has SD zero.
- Every metric reports its contributing count `n`; missing or null values are excluded, not replaced by zero.
- Other groups, such as topology and components, stay in the individual input metrics and are not pooled.

The input schema was checked against the public evaluation implementation in [gamorosino/app-seg-eval-metrics](https://github.com/gamorosino/app-seg-eval-metrics/blob/main/metrics.py).

### 💻 Locally

You need Python 3.8 or later; no third-party packages and no container are used.

1. Clone this repository.
2. Create `config.json` in the working directory (on brainlife.io the engine supplies the real staged paths and IDs):

   ```json
   {
       "metrics": ["../stage-a/a/metrics.json", "../stage-b/b/metrics.json"],
       "team": "ExampleTeam",
       "batch_id": "BATCH_ID",
       "input_dataset_ids": "[\"DATASET_A\",\"DATASET_B\"]"
   }
   ```

   `input_dataset_ids` is a JSON array (given as a string) with one unique dataset ID per metrics file, in the same order.

3. Run the App:

   ```bash
   ./main
   ```

   `main` runs `python3 aggregate.py`. The numeric and validation tests run with:

   ```bash
   python3 -m unittest discover -s . -p 'test_*.py'
   ```

### Registration on brainlife.io

`manifest.json` holds the App's inputs, outputs, configuration and GitHub identity; `datatype.json` describes the output datatype `neuro/seg-eval-metric-agg` (ID `6ada73fa1e6d29036a18edcc`). Keep the multi-input `metrics` (file ID `metrics`) and the output `aggregate` (file ID `aggregate`, filename `aggregate.json`) unchanged. Enable Python 3.8+ and this App on slurm24, and configure its App and datatype IDs and the pinned Git commit in Warehouse. Do not place user tokens or private reference mappings in this repository.

The worker archives the original output privately, validates its identities and arithmetic against private evaluations, and publishes a copy with public input IDs. It adds team, description and batch annotations to both aggregate datasets.

## 📦 Outputs

```text
aggregate/
└── aggregate.json   neuro/seg-eval-metric-agg
```

`aggregate.json` contains `schema_version`, `team`, `batch_id`, `input_dataset_ids`, `file_count`, `stddev` (`"population"`) and, for each of `raw` and `target_informed_neighbor_corrected`, an object per metric with `mean`, `std` and `n`.

## 🩺 Troubleshooting

- **`Provide one unique dataset ID for every metrics file.`**: `input_dataset_ids` must list exactly one unique ID per metrics file, in the same order.
- **`metrics must be an array of staged metrics.json paths.`**: the `metrics` entry must be a list of paths; provide the metrics input as a multi-input.
- **`Missing <group> metrics or Dice score.`**, **`Invalid <group>.<metric>.`** or **`Invalid <group> Dice score.`**: an input `metrics.json` lacks the `raw` or `target_informed_neighbor_corrected` group, has a non-numeric or non-finite value, or has a Dice score outside 0–1. Re-run the evaluation for that image.

## 📚 Citing

> [!TIP]
> If you use this App in your work, please cite the App, the software it builds on and brainlife.io (below). GitHub's **Cite this repository** button gives the App citation in APA and BibTeX.

- Segmentation evaluation metric aggregation. brainlife.io App. [doi:10.25663/brainlife.app.990](https://doi.org/10.25663/brainlife.app.990)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## 👥 Authors

- tjgrafft

## 💰 Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io is publicly funded, and acknowledging that support helps keep it running. This App was developed with support from Wellcome, the U.S. National Institutes of Health (including the BRAIN Initiative BRAIN CONNECTS program: The Axonal Projectome EXchange, U24NS140384, and the Center for Mesoscale Connectomics, UM1NS132207) and the U.S. National Science Foundation.</sub>

## ⚖️ License

[MIT](LICENSE).
