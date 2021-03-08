from rest_framework import serializers
from .models import User,Tel_opt


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("phone_number", "first_name", "last_name","password")

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class Tel_optSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tel_opt
        fields = '__all__'
