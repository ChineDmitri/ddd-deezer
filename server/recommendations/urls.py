from django.urls import path
from . import views

urlpatterns = [
    path('popular-genres-region/', views.get_popular_genres_by_region, name='popular_genres_by_region'),
    path('popular-genres-region-age/', views.get_popular_genres_by_region_and_age, name='popular_genres_by_region_and_age')
]
