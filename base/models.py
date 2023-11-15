from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        'self', related_name='followed_by', symmetrical=False, blank=True)

    def __str__(self) -> str:
        return self.user.username


class Tweet(models.Model):
    user = models.ForeignKey(User, related_name='tweets',
                             on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.text[:64]


def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
        profile.follows.set([instance.profile.id])
        profile.save()


post_save.connect(create_profile, sender=User)
