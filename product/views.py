from django.http import HttpRequest,HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from product.forms import ProductCreateForm, ProductEditForm, ProductDeleteForm
from product.models import Product


# Create your views here.

def product_list(request: HttpRequest) -> HttpResponse:

    products = Product.objects.prefetch_related('tag', 'alerts').order_by('-created_at')

    context = {
        'page_title': 'Product List',
        'products': products,

    }

    return render(request, 'products/product_list.html', context)


def add_product(request: HttpRequest) -> HttpResponse:
    form = ProductCreateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()

        return redirect('product:product_list')

    context = {
        'page_title': 'Add product',
        'form': form,

    }

    return render(request, 'products/form_create_product.html', context)


def edit_product(request: HttpRequest, slug: str) -> HttpResponse:
    product = get_object_or_404(Product, slug=slug)
    form = ProductEditForm(request.POST or None, instance=product)

    if request.method == 'POST' and form.is_valid():
        form.save()

        return redirect('product:product_list')

    context = {
        'page_title': 'Add product',
        'form': form,
    }

    return render(request, 'common/form_base.html', context)


def delete_product(request: HttpRequest, slug: str) -> HttpResponse:
    product = get_object_or_404(Product, slug=slug)
    form = ProductDeleteForm(request.POST or None, instance=product)

    if request.method == 'POST':
        product.delete()

        return redirect('product:product_list')

    context = {
        'page_title': 'Add product',
        'form': form,
        'product': product,
    }

    return render(request, 'common/form_delete_category.html', context)


def single_product(request:HttpRequest, slug=str) -> HttpResponse:
    product = get_object_or_404(Product, slug=slug)

    context = {
       ' page_title': f'{product.title}',
        'product': product,
    }

    return render(request, 'products/product_detail_page.html', context)



