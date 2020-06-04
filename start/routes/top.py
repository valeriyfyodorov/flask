from start import app
from flask import render_template, request, url_for
import urllib.request as urequest
from .settings import vocabulary
from .helpers import defaultEn
from start.intranet.config import PlatesSet

@app.route('/')
@app.route('/index')
def index():
    lngRows = [["lv", "ru"], ["en", "ee"], ["lt", "pl"]]
    return render_template('languages.html', title='Select language', lngRows=lngRows)

@app.route('/direction/')
def direction():
    lng = defaultEn(request.args.get('lng'), vocabulary)
    voc = vocabulary[lng]["direction"]
    return render_template('in_or_out.html', title='Choose direction', lng=lng, voc=voc)

@app.route('/scales/')
def scales():
    lng = defaultEn(request.args.get('lng'), vocabulary)
    voc = vocabulary[lng]["scales"]
    # TODO insert real url for outwards below
    url =  url_for('invoice') if "in" == request.args.get('dir') else url_for('direction')
    # TODO insert real plate nr finding function below
    plate0 = PlatesSet(front="LF0010", rear="L0001R") 
    plate1 = PlatesSet(front="RF0020", rear="R0002R") 
    # TODO insert real weight finding function below
    weight0 = 55005
    weight1 = 44004
    baseQuery = f"?lng={lng}"
    buttons = {
        "left":
        {
            "url": url + baseQuery + f"&sc=0&ptf={plate0.front}&ptr={plate0.rear}&wkg={weight0}",
            "textAbove": plate0.front,
            "textBelow": plate0.rear,
        },
        "right":
        {
            "url": url + baseQuery + f"&sc=1&ptf={plate1.front}&ptr={plate1.rear}&wkg={weight1}",
            "textAbove": plate1.front,
            "textBelow": plate1.rear,
        },
    }
    return render_template('scales.html', title='Choose scale', lng=lng, voc=voc, buttons=buttons)

@app.route('/directions/')
def directions():
    lng = defaultEn(request.args.get('lng'), vocabulary)
    voc = vocabulary[lng]["directions"]
    next_page_name = app.config['DB_SERVER_URL'] + "weighting-instructions.aspx"
    return render_template('directions.html', title='Proceed to terminal', voc=voc, next_page_name=next_page_name)


@app.route('/unknownerror/')
def unknownerror():
    lng = defaultEn(request.args.get('lng'), vocabulary)
    voc = vocabulary[lng]["unknownerror"]
    next_page_name = app.config['DB_SERVER_URL'] + "weighting-instructions.aspx"
    return render_template('unknownerror.html', title='Sorry. Error.', voc=voc)