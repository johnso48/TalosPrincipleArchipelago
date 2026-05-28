from typing import Dict, List

from BaseClasses import Entrance, Item, ItemClassification, Region, Tutorial
from worlds.AutoWorld import WebWorld, World

from .Items import (
    BONUS_PUZZLE_COUNT,
    FILLER_ITEMS,
    GATE_ITEMS,
    PURPLE_SIGIL_COUNT,
    TETROMINO_COUNTS,
    TOOL_ITEMS,
    WHITE_TETROMINO_COUNTS,
    TalosPrincipleItem,
    item_groups,
    item_table,
)
from .Locations import (
    BONUS_PUZZLE_LOCATIONS,
    MAIN_LOCATIONS,
    PURPLE_SIGIL_LOCATIONS,
    REGION_WORLD_A,
    REGION_WORLD_A1,
    REGION_WORLD_B,
    REGION_WORLD_C,
    STAR_LOCATIONS,
    TalosPrincipleLocation,
    location_groups
)
from .Options import TalosPrincipleOptions
from .Rules import set_location_rules, set_rules


class TalosPrincipleWeb(WebWorld):
    """Web world configuration for The Talos Principle Reawakened."""

    theme = "stone"

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up The Talos Principle Reawakened for Archipelago.",
            "English",
            "setup_en.md",
            "setup/en",
            ["YourName"],
        )
    ]


class TalosPrincipleWorld(World):
    """
    The Talos Principle Reawakened is a philosophical first-person puzzle game from Croteam.
    In this randomiser the 90 tetrominoes (sigils) required to progress are
    shuffled, creating a unique experience each playthrough.

    Goals:
      Transcendence – Reach World C and collect all 90 tetrominoes.
      Ascension     – Climb to the top of the tower (all 5 floors).
    """

    game = "The Talos Principle Reawakened"
    options_dataclass = TalosPrincipleOptions
    web = TalosPrincipleWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {
        **{name: data.id for name, data in MAIN_LOCATIONS.items()},
        **{name: data.id for name, data in PURPLE_SIGIL_LOCATIONS.items()},
        **{name: data.id for name, data in STAR_LOCATIONS.items()},
        **{name: data.id for name, data in BONUS_PUZZLE_LOCATIONS.items()},
    }
    item_name_groups = item_groups
    location_name_groups = location_groups

    required_client_version = (0, 5, 0)

    def generate_early(self) -> None:
        """Pre-collect starting tetrominoes if the option is set."""
        shuffle_mechanics = bool(self.options.shuffle_mechanics.value)
        shuffle_gates = bool(self.options.shuffle_world_gates.value)

        # Build full pool of tetromino instances.
        # When shuffle_mechanics is on, Golden tetrominoes are removed
        # (tools are shuffled items instead of golden-tetromino purchases).
        # When shuffle_world_gates is on, Green tetrominoes are removed
        # (gates are shuffled items instead of green-tetromino costs).
        self.tetromino_pool: List[str] = []
        for name, count in TETROMINO_COUNTS.items():
            if shuffle_gates and "Green" in name:
                continue
            if shuffle_mechanics and "Golden" in name:
                continue
            self.tetromino_pool.extend([name] * count)

        starting_count = self.options.starting_tetromino_count.value
        if starting_count > 0:
            starting = self.random.sample(
                self.tetromino_pool, min(starting_count, len(self.tetromino_pool))
            )
            for tetromino in starting:
                self.multiworld.push_precollected(self.create_item(tetromino))
                self.tetromino_pool.remove(tetromino)

    def create_regions(self) -> None:
        """Build the four game regions and wire up entrances."""
        menu = Region("Menu", self.player, self.multiworld)
        world_a1 = Region(REGION_WORLD_A1, self.player, self.multiworld)
        world_a = Region(REGION_WORLD_A, self.player, self.multiworld)
        world_b = Region(REGION_WORLD_B, self.player, self.multiworld)
        world_c = Region(REGION_WORLD_C, self.player, self.multiworld)

        region_map: Dict[str, Region] = {
            REGION_WORLD_A1: world_a1,
            REGION_WORLD_A: world_a,
            REGION_WORLD_B: world_b,
            REGION_WORLD_C: world_c,
        }

        # Populate locations into their regions
        for loc_name, loc_data in MAIN_LOCATIONS.items():
            region = region_map[loc_data.region]
            region.locations.append(
                TalosPrincipleLocation(self.player, loc_name, loc_data.id, region)
            )

        # Optionally add Purple Sigil locations
        if self.options.randomise_purple_sigils:
            for loc_name, loc_data in PURPLE_SIGIL_LOCATIONS.items():
                region = region_map[loc_data.region]
                region.locations.append(
                    TalosPrincipleLocation(self.player, loc_name, loc_data.id, region)
                )

        # Optionally add Star locations
        if self.options.randomise_stars:
            for loc_name, loc_data in STAR_LOCATIONS.items():
                region = region_map[loc_data.region]
                region.locations.append(
                    TalosPrincipleLocation(self.player, loc_name, loc_data.id, region)
                )

        # Optionally add Bonus Puzzle locations
        if self.options.randomise_bonus_puzzles:
            for loc_name, loc_data in BONUS_PUZZLE_LOCATIONS.items():
                region = region_map[loc_data.region]
                region.locations.append(
                    TalosPrincipleLocation(self.player, loc_name, loc_data.id, region)
                )

        # Entrances
        menu.exits.append(Entrance(self.player, "Menu -> World A1", menu))
        world_a1.exits.append(Entrance(self.player, "World A1 -> World A", world_a1))
        world_a.exits.append(Entrance(self.player, "World A -> World B", world_a))
        world_a.exits.append(Entrance(self.player, "World A -> World C", world_a))

        self.multiworld.get_entrance("Menu -> World A1", self.player).connect(world_a1)
        self.multiworld.get_entrance("World A1 -> World A", self.player).connect(world_a)
        self.multiworld.get_entrance("World A -> World B", self.player).connect(world_b)
        self.multiworld.get_entrance("World A -> World C", self.player).connect(world_c)

        self.multiworld.regions += [menu, world_a1, world_a, world_b, world_c]

    def create_items(self) -> None:
        """Fill the item pool with tetrominoes (and filler if needed)."""
        for tetromino in self.tetromino_pool:
            self.multiworld.itempool.append(self.create_item(tetromino))

        # Add the 5 tool items when shuffle_mechanics is enabled
        if self.options.shuffle_mechanics:
            for tool_name in TOOL_ITEMS:
                self.multiworld.itempool.append(self.create_item(tool_name))

        # Add the 4 gate items when shuffle_world_gates is enabled
        if self.options.shuffle_world_gates:
            for gate_name in GATE_ITEMS:
                self.multiworld.itempool.append(self.create_item(gate_name))

        # Add Purple Sigil items when the option is enabled
        if self.options.randomise_purple_sigils:
            for _ in range(PURPLE_SIGIL_COUNT):
                self.multiworld.itempool.append(self.create_item("Purple Sigil"))

        # Add Star items when the option is enabled
        if self.options.randomise_stars:
            star_count = len(STAR_LOCATIONS)
            # Messenger Island excluded when purple sigils are not randomised
            if not self.options.randomise_purple_sigils:
                star_count -= 1
            for _ in range(star_count):
                self.multiworld.itempool.append(self.create_item("Star"))

        # Add White tetromino items when bonus puzzles are enabled
        if self.options.randomise_bonus_puzzles:
            for name, count in WHITE_TETROMINO_COUNTS.items():
                for _ in range(count):
                    self.multiworld.itempool.append(self.create_item(name))

        # Pad with filler if precollected items left gaps
        total_locations = sum(
            len(r.locations)
            for r in self.multiworld.regions
            if r.player == self.player
        )
        filler_needed = total_locations - len(
            [i for i in self.multiworld.itempool if i.player == self.player]
        )
        for _ in range(max(0, filler_needed)):
            self.multiworld.itempool.append(
                self.create_item(self.get_filler_item_name())
            )

    def set_rules(self) -> None:
        set_rules(self)
        set_location_rules(self)

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        classification = data.classification
        # Purple Sigils: progression when stars are randomised (gates Messenger Island star behind 24 Purple Sigils),
        if name == "Purple Sigil" and self.options.randomise_purple_sigils:
            classification = ItemClassification.progression
        # Stars become progression when bonus puzzles are randomised
        # (bonus locations all require 30 Stars to access unless the player specifies otherwise in bonus_level_order)
        if (name == "Star"
                and self.options.randomise_stars
                and self.options.randomise_bonus_puzzles):
            classification = ItemClassification.progression
        return TalosPrincipleItem(name, classification, data.code, self.player)

    def fill_slot_data(self) -> Dict[str, any]:
        return {
            "reusable_tetrominoes": self.options.reusable_tetrominoes.value,
            "randomise_purple_sigils": self.options.randomise_purple_sigils.value,
            "randomise_stars": self.options.randomise_stars.value,
            "randomise_bonus_puzzles": self.options.randomise_bonus_puzzles.value,
            "shuffle_mechanics": self.options.shuffle_mechanics.value,
            "shuffle_world_gates": self.options.shuffle_world_gates.value,
            "bonus_level_order": self.options.bonus_level_order.value
        }

    def get_filler_item_name(self) -> str:
        return self.random.choice(FILLER_ITEMS)
