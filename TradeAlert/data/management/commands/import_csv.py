import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from data.models import Price

class Command(BaseCommand):
    help = 'Import data from a CSV file and add it to the Price model data'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='The path to the CSV file')
        parser.add_argument('time_frame', type=str, help='The time frame of the data')
        parser.add_argument('currency', type=str, help='The currency of time frame')

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        time_frame = options['time_frame']
        currency = options['currency']

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # skip header row
            for row in reader:
                # Create a new Price object from each row in the CSV file
                price = Price(
                    time=int(row[1]),
                    open_price=float(row[2]),
                    high_price=float(row[3]),
                    low_price=float(row[4]),
                    close_price=float(row[5]),
                    volume=int(row[6]),
                    date=datetime.strptime(row[0], '%Y%m%d').date(),
                    currency=currency,
                    time_frame=time_frame
                )
                price.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV file.'))
