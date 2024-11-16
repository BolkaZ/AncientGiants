from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from app.models import *
from api.serializers import PeriodGetSerializers

class PeriodGetView(APIView):
    def get(self, request, period_id):
        
        period = get_object_or_404(Period, id = period_id, is_active = True)

        serializers = PeriodGetSerializers(period)

        return Response(serializers.data)


class PeriodListView(APIView):
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



