from start import app
from flask import render_template, request
import json
from os import path
import codecs

vocabulary = None
vocabulary = json.load(codecs.open(path.join(app.config['JSON_FOLDER'], 'scales_lng.json'), 'r', 'utf-8-sig'))
# with open(path.join(app.config['JSON_FOLDER'], 'scales_lng.json')) as jsonfile:
#     vocabulary = load(jsonfile.read().decode('utf-8-sig'))
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

@app.route('/invoice/')
def invoice():
    lng = request.args.get('lng')
    if lng not in vocabulary: lng = "en" 
    # print(lng)
    voc = vocabulary[lng]["invoice"]
    return render_template('disch_in/invoice.html', title='Choose direction', lng=lng, voc=voc)