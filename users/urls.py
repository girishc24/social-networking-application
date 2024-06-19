from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('signup/', views.UserCreate.as_view()),
    path('search/', views.UserSearchView.as_view()),
    path('friend-request/', views.FriendRequestView.as_view(), name='friend_request'),
    path('friend-request/<int:pk>/', views.FriendRequestView.as_view(), name='friend_request'),
    path('friends/', views.FriendsListView.as_view(), name='friends_list'),
]