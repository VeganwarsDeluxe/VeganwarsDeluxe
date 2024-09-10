"""
Action - building block of the game.

All attacks, usage of items, and other actions that Entities do stem from it.
"""

from VegansDeluxe.core.Actions.ActionTags import ActionTag
from VegansDeluxe.core.Entities import Entity
from VegansDeluxe.core.Events.EventManager import EventManager
from VegansDeluxe.core.Session import Session
from VegansDeluxe.core.TargetType import TargetType, Own, Aliveness, Team, Distance
from VegansDeluxe.core.Translator.LocalizedString import ls, LocalizedString


class Action:
    id: str = 'action'
    """ID of the action."""

    name: str | LocalizedString = ls("base_action_name")
    """Name of the action, that is displayed to the player."""

    priority: int = 0
    """Priority of the action. Defines the order to be executed during CallActions stage."""

    target_type: TargetType = TargetType(0, 0, 0, 0)
    """Filter for targets, to which this action can be applied."""

    type: str = 'action'
    """String type definition for the class. Used internally."""

    def __init__(self, session: Session, source: Entity, *args):
        """
        :param session: Session instance
        :param source: Entity instance of action owner
        """
        self.tags: list[ActionTag] = []
        """List of tags to categorize the action."""

        self.session: Session = session
        self.event_manager: EventManager = self.session.event_manager

        self.source: Entity = source
        self.target: Entity = source

        self.canceled = False
        """If set to True, the action will not be executed."""
        self.type = 'action'
        self.removed = False
        self.queued = False

    async def func(self, source: Entity, target: Entity):
        """
        Function to override with actual mechanics of the action.

        All Actions have Source Entity and Target Entity. Source and Target may be the same.
        """
        pass

    async def execute(self):
        if self.canceled:
            return
        return await self.func(self.source, self.target)

    @property
    def cost(self):
        """
        True if player's turn should be finalized after selecting this action, otherwise False.
        """
        return None

    @property
    def hidden(self) -> bool:
        """
        True if action should not appear for selection.

        Overwrite this function to define behaviour.
        """
        return False

    @property
    def blocked(self) -> bool:
        """
        Returns True if action should appear, but be unavailable to select.

        Overwrite this function to define behaviour.
        """
        return False

    @property
    def targets(self):
        """
        Targets applicable by this Action.
        """
        return self.get_targets(self.source, self.target_type)

    def get_targets(self, source: Entity, target_type: TargetType):
        """
        Function that filters targets by TargetType filter relative to source.
        """
        target_pool = self.session.entities
        targets = []

        for target in target_pool:
            conditions = [
                not (target_type.own == Own.SELF_ONLY and target != source),
                not (target_type.own == Own.SELF_EXCLUDED and target == source),

                not (target_type.aliveness == Aliveness.ALIVE_ONLY and target.dead),
                not (target_type.aliveness == Aliveness.DEAD_ONLY and not target.dead),

                not (target_type.team == Team.ALLIES_ONLY and not source.is_ally(target)),
                not (target_type.team == Team.ENEMIES_ONLY and source.is_ally(target)),

                not (target_type.distance == Distance.NEARBY_ONLY and target not in source.nearby_entities),
                not (target_type.distance == Distance.DISTANT_ONLY and target in source.nearby_entities)
            ]

            if all(conditions):
                targets.append(target)

        return targets


class DecisiveAction(Action):
    """
    Action that finalizes player's turn.
    """
    @property
    def cost(self):
        return True


class FreeAction(Action):
    """
    Action that after selection allows to select more for the current turn.
    """
    @property
    def cost(self):
        return False
