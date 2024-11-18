from django.urls import path
from api import views

urlpatterns = [
    path('periods/<int:period_id>/', views.PeriodGetUpdateDeleteView.as_view()),
    path('periods/', views.PeriodListCreateView.as_view()),

    path('bids/periods/<int:period_id>/', views.PeriodInBidCreateView.as_view())
]