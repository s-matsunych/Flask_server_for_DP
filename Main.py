# Tu skusam co vie FLASK, ale na moje veľké prekvapenie tento kód funguje
import logging

from flask import Flask, request, current_app, redirect, session as session_f, jsonify
from Redis_I import Redis_data
import Parser
from Parser import Sequences as seq
import os

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
import datetime
from flask_cors import CORS

HOST = 'http://127.0.0.1'
PORT = '10'

app = Flask(__name__)
CORS(app)
logging.getLogger('flask_cors').level = logging.DEBUG
app.config["JWT_SECRET_KEY"] = os.urandom(20).hex()
jwt = JWTManager(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=11)
redis_data = Redis_data()


@app.route('/')
def hello_world():
    return "Ok CONECTION"


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = os.urandom(20).hex()  # Generate user ID
    access_token = create_access_token(identity=login)
    return jsonify(access_token=access_token)


@app.route('/test_token', methods=['GET'])
@jwt_required()
def test_token():
    current_user_id = get_jwt_identity()
    print(type(current_user_id))
    return jsonify(current_user_id)


@app.route('/reed_file', methods=['GET', 'POST'])
@jwt_required()
def reed_file():
    if request.method == 'POST':
        file = request.files["file"]
        if file.filename != '':
            data = Parser.Sequences.read_file_from_request(file.stream.read().decode("utf-8"))
            redis_data.set_data(user_id=get_jwt_identity(), data=data)
            return {"data": data}
    return redirect(location=f'{HOST}:{PORT}/error_massage', code=500)


@app.route('/get_heatmap_seq', methods=['GET', 'POST'])
@jwt_required()
def get_heatmap_seq():
    x1 = int(request.args.get("x1"))
    x2 = int(request.args.get("x2"))
    y1 = int(request.args.get("y1"))
    y2 = int(request.args.get("y2"))
    data = redis_data.get_data(get_jwt_identity())
    return {"data": Parser.Sequences.get_heatmap_full_data(x=(x1, x2), y=(y1, y2), data=data)}


@app.route('/get_gaps_stat', methods=['GET'])
@jwt_required()
def get_gaps_stat():
    data = redis_data.get_data(get_jwt_identity())
    char = request.args.get("char")
    print(char)
    return jsonify({"data": Parser.Sequences.get_percent_gaps_in_columns(data=data, element=char),
                    "unique_characters": Parser.Sequences.get_unique_characters(sequences=data)})


@app.route('/get_base_statistics', methods=['GET'])
@jwt_required()
def get_base_statistics():
    data = redis_data.get_data(get_jwt_identity())
    return {"data": Parser.Sequences.calculate_base_statistics(seqs=data)}


@app.route('/rm_user_from_redis', methods=['GET'])
@jwt_required()
def rm_user_from_redis():
    redis_data.rm_data(get_jwt_identity())
    return jsonify('Ok')


@app.route('/error_massage')
def error_massage():
    with open("Error_server.html", 'r') as error_massage:
        massage = error_massage.read()
    return massage


if __name__ == '__main__':
    app.debug = True
    app.run(
        port=8080, )
