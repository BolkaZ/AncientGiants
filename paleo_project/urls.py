from django.urls import path
from app import views
from app.views import index, getDetailPage, bid_view, add_to_bid
from django.contrib import admin

urlpatterns = [
    path('', index, name='index'),
    path('detail/<int:id>/', getDetailPage, name='getDetailPage'),
    path('bid/', bid_view, name='bid'),
    path('add-to-bid/<int:period_id>/', views.add_to_bid, name='add_to_bid'),
    path('admin/', admin.site.urls),
    path('clear_bid/', views.clear_bid, name='clear_bid'),
    #path('bid/<int:bid_id>/', bid_view, name='bid_detail'),  # для конкретной заявки
]
