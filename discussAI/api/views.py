from django.http import HttpResponse
from .models import Document, Result, DocumentPages, PositionArray
from .serializers import DocumentSerializer, ResultSerializer
from rest_framework.exceptions import ParseError
from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import sys
from pdf2image import convert_from_path 
import os
from resizeimage import resizeimage
from api.image import image_to_json
from api.image_resize import result_image

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
        # Store all the pages of the PDF in a variable 
        print(doc.pdf.name)
        try:
            link = 'https://discussai.blob.core.windows.net/media/' + doc.pdf.name
            pages = convert_from_path(link)
        except:
            print("Could not convert the file properly")
        # Counter to store images of each page of PDF to image 
        image_counter = 1
        # Iterate through all the pages stored above 
        print(pages)
        paths = []
        for page in pages:
            # Declaring filename for each page of PDF as JPG 
            # For each page, filename will be: 
            # PDF page 1 -> page_1.jpg 
            # PDF page 2 -> page_2.jpg 
            # PDF page 3 -> page_3.jpg 
            # ....
            # PDF page n -> pagen.jpg 
            filename = "page" + str(image_counter)+".png"
            new_image = resizeimage.resize_width(page, page.width)
            new_image_io = BytesIO()
            new_image.save(new_image_io, format='PNG')
            #print(a)
            # Increment the counter to update filename 
            image_counter = image_counter + 1
            final_image = ContentFile(new_image_io.getvalue())
            docPage = DocumentPages(pdf=doc, page=image_counter, image=InMemoryUploadedFile(
            final_image,       # file
            None,               # field_name
            filename,           # file name
            'image/png',       # content_type
            final_image.tell,  # size
            None))               # co)
            docPage.save()
            paths.append('https://discussai.blob.core.windows.net/media/' + docPage.image.name)
        
        print(paths)
        res = image_to_json(paths)
        print(res)
        arr = PositionArray(pdf=doc, array=res)
        arr.save()
        return Response({"Success": ""}, status=status.HTTP_201_CREATED)


class AskQuestionAPIView(APIView):
    serializer_class = ResultSerializer

    #def get_serializer_context(self):
    #    """ this function is used in the UserCreateSerializer to get
    #        the question """
    #    context = super(AskQuestionAPIView, self).get_serializer_context()
    #    context.update({"question": self.kwargs["question"]})
    #    return context

    def get(self, request, question):
        question = question.replace('_', ' ')
        print(question)
        a = question
        array = PositionArray.objects.get(pk=4).array
        for i in range (len(array)):
            string = array[i]
            string = string.replace('\'', '')
            string = string[1:-1]
            array[i] = string.split(', ')
            z = len(array[i])
            if z > 2:
                for x in range(7, z):
                    if array[i][x].lower() == a.lower():
                        url = array[i][0]
                        left = array[i][2]
                        top = array[i][3]
                        right = array[i][4]
                        bottom = array[i][5]
                        pos = i
                        print(pos)
                        link = result_image(url, int(left), int(top), int(right), int(bottom))
                        return Response({"link": link, "page": pos}, status=status.HTTP_202_ACCEPTED)
        return Response({"link": "", "page": 0}, status=status.HTTP_204_NO_CONTENT)
                        
     
