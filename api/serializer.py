from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'account_type', 'country', 
                 'country_code', 'state', 'address', 'phone_number']
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        name = validated_data.pop('first_name')
        user = User.objects.create(
            username=validated_data['email'],  # Using email as username
            first_name=name,
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user