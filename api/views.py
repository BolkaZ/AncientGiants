import uuid

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from app.models import *
from api.serializers import (PeriodGetSerializers, PeriodInputSerializer,
 PeriodUpdateInputSerializer, BidGetSerializer)

class PeriodGetUpdateDeleteView(APIView):

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
        period.image = serializer.validated_data['image']

        period.animals.set(serializer.validated_data['animals'])

        period.save()

        serializer_output = PeriodGetSerializers(period)
        return Response(serializer_output.data)

    def delete(self, request, period_id):
        # TODO needed delete image from minio.

        period = get_object_or_404(Period, id=period_id)
        period.delete()

        return Response(status=204)


class PeriodListCreateView(APIView):
    def get(self, request):

        search = request.query_params.get('search', '')

        if search != '':
            periods = Period.objects.filter(is_active = True, name__icontains = search)

        else:
            periods = Period.objects.filter(is_active = True)

        serializers = PeriodGetSerializers(periods, many = True)

        bid = Bid.objects.filter(session_id = request.session.get('session_id'), status = 'DRAFT').first()
        if bid != None:
            bid_info = {'bid_id': bid.id, 'count_of_periods': bid.period.all().count()}
        
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

        period.animals.set(serializer.validated_data['animals'])

        serializer_output = PeriodGetSerializers(period)
        return Response(serializer_output.data, status=201)



class PeriodInBidCreateView(APIView):

    def post(self, request, period_id):
        period = get_object_or_404(Period, id=period_id)

        session_id = request.session.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session['session_id'] = session_id

        bid = Bid.objects.filter(session_id=session_id, status='DRAFT').first()
        if not bid:
            bid = Bid.objects.create(session_id=session_id, status='DRAFT')

        bid.period.add(period)
        bid.save()

        serializer = BidGetSerializer(bid)
        return Response(serializer.data, status=201)



