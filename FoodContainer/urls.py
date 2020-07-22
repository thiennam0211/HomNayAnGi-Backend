from django.urls import path
from .views import listFoodView, addFoodToUserContainer, updateFoodOfUser, deleteFoodOfUser, listFoodOfUser

urlpatterns = [
    path('', listFoodView.as_view(), name='list food'),
    path('<int:userID>/addFood', addFoodToUserContainer.as_view(), name="add food"),
    path('<int:pk>/editFood', updateFoodOfUser.as_view(), name='update'),
    path('<int:pk>/delete', deleteFoodOfUser.as_view(), name='delete'),
    path('<int:userID>', listFoodOfUser.as_view(), name='get foods of user')
]
