from django import forms
from django.forms.formsets import formset_factory

from catalog.models import Category


class CategoryBasicForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['created_at']
        labels = {
            'title': 'Category name:'
        }
        help_texts = {
            'description': 'Provide a brief description of the destination.',
        }
        error_messages = {
            'title': {
                'required': 'Category title is required.',
                'max_length': 'Category title cannot be less than 2 characters.',
            }
        }

class CategoryCreateForm(CategoryBasicForm):
    pass

class CategoryEditForm(CategoryBasicForm):
    pass

class CategoryDeleteForm(CategoryBasicForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True


class TagForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        min_length=2,
        label='Tag title',
    )

TagFormSet = formset_factory(
    TagForm,
    extra=10,
    can_delete=True,
)










