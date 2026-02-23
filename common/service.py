from audioop import avgpp

from django.db.models import Avg, F, Sum

from alert.models import Alert, ArchiveAlert


def get_context_date_home():
    active_tracks_count = Alert.objects.get_active_alerts().count()
    top_alerts = ArchiveAlert.objects.get_archives_by_saved_money()
    results = top_alerts.aggregate(total=Sum('saved_money_db'),
                                   aver=Avg(F('alert_finished_at') - F('alert_created_at')),)
    most_profitable_category = (top_alerts
                                .values('category_title')
                                .annotate(total_saved=Sum(F('started_price_eur') - F('triggered_price_eur')))
                                .order_by('-total_saved')
                                .first()
                                )

    context_map = {
        'page_title': 'Home Page',
        'counter': active_tracks_count,
        'archivealert_list': top_alerts[:3],
        'counter_archive': top_alerts.count(),
        'saved_money': results['total'] or 0,
        'avg': results['aver'].days if results['aver'] else None,
        'best_category': most_profitable_category,
    }
    print(context_map)
    return context_map

get_context_date_home()