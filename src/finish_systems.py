from src.config import FINISH_SYSTEMS

def calculate_paint_materials(area_sqft: float):
    """Calculate primer + paint gallons for given area."""
    area = max(0.0, float(area_sqft))
    primer_cov = FINISH_SYSTEMS['paint']['primer']['coverage']
    finish_cov = FINISH_SYSTEMS['paint']['finish']['coverage']
    finish_coats = FINISH_SYSTEMS['paint']['finish']['coats']

    primer_gallons = area / primer_cov
    finish_gallons = (area * finish_coats) / finish_cov

    return {
        'primer_gallons': round(primer_gallons, 2),
        'finish_gallons': round(finish_gallons, 2),
        'total_gallons': round(primer_gallons + finish_gallons, 2),
    }

def calculate_wallcovering_materials(area_sqft: float):
    """Calculate wallcovering rolls needed."""
    area = max(0.0, float(area_sqft))
    rolls = area / FINISH_SYSTEMS['wallcovering']['coverage']
    return {'rolls': round(rolls, 1)}
