from django.db import models

class Item(models.Model):
    item_name = models.CharField('название товара', max_length = 200)
    item_description = models.TextField('описание товара')
    item_price = models.IntegerField('цена товара')
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
    total_price = models.IntegerField('окончательная цена товара', default = 1)
    purchase_date = models.DateTimeField('дата покупки', auto_now=True)

    def __str__(self):
        return "{} куплен {}".format(self.sale_item, self.purchase_date)

    def save(self, *args, **kwargs):
        self.total_price = self.sale_quantity * self.sale_item.item_price
        super().save(*args, **kwargs)


# class Price(models.Model):
#     pass
