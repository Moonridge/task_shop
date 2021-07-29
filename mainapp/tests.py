from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Item, Employee, Sale, Price

User = get_user_model()

class ShopTestCases(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username = "testuser", password = "password")
        self.item = Item.objects.create(
            item_name = "test name",
            item_description = "test description",
            item_price = "10",
            slug = "testslug",
        )
        self.employee = Employee.objects.create(employee_name = "test name")
        self.sale = Sale.objects.create(
            sale_item = self.item,
            sale_employee = self.employee,
        )

    def test_response_from_start_page(self):
        client = Client()
        response = client.get('')
        self.assertEqual(response.status_code, 200)
