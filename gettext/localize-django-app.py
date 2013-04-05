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

Dumps the gettext PO files them into locale/ subdirectories, using 
the FILEPATH + FILENAME formatting strings, perfect for Django.

So you want to put this file in the Django app directory that
you want to localize.

Add whatever header info you want in the HEADER.txt file.

Then, specify the SOURCE_URL variable below and call this script
to do the generation. You should now have populated locale/
folders, which contains:

    $ find locale -name django.po
    locale/ja/LC_MESSAGES/django.po
    locale/de/LC_MESSAGES/django.po
    locale/zh_Hant/LC_MESSAGES/django.po
    locale/en/LC_MESSAGES/django.po
    locale/de_AT/LC_MESSAGES/django.po
    locale/zh_Hans/LC_MESSAGES/django.po

On Django, you then need to run:

    django-admin.py compilemessages

And restart the Django instance.
"""

import codecs
import os
import requests
import textwrap

try:
    import markdown
except ImportError:
    print 'Markdown unavailable.'
    pass

FILEPATH    = 'locale/{}/LC_MESSAGES/'
FILENAME    = 'django.po'
HEADER_FILE = 'HEADER.txt'
HEADER      = u''

# LANGUAGES = ['de', 'en', 'es', 'fr', 'ru']

SOURCE_URL = 'https://script.google.com/macros/s/AKfycbxLnEUyElPtL01qHnL7pD2hmTmaO7Tc1yLhjJzQpitpuBfxxBU/exec?sheet%5fid=0AqrUvD5TZZs3dF9ULUh5X1JlakVJRGFHaWRZQmFuZEE&sheet%5fname=Main'

try:
    # Load contents of HEADER.txt if it exists.
    with codecs.open(HEADER_FILE, 'rb', encoding='utf-8') as header:
        HEADER = header.read()
        header.close()
except IOError:
    # Ok, no PO file header.
    pass


def createPoFromDict(language_code='', string_table={}):
    if not language_code:
        raise ValueError('language_code is a required parameter')
    
    if not string_table:
        raise ValueError('string_table is a required parameter')

    # Language_Code files in the spreadsheet are hyphenated 
    # by convention, but Django uses underscores in
    # language_code code names.
    language_code = language_code.replace('-', '_')

    output = []

    for k, v in sorted(string_table.iteritems()):
        # Apply Markdown if it's available.
        try:
            v = markdown.markdown(v)
        except:
            pass

        b = textwrap.wrap(v, drop_whitespace=False)
        c = [u'"{0}"\n'.format(element) for element in b]
        d = u''.join(c)

        output.append((u'msgid "{0}"\n'.format(k)))

        if len(c) == 1:
            output.append(u'msgstr {0}\n'.format(d))
        else:
            output.append(u'msgstr ""\n')
            output.append(d)
            output.append(u'\n')


    # Create locale directories.
    poPath = FILEPATH.format(language_code)
    if not os.path.isdir(poPath):
        os.makedirs(poPath)

    # Create django.po files.
    poName = poPath + FILENAME
    print u'Creating {0}'.format(poName)

    with codecs.open(poName, "wb", encoding='utf-8') as poFile:
        poFile.write(u''.join(output))
        poFile.close()


if __name__ == '__main__':
    r = requests.get(SOURCE_URL)
    
    if r.ok:
        data = r.json()
        for k, v in sorted(data.iteritems()):
            createPoFromDict(language_code=k, string_table=v)

