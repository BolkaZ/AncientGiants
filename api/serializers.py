from django.contrib.auth.models import User
from rest_framework import serializers
from app.models import *

class PeriodForBidSerializers(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()

    def get_comment(self, obj):
        bid_period = BidPeriod.objects.get(bid_id=self.context.get("bid_id",0), period=obj)
        return bid_period.comment if bid_period else ""

    class Meta:
        model = Period

        fields = (
            'id',
            'name',
            'image',
            'comment'
        )

class PeriodGetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Period

        fields = (
            'id',
            'name',
            'detail_text',
            'start',
            'end',
            'image'
        )


class PeriodListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Period
        fields = (
            'id',
            'name',
            'start',
            'end',
            'image'
        )


class PeriodInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Period
        fields = (
            'name',
            'detail_text',
            'start',
            'end'
        )


class PeriodUpdateInputSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=True)

    class Meta:
        model = Period
        fields = (
            'name',
            'detail_text',
            'start',
            'end',
            'is_active'
        )


class BidGetSerializer(serializers.ModelSerializer):
    periods = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.get_status_display()

    def get_periods(self, obj):
        period_ids = obj.periods.all().values_list('period_id', flat=True)
        periods = Period.objects.filter(id__in=period_ids)
        return PeriodForBidSerializers(periods, many=True, context={"bid_id":obj.id}).data

    class Meta:
        model = Bid
        fields = (
            'id',
            'status',
            'periods'
        )

class AnimalGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animal
        fields = (
            "name",
            "group",
            "quantity_found"
        )

class PeriodForBidFullInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="period.name")
    image = serializers.CharField(source="period.image")
    animals = serializers.SerializerMethodField()

    def get_animals(self, obj):
        return AnimalGetSerializer(obj.period.animals, many=True).data
    
    class Meta:
        model = BidPeriod
        fields = (
            'name',
            'image',
            'animals',
            'quantity_found'
        )

class BidGetFullInfoSerializer(BidGetSerializer):
    periods = PeriodForBidFullInfoSerializer(many=True)

    class Meta:
        model = Bid
        fields = (
            'periods',
            'created_at',
            'to_form_at',
            'updated_at',
            'finished_at',
            'comment'
        )

class BidListSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # moderator = UserSerializer()

    class Meta:
        model = Bid
        fields = (
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
    status = serializers.CharField()

    class Meta:
        model = Bid
        fields = (
            'status',
        )

class ImageInputSerializer(serializers.Serializer):
    image = serializers.ImageField()


class BidPeriodUpdateInputSerializer(serializers.ModelSerializer):
    bid_id = serializers.IntegerField()
    quantity_found = serializers.IntegerField()

    class Meta:
        model = BidPeriod
        fields = (
            "bid_id",
            "quantity_found",
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
            "id",
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
