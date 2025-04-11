from ..Utils import load_data_artists, get_popular_genres_by_region, get_popular_genres_by_region_and_age, calculate_genre_metrics, calculate_region_metrics


class MusicServiceArtist:
    def __init__(self):
        self.df_genre_region_age, self.df_tracks, self.data_loaded = load_data_artists()

    def get_artists_genre_by_region(self, region=None):
        return get_popular_genres_by_region(self.df_genre_region_age, region, True)

    def get_artists_genre_by_region_and_age(self, region=None, age=None):
        return get_popular_genres_by_region_and_age(self.df_genre_region_age, region, age, True)
    
    def get_tracks_from_genre_and_region(self, region=None, genre=None):
        
        tracks = self.df_tracks.copy()

        results = []

        if tracks is None or tracks.empty:
            return {"error": "Données des chansons non chargées"}

        if genre:
            contains_genre = lambda x: genre in x if isinstance(x, list) else genre in str(x)
            # Vérifie que le genre est présent dans au moins une ligne
            if not tracks['all_genres'].apply(contains_genre).any():
                return {"error": "Ce genre n'est pas présent dans les données des chansons"}

            # Filtrer les lignes où le genre est présent dans all_genres
            tracks = tracks[tracks['all_genres'].apply(contains_genre)]
        
        # on filtre par region dans les chansons restants 
        if region:
            contains_region = lambda x: region in x if isinstance(x, list) else region in str(x)
            # Vérifie que la région est présente dans au moins une ligne
            if not tracks['regions_recommandees'].apply(contains_region).any():
                return {"error": "Aucune chanson disponible pour cette région"}
            
            # Filtrer les lignes où la région est présente dans regions_recommandees
            tracks = tracks[tracks['regions_recommandees'].apply(contains_region)]

        result_data = {
            'tracks' : []
        }

        # On transforme la duration de secondes à minutes
        tracks['duration'] = tracks['duration'].apply(lambda x: f"{int(x // 60)}:{int(x % 60):02d}")
        # On utilise que les colonnes pertinantes pour l'affichage (titre, artist, longeur)
        tracks_columns = [col for col in tracks.columns if col in ['title', 'artist_name', 'duration']]

        # On transforme le DF en liste de dictionnaires
        for idx, row in tracks.iterrows():
            track_data = {col: row[col] for col in tracks_columns}
            result_data['tracks'].append(track_data)

        # On ajoute le résultat à la liste des résultats
        results.append(result_data)

        if region and genre:
            return results[0] if results else {"error": f"Aucune donnée pour la région: {region} et le genre: {genre}"}
        
        return results

    def get_metrics_by_genre(self, genre=None):
        
        if self.df_tracks is None or self.df_tracks.empty:
            return {"error": "Données des chansons non chargées"}
        
        tracks = self.df_tracks.copy()

        # Liste des métriques à analyser
        metrics = ['bpm', 'gain', 'duration_minutes', 'danceability', 
                   'energy', 'acousticness', 'instrumentalness', 'valence']
        
        # On s'assure d'avoir les colonnes dans le DF
        valid_metrics = [metric for metric in metrics if metric in tracks.columns]

        if not valid_metrics:
            return {"error": "Aucune métrique valide à analyser"}
        
        return calculate_genre_metrics(tracks, genre, valid_metrics)
        
    def get_metrics_by_region(self, region=None):

        if self.df_tracks is None or self.df_tracks.empty:
            return {"error": "Données des chansons non chargées"}
        
        tracks = self.df_tracks.copy()

        # Liste des métriques à analyser
        metrics = ['bpm', 'gain', 'duration_minutes', 'danceability', 
                   'energy', 'acousticness', 'instrumentalness', 'valence']
        
        # On s'assure d'avoir les colonnes dans le DF
        valid_metrics = [metric for metric in metrics if metric in tracks.columns]

        if not valid_metrics:
            return {"error": "Aucune métrique valide à analyser"}
        
        return calculate_region_metrics(tracks, region, valid_metrics)