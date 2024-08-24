import VegansDeluxe.core
import VegansDeluxe.rebuild
import VegansDeluxe.deluxe

from VegansDeluxe.core.ContentManager import content_manager

all_actions = []

for _, actions in content_manager.action_map.items():
    all_actions.extend(actions)

for action in all_actions:
    print(f"{action.id}: {action.priority}")
