from rest_framework import serializers
from .models import User, Book, Author, Borrow
from django.contrib.auth import authenticate


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
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Check if user exists
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError({
                    'status': 400,
                    'message': 'User with this email does not exist'
                })
            
            
            user = authenticate(username=email, password=password)  
            # Using email as username
            if not user:
                raise serializers.ValidationError({
                    'status': 400,
                    'message': 'Invalid credentials'
                })

            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError({
            'status': 400,
            'message': 'Both email and password are required'
        })

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'account_type', 'country', 
                 'country_code', 'state', 'address', 'phone_number']
        

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first() 
        if not user:
            raise serializers.ValidationError('User not found')
        data['user'] = user 
        return data

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']  

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'description', 'availability', 'created_at']

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author, created = Author.objects.get_or_create(**author_data)
        return Book.objects.create(author=author, **validated_data)
    
    def update(self, instance, validated_data):
        
        author_data = validated_data.pop('author', None)

        instance.title = validated_data.get('title', instance.title)
        instance.save()

        
        if author_data:
            author_instance = instance.author
            for attr, value in author_data.items():
                setattr(author_instance, attr, value)
            author_instance.save()

        return instance
    

class BorrowSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    borrowedBy = UserDataSerializer(read_only=True)

    class Meta:
        model = Borrow
        fields = ['dateBorrow', 'borrowedBy', 'book', 'dateReturn']

