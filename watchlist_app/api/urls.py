
from django.urls import path
# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import MovieDetailAV, MovieListAV

urlpatterns = [
    path('', MovieListAV.as_view(), name='movie-list'),
    path('<int:pk>/', MovieDetailAV.as_view(), name='movie-details')
]

# urlpatterns = [
#     path('list/', movie_list, name='movie-list'),
#     path('<int:pk>/', movie_details, name='movie-details')
# ]
