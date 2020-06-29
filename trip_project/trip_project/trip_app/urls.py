from django.conf.urls import include, url
from rest_framework_jwt.views import refresh_jwt_token
# from worldline.wlportal.api.router import router
from trip_project.trip_app.api.router import router

urlpatterns = [url(r"^api/", include(router.urls)), url(r"^auth/refresh_token/", refresh_jwt_token)]
