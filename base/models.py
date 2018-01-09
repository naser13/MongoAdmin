import json
import subprocess
from functools import lru_cache

from django.conf import settings

TYPES_NOT_SHOWN = ['Object', 'ObjectId']

variety_command = """%s %s --quiet --eval "var collection = '%s', outputFormat='json'" variety.js"""


@lru_cache(maxsize=128)
def get_collection_keys(db_name, collection_name):
    p = subprocess.Popen(variety_command % (settings.MONGO_PATH, db_name, collection_name), shell=True,
                         stdout=subprocess.PIPE)
    variety_result, _ = p.communicate()
    variety_result = json.loads(variety_result)
    collection_keys = []
    for result in variety_result:
        key = result['_id']['key']
        key_type = list(result['value']['types'].keys())[0]
        if key_type not in TYPES_NOT_SHOWN:
            collection_keys.append((key, key_type))

    return collection_keys
