from rest_framework import status,viewsets
from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from trip_project.trip_app.models import User
from trip_project.trip_app.api.serializers import UserSerializer
from validate_email import validate_email

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
            print("!!!",authenticated_user)
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
