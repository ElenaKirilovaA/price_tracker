from django.db.models import Avg, ExpressionWrapper, DurationField, F, Sum

from alert.models import Alert, ArchiveAlert


def get_context_date_home():
    active_tracks_count = Alert.objects.get_active_alerts().count()
    top_alerts = ArchiveAlert.objects.get_archives_by_saved_money()
    saved_money = sum(alert.saved_money_eur for alert in top_alerts)
    avg_trigger_days = (top_alerts
    .aggregate(aver=Avg(ExpressionWrapper(
        F('alert_finished_at') - F('alert_created_at'), output_field=DurationField()))
    ))
    most_profitable_category = (top_alerts
                                .values('category_title')
                                .annotate(
        total_saved=Sum(F('started_price_eur') - F('triggered_price_eur')))
                                .order_by('-total_saved')
                                .first()
                                )

    context_map = {
        'page_title': 'Home Page',
        'counter': active_tracks_count,
        'archivealert_list': top_alerts[:3],
        'counter_archive': top_alerts.count(),
        'saved_money': saved_money or 0,
        'avg': avg_trigger_days['aver'].days if avg_trigger_days['aver'] else None,
        'best_category': most_profitable_category,
    }

    return context_map