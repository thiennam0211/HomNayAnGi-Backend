from django.contrib.postgres.fields import ArrayField
from django.db import models

from usermanager import models as userModel


# Create your models here.


class Ingredients(models.Model):
    name = models.CharField(null=False, blank=False, max_length=1024, unique=True)
    possible_unit = ArrayField(models.TextField(null=True, blank=True), null=True, blank=True)


class Recipes(models.Model):
    title = models.CharField(null=False, blank=False, max_length=1024)
    dish_types = models.CharField(null=True, blank=True, max_length=1024)
    servings = models.IntegerField()
    readyInMinutes = models.IntegerField()
    summary = models.TextField()
    images = ArrayField(models.TextField(null=True, blank=True), null=True, blank=True)
    inductions = ArrayField(models.TextField(null=True, blank=True), null=True, blank=True)
    # ingredient = models.ManyToManyField(Ingredients, through='Recipe_Ingredients')
    author = models.ForeignKey(userModel.Users, on_delete=models.PROTECT, related_name='author')


class Recipe_Ingredients(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,  related_name='recipe')
    ingredient = models.ForeignKey(Ingredients, on_delete=models.PROTECT,  related_name='ingredient')
    amount = models.FloatField()
    unit = models.CharField(null=True, blank=True, max_length=1024)

    class Meta:
        unique_together = [['recipe', 'ingredient']]

