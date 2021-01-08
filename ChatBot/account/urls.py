from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/<slug:user>/', views.user_profile, name='profile'),
    path('comments/<int:comment_to>/<int:commenter>/', views.comments, name='comments'),
    path('profile/likes/<int:comment_owner>/', views.likes, name='likes'),
]