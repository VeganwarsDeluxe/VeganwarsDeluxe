Match stages
=====

Conventional flow
------------
The conventional session of Veganwars game consists of different stages (being a turn-based game).

1. Initialization of the **match lobby**.
2. Joining of the players.
    On this stage you may add AI entities to the battle or set up a team (#TODO: link teams doc page) building mechanic.
3. Starting the session.
    Usually this is followed by a process of players choosing different weapons and skills.
4. Executing the session turn cycle.
    1. Pre-move procedures.
        - Updating list of actions available to the entities
        - Sending out PreMoveGameEvent
        - Executing .pre_move() on Session (which executes this method on all entities by default)
        - Check if the Session should end now
        - Broadcasting info and action buttons to players
            On this step players choose their action for the following turn. During this stage, you can
            force someone skip a turn or choose actions for NPCs.
    2. Executing the move.
        For more details about the Session.move(), refer to the Session article. In general,
        it executes all actions in the **action queue**, calculates the damages and deaths, and increments
        the turn number in the end.
    3. Broadcasting the game logs.
        Each turn Session.texts contains LocalizedString objects,
        ready for the broadcast to each player on their language.
5. End of the match.
    Most often it occurs when only one team or player is left alive.

Initialization of the lobby
------------