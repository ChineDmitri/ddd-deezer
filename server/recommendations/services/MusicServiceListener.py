from ..Utils import load_data_listeners, get_popular_genres_by_region, get_popular_genres_by_region_and_age

class MusicServiceListeners:
    def __init__(self):
        self.df_genre_region_age, self.data_loaded = load_data_listeners()

    def get_listeners_genre_by_region(self, region=None):
        return get_popular_genres_by_region(self.df_genre_region_age, region)
    
    def get_listeners_genre_by_region_and_age(self, region=None, age=None):
        return get_popular_genres_by_region_and_age(self.df_genre_region_age, region, age)