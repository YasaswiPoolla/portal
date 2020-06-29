from rest_framework import routers
from trip_project.trip_app.api import viewsets

router = routers.DefaultRouter()
router.register(r"register", viewsets.RegistrationViewset)
router.register(r"user", viewsets.AuthenticationViewset)
