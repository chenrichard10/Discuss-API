from django.contrib import admin

from .models import Document, Result, DocumentPages, PositionArray

admin.site.register(Document)
admin.site.register(Result)
admin.site.register(DocumentPages)
admin.site.register(PositionArray)
# Register your models here.
