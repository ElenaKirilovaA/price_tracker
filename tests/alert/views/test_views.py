from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from alert.models import Alert
from catalog.models import Category
from product.models import Product
from store.models import Store

User = get_user_model()


class AlertViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@test.com', password='1234')
        cls.category = Category.objects.create(title='Test Category')
        cls.store = Store.objects.create(title='Test Store', url='https://test.com')
        cls.product = Product.objects.create(
            title='Test Product',
            current_price=100,
            currency='EUR',
            category=cls.category,
            store=cls.store
        )

        cls.alert = Alert.objects.create(
            target_price=50,
            email=cls.user.email,
            product=cls.product,
            user=cls.user
        )

    def test_user_can_access_alert_edit_view(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('alert:edit', kwargs={'pk': self.alert.pk}),
            {
                'target_price': 30,
                'email': self.user.email,
                'product': self.product.id,
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_alert_target_price_is_updated_after_edit(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse('alert:edit', kwargs={'pk': self.alert.pk}),
            {
                'target_price': 30,
                'email': self.user.email,
                'product': self.product.id,
            }
        )
        self.alert.refresh_from_db()
        self.assertEqual(self.alert.target_price, 30)

    def test_display_active_alerts_view(self):
        response = self.client.get(reverse('alert:alert_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.alert.product.title)