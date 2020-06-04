from start import app
from flask import render_template, request, url_for, redirect
from .settings import vocabulary
from .helpers import defaultEn, queryfromArgs, jsonDictFromUrl

@app.route('/final/')
def final():
    query = queryfromArgs(request.args)
    lng = defaultEn(request.args.get('lng'), vocabulary)
    voc = vocabulary[lng]["cmr"]
    action = url_for("cmr") + query
    backUrl = url_for('plates') + queryfromArgs(request.args, excludeKeysList=["pt"])
    return render_template('disch_in/cmr.html', title='Insert cmr data', voc=voc, query=query, backUrl=backUrl, action=action)

