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

# ── 24 optional Purple Sigil locations (enabled by randomise_purple_sigils) ─

PURPLE_SIGIL_LOCATIONS: typing.Dict[str, LocData] = {
    # World A  (internal IDs HL1-HL7)
    "World A2 Purple Sigil":    LocData(BASE_ID + 90,  REGION_WORLD_A),   # HL1
    "World A3 Purple Sigil 1":  LocData(BASE_ID + 91,  REGION_WORLD_A),   # HL2
    "World A3 Purple Sigil 2":  LocData(BASE_ID + 92,  REGION_WORLD_A),   # HL3
    "World A4 Purple Sigil":    LocData(BASE_ID + 93,  REGION_WORLD_A),   # HL4
    "World A5 Purple Sigil":    LocData(BASE_ID + 94,  REGION_WORLD_A),   # HL5
    "World A6 Purple Sigil":    LocData(BASE_ID + 95,  REGION_WORLD_A),   # HL6
    "World A7 Purple Sigil":    LocData(BASE_ID + 96,  REGION_WORLD_A),   # HL7
    # World B  (internal IDs HL8-HL17)
    "World B1 Purple Sigil 1":  LocData(BASE_ID + 97,  REGION_WORLD_B),   # HL8
    "World B1 Purple Sigil 2":  LocData(BASE_ID + 98,  REGION_WORLD_B),   # HL9
    "World B2 Purple Sigil":    LocData(BASE_ID + 99,  REGION_WORLD_B),   # HL10
    "World B3 Purple Sigil 1":  LocData(BASE_ID + 100, REGION_WORLD_B),   # HL11
    "World B3 Purple Sigil 2":  LocData(BASE_ID + 101, REGION_WORLD_B),   # HL12
    "World B4 Purple Sigil 1":  LocData(BASE_ID + 102, REGION_WORLD_B),   # HL13
    "World B4 Purple Sigil 2":  LocData(BASE_ID + 103, REGION_WORLD_B),   # HL14
    "World B5 Purple Sigil":    LocData(BASE_ID + 104, REGION_WORLD_B),   # HL15
    "World B6 Purple Sigil":    LocData(BASE_ID + 105, REGION_WORLD_B),   # HL16
    "World B7 Purple Sigil":    LocData(BASE_ID + 106, REGION_WORLD_B),   # HL17
    # World C  (internal IDs HL18-HL24)
    "World C1 Purple Sigil":    LocData(BASE_ID + 107, REGION_WORLD_C),   # HL18
    "World C2 Purple Sigil":    LocData(BASE_ID + 108, REGION_WORLD_C),   # HL19
    "World C3 Purple Sigil":    LocData(BASE_ID + 109, REGION_WORLD_C),   # HL20
    "World C4 Purple Sigil":    LocData(BASE_ID + 110, REGION_WORLD_C),   # HL21
    "World C5 Purple Sigil":    LocData(BASE_ID + 111, REGION_WORLD_C),   # HL22
    "World C6 Purple Sigil":    LocData(BASE_ID + 112, REGION_WORLD_C),   # HL23
    "World C7 Purple Sigil":    LocData(BASE_ID + 113, REGION_WORLD_C),   # HL24
}

# ── 30 optional Star locations (enabled by randomise_stars) ───────────────

STAR_LOCATIONS: typing.Dict[str, LocData] = {
    # World A1
    "World A1 Star":            LocData(BASE_ID + 114, REGION_WORLD_A1),  # SL5
    # World A
    "World A2 Star":            LocData(BASE_ID + 115, REGION_WORLD_A),   # SL2
    "World A3 Star 1":          LocData(BASE_ID + 116, REGION_WORLD_A),   # SZ3
    "World A3 Star 2":          LocData(BASE_ID + 117, REGION_WORLD_A),   # SL1
    "World A4 Star":            LocData(BASE_ID + 118, REGION_WORLD_A),   # SL4
    "World A5 Star 1":          LocData(BASE_ID + 119, REGION_WORLD_A),   # SL7
    "World A5 Star 2":          LocData(BASE_ID + 120, REGION_WORLD_A),   # SL6
    "World A6 Star":            LocData(BASE_ID + 121, REGION_WORLD_A),   # SZ8
    "World A7 Star":            LocData(BASE_ID + 122, REGION_WORLD_A),   # SL9
    # World B
    "World B1 Star":            LocData(BASE_ID + 123, REGION_WORLD_B),   # SL10
    "World B2 Star":            LocData(BASE_ID + 124, REGION_WORLD_B),   # SL11
    "World B3 Star":            LocData(BASE_ID + 125, REGION_WORLD_B),   # SL12
    "World B4 Star 1":          LocData(BASE_ID + 126, REGION_WORLD_B),   # SL13
    "World B4 Star 2":          LocData(BASE_ID + 127, REGION_WORLD_B),   # SZ24
    "World B5 Star":            LocData(BASE_ID + 128, REGION_WORLD_B),   # SZ14
    "World B7 Star 1":          LocData(BASE_ID + 129, REGION_WORLD_B),   # SZ15
    "World B7 Star 2":          LocData(BASE_ID + 130, REGION_WORLD_B),   # SL16
    # World C
    "World C1 Star":            LocData(BASE_ID + 131, REGION_WORLD_C),   # SL17
    "World C2 Star":            LocData(BASE_ID + 132, REGION_WORLD_C),   # SL18
    "World C3 Star":            LocData(BASE_ID + 133, REGION_WORLD_C),   # SL19
    "World C4 Star 1":          LocData(BASE_ID + 134, REGION_WORLD_C),   # SL20
    "World C4 Star 2":          LocData(BASE_ID + 135, REGION_WORLD_C),   # SL21
    "World C5 Star 1":          LocData(BASE_ID + 136, REGION_WORLD_C),   # SL22
    "World C5 Star 2":          LocData(BASE_ID + 137, REGION_WORLD_C),   # SL23
    "World C5 Star 3":          LocData(BASE_ID + 138, REGION_WORLD_C),   # SL27
    "World C6 Star":            LocData(BASE_ID + 139, REGION_WORLD_C),   # SL29
    "World C7 Star":            LocData(BASE_ID + 140, REGION_WORLD_C),   # SL30
    # Special locations
    "Messenger Island Star":    LocData(BASE_ID + 141, REGION_WORLD_C),   # SZ26
    "Tower Star":               LocData(BASE_ID + 142, REGION_WORLD_C),   # SL25
    "World Hub Star":           LocData(BASE_ID + 143, REGION_WORLD_C),   # SL28
}

# ── 9 optional Bonus Puzzle locations (enabled by randomise_bonus_puzzles) ──

BONUS_PUZZLE_LOCATIONS: typing.Dict[str, LocData] = {
    # World A Bonus Levels
    "World A Bonus ES1":  LocData(BASE_ID + 144, REGION_WORLD_A),   # White S
    "World A Bonus ES3":  LocData(BASE_ID + 145, REGION_WORLD_A),   # White S
    "World A Bonus EL1":  LocData(BASE_ID + 146, REGION_WORLD_A),   # White L
    # World B Bonus Levels
    "World B Bonus ES2":  LocData(BASE_ID + 147, REGION_WORLD_B),   # White S
    "World B Bonus EL2":  LocData(BASE_ID + 148, REGION_WORLD_B),   # White L
    "World B Bonus EL3":  LocData(BASE_ID + 149, REGION_WORLD_B),   # White L
    # World C Bonus Levels
    "World C Bonus ES4":  LocData(BASE_ID + 150, REGION_WORLD_C),   # White S
    "World C Bonus EL4":  LocData(BASE_ID + 151, REGION_WORLD_C),   # White L
    "World C Bonus EO1":  LocData(BASE_ID + 152, REGION_WORLD_C),   # White O
}

# Location name → ID mapping (includes all possible locations)
location_name_to_id: typing.Dict[str, int] = {
    **{name: data.id for name, data in MAIN_LOCATIONS.items()},
    **{name: data.id for name, data in PURPLE_SIGIL_LOCATIONS.items()},
    **{name: data.id for name, data in STAR_LOCATIONS.items()},
    **{name: data.id for name, data in BONUS_PUZZLE_LOCATIONS.items()},
}

# ── Item groups for hinting ────────────────────────────────────────────────

location_groups = {
    "World A Greens": {tet for tet in MAIN_LOCATIONS if "World A" in tet and "Green" in tet},
    "World A Goldens": {tet for tet in MAIN_LOCATIONS if "World A" in tet and "Golden" in tet},
    "World A Reds": {tet for tet in MAIN_LOCATIONS if "World A" in tet and "Red" in tet},
    "World A Purples": {tet for tet in PURPLE_SIGIL_LOCATIONS if "World A" in tet and "Purple" in tet},
    "World A Stars": {tet for tet in STAR_LOCATIONS if tet == "Messenger Island Star" or ("World A" in tet and "Star" in tet)},
    "World A Bonuses": {tet for tet in BONUS_PUZZLE_LOCATIONS if "World A" in tet and "Bonus" in tet},

    "World B Greens": {tet for tet in MAIN_LOCATIONS if "World B" in tet and "Green" in tet},
    "World B Goldens": {tet for tet in MAIN_LOCATIONS if "World B" in tet and "Golden" in tet},
    "World B Reds": {tet for tet in MAIN_LOCATIONS if "World B" in tet and "Red" in tet},
    "World B Purples": {tet for tet in PURPLE_SIGIL_LOCATIONS if "World B" in tet and "Purple" in tet},
    "World B Stars": {tet for tet in STAR_LOCATIONS if "World B" in tet and "Star" in tet},
    "World B Bonuses": {tet for tet in BONUS_PUZZLE_LOCATIONS if "World B" in tet and "Bonus" in tet},

    "World C Reds": {tet for tet in MAIN_LOCATIONS if "World C" in tet and "Red" in tet},
    "World C Purples": {tet for tet in PURPLE_SIGIL_LOCATIONS if "World C" in tet and "Purple" in tet},
    "World C Stars": {tet for tet in STAR_LOCATIONS if "World C" in tet and "Star" in tet},
    "World C Bonuses": {tet for tet in BONUS_PUZZLE_LOCATIONS if "World C" in tet and "Bonus" in tet},

    "Hub Stars": {"Tower Star", "World Hub Star"},
}
