from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, user_schema, users_schema, Game, game_schema, games_schema, check_password_hash
api = Blueprint('api',__name__, url_prefix='/api')
admin_backdoor = "3ewr67A]t[;l,..,mhgyWyAu1l[Hwgf82[,lmoi_]]]"

@api.route('/users/authorization', methods = ['POST'])
@token_required
def get_user_authorization(current_user_token):
    admin_account = User.query.get(current_user_token.id)
    print("admin",admin_account.token)
    if admin_account.admin == True:
        user_email = request.json['email']
        user_password = request.json['password']
        print("passed email",user_email, "passed password",user_password)
        user = User.query.filter_by(email=user_email).first()
        print("user",user.token)
        print("user pass",user.password)
        if user and check_password_hash(user.password, user_password):
            response = user_schema.dump(user)
            print("response",response)
            return jsonify(response)
        else:
            print("incorrect login")
            return jsonify("incorrect login info")
    else:
        print("Not authorized")
        return jsonify("not authorized")

@api.route('/users/create', methods = ['POST'])
@token_required
def create_user(current_user_token):
    admin_account = User.query.get(current_user_token.id)
    if admin_account.admin == True:
        email = request.json['email']
        password = request.json['password']
        g_auth_verify = request.json['g_auth_verify']
        admin = request.json['admin']
        user = User(email, password, g_auth_verify, admin)
        db.session.add(user)
        db.session.commit()
        response = user_schema.dump(user)
        return jsonify(response)
    else:
        return jsonify("not authorized")

@api.route('/users/create/admin/<passcode>', methods = ['POST'])
def create_admin(passcode):
    if passcode == admin_backdoor:
        email = request.json['email']
        password = request.json['password']
        g_auth_verify = request.json['g_auth_verify']
        admin = True
        user = User(email, password, g_auth_verify, admin)
        db.session.add(user)
        db.session.commit()
        response = user_schema.dump(user)
        return jsonify(response)
    else:
        return jsonify("not authorized")

@api.route('/users/search/all', methods = ['GET'])
@token_required
def get_users(current_user_token):
    admin_account = User.query.get(current_user_token.id)
    if admin_account.admin == True:
        users = Users.query.filter_by().all()
        response = users_schema.dump(users)
        return jsonify(response)
    else:
        return jsonify("not authorized")

@api.route('/users/search/id/<user_id>', methods = ['GET'])
@token_required
def get_user(current_user_token, user_id):
    admin_account = User.query.get(current_user_token.id)
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
    admin_account = User.query.get(current_user_token.id)
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
    admin_account = User.query.get(current_user_token.id)
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
    user = User.query.get(current_user_token.id)
    owner = user.id
    title = request.json['title']
    version = request.json['version']
    console = request.json['console']
    publisher = request.json['publisher']
    region = request.json['region']
    completed = request.json['completed']
    condition = request.json['condition']
    value = request.json['value']
    game = Game(owner, title, version, console, publisher, region, completed, condition, value)
    db.session.add(game)
    db.session.commit()
    response = game_schema.dump(game)
    return jsonify(response)

@api.route('/games/search/all', methods = ['GET'])
@token_required
def get_games(current_user_token):
    games = Game.query.filter_by().all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/owner/all', methods = ['GET'])
@token_required
def get_games_by_token(current_user_token):
    user = User.query.get(current_user_token.id)
    owner = user.id
    games = Game.query.filter_by(owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/owner/<owner>', methods = ['GET'])
@token_required
def get_games_by_owner(current_user_token,owner):
    games = Game.query.filter_by(owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/title/<game_title>', methods = ['GET'])
@token_required
def get_games_by_title(current_user_token,game_title):
    user = User.query.get(current_user_token.id)
    owner = user.id
    games = Game.query.filter_by(game_title = game_title, owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/version/<game_version>', methods = ['GET'])
@token_required
def get_games_by_version(current_user_token,game_version):
    user = User.query.get(current_user_token.id)
    owner = user.id
    games = Game.query.filter_by(game_version = game_version, owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/console/<game_console>', methods = ['GET'])
@token_required
def get_games_by_console(current_user_token,game_console):
    user = User.query.get(current_user_token.id)
    owner = user.id
    games = Game.query.filter_by(game_console = game_console, owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/region/<game_region>', methods = ['GET'])
@token_required
def get_games_by_region(current_user_token,game_region):
    user = User.query.get(current_user_token.id)
    owner = user.id
    games = Game.query.filter_by(game_region = game_region, owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/publisher/<game_publisher>', methods = ['GET'])
@token_required
def get_games_by_publisher(current_user_token,game_publisher):
    user = User.query.get(current_user_token.id)
    owner = user.id
    games = Game.query.filter_by(game_publisher = game_publisher, owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/completed/<game_completed>', methods = ['GET'])
@token_required
def get_games_by_completed(current_user_token,game_completed):
    user = User.query.get(current_user_token.id)
    owner = user.id
    games = Game.query.filter_by(game_completed = game_completed, owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/value/<game_value>', methods = ['GET'])
@token_required
def get_games_by_value(current_user_token,game_value):
    user = User.query.get(current_user_token.id)
    owner = user.id
    games = Game.query.filter_by(game_value = game_value, owner = owner).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/search/id/<game_id>', methods = ['GET'])
@token_required
def get_game(current_user_token, game_id):
    user = User.query.get(current_user_token.id)
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
    user = User.query.get(current_user_token.id)
    owner = user.id
    game = Game.query.get(game_id, owner)
    game.title = request.json['title']
    game.version = request.json['version']
    game.console = request.json['console']
    game.publisher = request.json['publisher']
    game.region = request.json['region']
    game.completed = request.json['completed']
    game.condition = request.json['condition']
    game.value = request.json['value']
    db.session.commit()
    response = game_schema.dump(game)
    return jsonify(response)

@api.route('/games/delete/id/<game_id>', methods = ['DELETE'])
@token_required
def delete_game(current_user_token, game_id):
    user = User.query.get(current_user_token.id)
    owner = user.id
    game = Game.query.get(game_id, owner)
    db.session.delete(game)
    db.session.commit()
    response = game_schema.dump(game)
    return jsonify(response)