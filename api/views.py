from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterSerializer

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': (user).data,
                'token': token.key,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def get(self, request):
        return Response({'message': 'Please use POST to register a new user'}, status=status.HTTP_200_OK)
