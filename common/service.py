from django.db.models import Avg, F, Sum, Count
from alert.models import Alert, ArchiveAlert


def get_context_date_home():
    active_tracks_count = Alert.objects.get_active_alerts()
    top_alerts = ArchiveAlert.objects.get_archives_with_saved_money()
    results = top_alerts.aggregate(total=Sum('saved_money_db'),
                                   average_days=Avg(F('alert_finished_at') - F('alert_created_at')),
                                   archive_count =Count('id'))
    most_profitable_category = (top_alerts
                                .values('category_title')
                                .annotate(total_saved=Sum('saved_money_db'))
                                .order_by('-total_saved')
                                .first()
                                )

    context_map = {
        'page_title': 'Home Page',
        'counter': active_tracks_count.count(),
        'counter_archive': results['archive_count'],
        'saved_money': results['total'] or 0,
        'average_days': results['average_days'].days if results['average_days'] else None,
        'best_category': most_profitable_category or '-',
        'archivealert_list': top_alerts.order_by('-saved_money_db')[:3],

    }

    return context_map
