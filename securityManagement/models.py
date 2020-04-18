from django.db import models

class Recipient(models.Model):
    register_num = models.IntegerField(unique = True)

    name = models.CharField(max_length=200)
    
    email = models.EmailField(
        max_length=200,
        unique = True,
        error_messages = {
            'unique': "The email is already being used by a recipient.",
        },
    )

# Create your models here.
