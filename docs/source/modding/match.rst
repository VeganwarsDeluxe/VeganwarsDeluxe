Writing a Match
=====

Writing a Dungeon
-----------------

A :class:`VegansDeluxe.matchmakery.Dungeon` runs a sequence of complete
``Match`` instances. Each level gets its own ordinary lobby, equipment and
skill selection, turn cycle, and ending. The Dungeon does not impose any
carry-over rule: its hooks receive both the previous and current matches, so
content can move or replace entities, alter their states, or create entirely
new participants.

.. code-block:: python

   from VegansDeluxe.matchmakery import Dungeon
   from DeluxeMod.Matches.BasicMatch import BasicMatch

   class ExampleDungeon(Dungeon):
       async def create_first_match(self):
           return BasicMatch(self.id, self.engine)

       async def create_next_match(self, previous):
           # Return another Match, or None after the final level.
           return None

       async def initialize_match(self, previous, current):
           # Populate current.session. On later levels, previous.session is
           # available for content-defined carry-over.
           pass

       async def before_match_launch(self, previous, current):
           # Runs before current.launch(), including before equipment choices.
           pass

       async def on_match_finished(self, completed):
           pass

       async def on_dungeon_finished(self, final_match):
           pass

``DungeonMatchStartedEvent`` is published after a child match is initialized
and before its selection lifecycle starts. UI implementations should bind to
that event to attach their per-session handlers when the active match changes.
