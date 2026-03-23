from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models.deletion import ProtectedError, RestrictedError
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from catalog.forms import CategoryCreateForm, CategoryEditForm, CategoryDeleteForm, TagFormSet
from catalog.models import Category, Tag
from catalog.service import create_tags

# Create your views here.

class CatalogOverview(ListView):
    model = Category
    template_name = 'catalog/category_list_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        catalog = (Category.objects
                   .annotate(
                    product_count=Count('products', distinct=True),
                    deals_count=Count('archives', distinct=True))
                   .order_by('-deals_count', '-product_count', 'title', ))

        context['page_title'] = 'Catalog Overview'
        context['catalog'] = catalog
        context['star_category'] = catalog[0] if catalog else None

        return context


class AddCategory(UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    success_url = reverse_lazy('catalog:catalog-overview')
    template_name = 'common/form_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = 'Add category'

        return context

    def test_func(self):
        user = self.request.user

        return user.has_perm('catalog.add_category') or user.is_staff


class EditCategory(UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryEditForm
    success_url = reverse_lazy('catalog:catalog-overview')
    template_name = 'common/form_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = self.get_object()
        context['page_title'] = f'Update {product}'

        return context

    def test_func(self):
        user = self.request.user

        return user.has_perm('catalog.change_category') or user.is_staff


class DeleteCategory(UserPassesTestMixin, DeleteView):
    model = Category
    form_class = CategoryDeleteForm
    success_url = reverse_lazy('catalog:catalog-overview')
    template_name = 'common/form_delete_category.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()

        return kwargs

    def form_valid(self, form):
        category = self.get_object()

        try:
            category.delete()
            messages.success(self.request,f'The {category} has been deleted.')
        except (ProtectedError, RestrictedError):
            messages.error(self.request,f'The {category} cannot be deleted. There are related objects.')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['page_title'] = f'Delete {category}'

        return context

    def test_func(self):
        user = self.request.user

        return user.has_perm('catalog.delete_category') or user.is_staff


def bulk_create_tags(request:HttpRequest) -> HttpResponse:
    formset_tag = TagFormSet(request.POST or None)

    if request.method == 'POST' and formset_tag.is_valid():
        all_tags = set()

        for form in formset_tag:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):  # cleaned_data -> {'title': 'cool', 'DELETE': False}
                all_tags.add(form.cleaned_data['title'])

        new_tags = create_tags(all_tags)

        if new_tags:
            tags = 'tags have' if len(new_tags) > 1 else 'tag has'
            messages.success(request, f'{len(new_tags)} {tags} been created.'  )

        return redirect('product:create')

    context = {
        'page_title': 'Tag creation',
        'form': formset_tag,
    }

    return render(request, 'catalog/tag_create.html', context)

@permission_required('catalog.delete_tag', raise_exception=True)
def tag_display(request:HttpRequest) -> HttpResponse:
    tags = Tag.objects.all().order_by('title')

    context = {
        'page_title': 'Tags display',
        'tags': tags,
    }
    return render(request, 'catalog/tag_list.html', context)

@require_POST
@permission_required('catalog.delete_tag', raise_exception=True)

def tag_bulk_delete(request:HttpRequest) -> HttpResponse:
    tags = request.POST.getlist('selected_tags')

    if tags:
        tags_str = 'tags have' if len(tags) > 1 else 'tag has'
        messages.success(request, f'{len(tags)} {tags_str} been deleted.')
        Tag.objects.filter(id__in=tags).delete()

    return redirect('product:create')

def category_info(request:HttpRequest, pk: int) -> HttpResponse:
    category = (Category.objects
                .prefetch_related('products', 'products__alerts', 'products__tag', 'archives')
                .get(id=pk))
    last_deal_obj = category.archives.order_by('-alert_finished_at').first()
    products = category.products.all()

    last_deal = None
    if last_deal_obj:
        last_deal = (now().date() - last_deal_obj.alert_finished_at.date()).days


    context = {
        'page_title': f'Category {category.title} - products',
        'category': category,
        'last_deal': last_deal,
        'products': products,
    }

    return render(request, 'catalog/current_category_page.html', context)
