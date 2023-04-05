from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
class Price(models.Model):
    time = models.IntegerField(_("Time"))
    open_price = models.DecimalField(_("Open Price"), decimal_places=2, max_digits=1000)
    high_price = models.DecimalField(_("High Price"), decimal_places=2, max_digits=1000)
    low_price = models.DecimalField(_("Low Price"), decimal_places=2, max_digits=1000)
    close_price = models.DecimalField(_("Close Price"), decimal_places=2, max_digits=1000)
    volume = models.IntegerField( ("Volume"))
    date = models.DateField(_("Date"))
    currency = models.CharField(_("Currency"), max_length=50)
    time_frame = models.CharField(_("Time Frame"), max_length=3)

    
    def __str__(self) -> str:
        return f'{self.currency} - {self.time_frame}'