from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from alert.forms import AlertCreateForm, AlertEditForm, AlertDeleteForm
from alert.models import Alert, ArchiveAlert
from alert.service import manage_simulation_tracking, set_timeline_checks
from django.core.paginator import Paginator

# Create your views here.

class AlertCreate(CreateView):
    model = Alert
    form_class = AlertCreateForm
    success_url = reverse_lazy('common:home-page')
    template_name = 'common/form_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['home_page'] = 'Create new track'

        return context


class AlertEdit(UpdateView):
    model = Alert
    form_class = AlertEditForm
    success_url = reverse_lazy('alert:alert_list')
    template_name = 'common/form_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = f'Update track for {self.object.product}'

        return context


class AlertDelete(DeleteView):
    model = Alert
    template_name = 'common/form_delete_category.html'
    success_url = reverse_lazy('alert:alert_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Delete track'
        context['form'] = AlertDeleteForm(instance=self.object)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, 'The track has been deleted.')

        return redirect(self.success_url)


def check_alerts(request: HttpRequest, product_id:int) -> HttpResponse:
    alerts = Alert.objects.filter(product_id=product_id, is_active=True)

    for alert in alerts:
        set_timeline_checks(alert)

        if alert.price_is_dropped:
            manage_simulation_tracking(alert)
            messages.success(request, 'Your turn. Check your email')

    return redirect('product:product_list')


class DisplayActiveAlerts(ListView):
    model = Alert
    template_name = 'alerts/alert_list.html'

    def get_queryset(self):
        return Alert.objects.get_active_alerts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = 'All tracks'

        return context

class DisplayArchivedAlerts(ListView):
    model = ArchiveAlert
    template_name = 'alerts/alert_history_list.html'
    ordering = '-alert_finished_at'
    paginate_by = 9

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
