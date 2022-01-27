
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from core import app
from exceptions import NotFoundException


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fullname = db.Column(db.String(200), nullable=False)
    
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    password = db.Column(db.String(128), nullable=False)

    
    movies = db.relationship('FavoriteMovie', backref='user', lazy='joined')

    def __init__(self, fullname, email, password) -> None:
        super().__init__()
        self.fullname = fullname
        self.email = email
        self.password = password 


class FavoriteMovie(db.Model):
    __tablename__ = 'favorite_movie'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    imdb_id = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, imdb_id) -> None:
        super().__init__()
        self.user_id = user_id
        self.imdb_id = imdb_id


def create_user(fullname, email, password):
    user = User(fullname, email, password)

    db.session.add(user)
    db.session.commit()

    return user


def find_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user


def match_password(email, password):
    user = find_user_by_email(email)
    if not user:
        raise NotFoundException('User with email')
    
    return user if user.password==password else None
def movie_already_exist(imdb_id):
    movie = FavoriteMovie.query.filter_by(imdb_id=imdb_id).first()
    
    return movie

def add_favorite_movie(user_id, imdb_id):
    movie = movie_already_exist(imdb_id)
    user = User.query.filter_by(id=user_id).first()
    
    if not movie:
        fav_movie = FavoriteMovie(user_id, imdb_id)

        
        user.movies.append(fav_movie)

        db.session.add(user)
        db.session.commit()
    return user.movies
    
class SearchLog(db.Model):
    __tablename__ = 'search_log'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    query = db.Column(db.Text)

    def __init__(self, user_id, query) -> None:
        super().__init__()
        self.user_id = user_id
        self.query = query


def create_log(user_id, query):
    log = SearchLog(user_id, query)

    db.session.add(log)
    db.session.commit()

    return log


