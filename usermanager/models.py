from django.db import models

# Create your models here.


class Users(models.Model):
    email = models.CharField(null=False, blank=False, max_length=1024, unique=True)
    password = models.CharField(null=False, blank=False, max_length=512)
    full_name = models.CharField(null=False, blank=False, max_length=512)
    display_name = models.CharField(null=True, blank=False, max_length=512)
    gender = models.CharField(null=True, blank=False,
                              default='Male', max_length=20)
    birthday = models.DateField(
        default='1-1-1990', null=False, blank=False)
    avatar = models.URLField(null=True)


    # @classmethod
    # def create(cls, email, password, full_name, display_name, gender, birthday, avatar):
    #     new_red = cls(email=email, password=password, full_name=full_name,
    #                   display_name=display_name, gender=gender, birthday=birthday, avatar=avatar)
    #     return new_red

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
