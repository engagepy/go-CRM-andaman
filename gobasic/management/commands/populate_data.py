import csv
from gobasic.models import Hotel
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Ingest data into db"

    def handle(self, *args, **options):
        self.stdout.write("Creating demo data...")

        # Open the CSV file and create a CSV reader object
        with open("hotel_sheet.csv", "r") as csvfile:
            csvreader = csv.reader(csvfile)

            # Skip the header row
            next(csvreader)

            # Loop through the rows in the CSV file
            for row in csvreader:
                # Extract the data from the row
                hotel_name = row[0]
                customer_rating = row[1]
                room_name = row[2]
                room_categories = row[3] if row[3] else "Budget"
                location = row[4]
                net_cp = int(row[5]) if row[5] else 0
                net_map = int(row[6]) if row[6] else 0
                net_ap = int(row[7]) if row[7] else 0
                net_cp_kid = int(row[8]) if row[8] else 0
                net_map_kid = int(row[9]) if row[9] else 0

                Hotel.objects.create(
                    hotel_name=hotel_name,
                    customer_rating=customer_rating,
                    room_name=room_name,
                    room_categories=room_categories,
                    location_id=location,
                    net_cp=net_cp,
                    net_ap=net_ap,
                    net_map=net_map,
                    net_cp_kid=net_cp_kid,
                    net_map_kid=net_map_kid,
                    net_ap_kid=0,
                )

        self.stdout.write("demo data created...")
