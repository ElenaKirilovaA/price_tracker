from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from decimal import Decimal
from catalog.models import Category
from store.models import Store
from product.models import Product
from alert.models import Alert
from django.contrib.auth import get_user_model

User = get_user_model()

class AlertModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@test.com', password='1234')
        cls.category = Category.objects.create(title="Test category", description='Test description')
        cls.store = Store.objects.create(title="Test Store")
        cls.product = Product.objects.create(
            title="Title test",
            description="Test description",
            url="https://example.com/titletest",
            current_price=Decimal("999.99"),
            category=cls.category,
            user=cls.user,
            store=cls.store,
        )
        cls.alert = Alert.objects.create(
            target_price=Decimal("900.00"),
            email="test@test.com",
            product=cls.product,
            user=cls.user,
        )

    def test_started_price_is_set_automatically(self):
        alert = self.alert
        self.assertEqual(alert.started_price, self.product.current_price)

    def test_price_is_dropped_true(self):
        alert = self.alert
        self.product.current_price = Decimal("800.00")
        self.product.save()
        self.assertTrue(alert.price_is_dropped)

    def test_triggered_price_is_set_when_price_drops(self):
        self.product.current_price = Decimal("800.00")
        self.product.save()
        self.alert.save()
        self.assertEqual(self.alert.triggered_price, Decimal("800.00"))

    def test_clean_raises_error_if_target_price_invalid(self):
        alert = Alert(
            target_price=Decimal("1000.01"),
            started_price=Decimal("1000.00"),
            email="test@test.com",
            product=self.product,
            user=self.user,
        )
        with self.assertRaises(ValidationError):
            alert.clean()

    def test_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            Alert.objects.create(
                target_price=Decimal("900.00"),
                email="test@test.com",
                product=self.product,
                user=self.user,
            )