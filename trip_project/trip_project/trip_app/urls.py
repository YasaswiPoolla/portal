from django.conf.urls import include, url
from rest_framework_jwt.views import refresh_jwt_token
from trip_project.trip_app.api.router import router
from trip_project.trip_app import views

urlpatterns = [url(r"^api/", include(router.urls)), url(r"^auth/refresh_token/", refresh_jwt_token),
url(r"^user-details/", views.UserUpdate.as_view(), name="user_details"),]
