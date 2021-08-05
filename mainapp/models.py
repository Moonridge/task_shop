from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Item(models.Model):
    item_name = models.CharField('название товара', max_length = 200)
    item_description = models.TextField('описание товара')
    item_price = models.DecimalField('цена товара', max_digits = 9, decimal_places = 2)
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.item_name

class Employee(models.Model):
    employee_name = models.CharField('имя продавца', max_length = 50)

    def __str__(self):
        return self.employee_name

class Sale(models.Model):
    sale_item = models.ForeignKey(Item, on_delete = models.DO_NOTHING)
    sale_employee = models.ForeignKey(Employee, on_delete = models.DO_NOTHING)
    sale_quantity = models.IntegerField('количество товара', default = 1)
    total_price = models.DecimalField('окончательная цена товара', default = 0, max_digits = 9, decimal_places = 2)
    purchase_date = models.DateTimeField('дата покупки', auto_now=True)

    def __str__(self):
        return "{} куплен {}".format(self.sale_item, self.purchase_date)

    def save(self, *args, **kwargs):
        self.total_price = self.sale_quantity * self.sale_item.item_price
        super().save(*args, **kwargs)


@receiver (post_save, sender = Item)
def price_change(sender, instance, created, update_fields=["item_price"], **kwargs):
        price = Price.objects.create(
            price_item = instance, new_price = instance.item_price,
        )

class Price(models.Model):
    price_item = models.ForeignKey(Item, on_delete = models.CASCADE)
    new_price = models.DecimalField('новая цена', max_digits = 9, decimal_places = 2)
    price_change_time = models.DateTimeField('время изменения цены', auto_now=True)

    def __str__(self):
        return "Новая цена {} для {}".format(self.new_price, self.price_item.item_name)
