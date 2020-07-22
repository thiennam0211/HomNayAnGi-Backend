from rest_framework import serializers
from .models import Food


class ContainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = '__all__'
        depth = 1
