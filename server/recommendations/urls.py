from django.urls import path
from . import views

urlpatterns = [
    path('listeners/popular-genres-region/', views.get_popular_genres_by_region, name='popular_genres_by_region'),
    path('listeners/popular-genres-region-age/', views.get_popular_genres_by_region_and_age, name='popular_genres_by_region_and_age'),
    path('artists/tracks-genre-region/', views.get_tracks_from_genre_and_region_artist, name='tracks_from_genre_and_region_artist')
]
