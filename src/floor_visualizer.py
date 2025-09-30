from typing import Dict, List, Tuple

# --- Visual design ---
ROOM_FILL_PAINT = "#cfe8ff"        # pastel blue
ROOM_FILL_WC = "#d2f2d0"           # pastel green
ROOM_STROKE = "#666666"            # gray outline
TEXT_COLOR = "#222222"
WALL_STROKE = "#111111"

SVG_W, SVG_H = 1100, 720          # canvas in px
MARGIN = 20                        # outer margin
GAP = 14                           # gap between rooms (px, pre-scale)
TARGET_WRAP_FEET = 120.0           # rough wrap threshold in "feet" width before breaking to next row
SCALE_MIN = 2.0                    # min px per foot to keep labels legible
LABEL_PAD = 6

def _room_color(finish_type: str) -> str:
    if (finish_type or "").lower() == "wallcovering":
        return ROOM_FILL_WC
    return ROOM_FILL_PAINT

def _room_label(room: Dict) -> str:
    L = room["length"]; W = room["width"]; H = room["height"]
    area = 2*(L+W)*H - (room.get("doors",0)*21 + room.get("windows",0)*12)
    area = max(0, round(area))
    return f'{room["id"]} • {area} sf'

def _flow_layout(rooms: List[Dict]) -> Tuple[List[Dict], float, float]:
    """
    Layout rooms in rows (flow/word-wrap) using their real-world LxW as width/height.
    Returns: positioned rooms with x,y (in 'feet'), and total extents (width_feet, height_feet).
    """
    placed = []
    x = 0.0
    y = 0.0
    row_h = 0.0
    max_w = 0.0

    for r in rooms:
        rw = float(r["length"])
        rh = float(r["width"])  # treat plan height as room width
        # wrap if exceeds target row width
        if x > 0 and (x + rw) > TARGET_WRAP_FEET:
            # new row
            max_w = max(max_w, x)
            x = 0.0
            y += row_h + (GAP/2)  # half-gap in feet (we'll scale gaps later)
            row_h = 0.0

        placed.append({**r, "_x": x, "_y": y, "_rw": rw, "_rh": rh})
        x += rw + (GAP/2)
        row_h = max(row_h, rh)

    max_w = max(max_w, x)
    total_h = y + row_h
    return placed, max_w, total_h

def _compute_scale(width_feet: float, height_feet: float) -> float:
    w_avail = SVG_W - 2*MARGIN
    h_avail = SVG_H - 2*MARGIN
    # convert gaps (already baked into flow as half-gap per room) after scale
    sx = w_avail / max(1e-6, width_feet)
    sy = h_avail / max(1e-6, height_feet)
    s = min(sx, sy)
    return max(s, SCALE_MIN)  # ensure labels readable

def _svg_rect(x, y, w, h, fill, stroke, stroke_w=1):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>'

def _svg_text(cx, cy, text, size=12, weight="500", anchor="middle"):
    return (f'<text x="{cx:.1f}" y="{cy:.1f}" font-size="{size}" '
            f'font-weight="{weight}" fill="{TEXT_COLOR}" text-anchor="{anchor}" '
            f'font-family="Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif">{text}</text>')

def _svg_title(text: str) -> str:
    # For hover tooltip inside a room <g> element
    return f'<title>{text}</title>'

def _legend() -> str:
    items = [
        ('Paint', ROOM_FILL_PAINT),
        ('Wallcovering', ROOM_FILL_WC),
    ]
    x0, y0 = SVG_W - 260, MARGIN + 10
    parts = [f'<g transform="translate({x0},{y0})">', _svg_text(80, -6, "Legend", 13, "600", "start")]
    y = 10
    for label, color in items:
        parts.append(_svg_rect(0, y, 22, 14, color, ROOM_STROKE, 1))
        parts.append(_svg_text(32, y+11.5, label, 12, "500", "start"))
        y += 22
    parts.append('</g>')
    return "\n".join(parts)

def generate_floor_plan_svg(rooms_data: Dict) -> str:
    """
    Generate SVG markup for a simple 2D floor plan from rooms_data:
    rooms_data = { 'rooms': [ {id,name,length,width,height,doors,windows,finish_type}, ... ] }
    """
    rooms = list(rooms_data.get("rooms", []))
    if not rooms:
        return '<div style="color:#a00;">No rooms available for visualization.</div>'

    placed, w_feet, h_feet = _flow_layout(rooms)
    scale = _compute_scale(w_feet, h_feet)

    # Canvas & border
    svg = [f'<svg width="{SVG_W}" height="{SVG_H}" viewBox="0 0 {SVG_W} {SVG_H}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Floor plan preview">']

    # Outer wall/border
    svg.append(_svg_rect(MARGIN, MARGIN, SVG_W - 2*MARGIN, SVG_H - 2*MARGIN, "#ffffff", WALL_STROKE, 2))

    # Rooms
    for r in placed:
        x = MARGIN + r["_x"] * scale
        y = MARGIN + r["_y"] * scale
        w = max(1.0, r["_rw"] * scale)
        h = max(1.0, r["_rh"] * scale)
        fill = _room_color(r.get("finish_type"))
        label = _room_label(r)

        # group with <title> for hover tooltip
        svg.append('<g>')
        svg.append(_svg_title(f'{r["name"]} | {label} | {r["length"]}x{r["width"]}x{r["height"]} ft | '
                              f'Doors:{r.get("doors",0)} Windows:{r.get("windows",0)}'))
        svg.append(_svg_rect(x, y, w, h, fill, ROOM_STROKE, 1))

        # label (two lines: id+area, then name)
        svg.append(_svg_text(x + w/2, y + h/2 - 4, label, 12, "600"))
        svg.append(_svg_text(x + w/2, y + h/2 + 12, r["name"], 11, "400"))

        # tiny ticks indicating doors/windows along top edge (visual hint only)
        dx = x + 6
        for _ in range(min(6, int(r.get("doors", 0)))):
            svg.append(_svg_rect(dx, y - 2, 6, 2, "#222", "#222", 0.5))
            dx += 10
        for _ in range(min(6, int(r.get("windows", 0)))):
            svg.append(_svg_rect(dx, y - 2, 6, 2, "#48a", "#48a", 0.5))
            dx += 10

        svg.append('</g>')

    # Title
    title = f'{rooms_data.get("project","Project")} • {rooms_data.get("floor","")}'.strip()
    svg.append(_svg_text(MARGIN + 4, MARGIN - 6, title or "Floor Plan Preview", 13, "700", "start"))

    # Legend
    svg.append(_legend())

    svg.append('</svg>')
    return "\n".join(svg)
