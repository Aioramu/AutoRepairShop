from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.RecordsView.as_view(), name='records_create'),
]
