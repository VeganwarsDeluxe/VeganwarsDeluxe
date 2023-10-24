import random
import string
from rpg.texts import RECIPE_COLOR_TO_NAME

from mongoengine import EmbeddedDocument, StringField, IntField, Document, DoesNotExist


recipe_emoji = {
    'red': '📕',
    'green': '📗',
    'blue': '📘'
}


def generate_object_code():
    while True:
        code = ''.join(random.choice(string.ascii_uppercase) for _ in range(5))
        try:
            object_code = ObjectCode.objects.get(code=code)
            continue
        except DoesNotExist:
            object_code = ObjectCode(code=code)
            object_code.save()
            return code


class ObjectCode(Document):
    code = StringField(primary_key=True)


def create_item(name="Предмет", emoji="❔", description="Описание предмета.", type="item"):
    item = Item(object_code=generate_object_code())
    item.name = name
    item.emoji = emoji
    item.description = description
    item.type = type
    return item


def create_unscroll():
    item = Unscroll(object_code=generate_object_code())
    return item


def create_recipe(color):
    item = Recipe(object_code=generate_object_code())
    item.color = color
    item.emoji = recipe_emoji.get(color, '📔')
    item.name = RECIPE_COLOR_TO_NAME.get(color, 'Странный рецепт')
    return item


class Item(EmbeddedDocument):
    object_code = StringField()
    emoji = StringField(default="❔")
    name = StringField(default="Предмет")
    type = StringField(default="item")
    description = StringField(default="Описание предмета.")

    meta = {'allow_inheritance': True}


class Unscroll(Item):
    emoji = StringField(default="🗞")
    name = StringField(default="Неопознанный свиток")
    type = StringField(default="unscroll")
    description = StringField(default="Свиток неизвестной способности. Посетите лавку в замке, "
                                      "чтобы расшифровать его.")


class Scroll(Item):
    object_code = StringField()
    emoji = StringField(default="📜")
    name = StringField(default="Свиток")
    type = StringField(default="scroll")
    description = StringField(default="Свиток.")

    skill = StringField()
    level = IntField(default=1)


class Recipe(Item):
    object_code = StringField()
    emoji = StringField(default="❔")
    name = StringField(default="📔|Рецепт")
    type = StringField(default="recipe")
    description = StringField(default="Рецепт. Посетите лавку в замке, "
                                      "чтобы расшифровать его.")

    color = StringField()


class DefinedRecipe(Item):
    object_code = StringField()
    emoji = StringField(default="❔")
    name = StringField(default="📔|Рецепт после обработки.")
    type = StringField(default="defined_recipe")
    description = StringField(default="Рецепт.")

    color = StringField()
    weapon = StringField()
