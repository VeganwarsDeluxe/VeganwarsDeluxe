from VegansDeluxe.core import ls
from VegansDeluxe.deluxe.Entities.Confucius import Confucius
from VegansDeluxe.matchmakery.Matches.Match import Match
from VegansDeluxe.rebuild import all_states


class ConfuciusMatch(Match):
    name = ls("matchmakery.matches.confucius")

    def __init__(self, match_id, engine):
        super().__init__(match_id, engine)

    async def join_session(self, player_id, player_name):
        player = await super().join_session(player_id, player_name)
        player.team = 'players'

        confucius = Confucius(self.id, name=ls("matchmakery.confucius.name"))
        self.session.attach_entity(confucius)
        await self.engine.attach_states(confucius, all_states)
