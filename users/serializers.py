from .models import CustomUser,Profile
from rest_framework import fields, serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import CustomUser


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'full_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Invalid credentials')
    
class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = ['mobile_number', 'avatar']

    def create(self, validated_data):
        user = self.context['request'].user
        return Profile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        if 'avatar' in validated_data:
            instance.avatar = validated_data.get('avatar')
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'profile']

    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email']
