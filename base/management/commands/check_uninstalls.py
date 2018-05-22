import csv
from collections import defaultdict

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
        uninstalls = defaultdict(lambda: [])

        devices = client['joojoo']['deviceDB'].find({"info.pusheId": {"$exists": True, "$ne": None}})
        for device in devices:
            if device["info"]["pusheId"] not in pusheIds:
                if "users" in device and device["users"]:
                    users = device["users"]
                else:
                    users = []
                if "branchReferral" in device["info"]:
                    branchReferral = device["info"]["branchReferral"]
                else:
                    branchReferral = "###"
                query_count = client['joojoo']['queryDB'].count({"device": device["guid"]})
                login_query_count = client['joojoo']['loginqueryDB'].count({"guid": device["guid"]})
                uninstalls[device["info"]["pusheId"]].append(
                    (branchReferral, users, login_query_count, query_count))

        for uninstall in uninstalls.items():
            print(uninstall)
