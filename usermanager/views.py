# from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status, APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser

from .models import Users
from .decorated import validate_request_data
from .serializers import UsersSerializers

import json
import datetime
from FilesManager.views import FileAWS


class ListUsersView(generics.ListAPIView):
    """
    GET users/
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializers


class ListCreateUsersView(generics.ListCreateAPIView):
    """
    POST users/create
    """

    queryset = Users.objects.all()
    parser_classes = (MultiPartParser,)
    serializer_class = UsersSerializers
    permission_classes = [permissions.AllowAny]

    @validate_request_data
    def post(self, request, *args, **kwargs):

        serializer = UsersSerializers(data=request.data)

        if serializer.is_valid():

            aws = FileAWS()

            images = request.data["images"]

            user_key_file = str(request.data["email"]).split('@')

            images.name = user_key_file[0] + "_" + images.name

            avatar_up = aws.upload_file(images, 'avatar')

            if avatar_up.status_code == status.HTTP_200_OK:
                print("Up avatar okela")

                a_user = Users.objects.create(
                    email=request.data["email"],
                    password=request.data["password"],
                    full_name=request.data["full_name"],
                    display_name=request.data["display_name"],
                    gender=request.data["gender"],
                    birthday=request.data["birthday"],
                    avatar=images
                )
            else:
                a_user = Users.objects.create(
                    email=request.data["email"],
                    password=request.data["password"],
                    full_name=request.data["full_name"],
                    display_name=request.data["display_name"],
                    gender=request.data["gender"],
                    birthday=request.data["birthday"]
                )

            return Response(
                data=UsersSerializers(a_user).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class UsersDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET users/:id/
    PUT users/:id/
    DELETE users/:id/
    """

    queryset = Users.objects.all()
    serializer_class = UsersSerializers

    def get(self, request, *args, **kwargs):
        try:
            a_user = self.queryset.get(pk=kwargs["pk"])

            if a_user.avatar is not None:

                aws = FileAWS()

                avatar_url = aws.get_file_url(a_user.avatar, 'avatar')

                if avatar_url.status_code == status.HTTP_200_OK:
                    res = json.loads(avatar_url.content)
                    a_user.avatar = res['fileUrl']

            return Response(UsersSerializers(a_user).data)

        except Users.DoesNotExist:
            return Response(
                data={
                    "message": "User with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            a_user = self.queryset.get(pk=kwargs["pk"])
            serializer = UsersSerializers()
            update_user = serializer.update(a_user, request.data)
            return Response(UsersSerializers(update_user).data)
        except Users.DoesNotExist:
            return Response(
                data={
                    "message": "User with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_user = self.queryset.get(pk=kwargs["pk"])
            a_user.delete()
            return Response(
                data={
                    "message": "Delete success"
                },
                status=status.HTTP_200_OK
            )
        except Users.DoesNotExist:
            return Response(
                data={
                    "message": "User with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class UserUpdateAvatar(generics.UpdateAPIView):
    """
    PUT users/id/update-avatar
    """
    queryset = Users.objects.all()
    parser_classes = (MultiPartParser,)
    serializer_class = UsersSerializers

    def put(self, request, *args, **kwargs):

        new_avatar = request.data["images"]

        now = datetime.datetime.now()

        aws = FileAWS()

        serializer = UsersSerializers()

        a_user = self.queryset.get(pk=kwargs["pk"])

        user_key_file = str(a_user.email).split('@')

        new_avatar.name = now.strftime("%H%M%S") + "_" + user_key_file[0] + "_" + new_avatar.name

        avatar_update = aws.upload_file(new_avatar, 'avatar')

        if avatar_update.status_code == status.HTTP_200_OK:
            if a_user.avatar is not None:
                delete_old_avatar = aws.remove_file(a_user.avatar, 'avatar')
            update_user = serializer.update(a_user, {'avatar': new_avatar.name})

        res = json.loads(avatar_update.content)

        return Response(
            data={
                "message": "Upload avatar success",
                "avatar_url": res['fileUrl']
            },
            status=status.HTTP_200_OK
        )


class UserLoginView(generics.ListCreateAPIView):
    """
    POST users/login/
    """

    queryset = Users.objects.all()
    serializer_class = UsersSerializers

    def post(self, request, *args, **kwargs):
        try:
            user_request = request.data
            print(request.data)
            email = user_request["email"]
            password = user_request["password"]
            if email or password:
                a_user = self.queryset.get(email=email)
                if password == a_user.password:

                    if a_user.avatar is not None:

                        aws = FileAWS()

                        avatar_url = aws.get_file_url(a_user.avatar, 'avatar')

                        if avatar_url.status_code == status.HTTP_200_OK:
                            res = json.loads(avatar_url.content)
                            a_user.avatar = res['fileUrl']

                    return Response(
                        data=UsersSerializers(a_user).data,
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        data={
                            "message": "Email or password incorrect"
                        },
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            else:
                return Response(
                    data={
                        "message": "Unset Value"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Users.DoesNotExist:
            return Response(
                data={
                    "message": "User with email: {} does not exist".format(email)
                },
                status=status.HTTP_404_NOT_FOUND
            )


class GetAvatarImage(APIView):

    def post(self, request, format=None):

        aws = FileAWS()

        image_name = request.data["image_name"]

        bucket = 'avatar'

        img_url = aws.get_file_url(image_name, bucket)

        if img_url.status_code == status.HTTP_200_OK:
            print(json.loads(img_url.content))
            res = json.loads(img_url.content)
            return JsonResponse({
                'message': 'OK',
                'fileUrl': res['fileUrl'],
            })


class UserForgotPasswordView(generics.UpdateAPIView):
    """
    GET users/:id/forgot-password
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializers

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = UsersSerializers()

            email = data["email"]
            old_password = data["password"]
            new_password = data["new_password"]

            a_user = self.queryset.get(email=email)
            if a_user.password == old_password:

                a_user.password = new_password

                update_user = serializer.update(a_user, UsersSerializers(a_user).data)

                return Response(UsersSerializers(update_user).data)
            else:
                message = "Password incorrect"
                return Response(
                    data={
                        "message": message
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        except Users.DoesNotExist:

            message = "User with email: {} does not exist".format(email)

            return Response(
                data={
                    "message": message
                },
                status=status.HTTP_404_NOT_FOUND
            )
