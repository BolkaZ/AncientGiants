from django.urls import path
from app import views
from app.views import index, getDetailPage, bid_view, add_to_bid
from django.contrib import admin
from django.urls import include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Paleo Project",
      default_version='v1',
      description="Документация для проекта - Paleo Project.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="my_email@snmy_emailippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('api.urls')),
    
    path('', index, name='index'),
    path('detail/<int:id>/', getDetailPage, name='getDetailPage'),
    path('bid/<int:bid_id>/', bid_view, name='bid'),
    path('add-to-bid/<int:period_id>/', views.add_to_bid, name='add_to_bid'),
    path('clear_bid/<int:bid_id>/', views.clear_bid, name='clear_bid'),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    #path('bid/<int:bid_id>/', bid_view, name='bid_detail'),  # для конкретной заявки
]
