"""Validate the final reviewer-facing output contract after a complete run."""

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "reviewer_revision_results"
TABLES = RESULTS / "tables"

required = [
    RESULTS / "analysis_summary.json",
    TABLES / "Table02_base_case_CEA.csv",
    TABLES / "reference_case_PSA_ICER_ranges.csv",
    TABLES / "Tables.docx",
]
missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
if missing:
    raise SystemExit("FAIL: missing outputs: " + ", ".join(missing))

ranges = pd.read_csv(TABLES / "reference_case_PSA_ICER_ranges.csv").set_index("Arm")
expected = {
    "SRP+Atridox": (1973, 35076, 0.019),
    "SRP+Periochip": (2022, 10789, 0.000),
    "SRP+Arestin": (3482, 14443, 0.000),
}
for arm, (lo, hi, p_nonpositive) in expected.items():
    observed_lo = float(ranges.loc[arm, "ICER 2.5th (positive dQALY draws)"])
    observed_hi = float(ranges.loc[arm, "ICER 97.5th (positive dQALY draws)"])
    observed_p = float(ranges.loc[arm, "P(dQALY <= 0)"])
    if abs(observed_lo - lo) > 1.0 or abs(observed_hi - hi) > 1.0:
        raise SystemExit(
            f"FAIL: {arm} ICER interval changed: {observed_lo:.3f}–{observed_hi:.3f}"
        )
    if abs(observed_p - p_nonpositive) > 0.0005:
        raise SystemExit(
            f"FAIL: {arm} P(dQALY <= 0) changed: {observed_p:.6f}"
        )

table2 = pd.read_csv(TABLES / "Table02_base_case_CEA.csv").set_index("Arm")
interval_column = "PSA ICER 2.5th–97.5th percentiles ($/QALY)*"
expected_display = {
    "SRP+Atridox": "1,973–35,076",
    "SRP+Periochip": "2,022–10,789",
    "SRP+Arestin": "3,482–14,443",
}
for arm, display in expected_display.items():
    if str(table2.loc[arm, interval_column]) != display:
        raise SystemExit(f"FAIL: Table 2 interval for {arm} is not {display}")

summary = json.loads((RESULTS / "analysis_summary.json").read_text(encoding="utf-8"))
if int(summary.get("psa_draws", 0)) != 5000:
    raise SystemExit("FAIL: analysis_summary.json does not report 5,000 PSA draws")
if len(summary.get("reference_case_psa_icer_ranges", [])) != 3:
    raise SystemExit("FAIL: reference-case ICER ranges are absent from analysis_summary.json")

print("PASS: final public-repository outputs reproduce the reviewer-facing ICER ranges.")
