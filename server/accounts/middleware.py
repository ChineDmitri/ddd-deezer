from django.http import HttpResponseForbidden

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si la demande est pour l'interface d'administration
        if request.path.startswith('/admin/'):
            # Autoriser l'accès à la page de connexion admin pour tout le monde
            if request.path == '/admin/login/' or request.path == '/admin/' and not request.user.is_authenticated:
                return self.get_response(request)
            
            # Si l'utilisateur n'est pas connecté, Django le redirigera vers la page de login
            if not request.user.is_authenticated:
                return self.get_response(request)
            
            # Vérifier si l'utilisateur est un superutilisateur
            if request.user.is_superuser:
                return self.get_response(request)
            
            # Vérifier si l'utilisateur a un profil avec le rôle "admin"
            try:
                if request.user.userprofile.role == 'admin':
                    return self.get_response(request)
            except:
                pass
            
            # Si l'utilisateur est connecté mais n'a pas le rôle "admin" ou n'est pas superuser
            return HttpResponseForbidden("Vous n'avez pas les droits d'accès à l'administration")
        
        # Pour toutes les autres URLs, laisser passer la requête
        return self.get_response(request)