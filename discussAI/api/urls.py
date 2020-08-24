""" URL routing for API """
from django.urls import path

from . import views
from .views import AskQuestionAPIView, DocumentAPIView, DocumentUploadAPIView

urlpatterns = [
    path('', views.index, name='index'),
    path('document/', DocumentAPIView.as_view(), name='doc'),
    path('upload/<filename>', DocumentUploadAPIView.as_view()),
    path('ask/<str:question>', AskQuestionAPIView.as_view())
]
