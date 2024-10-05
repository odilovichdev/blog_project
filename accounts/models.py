from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profiles')
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username
