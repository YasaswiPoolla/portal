import logging
import traceback

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from jwt import ExpiredSignatureError
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from .models import UserException

# Get an instance of a logger
logger = logging.getLogger(__name__)


class JWTTokeUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get("HTTP_AUTHORIZATION", " ").split(" ")[1]
        data = {"token": token}
        request.user = AnonymousUser()
        try:
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data["user"]
            request.user = user
        except ExpiredSignatureError:
            logger.info("No Logged In User")
        except ValidationError:
            logger.info("Signature Is expired")
        except Exception:
            stack_trace = traceback.format_exc()
            logger.exception(stack_trace)
        response = self.get_response(request)
        return response


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        meta_data = request.META
        stack_trace = traceback.format_exc()
        user = None
        if request.user:
            user = request.user
        if not user or user.is_anonymous:
            UserException.objects.create(
                user_request={"Meta_data": str(meta_data)}, stack_trace=stack_trace
            )
        else:
            UserException.objects.create(
                user=user, user_request={"Meta_data": str(meta_data)}, stack_trace=stack_trace
            )
        logger.error(stack_trace)
        return HttpResponse(
            "Unknown error occured. Please contact admin.", content_type="text/plain", status=400
        )
