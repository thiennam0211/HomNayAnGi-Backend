from django.urls import path
from .views import ListUsersView, ListCreateUsersView, UsersDetailView, UserLoginView, UserForgotPasswordView, UserUpdateAvatar, GetAvatarImage

urlpatterns = [
    path('', ListUsersView.as_view(), name='user-list'),
    path('create', ListCreateUsersView.as_view(), name='user-create'),
    path('<int:pk>', UsersDetailView.as_view(), name='user-detail'),
    path('login', UserLoginView.as_view(), name='login'),
    path('forgot-password', UserForgotPasswordView.as_view(), name='forgot-password'),
    path('<int:pk>/update-avatar', UserUpdateAvatar.as_view(), name='update-avatar'),
    path('get-img', GetAvatarImage.as_view(), name='get-avatar'),
]
