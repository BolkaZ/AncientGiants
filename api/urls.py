from django.urls import path
from api import views

urlpatterns = [
    # Period
    path('periods/<int:period_id>/', views.PeriodGetUpdateDeleteView.as_view()),
    path('periods/<int:period_id>/images/', views.PeriodImageCreateView.as_view()),
    path('periods/', views.PeriodListCreateView.as_view()),

    # Period/M2M(BidPeriod)
    path('bids/periods/<int:period_id>/', views.PeriodInBidCreateDeleteUpdateView.as_view()),

    # Bid
    path('bids/', views.BidListView.as_view()),
    path('bids/<int:bid_id>/', views.BidGetUpdateDeleteView.as_view()),
    path('bids/<int:bid_id>/form/', views.BidFormView.as_view()),
    path('bids/<int:bid_id>/moderation/', views.BidModerationView.as_view()),

    # User
    path('users/', views.UserCreateView.as_view()),
    path('users/<int:user_id>/', views.UserUpdateView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('logout/', views.UserLogoutView.as_view()),

    # Set session_id
    path('session/<str:session_id>/', views.SessionCreateView.as_view())
]