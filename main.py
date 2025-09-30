import argparse
from src.pdf_processor import mock_room_extraction, extract_metadata
from src.calculator import process_takeoff
from src.excel_exporter import generate_workbook

def main():
    parser = argparse.ArgumentParser(description='RAD PaintPilot MVP')
    parser.add_argument('--input', required=True, help='Input PDF path')
    parser.add_argument('--output', default='output/bid_package.xlsx', help='Output Excel path')
    args = parser.parse_args()

    print("🎨 RAD PaintPilot - Processing...")
    print("📄 Analyzing floor plans...")
    meta = extract_metadata(args.input)
    rooms_data = mock_room_extraction(args.input)

    print("📐 Calculating quantities...")
    results = process_takeoff(rooms_data)

    print("📊 Generating bid package...")
    output_path = generate_workbook(results, args.output)

    print(f"✅ Complete! Saved to: {output_path}")
    print(f"📁 Project: {rooms_data.get('project')} | Floor: {rooms_data.get('floor')}")
    # Demo ROI callout
    saved_hours = 3.5
    rate = 55
    print(f"⏱️  Time saved (demo): ~{saved_hours} hours")
    print(f"💵 ROI (demo): ~${saved_hours * rate:.2f} (@ ${rate}/hr)")

if __name__ == "__main__":
    main()
