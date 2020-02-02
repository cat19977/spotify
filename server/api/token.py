from flask import Blueprint, jsonify, request
from . import db
from .models import Token
from flask_cors import CORS, cross_origin
import sys
import json
from .songs import SongData

main = Blueprint('main', __name__)

@main.route('/add_token', methods=['GET','POST'])
def add_token():
    if request.method == 'POST':
        token = request.get_data()
        token = token.decode('utf-8')
        token_dict = json.loads(token) #consverts string dict to real dict
        
        #send token to database 
        send_token = Token(id = token_dict['token'])
        db.session.add(send_token)
        db.session.commit()
        
        return jsonify(token)
    else:
        return jsonify({"success": "yes"})

@main.route('/top-songs', methods=['GET'])
def songs():
    token = Token.query.first().id
    data.init_categories()
    data.set_top_songs()

    return jsonify({'token': 'success'})