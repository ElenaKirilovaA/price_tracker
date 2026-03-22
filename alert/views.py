from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from alert.forms import AlertCreateForm, AlertEditForm, AlertDeleteForm
from alert.models import Alert, ArchiveAlert
from alert.service import manage_simulation_tracking, set_timeline_checks
from django.core.paginator import Paginator

from common.mixins import AppUserQuerysetMixin


# Create your views here.

class AlertCreate(LoginRequiredMixin, CreateView):
    model = Alert
    form_class = AlertCreateForm
    success_url = reverse_lazy('accounts:dashboard')
    template_name = 'common/form_base.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = 'Create new track'

        return context


    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class AlertEdit(LoginRequiredMixin, AppUserQuerysetMixin, UpdateView):
    model = Alert
    form_class = AlertEditForm
    success_url = reverse_lazy('alert:alert_list')
    template_name = 'common/form_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = f'Update track for {self.object.product}'

        return context


class AlertDelete(LoginRequiredMixin, AppUserQuerysetMixin, DeleteView):
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


class DisplayAppUserActiveAlerts(LoginRequiredMixin, AppUserQuerysetMixin, DisplayActiveAlerts):
   pass


class DisplayArchivedAlerts(ListView):
    model = ArchiveAlert
    template_name = 'alerts/alert_history_list.html'
    ordering = '-alert_finished_at'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = f"All successful tracks of {self.request.user}"

        return context


class DisplayAppUserArchiveAlert(LoginRequiredMixin, AppUserQuerysetMixin, DisplayArchivedAlerts):
   pass


class ArchiveAlertInfo(LoginRequiredMixin, AppUserQuerysetMixin, DetailView):
    model = ArchiveAlert
    template_name = 'alerts/info_single_archive.html'
    context_object_name = 'alert'


    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        histories = self.object.history_alerts.all()

        paginator = Paginator(histories, 8)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_title'] = f'Display {self.object.id}'
        context['page_title'] = f'Display {self.object.id}'
        context['timeline'] = page_obj
        context['checks'] = paginator.count
        context['paginator'] = paginator

        return context
