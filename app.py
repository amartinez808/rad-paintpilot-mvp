import streamlit as st
import pandas as pd
from src.pdf_processor import mock_room_extraction
from src.calculator import process_takeoff
from src.excel_exporter import generate_workbook
from src.floor_visualizer import generate_floor_plan_svg

st.set_page_config(page_title="RAD PaintPilot MVP", page_icon="🎨")
st.title("🎨 RAD PaintPilot - Pro Plan Demo")

uploaded_file = st.file_uploader("Upload Floor Plan PDF", type=['pdf'])

if uploaded_file:
    with st.spinner("🤖 AI analyzing drawings..."):
        import time
        time.sleep(1.5)
        # Pass the file object - mock_room_extraction doesn't use it anyway
        rooms_data = mock_room_extraction(uploaded_file)
        results = process_takeoff(rooms_data)

    st.success("✅ Analysis complete!")
    
    # Debug: show rooms_data structure
    with st.expander("Debug: Room Data"):
        st.json(rooms_data)

    # --- Floor Plan Visualization ---
    st.subheader("📐 Floor Plan Preview")
    svg_markup = generate_floor_plan_svg(rooms_data)
    # Wrap in a responsive container to avoid clipping on smaller screens
    st.markdown(
        f"""
        <div style="max-width: 100%; overflow-x: auto; border-radius: 8px; padding: 12px; background: #ffffff; border: 1px solid #e0e0e0;">
          <div style="min-width: 1500px; margin: 0 auto;">
            {svg_markup}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Pastel blue = Paint • Pastel green = Wallcovering • Hover rooms for details")

    # --- Room Breakdown Table ---
    st.subheader("Room Breakdown")
    rows = []
    for r in results:
        room = r['room']
        m = r['materials']
        rows.append({
            "Room ID": room['id'],
            "Name": room['name'],
            "L": room['length'],
            "W": room['width'],
            "H": room['height'],
            "Doors": room['doors'],
            "Windows": room['windows'],
            "Finish": m['type'],
            "Gross Area": r['gross_area'],
            "Net Area": r['net_area'],
            "Primer (gal)": m.get('primer_gallons'),
            "Finish (gal)": m.get('finish_gallons'),
            "Total (gal)": m.get('total_gallons'),
            "Rolls": m.get('rolls'),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    # --- Export ---
    if st.button("📥 Generate Bid Package (Excel)"):
        import os
        os.makedirs("output", exist_ok=True)
        out_path = "output/bid.xlsx"
        generate_workbook(results, out_path)
        with open(out_path, "rb") as f:
            st.download_button("Download Excel", f, file_name="bid_package.xlsx")
