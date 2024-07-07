from django.urls import path
from .views import (
    UserSignupView,
    UserLoginView,
    UserSearchView,
    SendFriendRequestView,
    AcceptFriendRequestView,
    RejectFriendRequestView,
    ListFriendsView,
    ListPendingFriendRequestsView
)

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='search'),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('friend-request/accept/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('friend-request/reject/<int:pk>/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
    path('friends/', ListFriendsView.as_view(), name='list_friends'),
    path('friend-requests/', ListPendingFriendRequestsView.as_view(), name='list_pending_friend_requests'),
]
