from rest_framework import serializers
from trip_project.trip_app.models import User, Trips


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trips
        fields = ('from_location', 'to_location', 'trip_date', 'trip_distance')