from django.db import models

# Create your models here.

class Contact(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    query = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name




class Cuser(models.Model): 
    id = models.BigAutoField(primary_key=True) 
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to ='static/client/', null=True, blank=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    salary = models.IntegerField()
    gender = models.CharField(max_length=30)
    mothertoug = models.CharField(max_length=30)
    reigion = models.CharField(max_length=30)
    occupation = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.username


class Friend(models.Model):
    id = models.BigAutoField(primary_key=True) 
    username = models.CharField(max_length=30)
    touser = models.CharField(max_length=30)
    request = models.BooleanField()
    room = models.CharField(max_length=30)
    date = models.DateField()

    def __str__(self):
        return self.room