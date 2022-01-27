from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DB_PROTOCOL = 'mysql'
DB_USER = 'root'
DB_PASSWORD = ''
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'movie-search'

app = Flask('movieproject')

app.config['SQLALCHEMY_DATABASE_URI'] = f'{DB_PROTOCOL}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = False