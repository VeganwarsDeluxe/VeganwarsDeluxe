from mongoengine import Document, StringField, IntField, EmbeddedDocumentListField, EmbeddedDocumentField

from rpg.db.Item import Item
from rpg.db.Skill import Skill
from rpg.db.Weapon import Weapon
from rpg.texts import CASTLE_ID_TO_TEXT, ACTION_ID_TO_TEXT


class User(Document):
    # Core info
    id = IntField(primary_key=True)
    name = StringField(default="Не установил(а) игровое имя")
    username = StringField(default="ЮзернеймНеНайден")

    # RPG stats
    castle = StringField(default="outsider")
    level = IntField(default=1)
    exp = IntField(default=0)
    upgrade_points = IntField(default=0)

    stamina = IntField(default=5)
    max_stamina = IntField(default=5)

    weapon = EmbeddedDocumentField(Weapon, default=None)

    # Game entity stats
    hp = IntField(default=3)
    max_hp = IntField(default=3)

    energy = IntField(default=5)
    max_energy = IntField(default=5)

    damage_threshold = IntField(default=5)

    # Inventories and collections
    money = IntField(default=0)
    money_bags = IntField(default=0)

    max_skills = IntField(default=2)
    skills = EmbeddedDocumentListField(Skill)
    items = EmbeddedDocumentListField(Item)

    # Temporary variables
    current_action = StringField(default="rest")
    attack_target = StringField(default=None)

    def get_profile_text(self):
        current_state = ACTION_ID_TO_TEXT.get(self.current_action)
        if self.current_action == 'attack':
            current_state = f'{current_state} {CASTLE_ID_TO_TEXT.get(self.attack_target)}'

        profile = f'{self.name}, воин {CASTLE_ID_TO_TEXT.get(self.castle)}\n' \
                  f'🏅Уровень: {self.level}\n' \
                  f'🧬Очки навыков: {self.upgrade_points} (/lvlup)\n' \
                  f'🔥Опыт: {self.exp}/{self.max_exp} {self.exp_ratio}%\n' \
                  f'💰{self.money} 👝{self.money_bags}\n' \
                  f'🔋Выносливость: {self.stamina}/{self.max_stamina}\n' \
                  f'{"♥️"*self.hp}|ХП: {self.hp}/{self.max_hp}\n' \
                  f'⚔️Оружие: {self.weapon}\n' \
                  f'Состояние: {current_state}\n' \
                  f'❓Информация о расовой способности: /special_ability'
        return profile

    @property
    def max_exp(self):
        return round(pow((self.level * 5), 1.9))

    @property
    def exp_ratio(self):
        return (self.exp / self.max_exp) * 100

    def get_item(self, object_code):
        for item in self.items:
            if item.object_code == object_code:
                return item
