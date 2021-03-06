from django.urls import path
from .views import ListIngredientsView, ListCreateIngredientsView, IngredientsDetailView, \
    ListRecipesView, ListCreateRecipesView, RecipesDetailView, UploadRecipesImages, UploadRecipeIngredientsInfo, \
    GetRecipeImage, GetRecipeImages, RecipesIngredientsView, EditRecipeIngredientsInfo

urlpatterns = [
    path('ingredients/', ListIngredientsView.as_view(), name='ingredients-all-list'),
    path('ingredients/create', ListCreateIngredientsView.as_view(), name='ingredients-create'),
    path('ingredients/<int:pk>', IngredientsDetailView.as_view(), name='ingredients-detail'),

    path('', ListRecipesView.as_view(), name='recipes-all-list'),
    path('create', ListCreateRecipesView.as_view(), name='recipe-create'),
    path('<int:pk>', RecipesDetailView.as_view(), name='recipe-detail'),
    path('<int:pk>/upload-image', UploadRecipesImages.as_view(), name='upload-recipe-image'),
    path('get-image', GetRecipeImage.as_view(), name='get-image-recipes'),
    path('<int:pk>/get-images', GetRecipeImages.as_view(), name='get-all-image-url-of-recipes'),


    path('recipes-ingredients', RecipesIngredientsView.as_view(), name='recipes-ingredients-get-all'),
    path('recipes-ingredients/<int:pk>/edit', EditRecipeIngredientsInfo.as_view(), name='edit-recipe-ingredients'),
    path('<int:pk>/upload-ingredients', UploadRecipeIngredientsInfo.as_view(), name='upload-recipe-ingredients'),

]
