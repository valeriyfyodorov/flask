from start import app
from flask import render_template, request, url_for, redirect
import urllib.request as urequest
from .settings import vocabulary
from .helpers import defaultEn, queryfromArgs, jsonDictFromUrl
from start.intranet.config import PlatesSet, SCALES
from start.intranet.defs import readQrCodeFromCam, getPlatesNumbers, getWeightKg, archivePlates

@app.route('/')
def index():
    lngRows = [["lv", "ru"], ["en", "ee"], ["lt", "pl"]]
    return render_template('languages.html', title='Select language', lngRows=lngRows)

@app.route('/direction')
def direction():
    lng = defaultEn(request.args.get('lng'), vocabulary)
    voc = vocabulary[lng]["direction"]
    return render_template('in_or_out.html', title='Choose direction', lng=lng, voc=voc)

@app.route('/scales')
def scales():
    lng = defaultEn(request.args.get('lng'), vocabulary)
    voc = vocabulary[lng]["scales"]
    url =  url_for('invoice') if "disch_in" == request.args.get('dir') else url_for('qrcode')
    weight1 = getWeightKg("north")
    weight2 = getWeightKg("south")
    if weight1 < 200 and weight2 < 200: return redirect(url_for("unknownerror") + f"?lng={lng}&error=Small weight")
    plate1 = getPlatesNumbers("north")
    plate2 = getPlatesNumbers("south")
    scaleId1 = SCALES["north"]["id"]
    scaleId2 = SCALES["south"]["id"]
    baseQuery = f"?lng={lng}"
    buttons = {
        "left":
        {
            "url": url + baseQuery + f"&sc={scaleId1}&ptf={plate1.front}&ptr={plate1.rear}&wkg={weight1}",
            "textAbove": plate1.front,
            "textBelow": plate1.rear,
        },
        "right":
        {
            "url": url + baseQuery + f"&sc={scaleId2}&ptf={plate2.front}&ptr={plate2.rear}&wkg={weight2}",
            "textAbove": plate2.front,
            "textBelow": plate2.rear,
        },
    }
    if weight1 < 200: return redirect(buttons["right"]["url"]) # no left weight, no choice
    if weight2 < 200: return redirect(buttons["left"]["url"]) # no right weight no choice
    return render_template('scales.html', title='Choose scale', lng=lng, voc=voc, buttons=buttons)

@app.route('/directions')
def directions():
    lng = defaultEn(request.args.get('lng'), vocabulary)
    voc = vocabulary[lng]["directions"]
    # next_page_name = app.config['DB_SERVER_URL'] + "weighting-instructions.aspx" # for external server processing
    next_page_name = url_for("qrinstructions")
    return render_template('directions.html', title='Proceed to terminal', voc=voc, next_page_name=next_page_name)


@app.route('/unknownerror')
def unknownerror():
    lng = defaultEn(request.args.get('lng'), vocabulary)
    voc = vocabulary[lng]["unknownerror"]
    errorTxt=(request.args.get('error') or '')
    # next_page_name = app.config['DB_SERVER_URL'] + "weighting-instructions.aspx"
    return render_template('unknownerror.html', title='Sorry. Error.', voc=voc, errorTxt=errorTxt)


@app.route('/farewell')
def farewell():
    lng = defaultEn(request.args.get('lng'), vocabulary)
    tranunit = readQrCodeFromCam()
    voc = vocabulary[lng]["farewell"]
    query = queryfromArgs(request.args)
    if tranunit == 0 : return redirect(url_for("qrcode") + query)
    api_query = query[1:] + f"&tranunit={tranunit}"
    api_url = app.config['DB_SERVER_API_URL'] + f"&command=finalweight" + f"&{api_query}"
    weighting = jsonDictFromUrl(api_url)
    if weighting["result"] == 2 : # means repeated print out
        print(weighting["error"])
        # return redirect(app.config['DB_SERVER_URL'] + f"weighting-printout.aspx?{api_query}&local=1") # in case the printing at amgs
        return redirect(url_for("printout") + f"?{api_query}") 
    if weighting["result"] != 0 : # some error
        print(weighting["error"])
        return redirect(url_for("unknownerror") + query)
    archivePlates(tranunit, request.args)
    # next_page_name = app.config['DB_SERVER_URL'] + "weighting-printout.aspx" # in case the printing at amgs
    next_page_name = url_for("printout")
    return render_template('farewell.html', title='Get the documents and goodbye', voc=voc, next_page_name=next_page_name, tranunit=tranunit)

