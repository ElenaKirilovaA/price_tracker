from django import forms

from alert.models import Alert


class AlertBasicForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['target_price', 'email', 'product']
        error_messages = {
            'email': {
                'required': 'Please enter your email address.',
                'invalid': 'Please enter a valid email address.',
            },
            'product': {
                'required': 'Please select a product.',
            }
        }


        labels = {
            'target_price': 'Your target',
            'product': 'Choose product'
        }


    def clean(self):
        cleaned = super().clean()
        target_price = cleaned.get('target_price')
        product = cleaned.get('product')

        if not target_price or not product:
            return cleaned  # няма как да валидираме без поле target_price или product

        # Ако started_price още не е зададен, вземаме текущата цена на продукта
        started_price = self.instance.started_price or getattr(product, 'current_price', None)

        if started_price is None:
            return cleaned  # няма стойност за сравнение, пропускаме

        if target_price >= started_price:
            self.add_error('target_price', f'Target price must be less than started price ({started_price}).')

        return cleaned


class AlertCreateForm(AlertBasicForm):
    pass

class AlertEditForm(AlertBasicForm):
    pass


class AlertDeleteForm(AlertBasicForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for n, f in self.fields.items():
            f.widget.attrs['readonly'] = True
            f.widget.attrs['disabled'] = True


