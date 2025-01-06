from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models.query import QuerySet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializer import UserRegistrationSerializer, LoginSerializer, UserDataSerializer, ResetPasswordSerializer
from .models import User
from datetime import datetime

class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                
                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                
                response_data = {
                    "status": status.HTTP_201_CREATED,
                    "message": "User registered successfully",
                    "data": {
                        "token": token,
                        "user": {
                            "email": user.email,
                            "name": user.first_name,
                            "accountType": user.account_type,
                            "country": user.country,
                            "state": user.state,
                            "address": user.address,
                            "phoneNumber": user.phone_number
                        }
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access
    authentication_classes = []      # No authentication required for login
    
    http_method_names = ['post'] 
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'status': 400,
                    'message': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.validated_data['user']
            
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Get user data
            user_data = UserDataSerializer(user).data

            return Response({
                'status': 200,
                'message': 'Login successful',
                'data': {
                    'token': access_token,
                    'user': user_data
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 500,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ResetpasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'status': 400,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data.get("user")  
        
        if user is None:
            return Response({
                'status': 400,
                'message': 'User not found or invalid token/email.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = serializer.validated_data["password"]
        user.set_password(new_password)
        user.save()

        return Response({
            "status": 200,
            "message": "User password reset successfully",
            "data": {
                "email": user.email,
                "id": user.id,
                "name": user.get_full_name()
            }
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data.get('refresh_token')
            
            if refresh_token:
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                "status": 200,
                "message": "User logged out successfully",
                "data": {
                    "user_id": request.user.id,
                    "logout_time": datetime.datetime.now()
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": 400,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

