from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from demo.forms import RegisterUserForm
from demo.models import User, Product, Orders, Basket, Goods, Category


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')


def validate_username(request):
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


def about(request):
    products = Product.objects.filter(count__gte=1).order_by('-date')
    return render(request, 'demo/about.html', context={
            'products': products
    })


def catalog(request):
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    order_by = request.GET.get('order_by')
    if order_by:
        products = products.order_by(order_by)
    return render(request, 'demo/catalog.html',
                  context={
                      'products': products,
                      'category': Category.objects.all()
                  })


def contact(request):
    return render(request, 'demo/contact.html')


def product(request, pk):
    products = Product.objects.get(pk=pk)
    return render(request, 'demo/product.html', context={
        'products': products
    })


@login_required
def cart(request):
    cart_items = request.user.basket_set.all()
    return render(request, 'demo/cart.html',
                  context={
                      'cart_items': cart_items,
                  })


@login_required
def checkout(request):
    password = request.GET.get('password', None)
    valid = request.user.check_password(password)
    if not valid:
        return JsonResponse({
            'error': 'Не верный пароль'
        })
    item_in_cart = request.user.basket_set.all()
    if not item_in_cart:
        return JsonResponse({
            'error': 'Корзина пуста'
        })
    order = Orders.objects.create(user=request.user)
    # for item in item_in_cart:
    #     ItemInOrder.objects.create(order=order, product=item.product, price=item.price)
    item_in_cart.delete()
    return JsonResponse({
        'message': 'Order is processed'
    })


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Orders
    template_name = 'demo/orders.html'

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user).order_by('-date')


@login_required
def delete_order(request, pk):
    order = Orders.objects.filter(user=request.user, pk=pk, role='new')
    if order:
        order.delete()
    return redirect('orders')


@login_required
def to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    items_in_cart = Basket.objects.filter(user=request.user, product=product).first()
    if items_in_cart:
        if items_in_cart + 1 == 1:
            return JsonResponse({
                'error': 'Can\'t add more'
            })
        items_in_cart.cout += 1
        items_in_cart.save()
        return JsonResponse({
            'count': items_in_cart.count
        })
    items_in_cart = Basket(user=request.user, product=product)
    items_in_cart.save()
    return JsonResponse({
        'count': items_in_cart.count
    })
