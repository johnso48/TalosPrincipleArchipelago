from typing import Dict, List

from BaseClasses import Entrance, Item, ItemClassification, Region, Tutorial
from worlds.AutoWorld import WebWorld, World

from .Items import TETROMINO_COUNTS, TalosPrincipleItem, item_groups, item_table
from .Locations import (
    MAIN_LOCATIONS,
    REGION_WORLD_A,
    REGION_WORLD_A1,
    REGION_WORLD_B,
    REGION_WORLD_C,
    TalosPrincipleLocation,
)
from .Options import TalosPrincipleOptions
from .Rules import set_location_rules, set_rules


class TalosPrincipleWeb(WebWorld):
    """Web world configuration for The Talos Principle."""

    theme = "stone"

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up The Talos Principle for Archipelago.",
            "English",
            "setup_en.md",
            "setup/en",
            ["YourName"],
        )
    ]


class TalosPrincipleWorld(World):
    """
    The Talos Principle is a philosophical first-person puzzle game from Croteam.
    In this randomiser the 89 tetrominoes (sigils) required to progress are
    shuffled, creating a unique experience each playthrough.

    Goals:
      Transcendence – Reach World C and collect all 89 tetrominoes.
      Ascension     – Climb to the top of the tower (all 5 floors).
    """

    game = "The Talos Principle"
    options_dataclass = TalosPrincipleOptions
    web = TalosPrincipleWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in MAIN_LOCATIONS.items()}
    item_name_groups = item_groups

    required_client_version = (0, 5, 0)

    def generate_early(self) -> None:
        """Pre-collect starting tetrominoes if the option is set."""
        # Build full pool of 89 tetromino instances
        self.tetromino_pool: List[str] = []
        for name, count in TETROMINO_COUNTS.items():
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
        return TalosPrincipleItem(name, data.classification, data.code, self.player)

    def fill_slot_data(self) -> Dict[str, any]:
        return {
            "goal_requirement": self.options.goal_requirement.value,
        }

    def get_filler_item_name(self) -> str:
        return self.random.choice(["Energy Refill", "Time Extension", "Hint"])
