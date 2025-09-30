# RAD PaintPilot MVP

Lightweight, demo-ready estimator core for AC Wallcovering. Loads a plan PDF (mock), extracts hardcoded rooms for the demo, calculates wall areas, subtracts openings, estimates paint/wallcovering materials, and exports a formatted Excel bid package.

## Quick Start (macOS)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# CLI
python main.py --input data/sample_plans/office_2ndfloor.pdf --output output/bid_package.xlsx

# Streamlit UI (optional)
streamlit run app.py
```

Demo Flow

Upload PDF (any file works) → "AI analyzing drawings…" spinner

Room table appears (8 demo rooms)

Export → open output/bid_package.xlsx (formatted tabs)

ROI callout in console: Saved ~3.5 hours @ $55/hr ≈ $192.50
---
## Deploy to Streamlit Community Cloud
1. Push this repo to GitHub.
2. Go to streamlit.io → New app.
3. Select your repo (`rad-paintpilot-mvp`), branch (`main`), and file path (`app.py`).
4. Click **Deploy**. The app installs from `requirements.txt`.
5. Add secrets later via App → Settings → Secrets.
