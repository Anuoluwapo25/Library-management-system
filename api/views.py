from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import UserRegistrationSerializer

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