Terminology of the Engine
=====

I started writing Deluxe in the Rebuild era, where the game was spaghetti code
and the game was not divided into proper terminology. And so I set on to
crystallize the fundamental parts of the game itself.

Entity
----
An Entity is an actor in the game. It is the Player and it is the NPC.
At its core, the Entity can use Actions, has basic attributes such as HP and energy,
can have Items, has a Weapon, has many States (such as bleeding, stun, armor, etc.) and
can have various Skills.

All that Entity does during the game - is choose Actions to execute. Or dies/wins.

Action
----
90% of everything that happens during the game is the result of Actions.
Attack is an Action, dodging/approaching is an Action. Using an Item is an Action.
Actions are provided to the Entity by itself, Items, States, Skills and the Weapon.

There is one important feature of the Action - the cost.
There's 3 types of Actions by cost:
 - Instant Action. Executed **immediately** upon choice. Examples:
   Info/Visor (viewing entity's stats) and switching weapons.
 - Free Action. Executed normally during the turn (CallActionsGameEvent),
   but allows the Entity to choose more Actions to add to the queue. Examples:
   Using medicinal Items such as adrenaline. You can stack multiple in one turn.
 - Decisive Action. Same as Free Action, but concludes the action choice stage for the Entity. Examples:
   Attacking, dodging, approaching.

Other distinctive feature of the Action - it **always** has a Source and a Target (both of them are Entities). Actions that
seemingly don't have a target (approach, skip turn) have the Source as its Target.

Actions also have a Target Type - a filter with 4 values, limiting the scope of Targets the Action can be applied to.
Those values are Distance, Team, Aliveness and Selfishness (excludes or includes the Source itself).

Item
----
One of the simpler elements of the game. Usually provides an Action to the Entity
that is executed upon use of the Item. The Item then is consumed.

Weapon
----
An Entity must have exactly one Weapon, however it can be changed/swapped during the game. It provides Actions for the
Entity - usually Attack Actions, but optionally some other types as well.

A Weapon has an cubes, damage bonus, accuracy bonus and energy cost.

Imagine the Shotgun - 6 cubes, 1 damage bonus, -2 accuracy bonus and 4 energy cost.
6 cubes means that 6 times a 1-10 dice will be thrown and compared against the attack's total accuracy. That accuracy is
a sum of Source's energy and various accuracy bonuses. For a success, the dice must score -less or equal- of the total accuracy,
so the higher the accuracy, the higher the chance.

The number of successful dice throws is the amount of Damage **Calculated**. The Attack is considered missed if the Calculated Damage is 0.
After going through some transformations it will become Damage **Displayed** - a number you see in logs like "Player A attacked Player B, dealing X damage".
And finally it becomes Damage **Dealt** - an actual amount of damage that the Target will receive.
Those three steps are there to easily influence the damage (add bonuses/block it) either reflecting that in the logs, or not.

States & Skills
----
States are more complex, and are solutions for Entity's intrinsics.
All existing States that **may** be influenced **must** be attached to the Entity on the game's launch.
You never know when the Entity might be "bleeding" or "stunned" for example.

In Deluxe, Skill is identical to the State feature-wise. The only difference they have is conventional usage.
In contrast to States, Skills are completely optional for the game sequence, and are meant to be chosen as additional perks.

A State can influence the Entity right on attachment, before the first turn - add HP, energy, initialize cooldown timers, so on.
By convention, only Skills make visible changes right from the start, and States are usually noticed only when they are triggered
by something. For example, the Bat (Weapon) may increase Stun (State), so the Target is forced to skip a number of turns.

Both also can provide Actions to the Entity.

