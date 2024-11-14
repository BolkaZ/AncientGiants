from django.urls import path
from app import views
from app.views import index, getDetailPage, bid_view
from django.contrib import admin

urlpatterns = [
    path('', index, name='index'),
    path('detail/<int:id>/', getDetailPage, name='getDetailPage'),
    path('bid/', bid_view, name='bid'),
]
