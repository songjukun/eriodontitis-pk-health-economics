# Periodontitis PK health economics

Reproducible code for the mechanism-anchored proof-of-concept framework linking local periodontal pharmacokinetics, clinical pocket-closure scenarios, Markov health-economic modelling, probabilistic sensitivity analysis, and value-of-information analysis.

Public repository: <https://github.com/songjukun/eriodontitis-pk-health-economics>

Versioned manuscript snapshot: [v1.0.0](https://github.com/songjukun/eriodontitis-pk-health-economics/tree/v1.0.0)

## Scientific scope

This is a proof-of-concept simulation, not a decision-grade economic evaluation. Economic inputs and the PPD-to-pocket-closure mapping include explicitly labelled structural or illustrative assumptions. No individual patient data are included. Independent PK/GCF validation was not possible because an appropriate external patient-level dataset was unavailable.

The code keeps two decision lenses separate:

1. A homogeneous representative treated-site reference case, used for main Table 2 and its PSA ICER ranges.
2. A subgroup-prevalence-weighted target-population analysis, used for probability-optimal, EVPI, EVPPI, and EVIC results.

The Table 2 ICER range is defined as the 2.5th to 97.5th percentiles among PSA draws with positive incremental QALYs. The probability of non-positive incremental QALYs is reported separately in `reference_case_PSA_ICER_ranges.csv`.

## Repository contents

- `periodontal_miniPBPK_CEA.py`: canonical executable analysis.
- `periodontal_miniPBPK_CEA.ipynb`: notebook generated from the canonical Python source.
- `requirements.txt`: pinned Python dependencies used for the revision.
- `validate_outputs.py`: checks the reviewer-facing ICER ranges and output contract.
- `make_notebook.py`: regenerates the notebook from the canonical Python source.
- `reference_results/`: compact verified outputs from the final run.

## Reproduce the analysis

Python 3.12.x is recommended. The verified reference run used Python 3.12.14 with the package versions pinned in `requirements.txt`.

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python periodontal_miniPBPK_CEA.py
python validate_outputs.py
```

The analysis uses NumPy `default_rng` with a global seed of 2024 and 5,000 PSA draws. A complete run writes figures, CSV tables, a Word table file, and `analysis_summary.json` under `reviewer_revision_results/`.

To regenerate the notebook after editing the canonical Python file:

```bash
python make_notebook.py
```

## Verified reviewer-facing PSA ICER results

| Strategy versus SRP | ICER 2.5th to 97.5th percentiles, US$/QALY | P(incremental QALY <= 0) |
|---|---:|---:|
| SRP plus Atridox | 1,973 to 35,076 | 0.019 |
| SRP plus PerioChip | 2,022 to 10,789 | 0.000 |
| SRP plus Arestin | 3,482 to 14,443 | 0.000 |

These ICER percentiles are conditional on positive incremental QALYs and are not conventional confidence intervals for a ratio estimator.

## License

No software license has been assigned. The code is publicly accessible for reproducibility and peer review, but reuse permissions are not granted beyond rights provided by applicable law until the authors add a license.
