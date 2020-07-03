from rest_framework import serializers
from .models import Recipes, Ingredients, Recipe_Ingredients

import re
from django.http import QueryDict


def str_to_arr(value):
    if type(value) == str:
        delete_special = re.sub("\W+", " ", value)
        value = delete_special.split(" ")
    return value


class RecipesSerializer(serializers.ModelSerializer):

    def to_internal_value(self, value):
        return super().to_internal_value(value)

    class Meta:
        model = Recipes
        id = serializers.IntegerField()
        images = serializers.ListField(child=serializers.CharField(), allow_null=True, allow_empty=True,
                                       min_length=None, max_length=None)

        fields = '__all__'

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.dish_type = validated_data.get('dish_types', instance.dish_types)
        instance.servings = validated_data.get('servings', instance.servings)
        instance.readyInMinutes = validated_data.get('readyInMinutes', instance.readyInMinutes)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.images = validated_data.get('images', instance.images)
        instance.inductions = validated_data.get('inductions', instance.inductions)
        instance.save()

        return instance


class IngredientsSerializer(serializers.ModelSerializer):

    # def validate_possible_unit(self, value):
    #     return None

    def to_internal_value(self, value):
        #_mutable make data can change
        if type(value['possible_units']) == str:
            _mutable = value._mutable
            value._mutable = True
            value['possible_units'] = str_to_arr(value['possible_units'])
            value._mutable = _mutable
        return super().to_internal_value(value)

    class Meta:
        model = Ingredients
        id = serializers.IntegerField()
        name = serializers.CharField()
        possible_unit = serializers.ListField(child=serializers.CharField(), allow_empty=True,
                                              min_length=None, max_length=None)
        fields = '__all__'

    # def create(self, validated_data):
    #     return Ingredients(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.possible_unit = str_to_arr(validated_data.get('possible_unit', instance.possible_unit))
        instance.save()
        return instance


class Recipe_IngredientsSerializer(serializers.ModelSerializer):
    # def to_internal_value(self, data):
    #     return None

    class Meta:
        id = serializers.IntegerField()
        model = Recipe_Ingredients
        # fields = {'recipe', 'ingredient', 'amount', 'unit'}
        fields = '__all__'

    # def create(self, validated_data):
    #     return Recipe_Ingredients(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     return instance
