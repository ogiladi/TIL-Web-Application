# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=256, null=True)
    external_url = models.CharField(max_length=1000, null=True)
    post_url = models.CharField(max_length=1000, null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.title