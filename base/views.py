from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, HttpResponse
from django.shortcuts import render
from pymongo import MongoClient

from base.forms import SearchForm
from base.models import get_collection_keys, get_collection_csv

client = MongoClient()


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

    collection_keys = get_collection_keys(db_name, collection_name)

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


@staff_member_required
def get_csv(request, db_name, collection_name):
    csv = get_collection_csv(db_name, collection_name)
    response = HttpResponse(csv, content_type="text/csv; charset=utf-8")
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % collection_name
    return response
