from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

User = get_user_model()

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        query = self.request.query_params.get('q')
        if '@' in query:
            return User.objects.filter(email__iexact=query)
        return User.objects.filter(Q(username__icontains=query) | Q(email__icontains(query)))

class SendFriendRequestView(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        to_user = User.objects.get(id=self.request.data.get('to_user'))
        serializer.save(from_user=self.request.user, to_user=to_user)

class AcceptFriendRequestView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.to_user == request.user and instance.status == 'pending':
            instance.status = 'accepted'
            instance.save()
            return Response(FriendRequestSerializer(instance).data)
        return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

class RejectFriendRequestView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.to_user == request.user and instance.status == 'pending':
            instance.status = 'rejected'
            instance.save()
            return Response(FriendRequestSerializer(instance).data)
        return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            Q(sent_requests__to_user=self.request.user, sent_requests__status='accepted') |
            Q(received_requests__from_user=self.request.user, received_requests__status='accepted')
        ).distinct()

class ListPendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')
