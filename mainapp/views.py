from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Item, Employee, Sale, Price
from django.views.generic import DetailView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator


class BaseView(View):

    def get(self, request, *args, **kwargs):
        items_list = Item.objects.order_by('item_name')
        context = {
            'items_list' : items_list
        }
        return render(request, 'base.html', context)

class PriceView(View):

    def get(self, request, *args, **kwargs):
        price_change = Price.objects.all()
        context = {
            'price_change' : price_change
        }
        return render(request, 'price.html', context)

class SaleInfo(LoginRequiredMixin, ListView):

    model = Sale
    template_name = 'sale.html'
    context_object_name = 'sales_list'
    paginate_by = 5
    queryset = Sale.objects.all().order_by('-purchase_date')


class ItemDetailView(DetailView):

    queryset = Item.objects.all()
    model = Item
    context_object_name = 'item'
    template_name = 'detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_list'] = Employee.objects.all()
        context['sale'] = Sale.objects.all()
        return context

class AddSaleView(View):
    def post(self, request, *args, **kwargs):
        item_slug = kwargs.get('slug')
        qty = int(request.POST.get('qty'))
        em_name = request.POST.get('employee')
        item = Item.objects.get(slug=item_slug)
        employee = Employee.objects.get(employee_name=em_name)
        sale = Sale.objects.create(
            sale_item = item, sale_employee = employee, sale_quantity = qty
        )
        return HttpResponseRedirect('/')
