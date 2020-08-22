from django.http import HttpResponse
from .models import Document
from .serializers import DocumentSerializer
from rest_framework import generics

def index(request):
    return HttpResponse("Hello, world. You're at the discussAI main page.")

class DocumentAPIView(generics.ListAPIView):
    """ APIView for all documents """
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()