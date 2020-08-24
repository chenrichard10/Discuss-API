""" Views that handle requests """
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from pdf2image import convert_from_path
from resizeimage import resizeimage
from rest_framework import generics, status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from api.image import image_to_json
from api.image_resize import result_image
from .models import Document, DocumentPages, PositionArray, Result
from .serializers import DocumentSerializer, ResultSerializer


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
    # format = 'pdf' if issues occur
    def put(self, request, filename):
        """" put request for uploading the pdfs """
        if 'file' not in request.data:
            raise ParseError("Empty content")
        file_data = request.data['file']
        doc = Document(name=filename, pdf=file_data)
        doc.save()
        # Store all the pages of the PDF in a variable
        link = 'https://discussai.blob.core.windows.net/media/' + doc.pdf.name
        pages = convert_from_path(link)
        # Counter to store images of each page of PDF to image
        image_counter = 1
        # Iterate through all the pages stored above
        print(pages)
        paths = []
        for page in pages:
            # Declaring filename for each page of PDF as JPG
            filename = "page" + str(image_counter)+".png"
            new_image = resizeimage.resize_width(page, page.width)
            new_image_io = BytesIO()
            new_image.save(new_image_io, format='PNG')
            #print(a)
            # Increment the counter to update filename
            image_counter = image_counter + 1
            final_image = ContentFile(new_image_io.getvalue())
            doc_page = DocumentPages(pdf=doc, page=image_counter, image=InMemoryUploadedFile(
                final_image,       # file
                None,               # field_name
                filename,           # file name
                'image/png',       # content_type
                final_image.tell,  # size
                None))               # co)
            doc_page.save()
            paths.append('https://discussai.blob.core.windows.net/media/' + doc_page.image.name)

        res = image_to_json(paths)
        arr = PositionArray(pdf=doc, array=res)
        arr.save()
        return Response({"Success": ""}, status=status.HTTP_201_CREATED)


class AskQuestionAPIView(APIView):
    """ View for handling questions """
    serializer_class = ResultSerializer

    def get(self, request, question):
        """ Returns a screenshot of answer in textbook """
        question = question.replace('_', ' ')
        array = PositionArray.objects.get(pk=4).array
        for i in range(len(array)):
            string = array[i]
            string = string.replace('\'', '')
            string = string[1:-1]
            array[i] = string.split(', ')
            length = len(array[i])
            if length > 2:
                for x in range(7, length):
                    if array[i][x].lower() == question.lower():
                        url = array[i][0]
                        left = array[i][2]
                        top = array[i][3]
                        right = array[i][4]
                        bottom = array[i][5]
                        pos = i
                        print(pos)
                        link = result_image(url, int(left), int(top), int(right), int(bottom))
                        return Response({"link": link, "page": pos}, status=status.HTTP_202_ACCEPTED)
        return Response({"link": " ", "page": 0}, status=status.HTTP_202_ACCEPTED)
