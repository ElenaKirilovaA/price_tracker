from django.http import HttpRequest,HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.base import kwarg_re
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from product.forms import ProductCreateForm, ProductEditForm
from product.models import Product


# Create your views here.


class ProductList(ListView):
    model = Product
    template_name = 'products/product_list.html'
    ordering = '-created_at'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = 'Product List'

        return context


class AddProduct(CreateView):
    model = Product
    form_class = ProductCreateForm
    success_url = reverse_lazy('product:product_list')
    template_name = 'products/form_create_product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = 'Add new product'

        return context


class EditProduct(UpdateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'common/form_base.html'
    success_url = reverse_lazy('product:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = f'Edit product {self.object.title}'

        return context


class DeleteProduct(DeleteView):
    model = Product
    template_name = 'common/form_delete_category.html'
    success_url = reverse_lazy('product:product_list')


class SingleProduct(DetailView):
    model = Product
    template_name = 'products/product_detail_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = f'{self.object.title}'

        return context
