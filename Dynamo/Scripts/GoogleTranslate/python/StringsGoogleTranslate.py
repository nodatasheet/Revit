"""Translate list of strings using Google Translate Service.

IMPORTANT:
For CPython3.
This script uses module 'translatepy':
    https://github.com/Animenosekai/translate

More about installing Python modules in Dynamo:
    https://github.com/DynamoDS/Dynamo/wiki/Customizing-Dynamo%27s-Python-3-installation
    https://forum.dynamobim.com/t/how-to-install-python-modules-in-dynamo-core-runtime-2-8-0/52922/32

It is better to define source/destination language by its three-letter code
    according to ISO 639-2 / ISO 639-3:
    https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
    Simple language names are also acceptable ("English", "Japanese", etc).

If source language was not provided,
    service will try to define it automatically.
    This way works better with strings of mixed languages.

By default translation is done via 'translate.google.com' server.
    Feel free to change it to other suitable server in your region
    using SERVER_URL constant.
    Example: SERVER_URL = 'translate.google.cn'

List of supported languages and servers can be found here:
    https://github.com/Animenosekai/translate/blob/main/translatepy/translators/google.py

By default 'translatepy' caches translation results for better performance.
    https://github.com/Animenosekai/translate#caching
    Current script cleans the cash in the end of translation:
    controlled via CLEAN_TRANSLATION_CACHE constant.
    You may want to disable the cleaning.

As it is mentioned in 'translatepy' disclaimer:
    Please do not use this module in a commercial manner.
    Pay a proper API Key from one of the services to do so.
    https://github.com/Animenosekai/translate#disclaimer
"""

import re
import sys
import System
import requests

re_dir = System.IO.DirectoryInfo(re.__file__)
path_py3_lib = re_dir.Parent.Parent.FullName
sys.path.append(path_py3_lib + r'\Lib\site-packages')

from translatepy.translators.google import GoogleTranslate


def tolist(obj1):
    """Convert to list if not list."""
    if hasattr(obj1, '__iter__'):
        return obj1
    else:
        return [obj1]


def assure_online(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.status_code


source_texts = tolist(IN[0])
source_lang = IN[1]
dest_lang = IN[2]

SERVER_URL = 'translate.google.com'
CLEAN_TRANSLATION_CACHE = True

if not source_lang:
    source_lang = 'auto'

check_url = assure_online(f'http://{SERVER_URL}')

g_translate = GoogleTranslate(service_url=SERVER_URL)

translations = []
for text in source_texts:
    translation = g_translate.translate(text, dest_lang, source_lang).result
    translations.append(translation)

if CLEAN_TRANSLATION_CACHE is True:
    g_translate.clean_cache()

OUT = translations
