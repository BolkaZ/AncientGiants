from rest_framework import serializers
from app.models import *

class PeriodGetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Period

        fields = ('__all__')


class PeriodInputSerializer(serializers.ModelSerializer):
    animals = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all(), many=True)

    class Meta:
        model = Period
        fields = (
            'name',
            'detail_text',
            'start',
            'end',
            'animals'
        )


class PeriodUpdateInputSerializer(serializers.ModelSerializer):
    animals = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all(), many=True)

    class Meta:
        model = Period
        fields = (
            '__all__'
        )


class BidGetSerializer(serializers.ModelSerializer):
    period = PeriodGetSerializers(many=True)

    class Meta:
        model = Bid
        fields = (
            '__all__'
        )

