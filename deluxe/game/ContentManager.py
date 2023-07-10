from core.Weapons.Weapon import Weapon
from core.States.State import State
import modern
from core.Skills.Skill import Skill

from typing import Optional


class ContentManager:
    def __init__(self):
        self.all_skills = {skill.id: skill for skill in modern.all_skills}
        self.all_weapons = {weapon.id: weapon for weapon in modern.all_weapons}
        self.default_skill = State
        self.default_weapon = Weapon

    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """
        Retrieve a skill by its ID.
        If no skill is found, return a default skill.
        """
        return self.all_skills.get(skill_id, self.default_skill)

    def get_weapon(self, weapon_id: str) -> Optional[Weapon]:
        """
        Retrieve a weapon by its ID.
        If no weapon is found, return a default weapon.
        """
        return self.all_weapons.get(weapon_id, self.default_weapon)
