from start import app
from flask import render_template, request, url_for, redirect
from .settings import vocabulary
from .helpers import defaultEn, queryfromArgs, jsonDictFromUrl

@app.route('/invoice/')
def invoice():
    lng = defaultEn(request.args.get('lng'), vocabulary)
    voc = vocabulary[lng]["invoice"]
    query = queryfromArgs(request.args)
    return render_template('disch_in/invoice.html', title='Scan invoice or CMR', voc=voc, query=query)

@app.route('/lists/')
def lists():
    lng = defaultEn(request.args.get('lng'), vocabulary)
    voc = vocabulary[lng]["lists"]
    # TODO - Scan page procedure shall be here first below
    invoiceFileName = "2020/06/03/hh_mm_ss.jpg"
    query = queryfromArgs(request.args) + f"&ifn={invoiceFileName}"
    # get list from api
    api_url = app.config['DB_SERVER_API_URL'] + f"&command=todaylists&lng={lng}"
    shippersList = jsonDictFromUrl(api_url)
    # TODO redirect to right location here
    if len(shippersList) == 0 :
        return redirect(url_for('invoice'))
    # TODO in template right next page url_for
    return render_template('disch_in/lists.html', title='Choose a shipper', voc=voc, query=query, shippersList=shippersList)