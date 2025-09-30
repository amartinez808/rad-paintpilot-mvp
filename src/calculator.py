from typing import Dict, List
from src.config import STANDARD_OPENINGS
from src.finish_systems import (
    calculate_paint_materials,
    calculate_wallcovering_materials,
)

def calculate_wall_area(room: Dict) -> float:
    """Gross wall area in sq ft: perimeter * height."""
    L = float(room['length'])
    W = float(room['width'])
    H = float(room['height'])
    perimeter = 2 * (L + W)
    gross_area = perimeter * H
    return max(0.0, gross_area)

def subtract_openings(gross_area: float, doors: int, windows: int) -> float:
    """Subtract typical door/window areas from gross wall area."""
    gross = max(0.0, float(gross_area))
    door_area = max(0, int(doors)) * STANDARD_OPENINGS['door']['area']
    window_area = max(0, int(windows)) * STANDARD_OPENINGS['window']['area']
    net_area = gross - door_area - window_area
    return max(0.0, net_area)

def calculate_materials(net_area: float, finish_type: str):
    """Dispatch to the appropriate system calc."""
    ft = (finish_type or '').lower()
    if ft == 'paint':
        return {'type': 'paint', **calculate_paint_materials(net_area)}
    if ft == 'wallcovering':
        return {'type': 'wallcovering', **calculate_wallcovering_materials(net_area)}
    # default
    return {'type': 'paint', **calculate_paint_materials(net_area)}

def process_takeoff(rooms_data: Dict) -> List[Dict]:
    """Main calculation engine across rooms."""
    results = []
    for room in rooms_data.get('rooms', []):
        gross = calculate_wall_area(room)
        net = subtract_openings(gross, room.get('doors', 0), room.get('windows', 0))
        materials = calculate_materials(net, room.get('finish_type', 'paint'))
        results.append({
            'room': room,
            'gross_area': round(gross, 2),
            'net_area': round(net, 2),
            'materials': materials,
        })
    return results
