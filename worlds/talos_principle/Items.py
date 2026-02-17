import typing

from BaseClasses import Item, ItemClassification


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification


class TalosPrincipleItem(Item):
    game: str = "The Talos Principle"


# Base item ID - must match client's BASE_ITEM_ID (0x540000)
BASE_ID = 0x540000  # 5505024

# Tetromino definitions: {name: count}
# 21 unique color+shape combinations, 90 total pieces
TETROMINO_COUNTS = {
    # Green pieces (18 total)
    "Green J": 5,
    "Green Z": 4,
    "Green I": 2,
    "Green L": 3,
    "Green T": 4,
    # Golden pieces (23 total)
    "Golden T": 10,
    "Golden L": 4,
    "Golden Z": 4,
    "Golden S": 2,
    "Golden J": 1,
    "Golden O": 1,
    "Golden I": 1,
    # Red pieces (49 total)
    "Red L": 10,
    "Red Z": 6,
    "Red T": 12,
    "Red I": 6,
    "Red J": 4,
    "Red O": 7,
    "Red S": 4,
}

# List of unique tetromino names
TETROMINOES = list(TETROMINO_COUNTS.keys())

# ── Item groups by colour + shape (for gate / door rule counting) ──────────

# Green pieces - return lists with N copies for counting
GREEN_J = ["Green J"] * TETROMINO_COUNTS["Green J"]
GREEN_Z = ["Green Z"] * TETROMINO_COUNTS["Green Z"]
GREEN_I = ["Green I"] * TETROMINO_COUNTS["Green I"]
GREEN_L = ["Green L"] * TETROMINO_COUNTS["Green L"]
GREEN_T = ["Green T"] * TETROMINO_COUNTS["Green T"]

# Golden pieces
GOLDEN_T = ["Golden T"] * TETROMINO_COUNTS["Golden T"]
GOLDEN_L = ["Golden L"] * TETROMINO_COUNTS["Golden L"]
GOLDEN_Z = ["Golden Z"] * TETROMINO_COUNTS["Golden Z"]
GOLDEN_S = ["Golden S"] * TETROMINO_COUNTS["Golden S"]
GOLDEN_J = ["Golden J"] * TETROMINO_COUNTS["Golden J"]
GOLDEN_O = ["Golden O"] * TETROMINO_COUNTS["Golden O"]
GOLDEN_I = ["Golden I"] * TETROMINO_COUNTS["Golden I"]

# Red pieces
RED_L = ["Red L"] * TETROMINO_COUNTS["Red L"]
RED_Z = ["Red Z"] * TETROMINO_COUNTS["Red Z"]
RED_T = ["Red T"] * TETROMINO_COUNTS["Red T"]
RED_I = ["Red I"] * TETROMINO_COUNTS["Red I"]
RED_J = ["Red J"] * TETROMINO_COUNTS["Red J"]
RED_O = ["Red O"] * TETROMINO_COUNTS["Red O"]
RED_S = ["Red S"] * TETROMINO_COUNTS["Red S"]


# ── Build the item table ───────────────────────────────────────────────────

item_table: typing.Dict[str, ItemData] = {}

# All tetrominoes are progression (needed for gates / doors / goals)
for i, tetromino in enumerate(TETROMINOES):
    item_table[tetromino] = ItemData(
        BASE_ID + i,
        ItemClassification.progression,
    )

# Filler item (used when starting tetrominoes are pre-collected)
item_table["Nothing"] = ItemData(None, ItemClassification.filler)


# ── Item groups for hinting ────────────────────────────────────────────────

item_groups = {
    "Tetrominoes": set(TETROMINOES),
    "Green Tetrominoes": {t for t in TETROMINOES if "Green" in t},
    "Golden Tetrominoes": {t for t in TETROMINOES if "Golden" in t},
    "Red Tetrominoes": {t for t in TETROMINOES if "Red" in t},
}
