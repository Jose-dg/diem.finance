from django.db import models
from django.contrib.auth import get_user_model

class CustomGroup(models.Model):
   name = models.CharField(max_length=255, unique=True)
   description = models.TextField(blank=True, null=True)
   members = models.ManyToManyField(get_user_model(), related_name='custom_groups')

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
      return self.name

