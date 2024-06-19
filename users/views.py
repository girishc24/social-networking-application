from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import UserSerializer, FriendRequestSerializer
from rest_framework import status
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from . models import FriendRequest
from django.utils import timezone
from datetime import timedelta

def welcome(request):
    return  HttpResponse("Welcome Social Network")

#user Signup 
class UserCreate(APIView):
   
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            if User.objects.filter(email=email).exists():
                return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# USER SEARCH
class UserSearchView(APIView):
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
     

    def get(self, request):
        search_term = request.data.get('search_term')
        users = User.objects.filter(Q(email__icontains=search_term) | 
                                    Q(first_name__icontains=search_term) | 
                                    Q(last_name__icontains=search_term))
        paginator = PageNumberPagination()
        paginator.page_size = 10 
        
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

# Friends Request SEND, ACCEPT, REJECT
class FriendRequestView(APIView):
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def post(self, request):
        user_id = request.data.get('user_id')
        if request.user.id == user_id:
            return Response({'error': 'Cannot send friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)
        if FriendRequest.objects.filter(from_user=request.user, to_user_id=user_id).exists():
            return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
        
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(
            from_user=request.user,
            timestamp__gte=one_minute_ago
        ).count()

        if recent_requests_count >= 3:
            return Response({'error': 'Cannot send more than 3 friend requests within a minute'}, status=status.HTTP_400_BAD_REQUEST)
        
        friend_request = FriendRequest.objects.create(from_user=request.user, to_user_id=user_id, status='pending')
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data,  status=status.HTTP_201_CREATED)
    
    def get(self, request):
        friend_requests = FriendRequest.objects.filter(from_user=request.user, status='pending')
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(pk=pk)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

        request_status = request.data.get('status')
        if request_status in ['accepted', 'rejected']:
            if request_status == 'rejected':
                friend_request.delete()
                return Response({"message": "Friend request rejected"}, status=status.HTTP_200_OK)
            else:
                friend_request.status = request_status
                friend_request.save()
                return Response({"message": "Friend request Accepted"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

# Friends List
class FriendsListView(APIView):
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])

    def get(self, request):
        friends = FriendRequest.objects.filter(from_user=request.user, status='accepted')
        friend_list = [request.to_user for request in friends]
        #print(friend_list)
        serializer = UserSerializer(friend_list, many=True)
        return Response(serializer.data)