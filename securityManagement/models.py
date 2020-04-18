from django.db import models

class Recipient(models.Model):
    register_num=models.IntegerField()
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)

# Create your models here.
