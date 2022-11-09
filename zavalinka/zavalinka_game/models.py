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


class ZavalinkaWord(models.Model):
    word = models.CharField(max_length=200)
    definition = models.CharField(max_length=2000)

    def __str__(self):
        return f"{self.word}: {self.definition}"


class UserInZavalinkaGame(models.Model):
    user = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    game = models.ForeignKey('ZavalinkaGame', on_delete=models.CASCADE, related_name='users')
    last_answer = models.CharField(max_length=2000, default='')

    def __str__(self):
        return str(self.user)

class ZavalinkaGame(models.Model):
    round = models.IntegerField(default=0)
    PHASES = ['writing_definitions', 'choosing_definition']
    phase = models.CharField(max_length=100, default=PHASES[0])
    last_ask = models.ForeignKey('ZavalinkaWord', default=4, on_delete=models.PROTECT)

    def get_new_phase_and_round(self):
        phase = str(self.phase)
        round = int(self.round)
        PHASES = self.PHASES
        for i in range(len(PHASES)):
            if PHASES[i] == phase:
                if i + 1 < len(PHASES):
                    return (PHASES[i + 1], round)
                return (PHASES[0], round + 1)


    def __str__(self):
        rs = f"Game number {str(self.id)}"
        if len(self.users.all()) < 10:
            rs += f" (Users: {' '.join(map(str, self.users.all()))})"
        return rs