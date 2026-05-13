"""
Access rules for The Talos Principle Reawakened randomiser.

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
  + C Gate (from B):   + 2T + 2J + 1L + 1Z            = 5J + 4Z + 2I + 3L + 4T
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
import random

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
    reusable: bool = False,
    shuffle_mechanics: bool = False,
    shuffle_gates: bool = False,
    in_region: str | None = None,
    a1_gate: bool = False,
    connector: bool = False,
    hexahedron: bool = False,
    fans: bool = False,
    playback: bool = False,
    platform: bool = False,
) -> bool:
    """Check that the player has enough pieces for all gates and tools on
    the path to a particular location.

    ``in_region`` encodes which gate chain is needed just to *enter* the
    location's region:

    * ``"a1"``  – World A1 (no gate)
    * ``"a"``   – World A  (A1 Gate)
    * ``"b"``   – World B  (A1 + A + B Gates)
    * ``"c"``   – World C  (A1 + A + B + C Gates)

    Each tool flag adds that tool's golden cost **and** ensures its gate
    prerequisite is also open.

    When ``shuffle_mechanics`` is True the golden-tetromino cost for tools
    is replaced by shuffled tool items (``state.has("Connector", …)`` etc.).

    When ``shuffle_gates`` is True the green-tetromino cost for gates is
    replaced by shuffled gate items (``state.has("World A1 Gate", …)`` etc.).

    When ``reusable`` is False (default / single-use mode) costs are
    **summed** across every gate and tool on the path.  **Tool pairing**
    is also applied: Connector & Hexahedron share a golden pool, as do
    Fans & Playback, so requesting one of a pair budgets for both.

    When ``reusable`` is True pieces are returned after use, so only the
    costliest *individual* gate / tool matters.  No pair-budgeting is
    needed because the player can re-use pieces for each tool separately.
    """

    # ── Shuffle-mechanics mode: tools are items ───────────────────────
    if shuffle_mechanics:
        ok = True
        if connector:  ok = ok and state.has("Connector", player)
        if hexahedron: ok = ok and state.has("Hexahedron", player)
        if fans:       ok = ok and state.has("Fans", player)
        if playback:   ok = ok and state.has("Playback", player)
        if platform:   ok = ok and state.has("Platform", player)
        if not ok:
            return False

    # ── Which gates must be open? ─────────────────────────────────────
    if shuffle_gates:
        # When shuffling gates, world B and C can be done in either order after the world A gate
        need_a1 = a1_gate or in_region in ("a")
        need_a  = in_region in ("b", "c")
        need_b  = in_region == "b"
        need_c  = in_region == "c"
    else:
        need_a1 = a1_gate or in_region in ("a", "b", "c")
        need_a  = in_region in ("b", "c")
        need_b  = in_region in ("b", "c")  # reaching World C passes through the B gate
        need_c  = in_region == "c"

    # Tool gate prerequisites (only when gates are NOT shuffled items —
    # when gates are shuffled the entrance rules handle gate access)
    if not shuffle_gates:
        if connector or hexahedron:
            need_a1 = True
        if fans or playback:
            need_a1 = True; need_a = True; need_b = True
        if platform:
            need_a1 = True; need_a = True; need_c = True

    # ── Shuffle-gates mode: gate access via items ─────────────────────
    if shuffle_gates:
        ok = True
        if need_a1: ok = ok and state.has("World A1 Gate", player)
        if need_a:  ok = ok and state.has("World A Gate", player)
        if need_b:  ok = ok and state.has("World B Gate", player)
        if need_c:  ok = ok and state.has("World C Gate", player)
        if not ok:
            return False
        # Green costs are zero when gates are shuffled
        gj = gz = gi = gl = gt = 0
        # Golden costs handled below (may still need them if mechanics aren't shuffled)
        if shuffle_mechanics:
            mt = ml = mz = ms = mj = mi = mo = 0
        elif reusable:
            # Golden: no pair-budgeting — max per piece across requested tools.
            tool_costs: list[dict] = []
            if connector:  tool_costs.append({"t": 2, "l": 1})
            if hexahedron: tool_costs.append({"t": 2, "l": 1, "z": 1})
            if fans:       tool_costs.append({"t": 2, "l": 1, "z": 1, "s": 1})
            if playback:   tool_costs.append({"t": 2, "j": 1, "s": 1, "z": 1})
            if platform:   tool_costs.append({"t": 2, "l": 1, "z": 1, "i": 1, "o": 1})
            mt = max((c.get("t", 0) for c in tool_costs), default=0)
            ml = max((c.get("l", 0) for c in tool_costs), default=0)
            mz = max((c.get("z", 0) for c in tool_costs), default=0)
            ms = max((c.get("s", 0) for c in tool_costs), default=0)
            mj = max((c.get("j", 0) for c in tool_costs), default=0)
            mi = max((c.get("i", 0) for c in tool_costs), default=0)
            mo = max((c.get("o", 0) for c in tool_costs), default=0)
        else:
            # Single-use tool pairing
            if connector or hexahedron:
                connector = True; hexahedron = True
            if fans or playback:
                connector = True; hexahedron = True
                fans = True; playback = True
            if platform:
                connector = True; hexahedron = True
                fans = True; playback = True; platform = True
            mt = ml = mz = ms = mj = mi = mo = 0
            if connector:   mt += 2; ml += 1
            if hexahedron:  mt += 2; ml += 1; mz += 1
            if fans:        mt += 2; ml += 1; mz += 1; ms += 1
            if playback:    mt += 2; mj += 1; ms += 1; mz += 1
            if platform:    mt += 2; ml += 1; mz += 1; mi += 1; mo += 1
    elif reusable:
        # ── Reusable mode: pieces are returned after use ──────────────
        # Green: player only needs enough for the costliest single gate.
        gate_costs: list[dict] = []
        if need_a1: gate_costs.append({"j": 2, "z": 1})
        if need_a:  gate_costs.append({"j": 1, "z": 1, "i": 1, "l": 1})
        if need_b:  gate_costs.append({"t": 2, "z": 1, "i": 1, "l": 1})
        if need_c:  gate_costs.append({"t": 2, "j": 2, "l": 1, "z": 1})
        gj = max((g.get("j", 0) for g in gate_costs), default=0)
        gz = max((g.get("z", 0) for g in gate_costs), default=0)
        gi = max((g.get("i", 0) for g in gate_costs), default=0)
        gl = max((g.get("l", 0) for g in gate_costs), default=0)
        gt = max((g.get("t", 0) for g in gate_costs), default=0)

        # Golden: skip when mechanics are shuffled (already checked above)
        if shuffle_mechanics:
            mt = ml = mz = ms = mj = mi = mo = 0
        else:
            tool_costs: list[dict] = []
            if connector:  tool_costs.append({"t": 2, "l": 1})
            if hexahedron: tool_costs.append({"t": 2, "l": 1, "z": 1})
            if fans:       tool_costs.append({"t": 2, "l": 1, "z": 1, "s": 1})
            if playback:   tool_costs.append({"t": 2, "j": 1, "s": 1, "z": 1})
            if platform:   tool_costs.append({"t": 2, "l": 1, "z": 1, "i": 1, "o": 1})
            mt = max((c.get("t", 0) for c in tool_costs), default=0)
            ml = max((c.get("l", 0) for c in tool_costs), default=0)
            mz = max((c.get("z", 0) for c in tool_costs), default=0)
            ms = max((c.get("s", 0) for c in tool_costs), default=0)
            mj = max((c.get("j", 0) for c in tool_costs), default=0)
            mi = max((c.get("i", 0) for c in tool_costs), default=0)
            mo = max((c.get("o", 0) for c in tool_costs), default=0)
    else:
        # ── Single-use mode: pieces are consumed ──────────────────────
        # Pair tools that share a golden-tetromino pool (only when not shuffled).
        if not shuffle_mechanics:
            if connector or hexahedron:
                connector = True
                hexahedron = True
            if fans or playback:
                connector = True
                hexahedron = True
                fans = True
                playback = True
            if platform:
                connector = True
                hexahedron = True
                fans = True
                playback = True
                platform = True

        # Cumulative Green cost (gates)
        gj = gz = gi = gl = gt = 0
        if need_a1:  gj += 2; gz += 1                       # A1 Gate
        if need_a:   
            gj += 1; gi += 1; gl += 1; gz += 1     # A Gate
            if not shuffle_mechanics:
                connector = True; hexahedron = True
        if need_b:   gt += 2; gz += 1; gi += 1; gl += 1     # B Gate
        if need_c:   
            gt += 2; gj += 2; gl += 1; gz += 1     # C Gate
            if not shuffle_mechanics:
                connector = True; hexahedron = True
                fans = True; playback = True

        # Cumulative Golden cost (tools) — skip when mechanics are shuffled
        if shuffle_mechanics:
            mt = ml = mz = ms = mj = mi = mo = 0
        else:
            mt = ml = mz = ms = mj = mi = mo = 0
            if connector:   mt += 2; ml += 1
            if hexahedron:  mt += 2; ml += 1; mz += 1
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
#  Tower floor access – red-piece check for individual floors
# ═══════════════════════════════════════════════════════════════════════════

# Per-floor red tetromino costs (1-indexed via list access)
_TOWER_FLOOR_COSTS = [
    {"z": 2, "l": 2},                                          # Floor 1
    {"o": 1, "t": 4, "l": 4},                                  # Floor 2
    {"i": 4, "j": 2, "l": 2, "z": 1, "s": 1},                 # Floor 3
    {"o": 2, "t": 4, "j": 1, "l": 1, "s": 2, "z": 2},         # Floor 4
    {"i": 2, "o": 4, "t": 4, "j": 1, "l": 1, "z": 1, "s": 1}, # Floor 5
]


def can_open_tower_floor(
    state: CollectionState, player: int, floor: int, reusable: bool = False,
) -> bool:
    """Check that the player has enough red pieces to open tower doors
    through the given *floor* (1-indexed, so ``floor=1`` checks Floor 1 only,
    ``floor=5`` checks all five floors)."""
    costs = _TOWER_FLOOR_COSTS[:floor]
    if reusable:
        rt = max(c.get("t", 0) for c in costs)
        rl = max(c.get("l", 0) for c in costs)
        rz = max(c.get("z", 0) for c in costs)
        ri = max(c.get("i", 0) for c in costs)
        rj = max(c.get("j", 0) for c in costs)
        ro = max(c.get("o", 0) for c in costs)
        rs = max(c.get("s", 0) for c in costs)
    else:
        rt = rl = rz = ri = rj = ro = rs = 0
        for c in costs:
            rt += c.get("t", 0); rl += c.get("l", 0)
            rz += c.get("z", 0); ri += c.get("i", 0)
            rj += c.get("j", 0); ro += c.get("o", 0)
            rs += c.get("s", 0)
    return (
        _count(state, player, RED_T) >= rt and
        _count(state, player, RED_L) >= rl and
        _count(state, player, RED_Z) >= rz and
        _count(state, player, RED_I) >= ri and
        _count(state, player, RED_J) >= rj and
        _count(state, player, RED_O) >= ro and
        _count(state, player, RED_S) >= rs
    )


# ═══════════════════════════════════════════════════════════════════════════
#  Ascension (Tower) – cumulative red-piece check
# ═══════════════════════════════════════════════════════════════════════════

def can_ascend(
    state: CollectionState, player: int,
    reusable: bool = False,
    shuffle_mechanics: bool = False,
    shuffle_gates: bool = False,
) -> bool:
    """Ascension goal – climb all 5 tower floors.

    Requires:
      * World A Gate for tower access (unless shuffle_gates)
      * All five tools (Connector, Hexahedron, Fans, Playback, Platform)
      * Enough red pieces for all 5 doors

    In single-use mode the red cost is the cumulative total across all five
    floors (12T/10L/6Z/6I/4J/7O/4S).  In reusable mode only the costliest
    individual floor matters (4T/4L/2Z/4I/2J/4O/2S).
    """
    # Tools automatically pull in gates: A1+A (Connector/Hex) + B (Fans/Playback) + C (Platform)
    if not has_requirements(
        state, player, reusable=reusable,
        shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates,
        in_region="a",
        connector=True, hexahedron=True,
        fans=True, playback=True, platform=True,
    ):
        return False

    if reusable:
        # Max pieces needed for any single tower-floor door:
        #   F1: 2L 2Z  |  F2: 4T 4L 1O  |  F3: 4I 2J 2L 1Z 1S
        #   F4: 4T 2O 1J 1L 2S 2Z  |  F5: 4T 4O 2I 1J 1L 1Z 1S
        return (
            _count(state, player, RED_T) >= 4 and
            _count(state, player, RED_L) >= 4 and
            _count(state, player, RED_Z) >= 2 and
            _count(state, player, RED_I) >= 4 and
            _count(state, player, RED_J) >= 2 and
            _count(state, player, RED_O) >= 4 and
            _count(state, player, RED_S) >= 2
        )

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
    reusable = bool(world.options.reusable_tetrominos.value)
    shuffle_mechanics = bool(world.options.shuffle_mechanics.value)
    shuffle_gates = bool(world.options.shuffle_world_gates.value)

    # ── Entrance rules ────────────────────────────────────────────────
    # When shuffle_world_gates is on, entrance rules check for gate items.
    # Otherwise they check for green-tetromino costs.
    if shuffle_gates:
        multiworld.get_entrance("World A1 -> World A", player).access_rule = \
            lambda state: (
                state.has("World A1 Gate", player) and
                state.has("World A Gate", player)
            )
        multiworld.get_entrance("World A -> World B", player).access_rule = \
            lambda state: state.has("World B Gate", player)
        multiworld.get_entrance("World A -> World C", player).access_rule = \
            lambda state: state.has("World C Gate", player)
    else:
        multiworld.get_entrance("World A1 -> World A", player).access_rule = \
            lambda state: has_requirements(state, player, reusable=reusable, in_region="a")

        multiworld.get_entrance("World A -> World B", player).access_rule = \
            lambda state: has_requirements(state, player, reusable=reusable, in_region="b")

        multiworld.get_entrance("World A -> World C", player).access_rule = \
            lambda state: has_requirements(state, player, reusable=reusable, in_region="c")

    multiworld.completion_condition[player] = \
        lambda state: can_ascend(state, player, reusable=reusable,
                                 shuffle_mechanics=shuffle_mechanics,
                                 shuffle_gates=shuffle_gates)


def set_location_rules(world) -> None:
    """Set per-location access rules.

    Each rule uses ``has_requirements`` with the ``reusable`` flag forwarded
    from the world options, so logic correctly reflects either cumulative
    (single-use) or max-per-gate/tool (reusable) piece requirements.
    """
    player = world.player
    multiworld = world.multiworld
    reusable = bool(world.options.reusable_tetrominos.value)
    shuffle_mechanics = bool(world.options.shuffle_mechanics.value)
    shuffle_gates = bool(world.options.shuffle_world_gates.value)

    def loc(name: str):
        return multiworld.get_location(name, player)

    # ── World A1 – two locations behind the A1 Gate ───────────────────
    for name in ["World A1 Golden L", "World A1 Green I"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, a1_gate=True))

    # ── World A4 – Connector ──────────────────────────────────────────
    for name in ["World A4 Golden Z 1", "World A4 Golden Z 2",
                 "World A4 Golden T 1", "World A4 Golden T 2"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                                connector=True))

    # ── World A5 ──────────────────────────────────────────────────────
    for name in ["World A5 Red Z", "World A5 Green I"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                                hexahedron=True))
    for name in ["World A5 Green T 1", "World A5 Green T 2", "World A5 Green L"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                                connector=True, hexahedron=True))

    # ── World A6 ──────────────────────────────────────────────────────
    set_rule(loc("World A6 Green Z"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a"))
    for name in ["World A6 Red L 1", "World A6 Red Z"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                                connector=True))
    set_rule(loc("World A6 Red L 2"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                            connector=True, hexahedron=True))

    # ── World A7 ──────────────────────────────────────────────────────
    for name in ["World A7 Green L", "World A7 Red T",
                 "World A7 Red O", "World A7 Green T"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                                connector=True))
    set_rule(loc("World A7 Red L"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                            connector=True, hexahedron=True))

    # ── World B1 ──────────────────────────────────────────────────────
    for name in ["World B1 Golden L", "World B1 Golden Z", "World B1 Golden S"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                connector=True))
    for name in ["World B1 Golden T 1", "World B1 Golden T 2"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                hexahedron=True))

    # ── World B2 ──────────────────────────────────────────────────────
    set_rule(loc("World B2 Red L"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b"))
    set_rule(loc("World B2 Golden S"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            connector=True))
    set_rule(loc("World B2 Golden T"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            hexahedron=True, fans=True))
    set_rule(loc("World B2 Golden Z"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True))

    # ── World B3 ──────────────────────────────────────────────────────
    set_rule(loc("World B3 Golden T"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            hexahedron=True, fans=True))
    set_rule(loc("World B3 Golden J"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World B3 Red T"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            hexahedron=True, fans=True))
    set_rule(loc("World B3 Red L"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            hexahedron=True, fans=True))

    # ── World B4 ──────────────────────────────────────────────────────
    set_rule(loc("World B4 Red T 1"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            hexahedron=True, connector=True))
    set_rule(loc("World B4 Red T 2"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            hexahedron=True, playback=True))
    set_rule(loc("World B4 Green T"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            playback=True))
    set_rule(loc("World B4 Green J"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            playback=True))
    set_rule(loc("World B4 Red L 1"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World B4 Red L 2"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            playback=True, connector=True))

    # ── World B5 ──────────────────────────────────────────────────────
    set_rule(loc("World B5 Red I"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True, playback=True))
    set_rule(loc("World B5 Red L"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            playback=True))
    set_rule(loc("World B5 Red S"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World B5 Green J"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World B5 Red Z"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True))

    # ── World B6 ──────────────────────────────────────────────────────
    set_rule(loc("World B6 Red I"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b"))
    for name in ["World B6 Golden T", "World B6 Golden L"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                connector=True))

    # ── World B7 ──────────────────────────────────────────────────────
    set_rule(loc("World B7 Red J"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b"))
    set_rule(loc("World B7 Red I"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World B7 Golden O"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            hexahedron=True))
    set_rule(loc("World B7 Golden I"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                            connector=True))

    # ── World C1 ──────────────────────────────────────────────────────
    set_rule(loc("World C1 Red Z"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World C1 Red J"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World C1 Red I"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            connector=True))
    set_rule(loc("World C1 Red T"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c"))

    # ── World C2 ──────────────────────────────────────────────────────
    set_rule(loc("World C2 Red Z"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            playback=True, platform=True))
    set_rule(loc("World C2 Red O"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, connector=True,
                                            playback=True, platform=True))
    set_rule(loc("World C2 Red T"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, connector=True))
    set_rule(loc("World C2 Red S"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, playback=True,
                                            platform=True))

    # ── World C3 ──────────────────────────────────────────────────────
    for name in ["World C3 Red J", "World C3 Red O",
                 "World C3 Red Z", "World C3 Red T"]:
        set_rule(loc(name),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                                hexahedron=True,
                                                connector=True, fans=True))

    # ── World C4 ──────────────────────────────────────────────────────
    set_rule(loc("World C4 Red T 1"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            connector=True))
    set_rule(loc("World C4 Red I"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, connector=True))
    set_rule(loc("World C4 Red S"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, connector=True,
                                            playback=True, platform=True))
    set_rule(loc("World C4 Red T 2"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, connector=True,
                                            fans=True))

    # ── World C5 ──────────────────────────────────────────────────────
    set_rule(loc("World C5 Red I"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, connector=True,
                                            fans=True, playback=True))
    set_rule(loc("World C5 Red O 1"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, connector=True,
                                            playback=True))
    set_rule(loc("World C5 Red O 2"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World C5 Red T"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, connector=True))

    # ── World C6 ──────────────────────────────────────────────────────
    set_rule(loc("World C6 Red S"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c"))
    set_rule(loc("World C6 Red J"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, connector=True))
    set_rule(loc("World C6 Red O"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            connector=True, playback=True))

    # ── World C7 ──────────────────────────────────────────────────────
    set_rule(loc("World C7 Red T 1"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, connector=True,
                                            fans=True))
    set_rule(loc("World C7 Red O"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, fans=True))
    set_rule(loc("World C7 Red T 2"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            connector=True, playback=True))
    set_rule(loc("World C7 Red L"),
             lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                            hexahedron=True, connector=True, fans=True))

    # ── Purple Sigils (only present when randomise_purple_sigils is on) ──
    if bool(world.options.randomise_purple_sigils.value):
        # World A sigils
        set_rule(loc("World A4 Purple Sigil"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                                connector=True))
        set_rule(loc("World A5 Purple Sigil"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                                hexahedron=True))
        set_rule(loc("World A6 Purple Sigil"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                                connector=True))
        set_rule(loc("World A7 Purple Sigil"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                                connector=True))
        # World B sigils
        set_rule(loc("World B1 Purple Sigil 2"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                hexahedron=True))
        set_rule(loc("World B2 Purple Sigil"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                connector=True))
        set_rule(loc("World B3 Purple Sigil 2"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                hexahedron=True, fans=True))
        set_rule(loc("World B4 Purple Sigil 1"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                playback=True))
        set_rule(loc("World B4 Purple Sigil 2"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                connector=True))
        set_rule(loc("World B5 Purple Sigil"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                connector=True, hexahedron=True,
                                                fans=True))
        set_rule(loc("World B7 Purple Sigil"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                hexahedron=True))

    # ── Stars (only present when randomise_stars is on) ───────────────
    if bool(world.options.randomise_stars.value):
        # World Stars (A1 Star, A2 Star, A3 Stars need no tools beyond region)
        set_rule(loc("World A4 Star"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                                connector=True))
        set_rule(loc("World A5 Star 1"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                                connector=True))
        set_rule(loc("World A5 Star 2"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                                hexahedron=True))
        set_rule(loc("World A6 Star"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                                hexahedron=True))
        set_rule(loc("World A7 Star"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                                connector=True))
        # World B stars
        set_rule(loc("World B1 Star"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                connector=True))
        set_rule(loc("World B2 Star"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                connector=True, hexahedron=True, fans=True))
        set_rule(loc("World B3 Star"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                connector=True, hexahedron=True,
                                                fans=True))
        set_rule(loc("World B4 Star 1"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                connector=True, hexahedron=True))
        set_rule(loc("World B4 Star 2"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                connector=True, hexahedron=True,
                                                fans=True))
        set_rule(loc("World B5 Star"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                connector=True, hexahedron=True,
                                                fans=True))
        set_rule(loc("World B7 Star 1"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                hexahedron=True, fans=True))
        set_rule(loc("World B7 Star 2"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                                connector=True, hexahedron=True,
                                                fans=True))
        # World C stars
        set_rule(loc("World C1 Star"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                                connector=True))
        set_rule(loc("World C2 Star"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                                hexahedron=True, playback=True,
                                                platform=True))
        set_rule(loc("World C3 Star"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                                connector=True, hexahedron=True,
                                                fans=True))
        set_rule(loc("World C4 Star 1"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                                connector=True, hexahedron=True,
                                                playback=True, platform=True))
        set_rule(loc("World C4 Star 2"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                                connector=True, hexahedron=True,
                                                fans=True))
        set_rule(loc("World C5 Star 1"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                                connector=True, hexahedron=True,
                                                fans=True, playback=True))
        set_rule(loc("World C5 Star 2"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                                connector=True, hexahedron=True,
                                                fans=True, playback=True))
        set_rule(loc("World C5 Star 3"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                                connector=True, hexahedron=True))
        set_rule(loc("World C6 Star"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                                connector=True, playback=True))
        set_rule(loc("World C7 Star"),
                 lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                                connector=True, hexahedron=True,
                                                fans=True))
        # Messenger Island – requires 24 Purple Sigils (only when both options on)
        if bool(world.options.randomise_purple_sigils.value):
            set_rule(loc("Messenger Island Star"),
                     lambda state: (
                         has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c") and
                         state.count("Purple Sigil", player) >= 24
                     ))
        else:
            set_rule(loc("Messenger Island Star"),
                     lambda state: has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c", 
                       connector=True, hexahedron=True, 
                       fans=True, playback=True)) 
        # Tower Star – all tools + all 5 tower floors
        set_rule(loc("Tower Star"),
                 lambda state: can_ascend(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates))
        # World Hub Star – C gate + connector + tower floor 1
        set_rule(loc("World Hub Star"),
                 lambda state: (
                     has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                      connector=True) and
                     can_open_tower_floor(state, player, 1, reusable=reusable)
                 ))

    # ── Bonus Puzzles (only present when randomise_bonus_puzzles is on) ───
    if bool(world.options.randomise_bonus_puzzles.value):
        randomise_stars = bool(world.options.randomise_stars.value)

        star_worlds_ordered = False
        choice = random.choice(list(world.options.assume_star_order.value))
        if choice != "unchanged":
            star_worlds_ordered = True
            world_ordering = {
                choice[0].upper(): 10,
                choice[1].upper(): 20,
                choice[2].upper(): 30
            }
            world.options.assume_star_order.value = choice[0] + choice[1] + choice[2]  # for spoiler file output

        def _bonus_prereq(state, world) -> bool:
            """Bonus puzzles require either 30 Stars (if randomised) or
            access to all worlds + all tools (if stars are not randomised)."""
            if randomise_stars:
                if not star_worlds_ordered:
                    return state.count("Star", player) >= 30
                else:
                    return state.count("Star", player) >= world_ordering[world]

            return has_requirements(
                state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                connector=True, hexahedron=True,
                fans=True, playback=True, platform=True,
            )

        # World A Bonus Levels – require World A access + bonus prereq
        # ES1 – no extra tools
        set_rule(loc("World A Bonus ES1"),
                 lambda state: (
                     has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a") and
                     _bonus_prereq(state, "A")
                 ))
        # ES3 – Fans
        set_rule(loc("World A Bonus ES3"),
                 lambda state: (
                     has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a",
                                      fans=True) and
                     _bonus_prereq(state, "A")
                 ))
        # EL1 – no extra tools
        set_rule(loc("World A Bonus EL1"),
                 lambda state: (
                     has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="a") and
                     _bonus_prereq(state, "A")
                 ))

        # World B Bonus Levels – require World B access + bonus prereq
        # ES2 – Connector
        set_rule(loc("World B Bonus ES2"),
                 lambda state: (
                     has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                      connector=True) and
                     _bonus_prereq(state, "B")
                 ))
        # EL2 – Connector
        set_rule(loc("World B Bonus EL2"),
                 lambda state: (
                     has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                      connector=True) and
                     _bonus_prereq(state, "B")
                 ))
        # EL3 – Connector + Playback
        set_rule(loc("World B Bonus EL3"),
                 lambda state: (
                     has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="b",
                                      connector=True, playback=True) and
                     _bonus_prereq(state, "B")
                 ))

        # World C Bonus Levels – require World C access + bonus prereq
        # ES4 – Hexahedron + Connector
        set_rule(loc("World C Bonus ES4"),
                 lambda state: (
                     has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                      hexahedron=True, connector=True) and
                     _bonus_prereq(state, "C")
                 ))
        # EL4 – Connector + Hexahedron + Playback + Platform
        set_rule(loc("World C Bonus EL4"),
                 lambda state: (
                     has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                      connector=True, hexahedron=True,
                                      playback=True, platform=True) and
                     _bonus_prereq(state, "C")
                 ))
        # EO1 – Hexahedron + Connector
        set_rule(loc("World C Bonus EO1"),
                 lambda state: (
                     has_requirements(state, player, reusable=reusable, shuffle_mechanics=shuffle_mechanics, shuffle_gates=shuffle_gates, in_region="c",
                                      hexahedron=True, connector=True) and
                     _bonus_prereq(state, "C")
                 ))
