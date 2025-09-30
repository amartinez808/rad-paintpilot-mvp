from typing import Dict, List, Tuple

# === Visual design ===
ROOM_FILL_PAINT = "#cfe8ff"      # pastel blue
ROOM_FILL_WC   = "#d2f2d0"       # pastel green
ROOM_STROKE    = "#666666"
TEXT_COLOR     = "#222222"
WALL_STROKE    = "#111111"

# Canvas
SVG_W, SVG_H = 2000, 1100
MARGIN = 28

# Reserved bands so title/legend never collide with rooms
TITLE_BAND_PX   = 36                 # space along top for title
LEGEND_PANEL_PX = 260                # reserved panel on right for legend

# Layout behavior
GAP_PX       = 20                    # fixed pixel gap between rooms
ROW_WRAP_FT  = 150.0                 # wrap when row would exceed this width (in feet)
SCALE_MIN    = 3.2                   # keep labels readable
ROOM_MIN_WPX = 150                   # never render smaller than this
ROOM_MIN_HPX = 110

LABEL_MAIN_SIZE = 14
LABEL_SUB_SIZE  = 12

def _room_color(finish_type: str) -> str:
    return ROOM_FILL_WC if (finish_type or "").lower() == "wallcovering" else ROOM_FILL_PAINT

def _condense_label(text: str, max_chars: int) -> str:
    return text if len(text) <= max_chars else text[:max_chars-1] + "…"

def _computed_area(room: Dict) -> int:
    L = float(room["length"]); W = float(room["width"]); H = float(room["height"])
    doors = int(room.get("doors", 0)); windows = int(room.get("windows", 0))
    area = 2*(L+W)*H - (doors*21 + windows*12)
    return max(0, int(round(area)))

def _flow_layout(rooms: List[Dict]) -> Tuple[List[Dict], float, float]:
    """
    Place rooms into rows in "feet" units (width=length, height=width).
    Return placed rooms (with _x,_y,_rw,_rh) and total extents (ft).
    """
    placed = []
    x_ft = 0.0
    y_ft = 0.0
    row_h_ft = 0.0
    max_w_ft = 0.0

    for r in rooms:
        rw = float(r["length"])
        rh = float(r["width"])
        # wrap row if needed
        if x_ft > 0 and (x_ft + rw) > ROW_WRAP_FT:
            max_w_ft = max(max_w_ft, x_ft)
            x_ft = 0.0
            y_ft += row_h_ft  # next row directly below (pixel gaps handled at draw time)
            row_h_ft = 0.0

        placed.append({**r, "_x": x_ft, "_y": y_ft, "_rw": rw, "_rh": rh})
        x_ft += rw
        row_h_ft = max(row_h_ft, rh)

    max_w_ft = max(max_w_ft, x_ft)
    total_h_ft = y_ft + row_h_ft
    return placed, max_w_ft, total_h_ft

def _compute_scale(width_ft: float, height_ft: float) -> float:
    draw_w_px = SVG_W - 2*MARGIN - LEGEND_PANEL_PX
    draw_h_px = SVG_H - 2*MARGIN - TITLE_BAND_PX
    if width_ft <= 0 or height_ft <= 0:
        return SCALE_MIN
    sx = draw_w_px / width_ft
    sy = draw_h_px / height_ft
    return max(min(sx, sy), SCALE_MIN)

def _svg_rect(x, y, w, h, fill, stroke, stroke_w=1, rx=3):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>')

def _svg_text(cx, cy, text, size=12, weight="500", anchor="middle"):
    return (f'<text x="{cx:.1f}" y="{cy:.1f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{TEXT_COLOR}" text-anchor="{anchor}" '
            f'font-family="Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif">{text}</text>')

def _svg_title(text: str) -> str:
    return f'<title>{text}</title>'

def _legend() -> str:
    x0 = SVG_W - LEGEND_PANEL_PX + 10
    y0 = MARGIN + 10
    parts = []
    # panel
    parts.append(_svg_rect(x0-10, y0-10, LEGEND_PANEL_PX-20, 80, "#ffffff", "#cccccc", 1, rx=6))
    parts.append(_svg_text(x0, y0, "Legend", 13, "600", "start"))
    # items
    items = [("Paint", ROOM_FILL_PAINT), ("Wallcovering", ROOM_FILL_WC)]
    yy = y0 + 18
    for label, color in items:
        parts.append(_svg_rect(x0, yy, 22, 14, color, ROOM_STROKE, 1, rx=2))
        parts.append(_svg_text(x0 + 32, yy + 11.5, label, 12, "500", "start"))
        yy += 22
    return "\n".join(parts)

def generate_floor_plan_svg(rooms_data: Dict) -> str:
    """
    Generate an SVG floor plan from rooms_data['rooms'].
    Each room should include: id, name, length, width, height, doors, windows, finish_type.
    """
    rooms = list(rooms_data.get("rooms", []))
    if not rooms:
        return '<div style="color:#a00;">No rooms available for visualization.</div>'

    # Stable ordering: by id, then name
    rooms.sort(key=lambda r: (str(r.get("id","")), str(r.get("name",""))))

    placed, w_ft, h_ft = _flow_layout(rooms)
    scale = _compute_scale(w_ft, h_ft)

    # Drawing origin for the layout area (top-left inside border/title)
    origin_x = MARGIN
    origin_y = MARGIN + TITLE_BAND_PX

    svg = [
        f'<svg width="{SVG_W}" height="{SVG_H}" viewBox="0 0 {SVG_W} {SVG_H}" '
        f'style="width:{SVG_W}px; height:auto; max-width:100%;" '
        f'preserveAspectRatio="xMidYMid meet" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Floor plan preview">'
    ]

    # Outer frame
    svg.append(_svg_rect(MARGIN/2, MARGIN/2, SVG_W - MARGIN, SVG_H - MARGIN, "#ffffff", WALL_STROKE, 2, rx=8))

    # Title
    title = f'{rooms_data.get("project","Project")} - {rooms_data.get("floor","")}'.strip(" -")
    svg.append(_svg_text(origin_x + 4, MARGIN + 14, title or "Floor Plan Preview", 16, "700", "start"))

    # Rooms
    for r in placed:
        x = origin_x + r["_x"] * scale
        y = origin_y + r["_y"] * scale
        w = max(ROOM_MIN_WPX, r["_rw"] * scale)
        h = max(ROOM_MIN_HPX, r["_rh"] * scale)

        # Apply pixel gap
        x += GAP_PX/2
        y += GAP_PX/2
        w -= GAP_PX
        h -= GAP_PX

        fill  = _room_color(r.get("finish_type"))
        area  = _computed_area(r)
        label_main = f'{r["id"]} • {area} sf'
        label_sub  = r["name"]

        # smartly shorten labels for small rooms
        if w < 130:
            label_main = _condense_label(label_main, 10)
            label_sub  = _condense_label(label_sub, 10)

        svg.append('<g>')
        svg.append(_svg_title(f'{r["name"]} | {label_main} | '
                              f'{r["length"]}x{r["width"]}x{r["height"]} ft | '
                              f'Doors:{r.get("doors",0)} Windows:{r.get("windows",0)}'))

        svg.append(_svg_rect(x, y, w, h, fill, ROOM_STROKE, 1))

        # Labels (centered)
        svg.append(_svg_text(x + w/2, y + h/2 - 4, label_main, LABEL_MAIN_SIZE, "600"))
        svg.append(_svg_text(x + w/2, y + h/2 + 12, label_sub, LABEL_SUB_SIZE, "400"))

        # Optional tiny markers along the top edge (only if width allows)
        if w >= 120:
            dx = x + 6
            for _ in range(min(6, int(r.get("doors", 0)))):
                svg.append(_svg_rect(dx, y + 2, 6, 2, "#222", "#222", 0.5, rx=1))
                dx += 10
            for _ in range(min(6, int(r.get("windows", 0)))):
                svg.append(_svg_rect(dx, y + 2, 6, 2, "#48a", "#48a", 0.5, rx=1))
                dx += 10

        svg.append('</g>')

    # Legend panel (in reserved right area)
    svg.append(_legend())

    svg.append('</svg>')
    return "\n".join(svg)
