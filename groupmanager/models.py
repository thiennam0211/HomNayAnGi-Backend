from django.db import models

# Create your models here.


class Group(models.Model):
    name = models.CharField(null=False, blank=False,
                            max_length=512, unique=True)
    password = models.CharField(null=True, blank=False, max_length=512)

    def __str__(self):
        return "{} - {} ".format(self.name, self.password)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
  

