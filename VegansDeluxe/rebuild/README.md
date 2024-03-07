# Модуль Rebuid
Наразі це просто коллекція контенту з Rebuild версії. Контент імпортується з `rebuild/__init__.py`.

```python
from VegansDeluxe.rebuild import Knife
from VegansDeluxe.core.Entities import Entity

player = Entity()
player.weapon = Knife(player.session_id, player.id)
```