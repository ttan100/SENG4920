# code for mongodb

from flask import Flask, jsonify, request, json, abort, session, redirect, render_template, \
     url_for, Response, flash
from flask_pymongo import PyMongo
from flask_restplus import Resource
from bson import json_util
from bson.objectid import ObjectId
from models import *

app = Flask(__name__)

# dumps mongo data object as json
def toJson(data):
    return json.dumps(data, default=json_util.default)

# test that the index uri works
@app.route('/')
def index():
#    mongo.db.users.create_index("email", unique=True)
    meals = Meal.objects.as_pymongo()
    return render_template('index.html', meals=meals)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            login_user = User.objects.get(email=request.form['email'])
            if login_user.password != request.form['pass']:
                error = 'Incorrect password, try again.'
            else:
                session['session_user'] = login_user.name
                session['session_userid'] = str(login_user.id)
                flash('You were successfully logged in')
                return redirect(url_for('index'))
        except:
            flash('User does not exist')

    return render_template('login.html', error=error)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Check if user exists
        existing_user = User._get_collection().find_one({'email' : request.form['email']})

        # If not found, then add user into the database
        if existing_user is None:
            user = User()
            user.email=request.form['email']
            user.name=request.form['name']
            user.password=request.form['pass']
            user.save()
            
            # Automatically login, for now no confirmation email
            #session['session_user'] = login_user.name
            return redirect(url_for('index'))

        # If there already is an existing user, tell them!
        return 'That email is already being used!'

    # If it's a get method, render register.html
    return render_template('register.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('session_user', None)
    session.pop('session_userid', None)
    flash('You have been logged out!')
    return redirect(url_for('index'))

@app.route('/my_meal_plan', methods=['GET'])
def my_meal_plan():
    # my meal plan only appears if you are logged in, checked in index.html

    # Firstly get the user
    user = User.objects(id=ObjectId(session['session_userid'])).get();
    
    saved_meal_plans = []
    for mp in user.meal_plan_ids:     
        saved_meal_plans.append(Meal_Plan.objects(id=mp.id).get())

    # Try and see if there's a current meal plan
    try:
        current_meal_plan = Meal_Plan.objects(id=user.current_meal_plan).get()
        print(current_meal_plan)    
        return render_template('my_meal_plan.html', user=user, saved_meal_plans=saved_meal_plans, current_meal_plan=current_meal_plan)
    except:
    
    # if not, don't worry! just don't return it
        flash('No current meal plan')
        return render_template('my_meal_plan.html', user=user, saved_meal_plans=saved_meal_plans)
    

@app.route('/meals/<meal_id>', methods=['GET'])
def get_meal(meal_id):
    return render_template('meal.html', meal=Meal.objects(id=meal_id).get())
    
@app.route('/meals', methods=['POST'])
def add_meal():
    ingredients = [y for y in (x.strip() for x in request.form['ingredients'].split('--')) if y]
    recipe = [y for y in (x.strip() for x in request.form['recipe'].split('--')) if y]

    meal = Meal()
    meal.name = request.form['name']
    meal.cuisine = request.form['cuisine']
    meal.difficulty = request.form['difficulty']
    meal.total_cooking_time = request.form['total_cooking_time']
    meal.ingredients = ingredients
    meal.recipe = recipe
    meal.img_url = request.form['img_url']
    return meal.save().to_json()
    
# patch ratings for a meal
@app.route('/meals/<meal_id>', methods=['PATCH'])
def update_field(meal_id):
    meal = update_ratings(meal_id, request.form['patch_field'])
    if meal:
        return Response(status=200)

def update_ratings(meal_id, rating):
    if rating == "zero":
        return Meal.objects(id=meal_id).update(inc__ratings__zero=1)
    elif rating == "one":
        return Meal.objects(id=meal_id).update(inc__ratings__one=1)
    elif rating == "two":
        return Meal.objects(id=meal_id).update(inc__ratings__two=1)
    elif rating == "three":
        return Meal.objects(id=meal_id).update(inc__ratings__three=1)
    elif rating == "four":
        return Meal.objects(id=meal_id).update(inc__ratings__four=1)
    else:
        return Meal.objects(id=meal_id).update(inc__ratings__five=1)

@app.route('/meals/<meal_id>', methods=['DELETE'])
def delete_meal(meal_id):    
    deletedItem = Meal.objects(id = meal_id).delete()
    if deletedItem:
        return Response(status=204)
    else:
        abort(404)

# user data section    
@app.route('/users', methods=['GET'])
def get_all_users():
    return User.objects.all().to_json()
    
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    return User.objects(id = user_id).to_json()

# only does update for verification and meal plan adding    
@app.route('/users/<user_id>', methods=['PATCH'])
def verify_user(user_id):
    if request.form['patch'] == 'verified':
        result = User.objects(id = user_id).update(set__verified=True)
    else:    
        meal_plans_id = [y for y in (x.strip() for x in request.form['meal_plan_ids'].split('--')) if y]
        result = User.objects.update(set__meal_plans_id=meal_plans_id)
    if result:
        return Response(status=200)
    else:
        abort(404)
    
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    deletedItem = User.objects(id=user_id).delete()
    if deletedItem:
        return Response(status=204)
    else:
        return abort(404)

# meal plan data section    
@app.route('/meal_plans', methods=['GET'])
def get_meal_plans():
    return Meal_Plan.objects.all().to_json()

@app.route('/meal_plans/<meal_plan_id>', methods=['GET'])
def get_meal_plan(meal_plan_id):
    return User.objects(id = user_id).to_json()

@app.route('/meal_plans', methods=['POST'])
def add_meal_plan():
    meal_ids = [ObjectId(y) for y in (x.strip() for x in request.form['meal_ids'].split('--')) if y]
    meal_plan = Meal_Plan()
    meal_plan.name = request.form['name']
    meal_plan.meal_id_list = meal_ids
    meal_plan.duration = request.form['duration']
    meal_plan.start_date = request.form['start_date']
    meal_plan.save()
    user = User.objects(id = ObjectId(session['session_userid'])).get()
    user.meal_plan_ids.append(meal_plan.id)
    user.update(set__meal_plan_ids=user.meal_plan_ids)
    return redirect(url_for('index'))


@app.route('/meal_plans/<meal_plan_id>', methods=['PATCH'])
def modify_meal_plan(meal_plan_id):
    meal_ids = [y for y in (x.strip() for x in request.form['meal_ids'].split('--')) if y]    
    result = Meal_Plan.objects(id = meal_plan_id).update(set__meal_plans_id=meal_ids)
    if result:
        return Response(status=200)
    else:
        abort(404)
    
if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True)
