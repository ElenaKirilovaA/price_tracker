from django import forms

from product.models import Product


class ProductBasicForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['slug', 'started_price', 'started_price_eur' ,'updated_at', 'user']
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
    pass


class ProductEditForm(ProductBasicForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user



        if not self.user.is_staff:

            self.fields['current_price'].disabled = True
            self.fields['currency'].disabled = True

