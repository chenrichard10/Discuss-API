from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    """ Serializer for documents to JSON """

    class Meta:
        model = Document
        fields = ['name', 'pdf']