from django.core.management.base import BaseCommand
from pymongo import MongoClient

client = MongoClient()


class Command(BaseCommand):
    help = 'map devices to users'

    def handle(self, *args, **options):
        devices = client['joojoo']['deviceDB'].find({"info.pusheId": {"$exists": True}})
        counter = 0
        for device in devices:
            guid = device["guid"]
            users = device["users"]
            for user_id in users:
                user = client['joojoo']['userDB'].find_one({"phoneNumber": user_id})
                user_devices = user.get('devices') or []
                user_devices = set(user_devices)
                user_devices.add(guid)
                user["devices"] = list(user_devices)
                client['joojoo']['userDB'].find_one_and_replace({"_id": user.pop("_id")}, user)
            counter += 1
            self.stdout.write(self.style.SUCCESS(counter))
        self.stdout.write(self.style.SUCCESS('Successful'))
