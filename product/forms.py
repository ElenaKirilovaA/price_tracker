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


class ProductCreateForm(ProductBasicForm):
    pass


class ProductEditForm(ProductBasicForm):
    # class Meta(ProductBasicForm.Meta):
    #     exclude = ['currency']
    pass


class ProductDeleteForm(ProductBasicForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True
