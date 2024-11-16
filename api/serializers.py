from rest_framework import serializers
from app.models import *

class PeriodGetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Period

        fields = ('__all__')

