""" Simple Model Serializers """
from rest_framework import serializers

from .models import Document, Result


class DocumentSerializer(serializers.ModelSerializer):
    """ Serializer for documents to JSON """

    class Meta:
        model = Document
        fields = ['name', 'pdf']

class ResultSerializer(serializers.ModelSerializer):
    """ Serializer for results """

    class Meta:
        model = Result
        fields = ['link', 'page']
