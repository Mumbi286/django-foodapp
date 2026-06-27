# Defining my own custom managers
from django.db import models


class ItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
    # returns the items that are soft deleted
    def deleted(self):
        return super().get_queryset().filter(is_deleted=True)