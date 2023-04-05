from django.test import TestCase
from datetime import datetime
from .models import Price

class PriceTestCase(TestCase):
    def setUp(self):
        Price.objects.create(
            time=122000,
            open_price=59420.25,
            high_price=59700.0,
            low_price=59000.0,
            close_price=59210.5,
            volume=12345,
            date= datetime.strptime('20230324', '%Y%m%d').date(),
            currency='BTC',
            time_frame='5m'
        )

    def test_price_str(self):
        price = Price.objects.get(currency='BTC', time_frame='5m')
        self.assertEqual(price.time, 122000)