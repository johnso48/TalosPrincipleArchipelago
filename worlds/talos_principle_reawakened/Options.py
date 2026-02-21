from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Toggle


class GoalRequirement(Choice):
    """
    What is required to complete the game.

    Transcendence: Reach World C and collect all 89 tetrominoes.
    Ascension:     Climb to the top of the tower (all 5 floors).
    """
    display_name = "Goal Requirement"
    option_transcendence = 0
    option_ascension = 1
    default = 0


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

    This dramatically reduces the number of tetrominoes required to reach any
    goal (from 90 down to ~37).
    """
    display_name = "Reusable Tetrominos"
    default = 0


@dataclass
class TalosPrincipleOptions(PerGameCommonOptions):
    goal_requirement: GoalRequirement
    starting_tetromino_count: StartingTetrominoCount
    reusable_tetrominos: ReusableTetrominos
