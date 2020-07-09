from rest_framework import routers
from trip_project.trip_app.api import viewsets

router = routers.DefaultRouter()
router.register(r"register", viewsets.RegistrationViewset)
router.register(r"user", viewsets.AuthenticationViewset)
router.register(r'file_upload',viewsets.FileUploadViewSet)
router.register(r'trips-list', viewsets.TripListViewSet)
router.register(r'trips', viewsets.TripViewSet)
router.register(r'images',viewsets.TripImagesViewSet)
