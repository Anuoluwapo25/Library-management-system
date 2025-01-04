from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'country', 'countrycode', 
                 'state', 'address', 'phoneNumber')
        read_only_fields = ('id',)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'password', 'country', 'countrycode', 
                 'state', 'address', 'phoneNumber')
        extra_kwargs = {
            'country': {'required': False},
            'countrycode': {'required': False},
            'state': {'required': False},
            'address': {'required': False},
            'phoneNumber': {'required': False}
        }

    def create(self, validated_data):
        User = get_user_model()
        
        # Set default values for optional fields
        validated_data.setdefault('country', '')
        validated_data.setdefault('countrycode', None)
        validated_data.setdefault('state', '')
        validated_data.setdefault('address', '')
        validated_data.setdefault('phoneNumber', '')
        
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            country=validated_data['country'],
            countrycode=validated_data['countrycode'],
            state=validated_data['state'],
            address=validated_data['address'],
            phoneNumber=validated_data['phoneNumber'],
            password=validated_data['password']  # create_user will hash the password
        )
        
        return user