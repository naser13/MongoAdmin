import datetime
from collections import defaultdict

from django.core.management.base import BaseCommand
from pymongo import MongoClient

client = MongoClient()


class Command(BaseCommand):
    help = 'get devices use days'

    def handle(self, *args, **options):
        uninstalls = defaultdict(lambda: set())

        devices = client['joojoo']['deviceDB'].find({"firstDate": {"$exists": True, "$ne": None}})
        for device in devices:
            first_date = datetime.datetime.fromtimestamp(int(device["firstDate"] / 1000))
            if first_date.date() >= (datetime.datetime.now() - datetime.timedelta(days=1)).date():
                continue
            last_date = datetime.datetime.fromtimestamp(int(device["lastDate"] / 1000))
            if first_date == last_date:
                uninstalls[-1].add(device["info"]["pusheId"])
            else:
                usage_duration = last_date - first_date
                uninstalls[usage_duration.days].add(device["info"]["pusheId"])

        for days, ids in uninstalls.items():
            print(days, len(list(ids)))
