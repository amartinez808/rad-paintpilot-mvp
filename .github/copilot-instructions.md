This repository is a small, demo-ready estimator core (RAD PaintPilot MVP).
The goal of this file is to give an AI coding agent the minimum, actionable knowledge
it needs to be productive: architecture, key files, data shapes, developer workflows,
and where to make changes safely.

1) Big-picture architecture
- CLI runner: `main.py` orchestrates the demo flow: extract metadata, extract rooms (mock), calculate quantities, and export Excel via `src/excel_exporter.py`.
- Streamlit UI: `app.py` reuses the same core functions (`src.pdf_processor`, `src.calculator`, `src.excel_exporter`) so keep changes backward-compatible.
- Core modules (under `src/`):
  - `src/pdf_processor.py` — deterministic/mock PDF metadata & room extraction used by the demo.
  - `src/calculator.py` — calculation engine: `process_takeoff(rooms_data)` returns a list of per-room results.
  - `src/finish_systems.py` — material math for paint and wallcovering.
  - `src/excel_exporter.py` — uses `openpyxl` to produce the bid package workbook and returns the saved path.
  - `src/config.py` — constant defaults (coverage, opening sizes, default heights).

2) Key developer workflows and commands (discoverable in `README.md`)
- Set up environment and install deps: use `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`.
- CLI: `python main.py --input data/sample_plans/office_2ndfloor.pdf --output output/bid_package.xlsx`.
- Streamlit UI: `streamlit run app.py` (reuses same logic as CLI).

3) Important data shapes and examples (use these exactly when calling core functions)
- rooms_data (returned from `mock_room_extraction`) — dict with keys: `project`, `floor`, `rooms`.
  - `rooms` is a list of room dicts: {"id": str, "name": str, "length": number, "width": number, "height": number, "doors": int, "windows": int, "finish_type": "paint"|"wallcovering"}
- calculator output (each item returned by `process_takeoff`) — dict:
  - `{'room': <room dict>, 'gross_area': float, 'net_area': float, 'materials': {...}}`
- materials shapes (examples from `src/finish_systems.py`):
  - paint: `{ 'type': 'paint', 'primer_gallons': float, 'finish_gallons': float, 'total_gallons': float }`
  - wallcovering: `{ 'type': 'wallcovering', 'rolls': float }`

4) Project-specific conventions and patterns
- Use pure, small helper functions (see `src/calculator.py`) — keep calculation logic deterministic and testable.
- Mocking is intentional: `src/pdf_processor.mock_room_extraction` returns hardcoded rooms for demo reliability. If adding real PDF parsing, keep the same `rooms_data` output shape so `process_takeoff` and `excel_exporter` continue to work.
- Excel export is authoritative: `src/excel_exporter.generate_workbook(results, output_path)` saves a workbook and returns the path. Other code relies on its side-effect (file on disk) and return value.

5) Integration points & external dependencies
- openpyxl — used for Excel generation in `src/excel_exporter.py`.
- pandas — used in `app.py` to render tables in Streamlit (not required by core logic).
- pdfplumber / PyPDF2 — listed in `requirements.txt` but not used for extraction in the demo (placeholder for future real parsing).

6) Where to make changes safely (guidance for code edits)
- To implement real PDF extraction: edit `src/pdf_processor.py`. Preserve the `extract_metadata(pdf_path)` and `mock_room_extraction` return shapes or add a new function and wire it into `main.py` and `app.py` behind a flag.
- To change calculation assumptions: update `src/config.py` constants (e.g. `FINISH_SYSTEMS`, `STANDARD_OPENINGS`) and keep `finish_systems` functions in sync.
- To alter Excel layout: edit `src/excel_exporter.py`. Follow existing style helpers (`_header`, sheet creation functions).

7) Small examples an agent might apply immediately
- Example: Add a new finish type "eco-paint" — add config constants to `src/config.py`, add calculation logic to `src/finish_systems.py` returning the same material keys as existing systems, and ensure `src/calculator.calculate_materials` dispatches to it.
- Example: Replace mock extraction with a new `extract_rooms_from_pdf(pdf_path)` — implement it in `src/pdf_processor.py` and update `main.py` to call the new function when `--real-extract` flag is present. Keep demo path untouched.

8) Tests & validation
- There are no tests in the repo. Before modifying public functions, run the demo CLI (`python main.py ...`) and the Streamlit UI to smoke test. Use the `output/` folder to inspect Excel outputs.

9) Notes for the AI agent
- Preserve the deterministic demo behavior unless explicitly asked to change it.
- Prefer minimal, focused edits that keep public function signatures stable (`process_takeoff`, `generate_workbook`, `mock_room_extraction` / `extract_metadata`).
- When adding new dependencies, update `requirements.txt` and mention why in the PR body.

If anything in this guide is unclear or you want more examples (unit-test templates, CI steps, or a short refactor to add a real PDF extractor), tell me which part to expand and I will update this document.
