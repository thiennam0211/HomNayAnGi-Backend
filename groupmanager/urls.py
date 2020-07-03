from django.urls import path
from .views import ListCreateGroupsView, GroupsDetailView, ListGroupsView


urlpatterns = [
    path('', ListGroupsView.as_view(), name='groups-list'),
    path('create', ListCreateGroupsView.as_view(), name='groups-create'),
    path('<int:pk>', GroupsDetailView.as_view(), name="groups-detail"),

]
