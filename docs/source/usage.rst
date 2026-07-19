Usage
=====

.. _installation:

Installation
------------

To use Deluxe engine, first install it using pip:

.. code-block:: console

   (.venv) $ pip3 install git+https://onedev.gts.org.ua/vezono/vegans-deluxe#egg=VegansDeluxe

Currently, we do not distribute our library on pypi.org. Yet.

If for some reason you need to install a version from different branch (ex. dev):

.. code-block:: console

   (.venv) $ pip3 install git+https://onedev.gts.org.ua/vezono/vegans-deluxe@dev#egg=VegansDeluxe

Then, you must create an Engine instance.

.. code-block:: python3

    from VegansDeluxe.core import Engine
    engine = Engine()

As simple as that. At this point, the Engine is ready to be used,
and content is ready to be loaded. For more, read the Implementation chapter.

Implementation
------------

Implementing is one of the main purposes of the Engine.
However, if you wish to implement your own VeganWars game, you must adhere
to very arbitrary conventions that are not well represented in the engine.

However, even if you just wish to write content expansions, it would still
help to read these briefly to have an understanding of the engine.

.. toctree::

   elements
   implementing/event_system
   implementing/content_system
   implementing/match_flow

Modding
------------

Deluxe is meant to be modded since the inception. Writing a content expansion
for the Deluxe Engine, you write it for all VeganWars Deluxe implementations.
Whether you play in Telegram, on Web, on PC or anywhere else.

.. toctree::

   modding/item
   modding/state
   modding/skill
   modding/weapon
   modding/npc
   modding/match