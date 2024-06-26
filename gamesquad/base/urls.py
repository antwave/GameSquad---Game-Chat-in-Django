from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutView, name="logout"),
    path("register/", views.registerView, name="register"),
    path("", views.home, name="home"),
    path("room/<int:pk>/", views.room, name="room"),
    path("profile/<int:pk>/", views.userProfile, name="user-profile"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<int:pk>/", views.updateRoom, name="update-room"),
    path("delete-room/<int:pk>/", views.deleteRoom, name="delete-room"),
    path("delete-message/<int:pk>/", views.deleteMessage, name="delete-message"),
    path("edit-user/", views.editUser, name="edit-user"),
    path("games/", views.gamesPage, name="games"),
    path("activities/", views.activityPage, name="activities"),
]
