from django.contrib.auth.models import User
from config.tools.datetime_tools import datetime_difference_from_now, now_tehran
from config.tools.jwt_tools import get_tokens_for_user
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample, OpenApiRequest, OpenApiTypes
from .serializers import UserSerializer, OtpSerializer, JwtSerializer


class CreateUser(APIView):

    @staticmethod
    @extend_schema(
        parameters=[
            OpenApiParameter(name='fullname', required=True, type=str, description="Alphabet String"),
            OpenApiParameter(name='phone', required=True, type=str, description="Length = 11"),
        ],

        request=OpenApiRequest(
            examples=[
                OpenApiExample(name='Request example',
                               description='Example of a correct format request',
                               value={"fullname": "fullname (Persian alphabet)",
                                      "phone": "09123456789",
                                      }),
            ], request=OpenApiTypes.JSON_PTR
        ),
        responses={201: OpenApiResponse(
            description="New user created successfully",
            examples=[
                OpenApiExample(
                    name='Successful Response',
                    description='Example of successful response',
                    value={"fullname": "Fullname", "phone": "09356818856"}),
            ], response=201
        )},
    )
    def post(request: Request):  # create new User
        """
        Takes a "phone number" and "full name"  to register a new user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)

            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# region OTP
class OtpUnit(APIView):

    @staticmethod
    @extend_schema(
        parameters=[
            OpenApiParameter(name='phone', required=True, type=str, description="Length = 11"),
        ],

        request=OpenApiRequest(
            examples=[
                OpenApiExample(name='Request example',
                               description='Example of a correct format request',
                               value={"phone": "09123456789"}),
            ], request=OpenApiTypes.JSON_PTR
        ),
        responses={200: OpenApiResponse(
            description="OTP is sent successfully",
            examples=[
                OpenApiExample(
                    name='Successful Response',
                    description='Example of successful response',
                    value={"detail": "OTP sent successfully"}),
            ], response=200
        )},
    )
    def post(request: Request):  # Requested to create otp
        """
        takes a "phone number". If the user exists, an "OTP" will be sent to the "phone number".
        """
        serializer = OtpSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.create(validated_data=serializer.validated_data)
                return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({f"detail": e}, status=status.HTTP_429_TOO_MANY_REQUESTS)


# endregion


# region jwt

class JwtUnit(APIView):

    @staticmethod
    @extend_schema(

        parameters=[
            OpenApiParameter(name='phone', required=True, type=str, description="Length = 11"),
            OpenApiParameter(name='OTP', required=True, type=str, description="Length = 6"),
        ],

        request=OpenApiRequest(
            examples=[
                OpenApiExample(name='Request example', description='Example of a correct format request',
                               value={"phone": "09123456789", "otp": "123456"}
                               ),
            ], request=OpenApiTypes.JSON_PTR
        ),
        responses={201: OpenApiResponse(
            description="Access and refresh tokens are generated",
            examples=[
                OpenApiExample(
                    name='Successful Response',
                    description='Example of successful response',
                    value={'access_token': 'your_access_token', 'refresh_token': 'your_refresh_token'}),
            ], response=201
        )},
    )
    def post(request: Request):
        """
        Takes "phone" and "OTP", Response: generates "access token" and "refresh token"
        """
        serializer = JwtSerializer(data=request.data)
        if serializer.is_valid():
            #  select user
            the_user = User.objects.filter(username__exact=serializer.validated_data['phone']).first()
            #  check the password (otp)
            if the_user.check_password(serializer.validated_data['otp']):
                #  check otp expire date
                if datetime_difference_from_now(the_user.useradditional.opt_expire_date) > 0:
                    # Verify Phone Number and set last login field
                    the_user.useradditional.otp_verify = True
                    the_user.last_login = now_tehran()
                    the_user.save()
                    the_user.useradditional.save()
                    #  create token and return it
                    received_api = get_tokens_for_user(the_user)
                    return Response(received_api, status=status.HTTP_201_CREATED)
                else:
                    return Response({f"detail": "otp expired"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({f"detail": "Incorrect OTP"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# endregion
