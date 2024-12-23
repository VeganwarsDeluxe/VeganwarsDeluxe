from VegansDeluxe.core import ActionManager
from VegansDeluxe.core.ContentManager import RegisterEvent
from VegansDeluxe.core.Context import EventContext
from VegansDeluxe.core.Entities.Entity import Entity
from VegansDeluxe.core.Events.NPCEvents import NPCChooseAction
from VegansDeluxe.core.Session import Session


class NPC(Entity):
    type = "npc"

    def __init__(self,
                 session_id: str = '', name: str = '',
                 hp: int = 0, max_hp: int = 0,
                 energy: int = 0, max_energy: int = 0):
        super().__init__(session_id, name, hp, max_hp, energy, max_energy)

        @RegisterEvent(session_id, event=NPCChooseAction)
        async def handle_choose_action_call(context: EventContext[NPCChooseAction]):
            if self.id != context.event.entity_id:
                return
            await self.choose_act(context.session, context.action_manager)

    async def choose_act(self, session: Session, action_manager: ActionManager):
        pass
