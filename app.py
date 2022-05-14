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

@app.route("/hide", methods=["POST"])
def hide():
    text = request.files['text']
    wav = request.files['wav']

    unique = secrets.token_urlsafe(4)
    textDir = os.path.join('/var/www/stegano-rindik/static/text/',unique+'-'+text.filename)
    wavDir = os.path.join('/var/www/stegano-rindik/static/audio/',unique+'-'+wav.filename)
    outputFilename = 'stegano-'+unique+'-'+wav.filename
    outputDir = os.path.join('/var/www/stegano-rindik/static/output/',outputFilename)
    text.save(textDir)
    wav.save(wavDir)
    Stegano.hide(file_to_hide=textDir, audio_file_for_hiding=wavDir, output=outputFilename)
    os.remove(wavDir)
    return send_file(outputDir)

@app.route("/retrieve", methods=["POST"])
def retrieve():
    wav = request.files['wav']
    wavDir = os.path.join('/var/www/stegano-rindik/static/audio-stegano/', wav.filename)
    wav.save(wavDir)
    res = Stegano.retrieve(wavDir)
    os.remove(wavDir)
    return res

if __name__=='__main__':
    app.run()
