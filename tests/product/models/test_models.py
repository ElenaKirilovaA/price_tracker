from django.contrib.auth import get_user_model
from django.test import TestCase
from decimal import Decimal
from catalog.models import Category
from store.models import Store
from product.models import Product


class ProductModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@test.com',password='1234')
        self.product = Product.objects.create(
            title="Title test",
            description="Test description",
            url="https://example.com/titletest",
            current_price=Decimal("999.99"),
            category=Category.objects.create(title="Test category", description='Test description'),
            user=self.user,
            store=Store.objects.create(title="Test Store"),
        )

    def test_slug_is_generated_on_create(self):
        self.assertIsNotNone(self.product.slug)
        self.assertEqual(self.product.slug, "title-test-test-category")

    def test_slug_not_changed_on_update(self):
        old_slug = self.product.slug

        self.product.title = "New name"
        self.product.save()
        self.product.refresh_from_db()
        self.assertEqual(self.product.slug, old_slug)

    def test_str_method(self):
        expected_result = f"{self.product.title} - {self.product.current_price} {self.product.currency}"
        self.assertEqual(str(self.product), expected_result)

    def test_user_can_add_favorite_product(self):
        self.user.favourite_product.add(self.product)
        self.assertIn(self.product, self.user.favourite_product.all())
        self.assertIn(self.user, self.product.users_favorite.all())

    def test_is_tracking_false_by_default(self):
        self.assertFalse(self.product.is_tracking)
