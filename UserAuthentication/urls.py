from django.urls import path
from .views import *


urlpatterns = [
    path('show-users', ListUsers.as_view()),
    path('register', RegisterUser.as_view()),
    path('login', LoginView.as_view()),
    path('get-user', UserProfileView.as_view()),
    path('update-user', UpdateUserDetails.as_view()),
    path('change-password', UpdatePassword.as_view()),
    path('save-progress', SaveProgress.as_view()),
    path('view-progress', ViewProgress.as_view()),
    path('teachers-list', Teachers.as_view()),
]
