class Weapon:
    id = 'None'
    name = 'None'
    description = 'Описание еще не написано.'
    ranged = False

    def __init__(self, energy_cost=2, cubes=2, damage_bonus=0, accuracy_bonus=0):
        self.energy_cost = energy_cost
        self.cubes = cubes
        self.damage_bonus = damage_bonus
        self.accuracy_bonus = accuracy_bonus

    def reload_text(self, source):
        if self.ranged:
            tts = f"🕓|{source.name} перезаряжается. " \
                  f"Энергия восстановлена до максимальной! ({source.max_energy})"
        else:
            tts = f"😤|{source.name}️ переводит дух. Энергия восстановлена до максимальной! ({source.max_energy})"
        return tts


class MeleeWeapon(Weapon):
    ranged = False


class RangedWeapon(Weapon):
    ranged = True
