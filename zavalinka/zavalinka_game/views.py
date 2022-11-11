from http.client import HTTPResponse
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from .models import UserInZavalinkaGame, ZavalinkaGame, Profile
from django.contrib.auth.models import User

# Create your views here.


def home_page_view(request):
    return render(request, "zavalinka_game/home_page.html")


def friends_list(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    profile = request.user.profile
    context = {"all_friends": profile.friends.all()}
    return render(request, "zavalinka_game/friends_list.html", context=context)

class ProfilePage(TemplateView):
    def get(self, request, user):
        profile_img = User.objects.get(username=user).profile.profile_pic
        users_profile = request.user.is_authenticated
        if users_profile:
            users_profile = users_profile & (user == request.user.username)
        context = {
            "profile_img":profile_img,
            "users_profile":users_profile,
            "user":user,
        }
        return render(request, "zavalinka_game/profile.html", context=context)
    def post(self, request):
        request.user.profile_img = request.POST.get("profimg")

class CreateGameView(TemplateView):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return render(request, 'zavalinka_game/create_game.html')

    def post(self, request):
        game = ZavalinkaGame.objects.create(rounds=request.POST.get("number_of_rounds"),
                                            name=request.POST.get("name"))
        user_in_game = UserInZavalinkaGame(user=request.user.profile, game=game)
        user_in_game.save()
        return HttpResponseRedirect(reverse('game') + '?game_id=' + str(game.id))

class GameView(TemplateView):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        if 'game_id' not in request.POST:
            return render(request, 'zavalinka_game/join_game_error.html')
        game_id = request.GET['game_id']
        games = ZavalinkaGame.objects.filter(id=game_id)
        if games.count() != 1:
            return render(request, 'zavalinka_game/join_game_error.html')
        user = request.user
        game = games[0]
        game_phase = str(game.phase)
        if game_phase == 'waiting_for_players':
            return render(request, 'zavalinka_game/game/waiting_for_players.html')
        if game_phase == 'writing_definitions':
            return render(request, 'zavalinka_game/game/writing_definitions.html')
        return render(request, 'zavalinka_game/game/game.html')

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        if 'game_id' not in request.GET:
            return render(request, 'zavalinka_game/join_game_error.html')
        game_id = request.GET['game_id']
        games = ZavalinkaGame.objects.filter(id=game_id)
        if games.count() != 1:
            return render(request, 'zavalinka_game/join_game_error.html')
        user = request.user
        game = games[0]
        game_phase = str(game.phase)
        users_in_game = UserInZavalinkaGame.objects.filter(game=game)
        context = {
            'game': game,
            'users_in_game':users_in_game,
        }
        if game_phase == 'waiting_for_players':
            return render(request, 'zavalinka_game/game/waiting_for_players.html', context=context)
        if game_phase == 'writing_definitions':
            return render(request, 'zavalinka_game/game/writing_definitions.html', context=context)
        return render(request, 'zavalinka_game/game/game.html', context=context)


class AllGamesView(TemplateView):
    def get(self, request):
        games = ZavalinkaGame.objects.all()
        context = {"games": [(game, {"users_str": ", ".join([str(user_in_game.user.user.username) for user_in_game in game.users.all()])}) for game in games]}
        return render(request, 'zavalinka_game/all_games.html', context=context)


class JoinGameView(TemplateView):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        if 'game_id' not in request.POST:
            return render(request, 'zavalinka_game/join_game_error.html')
        game_id = request.POST['game_id']
        games = ZavalinkaGame.objects.filter(id=game_id)
        if games.count() != 1:
            return render(request, 'zavalinka_game/join_game_error.html')
        user = request.user
        game = games[0]
        if not game.users.filter(user=user.profile).exists():
            user_in_game = UserInZavalinkaGame(user=user.profile, game=game)
            user_in_game.save()
        return HttpResponseRedirect(reverse('game') + '?game_id=' + str(game.id))


