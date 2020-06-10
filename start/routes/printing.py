from datetime import datetime
from start import app
from flask import render_template, request, url_for, redirect
import qrcode
from .settings import vocabulary
from .helpers import defaultEn, queryfromArgs, servePILimageAsPNG, dateFromJson, jsonDictFromUrl

@app.route('/qrinstructions')
def qrinstructions():
    lng = defaultEn(request.args.get('lng'), vocabulary)
    voc = vocabulary[lng]["scales"]
    query = queryfromArgs(request.args)
    api_query = query[1:]
    tranunit_id = request.args.get('tranunit')
    tranunit = jsonDictFromUrl(app.config['DB_SERVER_API_URL'] + f"&command=tranunit" + f"&id={tranunit_id}")
    cargo = jsonDictFromUrl(app.config['DB_SERVER_API_URL'] + f"&command=cargo" + f"&id={tranunit['cargoId']}")
    client = jsonDictFromUrl(app.config['DB_SERVER_API_URL'] + f"&command=company" + f"&id={tranunit['shipperId']}")
    factory = jsonDictFromUrl(app.config['DB_SERVER_API_URL'] + f"&command=company" + f"&id={tranunit['factoryId']}")
    stevedoreInfo = jsonDictFromUrl(
        app.config['DB_SERVER_API_URL'] + 
        f"&command=steveinfo" + 
        f"&cargo={tranunit['cargoId']}&shipper={tranunit['shipperId']}&factory={tranunit['factoryId']}"
        )
    drivingScheme = stevedoreInfo["drivingScheme"] + ".jpg";
    info = stevedoreInfo["stevedoreInfo"];
    if info is None : info = ""
    print_time = datetime.now().strftime("%d/%m/%Y %H:%M");
    netWeightScales = tranunit["weightScales"]
    grossWeightMoment = dateFromJson(tranunit["weightingGrossMoment"])
    grossWeightScales = tranunit["weightingGrossWeight"]
    tareWeightMoment = dateFromJson(tranunit["weightingEmptyMoment"])
    tareWeightScales = tranunit["weightingEmptyWeight"]
    if (grossWeightScales < tareWeightScales): # loading, not discharging
        grossWeightMoment = dateFromJson(tranunit["weightingEmptyMoment"])
        grossWeightScales = tranunit["weightingEmptyWeight"]
        tareWeightMoment = dateFromJson(tranunit["weightingGrossMoment"]) 
        tareWeightScales = tranunit["weightingGrossWeight"]
        netWeightScales = -netWeightScales;
    showIncomingTitle = (grossWeightScales > tareWeightScales);
    grossWeightScales = "{:.0f}".format(grossWeightScales * 1000)
    issueMoment = grossWeightMoment
    extraHeading = tranunit["declarationNr"] + " // " + "{:.0f}".format(tranunit['weightDeclared'] * 1000) + " kg"
    remark = factory["name"]
    if tranunit["remark"] is not None:
        remark += " " + tranunit["remark"]
    content = {
        "tranunit_id": tranunit["id"],
        "cargoName": cargo["name"],
        "clientName": client["name"],
        "clientAddress": client["invoiceAddressWording"],
        "clientRegNr": client["officialRegNr"],
        "remark": remark,
        "extraHeading": extraHeading,
        "nr": tranunit["nr"],
        "print_time": print_time,
        "showIncomingTitle": showIncomingTitle,
        "grossWeightScales": grossWeightScales,
        "issueMoment": issueMoment,
        "drivingScheme": drivingScheme,
        "info": info,
    }
    return render_template('disch_in/qrinstructions.html', title='Keep this all time', lng=lng, voc=voc, content=content)

@app.route('/qrimg')
def qrimg():
    code = request.args.get('code')
    img = qrcode.make(code)
    return servePILimageAsPNG(img)

@app.route('/waitprint')
def waitprint():
    lng = defaultEn(request.args.get('lng'), vocabulary)
    voc = vocabulary[lng]["scales"]
    return render_template('scales.html', title='Choose scale', lng=lng, voc=voc)
