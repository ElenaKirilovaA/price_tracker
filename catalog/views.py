from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models.deletion import ProtectedError, RestrictedError
from django.utils.timezone import now
from django.views.decorators.http import require_POST

from alert.models import ArchiveAlert
from catalog.forms import CategoryCreateForm, CategoryEditForm, CategoryDeleteForm, TagFormSet
from catalog.models import Category, Tag
from catalog.service import create_tags

# Create your views here.


def catalog_overview(request: HttpRequest) -> HttpResponse:
    catalog = (Category.objects
               .annotate(
                    product_count=Count('products', distinct=True),
                    deals_count=Count('archives', distinct=True))
               .order_by('-deals_count', '-product_count', 'title', ))

    context = {
        'page_title': 'Catalog Overview',
        'catalog': catalog,
        'star_category': catalog[0] if catalog else None
    }
    return render(request, 'catalog/category_list_page.html', context)


def add_category(request:HttpRequest) -> HttpResponse:
    form = CategoryCreateForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('catalog:catalog-overview')

    context = {
        'page_title': 'Add category',
        'form': form,

    }

    return render(request, 'common/form_base.html', context)


def edit_category(request:HttpRequest, category_id: int) -> HttpResponse:
    category = get_object_or_404(Category, id=category_id)
    form = CategoryEditForm(request.POST or None, request.FILES or None, instance=category)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('catalog:catalog-overview')

    context = {
        'page_title': f'Update {category}',
        'form': form,
    }
    return render(request, 'common/form_base.html', context)


def delete_category(request: HttpRequest, category_id: int) -> HttpResponse:
    category = get_object_or_404(Category, id=category_id)
    form = CategoryDeleteForm(request.POST or None, instance=category)

    if request.method == 'POST':
        try:
            category.delete()
            messages.success(request, f'The {category} has been deleted.')
        except (ProtectedError, RestrictedError):
            messages.error(request, f'The {category} can not be deleted. There is connection.')


        return redirect('catalog:catalog-overview')

    context = {
        'page_title': f'Delete {category}',
        'form': form,
    }

    return render(request, 'common/form_delete_category.html', context)


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


def tag_display(request:HttpRequest) -> HttpResponse:
    tags = Tag.objects.all().order_by('title')

    context = {
        'page_title': 'Tags display',
        'tags': tags,
    }
    return render(request, 'catalog/tag_list.html', context)


@require_POST
def tag_bulk_delete(request:HttpRequest) -> HttpResponse:
    tags = request.POST.getlist('selected_tags')

    if tags:
        tags_str = 'tags have' if len(tags) > 1 else 'tag has'
        messages.success(request, f'{len(tags)} {tags_str} been deleted.')
        Tag.objects.filter(id__in=tags).delete()

    return redirect('product:create')


def category_info(request:HttpRequest, category_id: int) -> HttpResponse:
    category = (Category.objects
                .prefetch_related('products', 'products__alerts', 'products__tag', 'archives')
                .get(id=category_id))
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
