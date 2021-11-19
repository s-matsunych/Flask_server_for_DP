from flask import Flask, request, current_app, redirect
from flask import send_file
import Parser
from Parser import Sequences as seq
# from werkzeug import secure_filename



HOST = 'http://127.0.0.1'
PORT = '10'


app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Ok CONECTION"


@app.route('/reed_file', methods=['GET', 'POST'])
def reed_file():
    if request.method == 'POST':
        file = request.files["file"]
        if file.filename != '':
            # file.save(file.filename)
            # return file.stream.read()
            seq = Parser.Sequences(file_name="sekvencie.txt")
            seq.file_to_DataFrame()
            print(seq.get_percent_gaps_in_columns())
            return {"data": seq.get_percent_gaps_in_columns()}
    return redirect(location=f'{HOST}:{PORT}/error_massage', code=500)


@app.route('/get_gaps_stat', methods=['GET'])
def get_gaps_stat():
    seq = Parser.Sequences(file_name="sekvencie.txt")
    seq.file_to_DataFrame()
    print(seq.get_percent_gaps_in_columns())
    return {"data": seq.get_percent_gaps_in_columns()}



@app.route('/error_massage')
def error_massage():
    with open("Error_server.html", 'r') as error_massage:
        massage = error_massage.read()
    return massage


if __name__ == '__main__':
    app.debug = True
    app.run(
        port=8080,)





