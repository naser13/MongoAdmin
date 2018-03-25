import datetime
from collections import defaultdict

from django.core.management.base import BaseCommand
from pymongo import MongoClient

client = MongoClient()


class Command(BaseCommand):
    help = 'get devices use days'

    def handle(self, *args, **options):
        uninstalls = defaultdict(lambda: 0)

        devices = client['joojoo']['deviceDB'].find({"firstDate": {"$exists": True, "$ne": None}})
        for device in devices:
            first_date = datetime.datetime.fromtimestamp(int(device["firstDate"] / 1000))
            last_date = datetime.datetime.fromtimestamp(int(device["lastDate"] / 1000))
            usage_duration = last_date - first_date
            uninstalls[usage_duration.days] += 1

        for uninstall in uninstalls.items():
            print(uninstall)
