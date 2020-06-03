import json
import urllib.request as urequest

def defaultEn(lng, dict):
    if lng is None: return "en" 
    return "en" if lng not in dict else lng

def queryfromArgs(args):
    query = "?"
    for k, v in args.to_dict(flat=True).items():
        query += f"{k}={v}&"
    if len(query) < 2 : return ""
    return query[:-1]

def jsonDictFromUrl(api_url):
    result = None
    with urequest.urlopen(api_url) as response:
        if response.getcode() == 200:
            source = response.read()
            result = json.loads(source)
        else:
            print('An error occurred while attempting to retrieve lists data from the API.') 
    return result