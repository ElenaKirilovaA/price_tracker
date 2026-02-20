from django import forms

from product.models import Product


class ProductBasicForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['slug','started_price', 'started_price_eur' ,'updated_at']
        labels = {
            'current_price': 'Product price',
            'currency': 'Choose currency'
        }
        error_messages = {
            'title': {
                'required': 'Category title is required.',
                'min_length': 'Category title cannot be less than 2 characters.',
                'max_length': 'Category title cannot exceed 100 characters',
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
    pass


class ProductDeleteForm(ProductBasicForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True
