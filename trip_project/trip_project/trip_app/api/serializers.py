from rest_framework import serializers
from trip_project.trip_app.models import User, Trips,TripImages


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ('first_name','last_name','email','mobile','profile_image')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ('first_name','last_name','email','mobile')

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trips
        fields = ('from_location', 'to_location', 'trip_date', 'trip_distance')


class TripImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripImages
        fields = "__all__" 
