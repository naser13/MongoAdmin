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
        uninstalls = []

        devices = client['joojoo']['deviceDB'].find({"info.pusheId": {"$exists": True, "$ne": None}})
        for device in devices:
            if device["info"]["pusheId"] not in pusheIds:
                if "users" in device and device["users"]:
                    users = device["users"]
                else:
                    users = []
                if "branchReferral" in device:
                    branchReferral = device["branchReferral"]
                else:
                    branchReferral = "###"
                uninstalls.append((branchReferral, users))

        for uninstall in uninstalls:
            print(uninstall)
        self.stdout.write(self.style.SUCCESS('Finish'))
