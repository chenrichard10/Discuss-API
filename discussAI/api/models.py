""" Defined Database Tables for Django """
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
class Document(models.Model):
    """ PDF Document Storage """
    name = models.CharField(max_length=200)
    pdf = models.FileField()

    def __str__(self):
        return self.name


class Result(models.Model):
    """ Processed Answer Storage """
    link = models.FileField()
    page = models.IntegerField()


class DocumentPages(models.Model):
    """ Splitted Images of PDFs """
    pdf = models.ForeignKey(Document, on_delete=models.CASCADE)
    page = models.IntegerField()
    image = models.FileField()


class PositionArray(models.Model):
    """ Position Array containing keywords """
    pdf = models.ForeignKey(Document, on_delete=models.CASCADE)
    array = ArrayField(models.CharField(max_length=200, blank=True), size=500)
