from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page_view, name='home_page'),
    path('friends_list/', views.friends_list, name='friends_list'),
    path('profile/<str:user>/', views.profile, name="profile"),
    path('create_game/', views.CreateGamgeView.as_view(), name="create_game"),
    path('game/', views.GameView.as_view(), name='game'),
]