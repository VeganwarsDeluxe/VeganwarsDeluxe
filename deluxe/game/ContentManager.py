import modern
from core.Entities.Entity import Entity
from core.Sessions.Session import Session
from core.Skills.Skill import Skill


class ContentManager:
    def __init__(self):
        self.session = Session()
        self.entity = Entity(self.session)

    def get_skill(self, skill_id):
        skills = list(filter(lambda s: s.id == skill_id, modern.all_skills))
        return skills[0] if skills else Skill

    def get_weapon(self, weapon_id):
        weapon_id = int(weapon_id)
        weapons = list(filter(lambda w: w.id == weapon_id, modern.all_weapons))
        return weapons[0] if weapons else modern.Fist
