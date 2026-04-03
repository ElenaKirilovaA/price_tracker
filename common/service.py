from django.db.models import Avg, F, Sum, Count, ExpressionWrapper, DecimalField
from accounts.models import AppUser
from alert.models import Alert, ArchiveAlert
from catalog.models import Category, Tag
from product.models import Product
from store.models import Store


def get_context_date_home() -> dict:
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

def get_context_date_moderator_home() -> dict:
    products = Product.objects.count()
    categories = Category.objects.count()
    tags = Tag.objects.count()
    stores = Store.objects.count()
    base_context = get_context_date_home()
    moderator_context = {
        'products': products,
        'categories': categories,
        'stores': stores,
        'tags': tags,
    }

    return {**base_context, **moderator_context}

def get_context_data_appuser_manager() -> dict:
    users = AppUser.objects.all()
    context_mapper = {}

    for user in users:
        name = user.get_full_name()
        email = user.email
        user_alerts = user.alerts.count()
        saved_money = (ArchiveAlert.objects
                       .filter(user=user)
                       .aggregate(saved_money_db=Sum(ExpressionWrapper(F('started_price_eur') - F('triggered_price_eur'), output_field=DecimalField()))))
        context_mapper[user.pk] = {
            'name': name,
            'email': email,
            'alerts': user_alerts,
            'saved_money': saved_money['saved_money_db'] or 0,
        }

    return {'context_mapper': context_mapper}
