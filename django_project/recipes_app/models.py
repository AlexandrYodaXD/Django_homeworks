from django.contrib.auth.models import User
from django.db import models




class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    preparation_steps = models.TextField(max_length=4096)
    preparation_time = models.TimeField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)


class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)