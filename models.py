from mongoengine import *
from bson import ObjectId
from dotenv import load_dotenv, find_dotenv
import os

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
    cuisine = StringField()
    difficulty = StringField(choices = DIFFICULTY)
    total_cooking_time = StringField()
    ingredients = ListField(StringField())
    recipe = ListField(StringField())
    ratings = EmbeddedDocumentField(Rating, default=Rating)
    img_url = URLField()

class Meal_Plan(Document):
    viewable = BooleanField(default=False)
    name = StringField()
    meal_id_list = ListField(ReferenceField(Meal, reverse_delete_rule=PULL))
    duration = IntField()
    start_date = DateTimeField()
    def clean(self):
        self.start_date = datetime.now()

class User(Document):
    email = EmailField(required=True, unique=True)
    name = StringField(required=True, max_length=50)
    password = StringField(required=True, max_length=200)
    verified = BooleanField(default=False)
    meal_plans_id = ListField(ReferenceField(Meal_Plan, reverse_delete_rule=PULL))
