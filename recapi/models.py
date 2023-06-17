from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User

import os
import uuid
import random

from datetime import datetime 

GENDERS = (
    ("MALE", "MALE"),
    ("FEMALE", "FEMALE"),
    ("OTHERS", "OTHERS")
)


def user_directory_path(instance, filename):

    path = "static/faces/"
    extension = "." + filename.split('.')[-1]


    # Filename reformat
    filename_reformat = str(instance.username) + extension

    return os.path.join(path, filename_reformat)


class UserProfile(models.Model):
    # MODEL FOR THE USER PROFILE
    username = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    # first_name
    # last_name
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDERS)
    married = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(max_length=100, blank=True, null=True)
    crime_committed = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()
    
    def get_criminal_data(self):
        # Getting the User's Firstname, Lastname
        criminal = User.objects.get(username=self.username)
        criminal_first_name = criminal.first_name
        criminal_last_name = criminal.last_name
        
        return (criminal_first_name, criminal_last_name)
    
    def __str__(self):
        first_name, last_name = self.get_criminal_data()
        return f"{self.username}: {first_name} {last_name}"
    
    class Meta:
        ordering = ["date_created"]
        
    
