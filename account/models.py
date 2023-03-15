from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Extending User Model Using a One-To-One Link
class Profile(models.Model):


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)


    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('bio_update', kwargs={'pk': self.pk})