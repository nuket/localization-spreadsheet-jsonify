"""
Copyright (c) 2013 Max Vilimpoc

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom 
the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR 
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE 
OR OTHER DEALINGS IN THE SOFTWARE.
"""

"""
Generates gettext translations from Localization Spreadsheet 
JSONify output.

Just specify the SOURCE_URL variable below and call this script
to do the generation. 

You will then have a bunch of .json files in the same directory 
as your script that comprise your language pack:

    Loading translation spreadsheet data.
    Generating translations.
    Creating translation-de.json
    Creating translation-de-AT.json
    Creating translation-en.json
    Creating translation-ja.json
    Creating translation-zh-Hans.json
    Creating translation-zh-Hant.json
"""

import codecs
import json
import os
import requests

FILENAME = 'translation-{code}.json'

SOURCE_URL = 'https://script.google.com/macros/s/AKfycbxLnEUyElPtL01qHnL7pD2hmTmaO7Tc1yLhjJzQpitpuBfxxBU/exec?sheet%5fid=0AqrUvD5TZZs3dF9ULUh5X1JlakVJRGFHaWRZQmFuZEE&sheet%5fname=Main'

if __name__ == '__main__':
    print 'Loading translation spreadsheet data.'
    r = requests.get(SOURCE_URL)
    
    if r.ok:
        print 'Generating translations.'

        data = r.json()
        for k, v in sorted(data.iteritems()):
            filename = FILENAME.format(code=k)
            print u'Creating {0}'.format(filename)

            with codecs.open(filename, "wb", encoding='utf-8') as jsonFile:
                json.dump(v, jsonFile, indent=4)
                jsonFile.close()
    else:
        print r"Couldn't load spreadsheet data from Google Docs."
