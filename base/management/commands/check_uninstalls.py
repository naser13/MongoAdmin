import csv

from django.core.management.base import BaseCommand
from pymongo import MongoClient

client = MongoClient()


class Command(BaseCommand):
    help = 'check user uninstalls with pusheIds'

    def add_arguments(self, parser):
        parser.add_argument('csv_path')

    def handle(self, *args, **options):
        f = open(options['csv_path'], "r", encoding="utf-8")
        reader = csv.reader(f)
        pusheIds = list(reader)
        pusheIds = sum(pusheIds, [])

        devices = client['joojoo']['deviceDB'].find({"info.pusheId": {"$exists": True}})
        for device in devices:
            if device["info"]["pusheId"] not in pusheIds:
                for user in device["users"]:
                    self.stdout.write(user)
        self.stdout.write(self.style.SUCCESS('Finish'))
