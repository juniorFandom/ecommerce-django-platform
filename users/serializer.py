# serializer.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

User = get_user_model() 


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création et la gestion des utilisateurs
    """
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'role',
            'is_active',
            'slug',
            'date_joined',
            'last_login'
        ]
        read_only_fields = [
            'id',
            'slug',
            'date_joined',
            'last_login'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, attrs):
        # Vérifier que les mots de passe correspondent
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        
        if password != password_confirm:
            raise serializers.ValidationError({
                "password_confirm": "Les mots de passe ne correspondent pas."
            })
        
        # Vérifier que l'email est unique (déjà géré par le modèle)
        email = attrs.get('email')
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                "email": "Un utilisateur avec cet email existe déjà."
            })
        
        return attrs

    def create(self, validated_data):
        print('voici les donnees transmis dans le serializers')
        print(validated_data)
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')  
        
        username = validated_data.pop('username')
        email = validated_data.pop('email', '')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **validated_data  
        )
        
        return user
    
    def update(self, instance, validated_data):
        # Mise à jour sécurisée
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        
        # Mettre à jour les autres champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer détaillé pour la consultation
    """
    
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'role',
            'role_display',
            'password',
            'slug',
            'is_active',
            'is_staff',
            'is_superuser',
            'date_joined',
            'last_login'
        ]
        read_only_fields = [
            'id',
            'slug',
            'date_joined',
            'last_login'
        ]
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer pour le changement de mot de passe
    """
    old_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Ancien mot de passe incorrect.")
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                "new_password_confirm": "Les mots de passe ne correspondent pas."
            })
        return attrs
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user