import uuid
import redis

from datetime import datetime
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from app.models import *
from api.serializers import (PeriodGetSerializers, PeriodInputSerializer,
 PeriodUpdateInputSerializer, BidGetSerializer,ImageInputSerializer, BidListSerializer,
 BidUpdateInputSerializer, BidModerationInputSerializer, BidPeriodUpdateInputSerializer,
 BidPeriodListSerializer, UserCreateInputSerializer, UserListSerializer,
 UserLoginInputSerializer, UserUpdateInputSerializer, PeriodListSerializer,
 BidGetFullInfoSerializer )
from api.minio import add_pic, delete_pic
from api.permissions import IsModeratorOrReadOnly, IsCreator, IsAuth, IsModerator, IsCreatorOrModerator
from paleo_project import settings


redis = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

class PeriodGetUpdateDeleteView(APIView):
    permission_classes = (IsModeratorOrReadOnly,)

    def get(self, request, period_id):
        period = get_object_or_404(Period, id = period_id, is_active = True)

        serializers = PeriodGetSerializers(period)

        return Response(serializers.data)

    def put(self, request, period_id):
        period = get_object_or_404(Period, id=period_id)

        input_data = request.data
        serializer = PeriodUpdateInputSerializer(data=input_data)
        serializer.is_valid(raise_exception=True)
        
        period.name = serializer.validated_data['name']
        period.detail_text = serializer.validated_data['detail_text']
        period.start = serializer.validated_data['start']
        period.end = serializer.validated_data['end']
        period.is_active = serializer.validated_data['is_active']

        period.save()

        serializer_output = PeriodGetSerializers(period)
        return Response(serializer_output.data)

    def delete(self, request, period_id):
        period = get_object_or_404(Period, id=period_id)
        delete_pic(period)
        period.delete()

        return Response(status=204)


class PeriodListCreateView(APIView):
    permission_classes = (IsModeratorOrReadOnly,)

    def get(self, request):
        search = request.query_params.get('search', '')

        if search != '':
            periods = Period.objects.filter(is_active = True, name__icontains = search)

        else:
            periods = Period.objects.filter(is_active = True)

        serializers = PeriodListSerializer(periods, many = True)

        bid = Bid.objects.filter(session_id = request.session.get('session_id'), status = 'DRAFT').first()
        if bid != None:
            bid_info = {'bid_id': bid.id, 'count_of_periods': bid.periods.all().count()}
        
        else:
            bid_info = {'detail': 'Черновой заявки нет'}

        return Response({'periods': serializers.data, 'bid_info': bid_info})

    def post(self, request):
        input_data = request.data # {'key':'value'}
        serializer = PeriodInputSerializer(data=input_data)
        serializer.is_valid(raise_exception=True)

        period = Period.objects.create(
            name=serializer.validated_data['name'], # {'key':'value'}
            detail_text=serializer.validated_data['detail_text'],
            start=serializer.validated_data['start'],
            end=serializer.validated_data['end'],
        )

        serializer_output = PeriodGetSerializers(period)
        return Response(serializer_output.data, status=201)



class PeriodInBidCreateDeleteUpdateView(APIView):

    def post(self, request,  period_id):
        self.permission_classes = (IsAuth, IsCreator,)
        self.check_permissions(request)

        bid_id = request.data.get("bid_id")

        if bid_id is None:
            user_id = str(redis.get(request.COOKIES.get("session_id"))).split("b'")[-1].split("'")[0]
            bid = Bid.objects.create(status="DRAFT", session_id=user_id)
        else:
            bid = get_object_or_404(Bid, id=bid_id, status="DRAFT")

        self.check_object_permissions(request, obj=bid)
        period = get_object_or_404(Period, id=period_id)

        bid_period = BidPeriod.objects.filter(bid=bid, period=period)
        if not bid_period.exists():
            BidPeriod.objects.create(bid=bid, period=period)

        serializer = BidGetFullInfoSerializer(bid)
        return Response(serializer.data, status=201)

    def delete(self, request, period_id):
        self.permission_classes = (IsAuth, IsCreator,)
        self.check_permissions(request)

        bid = get_object_or_404(Bid, id=request.data.get("bid_id", -1), status='DRAFT')
        self.check_object_permissions(request, obj=bid)

        period = get_object_or_404(Period, id=period_id)

        bid_period_item = get_object_or_404(BidPeriod, bid=bid, period=period)

        bid_period_item.delete()

        return Response(status=204)

    def put(self, request, period_id):
        self.permission_classes = (IsAuth, IsCreator,)
        self.check_permissions(request)

        data = request.data
        serializer = BidPeriodUpdateInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        bid = get_object_or_404(Bid, id=serializer.validated_data["bid_id"])
        self.check_object_permissions(request, obj=bid)

        period = get_object_or_404(Period, id=period_id)

        bid_period_item = get_object_or_404(BidPeriod, bid=bid, period=period)
        bid_period_item.quantity_found = serializer.validated_data["quantity_found"]
        bid_period_item.save()

        serializer_output = BidGetFullInfoSerializer(bid)
        return Response(serializer_output.data)

        


class PeriodImageCreateView(APIView):
    permission_classes = (IsModeratorOrReadOnly,)

    def post(self, request, period_id):
        period = get_object_or_404(Period, id=period_id)

        data = request.FILES

        serializer = ImageInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        delete_result = delete_pic(period)
        if delete_result.get('error'):
            return Response(delete_result['error'], status=400)

        result = add_pic(period, serializer.validated_data['image'])

        return result


class BidListView(APIView):
    permission_classes = (IsModerator, )
    
    def get(self, request):
        status_filter = request.query_params.get('status')
        date_start = request.query_params.get('date_start')
        date_end = request.query_params.get('date_end')

        bids = Bid.objects.exclude(status__in=['DRAFT', 'ON_DELETE'])

        if status_filter:
            bids = bids.filter(status=status_filter)
        if date_start and date_end:
            bids = bids.filter(created_at__range=[date_start, date_end])

        serializer = BidListSerializer(bids, many=True)
        return Response(serializer.data, status=200)


class BidGetUpdateDeleteView(APIView):

    def get(self, request, bid_id):
        self.permission_classes = (IsCreatorOrModerator, )
        bid = get_object_or_404(Bid, id=bid_id)
        self.check_object_permissions(request, obj=bid)

        serializer = BidGetFullInfoSerializer(bid)
        return Response(serializer.data, status=200)

    def put(self, request, bid_id):
        self.permission_classes = (IsCreatorOrModerator, )
        bid = get_object_or_404(Bid, id=bid_id, status='DRAFT')
        self.check_object_permissions(request, obj=bid)

        data = request.data
        serializer = BidUpdateInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        bid.comment = serializer.validated_data['comment']
        bid.save()

        serializer_output = BidGetFullInfoSerializer(bid)
        return Response(serializer_output.data)

    def delete(self, request, bid_id):
        self.permission_classes = (IsCreatorOrModerator, )
        bid = get_object_or_404(Bid, id=bid_id, status='DRAFT')
        self.check_object_permissions(request, obj=bid)

        bid.status = 'ON_DELETE'
        bid.save()

        return Response(status=204)


class BidFormView(APIView):

    def put(self, request, bid_id):
        self.permission_classes = (IsCreatorOrModerator,)
        bid = get_object_or_404(Bid, id=bid_id, status='DRAFT')
        self.check_object_permissions(request, obj=bid)

        if not bid.periods.all():
            return Response({'detail':'Bid is empty.'})

        bid.status = 'APPROVED'
        bid.to_form_at = datetime.now()

        bid.save()

        serializer = BidGetFullInfoSerializer(bid)
        return Response(serializer.data)

class BidModerationView(APIView):
    permission_classes = (IsModerator,)

    def put(self, request, bid_id):
        bid = get_object_or_404(Bid, id=bid_id, status='APPROVED')

        data = request.data
        serializer = BidModerationInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['status'] not in ['REJECTED', 'FINISHED']:
            return Response({'detail':'Status must be rejected or finished.'})

        bid.status = serializer.validated_data['status']
        bid.finished_at = datetime.now()

        bid.save()

        serializer_output = BidListSerializer(bid)
        return Response(serializer_output.data)
        

class SessionCreateView(APIView):

    def post(self, request, session_id):
        request.session["session_id"] = session_id
        return Response(status=204)


class UserCreateView(APIView):

    def post(self, request):
        data = request.data
        serializer = UserCreateInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            first_name=serializer.validated_data.get("first_name", ""),
            last_name=serializer.validated_data.get("last_name", ""),
            email=serializer.validated_data.get("email",""),
            password=serializer.validated_data["password"],
        )

        serializer_output = UserListSerializer(user)
        return Response(serializer_output.data)

class UserUpdateView(APIView):
    permission_classes = (IsModerator, )

    def put(self, request, user_id):
        data = request.data
        serializer = UserUpdateInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, id=user_id)
        if serializer.validated_data.get("first_name"):
            user.first_name = serializer.validated_data["first_name"]

        if serializer.validated_data.get("last_name"):
            user.last_name = serializer.validated_data["last_name"]

        if serializer.validated_data.get("email"):
            user.email = serializer.validated_data["email"]

        if serializer.validated_data.get("password"):
            user.set_password(serializer.validated_data["password"])

        user.save()

        serializer_output = UserListSerializer(user)
        return Response(serializer_output.data)


class UserLoginView(APIView):

    def post(self, request):
        data = request.data
        serializer = UserLoginInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"]
        )

        if user is not None:
            session_id = str(uuid.uuid4())
            redis.set(session_id, user.id)
            # login(request, user)
            serializer_output = UserListSerializer(user)
            response = Response(serializer_output.data)
            response.set_cookie("session_id", session_id, secure=False, httponly=True, samesite='None', max_age=600)
            print(redis.get(session_id))
            return response
        else:
            return Response({"detail":"Invalid credentianls."}, status=403)


class UserLogoutView(APIView):

    def post(self, request):
        session_id = request.COOKIES.get("session_id")
        print(session_id)
        if session_id:
            redis.delete(session_id)
        # logout(request)
            response = Response({"detail":"success"})
            response.delete_cookie("session_id")
            return response
        return Response({"detail": "You must authorize before."})
    





