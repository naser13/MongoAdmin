import json
import subprocess

from django.conf import settings
from pymongo import MongoClient

TYPES_IGNORED = ['ObjectId']

variety_command = """%s %s --quiet --eval "var collection = '%s', limit = 100, outputFormat='json'" variety.js"""
csv_command = """%sexport --db %s --collection %s --query '%s' --type=csv --fields %s"""

client = MongoClient()


def cache_collection_keys(db_name, collection_name):
    p = subprocess.Popen(variety_command % (settings.MONGO_PATH, db_name, collection_name),
                         shell=True, stdout=subprocess.PIPE)
    variety_result, _ = p.communicate()
    variety_result = json.loads(variety_result.decode('utf8'))
    collection_keys = []
    search_keys = []
    for result in variety_result:
        key = result['_id']['key']
        key_type = list(result['value']['types'].keys())[0]
        if key_type not in TYPES_IGNORED:
            if '.' not in key:
                collection_keys.append((key, key_type))
            if 'XX' not in key:
                search_keys.append((key, key_type))

    client['variety'][db_name].insert_one({"collection": collection_name,
                                           "collection_keys": collection_keys,
                                           "search_keys": search_keys})


def get_collection_keys(db_name, collection_name):
    cached = client['variety'][db_name].find_one({"collection": collection_name})
    if not cached:
        cache_collection_keys(db_name, collection_name)
        return get_collection_keys(db_name, collection_name)
    return cached["collection_keys"], cached["search_keys"]


def get_collection_csv(db_name, collection_name, fields, query):
    command = csv_command % (settings.MONGO_PATH, db_name, collection_name,
                             json.dumps(query, ensure_ascii=False),
                             ",".join([field[0] for field in fields]))
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    csv, _ = p.communicate()
    return csv
