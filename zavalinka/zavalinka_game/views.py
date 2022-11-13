from http.client import HTTPResponse
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from .models import UserInZavalinkaGame, ZavalinkaGame, Profile
from django.contrib.auth.models import User
from random import shuffle

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
    def post(self, request, user):
        
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
        game_id = request.POST['game_id']
        games = ZavalinkaGame.objects.filter(id=game_id)
        if games.count() != 1:
            return render(request, 'zavalinka_game/join_game_error.html')
        user = request.user
        game = games[0]
        game_phase = game.phase
        users_in_game = game.users.all()
        if game_phase == 'waiting_for_players':
            game.next_phase()
        if game_phase == 'writing_definitions':
            users_in_game.get(user=user.profile, game=game).user_answered(request.POST['definition'])
            game.user_answered()
            num_of_ans = game.status
            if num_of_ans == users_in_game.count():
                game.next_phase()
        if game_phase == 'choosing_definition':
            users_in_game.get(user=user.profile, game=game).user_chose(request.POST['definition'])
            game.user_answered()
            num_of_ans = game.status
            if num_of_ans == users_in_game.count():
                for user_in_game in users_in_game:
                    if user_in_game.last_choice == str(game.last_ask.definition):
                        user_in_game.change_score(3)
                    else:
                        for user in users_in_game.filter(last_answer=user_in_game.last_choice):
                            user.change_score(1)
                game.next_phase()
        if game_phase == 'round_results':
            game.next_phase()
        return HttpResponseRedirect(reverse('game') + '?game_id=' + str(game.id))
        

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
        users_in_game = game.users.all()
        context = {
            'game': game,
            'users_in_game':users_in_game,
            'user_answered':users_in_game.get(user=user.profile).not_answered,
        }
        if game_phase == 'waiting_for_players':
            return render(request, 'zavalinka_game/game/waiting_for_players.html', context=context)
        if game_phase == 'writing_definitions':
            return render(request, 'zavalinka_game/game/writing_definitions.html', context=context)
        if game_phase == 'choosing_definition':
            definitions = [game.last_ask.definition]
            for user_in_game in users_in_game:
                definitions.append(user_in_game.last_answer)
            shuffle(definitions)
            context['definitions'] = definitions
            return render(request, 'zavalinka_game/game/choosing_definition.html', context=context)
        if game_phase == 'round_results':
            return render(request, 'zavalinka_game/game/round_results.html', context=context)
        if game_phase == 'endscreen':
            max_score = -1
            winner = None
            for user_in_game in users_in_game:
                if max_score < user_in_game.score:
                    max_score = user_in_game.score
                    winner = str(user_in_game)
            context['winner'] = winner
            return render(request, 'zavalinka_game/game/endscreen.html', context=context)


class AllGamesView(TemplateView):
    def get(self, request):
        games = ZavalinkaGame.objects.exclude(phase__exact='endscreen')
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


