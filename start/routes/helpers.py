import json
import urllib.request as urequest
from  urllib.parse import urlencode as encode

def defaultEn(lng, dictionary):
    if lng is None: return "en" 
    return "en" if lng not in dictionary else lng

def queryfromArgs(args, excludeKeysList=None):
    query = "?"
    convertedDict = args.to_dict(flat=True)
    if excludeKeysList is not None:
        for item in excludeKeysList:
            convertedDict.pop(item, None)
    query += encode(convertedDict)
    if len(query) < 2 : return ""
    return query

def jsonDictFromUrl(api_url):
    result = None
    with urequest.urlopen(api_url) as response:
        if response.getcode() == 200:
            source = response.read()
            result = json.loads(source)
        else:
            print('An error occurred while attempting to retrieve lists data from the API.') 
    return result

def splitDictInto3(dictionary, extraDict=None):
    dict1 = []
    dict2 = []
    dict3 = []
    if extraDict is not None : dictionary.append(extraDict)
    if len(dictionary) < 1:
        return dict1, dict2, dict3 
    elif len(dictionary) == 1:
        return dictionary, dict2, dict3
    elif len(dictionary) == 2:
        return dictionary[0:1], dictionary[1:], dict3
    divResult = int(len(dictionary) / 3)
    return dictionary[0:divResult], dictionary[divResult : divResult * 2], dictionary[divResult * 2 :]