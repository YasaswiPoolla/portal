from rest_framework import serializers
from trip_project.trip_app.models import User, Trips,TripImages
from django.db.models import Sum,Count


class UserSerializer(serializers.ModelSerializer):
    total_distance = serializers.SerializerMethodField()
    total_trips = serializers.SerializerMethodField()
    class Meta:
        model = User
        # fields = "__all__"
        fields = ('first_name','last_name','email','mobile','profile_image','total_distance','total_trips')
    
    def get_total_distance(self, obj):
        total_distance = Trips.objects.filter(user = obj.user_sqn).aggregate(Sum = Sum('trip_distance'))
        return total_distance
    
    def get_total_trips(self,obj):
        return Trips.objects.filter(user = obj.user_sqn).aggregate(Count = Count('trip_date'))

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ('first_name','last_name','email','mobile')

class TripSerializer(serializers.ModelSerializer):
    trip_distance = serializers.SerializerMethodField()
    class Meta:
        model = Trips
        fields = ('from_location', 'to_location', 'trip_date', 'trip_distance')

    def get_trip_distance(self, obj):
        if obj.trip_distance == None:    
            return str(0)+" " +" Km"
        else:
            return str(obj.trip_distance)+" " +" Km"        


class TripImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripImages
        fields = "__all__" 
