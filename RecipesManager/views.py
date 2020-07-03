import unidecode as unidecode
from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from rest_framework.views import status, APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser

from django.http import JsonResponse, QueryDict

from .models import Recipes, Ingredients, Recipe_Ingredients
from .serializers import RecipesSerializer, IngredientsSerializer, Recipe_IngredientsSerializer

import re
import json
import datetime
import unicodedata
from FilesManager.views import FileAWS

now = datetime.datetime.now()


# def upload_image(files, bucket):
#     aws = FileAWS()
#
#
def delete_image(files, bucket):
    aws = FileAWS()

    if type(files) == list:
        for file in files:
            aws.remove_file(file, bucket)
    else:
        aws.remove_file(files, bucket)


"""
Ingredients APIs
"""


class ListIngredientsView(generics.ListAPIView):
    """
    GET Ingredients/
    GET Ingredients/?search=something
    """
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class ListCreateIngredientsView(generics.ListCreateAPIView):
    """
    POST Ingredients/create
    """

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        print(request)

        serializer = IngredientsSerializer(data=request.data)

        if serializer.is_valid():

            a_ingredients = Ingredients.objects.create(
                name=request.data["name"],
                possible_unit=request.data["possible_units"]
            )

            return Response(
                data=IngredientsSerializer(a_ingredients).data,
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class IngredientsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET Ingredients/:id/
    PUT Ingredients/:id/
    DELETE Ingredients/:id/
    """
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer

    def get(self, request, *args, **kwargs):
        try:
            an_ingredient = self.queryset.get(pk=kwargs["pk"])
            return Response(IngredientsSerializer(an_ingredient).data)
        except Ingredients.DoesNotExist:
            return Response(
                data={
                    "message": "Ingredient with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            print(request.data)
            an_ingredient = self.queryset.get(pk=kwargs["pk"])
            serializer = IngredientsSerializer()
            update_ingredients = serializer.update(an_ingredient, request.data)
            return Response(IngredientsSerializer(update_ingredients).data)
        except Ingredients.DoesNotExist:
            return Response(
                data={
                    "message": "Ingredients with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            an_ingredient = self.queryset.get(pk=kwargs["pk"])

            recipes_has_ingredient = Recipe_Ingredients.objects.get(pk=an_ingredient.pk)

            if recipes_has_ingredient.DoesNotExist:
                an_ingredient.delete()
                delete_message = "Delete success"
                stt_code = status.HTTP_200_OK
            else:
                delete_message = "Can not delete, because this ingredient has appeared in some recipes"
                stt_code = status.HTTP_400_BAD_REQUEST
            return Response(
                data={
                    "message": delete_message
                },
                status=stt_code
            )

        except Ingredients.DoesNotExist:
            return Response(
                data={
                    "message": "Ingredients with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


"""
Recipes APIs
"""


class ListRecipesView(generics.ListAPIView):
    """
    GET recipes/
    GET recipes/?search=something
    """
    search_fields = ['title']
    filter_fields = ['dish_types', 'servings']
    filter_backends = (filters.SearchFilter,)
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer


class ListCreateRecipesView(generics.ListCreateAPIView):
    """
    POST recipes/create
    """

    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = RecipesSerializer(data=request.data)

        print(request.data)

        if serializer.is_valid():
            a_recipe = Recipes.objects.create(
                title=request.data['title'],
                dish_types=request.data['dish_types'],
                servings=request.data['servings'],
                readyInMinutes=request.data['readyInMinutes'],
                summary=request.data['summary'],
                images=None,
                inductions=request.data['inductions']
            )

            return Response(
                data=RecipesSerializer(a_recipe).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class RecipesDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET recipes/:id/
    PUT recipes/:id/
    DELETE recipes/:id/
    """

    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_recipe = self.queryset.get(pk=kwargs["pk"])

            if a_recipe.images is not None:

                aws = FileAWS()

                image_recipe_list = []

                for image in a_recipe.images:
                    image_url = aws.get_file_url(image, 'recipes-img')

                    if image_url.status_code == status.HTTP_200_OK:
                        res = json.loads(image_url.content)
                        image_recipe_list.append(res["fileUrl"])

                if not image_recipe_list:
                    return Response(
                        data={
                            "message": "Load image failed, please try again"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    a_recipe.images = image_recipe_list
                    return Response(
                        RecipesSerializer(a_recipe).data
                    )

        except Recipes.DoesNotExist:
            return Response(
                data={
                    "message": "User with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            print("Edit recipes")
            myQuery = request.data.copy()

            print(type(myQuery))
            print(type(request.data))

            print(myQuery)
            myDict = dict(myQuery)
            if isinstance(request.data, QueryDict):
                print("Querydict nè")

                myDict["title"] = myDict["title"][0]
                myDict["summary"] = myDict["summary"][0]
                myDict["dish_types"] = myDict["dish_types"][0]
                myDict["servings"] = int(myDict["servings"][0])
                myDict["readyInMinutes"] = int(myDict["readyInMinutes"][0])

                inductions_str = myDict["inductions"][0]

                my_json = json.loads(inductions_str)

                myDict["inductions"] = my_json
            else:
                print("dict nè")

            a_recipe = self.queryset.get(pk=kwargs["pk"])

            serializer = RecipesSerializer()
            update = serializer.update(a_recipe, myDict)
            return Response(RecipesSerializer(a_recipe).data)

        except Recipes.DoesNotExist:
            return Response(
                data={
                    "message": "User with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_recipe = self.queryset.get(pk=kwargs["pk"])

        except Recipes.DoesNotExist:
            return Response(
                data={
                    "message": "User with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class UploadRecipeIngredientsInfo(generics.CreateAPIView):
    queryset = Recipe_Ingredients.objects.all()
    serializer_class = Recipe_IngredientsSerializer

    def post(self, request, *args, **kwargs):

        recipe_id = kwargs["pk"]

        ingredients_list = request.data["recipe_ingredients"]

        index = 0

        for food in ingredients_list:

            food["recipe"] = recipe_id
            print(food)
            serializer = Recipe_IngredientsSerializer(data=food)

            if serializer.is_valid():
                a_recipe_ingredient = Recipe_Ingredients.objects.create(
                    recipe=Recipes.objects.get(pk=recipe_id),
                    ingredient=Ingredients.objects.get(pk=food["ingredient"]),
                    amount=food["amount"],
                    unit=food["unit"],
                )
                ++index
            else:
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(data="Save ok")


class EditRecipeIngredientsInfo(generics.UpdateAPIView):
    queryset = Recipe_Ingredients.objects.all()
    serializer_class = Recipe_IngredientsSerializer

    def put(self, request, *args, **kwargs):
        recipe_id = kwargs["pk"]

        ingredients_list = request.data["recipe_ingredients"]

        # for food in ingredients_list:
        #
        #     food["recipe"] = recipe_id
        #     print(food)
        #     serializer = Recipe_IngredientsSerializer(data=food)
        #
        #     if serializer.is_valid():
        #         a_recipe_ingredient = Recipe_Ingredients.objects.create(
        #             recipe=Recipes.objects.get(pk=recipe_id),
        #             ingredient=Ingredients.objects.get(pk=food["ingredient"]),
        #             amount=food["amount"],
        #             unit=food["unit"],
        #         )
        #         ++index
        #     else:
        #         return Response(
        #             data=serializer.errors,
        #             status=status.HTTP_400_BAD_REQUEST
        #         )

        return Response(data="Save ok")


class UploadRecipesImages(generics.UpdateAPIView):
    queryset = Recipes.objects.all()
    parser_classes = (MultiPartParser,)
    serializer_class = RecipesSerializer

    def put(self, request, *args, **kwargs):
        serializer = RecipesSerializer()

        a_recipe = self.queryset.get(pk=kwargs["pk"])

        aws = FileAWS()

        file_list = request.FILES.getlist('images')

        image_key_file = unidecode.unidecode(a_recipe.title)

        images_list = list()

        for image in file_list:
            image.name = now.strftime("%d%m%y%H%M%S") + "_" + re.sub("[ ]+", '', image_key_file) + "_" + image.name
            img_up = aws.upload_file(image, 'recipes-img')
            if img_up.status_code == status.HTTP_200_OK:
                images_list.append(str(image.name))

        if not images_list:
            return Response(
                data={
                    "message": "Upload image failed, please try again"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            upload_img = serializer.update(a_recipe, {'images': images_list})

            return Response(RecipesSerializer(upload_img).data)


class GetRecipeImage(APIView):

    def post(self, request, format=None):
        aws = FileAWS()

        image_name = request.data["image_name"]

        bucket = 'recipes-img'

        img_url = aws.get_file_url(image_name, bucket)

        if img_url.status_code == status.HTTP_200_OK:
            res = json.loads(img_url.content)
            return JsonResponse({
                'message': 'OK',
                'fileUrl': res['fileUrl'],
            })


class GetRecipeImages(generics.UpdateAPIView):
    queryset = Recipes.objects.all()
    parser_classes = (MultiPartParser,)
    serializer_class = RecipesSerializer

    def put(self, request, *args, **kwargs):
        aws = FileAWS()

        serializer = RecipesSerializer()

        a_recipe = self.queryset.get(pk=kwargs["pk"])

        bucket = 'recipes-img'

        list_urls = []

        for img in a_recipe.images:
            if img:
                img_url = aws.get_file_url(img, bucket)
                if img_url.status_code == status.HTTP_200_OK:
                    res = json.loads(img_url.content)
                    list_urls.append(res['fileUrl'])

        print(list_urls)

        return JsonResponse({
            'message': 'OK',
            'fileUrls': list_urls,
        })
