# Improting Image class from PIL module 
from PIL import Image
import requests
from io import BytesIO
from resizeimage import resizeimage
from .models import DocumentPages, Document
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile

# test case "https://discussai.blob.core.windows.net/media/page1_77tCnWq.png"
def result_image(url, left, top, right, bottom):
    response = requests.get(url)
    im = Image.open(BytesIO(response.content))
    # Size of the image in pixels (size of orginal image)
    # (This is not mandatory) 
    width, height = im.size 
    print(width)
    print(height)
    # Setting the points for cropped image 
    #left = 5
    #top = height / 4
    #right = 164
    #bottom = 3 * height / 4
    # Cropped image of above dimension 
    # (It will not change orginal image) 
    im1 = im.crop((left, top, right, bottom))
    # Shows the image in image viewer 
    filename = "result.png"
    new_image = resizeimage.resize_width(im1, im1.width)
    new_image_io = BytesIO()
    new_image.save(new_image_io, format='PNG')
    final_image = ContentFile(new_image_io.getvalue())
    docPage = DocumentPages(pdf=Document.objects.get(pk=1), page=42, image=InMemoryUploadedFile(
        final_image,       # file
        None,               # field_name
        filename,           # file name
        'image/png',       # content_type
        final_image.tell,  # size
        None))               # co)
    docPage.save()
    link = 'https://discussai.blob.core.windows.net/media/' + docPage.image.name
    return link
    im1.show()