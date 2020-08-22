from django.db import models

# Create your models here.
class Document(models.Model):
    name = models.CharField(max_length=200)
    pdf = models.FileField()

    def __str__(self):
        return self.name

class Result(models.Model):
    link = models.FileField()
    page = models.IntegerField()
   
class DocumentPages(models.Model):
    pdf = models.ForeignKey(Document, on_delete=models.CASCADE)
    page = models.IntegerField()
    image = models.FileField()

