from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Item, Employee, Sale, Price
from django.views.generic import DetailView, ListView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator
from annoying.decorators import render_to
from .forms import SaleForm
from django.urls import reverse


# class BaseView(View):
#
#     def get(self, request, *args, **kwargs):
#         items_list = Item.objects.order_by('item_name')
#         context = {
#             'items_list' : items_list
#         }
#         return render(request, 'base.html', context)

@render_to('base.html')
def index(request):
    items_list = Item.objects.order_by('item_name')
    return {'items_list' : items_list}

class PriceView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        item_slug = kwargs.get('slug')
        price_list = Price.objects.order_by('-price_change_time')
        price_name = Item.objects.get(slug = item_slug)
        context = {
            'price_list' : price_list,
            'item_slug' : item_slug,
            'price_name' : price_name,
        }
        return render(request, 'price.html', context)

class SaleInfo(LoginRequiredMixin, ListView):

    model = Sale
    template_name = 'sale.html'
    context_object_name = 'sales_list'
    paginate_by = 5
    queryset = Sale.objects.all().order_by('-purchase_date')


class ItemDetailView(FormMixin, DetailView):

    queryset = Item.objects.all()
    model = Item
    context_object_name = 'item'
    template_name = 'detail.html'
    slug_url_kwarg = 'slug'
    form_class = SaleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_list'] = Employee.objects.all()
        context['sale'] = Sale.objects.all()
        context['form'] = SaleForm(initial={
            'sale': self.object
        })
        return context

    def get_success_url(self):
        return reverse('mainapp:index')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(ItemDetailView, self).form_valid(form)

# class AddSaleView(View): #CreateView FromView
#     def post(self, request, *args, **kwargs):
#         item_slug = kwargs.get('slug')
#         qty = int(request.POST.get('qty'))
#         em_name = request.POST.get('employee')
#         item = Item.objects.get(slug=item_slug)
#         employee = Employee.objects.get(employee_name=em_name)
#         sale = Sale.objects.create(
#             sale_item = item, sale_employee = employee, sale_quantity = qty
#         )
#         return HttpResponseRedirect('/')

# class AddSaleView(CreateView):
#     pass
