from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from .services.MusiqueService import MusiqueService

# Init du service (une fois pour toute l'application)
musique_service = MusiqueService()

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_popular_genres_by_region(request):
    
    region = request.query_params.get('region', None)

    result = musique_service.get_popular_genres_by_region(region)

    if "error" in result:
        return Response({"error": result["error"]}, status=400)
    
    return Response(result, status=200)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_popular_genres_by_region_and_age(request):
    
    region = request.query_params.get('region', None)
    age = request.query_params.get('age', None)

    result = musique_service.get_popular_genres_by_region_and_age(region, age)

    if "error" in result:
        return Response({"error": result["error"]}, status=400)
    
    return Response(result, status=200)
