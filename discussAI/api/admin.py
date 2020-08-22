from django.contrib import admin

from .models import Document, Result, DocumentPages

admin.site.register(Document)
admin.site.register(Result)
admin.site.register(DocumentPages)
# Register your models here.
