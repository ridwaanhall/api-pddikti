from django.urls import path
from . import views

urlpatterns = [
    # api overview
    path('', views.APIOverview.as_view(), name='api-overview'),
]
