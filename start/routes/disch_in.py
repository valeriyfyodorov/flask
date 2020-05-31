from start import app
from flask import render_template, request
import json
import urllib.request as urequest
from .settings import vocabulary

@app.route('/invoice/')
def invoice():
    lng = request.args.get('lng')
    if lng not in vocabulary: lng = "en" 
    voc = vocabulary[lng]["invoice"]
    api_url = app.config['DB_SERVER_API_URL'] + f"&command=todaylists&lng={lng}"
    # remove for the proper area
    shippersLists = None
    with urequest.urlopen(api_url) as response:
        if response.getcode() == 200:
            source = response.read()
            shippersLists = json.loads(source)
        else:
            print('An error occurred while attempting to retrieve lists data from the API.')  
    print(len(shippersLists))
    # remove above
    return render_template('disch_in/invoice.html', title='Choose direction', lng=lng, voc=voc)