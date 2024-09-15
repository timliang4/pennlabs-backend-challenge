import os
import json

from app import app, db, DB_FILE

from models import *

def create_user():
    usr = User(username='josh')
    db.session.add(usr)
    db.session.commit()

def load_data():
    with open('clubs.json', 'r') as f:
        clubs = json.load(f)
        usr = User(username='mike')
        for club_dict in clubs:
            club = Club(code=club_dict['code'], name=club_dict['name'], 
                description=club_dict['description'])
            if (club_dict['code'] == 'locustlabs'):
                club.favorited_by.append(usr)
            elif club_dict['code'] == 'pppp':
                club.favorited_by.append(usr)
            db.session.add(club)
            for tag_name in club_dict['tags']:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                club.tags.append(tag)
        db.session.commit()

# No need to modify the below code.
if __name__ == "__main__":
    # Delete any existing database before bootstrapping a new one.
    LOCAL_DB_FILE = "instance/" + DB_FILE
    if os.path.exists(LOCAL_DB_FILE):
        os.remove(LOCAL_DB_FILE)

    with app.app_context():
        db.create_all()
        create_user()
        load_data()
