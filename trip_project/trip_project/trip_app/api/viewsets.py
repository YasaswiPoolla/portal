import datetime
from isoweek import Week
from django.db.models import Count
from rest_framework import status,viewsets
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from trip_project.trip_app.models import User,Trips, TripImages
from trip_project.trip_app.api.serializers import UserSerializer, TripImagesSerializer, TripSerializer
from validate_email import validate_email


from rest_framework.parsers import FormParser, MultiPartParser
from trip_project.trip_app.api.BaseViewset import BaseFilterablePaginatedViewset

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class RegistrationViewset(viewsets.ViewSet):
    User = get_user_model()
    queryset = get_user_model().objects.all()
    model = User
    permission_classes = []

    @csrf_exempt
    @action(methods=["post"], detail=False)
    def user(self, request):
        first_name = request.data["firstName"]
        last_name = request.data["lastName"]
        email = request.data["email"]
        mobile = request.data["mobile"]
        password = request.data["password"]
        confirm_password = request.data["confirmPassword"]
        if not validate_email(email):
            raise ValidationError("Email is not valid")
        if password is None or str(password).strip() == "":
            raise ValidationError("Password can't be empty")
        if mobile is None or str(mobile).strip() == "":
            raise ValidationError("Mobile number can't be empty")
        if confirm_password is None or str(confirm_password).strip() == "":
            raise ValidationError("Confirm Password can't be empty")
        if password != confirm_password:
            raise ValidationError("Passwords didn't match")
        try:
            User.objects.get(email=email)
            raise ValidationError("Email Already Registered")
        except User.DoesNotExist:
            pass
            user = User.objects.create_user(email, first_name, last_name, mobile, password)
            user.save()
        return Response({"message": "success"})

class AuthenticationViewset(viewsets.ViewSet):
    queryset = get_user_model().objects.all()
    model = User
    serializer_class = UserSerializer
    permission_classes = []

    @action(methods=["post"], detail=False)
    def login(self, request):
        username = request.data["email"]
        password = request.data["password"]

        if username is None or str(username).strip() == "":
            raise ValidationError("User ID is required")

        if password is None or str(password).strip() == "":
            raise ValidationError("Password is required")

        try:
            user = User.objects.get(email=username)

        except User.DoesNotExist:
            raise ValidationError("User Does Not Exist")

        if user and not user.is_active:
            raise ValidationError(
                "Account is deactivated due to inactivity or incorrect logins. Please contact admin to reactivate it"
            )

        try:

            authenticated_user = authenticate(email=username, password=password)
            user = User.objects.get(email=username)

            if authenticated_user:
                payload = jwt_payload_handler(user)

                return Response({"token": jwt_encode_handler(payload)})
            else:
                raise ValidationError("Credentials do not match")
        except Exception:
            raise ValidationError("Credentials do not match")
    
    @action(methods=["get"], detail=False)
    def current_user(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        data = UserSerializer(user).data
        return Response(data)
    
    @action(methods=["post"], detail=False)
    def logout(self, request):
        if request.user.is_authenticated:
            user = request.user
            
            return Response({"message": "success logged"})
        return Response({"message": "success"})


class FileUploadViewSet(viewsets.ViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser,)

    @action(methods=["post"], detail=False)
    def perform_create(self, serializer):
        user = self.request.user
        user.profile_image = self.request.data.get('datafile')
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)



class TripListViewSet(BaseFilterablePaginatedViewset):
    queryset = Trips.objects.all()
    serializer_class = TripSerializer
    model = Trips
    columns_to_display = [
    ]
    filter_only_columns = []
    date_column = "trip_date"
    db_date_column = "tripdate"
    date_type = "datetime"
    columns_with_text_filter = BaseFilterablePaginatedViewset.columns_with_text_filter + [
        "from_location",
        "to_location",
    ]
    date_input_format = "dd-MM-yyyy HH:mm:ss"
    default_start_date = (
        (datetime.datetime.now() - datetime.timedelta(days=3650))
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .date()
    )


class TripViewSet(BaseFilterablePaginatedViewset):
    queryset = Trips.objects.all()
    serializer_class = TripSerializer
    model = Trips

    @action(methods=["get"], detail=False, url_path="week_trips_count")
    def week_trips_count(self, request):
        trips = self.get_queryset()
        end_date = datetime.datetime.now()
        week_no = end_date.isocalendar()[1]
        start_week_no = week_no - 4
        current_year = datetime.datetime.now().year
        date = Week(current_year, start_week_no).monday()
        start_date = datetime.datetime.combine(date, datetime.datetime.min.time())
        response_data = {}
        trip_queryset = (
            trips.filter(trip_date__range=(start_date, end_date))
            .values("trip_date")
            .annotate(count=Count("trip_date"))
        )
        for trip in trip_queryset:
            week = trip["trip_date"].isocalendar()[1]
            val = trip["count"]
            week_start_date = datetime.datetime.strptime(
                "{} {} 1".format(current_year, week-1), "%Y %W %w"
            )
            week_end_date = week_start_date + datetime.timedelta(days=6)
            week_start_date_formatted = week_start_date.strftime("%b %d")
            week_end_date_formatted = week_end_date.strftime("%b %d")
            week_formatted = week_start_date_formatted + " - " + week_end_date_formatted
            response_data[week_formatted] = response_data.get(week_formatted, 0) + val

        return Response(response_data)

class TripImagesViewSet(viewsets.ViewSet):
    queryset = TripImages.objects.all()
    serializer_class = TripImagesSerializer
    parser_classes = (MultiPartParser, FormParser,)

    @action(methods=["post"], detail=False)
    def perform_create(self, serializer):
        if self.request.method == "POST":
            from_location = self.request.data['from_location']
            to_location = self.request.data['to_location']
            trip_date = self.request.data['trip_date']
            trip = Trips.objects.get(from_location = from_location,to_location=to_location,trip_date__startswith=trip_date)
            for image in self.request.data.getlist('files'):
                record = TripImages.objects.create(images=image,trip = trip)
                record.save()
            return Response({'message':'success'})


    @action(methods=["post"], detail=False)
    def get_images(self, serializer):
        if self.request.method == "POST":
            from_location = self.request.data['from_location']
            to_location = self.request.data['to_location']
            trip_date = self.request.data['trip_date']
            trip = Trips.objects.get(from_location = from_location,to_location=to_location,trip_date__startswith=trip_date)
            images = TripImages.objects.filter(trip = trip)
            serializer = TripImagesSerializer(images, many = True)
            return Response(serializer.data)
