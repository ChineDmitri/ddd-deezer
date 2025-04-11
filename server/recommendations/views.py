from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from .services.MusicServiceListener import MusicServiceListeners
from .services.MusicServiceArtist import MusicServiceArtist

# Init du service (une fois pour toute l'application)
music_listeners_service = MusicServiceListeners()
music_artist_service = MusicServiceArtist()

# Endpoints pour les listeners
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_popular_genres_by_region(request):
    
    region = request.query_params.get('region', None)

    result = music_listeners_service.get_listeners_genre_by_region(region)

    if "error" in result:
        return Response({"error": result["error"]}, status=400)
    
    return Response(result, status=200)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_popular_genres_by_region_and_age(request):
    
    region = request.query_params.get('region', None)
    age = request.query_params.get('age', None)

    result = music_listeners_service.get_listeners_genre_by_region_and_age(region, age)

    if "error" in result:
        return Response({"error": result["error"]}, status=400)
    
    return Response(result, status=200)

# Endpoints pour les artistes
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_popular_genres_by_region_artist(request):
    
    region = request.query_params.get('region', None)

    result = music_artist_service.get_artists_genre_by_region(region)

    if "error" in result:
        return Response({"error": result["error"]}, status=400)
    
    return Response(result, status=200)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_popular_genres_by_region_and_age_artist(request):
    
    region = request.query_params.get('region', None)
    age = request.query_params.get('age', None)

    result = music_artist_service.get_artists_genre_by_region_and_age(region, age)

    if "error" in result:
        return Response({"error": result["error"]}, status=400)
    
    return Response(result, status=200)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_tracks_from_genre_and_region_artist(request):

    region = request.query_params.get('region', None)
    genre = request.query_params.get('genre', None)

    result = music_artist_service.get_tracks_from_genre_and_region(region, genre)

    if "error" in result:
        return Response({"error": result["error"]}, status=400)
    
    return Response(result, status=200)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_metrics_by_genre(request):

    genre = request.query_params.get('genre', None)

    result = music_artist_service.get_metrics_by_genre(genre)

    if "error" in result:
        return Response({"error": result["error"]}, status=400)
    
    return Response(result, status=200)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_metrics_by_region(request):

    region = request.query_params.get('region', None)

    result = music_artist_service.get_metrics_by_region(region)

    if "error" in result:
        return Response({"error": result["error"]}, status=400)
    
    return Response(result, status=200)


