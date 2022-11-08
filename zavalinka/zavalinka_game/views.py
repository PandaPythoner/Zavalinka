from http.client import HTTPResponse
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from .models import UserInZavalinkaGame, ZavalinkaGame

# Create your views here.


def home_page_view(request):
    return render(request, "zavalinka_game/home_page.html")


def friends_list(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    profile = request.user.profile
    context = {"all_friends": profile.friends.all()}
    return render(request, "zavalinka_game/friends_list.html", context=context)

def profile(request, user):
    return render(request, "zavalinka_game/profile.html")

class CreateGamgeView(TemplateView):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return render(request, 'zavalinka_game/create_game.html')

    def post(self, request):
        game = ZavalinkaGame()
        user_in_game = UserInZavalinkaGame(user=request.user.profile)
        game.save()
        user_in_game.save()
        game.users.add(user_in_game)
        game.save()
        user_in_game.save()
        return HttpResponseRedirect(reverse('game') + '?game_id=' + str(game.id))

class GameView(TemplateView):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return render(request, 'zavalinka_game/game.html')


class AllGamesView(TemplateView):
    def get(self, request):
        games = ZavalinkaGame.objects.all()
        context = {"games": [(game, {"users_str": ", ".join([str(user_in_game.user.user.username) for user_in_game in game.users.all()])}) for game in games]}
        return render(request, 'zavalinka_game/all_games.html', context=context)


class JoinGameView(TemplateView):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        game_id = request.POST['game_id']
        games = ZavalinkaGame.objects.filter(id=game_id)
        if games.count() != 1:
            return render(request, 'zavalinka_game/join_game_error.html')
        user = request.user
        user_in_game = UserInZavalinkaGame(user=user.profile)
        user_in_game.save()
        game = games[0]
        if not game.users.filter(user=user.profile).exists():
            game.users.add(user_in_game)
            game.save()
        return HttpResponseRedirect(reverse('game') + '?game_id=' + str(game.id))


