from flask import jsonify, make_response, request

from models.models import (add_favorite_movie, app, create_log,
                                         create_user,match_password)
from utilities.movie_search import search_movie
from utilities.jwt import encode,decode
from utilities import token_required
from exceptions import NotFoundException


@app.errorhandler(NotFoundException)
def handle_not_found(err):
    error  = {'message': err.message}
    return make_response(jsonify(error), err.status_code)



@app.route('/register',methods=['POST'])
def register():
    request_body = request.get_json()
    fullname = request_body['fullname']
    email =  request_body['email']
    passward = request_body['passward']
    user = create_user(fullname,email,passward)
    data = {'id':user.id,'name':user.fullname}
    return make_response(jsonify(data))

    
@app.route('/login',methods=['POST'])
def login():
    request_body = request.get_json()
    email = request_body['email']
    passward = request_body['passward']
    user = match_password(email,passward)
    if not user:
       error = {'message':'Passward Not Matched'}
       return make_response(jsonify(error),401)

    user_data = { 'id':user.id,'fullname':user.fullname}

    token = encode(user_data)
    data = {'token':token}
    return make_response(jsonify(data))

@app.route('/search',methods=['GET'])
@token_required
def search():
    token = request.headers['token']
    user_id = decode(token)['id']
    search_parms = request.args.get('q')
    page = int(request.args.get('page','1'))
    create_log(user_id,search_parms)
    movies = search_movie(search_parms,page)
    response = {'data':movies}
    return make_response(jsonify(response))
@app.route('/me/favourite',methods=['POST'])
@token_required
def favourite():
    request_body = request.get_json()
    token = request.headers['token']
    user_id = decode(token)['id']
    imdb_id = request_body['imdb_id']
    movies = add_favorite_movie(user_id,imdb_id)
    imdb_ids = [movie.imdb_id for movie in movies]
    response = {'data':imdb_ids}
    return make_response(jsonify(response))








if __name__ == '__main__':
    app.run(debug=True)