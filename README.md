# Instructions de Configuration pour le Projet Django

## Prérequis

Avant de configurer le projet, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- Python 3.8 ou une version ultérieure
- pip (le gestionnaire de paquets Python)
- Virtualenv (optionnel mais recommandé)

## Configuration du Projet partie Backend

1. **Cloner le Dépôt**

   Clonez le dépôt du projet depuis votre système de gestion de version (par exemple, GitHub) :

   ```bash
   git clone <repository-url>
   cd ddd-deezer/server
   ```

2. **Créer un Environnement Virtuel**

   Il est recommandé de créer un environnement virtuel pour gérer les dépendances :

   ```bash
   python -m venv venv
   ```

   Activez l'environnement virtuel :

   - Sur Windows :
     ```bash
     venv\Scripts\activate
     ```

   - Sur macOS/Linux :
     ```bash
     source venv/bin/activate
     ```

3. **Installer les Dépendances**

   Installez les paquets requis avec pip.

   ```bash
   pip install django==5.2 djangorestframework==3.14 djangorestframework-simplejwt==5.2 django-cors-headers==4.0 django-admin-interface==0.20 colorfield==0.9
   ```

4. **Configurer la Base de Données**

   Mettez à jour les paramètres de la base de données dans `recoMusique/settings.py` en fonction de votre configuration. Par défaut ce projet utilise SQLite, mais vous pouvez le configurer pour utiliser PostgreSQL, MySQL, etc.

5. **Appliquer les Migrations**

   Appliquez les migrations de la base de données pour configurer le schéma initial :

   ```bash
   python manage.py migrate
   ```

6. **Lancer le Serveur de Développement**

   Démarrez le serveur de développement Django :

   ```bash
   python manage.py runserver
   ```

   Vous pouvez maintenant accéder à l'application à l'adresse `http://127.0.0.1:8000/`.
