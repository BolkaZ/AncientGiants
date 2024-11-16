from django.urls import path
from api import views

urlpatterns = [
    path('periods/<int:period_id>/', views.PeriodGetView.as_view()),
    path('periods/', views.PeriodListView.as_view()),
]