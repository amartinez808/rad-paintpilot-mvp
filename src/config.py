# Defaults and finish system parameters for calculations

DEFAULT_WALL_HEIGHTS = {
    "standard": 8,
    "tall": 9,
    "high": 10,
}

# Typical opening sizes and areas (ft)
STANDARD_OPENINGS = {
    "door": {"width": 3, "height": 7, "area": 21},
    "window": {"width": 3, "height": 4, "area": 12},
}

# Coverage assumptions
# paint coverage in sq ft per gallon, wallcovering in sq ft per roll
FINISH_SYSTEMS = {
    "paint": {
        "primer": {"coats": 1, "coverage": 400},
        "finish": {"coats": 2, "coverage": 400},
    },
    "wallcovering": {"coverage": 30},  # sq ft per roll
}
