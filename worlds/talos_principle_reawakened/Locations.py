import typing

from BaseClasses import Location


class LocData(typing.NamedTuple):
    id: int
    region: str


class TalosPrincipleLocation(Location):
    game: str = "The Talos Principle Reawakened"


# Base location ID - must match client's BASE_LOCATION_ID (0x540000)
BASE_ID = 0x540000  # 5505024

# Region constants
REGION_WORLD_A1 = "World A1"
REGION_WORLD_A = "World A"
REGION_WORLD_B = "World B"
REGION_WORLD_C = "World C"

# ── All 89 tetromino locations, ordered to match Items.py ──────────────────

MAIN_LOCATIONS: typing.Dict[str, LocData] = {
    # World A1 (7) - always accessible
    "World A1 Green J 3":  LocData(BASE_ID + 0,  REGION_WORLD_A1),
    "World A1 Golden T":   LocData(BASE_ID + 1,  REGION_WORLD_A1),
    "World A1 Green Z":    LocData(BASE_ID + 2,  REGION_WORLD_A1),
    "World A1 Green J 2":  LocData(BASE_ID + 3,  REGION_WORLD_A1),
    "World A1 Green J 1":  LocData(BASE_ID + 4,  REGION_WORLD_A1),
    "World A1 Golden L":   LocData(BASE_ID + 5,  REGION_WORLD_A1),
    "World A1 Green I":    LocData(BASE_ID + 6,  REGION_WORLD_A1),
    # World A2-A7 (25) - behind A1 Gate
    "World A2 Golden L":   LocData(BASE_ID + 7,  REGION_WORLD_A),
    "World A2 Green L":    LocData(BASE_ID + 8,  REGION_WORLD_A),
    "World A2 Green Z":    LocData(BASE_ID + 9,  REGION_WORLD_A),
    "World A3 Golden T 1": LocData(BASE_ID + 10, REGION_WORLD_A),
    "World A3 Green Z":    LocData(BASE_ID + 11, REGION_WORLD_A),
    "World A3 Red L":      LocData(BASE_ID + 12, REGION_WORLD_A),
    "World A3 Golden T 2": LocData(BASE_ID + 13, REGION_WORLD_A),
    "World A4 Golden Z 1": LocData(BASE_ID + 14, REGION_WORLD_A),
    "World A4 Golden Z 2": LocData(BASE_ID + 15, REGION_WORLD_A),
    "World A4 Golden T 1": LocData(BASE_ID + 16, REGION_WORLD_A),
    "World A4 Golden T 2": LocData(BASE_ID + 17, REGION_WORLD_A),
    "World A5 Red Z":      LocData(BASE_ID + 18, REGION_WORLD_A),
    "World A5 Green I":    LocData(BASE_ID + 19, REGION_WORLD_A),
    "World A5 Green T 1":  LocData(BASE_ID + 20, REGION_WORLD_A),
    "World A5 Green T 2":  LocData(BASE_ID + 21, REGION_WORLD_A),
    "World A5 Green L":    LocData(BASE_ID + 22, REGION_WORLD_A),
    "World A6 Green Z":    LocData(BASE_ID + 23, REGION_WORLD_A),
    "World A6 Red L 1":    LocData(BASE_ID + 24, REGION_WORLD_A),
    "World A6 Red L 2":    LocData(BASE_ID + 25, REGION_WORLD_A),
    "World A6 Red Z":      LocData(BASE_ID + 26, REGION_WORLD_A),
    "World A7 Red L":      LocData(BASE_ID + 27, REGION_WORLD_A),
    "World A7 Green L":    LocData(BASE_ID + 28, REGION_WORLD_A),
    "World A7 Red T":      LocData(BASE_ID + 29, REGION_WORLD_A),
    "World A7 Red O":      LocData(BASE_ID + 30, REGION_WORLD_A),
    "World A7 Green T":    LocData(BASE_ID + 31, REGION_WORLD_A),
    # World B1-B7 (30) - behind B Gate
    "World B1 Golden L":   LocData(BASE_ID + 32, REGION_WORLD_B),
    "World B1 Golden Z":   LocData(BASE_ID + 33, REGION_WORLD_B),
    "World B1 Golden S":   LocData(BASE_ID + 34, REGION_WORLD_B),
    "World B1 Golden T 1": LocData(BASE_ID + 35, REGION_WORLD_B),
    "World B1 Golden T 2": LocData(BASE_ID + 36, REGION_WORLD_B),
    "World B2 Red L":      LocData(BASE_ID + 37, REGION_WORLD_B),
    "World B2 Golden S":   LocData(BASE_ID + 38, REGION_WORLD_B),
    "World B2 Golden T":   LocData(BASE_ID + 39, REGION_WORLD_B),
    "World B2 Golden Z":   LocData(BASE_ID + 40, REGION_WORLD_B),
    "World B3 Golden T":   LocData(BASE_ID + 41, REGION_WORLD_B),
    "World B3 Golden J":   LocData(BASE_ID + 42, REGION_WORLD_B),
    "World B3 Red T":      LocData(BASE_ID + 43, REGION_WORLD_B),
    "World B3 Red L":      LocData(BASE_ID + 44, REGION_WORLD_B),
    "World B4 Red T 1":    LocData(BASE_ID + 45, REGION_WORLD_B),
    "World B4 Red T 2":    LocData(BASE_ID + 46, REGION_WORLD_B),
    "World B4 Green T":    LocData(BASE_ID + 47, REGION_WORLD_B),
    "World B4 Green J":    LocData(BASE_ID + 48, REGION_WORLD_B),
    "World B4 Red L 1":    LocData(BASE_ID + 49, REGION_WORLD_B),
    "World B4 Red L 2":    LocData(BASE_ID + 50, REGION_WORLD_B),
    "World B5 Red I":      LocData(BASE_ID + 51, REGION_WORLD_B),
    "World B5 Red L":      LocData(BASE_ID + 52, REGION_WORLD_B),
    "World B5 Red S":      LocData(BASE_ID + 53, REGION_WORLD_B),
    "World B5 Green J":    LocData(BASE_ID + 54, REGION_WORLD_B),
    "World B5 Red Z":      LocData(BASE_ID + 55, REGION_WORLD_B),
    "World B6 Red I":      LocData(BASE_ID + 56, REGION_WORLD_B),
    "World B6 Golden T":   LocData(BASE_ID + 57, REGION_WORLD_B),
    "World B6 Golden L":   LocData(BASE_ID + 58, REGION_WORLD_B),
    "World B7 Red J":      LocData(BASE_ID + 59, REGION_WORLD_B),
    "World B7 Red I":      LocData(BASE_ID + 60, REGION_WORLD_B),
    "World B7 Golden O":   LocData(BASE_ID + 61, REGION_WORLD_B),
    "World B7 Golden I":   LocData(BASE_ID + 62, REGION_WORLD_B),
    # World C1-C7 (27) - behind C Gate
    "World C1 Red Z":      LocData(BASE_ID + 63, REGION_WORLD_C),
    "World C1 Red J":      LocData(BASE_ID + 64, REGION_WORLD_C),
    "World C1 Red I":      LocData(BASE_ID + 65, REGION_WORLD_C),
    "World C1 Red T":      LocData(BASE_ID + 66, REGION_WORLD_C),
    "World C2 Red Z":      LocData(BASE_ID + 67, REGION_WORLD_C),
    "World C2 Red O":      LocData(BASE_ID + 68, REGION_WORLD_C),
    "World C2 Red T":      LocData(BASE_ID + 69, REGION_WORLD_C),
    "World C2 Red S":      LocData(BASE_ID + 70, REGION_WORLD_C),
    "World C3 Red J":      LocData(BASE_ID + 71, REGION_WORLD_C),
    "World C3 Red O":      LocData(BASE_ID + 72, REGION_WORLD_C),
    "World C3 Red Z":      LocData(BASE_ID + 73, REGION_WORLD_C),
    "World C3 Red T":      LocData(BASE_ID + 74, REGION_WORLD_C),
    "World C4 Red T 1":    LocData(BASE_ID + 75, REGION_WORLD_C),
    "World C4 Red I":      LocData(BASE_ID + 76, REGION_WORLD_C),
    "World C4 Red S":      LocData(BASE_ID + 77, REGION_WORLD_C),
    "World C4 Red T 2":    LocData(BASE_ID + 78, REGION_WORLD_C),
    "World C5 Red I":      LocData(BASE_ID + 79, REGION_WORLD_C),
    "World C5 Red O 1":    LocData(BASE_ID + 80, REGION_WORLD_C),
    "World C5 Red O 2":    LocData(BASE_ID + 81, REGION_WORLD_C),
    "World C5 Red T":      LocData(BASE_ID + 82, REGION_WORLD_C),
    "World C6 Red S":      LocData(BASE_ID + 83, REGION_WORLD_C),
    "World C6 Red J":      LocData(BASE_ID + 84, REGION_WORLD_C),
    "World C6 Red O":      LocData(BASE_ID + 85, REGION_WORLD_C),
    "World C7 Red T 1":    LocData(BASE_ID + 86, REGION_WORLD_C),
    "World C7 Red O":      LocData(BASE_ID + 87, REGION_WORLD_C),
    "World C7 Red T 2":    LocData(BASE_ID + 88, REGION_WORLD_C),
    "World C7 Red L":      LocData(BASE_ID + 89, REGION_WORLD_C),
}

# Location name → ID mapping
location_name_to_id: typing.Dict[str, int] = {
    name: data.id for name, data in MAIN_LOCATIONS.items()
}
