from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page_view, name='home_page'),
    path('friends_list/', views.friends_list, name='friends_list'),
    path('profile/<str:user>/', views.ProfilePage.as_view(), name="profile"),
    path('create_game/', views.CreateGameView.as_view(), name="create_game"),
    path('game/', views.GameView.as_view(), name='game'),
    path('all_games/', views.AllGamesView.as_view(), name='all_games'),
    path('join_game/', views.JoinGameView.as_view(), name='join_game'),
    path('add_words/', views.AddWordsView.as_view(), name='add_words'),
]