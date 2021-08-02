from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Item, Employee, Sale, Price

User = get_user_model()
client = Client()

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

    def test_response_from_start_page(self):
        response = client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.item_name)

    def test_sale_form_post(self):
        response = client.post('/add_sale/testslug/', {
            'slug': self.item.slug,
            'employee': self.employee.employee_name,
            'qty' : '4',
        }, follow = True)
        new_sale = Sale.objects.get(id = 1)
        self.assertEqual(new_sale.sale_quantity, 4)
        self.assertEqual(new_sale.total_price, 40)
        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 200)

    def test_sale_response(self):
        client.post('/login/', {
            'name': self.user.username,
            'password': self.user.password,
        }, follow = True)
        response = client.get('/sales/', follow = True)
        self.assertEqual(response.status_code, 200)

    def test_price_save(self):
        start_price = Price.objects.get(id = 1)
        self.assertEqual(self.item.item_price, str(start_price.new_price))
        updated_item_price = self.item
        updated_item_price.item_price = '20'
        updated_item_price.save()
        new_price = Price.objects.get(new_price = '20')
        self.assertEqual(updated_item_price.item_price, str(new_price.new_price))
