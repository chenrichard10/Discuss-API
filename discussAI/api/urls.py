from django.urls import path
from . import views
from .views import DocumentAPIView

urlpatterns = [
    path('', views.index, name='index'),
    path('document/', DocumentAPIView.as_view(), name='doc')
]