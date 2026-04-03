from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from alert.forms import AlertCreateForm, AlertEditForm, AlertDeleteForm
from alert.models import Alert, ArchiveAlert
from django.core.paginator import Paginator
from common.mixins import AppUserQuerysetMixin, PageTitleMixin


# Create your views here.

class AlertCreate(LoginRequiredMixin, PageTitleMixin, CreateView):
    model = Alert
    form_class = AlertCreateForm
    success_url = reverse_lazy('accounts:dashboard')
    template_name = 'common/form_base.html'
    page_title = 'Create new track'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class AlertEdit(LoginRequiredMixin, PageTitleMixin, AppUserQuerysetMixin, UpdateView):
    model = Alert
    form_class = AlertEditForm
    success_url = reverse_lazy('alert:alert_list')
    template_name = 'common/form_base.html'

    def get_page_title(self):
        return f'Update track for {self.object.product}'


class AlertDelete(LoginRequiredMixin, AppUserQuerysetMixin, PageTitleMixin, DeleteView):
    model = Alert
    template_name = 'common/form_delete_category.html'
    success_url = reverse_lazy('alert:alert_list')
    page_title = 'Delete track'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AlertDeleteForm(instance=self.object)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, 'The track has been deleted.')

        return redirect(self.success_url)

class DisplayActiveAlerts(PageTitleMixin, ListView):
    model = Alert
    template_name = 'alerts/alert_list.html'
    page_title = 'All tracks'

    def get_queryset(self):
        return Alert.objects.get_active_alerts()


class DisplayAppUserActiveAlerts(LoginRequiredMixin, AppUserQuerysetMixin, DisplayActiveAlerts):
   pass


class DisplayArchivedAlerts(PageTitleMixin, ListView):
    model = ArchiveAlert
    template_name = 'alerts/alert_history_list.html'
    ordering = '-alert_finished_at'
    paginate_by = 6

    def get_page_title(self):
        return f"All successful tracks of {self.request.user}"


class DisplayAppUserArchiveAlert(LoginRequiredMixin, AppUserQuerysetMixin, DisplayArchivedAlerts):
   pass


class ArchiveAlertInfo(LoginRequiredMixin, UserPassesTestMixin, PageTitleMixin, DetailView):
    model = ArchiveAlert
    template_name = 'alerts/info_single_archive.html'
    context_object_name = 'alert'

    def test_func(self):
        user = self.request.user
        archive = self.get_object()

        return user == archive.user or user.has_perm('alert.view_archivealert')

    def get_page_title(self):
        return f'Display {self.object.id}'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        histories = self.object.history_alerts.all()

        paginator = Paginator(histories, 8)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['timeline'] = page_obj
        context['checks'] = paginator.count
        context['paginator'] = paginator

        return context
