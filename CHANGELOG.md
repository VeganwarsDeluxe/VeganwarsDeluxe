# Changelog

All notable changes to this project will be documented in this file.

(unfortunately, i didn't start with conventional commits. you'll see what you see.)

## [1.5.1] - 2024-09-24

### 🏷 Release

- 1.4.7

### 🐛 Bug Fixes

- Skip action was incorrectly handling events
- Skip action was incorrectly handling events

### 🧩 Structure

- Merged dev into master

### Other

- Merges pull request #3

Merge dev

## [1.4.7] - 2024-08-28

### 🏷 Release

- 1.4.7

### 🚀 Features

- Changelog

### Other

- *(dev)* Fix for inquisitor (#7)

## [1.5.0] - 2024-09-24

### 🏷 Release

- 1.5.0

### 🚀 Features

- Picking up weapon with corresponding state
- *(questions)* Introducing question/choice system
- *(async)* Added unit testing
- *(async)* Fix naming and small inconsistencies
- *(async)* Fix typo
- *(async)* Fix grenade
- *(session)* Added StopSessionGameEvent
- [**breaking**] Migrated to new naming convention
- *(localization)* [**breaking**] Migrated to new naming convention
- *(localization)* [**breaking**] Migrated to new naming convention
- *(async)* Fix ScheduledEventSubscription
- Add SessionFinishGameEvent
- [**breaking**] Type hints for State when using Entity.get_state()
- [**breaking**] Type hints for State when using Entity.get_state()
- Fixed skip action

### ⚙️ Core

- Fix typo
- Fix session manager import

### 🎮️ Rebuild content

- *(inquisitor)* Cloud timer should be displayed in effects section, not in results
- *(inquisitor)* Fixing premature stunning
- *(weaponsmith)* Utilizing new question system to implement weaponsmith
- Fixed a few inconsistencies
- Removed pyrotechnic for now
- Added pyromaniac
- *(pyromaniac)* Fix event handling
- *(pyromaniac)* Fix uk localization
- *(async)* Forgot about rifle

### 🐛 Bug Fixes

- *(actions)* Action queue is now cleaned at PostActionsGameEvent

### 🧩 Structure

- Structure(session)!: moved session to the core module instead of core.Session module
goatexchanger convinced me that Session should not be inherited by users. We don't need a separate module for it therefore.

- *(engine)* [**breaking**] Moved session to the core module instead of core.Engine module
- *(engine)* [**breaking**] Moved session to the core module instead of core.Engine module
- *(session)* [**breaking**] Moved session to the core module instead of core.Session module
- *(async)* Adding to publish (and everywhere in between)
- Dev version

### Other

- Circular imports

- Hotfix of chain

- More docstrings


## [1.4.6] - 2024-08-24

### 🧪 Testing

- Testing autodoc

- Testing autodoc

- Testing autodoc

- Testing autodoc

- Testing doc

- Testing doc


### Other

- #3 fix

- Merges pull request #1

fire fixes merge
- Change github location

- Adding a license

- Removing old stuff from .gitignore

- Trying out the docs

- Oops

- Add docs to the pyproject.toml

- Moving .readthedocs.yaml to docs

- More fancy

- More fancy

- Write basic docs and add examples

- Conventional flow article

- Npc guide

- Identations and full example

- Removing remnants of hammer from bow

- Axe fix

- Added docs on Action and partially on ActionManager
actually enabled docs

- Now gotta debug readthedocs

- Goofy ahh python version moment

- Napoleonic plans

- Module docs

- Expanding ActionManager and its docs

- More code coherence


## [1.4.5] - 2024-08-21

### Other

- Introducing LocalizedList and hopefully fix for #25

- Finishing localization for necromancer and closing #19

- Migrate action check in Chain to ActionTag tech (also closing #10)

- Thinking to migrate some content from rebuild to deluxe module

- Experimenting with setup.py

- Experimenting with src

- Experimenting with src

- Experimenting with src

- Deployment job

- Long awaited fire fix


## [1.4.4] - 2024-07-12

### Other

- Introducing LocalizedList and hopefully fix for #25


## [1.4.3] - 2024-06-15

### Other

- Circular...

- Necromancer!


## [1.4.2] - 2024-06-15

### Other

- Notifications localization

- Notifications localization

- #22 fix

- Minor localization change

- Minor localization change

- Trying to add visor to the game


## [1.4.1] - 2024-06-01

### Other

- Minor typings

- Death of session inheritance


## [1.4.0] - 2024-06-01

### Other

- Stockpile hotfix

- Rifle hotfix

- Deep Localization Release!

## [1.3.1] - 2024-05-31

### Other

- Merge remote-tracking branch 'onedev/master'

- Circular import hotfix

- Inquizitor hotfix


## [1.3.0] - 2024-05-31

### Other

- ActionTag update!
- ActionTag update!

## [1.2.8] - 2024-05-30

### 🐛 Bug Fixes

- Fixed #17 for now


### Other

- Trying to fix the None error

- Trying to fix the None error


## [1.2.7] - 2024-05-30

### Other

- Less strictness for translator


## [1.2.6] - 2024-05-30

### Other

- Flash grenade kek error

- Hotfix for thief


## [1.2.5] - 2024-05-30

### Other

- Log anomaly fixed

- Utf-8 hotfix


## [1.2.4] - 2024-05-30

### Other

- Cool

- Log anomaly fixed

- Log anomaly fixed


## [1.2.3] - 2024-05-30

### Other

- More info on errors


## [1.2.2] - 2024-05-30

### Other

- Minor localization patch

- Minor localization patch


## [1.2.1] - 2024-05-29

### 🚀 Features

- Localization patch


### Other

- + no way: localization!

- + no way: localization!

- + no way: localization!

- + no way: localization!

- + no way: localization!

- + no way: localization!

- + no way: localization!

- Setup.py fixes

- Setup.py fixes

- Setup.py fixes

- Grenade localization fixes

- Readme update

- Version


## [1.2.0] - 2024-03-27

### Other

- Chain cooldown is too small

- Enable shieldgen

- + pyrotechnic

- + nevermind

- + no way: localization!

- + no way: localization!


## [1.1.3] - 2024-03-12

### Other

- Resolve issue #4

- Resolve other issues


## [1.1.2] - 2024-03-12

### Other

- Weapon attack patch

- Resolve issue #8

- Resolve issue #8


## [1.1.1] - 2024-03-11

### Other

- Thief patch


## [1.1.0] - 2024-03-09

### Other

- Bit of logging

- Session should not do that

- Version


## [1.0.1] - 2024-03-07

### Other

- Prepared to become a package. all tests passed


## [1.0.0] - 2024-03-07

### 🚀 Features

- New action system for everyone!


### ⚙️ Core

- Core architecture

- Core + modern kinda finished


### 🚜 Refactor

- Refactoring and some ai improvements


### 🐛 Bug Fixes

- Fixed bugs with stimulator and weapon choice

- Fixes


### 📚 Documentation

- Dockerfile for good luck

- Dockerfile for good luck


### Other

- Polishing action system

- Skills - implemented

- State - aflame and flamethrower, proof of concept

- All states and state-based weapons - done!!

- Items - stimulator as a proof of concept - done!!

- Slowly and surely...

- Text system

- Modern!

- Team system, bugfixes

- Targeting system ()

- Adequate tartgeting system

- Damage accounting system

- Target type fixes

- Action rework (still needs revision)

- Grenade and Molotov

- Source rework (still gonna revise again)

- Revising many systems

- Deluxe release, yay!!

- Huge update:
- more weapons from modern
- some minor reworks of internal cycle
- items now in production!
- cows

- Imports

- Imports

- Merge remote-tracking branch 'origin/master'

- Remove debug prints

- Thief fix

- Flame final (i hope) fix

- +1 item, +2 skills and descriptions

- Armor rework, flame fix

- No pasyuk

- Scheduling and handling!

- More items!

- More items!

- Weapon static instanity

- Weapon static instanity

- More static instanity

- ContentManager fixed, yay

- Cd for thief

- Alchemists...

- Breaking, fixing and bending space-time

- Lets test, guys

- Bit by bit

- Architectural madness

- + mimic

- Working on message, timelines, events and publishing systems....

- Migration to publishing-subscription system

- More adequate patterns

- I should have done this before

- I should have done this before

- I should have done this before

- PEP

- Improving...

- Conventions...

- Conventions...

- Conventions...

- Migrating modern to new architecture

- Skills and states migrated, yay!!!!!

- Update TODO's

- Weapons

- Formulas

- Merge pull request #1 from Vezono/master

formulas
- Merge remote-tracking branch 'origin/feature/actionManager' into feature/actionManager

- More skills

- Enable rating

- Merge pull request #2 from Vezono/feature/actionManager

Feature/action manager
- Disable debug mode

- Thief dupe patch

- + inquisitor
+ attack range patch

- + approach patch

- + zombie
+ game end fix

- + Matchmaker refactor

- + 2 different matches

- + vegan naming convention

- + minor patches

- + minor patches

- + more minor patches

- + fixed chain
+ mimic reenabled

- + more minor fixes

- + more minor fixes

- + kuvalda

- + static stats for weapons

- + rethinking events

- + ninja fix

- + notifications and weaponry rework

- + started work on rats
+ grand fix of flame

- + skip fix

- No way, context is here!

- + readme
+ work on context

- + readme
+ work on context

- + readme
+ work on context

- Everything is fixed
+ ContentManager created
+ EventManager, SessionManager, EventManager are not singletons now
+ Context are now very powerful

- Cleanup

- Committing a cardinal sin

- Import rearrange

- .gitignore

- Giving ContentManager more power

- Registering items

- Silly

- Pack your shit and lets go

- Onedeved

- Dementia

- Secrets

- Enable ratings

- Why do we exist

- Enable autoupdate
- Enable autoupdate
- Add publishing
- Setup

- Edit setup.py
- Small fix

- God forgive me


## [a0.0.1] - 2023-05-30

### Other

- Foundation


<!-- generated by git-cliff -->
