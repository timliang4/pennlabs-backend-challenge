from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

DB_FILE = "clubreview.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE}"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

from models import *

@app.route("/")
def main():
    return "Welcome to Penn Club Review!"

@app.route("/api")
def api():
    return jsonify({"message": "Welcome to the Penn Club Review API!."})

@app.route("/api/clubs", methods=['GET'])
def allClubs():
    favoriteCounts = db.session.query(func.count(User.username)).\
        outerjoin(Club.favorited_by).group_by(Club.name).\
        order_by(Club.name).all()
    return jsonify(
        [
            {
                "code": club.code,
                "name": club.name, 
                "description": club.description, 
                "tags": [tag.name for tag in club.tags],
                "favorite_count": favoriteCount[0]
            }
            for club, favoriteCount in 
            zip(Club.query.order_by(Club.name).all(), favoriteCounts)
        ]
    )

@app.route("/api/clubs", methods=["POST"])
def newClub():
    try:
        body = request.get_json()
        code, name, description, tags = (body['code'], body['name'], 
            body['description'], body['tags'])
    except:
        return jsonifyErrorMsg("include code, name, description, and tags"), 500
    if Club.query.filter_by(code=code).first():
        return jsonifyErrorMsg("club code already used"), 500
    if Club.query.filter_by(name=name).first():
        return jsonifyErrorMsg("club name already used"), 500
    if not isListOfStrings(tags):
        return jsonifyErrorMsg("tags must be list of strings"), 500
    club = Club(code=code, name=name, description=description)
    db.session.add(club)
    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
        db.session.add(tag)
        club.tags.append(tag)
    try:
        db.session.commit()
    except:
        return jsonifyErrorMsg("cannot have duplicate tags"), 500
    return jsonify(
        {
            "code": club.code,
            "name": club.name,
            "description": club.description,
            "tags": [tag.name for tag in club.tags],
            "favorite_count": club.favorited_by.count()
        }
    )

@app.route("/api/clubs", methods=["PATCH"])
def updateClub():
    try:
        body = request.get_json()
        code, newCode, newName, newDescription, newTags = (body['code'], 
            body['newCode'], body['newName'], 
            body['newDescription'], body['newTags'])
    except:
        return jsonifyErrorMsg("include club code and new parameters"), 500
    print(code)
    print(newCode)
    club = Club.query.get(code)
    if not club:
        return jsonifyErrorMsg("invalid club code"), 500
    if code != newCode and Club.query.filter_by(code=newCode).first():
        return jsonifyErrorMsg("new code already in use"), 500
    if club.name != newName and Club.query.filter_by(name=newName).first():
        return jsonifyErrorMsg("new name already in use"), 500
    if not isListOfStrings(newTags):
        return jsonifyErrorMsg("tags must be list of strings"), 500
    club.code = newCode
    club.name = newName
    club.description = newDescription
    club.tags.clear()
    for tag_name in newTags:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        club.tags.append(tag)
    try:
        db.session.commit()
    except:
        return jsonifyErrorMsg("cannot have duplicate tags"), 500
    return jsonify(
        {
            "code": club.code,
            "name": club.name,
            "description": club.description,
            "tags": [tag.name for tag in club.tags],
            "favorite_count": club.favorited_by.count()
        }
    )

@app.route("/api/clubs/search", methods=['GET'])
def searchClubs():
    try:
        body = request.get_json()
        name = body['name']
    except:
        return jsonifyErrorMsg("provide name to search for"), 500
    favoriteCounts = db.session.query(func.count(User.username)).\
        outerjoin(Club.favorited_by).group_by(Club.name).\
        filter(Club.name.like(f'%{name}%')).order_by(Club.name).all()
    return jsonify(
        [
            {
                "code": club.code, 
                "name": club.name,
                "description": club.description,
                "tags": [tag.name for tag in club.tags],
                "favorite_count": favoriteCount[0]
            }
            for club, favoriteCount in 
            zip(Club.query.filter(Club.name.like(f'%{name}%')).
                order_by(Club.name).all(),
                favoriteCounts)
        ]
    )

@app.route("/api/user", methods=['GET'])
def getUserInfo():
    try:
        body = request.get_json()
        username = body['username']
    except:
        return jsonifyErrorMsg("provide username"), 500
    user = User.query.get(username)
    if not user:
        return jsonifyErrorMsg("unknown username"), 404
    return jsonify(
        {
            "username": user.username
        }
    )

@app.route("/api/user/favorite", methods=["POST"])
def addFavorite():
    try:
        body = request.get_json()
        username, code = body['username'], body['code']
    except:
        return jsonifyErrorMsg('include username and club code to favorite'), 500
    user = User.query.filter_by(username=username).first()
    club = Club.query.filter_by(code=code).first()
    if not user:
        return jsonifyErrorMsg('unknown username'), 404
    if not club:
        return jsonifyErrorMsg('unknown club code'), 404
    club.favorited_by.append(user)
    try:
        db.session.commit()
    except:
        return jsonifyErrorMsg('club already favorited'), 505
    return jsonify(
        {
            "username": user.username,
            "favorite_clubs": [club.name for club in user.favorite_clubs]
        }
    )
    

@app.route("/api/tags", methods=["GET"])
def tags():
    tagCounts = db.session.query(Tag.name, func.count(Club.code)).\
        join(Tag.clubs).group_by(Tag.name).all()
    return jsonify(
        [
            {
                "tag_name": name,
                "number_of_clubs": number_of_clubs
            }
            for name, number_of_clubs in tagCounts
        ]
    )

def jsonifyErrorMsg(msg):
    return jsonify({"error": msg})

def isListOfStrings(x):
    if isinstance(x, str):
        return False
    try:
        if all(isinstance(y, str) for y in x):
            return True
    except TypeError:
        pass
    return False

if __name__ == "__main__":
    app.run()
