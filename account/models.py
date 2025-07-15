from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.webp')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['emails']
    

    def __str__(self):
        return self.username