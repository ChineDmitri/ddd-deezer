from django.urls import path
from . import views

urlpatterns = [
    path('listeners/popular-genres-region/', views.get_popular_genres_by_region, name='popular_genres_by_region'),
    path('listeners/popular-genres-region-age/', views.get_popular_genres_by_region_and_age, name='popular_genres_by_region_and_age'),
    path('artists/popular-genres-region/', views.get_popular_genres_by_region_artist, name='popular_genres_by_region'),
    path('artists/popular-genres-region-age/', views.get_popular_genres_by_region_and_age_artist, name='popular_genres_by_region_and_age'),
    path('artists/tracks-genre-region/', views.get_tracks_from_genre_and_region_artist, name='tracks_from_genre_and_region_artist'),
    path('artists/metrics-genre/', views.get_metrics_by_genre, name='metrics_by_genre'),
    path('artists/metrics-region/', views.get_metrics_by_region, name='metrics_by_region'),
]
