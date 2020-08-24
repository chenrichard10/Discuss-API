""" Admin settings for Django project """
from django.contrib import admin

from .models import Document, DocumentPages, PositionArray, Result

admin.site.register(Document)
admin.site.register(Result)
admin.site.register(DocumentPages)
admin.site.register(PositionArray)
# Register your models here.
