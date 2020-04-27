from django.db import models
from django.contrib.auth.models import auth,User

# Create your models here.

class Card_Detailss(models.Model):
    holder_name = models.CharField(max_length=225)
    cvv = models.CharField(max_length=225)
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    card_no = models.CharField(max_length=225)
    expiry = models.DateField()

class Profile(models.Model):
    hobby = models.CharField(max_length=225)
    interst_area = models.CharField(max_length=225)
    Puser = models.ForeignKey(User,on_delete=models.PROTECT)
    location = models.CharField(max_length=225)
    fav_author = models.CharField(max_length=225)

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profilee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profilee.objects.create(user=instance)
        instance.profilee.save()
