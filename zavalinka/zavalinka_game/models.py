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
    score = models.IntegerField(default=0)
    not_answered = models.BooleanField(default=1)

    def __str__(self):
        return str(self.user)

class ZavalinkaGame(models.Model):
    name = models.CharField(max_length=200, default="Игра бебра")
    round = models.IntegerField(default=1)
    rounds = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    PHASES = ['waiting_for_players', 'writing_definitions', 'choosing_definition', 'endscreen']
    phase = models.CharField(max_length=100, default=PHASES[0])
    last_ask = models.ForeignKey('ZavalinkaWord', default=1, on_delete=models.PROTECT)

    def get_new_phase_and_round(self):
        phase = str(self.phase)
        round = int(self.round)
        rounds = int(self.rounds)
        PHASES = self.PHASES
        for i in range(0, len(PHASES) - 1):
            if PHASES[i] == phase:
                if i + 1 < len(PHASES) - 1:
                    return (PHASES[i + 1], round)
                if round == rounds:
                    return (PHASES[i + 1], round)
                return (PHASES[1], round + 1)
    
    def next_phase(self):
        phase = str(self.phase)
        round = int(self.round)
        PHASES = self.PHASES
        for i in range(0, len(PHASES) - 1):
            if PHASES[i] == phase:
                if i + 1 < len(PHASES) - 1:
                    self.phase = PHASES[i + 1]
                elif round == rounds:
                    self.phase = PHASES[i + 1]
                else:
                    self.phase = PHASES[1]
                    self.round += 1
                self.save()
                break

    def __str__(self):
        rs = f"Game number {str(self.id)}"
        if len(self.users.all()) < 10:
            rs += f" (Users: {' '.join(map(str, self.users.all()))})"
        return rs