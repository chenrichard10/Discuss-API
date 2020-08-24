""" This Module is primarily used for screenshotting
a resized image from Azure's bounding box results """
from io import BytesIO

import requests
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from resizeimage import resizeimage

from .models import Document, DocumentPages


# test case "https://discussai.blob.core.windows.net/media/page1_77tCnWq.png"
def result_image(url, left, top, right, bottom):
    """ Returns a resized image of PDF page based on bounding box """
    response = requests.get(url)
    byte_array = Image.open(BytesIO(response.content))
    # Size of the image in pixels (size of orginal image)
    # (This is not mandatory)
    width, height = byte_array.size
    im1 = byte_array.crop((left, top, right, bottom))
    # Shows the image in image viewer
    filename = "result.png"
    new_image = resizeimage.resize_width(im1, im1.width)
    new_image_io = BytesIO()
    new_image.save(new_image_io, format='PNG')
    final_image = ContentFile(new_image_io.getvalue())
    doc_page = DocumentPages(pdf=Document.objects.get(pk=1), page=42, image=InMemoryUploadedFile(
        final_image,       # file
        None,               # field_name
        filename,           # file name
        'image/png',       # content_type
        final_image.tell,  # size
        None))               # co)
    doc_page.save()
    link = 'https://discussai.blob.core.windows.net/media/' + doc_page.image.name
    return link
    im1.show()
