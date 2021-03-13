from django.db import models

# Create your models here.


class Company_Code(models.Model):
    code = models.CharField(max_length=10)


class Favorite_Code(models.Model):
    code = models.CharField(max_length=10)
    user = models.CharField(max_length=10)


class BoardModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=10)
    images_code = models.CharField(max_length=10)


class ImageModel(models.Model):
    images = models.ImageField(upload_to='')
