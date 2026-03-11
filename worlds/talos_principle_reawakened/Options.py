from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Toggle

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


@dataclass
class TalosPrincipleOptions(PerGameCommonOptions):
    starting_tetromino_count: StartingTetrominoCount
    reusable_tetrominos: ReusableTetrominos
    randomise_purple_sigils: RandomisePurpleSigils
    randomise_stars: RandomiseStars
    randomise_bonus_puzzles: RandomiseBonusPuzzles
