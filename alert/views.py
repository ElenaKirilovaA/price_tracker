from django.contrib import messages
from django.contrib.admin.templatetags.admin_list import pagination
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from alert.forms import AlertCreateForm, AlertEditForm, AlertDeleteForm
from alert.models import Alert, ArchiveAlert
from alert.service import manage_simulation_tracking, set_timeline_checks
from django.core.paginator import Paginator


# Create your views here.
def alert_create(request: HttpRequest) -> HttpResponse:
    form = AlertCreateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('common:home-page')

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
    form = AlertDeleteForm(request.POST or None, instance=alert)

    if request.method == 'POST':
        alert.delete()
        messages.success(request, f'The track has been deleted.')

        return redirect('alert:alert_list')

    context = {
        'page_title': 'Delete track',
        'form': form,
    }

    return render(request, 'common/form_delete_category.html', context)



class DisplayArchivedAlerts(ListView):
    model = ArchiveAlert
    template_name = 'alerts/alert_history_list.html'
    ordering = '-alert_finished_at'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = "All successful tracks"

        return context

def archive_alert_info(request: HttpRequest, archived_id: int) -> HttpResponse:
    alert = get_object_or_404(ArchiveAlert, id=archived_id)
    timelines = alert.history_alerts.all()

    paginator = Paginator(timelines, 8)
    page_number = request.GET.get('page')
    timeline = paginator.get_page(page_number)

    context = {
        'page_title': f'Display {alert.id}',
        'alert': alert,
        'timeline': timeline,
        'checks': timelines.count(),
    }

    return render(request, 'alerts/info_single_archive.html', context)

