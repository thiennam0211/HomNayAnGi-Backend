# from django.shortcuts import render
# from django.http import HttpResponse

# # Create your views here.
# def index(request):
#     return HttpResponse('Group managerment')


from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status

from .decorators import validate_request_data
from .models import Group
from .serializers import GroupSerializer


class ListGroupsView(generics.ListAPIView):
    """
    GET group/
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ListCreateGroupsView(generics.ListCreateAPIView):
    """
    GET group/
    POST group/
    """

    queryset = Group.objects.all()

    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]

    @validate_request_data
    def post(self, request, *args, **kwargs):
        a_group = Group.objects.create(
            name=request.data["name"],
            password=request.data["password"]
        )
        return Response(
            data=GroupSerializer(a_group).data,
            status=status.HTTP_201_CREATED
        )


class GroupsDetailView(generics.RetrieveUpdateDestroyAPIView):

    """
    GET Group/:id/
    PUT Group/:id/
    DELETE Group/:id/
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_group = self.queryset.get(pk=kwargs["pk"])
            return Response(GroupSerializer(a_group).data)
        except Group.DoesNotExist:
            return Response(
                data={
                    "message": "Group with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            a_group = self.queryset.get(pk=kwargs["pk"])
            serializer = GroupSerializer()
            update_group = serializer.update(a_group, request.data)
            return Response(GroupSerializer(update_group).data)
        except Group.DoesNotExist:
            return Response(
                data={
                    "message": "Group with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_group = self.queryset.get(pk=kwargs["pk"])
            a_group.delete()
            return Response(
                data={
                    "message": "Delete success"
                },
                status=status.HTTP_200_OK
            )
        except Group.DoesNotExist:
            return Response(
                data={
                    "message": "Group with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
