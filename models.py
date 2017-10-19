from mongoengine import *
from dotenv import load_dotenv, find_dotenv
import os
import datetime

load_dotenv(find_dotenv())

# connect to the database
connect(
    os.getenv('DBNAME'),
    username = os.getenv('DB_USERNAME'),
    password = os.getenv('DB_PASSWORD'),
    host = os.getenv('MONGO_URL'),
    port = int(os.getenv('PORT'))
)

DIFFICULTY = ('Easy', 'Medium', 'Hard', 'Expert')
    
class Rating(EmbeddedDocument):
    zero = IntField()
    one = IntField()
    two = IntField()
    three = IntField()
    four = IntField()
    five = IntField()
    avg = FloatField()
    def clean(self):
        self.zero = 0
        self.one = 0
        self.two = 0
        self.three = 0
        self.four = 0
        self.five = 0
        self.avg = 0
        
class Meal(Document):
    name = StringField(required=True)
    difficulty = StringField(choices = DIFFICULTY)
    total_cooking_time = StringField()
    ingredients = ListField(StringField())
    recipe = ListField(StringField())
    ratings = EmbeddedDocumentField(Rating, default=Rating)
    tags = ListField(StringField())
    img_url = URLField()
    def clean(self):
        self.tags = [self.name]

class Meal_Plan(Document):
    viewable = BooleanField(default=False)
    name = StringField()
    meal_id_list = ListField(ReferenceField(Meal, reverse_delete_rule=PULL))
    ratings = EmbeddedDocumentField(Rating, default=Rating)
    duration = IntField()
    tags = ListField(StringField())
    def clean(self):
        self.tags = []

class User(Document):
    email = EmailField(required=True, unique=True)
    name = StringField(required=True, max_length=50)
    password = StringField(required=True, max_length=200)
    verified = BooleanField(default=False)
    meal_plan_ids = ListField(ReferenceField(Meal_Plan, reverse_delete_rule=PULL))
    current_meal_plan = ReferenceField(Meal_Plan, reverse_delete_rule=PULL)
    meal_plan_start_date = DateTimeField()
    def clean(self):
        self.current_meal_plan = None
        self.start_date = datetime.datetime.now()