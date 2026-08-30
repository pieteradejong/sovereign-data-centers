# Dutch Sovereign Data Center Capacity Model

Portable planning package.

## Files
- `dutch_sovereign_data_center_capacity_model.xlsx` — formula-driven primary model
- `assumptions.csv` — engineering/economic assumptions
- `workloads_inputs.csv` — workload demand inputs
- `region_allocation_inputs.csv` — regional allocation inputs

## Flow
Workloads → CPU/GPU/storage → servers → racks → IT MW → facility MW → sites → CAPEX/OPEX.

The CSV files can be consumed by Python, R, DuckDB, SQLite, Postgres, Google Sheets, LibreOffice, or future tooling.
