from flask import Flask, render_template, send_file, request
from flask_cors import CORS
from flask_restful import Api
import os
import secrets

from stegano import Stegano

# init object flask
app = Flask(__name__)

# init object flask restfull
api = Api(app)

# init cors
CORS(app)

@app.route("/")
def main():
    return render_template("indexx.html")

@app.route("/download")
def download():
    return send_file(os.path.join('./audio/stegano-1BNvpg-Cemagi.wav'), as_attachment=True)

@app.route("/hide", methods=["POST"])
def hide():
    text = request.files['text']
    wav = request.files['wav']

    text.save(text.filename)
    unique = secrets.token_urlsafe(4)
    wav.save(os.path.join('./audio/',unique+'-'+wav.filename))
    Stegano.hide(file_to_hide=text.filename, audio_file_for_hiding=os.path.join('./audio/',unique+'-'+wav.filename))
    os.remove(os.path.join('./audio/',unique+'-'+wav.filename))
    return send_file("output.wav")

@app.route("/retrieve", methods=["POST"])
def retrieve():
    wav = request.files['wav']
    res = {"hiddenText": str(Stegano.retrieve(wav.filename))}
    return res

if __name__=='__main__':
    app.run()
