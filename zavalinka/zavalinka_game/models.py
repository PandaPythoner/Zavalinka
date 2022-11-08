from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('Profile', blank=True)
    profile_pic = models.ImageField(null=True, blank=True, default='default_icon.png')
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class UserInZavalinkaGame(models.Model):
    user = models.ForeignKey(to=Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

class ZavalinkaGame(models.Model):
    users = models.ManyToManyField('UserInZavalinkaGame', blank=True)
    round = models.IntegerField(default=0)

    def __str__(self):
        rs = f"Game number {str(self.id)}"
        if len(self.users.all()) < 10:
            rs += f" (Users: {' '.join(map(str, self.users.all()))})"
        return rs