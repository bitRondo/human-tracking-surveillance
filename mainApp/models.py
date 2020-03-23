from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100, unique = True)
    mobile_number = models.CharField(max_length = 15, unique = True)

    def __str__(self):
        return self.first_name

class UserCredential(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    username = models.CharField(max_length = 50, primary_key = True)
    password = models.CharField(max_length = 150)
    access_level = models.IntegerField(default = 0)

    def __str__(self):
        return self.username