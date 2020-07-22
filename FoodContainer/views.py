from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from rest_framework.views import status, APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser

from django.http import JsonResponse, QueryDict

from .models import Food
from usermanager.models import Users
from RecipesManager.models import Ingredients

from .serializers import ContainerSerializer

import json


class listFoodView(generics.ListAPIView):
    """
    GET container/
    """
    filterset_fields = ['user']
    search_fields = ['food']
    filter_backends = (filters.SearchFilter,)
    queryset = Food.objects.all()
    serializer_class = ContainerSerializer


class listFoodOfUser(generics.RetrieveUpdateDestroyAPIView):
    """
    GET container/userID
    """

    queryset = Food.objects.all()
    serializer_class = ContainerSerializer

    def get(self, request, *args, **kwargs):
        userID = kwargs["userID"]

        user = Users.objects.get(pk=userID)

        try:

            return Response(
                data=self.queryset.filter(user=userID),
                status=status.HTTP_200_OK
            )
        except user.DoesNotExist:
            return Response(
                data={
                    "message": "User with id: {} does not exist".format(userID)
                },
                status=status.HTTP_404_NOT_FOUND
            )


class addFoodToUserContainer(generics.ListCreateAPIView):
    """
    POST container/userID/addFood
    """
    queryset = Food.objects.all()
    serializer_class = ContainerSerializer

    def post(self, request, *args, **kwargs):

        userID = kwargs["userID"]

        user = Users.objects.get(pk=userID)

        print(user.email)

        try:
            serializerData = ContainerSerializer(data=request.data)

            if serializerData.is_valid():

                try:
                    a_food = self.queryset.get(user=userID, food=request.data["food"])

                    serializer = ContainerSerializer()

                    data = request.data

                    data["user"] = a_food.user

                    data["food"] = a_food.food

                    data["amount"] += a_food.amount

                    update_food = serializer.update(a_food, data)

                    return Response(
                        data=ContainerSerializer(update_food).data,
                        status=status.HTTP_200_OK
                    )

                except Food.DoesNotExist:

                    food = Ingredients.objects.get(pk=request.data["food"])

                    a_food = Food.objects.create(
                        user=user,
                        food=food,
                        amount=request.data["amount"],
                        unit=request.data["unit"],
                        note=request.data["note"]
                    )

                    return Response(
                        data=ContainerSerializer(a_food).data,
                        status=status.HTTP_201_CREATED
                    )

            else:
                print(serializerData.errors)
                return Response(
                    data={
                        "message": "Invalid Data"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        except user.DoesNotExist:
            return Response(
                data={
                    "message": "User with id: {} does not exist".format(userID)
                },
                status=status.HTTP_404_NOT_FOUND
            )


class updateFoodOfUser(generics.UpdateAPIView):
    """
    PUT container/foodID
    """
    queryset = Food.objects.all()
    serializer_class = ContainerSerializer

    def put(self, request, *args, **kwargs):
        try:
            a_food = self.queryset.get(pk=kwargs["pk"])

            serializer = ContainerSerializer()

            update_food = serializer.update(a_food, request.data)

            return Response(
                data=ContainerSerializer(update_food).data,
                status=status.HTTP_200_OK
            )

        except Food.DoesNotExist:
            return Response(
                data={
                    "message": "Food with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class deleteFoodOfUser(generics.DestroyAPIView):
    """
    DELETE container/id
    """
    queryset = Food.objects.all()
    serializer_class = ContainerSerializer

    def delete(self, request, *args, **kwargs):
        foodId = kwargs["pk"]

        food = self.queryset.get(pk=foodId)

        food.delete()

        return Response(
            data={
                "message": "delete success"
            },
            status=status.HTTP_200_OK
        )
