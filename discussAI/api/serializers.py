from rest_framework import serializers
from .models import Document, Result

class DocumentSerializer(serializers.ModelSerializer):
    """ Serializer for documents to JSON """

    class Meta:
        model = Document
        fields = ['name', 'pdf']
        # Find the colour that is most aggregrated
        # Find colours that are not equal to aggregrated
        # If someone if not equal to black
        # Filter for italics

class ResultSerializer(serializers.ModelSerializer):
    """ Serializer for results """

    class Meta:
        model = Result
        fields = ['link', 'page']

