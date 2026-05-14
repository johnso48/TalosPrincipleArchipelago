from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Toggle, OptionList

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


class ReusableTetrominos(Toggle):
    """
    When enabled, tetrominoes are returned to the player after being placed in
    a gate, tool panel, or tower door, making each piece reusable.

    This dramatically reduces the number of tetrominoes required to reach climb
    the tower (from 90 down to ~37).
    """
    display_name = "Reusable Tetrominos"
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
    When enabled, the 9 Bonus White Tetrominos are randomised.

    If stars are also randomised, logic will require all 30 stars to be collected before 
    the bonus puzzles can be completed due to the potential of unlocking them in any order
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

    When received, the tetrominos required to open the gate will be granted to the player
    """
    display_name = "Shuffle Messenger Gates"
    default = 0


class StarWorldOrder(OptionList):
    """
    Logic normally waits until the player has all 30 stars before requiring star world puzzles,
    because it can't predict what order the player will spend those 30 stars. This option allows
    for specifying an order to access the 3 star worlds, allowing for star puzzles to be more spread
    out throughout the seed instead of all coming into logic simultaneously.

    Valid options are: unchanged, ABC, ACB, BAC, BCA, CAB, and CBA.
    As an example: "BAC" would put world B's star world in logic at 10 stars, A's at 20 stars, and C's at 30 stars.
        They will only appear in logic if you have the appropriate hub access and puzzle mechanics unlocked.
    "unchanged" will keep the above behavior as-is (requiring all 30 stars for star worlds).
    Putting multiple options into the list below will result in one being chosen at random.

    Note that the game will not prevent you from diverging from any order you set here. Do so at your own risk.
    """
    display_name = "Star World Order"
    valid_keys = ["unchanged", "ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]
    default = ["unchanged"]

@dataclass
class TalosPrincipleOptions(PerGameCommonOptions):
    starting_tetromino_count: StartingTetrominoCount
    reusable_tetrominos: ReusableTetrominos
    randomise_purple_sigils: RandomisePurpleSigils
    randomise_stars: RandomiseStars
    randomise_bonus_puzzles: RandomiseBonusPuzzles
    shuffle_mechanics: ShuffleMechanics
    shuffle_world_gates: ShuffleWorldGates
    star_world_order: StarWorldOrder
