from django.urls import path
from app import views
from app.views import index, getDetailPage, bid_view, add_to_bid
from django.contrib import admin
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('api.urls')),
    
    path('', index, name='index'),
    path('detail/<int:id>/', getDetailPage, name='getDetailPage'),
    path('bid/<int:bid_id>/', bid_view, name='bid'),
    path('add-to-bid/<int:period_id>/', views.add_to_bid, name='add_to_bid'),
    path('clear_bid/<int:bid_id>/', views.clear_bid, name='clear_bid'),

    #path('bid/<int:bid_id>/', bid_view, name='bid_detail'),  # для конкретной заявки
]
