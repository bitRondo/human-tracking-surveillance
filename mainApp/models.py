from django.db import models


class Recipient(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

# Create your models here.
