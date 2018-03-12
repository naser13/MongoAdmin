from django.core.management.base import BaseCommand
from pymongo import MongoClient

client = MongoClient()


class Command(BaseCommand):
    help = 'map users to devices'

    def handle(self, *args, **options):
        devices = client['joojoo']['deviceDB'].find({"info.pusheId": {"$exists": True}})
        counter = 0
        for device in devices:
            guid = device["guid"]
            queries = client['joojoo']['V2queryDB'].find({"guid": guid, "Authorization": {"$exists": True}})
            users = set()
            for query in queries:
                token = query["Authorization"][6:]
                token = client['joojoo']['tokenDB'].find_one({"accessToken": token})
                if token:
                    users.add(token['phoneNumber'])
            device["users"] = list(users)
            client['joojoo']['deviceDB'].find_one_and_replace({"_id": device.pop("_id")}, device)
            counter += 1
            self.stdout.write(self.style.SUCCESS(counter))
        self.stdout.write(self.style.SUCCESS('Successful'))
