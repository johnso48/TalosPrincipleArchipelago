"""
Access rules for The Talos Principle randomiser.

Tetrominoes are **single-use** – each piece is consumed when placed in a
gate, tool panel, or tower door.  Logic checks must verify the player has
enough *cumulative* pieces of each colour + shape for every gate / tool /
door on the path to a given location or goal.

Colors: Green, Golden, Red
Shapes: I, J, L, O, S, T, Z

Gate cost summary (Green pieces, cumulative along the chain):
  A1 Gate:               2J + 1Z
  + A Gate:            + 1J + 1I + 1L + 1Z            = 3J + 2Z + 1I + 1L
  + B Gate (from A):   + 2T + 1Z + 1I + 1L            = 3J + 3Z + 2I + 2L + 2T
  + C Gate (from A):   + 2T + 2J + 1L + 1Z            = 5J + 3Z + 1I + 2L + 2T
  All four gates:                                        5J + 4Z + 2I + 3L + 4T

Tool cost summary (Golden pieces, each an independent purchase):
  Connector:    2T + 1L                 (requires A1 Gate)
  Hexahedron:   2T + 1L                 (requires A1 Gate)
  Fans:         2T + 1L + 1Z + 1S       (requires B Gate)
  Playback:     2T + 1J + 1S + 1Z       (requires B Gate)
  Platform:     2T + 1L + 1Z + 1I + 1O  (requires C Gate)
  All five:     10T + 4L + 3Z + 2S + 1J + 1I + 1O

Tower door cost summary (Red pieces, cumulative across 5 floors):
  Floor 1:  2Z + 2L
  Floor 2:  1O + 4T + 4L
  Floor 3:  4I + 2J + 2L + 1Z + 1S
  Floor 4:  2O + 4T + 1J + 1L + 2S + 2Z
  Floor 5:  2I + 4O + 4T + 1J + 1L + 1Z + 1S
  Total:    12T + 10L + 6Z + 6I + 4J + 7O + 4S  (49 pieces)
"""

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule

from .Items import (
    TETROMINO_COUNTS,
    GREEN_J, GREEN_Z, GREEN_I, GREEN_L, GREEN_T,
    GOLDEN_T, GOLDEN_L, GOLDEN_Z, GOLDEN_S, GOLDEN_J, GOLDEN_O, GOLDEN_I,
    RED_L, RED_Z, RED_T, RED_I, RED_J, RED_O, RED_S,
)


# ═══════════════════════════════════════════════════════════════════════════
#  Counting helper
# ═══════════════════════════════════════════════════════════════════════════

def _count(state: CollectionState, player: int, items: list[str]) -> int:
    """Return how many items from *items* the player has received.
    
    Since we now have duplicate item names (e.g., multiple "Green J" items),
    we use state.count() to get the actual count rather than checking has().
    """
    if not items:
        return 0
    # All items in the list are the same name, just count that item
    return state.count(items[0], player)


# ═══════════════════════════════════════════════════════════════════════════
#  Core requirement checker (single-use aware)
# ═══════════════════════════════════════════════════════════════════════════

def has_requirements(
    state: CollectionState,
    player: int,
    in_region: str | None = None,
    a1_gate: bool = False,
    connector: bool = False,
    hexahedron: bool = False,
    fans: bool = False,
    playback: bool = False,
    platform: bool = False,
) -> bool:
    """Check that the player has enough *cumulative* pieces for all gates
    and tools on the path to a particular location.

    ``in_region`` encodes which gate chain is needed just to *enter* the
    location's region:

    * ``"a1"``  – World A1 (no gate)
    * ``"a"``   – World A  (A1 Gate)
    * ``"b"``   – World B  (A1 + A + B Gates)
    * ``"c"``   – World C  (A1 + A + C Gates)

    Each tool flag adds that tool's golden cost **and** ensures its gate
    prerequisite is also open.  Since pieces are single-use the costs are
    **summed**, not max'd.

    **Tool pairing:** Connector & Hexahedron share the golden pool at A1
    Gate level; Fans & Playback share the golden pool at B Gate level.
    Because the player can unlock either tool of a pair first, requesting
    *one* tool of a pair automatically budgets for *both* to prevent
    false-positive reachability (the player could have already spent
    pieces on the partner tool).
    """

    # ── Pair tools that share a golden-tetromino pool ────────────────
    # Connector & Hexahedron are both purchasable at A1 Gate level.
    # Fans & Playback are both purchasable at B Gate level.
    # Since golden tetrominoes are single-use, the player can unlock
    # either tool of a pair first.  If the logic only budgets for one
    # tool, the player could have already spent those pieces on its
    # partner, leaving the checked tool unaffordable.  Budgeting for
    # the whole pair prevents the tracker from marking both sets of
    # locations as reachable when the player can only afford one.
    if connector or hexahedron:
        connector = True
        hexahedron = True
    if fans or playback:
        fans = True
        playback = True

    # ── Which gates must be open? ─────────────────────────────────────
    need_a1 = a1_gate or in_region in ("a", "b", "c")
    need_a  = in_region in ("b", "c")
    need_b  = in_region == "b"
    need_c  = in_region == "c"

    # Tool gate prerequisites
    if connector or hexahedron:
        need_a1 = True
    if fans or playback:
        need_a1 = True; need_a = True; need_b = True
    if platform:
        need_a1 = True; need_a = True; need_c = True

    # ── Cumulative Green cost (gates) ─────────────────────────────────
    gj = gz = gi = gl = gt = 0
    if need_a1:  gj += 2; gz += 1                       # A1 Gate
    if need_a:   gj += 1; gi += 1; gl += 1; gz += 1     # A Gate
    if need_b:   gt += 2; gz += 1; gi += 1; gl += 1     # B Gate
    if need_c:   gt += 2; gj += 2; gl += 1; gz += 1     # C Gate

    # ── Cumulative Golden cost (tools) ────────────────────────────────
    mt = ml = mz = ms = mj = mi = mo = 0
    if connector:   mt += 2; ml += 1
    if hexahedron:  mt += 2; ml += 1
    if fans:        mt += 2; ml += 1; mz += 1; ms += 1
    if playback:    mt += 2; mj += 1; ms += 1; mz += 1
    if platform:    mt += 2; ml += 1; mz += 1; mi += 1; mo += 1

    return (
        _count(state, player, GREEN_J)  >= gj and
        _count(state, player, GREEN_Z)  >= gz and
        _count(state, player, GREEN_I)  >= gi and
        _count(state, player, GREEN_L)  >= gl and
        _count(state, player, GREEN_T)  >= gt and
        _count(state, player, GOLDEN_T) >= mt and
        _count(state, player, GOLDEN_L) >= ml and
        _count(state, player, GOLDEN_Z) >= mz and
        _count(state, player, GOLDEN_S) >= ms and
        _count(state, player, GOLDEN_J) >= mj and
        _count(state, player, GOLDEN_I) >= mi and
        _count(state, player, GOLDEN_O) >= mo
    )


# ═══════════════════════════════════════════════════════════════════════════
#  Ascension (Tower) – cumulative red-piece check
# ═══════════════════════════════════════════════════════════════════════════

def can_ascend(state: CollectionState, player: int) -> bool:
    """Ascension goal – climb all 5 tower floors.

    Requires:
      * World A Gate for tower access
      * All five tools (Connector, Hexahedron, Fans, Playback, Platform)
      * Enough red pieces for all 5 doors (cumulative, single-use)
    """
    # Tools automatically pull in gates: A1+A (Connector/Hex) + B (Fans/Playback) + C (Platform)
    if not has_requirements(
        state, player, in_region="a",
        connector=True, hexahedron=True,
        fans=True, playback=True, platform=True,
    ):
        return False

    return (
        _count(state, player, RED_T)  >= 12 and
        _count(state, player, RED_L)  >= 10 and
        _count(state, player, RED_Z)  >= 6  and
        _count(state, player, RED_I)  >= 6  and
        _count(state, player, RED_J)  >= 4  and
        _count(state, player, RED_O)  >= 7  and
        _count(state, player, RED_S)  >= 4
    )


# ═══════════════════════════════════════════════════════════════════════════
#  Public entry points called from __init__.py
# ═══════════════════════════════════════════════════════════════════════════

def set_rules(world) -> None:
    """Set entrance rules and the victory condition."""
    player = world.player
    multiworld = world.multiworld

    # ── Entrance rules (cumulative Green for the gate chain) ──────────
    # World A1 → World A: A1 Gate = 2J + 1Z
    multiworld.get_entrance("World A1 -> World A", player).access_rule = \
        lambda state: has_requirements(state, player, in_region="a")

    # World A → World B: A1 + A + B Gates = 3J + 3Z + 2I + 2L + 2T
    multiworld.get_entrance("World A -> World B", player).access_rule = \
        lambda state: has_requirements(state, player, in_region="b")

    # World A → World C: A1 + A + C Gates = 5J + 3Z + 1I + 2L + 2T
    multiworld.get_entrance("World A -> World C", player).access_rule = \
        lambda state: has_requirements(state, player, in_region="c")

    # ── Victory condition ─────────────────────────────────────────────
    goal = world.options.goal_requirement.value

    if goal == 1:  # Ascension
        multiworld.completion_condition[player] = \
            lambda state: can_ascend(state, player)
    else:  # Transcendence – reach World C + all tetrominoes
        total_tetrominoes = sum(TETROMINO_COUNTS.values())
        multiworld.completion_condition[player] = \
            lambda state: (
                has_requirements(state, player, in_region="c") and
                sum(_count(state, player, [name] * count)
                    for name, count in TETROMINO_COUNTS.items()) >= total_tetrominoes
            )


def set_location_rules(world) -> None:
    """Set per-location access rules accounting for single-use consumption.

    Each rule uses ``has_requirements`` which computes the *total* Green and
    Golden pieces the player must have received to open every gate and tool
    on the path to that location.
    """
    player = world.player
    multiworld = world.multiworld

    def loc(name: str):
        return multiworld.get_location(name, player)

    # ── World A1 – two locations behind the A1 Gate ───────────────────
    for name in ["World A1 Golden L", "World A1 Green I"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, a1_gate=True))

    # ── World A4 – Connector ──────────────────────────────────────────
    for name in ["World A4 Golden Z 1", "World A4 Golden Z 2",
                 "World A4 Golden T 1", "World A4 Golden T 2"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, in_region="a",
                                                connector=True))

    # ── World A5 ──────────────────────────────────────────────────────
    for name in ["World A5 Red Z", "World A5 Green I"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, in_region="a",
                                                hexahedron=True))
    for name in ["World A5 Green T 1", "World A5 Green T 2", "World A5 Green L"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, in_region="a",
                                                connector=True, hexahedron=True))

    # ── World A6 ──────────────────────────────────────────────────────
    set_rule(loc("World A6 Green Z"),
             lambda state: has_requirements(state, player, in_region="a"))
    for name in ["World A6 Red L 1", "World A6 Red Z"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, in_region="a",
                                                connector=True))
    set_rule(loc("World A6 Red L 2"),
             lambda state: has_requirements(state, player, in_region="a",
                                            connector=True, hexahedron=True))

    # ── World A7 ──────────────────────────────────────────────────────
    for name in ["World A7 Green L", "World A7 Red T",
                 "World A7 Red O", "World A7 Green T"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, in_region="a",
                                                connector=True))
    set_rule(loc("World A7 Red L"),
             lambda state: has_requirements(state, player, in_region="a",
                                            connector=True, hexahedron=True))

    # ── World B1 ──────────────────────────────────────────────────────
    for name in ["World B1 Golden L", "World B1 Golden Z", "World B1 Golden S"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, in_region="b",
                                                connector=True))
    for name in ["World B1 Golden T 1", "World B1 Golden T 2"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, in_region="b",
                                                hexahedron=True))

    # ── World B2 ──────────────────────────────────────────────────────
    set_rule(loc("World B2 Red L"),
             lambda state: has_requirements(state, player, in_region="b"))
    set_rule(loc("World B2 Golden S"),
             lambda state: has_requirements(state, player, in_region="b",
                                            connector=True))
    set_rule(loc("World B2 Golden T"),
             lambda state: has_requirements(state, player, in_region="b",
                                            hexahedron=True, fans=True))
    set_rule(loc("World B2 Golden Z"),
             lambda state: has_requirements(state, player, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True))

    # ── World B3 ──────────────────────────────────────────────────────
    set_rule(loc("World B3 Golden T"),
             lambda state: has_requirements(state, player, in_region="b",
                                            hexahedron=True, fans=True))
    set_rule(loc("World B3 Golden J"),
             lambda state: has_requirements(state, player, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World B3 Red T"),
             lambda state: has_requirements(state, player, in_region="b",
                                            hexahedron=True, fans=True))
    set_rule(loc("World B3 Red L"),
             lambda state: has_requirements(state, player, in_region="b",
                                            hexahedron=True, fans=True))

    # ── World B4 ──────────────────────────────────────────────────────
    set_rule(loc("World B4 Red T 1"),
             lambda state: has_requirements(state, player, in_region="b",
                                            hexahedron=True, connector=True))
    set_rule(loc("World B4 Red T 2"),
             lambda state: has_requirements(state, player, in_region="b",
                                            hexahedron=True, playback=True))
    set_rule(loc("World B4 Green T"),
             lambda state: has_requirements(state, player, in_region="b",
                                            playback=True))
    set_rule(loc("World B4 Green J"),
             lambda state: has_requirements(state, player, in_region="b",
                                            playback=True))
    set_rule(loc("World B4 Red L 1"),
             lambda state: has_requirements(state, player, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World B4 Red L 2"),
             lambda state: has_requirements(state, player, in_region="b",
                                            playback=True, connector=True))

    # ── World B5 ──────────────────────────────────────────────────────
    set_rule(loc("World B5 Red I"),
             lambda state: has_requirements(state, player, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True, playback=True))
    set_rule(loc("World B5 Red L"),
             lambda state: has_requirements(state, player, in_region="b",
                                            playback=True))
    set_rule(loc("World B5 Red S"),
             lambda state: has_requirements(state, player, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World B5 Green J"),
             lambda state: has_requirements(state, player, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World B5 Red Z"),
             lambda state: has_requirements(state, player, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True))

    # ── World B6 ──────────────────────────────────────────────────────
    set_rule(loc("World B6 Red I"),
             lambda state: has_requirements(state, player, in_region="b"))
    for name in ["World B6 Golden T", "World B6 Golden L"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, in_region="b",
                                                connector=True))

    # ── World B7 ──────────────────────────────────────────────────────
    set_rule(loc("World B7 Red J"),
             lambda state: has_requirements(state, player, in_region="b"))
    set_rule(loc("World B7 Red I"),
             lambda state: has_requirements(state, player, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World B7 Golden O"),
             lambda state: has_requirements(state, player, in_region="b",
                                            hexahedron=True))
    set_rule(loc("World B7 Golden I"),
             lambda state: has_requirements(state, player, in_region="b",
                                            connector=True))

    # ── World C1 ──────────────────────────────────────────────────────
    set_rule(loc("World C1 Red Z"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World C1 Red J"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World C1 Red I"),
             lambda state: has_requirements(state, player, in_region="c",
                                            connector=True))
    set_rule(loc("World C1 Red T"),
             lambda state: has_requirements(state, player, in_region="c"))

    # ── World C2 ──────────────────────────────────────────────────────
    set_rule(loc("World C2 Red Z"),
             lambda state: has_requirements(state, player, in_region="c",
                                            playback=True, platform=True))
    set_rule(loc("World C2 Red O"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, connector=True,
                                            playback=True, platform=True))
    set_rule(loc("World C2 Red T"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, connector=True))
    set_rule(loc("World C2 Red S"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, playback=True,
                                            platform=True))

    # ── World C3 ──────────────────────────────────────────────────────
    for name in ["World C3 Red J", "World C3 Red O",
                 "World C3 Red Z", "World C3 Red T"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, in_region="c",
                                                hexahedron=True,
                                                connector=True, fans=True))

    # ── World C4 ──────────────────────────────────────────────────────
    set_rule(loc("World C4 Red T 1"),
             lambda state: has_requirements(state, player, in_region="c",
                                            connector=True))
    set_rule(loc("World C4 Red I"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, connector=True))
    set_rule(loc("World C4 Red S"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, connector=True,
                                            playback=True, platform=True))
    set_rule(loc("World C4 Red T 2"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, connector=True,
                                            fans=True))

    # ── World C5 ──────────────────────────────────────────────────────
    set_rule(loc("World C5 Red I"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, connector=True,
                                            fans=True, playback=True))
    set_rule(loc("World C5 Red O 1"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, connector=True,
                                            playback=True))
    set_rule(loc("World C5 Red O 2"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World C5 Red T"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, connector=True))

    # ── World C6 ──────────────────────────────────────────────────────
    set_rule(loc("World C6 Red S"),
             lambda state: has_requirements(state, player, in_region="c"))
    set_rule(loc("World C6 Red J"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, connector=True))
    set_rule(loc("World C6 Red O"),
             lambda state: has_requirements(state, player, in_region="c",
                                            connector=True, playback=True))

    # ── World C7 ──────────────────────────────────────────────────────
    set_rule(loc("World C7 Red T 1"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World C7 Red O"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, fans=True))
    set_rule(loc("World C7 Red T 2"),
             lambda state: has_requirements(state, player, in_region="c",
                                            connector=True, playback=True))
    set_rule(loc("World C7 Red L"),
             lambda state: has_requirements(state, player, in_region="c",
                                            hexahedron=True, connector=True))
