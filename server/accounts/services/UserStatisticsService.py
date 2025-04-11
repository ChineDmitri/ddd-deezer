from typing import Dict, Any
from accounts.models import User, UserProfile
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear, TruncDay, TruncWeek

class UserStatisticsService:

    @staticmethod
    def get_user_statistics() -> Dict[str, Any]:
        
        total_users = User.objects.count()
        total_artists = UserProfile.objects.filter(role='artist').count()
        total_listeners = UserProfile.objects.filter(role='listener').count()

        return {
            "total_users" : total_users,
            "total_artists" : total_artists,
            "total_listeners" : total_listeners,
            "artist_percentage" : round((total_artists / total_users * 100), 2) if total_users > 0 else 0,
            "listener_percentage" : round((total_listeners / total_users * 100), 2) if total_users > 0 else 0,
        }
    
    @staticmethod
    def get_user_growth_statistics(period: str = 'month') -> Dict[str, Any]:

        trunc_map = {
            'day': TruncDay,
            'week': TruncWeek,
            'month': TruncMonth,
            'year': TruncYear,
        }

        trunc_function = trunc_map.get(period, TruncMonth)
        user_growth = (
            User.objects.annotate(period=trunc_function('date_joined'))
            .values('period')
            .annotate(user_count=Count('id'))
            .order_by('period')
        )

        return {
            "period": period,
            "growth_data": list(user_growth)
        }
