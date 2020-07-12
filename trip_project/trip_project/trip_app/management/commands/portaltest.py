from django.core.management.base import BaseCommand
from trip_project.trip_app.models import User, Trips, Locations
import math
from django.db.models import Count, Sum

class Command(BaseCommand):
    help = "Test scripts"

    def handle(self, *args, **options):
        trips = Trips.objects.filter(trip_distance__isnull = True)
        for trip in trips :
            loc = Locations.objects.filter(trip = trip).order_by('created_date')
            if len(loc) > 2:
                lat_log_list = []
                final_list = []
                for i in loc:
                    lat_log_list.append(i.latitude)
                    lat_log_list.append(i.longitude)
                    final_list.append(lat_log_list)
                    lat_log_list = []
                total_dist = 0
                for i in range(len(final_list)-1):
                    dist = self.distance(final_list[i],final_list[i+1])
                    total_dist +=self.distance(final_list[i],final_list[i+1]) 

                trip.trip_distance = round(total_dist,2)
                trip.save()

    def distance(self,source , destination): 
        lat1, lon1 = source [0],source [1]
        lat2, lon2 = destination[0],destination[1]
        radius = 6371 # km
        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
        return d
