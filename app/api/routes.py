from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, user_schema, users_schema, Game, game_schema, games_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/users/create', methods = ['POST'])
#@token_required
def create_user():
    #admin_account = User.query.get(current_user_token)
    #if admin_account.admin == True:

    #else:
        #return jsonify("not authorized")
    email = request.json['email']
    password = request.json['password']
    g_auth_verify = request.json['g_auth_verify']
    admin = request.json['admin']
    user = User(email, password, g_auth_verify, admin)
    db.session.add(user)
    db.session.commit()
    response = user_schema.dump(user)
    return jsonify(response)

@api.route('/users/search/all', methods = ['GET'])
@token_required
def get_users(current_user_token):
    admin_account = User.query.get(current_user_token)
    if admin_account.admin == True:
        users = Users.query.filter_by().all()
        response = users_schema.dump(users)
        return jsonify(response)
    else:
        return jsonify("not authorized")

@api.route('/users/search/id/<user_id>', methods = ['GET'])
@token_required
def get_user(current_user_token, user_id):
    admin_account = User.query.get(current_user_token)
    if admin_account.admin == True:
        fan = current_user_token.token
        if fan == current_user_token.token:
            user = User.query.get(user_id)
            response = user_schema.dump(user)
            return jsonify(response)
        else:
            return jsonify({"message": "Valid Token Required"}),401
    else:
        return jsonify("not authorized")

@api.route('/users/update/id/<user_id>', methods = ['POST','PUT'])
@token_required
def update_user(current_user_token,user_id):
    admin_account = User.query.get(current_user_token)
    if admin_account.admin == True:
        user = User.query.get(user_id) 
        user.email = request.json['email']
        user.password = request.json['password']
        user.g_auth_verify = request.json['g_auth_verify']
        user.admin = request.json['admin']
        user = User(email, password, g_auth_verify, admin)
        db.session.commit()
        response = user_schema.dump(user)
        return jsonify(response)
    else:
        return jsonify("not authorized")

@api.route('/users/delete/id/<user_id>', methods = ['DELETE'])
@token_required
def delete_user(current_user_token, user_id):
    admin_account = User.query.get(current_user_token)
    if admin_account.admin == True:
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        response = user_schema.dump(user)
        return jsonify(response)
    else:
        return jsonify("not authorized")

@api.route('/games/create', methods = ['POST'])
@token_required
def create_game(current_user_token):
    user = User.query.get(current_user_token)
    owner = user.id
    title = request.json['title']
    version = request.json['version']
    publisher = request.json['publisher']
    region = request.json['region']
    completed = request.json['completed']
    status = request.json['status']
    value = request.json['value']
    game = Game(owner, title, version, publisher, region, completed, status, value)
    db.session.add(game)
    db.session.commit()
    response = game_schema.dump(game)
    return jsonify(response)

@api.route('/games/search/all', methods = ['GET'])
@token_required
def get_games(current_user_token):
    games = Games.query.filter_by().all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/owner/all', methods = ['GET'])
@token_required
def get_games_by_owner(current_user_token):
    user = User.query.get(current_user_token)
    owner = user.id
    games = Games.query.filter_by(owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/title/<game_title>', methods = ['GET'])
@token_required
def get_games_by_title(current_user_token,game_title):
    user = User.query.get(current_user_token)
    owner = user.id
    games = Game.query.filter_by(game_title = game_title, owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/version/<game_version>', methods = ['GET'])
@token_required
def get_games_by_version(current_user_token,game_version):
    user = User.query.get(current_user_token)
    owner = user.id
    games = Game.query.filter_by(game_version = game_version, owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/region/<game_region>', methods = ['GET'])
@token_required
def get_games_by_region(current_user_token,game_region):
    user = User.query.get(current_user_token)
    owner = user.id
    games = Game.query.filter_by(game_region = game_region, owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/publisher/<game_publisher>', methods = ['GET'])
@token_required
def get_games_by_publisher(current_user_token,game_publisher):
    user = User.query.get(current_user_token)
    owner = user.id
    games = Game.query.filter_by(game_publisher = game_publisher, owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/completed/<game_completed>', methods = ['GET'])
@token_required
def get_games_by_completed(current_user_token,game_completed):
    user = User.query.get(current_user_token)
    owner = user.id
    games = Game.query.filter_by(game_completed = game_completed, owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/value/<game_value>', methods = ['GET'])
@token_required
def get_games_by_value(current_user_token,game_value):
    user = User.query.get(current_user_token)
    owner = user.id
    games = Game.query.filter_by(game_value = game_value, owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/id/<game_id>', methods = ['GET'])
@token_required
def get_game(current_user_token, game_id):
    user = User.query.get(current_user_token)
    owner = user.id
    fan = current_user_token.token
    if fan == current_user_token.token:
        game = Game.query.get(game_id, owner)
        response = game_schema.dump(game)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

@api.route('/games/update/id/<game_id>', methods = ['POST','PUT'])
@token_required
def update_game(current_user_token,game_id):
    user = User.query.get(current_user_token)
    owner = user.id
    game = Game.query.get(game_id, owner)
    game.title = request.json['title']
    game.version = request.json['version']
    game.publisher = request.json['publisher']
    game.region = request.json['region']
    game.completed = request.json['completed']
    game.status = request.json['status']
    game.value = request.json['value']
    db.session.commit()
    response = game_schema.dump(game)
    return jsonify(response)

@api.route('/games/delete/id/<game_id>', methods = ['DELETE'])
@token_required
def delete_game(current_user_token, game_id):
    user = User.query.get(current_user_token)
    owner = user.id
    game = Game.query.get(game_id, owner)
    db.session.delete(game)
    db.session.commit()
    response = game_schema.dump(game)
    return jsonify(response)