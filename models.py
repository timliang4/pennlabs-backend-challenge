from app import db

tags = db.Table('tags',
    db.Column('club_code', db.String(64), 
        db.ForeignKey('club.code'), primary_key=True),
    db.Column('tag_id', db.String(64), 
        db.ForeignKey('tag.name'), primary_key=True)
)

favorites = db.Table('favorites',
    db.Column('club_code', db.String(64), 
        db.ForeignKey('club.code'), primary_key=True),
    db.Column('user_username', db.String(64), 
        db.ForeignKey('user.username'), primary_key=True)
)

class Club(db.Model):
    code = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.Text)
    tags = db.relationship('Tag', secondary=tags, lazy='joined', 
        backref=db.backref('clubs', lazy='dynamic'))
    favorited_by = db.relationship('User', secondary=favorites, 
        lazy='dynamic', backref=db.backref('favorite_clubs', lazy='dynamic'))

class Tag(db.Model):
    name = db.Column(db.String(64), primary_key=True)

class User(db.Model):
    username = db.Column(db.String(64), primary_key=True)
