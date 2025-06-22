from django.shortcuts import render
from .models import CustomUser, Profile
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . serializers import SignupSerializer, LoginSerializer,UserProfileSerializer,ProfileSerializer,UserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse

def example_view(request):
    return HttpResponse("Authentication app is working.")

class LoginView(APIView):
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)



class SignupAPIView(APIView):
     def post(self, request):

         
          serializer = SignupSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          data = serializer.data
          response = status.HTTP_201_CREATED
    
          return Response(data, status=response)
     

class UserView(APIView):
    permission_classes = [IsAuthenticated]   

    def post(self, request):
        user = request.user
        if hasattr(user, 'profile'):
            return Response({'detail': 'Profile already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Profile created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
     user = request.user

     # User data
     user_data = {
          "full_name": request.data.get("full_name", user.full_name),
          "email": request.data.get("email", user.email),
     }

     # Profile data
     profile_data = {}
     if "mobile_number" in request.data:
          profile_data["mobile_number"] = request.data["mobile_number"]
     if "avatar" in request.FILES:
          profile_data["avatar"] = request.FILES["avatar"]

     # Serializers
     user_serializer = UserSerializer(user, data=user_data, partial=True)

     #  Check if profile exists
     if hasattr(user, 'profile'):
          profile_serializer = ProfileSerializer(user.profile, data=profile_data, partial=True, context={'request': request})
     else:
          # Create a new profile if it doesn't exist
          profile_serializer = ProfileSerializer(data=profile_data, context={'request': request})

     # Validate both
     if user_serializer.is_valid() and profile_serializer.is_valid():
          user_serializer.save()

          # Save profile (create or update)
          if hasattr(user, 'profile'):
               profile_serializer.save()
          else:
               profile_serializer.save(user=user)

          return Response({'detail': 'Profile updated successfully'}, status=status.HTTP_200_OK)

     return Response({
          'user_errors': user_serializer.errors,
          'profile_errors': profile_serializer.errors
     }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes =[IsAuthenticated]
    def post(self,request):
        try:
          refresh_token = request.data['refresh']
          token = RefreshToken(refresh_token)
          token.blacklist()
          return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST) 


class AlluserView(APIView):
    def get(self,request):
        queryset=CustomUser.objects.all()
        serializer = UserProfileSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
