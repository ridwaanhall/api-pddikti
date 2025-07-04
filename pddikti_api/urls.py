from django.urls import path
from .views import APIOverview

urlpatterns = [
    # api overview
    path('', APIOverview.as_view(), name='api-overview'),
]
