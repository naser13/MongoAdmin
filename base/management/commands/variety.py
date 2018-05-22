from django.core.management.base import BaseCommand

from base.models import cache_collection_keys


class Command(BaseCommand):
    help = 'update variety'

    def add_arguments(self, parser):
        parser.add_argument('db')
        parser.add_argument('collection')

    def handle(self, *args, **options):
        db = options['db']
        collection = options['collection']
        cache_collection_keys(db, collection)
        print("done")
