from mongoengine import *


class FoodItem(Document):
    src = StringField()
    title = StringField()
    description = StringField()