from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['slug','email', 'username','first_name', 'last_name','password','role','is_active']
        read_only_fields = [
            'role',
            'slug',
            'is_active'
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'




class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(
        write_only=True,
        required=True
    )

    new_password = serializers.CharField(
        write_only=True,
        required=True
    )

    new_password_confirm = serializers.CharField(
        write_only=True,
        required=True
    )

    def validate_old_password(self, value):

        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError(
                "L'ancien mot de passe est incorrect."
            )

        return value

    def validate(self, attrs):

        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm':
                "Les mots de passe ne correspondent pas."
            })

        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({
                'new_password':
                "Le nouveau mot de passe doit être différent "
                "de l'ancien."
            })

        return attrs

    def validate_new_password(self, value):

        from django.contrib.auth.password_validation import (
            validate_password
        )

        validate_password(
            value,
            self.context['request'].user
        )

        return value

    def save(self, **kwargs):

        user = self.context['request'].user

        user.set_password(
            self.validated_data['new_password']
        )

        user.save(
            update_fields=['password']
        )

        return user