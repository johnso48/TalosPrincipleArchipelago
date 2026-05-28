from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Toggle

ORDERING_OPTIONS = {
    1: "ABC",
    2: "ACB",
    3: "BAC",
    4: "BCA",
    5: "CAB",
    6: "CBA"
}

class StartingTetrominoCount(Choice):
    """
    Number of random tetrominoes to start with.
    This can help prevent softlocks and make the early game more forgiving.
    """
    display_name = "Starting Tetromino Count"
    option_0 = 0
    option_3 = 3
    option_5 = 5
    option_10 = 10
    default = 0


class ReusableTetrominoes(Toggle):
    """
    When enabled, tetrominoes are returned to the player after being placed in
    a gate, tool panel, or tower door, making each piece reusable.

    This dramatically reduces the number of tetrominoes required to reach climb
    the tower (from 90 down to ~37).
    """
    display_name = "Reusable Tetrominoes"
    default = 0


class RandomisePurpleSigils(Toggle):
    """
    When enabled, the 24 Purple Sigils hidden throughout the worlds are randomised
    """
    display_name = "Randomise Purple Sigils"
    default = 0


class RandomiseStars(Toggle):
    """
    When enabled, the 30 Stars hidden throughout the worlds are randomised.
    """
    display_name = "Randomise Stars"
    default = 0


class RandomiseBonusPuzzles(Toggle):
    """
    When enabled, the 9 Bonus White tetrominoes are randomised.

    If stars are also randomised, logic will require all 30 stars to be collected before 
    the bonus puzzles can be completed due to the potential of unlocking them in any order,
    unless an order is specified in bonus_level_order below.
    """
    display_name = "Randomise Bonus Puzzles"
    default = 0


class ShuffleMechanics(Toggle):
    """
    When enabled, Golden tetrominoes are removed from the item pool and the
    five mechanic tools (Connector, Hexahedron, Fans, Playback, Platform)
    are shuffled into the item pool.
    """
    display_name = "Shuffle Mechanics"
    default = 0


class ShuffleWorldGates(Toggle):
    """
    When enabled, Green tetrominoes are removed from the item pool and the
    four world gates (World A1 Gate, World A Gate, World B Gate, World C
    Gate) are shuffled into the item pool.

    When received, the tetrominoes required to open the gate will be granted to the player
    """
    display_name = "Shuffle Messenger Gates"
    default = 0


class BonusLevelOrder(Choice):
    """
    Logic normally requires all 30 stars to access the 3 bonus levels, to avoid potential softlocks.
    This option allows for specifying the access order for the 3 bonus levels. If an order is specified,
    you will still need the appropriate world access and puzzle mechanics unlocked to complete them.

    For example, selecting "BAC" would put world B's bonus level into logic at 10 stars, A's at 20, and C's at 30.
    "unchanged" keeps the above behavior, requiring all 30 stars for bonus level access.
    """
    display_name = "Bonus Level Order"
    default = 0
    option_UNCHANGED = 0
    option_ABC = 1
    option_ACB = 2
    option_BAC = 3
    option_BCA = 4
    option_CAB = 5
    option_CBA = 6


class MessengerIslandOrder(Choice):
    """
    Logic normally requires all 24 purple sigils to access the 3 messenger islands, to avoid potential softlocks.
    This option allows for specifying the access order for the 3 messenger islands. If an order is specified,
    you will still need the appropriate world access to access them.

    Note this option currently has minimal value, because the only messenger island check currently is the star in
    messenger island A. Thus, setting an order only affects how late into the seed that star may enter logic.
    This option will gain value if messenger items are added as Archipelago items in the future.

    For example, selecting "CAB" would put messenger island A's star into logic at 16 purple sigils.
    "unchanged" keeps the above behavior, requiring all 24 purple sigils for messenger island access.
    """
    display_name = "Messenger Island Order"
    default = 0
    option_UNCHANGED = 0
    option_ABC = 1
    option_ACB = 2
    option_BAC = 3
    option_BCA = 4
    option_CAB = 5
    option_CBA = 6

@dataclass
class TalosPrincipleOptions(PerGameCommonOptions):
    starting_tetromino_count: StartingTetrominoCount
    reusable_tetrominoes: ReusableTetrominoes
    randomise_purple_sigils: RandomisePurpleSigils
    randomise_stars: RandomiseStars
    randomise_bonus_puzzles: RandomiseBonusPuzzles
    shuffle_mechanics: ShuffleMechanics
    shuffle_world_gates: ShuffleWorldGates
    bonus_level_order: BonusLevelOrder
    messenger_island_order: MessengerIslandOrder
