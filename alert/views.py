from django.contrib import messages
from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from alert.forms import AlertCreateForm, AlertEditForm
from alert.models import Alert, ArchiveAlert
from alert.service import manage_simulation_tracking, set_timeline_checks


# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    active_tracks_count =  Alert.objects.get_active_alerts().count()
    top_alerts = ArchiveAlert.objects.get_archives_by_saved_money()
    saved_money = sum(alert.saved_money_eur for alert in top_alerts)

    context = {
        'page_title': 'Home Page',
        'counter': active_tracks_count,
        'alerts': top_alerts[:3],
        'counter_archive': top_alerts.count(),
        'saved_money': saved_money or 0,
    }

    return render(request, 'common/home_page.html', context)


def alert_create(request: HttpRequest) -> HttpResponse:
    form = AlertCreateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('alert:home-page')

    context ={
        'home_page': 'Create new track',
        'form': form,
    }

    return render(request, 'common/form_base.html', context)


def check_alerts(request: HttpRequest, product_id:int) -> HttpResponse:
    alerts = Alert.objects.filter(product_id=product_id, is_active=True)

    for alert in alerts:
        set_timeline_checks(alert)

        if alert.price_is_dropped:
            manage_simulation_tracking(alert)
            messages.success(request, 'Your turn. Check your email')

    return redirect('product:product_list')


def display_active_alert(request:HttpRequest) -> HttpResponse:
    alerts = Alert.objects.get_active_alerts()

    context = {
        'page_title': 'All tracks',
        'alerts': alerts,
    }

    return render(request, 'alerts/alert_list.html', context)


def alert_edit(request:HttpRequest, alert_id: int) -> HttpResponse:
    alert = get_object_or_404(Alert, id=alert_id)
    form = AlertEditForm(request.POST or None, instance=alert)

    if request.method == 'POST' and form.is_valid():
        form.save()

        return  redirect('alert:alert_list')

    context = {
        'page_title': f'Update track for {alert.product}',
        'form': form,
    }

    return render(request, 'common/form_base.html', context)


def alert_delete(request:HttpRequest, alert_id: int) -> HttpResponse:
    alert = get_object_or_404(Alert, id=alert_id)
    form = AlertEditForm(request.POST or None, instance=alert)

    if request.method == 'POST':
        alert.delete()
        messages.success(request, f'The track has been deleted.')

        return redirect('alert:alert_list')

    context = {
        'page_title': 'Delete track',
        'form': form,
    }

    return render(request, 'common/form_delete_category.html', context)


def display_archived_alert(request:HttpRequest) -> HttpResponse:
    alerts = ArchiveAlert.objects.get_archives_by_saved_money()

    context = {
        'page_title': 'All tracks',
        'alerts': alerts,
    }

    return render(request, 'alerts/alert_history_list.html', context)


def archive_alert_info(request: HttpRequest, archived_id: int) -> HttpResponse:
    alert = get_object_or_404(ArchiveAlert, id=archived_id)
    timeline = alert.history_alerts.all()

    context = {
        'page_title': f'Display {alert.id}',
        'alert': alert,
        'timeline': timeline,
    }

    return render(request, 'alerts/info_single_archive.html', context)

