# For the demo we keep extraction deterministic and fast.
# Swap with real parsing later (pdfplumber/PyPDF2/LLM extraction).

from typing import Dict, Any

def extract_metadata(pdf_path: str) -> Dict[str, Any]:
    """Extract basic metadata (mock for demo)."""
    return {
        "file": str(pdf_path),
        "pages": 12,   # mock
        "project": "AC Wallcovering Office – 2nd Floor",
    }

def mock_room_extraction(pdf_path) -> Dict[str, Any]:
    """Return hardcoded room data for demo reliability."""
    return {
        "project": "AC Wallcovering Office",
        "floor": "2nd Floor",
        "rooms": [
            {"id": "201", "name": "Conference A",     "length": 20, "width": 15, "height": 9,  "doors": 2, "windows": 3, "finish_type": "paint"},
            {"id": "202", "name": "Open Office",      "length": 35, "width": 22, "height": 9,  "doors": 2, "windows": 6, "finish_type": "paint"},
            {"id": "203", "name": "Private Office 1", "length": 12, "width": 10, "height": 9,  "doors": 1, "windows": 1, "finish_type": "paint"},
            {"id": "204", "name": "Private Office 2", "length": 12, "width": 10, "height": 9,  "doors": 1, "windows": 1, "finish_type": "paint"},
            {"id": "205", "name": "Break Room",       "length": 16, "width": 12, "height": 9,  "doors": 1, "windows": 2, "finish_type": "wallcovering"},
            {"id": "206", "name": "Reception",        "length": 18, "width": 14, "height": 10, "doors": 1, "windows": 3, "finish_type": "paint"},
            {"id": "207", "name": "Corridor",         "length": 50, "width": 6,  "height": 9,  "doors": 6, "windows": 0, "finish_type": "paint"},
            {"id": "208", "name": "Storage",          "length": 10, "width": 8,  "height": 9,  "doors": 1, "windows": 0, "finish_type": "paint"},
        ],
    }
