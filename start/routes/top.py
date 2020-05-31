from start import app
from flask import render_template, request
import urllib.request as urequest
from .settings import vocabulary

@app.route('/')
@app.route('/index')
def index():
    lngRows = [["lv", "ru"], ["en", "ee"], ["lt", "pl"]]
    return render_template('languages.html', title='Select language', lngRows=lngRows)

@app.route('/direction/')
def direction():
    lng = request.args.get('lng')
    if lng not in vocabulary: lng = "en" 
    # print(lng)
    voc = vocabulary[lng]["direction"]
    return render_template('in_or_out.html', title='Choose direction', lng=lng, voc=voc)
