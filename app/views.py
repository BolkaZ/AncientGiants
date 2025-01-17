import uuid
from django.shortcuts import get_object_or_404, redirect
from .models import Period, Bid, Animal, BidPeriod
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.db import connection

USER_ID = 1

def add_to_bid(request, period_id):
    bid_id = request.POST['bid_id']

    if not bid_id:
        order = Bid.objects.create(status = 'DRAFT')
        request.session['bid_id'] = order.id
    else:
        order = Bid.objects.filter(id=int(bid_id), status="DRAFT").first()

        if not order:
            order = Bid.objects.create(status = 'DRAFT')
            request.session['bid_id'] = order.id

    period = Period.objects.get(id = period_id)

    bid_period = BidPeriod.objects.filter(bid=order, period=period)
    if not bid_period.exists():
        BidPeriod.objects.create(bid=order, period=period)

    return redirect('index')


def bid_view(request, bid_id):
    order = Bid.objects.filter(id=bid_id, status='DRAFT').first()

    if order and order.periods.all():
        return render(request, 'animal.html', context = {'order': order})

    else:
        return redirect('index')



def clear_bid(request, bid_id):
    request.session['bid_id'] = ''

    with connection.cursor() as database:
        database.execute(f"update app_bid set status = 'ON_DELETE' where id='{bid_id}'")


    return redirect('index')



def index(request):
    query = request.GET.get('q', '')

    if query:
        results = Period.objects.filter(name__icontains=query, is_active=True) 
    else:
        results = Period.objects.filter(is_active=True)


    return render(request, 'main.html', {
        'results': results.order_by('id'),
        'query': query,
    })



def getDetailPage(request, id):
    item = get_object_or_404(Period, id=id)

    return render(request, 'description.html', {'item': item})
