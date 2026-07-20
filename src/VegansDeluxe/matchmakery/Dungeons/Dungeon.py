"""A controller for a sequence of complete Match lifecycles.

Written by AI, which is rare for the engine. Proceed with caution.
"""

from VegansDeluxe.core import Engine
from VegansDeluxe.matchmakery.Events.MatchEvents import (
    DungeonFailedEvent,
    DungeonFinishedEvent,
    DungeonMatchFinishedEvent,
    DungeonMatchStartedEvent,
)
from VegansDeluxe.matchmakery.Matches.Match import Match


class Dungeon(Match):
    """Run a sequence of ordinary :class:`Match` instances.

    A Dungeon does not prescribe how players, items, weapons, or states carry
    between levels. Its subclass creates and initializes every child Match and
    may inspect the completed Match before building the next one.

    The currently active child Match is exposed through ``session`` and all
    interaction methods are delegated to it, which makes a Dungeon usable in
    places that already accept a Match.
    """

    @staticmethod
    def _delegated_match_attribute(name):
        def getter(self):
            if self.current_match:
                return getattr(self.current_match, name)
            return self.__dict__[f"_dungeon_{name}"]

        def setter(self, value):
            if self.__dict__.get("current_match"):
                setattr(self.current_match, name, value)
            else:
                self.__dict__[f"_dungeon_{name}"] = value

        return property(getter, setter)

    weapon_pool = _delegated_match_attribute.__func__("weapon_pool")
    skill_pool = _delegated_match_attribute.__func__("skill_pool")
    item_pool = _delegated_match_attribute.__func__("item_pool")
    state_pool = _delegated_match_attribute.__func__("state_pool")
    item_amount = _delegated_match_attribute.__func__("item_amount")
    skill_amount = _delegated_match_attribute.__func__("skill_amount")
    weapon_choice_window = _delegated_match_attribute.__func__("weapon_choice_window")
    skill_choice_window = _delegated_match_attribute.__func__("skill_choice_window")
    item_choice_window = _delegated_match_attribute.__func__("item_choice_window")
    players_with_skill_choice = _delegated_match_attribute.__func__("players_with_skill_choice")
    players_with_weapon_choice = _delegated_match_attribute.__func__("players_with_weapon_choice")
    ready_players = _delegated_match_attribute.__func__("ready_players")
    question_cache = _delegated_match_attribute.__func__("question_cache")

    def __init__(self, match_id: str, engine: Engine):
        super().__init__(match_id, engine)
        self.current_match: Match | None = None
        self.completed_matches: list[Match] = []
        self.dungeon_player_ids: set[str] = set()
        self.finished = False

    async def create_first_match(self) -> Match:
        """Create the first level. Subclasses must implement this."""
        raise NotImplementedError

    async def create_next_match(self, previous: Match) -> Match | None:
        """Create the level after ``previous``; return ``None`` to finish."""
        raise NotImplementedError

    async def initialize_match(self, previous: Match | None, current: Match) -> None:
        """Populate and configure ``current`` before it is launched.

        This is deliberately the Dungeon author's extension point. It can
        inspect ``previous.session`` and transfer, replace, or create entities
        in ``current.session`` in any way the content requires.
        """

    async def before_match_launch(self, previous: Match | None, current: Match) -> None:
        """Customize a level immediately before its normal ``launch`` call."""

    async def on_match_finished(self, completed: Match) -> None:
        """Inspect a completed level before the next level is created."""

    async def on_dungeon_finished(self, final_match: Match) -> None:
        """Run final dungeon-specific cleanup or rewards."""

    def is_dungeon_failed(self, completed: Match) -> bool:
        """Return whether every player who joined this Dungeon is dead.

        Subclasses inherit this terminal condition by default, but can override
        it for modes with revives, alternate objectives, or other rules.
        """
        if not self.dungeon_player_ids:
            return False
        return not any(not entity.dead for entity in self.dungeon_players(completed))

    def dungeon_players(self, match: Match) -> list:
        """Return every human player who joined this Dungeon, alive or dead.

        A Dungeon ends only when this roster has no survivors. When at least
        one player survived, content can use this complete roster to initialize
        the next Match; a fresh Match may therefore revive players who died in
        the previous level.
        """
        return [
            entity for entity in match.session.entities
            if entity.id in self.dungeon_player_ids
        ]

    async def on_dungeon_failed(self, completed: Match) -> None:
        """Run dungeon-specific handling when all Dungeon players have died."""

    async def init_async(self):
        await self._activate_match(None)

    async def _new_match(self, previous: Match | None) -> Match | None:
        match = await (self.create_first_match() if previous is None
                       else self.create_next_match(previous))
        if match is None:
            return None
        if match.engine is not self.engine:
            raise ValueError("Dungeon matches must use the Dungeon engine.")
        if match.id != self.id:
            raise ValueError("Dungeon matches must use the Dungeon match ID.")
        return match

    async def _activate_match(self, previous: Match | None) -> Match:
        match = await self._new_match(previous)
        if match is None:
            raise RuntimeError("The first Dungeon match cannot be None.")

        await match.init_async()
        match.completion_handler = self._handle_match_completion
        self.current_match = match
        self.session = match.session

        await self.initialize_match(previous, match)
        event = DungeonMatchStartedEvent(match.session.id, match.session.turn, self, previous, match)
        await self.engine.event_manager.publish(event)
        return match

    async def _handle_match_completion(self, completed: Match) -> bool:
        """Replace a completed child Match, or finish the Dungeon."""
        self.completed_matches.append(completed)
        event = DungeonMatchFinishedEvent(completed.session.id, completed.session.turn, self, completed)
        await self.engine.event_manager.publish(event)
        await self.on_match_finished(completed)

        if self.is_dungeon_failed(completed):
            self.finished = True
            event = DungeonFailedEvent(completed.session.id, completed.session.turn, self, completed)
            await self.engine.event_manager.publish(event)
            await self.on_dungeon_failed(completed)
            self.engine.detach_session(completed.session)
            return True

        next_match = await self._new_match(completed)
        if next_match is None:
            self.finished = True
            event = DungeonFinishedEvent(completed.session.id, completed.session.turn, self, completed)
            await self.engine.event_manager.publish(event)
            await self.on_dungeon_finished(completed)
            self.engine.detach_session(completed.session)
            return True

        # The old Session's subscriptions must be removed before a new child
        # reuses this Dungeon's stable match ID.
        self.engine.detach_session(completed.session)
        await self._activate_prepared_match(completed, next_match)
        return True

    async def _activate_prepared_match(self, previous: Match, match: Match) -> Match:
        await match.init_async()
        match.completion_handler = self._handle_match_completion
        self.current_match = match
        self.session = match.session

        await self.initialize_match(previous, match)
        event = DungeonMatchStartedEvent(match.session.id, match.session.turn, self, previous, match)
        await self.engine.event_manager.publish(event)
        await self.before_match_launch(previous, match)
        await match.launch()
        return match

    async def launch(self):
        if not self.current_match:
            raise RuntimeError("Dungeon must be initialized before launch.")
        await self.before_match_launch(None, self.current_match)
        await self.current_match.launch()

    async def join_session(self, player_id: int, player_name: str):
        if not self.current_match:
            raise RuntimeError("Dungeon must be initialized before players can join.")
        player = await self.current_match.join_session(player_id, player_name)
        # Some existing Match subclasses perform the join but do not return
        # the created Entity. Resolve it from the active session so they can
        # still participate in the Dungeon's failure condition.
        if player is None:
            player = self.current_match.get_player(player_id)
        if player:
            self.dungeon_player_ids.add(str(player.id))
        return player

    async def process_selected_action(self, user_id, target_id, act_id):
        if not self.current_match:
            raise RuntimeError("Dungeon has no active match.")
        return await self.current_match.process_selected_action(user_id, target_id, act_id)

    def player_skill_pool(self, player):
        return self.current_match.player_skill_pool(player)

    def player_item_pool(self, player):
        return self.current_match.player_item_pool(player)

    async def attempt_finish_weapon_choice(self):
        return await self.current_match.attempt_finish_weapon_choice()

    async def attempt_finish_skill_choice(self):
        return await self.current_match.attempt_finish_skill_choice()

    async def ui_display_question_choice_menu(self, player, question):
        return await self.current_match.ui_display_question_choice_menu(player, question)

    async def start_game(self):
        if not self.current_match:
            raise RuntimeError("Dungeon has no active match.")
        return await self.current_match.start_game()

    async def move(self):
        if not self.current_match:
            raise RuntimeError("Dungeon has no active match.")
        return await self.current_match.move()
