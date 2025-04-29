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


--- 

# Instructions de Configuration pour le Client (Front-end) Vue.js

Interface utilisateur pour la plateforme développée avec Vue 3 et TypeScript.

## Prérequis

- Node.js v20.17.0
- npm (inclus avec Node.js)

### Installation des dépendances

```bash
npm install
```

### Lancement du serveur de développement

```bash
npm run dev
```

Le serveur de développement sera accessible à l'adresse locale indiquée dans le terminal (généralement http://localhost:5173).

### Compilation et minification pour la production

```bash
npm run build
```

## Structure du projet

- **src/** - Code source de l'application
  - **assets/** - Ressources statiques (images, styles)
  - **components/** - Composants Vue réutilisables
  - **router/** - Configuration des routes de l'application
  - **services/** - Services et utilitaires
  - **views/** - Composants Vue représentant des pages complètes

## Fonctionnalités principales

- **Authentification** - Gestion des utilisateurs et des rôles
- **Tableau de bord administrateur** - Statistiques et monitoring
- **Visualisation des tendances** - Carte interactive des genres populaires

## Technologies utilisées

- Vue.js 3 avec l'API de composition
- TypeScript
- Vue Router pour la navigation
- Chart.js pour la visualisation de données
- Vite comme outil de build

## Exécution des tests
Assurez-vous que le serveur backend Django est en cours d'exécution sur le port 8000
Assurez-vous que le client frontend Vue.js est en cours d'exécution sur le port 5173
Exécutez les tests d'intégration:
\# À partir de la racine du projet
```bash
python -m unittest discover tests/integration
```
