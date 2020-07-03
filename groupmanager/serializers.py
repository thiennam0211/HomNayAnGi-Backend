from rest_framework import serializers
from groupmanager.models import Group


class GroupSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'password')
