from django import forms
from product.models import Product
from product.services import dispatch_store, get_pattern
import re


class ProductBasicForm(forms.ModelForm):
    class Meta:
        model = Product

        fields = '__all__'
        labels = {
            'current_price': 'Product price',
            'currency': 'Choose currency'
        }
        error_messages = {
            'title': {
                'required': 'Product title is required.',
                'min_length': 'Product title cannot be less than 2 characters.',
                'max_length': 'Product title cannot exceed 100 characters',
            }
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter description:'}),
            'url': forms.URLInput(attrs={'placeholder': 'ex: https://'}),
        }
        help_texts = {
            'tag': 'choose a tag or create your own'
        }


class ProductCreateForm(ProductBasicForm):
    class Meta(ProductBasicForm.Meta):
        fields = ['url', 'category', 'tag', 'store']

    def clean(self):
        cleaned_data = super().clean()
        store = cleaned_data.get('store')
        url = cleaned_data.get('url')

        if store and url:
            pattern = get_pattern(store.title)

            if store.url not in url:
                self.add_error('url', 'URL not from the selected store')
            elif not re.search(pattern, url):
                self.add_error('url', 'URL does not show a single product. Select one product only')

        return cleaned_data


    def save(self, commit=True):
        product = super().save(commit=False)
        info = dispatch_store(product.url, product.store.title)

        if info:
            product.title = info.get('title')
            product.description = info.get('description')
            product.current_price = info.get('price')
            product.currency = info.get('currency')

        if commit:
            product.save()

        return product


class ProductEditForm(ProductBasicForm):
    class Meta(ProductBasicForm.Meta):
        fields = ['title', 'category', 'tag', 'description', 'current_price', 'currency']

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['current_price'].disabled = True
        self.fields['currency'].disabled = True
