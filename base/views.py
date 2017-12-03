import json
import subprocess

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render
from pymongo import MongoClient

from base.forms import SearchForm

client = MongoClient()

variety_command = """%s %s --quiet --eval "var collection = '%s', outputFormat='json'" variety.js"""

TYPES_NOT_SHOWN = ['Object', 'ObjectId']


def index(request):
    objects = []
    for db in client.database_names():
        objects.append({'name': db, 'count': len(client[db].collection_names())})
    return render(request, 'index.html', {'objects': objects})


@staff_member_required
def db_view(request, db_name):
    if db_name not in client.database_names():
        raise Http404()
    objects = []
    db = client[db_name]
    for collection in db.collection_names():
        objects.append({'name': collection, 'count': db[collection].count()})
    return render(request, 'db_view.html', {'objects': objects, 'db_name': db_name})


@staff_member_required
def collection_view(request, db_name, collection_name):
    if db_name not in client.database_names():
        raise Http404()
    db = client[db_name]
    if collection_name not in db.collection_names():
        raise Http404()
    collection = db[collection_name]

    p = subprocess.Popen(variety_command % (settings.MONGO_PATH, db_name, collection_name), shell=True, stdout=subprocess.PIPE)
    variety_result, _ = p.communicate()
    variety_result = json.loads(variety_result)
    collection_keys = []
    for result in variety_result:
        key = result['_id']['key']
        key_type = list(result['value']['types'].keys())[0]
        if key_type not in TYPES_NOT_SHOWN:
            collection_keys.append((key, key_type))

    objects = collection.find()
    if request.method == 'POST':
        form = SearchForm(data=request.POST, keys=collection_keys)
        if form.is_valid():
            query = form.get_result()
            objects = collection.find(query)
    else:
        form = SearchForm(keys=collection_keys)

    page = request.POST.get('page')
    paginator = Paginator(objects, 10)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    return render(request, 'collection_view.html', {'objects': objects, 'form': form, 'keys': collection_keys})
