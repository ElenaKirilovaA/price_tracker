from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import ProtectedError, RestrictedError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from common.mixins import AppUserQuerysetMixin
from product.forms import ProductCreateForm, ProductEditForm
from product.models import Product

# Create your views here.

UserModel = get_user_model()


class ProductList(ListView):
    model = Product
    template_name = 'products/product_list.html'
    ordering = '-created_at'

    def get_context_data(self, **kwargs):

        context = super().get_context_data()
        context['page_title'] = 'Product List'


        return context


class AppUserProductList(LoginRequiredMixin, AppUserQuerysetMixin, ProductList):
    pass

class AppUserFavouriteProductList(AppUserProductList):
    def get_queryset(self):
        return self.request.user.favourite_product.all()

class AddProduct(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    success_url = reverse_lazy('product:product_list')
    template_name = 'products/form_create_product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = 'Add new product'

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class EditProduct(UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'products/form_create_product.html'
    success_url = reverse_lazy('product:product_list')
    permission_required =  'product.change_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = f'Edit product {self.object.title}'

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs


    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return user == product.user or user.has_perm('product.change_product') or user.is_staff


class DeleteProduct(UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'common/form_delete_category.html'
    success_url = reverse_lazy('product:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = f'{self.object.title}'

        return context

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return user == product.user or user.is_staff

    def form_valid(self, form):
        product = self.get_object()

        try:
            product.delete()
            messages.success(self.request,f'The {product} has been deleted.')
        except (ProtectedError, RestrictedError):
            messages.error(self.request,f'The {product} cannot be deleted. The product is tracking by our users.')
        return redirect(self.success_url)


class SingleProduct(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = f'{self.object.title}'

        return context

@login_required
def liked_product(request: HttpRequest, slug: str) -> HttpResponse:
    user = request.user
    current_product = Product.objects.get(slug=slug)

    if current_product in user.favourite_product.all():
        user.favourite_product.remove(current_product)

    else:
        user.favourite_product.add(current_product)

    return redirect('product:list')


