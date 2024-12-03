from django.contrib import admin
from .models import Period, Animal, Bid, BidPeriod

admin.site.register(Period)
admin.site.register(Animal)
admin.site.register(Bid)
admin.site.register(BidPeriod)