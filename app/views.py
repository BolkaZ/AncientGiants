import uuid
from django.shortcuts import get_object_or_404, redirect
from .models import Period, Bid, Animal
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.db import connection

USER_ID = 1


from django.shortcuts import redirect, get_object_or_404
from .models import Period, Bid

def add_to_bid(request, period_id):
    orders = Bid.objects.filter(status = 'DRAFT', session_id = request.session.get('session_id'))
    order = None

    if not orders.exists():
        order = Bid.objects.create(session_id = request.session.get('session_id'), status = 'DRAFT')

    else:
        order = orders.first()

    period = Period.objects.get(id = period_id)

    order.period.add(period)

    order.save()

    return redirect('getDetailPage', id=period_id)


def bid_view(request):

    orders = Bid.objects.filter(session_id = request.session.get('session_id'), status = 'DRAFT')

    if orders.exists():
        return render(request, 'animal.html', context = {'order': orders.first()})

    else:
        return redirect('index')



def clear_bid(request):

    #bid = get_object_or_404(Bid, session_id=request.session.get('session_id'), status='DRAFT')

    #orm для соединения с бд
    #Bid.objects.raw(f"update bid status='ON_DELETE' where session_id={request.session.get('session_id')} and status='DRAFT'")

    with connection.cursor() as database:
        database.execute(f"update app_bid set status = 'ON_DELETE' where session_id='{request.session.get('session_id')}' and status='DRAFT'")


    return redirect('index')



def index(request):
    if not request.session.get('session_id'):
        request.session['session_id'] = str(uuid.uuid4())

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


def cart(request):
    orders = Bid.objects.filter(session_id = request.session.get('session_id'), status = 'DRAFT')

    if orders.exists():
        return render(request, 'animal.html')

    else:
        return redirect('index')

