from django.http import HttpResponse
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.exceptions import ParseError
from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

def index(request):
    """ Basic home page """
    return HttpResponse("Hello, world. You're at the discussAI main page.")

class DocumentAPIView(generics.ListAPIView):
    """ APIView for all documents """
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

class DocumentUploadAPIView(APIView):
    """ APIView for uploading images """
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format='pdf'):
        """" put request for uploading the pdfs """
        if 'file' not in request.data:
            raise ParseError("Empty content")
        f = request.data['file']
        doc = Document(name=filename, pdf=f)
        doc.save()
        return Response({"Success": "Brogey Groge"}, status=status.HTTP_201_CREATED)
