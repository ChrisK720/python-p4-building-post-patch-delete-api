#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():

    games = []
    for game in Game.query.all():
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
        }
        games.append(game_dict)

    response = make_response(
        games,
        200
    )

    return response

@app.route('/games/<int:id>', methods=['GET','DELETE'])
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    if not game:
        return make_response({'message':f'There is no game with an id of {id}'},404)
    
    if request.method == 'GET':
        game_dict = game.to_dict()

        response = make_response(
            game_dict,
            200
        )
    
        
        

    return response



@app.route('/users')
def users():

    users = []
    for user in User.query.all():
        user_dict = user.to_dict()
        users.append(user_dict)

    response = make_response(
        users,
        200
    )

    return response

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    reviews = Review.query.all()
    if not reviews:
        return make_response({'message':'There are no reviews'})
    if request.method == 'GET':
        reviews_to_return = [review.to_dict() for review in reviews]
        return make_response(reviews_to_return,200)
    elif request.method == 'POST':
        new_review = Review(
            score= request.form.get('score'),
            comment= request.form.get('comment'),
            game_id= request.form.get('game_id'),
            user_id= request.form.get('user_id')
        )

        db.session.add(new_review)
        db.session.commit()
        
        review_dict = new_review.to_dict()
        return make_response(review_dict, 201)

@app.route('/reviews/<int:id>', methods=['GET','DELETE','POST','Patch'])
def review_by_id(id):
    review = Review.query.filter_by(id = id).first()
    if not review:
        return make_response({'message':f'There is no review with an id of {id}'}, 404)
    if request.method == 'GET':
        return make_response(review.to_dict(),200)
    elif request.method == 'DELETE':
        db.session.delete(review)
        db.session.commit()
        response = {
            'successfuly_deleted':True,
            'message':'review has been deleted'
        }
        return make_response(response,200)
    # I want to do a patch
    # I need to use the review which is the specific review
    # then I need acces the data in the request
    # update the review with it
    # commit the cahnges then return the updated review in a JSON response
    elif request.method == 'PATCH':
        # setattr(object, attribute, value)
        # we use setattr because we do not know which fields are being updated from the frontend very important
        for attr in request.form:
            setattr(review,attr,request.form.get(attr))
        db.session.commit()
        review_dict = review.to_dict()
        return make_response(review_dict,200)
        



if __name__ == '__main__':
    app.run(port=5555, debug=True)
