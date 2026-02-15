import typing

from BaseClasses import Item, ItemClassification


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification


class TalosPrincipleItem(Item):
    game: str = "The Talos Principle"


# Base item ID - must match client's BASE_ITEM_ID (0x540000)
BASE_ID = 0x540000  # 5505024

# All 89 tetrominoes from the game, in canonical order.
# Format: "World [region] [Color] [Shape] [#]" where # only appears if multiple of same color+shape in region
TETROMINOES = [
    # World A1 (7)
    "World A1 Green J 3", "World A1 Golden T", "World A1 Green Z", "World A1 Green J 2", 
    "World A1 Green J 1", "World A1 Golden L", "World A1 Green I",
    # World A2 (3)
    "World A2 Golden L", "World A2 Green L", "World A2 Green Z",
    # World A3 (4)
    "World A3 Golden T 1", "World A3 Green Z", "World A3 Red L", "World A3 Golden T 2",
    # World A4 (4)
    "World A4 Golden Z 1", "World A4 Golden Z 2", "World A4 Golden T 1", "World A4 Golden T 2",
    # World A5 (5)
    "World A5 Red Z", "World A5 Green I", "World A5 Green T 1", "World A5 Green T 2", "World A5 Green L",
    # World A6 (4)
    "World A6 Green Z", "World A6 Red L 1", "World A6 Red L 2", "World A6 Red Z",
    # World A7 (5)
    "World A7 Red L", "World A7 Green L", "World A7 Red T", "World A7 Red O", "World A7 Green T",
    # World B1 (5)
    "World B1 Golden L", "World B1 Golden Z", "World B1 Golden S", "World B1 Golden T 1", "World B1 Golden T 2",
    # World B2 (4)
    "World B2 Red L", "World B2 Golden S", "World B2 Golden T", "World B2 Golden Z",
    # World B3 (3)
    "World B3 Golden T", "World B3 Golden J", "World B3 Red L",
    # World B4 (6)
    "World B4 Red T 1", "World B4 Red T 2", "World B4 Green T", "World B4 Green J", "World B4 Red L 1", "World B4 Red L 2",
    # World B5 (5)
    "World B5 Red I", "World B5 Red L", "World B5 Red S", "World B5 Green J", "World B5 Red Z",
    # World B6 (3)
    "World B6 Red I", "World B6 Golden T", "World B6 Golden L",
    # World B7 (4)
    "World B7 Red J", "World B7 Red I", "World B7 Golden O", "World B7 Golden I",
    # World C1 (4)
    "World C1 Red Z", "World C1 Red J", "World C1 Red I", "World C1 Red T",
    # World C2 (4)
    "World C2 Red Z", "World C2 Red O", "World C2 Red T", "World C2 Red S",
    # World C3 (4)
    "World C3 Red J", "World C3 Red O", "World C3 Red Z", "World C3 Red T",
    # World C4 (4)
    "World C4 Red T 1", "World C4 Red I", "World C4 Red S", "World C4 Red T 2",
    # World C5 (4)
    "World C5 Red I", "World C5 Red O 1", "World C5 Red O 2", "World C5 Red T",
    # World C6 (3)
    "World C6 Red S", "World C6 Red J", "World C6 Red O",
    # World C7 (4)
    "World C7 Red T 1", "World C7 Red O", "World C7 Red T 2", "World C7 Red L",
]

# ── Item groups by colour + shape (for gate / door rule counting) ──────────

# Green pieces
GREEN_J = [t for t in TETROMINOES if "Green J" in t]
GREEN_Z = [t for t in TETROMINOES if "Green Z" in t]
GREEN_I = [t for t in TETROMINOES if "Green I" in t]
GREEN_L = [t for t in TETROMINOES if "Green L" in t]
GREEN_T = [t for t in TETROMINOES if "Green T" in t]

# Golden pieces
GOLDEN_T = [t for t in TETROMINOES if "Golden T" in t]
GOLDEN_L = [t for t in TETROMINOES if "Golden L" in t]
GOLDEN_Z = [t for t in TETROMINOES if "Golden Z" in t]
GOLDEN_S = [t for t in TETROMINOES if "Golden S" in t]
GOLDEN_J = [t for t in TETROMINOES if "Golden J" in t]
GOLDEN_O = [t for t in TETROMINOES if "Golden O" in t]
GOLDEN_I = [t for t in TETROMINOES if "Golden I" in t]

# Red pieces
RED_L = [t for t in TETROMINOES if "Red L" in t]
RED_Z = [t for t in TETROMINOES if "Red Z" in t]
RED_T = [t for t in TETROMINOES if "Red T" in t]
RED_I = [t for t in TETROMINOES if "Red I" in t]
RED_J = [t for t in TETROMINOES if "Red J" in t]
RED_O = [t for t in TETROMINOES if "Red O" in t]
RED_S = [t for t in TETROMINOES if "Red S" in t]


# ── Build the item table ───────────────────────────────────────────────────

item_table: typing.Dict[str, ItemData] = {}

# All tetrominoes are progression (needed for gates / doors / goals)
for i, tetromino in enumerate(TETROMINOES):
    item_table[tetromino] = ItemData(
        BASE_ID + i,
        ItemClassification.progression,
    )

# Filler items
item_table["Energy Refill"] = ItemData(BASE_ID + 200, ItemClassification.filler)
item_table["Time Extension"] = ItemData(BASE_ID + 201, ItemClassification.filler)
item_table["Hint"] = ItemData(BASE_ID + 202, ItemClassification.filler)


# ── Item groups for hinting ────────────────────────────────────────────────

item_groups = {
    "Tetrominoes": set(TETROMINOES),
    "Green Tetrominoes": {t for t in TETROMINOES if "Green" in t},
    "Golden Tetrominoes": {t for t in TETROMINOES if "Golden" in t},
    "Red Tetrominoes": {t for t in TETROMINOES if "Red" in t},
}
