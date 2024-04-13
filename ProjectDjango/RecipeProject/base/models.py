from django.db import models
from django.contrib.auth.models import User




# broad-category of some Topics
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name




class Recipe(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants =
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # for ordering the recipes in the order: recent first
        # '-' is for descending order
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name




# for conversation inside a recipe
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # returns only first 50 characters
        return self.body[0:50]
    