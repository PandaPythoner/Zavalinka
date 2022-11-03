from django.urls import path
from sign_up.views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]