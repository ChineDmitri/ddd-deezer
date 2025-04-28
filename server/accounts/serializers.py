from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'favorite_genres', 'birth_date', 'role')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    favorite_genres = serializers.CharField(required=False, allow_blank=True, write_only=True)
    birth_date = serializers.DateField(required=False, allow_null=True, write_only=True)
    role = serializers.ChoiceField(
        choices=[('artist', 'Artist'), ('listener', 'Listener'), ('admin', 'admin')],
        write_only=True
    )
    class Meta: 
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'favorite_genres', 'birth_date', 'role')

    def create(self, validated_data): 
        # Extract profile data
        favorite_genres = validated_data.pop('favorite_genres', '')
        birth_date = validated_data.pop('birth_date', None)
        role = validated_data.pop('role', 'listener')
        # Creation de l'utilisateur 
        user = User.objects.create_user(**validated_data)

        # Creation du profil utilisateur
        UserProfile.objects.create(user=user, favorite_genres=favorite_genres, birth_date=birth_date, role=role)

        return user
    
    def to_representation(self, instance):
        """Override to include UserProfile data in the response"""
        # Get the default representation
        representation = super().to_representation(instance)
        
        # Add UserProfile fields to the representation
        try:
            user_profile = UserProfile.objects.get(user=instance)
            representation['favorite_genres'] = user_profile.favorite_genres
            representation['birth_date'] = user_profile.birth_date
            representation['role'] = user_profile.role
        except UserProfile.DoesNotExist:
            pass
            
        return representation