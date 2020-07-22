from django.db import models

from usermanager.models import Users
from RecipesManager.models import Ingredients

from django.utils import timezone


# Create your models here.
class Food(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user')
    food = models.ForeignKey(Ingredients, on_delete=models.CASCADE, related_name="food")
    amount = models.FloatField(null=False)
    unit = models.CharField(max_length=1024)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user', 'food']]

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.created_at = timezone.now()
    #     self.update_at = timezone.now()
    #     return super(Food, self).save(*args, **kwargs)
