from decimal import Decimal
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from product.forms import ProductCreateForm, ProductEditForm
from product.models import Product
from catalog.models import Category
from store.models import Store

User = get_user_model()

class ProductFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@test.com', password='1234')
        cls.category = Category.objects.create(title="Test category", description="Test description")
        cls.store = Store.objects.create(title="Test Store", url="https://store.com")

    def test_create_form_invalid_url_pattern(self):
        form_data = {
            'url': 'https://store.com/category',
            'category': self.category.id,
            'store': self.store.id,
        }
        with patch('product.forms.get_pattern', return_value=r'/product/\d+'):
            form = ProductCreateForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn('url', form.errors)
            self.assertIn('URL does not show a single product. Select one product only', form.errors['url'])

    def test_edit_form_fields_disabled(self):
        product = Product.objects.create(
            title="Existing Product",
            category=self.category,
            store=self.store,
            url="https://store.com/product123",
            current_price=Decimal('50.00'),
            currency='EUR',
            user=self.user,
        )
        form = ProductEditForm(instance=product)
        self.assertTrue(form.fields['current_price'].disabled)
        self.assertTrue(form.fields['currency'].disabled)
