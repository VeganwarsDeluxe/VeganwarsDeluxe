from mongoengine import Document, StringField, IntField


class Player(Document):
    id = IntField(primary_key=True)
    name = StringField(default='Unknown')
    username = StringField(default='@none')
    rating = IntField(default=1000)
    money = IntField(default=0)
