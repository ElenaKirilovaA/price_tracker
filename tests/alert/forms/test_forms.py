from decimal import Decimal
from django.test import TestCase
from alert.forms import AlertCreateForm
from product.models import Product
from catalog.models import Category
from accounts.models import AppUser
from store.models import Store

class AlertFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AppUser.objects.create_user(email="test@test.com", password="123456")
        cls.category = Category.objects.create(title="Category", description="desc")
        cls.store = Store.objects.create(title="Test Store", url="https://store.com")
        cls.product = Product.objects.create(
            title="Test Product",
            description="Product desc",
            url="https://store.com/product123",
            current_price=Decimal("100.00"),
            category=cls.category,
            store=cls.store,
            user=cls.user
        )

    def test_alert_create_form_valid(self):
        form_data = {
            'target_price': Decimal("90.00"),
            'email': "test@test.com",
            'product': self.product.id,
        }
        form = AlertCreateForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
