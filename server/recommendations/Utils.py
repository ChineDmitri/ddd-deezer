import os
from django.conf import settings
import pandas as pd

def load_data_artists():

    try:
        # Chemin ver les données du CSV
        genre_region_age_path = os.path.join(settings.DATA_DIR, 'df_genre_region_age_augmente.csv')
        tracks_path = os.path.join(settings.DATA_DIR, 'df_tracks.csv')

        # Chargement des données
        df_genre_region_age = pd.read_csv(genre_region_age_path)
        df_tracks = pd.read_csv(tracks_path)

        print("Données chargées avec succès!")
        print(f"- Nombre de régions chargées : {df_genre_region_age.shape[0]}")
        print(f"- Nombre de pistes chargées : {df_tracks.shape[0]}")

        return df_genre_region_age, df_tracks, True
    except Exception as e:
        print(f"Erreur lors du chargement des données : {e}")
        return None, None, False
    
def load_data_listeners():

    try:
        # Chemin ver les données du CSV
        genre_region_age_path = os.path.join(settings.DATA_DIR, 'df_genre_region_age_augmente.csv')

        # Chargement des données
        df_genre_region_age = pd.read_csv(genre_region_age_path)

        print("Données chargées avec succès!")
        print(f"- Nombre de régions chargées : {df_genre_region_age.shape[0]}")

        return df_genre_region_age, True
    except Exception as e:
        print(f"Erreur lors du chargement des données : {e}")
        return None, False
    
def get_popular_genres_by_region(df_genre_region_age, region=None, artist=False):
    if df_genre_region_age is None or df_genre_region_age.empty:
        return {"error": "Données non chargées."}

    df = df_genre_region_age.copy()

    if region:
        if region not in df['Nom_region'].values:
            return {"error": f"Région '{region}' non trouvée."}
        
        # Filtrer par région
        df = df[df['Nom_region'] == region]

    results = []

    # On parcourt le DF pour chaque région
    for idx, row in df.iterrows():
        region_name = row['Nom_region']
        region_data = {
            'region': region_name,
            'genres': []
        }

    # Extraction des genres et de leur popularité
    genres_columns = [col for col in df.columns if col != 'Nom_region']
    genres_scores = {}

    # On transforme le genre car data set du type 'jeune_rap'
    for col in genres_columns:
        genre_part = col.split('_')
        if len(genre_part) >= 2:
            genre = genre_part[0]
            if genre not in genres_scores:
                genres_scores[genre] = 0
            genres_scores[genre] += row[col]

    # On trie les genres par popularité
    sorted_genres = sorted(genres_scores.items(), key=lambda x: x[1], reverse=True)

    # Calculer le score maximum pour normaliser sur 10
    if sorted_genres:
        # Score du genre le plus populaire
        max_score = sorted_genres[0][1]
    else:
        # Évite division par zéro
        max_score = 1
    
    if artist:
        # Ajout des scores dans le résultat, normalisés sur 10
        for genre, score in sorted_genres:
            # Normalisation du score sur 10
            normalized_score = min(10, round((score / max_score) * 10, 1))
            
            region_data["genres"].append({
                'genre': genre,
                'score': f"{normalized_score}/10",
                'raw_score': score
            })
    else: 
        # Ajout des scores dans le résultat, normalisés sur 10
        for genre, score in sorted_genres[:10]:
            # Normalisation du score sur 10
            normalized_score = min(10, round((score / max_score) * 10, 1))
            
            region_data["genres"].append({
                'genre': genre,
                'score': f"{normalized_score}/10",
                'raw_score': score
            })

    results.append(region_data)

    if region:
        return results[0] if results else {"error": f"Aucune donnée pour la région: {region}"}
    
    return results

def get_popular_genres_by_region_and_age(df_genre_region_age, region=None, age_group=None, artist=False):
    if df_genre_region_age is None or df_genre_region_age.empty:
        return {"error": "Données pas chargées"}
    
    df = df_genre_region_age.copy()

    if region:
        if region not in df['Nom_region'].values:
            return {"error": f"Région '{region}' non trouvée."}
        
        df = df[df['Nom_region'] == region]

    results = []

    # On parcourt le DF pour chaque région
    for idx, row in df.iterrows():
        region_name = row['Nom_region']
        region_data = {
            'region': region_name,
            'genres': [],
        }
    
    genres_columns = [col for col in df.columns if col != 'Nom_region']
    genres_scores = {}

    # On transforme les genres et on recupère juste ceux qui correspondent à l'age
    for col in genres_columns:
        genre_part = col.split('_')
        if len(genre_part) >= 2:
            genre = genre_part[0]
            age = genre_part[1]

            if age_group == age:
                if genre not in genres_scores:
                    genres_scores[genre] = 0
                genres_scores[genre] += row[col]
    
    # On trie les genres par popularité
    sorted_genres = sorted(genres_scores.items(), key=lambda x: x[1], reverse=True)

    # Calculer le score maximum pour normaliser sur 10
    if sorted_genres:
        # Score du genre le plus populaire
        max_score = sorted_genres[0][1]
    else:
        # Évite division par zéro
        max_score = 1
    
    if artist:
        # Ajout des scores dans le résultat, normalisés sur 10
        for genre, score in sorted_genres:
            # Normalisation du score sur 10
            normalized_score = min(10, round((score / max_score) * 10, 1))
            
            region_data["genres"].append({
                'genre': genre,
                'score': f"{normalized_score}/10",
                'raw_score': score
            })
    else:
        # Ajout des scores dans le résultat, normalisés sur 10
        for genre, score in sorted_genres[:10]:
            # Normalisation du score sur 10
            normalized_score = min(10, round((score / max_score) * 10, 1))
            
            region_data["genres"].append({
                'genre': genre,
                'score': f"{normalized_score}/10",
                'raw_score': score
            })
    
    region_data["age_group"] = age_group
    results.append(region_data)

    if region:
        return results[0] if results else {"error": f"Aucune donnée pour la région: {region}"}
    
    return results

def calculate_genre_metrics(df, genre, valid_metrics):
    print(f"LE GENRE EST {genre}")
    # On explode la liste des genres pour avoir une ligne par genre
    df_exploded = df.explode('all_genres')

    # On filtre par genre
    if genre:
        df_exploded = df_exploded[df_exploded['all_genres'].str.contains(genre, na=False)]
        if df_exploded.empty:
            return {"error": f"Aucune donnée pour le genre: {genre}"}
    
    resuls = df_exploded.groupby('all_genres')[valid_metrics].mean().reset_index()

    # Formatage des résultats
    genre_stats = []
    for _, row in resuls.iterrows():
        genre_data = {
            'genre': genre,
            'metrics': {metric: round(row[metric], 2) if not pd.isna(row[metric]) else 0 for metric in valid_metrics}
        }
        genre_stats.append(genre_data)
    
    # On retourne les résultats du genre passé en paramètre
    if genre:
        return genre_stats[0] if genre_stats else {"error": f"Aucune donnée pour le genre: {genre}"}
    return genre_stats

def calculate_region_metrics(df, region, valid_metrics):
    # On explode la liste des regions pour avoir une ligne par région
    df_exploded = df.explode('regions_recommandees')
    # On filtre par région
    if region:
        df_exploded = df_exploded[df_exploded['regions_recommandees'].str.contains(region, na=False)]
        if df_exploded.empty:
            return {"error": f"Aucune donnée pour la région: {region}"}

    # Groupement par région et calcul de la moyenne
    resuls = df_exploded.groupby('regions_recommandees')[valid_metrics].mean().reset_index()

    # Formatage des résultats
    region_stats = []
    for _, row in resuls.iterrows():
        region_data = {
            'region': region,
            'metrics': {metric: round(row[metric], 2) if not pd.isna(row[metric]) else 0 for metric in valid_metrics}
        }
        region_stats.append(region_data)

    # On retourne les résultats de la région passée en paramètre
    if region:
        return region_stats[0] if region_stats else {"error": f"Aucune donnée pour la région: {region}"}
    return region_stats
    
