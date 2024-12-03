from django.contrib.auth.models import User
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
    periods = serializers.SerializerMethodField()

    def get_periods(self, obj):
        period_ids = obj.periods.all().values_list('period_id', flat=True)
        periods = Period.objects.filter(id__in=period_ids)
        return PeriodGetSerializers(periods, many=True).data

    class Meta:
        model = Bid
        fields = (
            '__all__'
        )

class BidListSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # moderator = UserSerializer()

    class Meta:
        model = Bid
        fields = (
                'id', 
                'status', 
                'created_at', 
                'to_form_at',
                'finished_at',
                'updated_at', 
                'comment',
                # 'user', 
                # 'moderator'
            )

class BidUpdateInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bid
        fields = (
            'comment',
        )

class BidModerationInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bid
        fields = (
            'status',
        )

class ImageInputSerializer(serializers.Serializer):
    image = serializers.ImageField()

class BidPeriodUpdateInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = BidPeriod
        fields = (
            "count",
        )

class BidPeriodListSerializer(serializers.ModelSerializer):

    class Meta:
        model = BidPeriod
        fields = ("__all__")


class UserCreateInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("__all__")

class UserLoginInputSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "username",
            "password"
        )


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email"
        )

class UserUpdateInputSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password"
        )
