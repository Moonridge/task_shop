from django.test import TestCase
from django.contrib.auth.models import User
from .models import Item, Employee, Sale, Price



class ShopTestCases(TestCase):

    fixtures = ['initial_data.json', 'models.json']

    def setUp(self) -> None:
        self.user = User.objects.create_user(username = "testuser", password = "password")
        self.item = Item.objects.get(pk = 1)
        self.employee = Employee.objects.get(pk = 1)
        # self.item = Item.objects.create(
        #     item_name = "test name",
        #     item_description = "test description",
        #     item_price = 10,
        #     slug = "testslug",
        # )
        # self.employee = Employee.objects.create(employee_name = "test name")

    def test_response_from_start_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.item_name)

    def test_detail_response(self):
        response = self.client.get('/items/testslug/')
        self.assertEqual(response.status_code, 200)

    # def test_sale_form_post(self):
    #     response = self.client.post('/add_sale/testslug/', {
    #         'slug': self.item.slug,
    #         'employee': self.employee.employee_name,
    #         'qty' : '4',
    #     }, follow = True)
    #     new_sale = Sale.objects.get(id = 1)
    #     self.assertEqual(new_sale.sale_quantity, 4)
    #     self.assertEqual(new_sale.total_price, 40)
    #     self.assertRedirects(response, '/')
    #     self.assertEqual(response.status_code, 200)

    def test_sale_response(self):
        response = self.client.get('/sales/')
        self.assertEqual(response.status_code, 302)
        self.client.post('/login/', {
            'name': self.user.username,
            'password': self.user.password,
        }, follow = True)
        response = self.client.get('/sales/', follow = True)
        self.assertEqual(response.status_code, 200)

    def test_price_save(self):
        start_price = Price.objects.get(id = 1)
        self.assertEqual(self.item.item_price, start_price.new_price)
        updated_item_price = self.item
        updated_item_price.item_price = 20
        updated_item_price.save()
        new_price = Price.objects.get(new_price = 20)
        self.assertEqual(updated_item_price.item_price, new_price.new_price)
