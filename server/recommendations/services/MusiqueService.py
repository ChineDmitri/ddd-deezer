import os
import pandas as pd
import numpy as np
from django.conf import settings

class MusiqueService:
    def __init__(self):
        self.data_dir = settings.DATA_DIR
        self.load_data()

    def load_data(self):
        try:
            # Chemin ver les données du CSV
            genre_region_age_path = os.path.join(self.data_dir, 'df_genre_region_age_augmente.csv')
            tracks_path = os.path.join(self.data_dir, 'df_tracks.csv')

            # Chargement des données
            self.df_genre_region_age = pd.read_csv(genre_region_age_path)
            self.df_tracks = pd.read_csv(tracks_path)

            print("Données chargées avec succès!")
            print(f"- Nombre de régions chargées : {self.df_genre_region_age.shape[0]}")
            print(f"- Nombre de pistes chargées : {self.df_tracks.shape[0]}")

            self.data_loaded = True
        except Exception as e:
            print(f"Erreur lors du chargement des données : {e}")
            self.data_loaded = False
    
    def get_popular_genres_by_region(self, region=None):

        if not self.data_loaded:
            return {"error": "Données non chargées."}

        df = self.df_genre_region_age.copy()

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

    def get_popular_genres_by_region_and_age(self, region=None, age_group=None):
        if not self.data_loaded:
            return {"error": "Données pas chargées"}
        
        df = self.df_genre_region_age.copy()

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
        
        sorted_genres = sorted(genres_scores.items(), key=lambda x: x[1], reverse=True)

        # Calculer le score maximum pour normaliser sur 10
        if sorted_genres:
            # Score du genre le plus populaire
            max_score = sorted_genres[0][1]
        else:
            # Évite division par zéro
            max_score = 1
        
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
                

                
        

