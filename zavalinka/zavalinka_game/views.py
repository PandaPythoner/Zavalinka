from http.client import HTTPResponse
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

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