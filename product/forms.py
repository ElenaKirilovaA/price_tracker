from django import forms
from product.models import Product
from product.services import dispatch_store, get_pattern, BaseScraper
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
            qs = Product.objects.filter(url=url, store=store)
            if qs.exists():
                self.add_error('url', 'Our application already has this product from the selected store')

        return cleaned_data


    def save(self, commit=True):
        product = super().save(commit=False)
        scraper: BaseScraper = dispatch_store(product.store.title)
        info = scraper.scrape(product.url)

        if info:
                product.title = info.get('title')
                product.description = info.get('description')
                product.current_price = info.get('price')
                product.currency = info.get('currency')


        if commit:
            product.save()
            tags = self.cleaned_data.get('tag')

            if tags:
                product.tag.set(tags)

            self.save_m2m()

        return product


class ProductEditForm(ProductBasicForm):
    class Meta(ProductBasicForm.Meta):
        fields = ['title', 'category', 'tag', 'description', 'current_price', 'currency']

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['current_price'].disabled = True
        self.fields['currency'].disabled = True
