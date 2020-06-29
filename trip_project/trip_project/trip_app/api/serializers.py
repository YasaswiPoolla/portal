from rest_framework import serializers
from trip_project.trip_app.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)
