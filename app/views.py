import uuid
from django.shortcuts import get_object_or_404, redirect
from .models import Period, Bid, Animal
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.db import connection

USER_ID = 1


def bid_view(request):

    orders = Bid.objects.filter(session_id = request.session.get('session_id'), status = 'DRAFT')

    if orders.exists():
        return render(request, 'animal.html', context = {'order': orders.first()})

    else:
        return redirect('animal.html')


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

