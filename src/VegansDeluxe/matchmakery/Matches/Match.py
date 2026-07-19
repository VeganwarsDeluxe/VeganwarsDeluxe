import random

from VegansDeluxe.core import Engine, Session, RegisterEvent, EventContext, Entity, ls, PreMoveGameEvent, ItemAction, \
    Skill, ActionTag, Item
from VegansDeluxe.core.Question.Question import Question
from VegansDeluxe.core.Skills.Skill import SkillTag
from VegansDeluxe.core.Translator.LocalizedString import LocalizedString
from VegansDeluxe.matchmakery.Events.MatchEvents import RequestTeamChoiceEvent, \
    RequestActionChoiceEvent, BroadcastLogsEvent, BroadcastEndMessagesEvent, DisplayActionSelectionMenuEvent, \
    DisplayQuestionChoiceMenuEvent, DisplayItemChoiceEvent, DisplayWeaponSelectionMenuEvent, WeaponsChosenEvent, \
    SkillsChosenEvent, DisplaySkillSelectionMenuEvent
from VegansDeluxe.matchmakery.Events.NPCEvents import NPCChooseAction
from VegansDeluxe.matchmakery.Tags import EntityTag


class Match:
    name: str | LocalizedString = ls("matches.basic")

    def __init__(self, match_id, engine: Engine):
        self.engine = engine

        self.id = match_id
        self.session: Session = None # TODO: late init here, because of init_async. this is really stupid.

        # Preparation stage
        self.preparation_steps = [
            self.distribute_starting_items,
            self.choose_weapons,
            self.choose_skills,
        ]

        self.state_pool = []
        self.item_pool = []
        self.weapon_pool = []
        self.skill_pool = []

        self.item_amount = 2
        self.skill_amount = 2

        self.weapon_choice_window = 3
        self.skill_choice_window = 5
        self.item_choice_window = 3

        # Misc
        self.detached = False

        # Setup temporaries:
        self.players_with_skill_choice = []
        self.players_with_weapon_choice = []

        # Per-cycle temporaries:
        self.ready_players = []
        self.question_cache = {}

    async def init_async(self):
        """To be overridden by implementations."""

        self.session: Session = await self.create_session(self.id)

        @RegisterEvent(self.session.id, BroadcastLogsEvent, subscription_id="BroadcastLogsEvent")
        async def handler(context: EventContext[BroadcastLogsEvent]):
            """
            Event handler.
            Hook for UI to handle their displays.

            ex: await send.telegram.message
            """

        @RegisterEvent(self.session.id, DisplayActionSelectionMenuEvent)
        async def handler(context: EventContext[DisplayActionSelectionMenuEvent]):
            pass

        @RegisterEvent(self.session.id, DisplayQuestionChoiceMenuEvent)
        async def handler(context: EventContext[DisplayQuestionChoiceMenuEvent]):
            pass

        @RegisterEvent(self.session.id, DisplayItemChoiceEvent)
        async def handler(context: EventContext[DisplayItemChoiceEvent]):
            """
            if not EntityTag.NPC in player.tags:
                code = player.locale
                items = ', '.join([self.localize_text(item.name, code) for item in player.items])
                await self.send_message_to_player(ls("deluxe.matches.messages.your_items").format(items), player,
                                                  ignore_dm_game=True)
            """

        @RegisterEvent(self.session.id, DisplayItemChoiceEvent)
        async def handler(context: EventContext[DisplayItemChoiceEvent]):
            """
            await self.send_message_to_chat(ls("deluxe.matches.messages.weapons_chosen"))
            """

        @RegisterEvent(self.session.id, SkillsChosenEvent)
        async def handler(context: EventContext[DisplayItemChoiceEvent]):
            """
            weapons_text = LocalizedList([
                ls("bot.common.player_weapon").format(player.name, player.weapon.name)
                for player in self.session.alive_entities], separator="\n"
            )
            text = ls("bot.matches.messages.start").format(weapons_text)
            await self.broadcast_to_players(text)
            await self.send_message_to_chat(text)
            """

        @RegisterEvent(self.session.id, event=RequestActionChoiceEvent)
        async def handle_choose_action_call(context: EventContext[RequestActionChoiceEvent]):
            entity = self.session.get_entity(context.event.entity_id)
            if context.event.canceled or entity.dead:
                self.ready_players.append(entity)
                return
            if EntityTag.NPC in entity.tags:
                npc_event = NPCChooseAction(self.session.id, self.session.turn, entity.id)
                await self.engine.event_manager.publish(npc_event)
                self.ready_players.append(entity)
            else:
                await self.ui_display_action_selection_menu(entity)

    # --- INFO, GETTERS & PROPERTIES ---

    def is_everyone_ready(self):
        ready_ids = {entity.id for entity in self.ready_players}
        alive_ids = {entity.id for entity in self.session.alive_entities}
        return alive_ids.issubset(ready_ids)

    @property
    def player_ids(self):
        return [p.id for p in self.session.entities]

    def player_skill_pool(self, player: Entity):
        skill_pool: list[Skill] = []
        for skill in self.skill_pool:
            if player.weapon.ranged and SkillTag.MELEE_WEAPON_ONLY in skill.tags:
                continue
            if not player.weapon.ranged and SkillTag.RANGED_WEAPON_ONLY in skill.tags:
                continue
            skill_pool.append(skill)
        return skill_pool

    def player_item_pool(self, player: Entity):
        item_pool: list[Item] = []
        for item in self.item_pool:
            item_pool.append(item)
        return item_pool

    def get_player(self, user_id):
        user_id = str(user_id)
        result = [p for p in self.session.entities if p.id == user_id]
        if result:
            return result[0]
        return None

    # --- LOGIC ---

    async def create_session(self, match_id: str) -> Session:
        session = Session(self.engine.event_manager)
        session.id = match_id
        await self.engine.attach_session(session)
        return session

    async def join_session(self, player_id: int, player_name: str) -> Entity:
        player = Entity(self.session.id, name=player_name)
        player.energy, player.max_energy, player.hp, player.max_hp = 5, 5, 4, 4
        player.id = player_id
        self.session.attach_entity(player)
        await self.engine.attach_states(player, self.state_pool)
        await self.request_team_selection(player)
        return player

    async def launch(self):
        """Starts the preparation sequence, ending the Lobby stage."""
        await self.distribute_starting_items()
        await self.choose_weapons()

    async def start_game(self):
        """Starts a game."""
        await self.session.start()
        await self.pre_move()

    async def update_game_actions(self):
        """Updates actions for a game."""
        await self.engine.action_manager.update_actions(self.session)

    async def handle_pre_move_events(self):
        """Handles events before a move."""
        self.session.pre_move()
        await self.engine.event_manager.publish(PreMoveGameEvent(self.session.id, self.session.turn))

    async def process_selected_action(self, user_id, target_id, act_id):
        """
        Receives the action selection from the player, queues it, and tries to advance the game.
        """
        player: Entity = self.get_player(user_id)
        target = self.session.get_entity(target_id)
        action = self.engine.action_manager.get_action(self.session, player, act_id)

        action.target = target

        if ActionTag.ITEM in action.tags:
            action: ItemAction
            player.items.remove(action.item)

        if action.cost == -1:
            queue = True
            await action.execute()
        else:
            queue = self.engine.action_manager.queue_action_instance(action)

        await self.engine.action_manager.update_actions(self.session)

        if queue:
            await self.ui_display_action_selection_menu(player)
            return
        self.ready_players.append(player)
        if self.is_everyone_ready():
            await self.move()


    # --- Match setup logic ---

    async def pre_move(self):
        """First part of the turn cycle. Preparation phase, or "pre-move".
        - Updating available actions (accounting for any changes from the previous turn)
        - Unready all players
        - Broadcasts the PreMoveEvent
        - Checks the status of the match. If it matches all finishing conditions - it is immediately ended.
        - Requests action choices from players (rendering respective UIs)
        - Tries to advance the game to the second part if all players are already ready (all either stunned or NPCs)
        """
        await self.engine.action_manager.update_actions(self.session)
        self.ready_players = []

        self.session.pre_move()
        await self.engine.event_manager.publish(PreMoveGameEvent(self.session.id, self.session.turn))

        if not await self.check_game_status():
            return
        await self.request_action_choice()
        if self.is_everyone_ready():
            await self.move()

    async def move(self):
        """Second part of the turn cycle. The "move" itself.
        - Checks the status of the match again, trying to end it.
        - Executes all the queued actions, broadcasts the MoveEvents (a lot of them) and displays the logs where needed.
        - Advances to the pre-move phase of the next turn.
        """
        if not await self.check_game_status():
            return
        self.session.say(ls("matchmakery.messages.turn_number").format(self.session.turn))
        await self.session.move()

        broadcast_logs_event = BroadcastLogsEvent(self.session.id, self.session.turn)
        await self.engine.event_manager.publish(broadcast_logs_event)

        await self.pre_move()

    async def check_game_status(self):
        """Checks the status of the game and sends end game messages if needed."""
        if not self.session.active:
            if self.detached:
                # TODO: As i remember, this is a bad bugfix.
                #  This function tries to detach the session multiple times. Which it shouldn't.
                return
            self.detached = True

            broadcast_logs_event = BroadcastEndMessagesEvent(self.session.id, self.session.turn)
            await self.engine.event_manager.publish(broadcast_logs_event)

            self.engine.detach_session(self.session)
            return False
        return True

    async def distribute_starting_items(self):
        for player in self.session.entities:
            given = []
            for _ in range(self.item_amount):
                item = random.choice(self.item_pool)()
                pool = list(filter(lambda i: i.id not in given, self.item_pool))
                if pool:
                    item = random.choice(pool)()
                given.append(item.id)
                player.items.append(item)

            display_item_choice_event = DisplayItemChoiceEvent(self.session.id, self.session.turn, player.id)
            await self.engine.event_manager.publish(display_item_choice_event)

    async def choose_weapons(self):
        for player in self.session.entities:
            if player in self.players_with_weapon_choice:
                continue
            if EntityTag.NPC in player.tags:
                # TODO: But again. Maybe they also should choose weapons like any other?
                self.players_with_weapon_choice.append(player)
                continue
            await self.ui_display_weapon_choice_menu(player)
        await self.attempt_finish_weapon_choice()

    async def attempt_finish_weapon_choice(self):
        if len(self.players_with_weapon_choice) == len(self.session.entities):
            event = WeaponsChosenEvent(self.session.id, self.session.turn)
            await self.engine.event_manager.publish(event)
            await self.choose_skills()

    async def attempt_finish_skill_choice(self):
        if not len(self.players_with_skill_choice) == len(self.session.entities):
            return
        event = SkillsChosenEvent(self.session.id, self.session.turn)
        await self.engine.event_manager.publish(event)
        await self.start_game()

    async def choose_skills(self):
        for player in self.session.entities:
            if player in self.players_with_skill_choice:
                continue
            if EntityTag.NPC in player.tags:
                # TODO: But again. Maybe they also should choose skills like any other?
                self.players_with_skill_choice.append(player)
                continue
            if self.skill_amount == 0:
                self.players_with_skill_choice.append(player)
                continue
            await self.ui_display_skill_choice_menu(player)
        await self.attempt_finish_skill_choice()

    async def request_team_selection(self, player: Entity):
        team_choice_event = RequestTeamChoiceEvent(self.session.id, self.session.turn, player.id)
        await self.engine.event_manager.publish(team_choice_event)

    async def request_action_choice(self):
        """Requests choice of action from entities. If all are ready, advances the cycle."""
        for entity in self.session.alive_entities:
            choose_action_event = RequestActionChoiceEvent(self.session.id, self.session.turn, entity.id)
            await self.engine.event_manager.publish(choose_action_event)

        if self.is_everyone_ready():
            await self.move()
            return

    # --- UI Methods ---

    async def ui_display_action_selection_menu(self, player):
        event = DisplayActionSelectionMenuEvent(self.session.id, self.session.turn, player.id)
        await self.engine.event_manager.publish(event)

    async def ui_display_question_choice_menu(self, player: Entity, question: Question):
        event = DisplayQuestionChoiceMenuEvent(self.session.id, self.session.turn, player.id, question.id)
        await self.engine.event_manager.publish(event)

    async def ui_display_weapon_choice_menu(self, player: Entity):
        event = DisplayWeaponSelectionMenuEvent(self.session.id, self.session.turn, player.id)
        await self.engine.event_manager.publish(event)

    async def ui_display_skill_choice_menu(self, player: Entity):
        event = DisplaySkillSelectionMenuEvent(self.session.id, self.session.turn, player.id)
        await self.engine.event_manager.publish(event)