from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .utils import cookieCart, cartData, guestOrder
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
# Create your views here.


def home_page(request): 
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {"products": products, "cartItems": cartItems}
    return render(request, "products.html", context)


def cart_page(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "cart.html", context)


def checkout_page(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "checkout.html", context)


def vegetable_page(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.filter(catogery=2)
    context = {"products": products, "cartItems": cartItems}
    return render(request, "vegetables.html", context)


def fruits_page(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.filter(catogery=1)
    context = {"products": products, "cartItems": cartItems}
    return render(request, "fruits.html", context)


def homemade_products_page(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.filter(catogery=3)
    context = {"products": products, "cartItems": cartItems}
    return render(request, "homemade_products.html", context)


def natural_products_page(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.filter(catogery=4)
    context = {"products": products, "cartItems": cartItems}
    return render(request, "natural_products.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
	    orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
	    orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if (orderItem.quantity <= 0):
	    orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
	    customer = request.user.customer
	    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
	    customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
	    order.complete = True
    order.status = 'Pending'
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        state=data['shipping']['state'],
        city=data['shipping']['city'],
        pincode=data['shipping']['pincode'],
    )

    return JsonResponse('Payment submitted..', safe=False)


@unauthenticated_user
def register_page(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('home')
    else:
        form = CreateUserForm()
    return render(request, 'registration/register.html', {'form': form})


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    shippingdetails = ShippingAddress.objects.get(order = order)
    items = OrderItem.objects.get(order = order)
    if request.method == "POST":
        order.delete()
        shippingdetails.delete()
        items.delete()
        return redirect('my_orders_page')
    context = {'item': order}
    return render(request, 'delete.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(user)
            return redirect("home")
        else:
            messages.info(request, "Username or Password is incorrect")

    context = {}
    return render(request, "registration/login.html", context)


def about_page(request):
    context = {}
    return render(request, "about.html", context)


@login_required(login_url='login')
def my_orders_page(request):
    customer = request.user.customer
    order = Order.objects.filter(customer = customer, complete = True)
    items = OrderItem.objects.filter(order__in = order)
    context = {"items": items}
    return render(request, "myorder.html", context)


def view_page(request, pk):
    data = cartData(request)
    cartItems = data['cartItems']
    product = Product.objects.get(id = pk)
    images = ProductImage.objects.filter(product = product)
    similarproducts = Product.objects.filter(catogery = product.catogery)
    context = {"product": product, "images": images, "similarproducts": similarproducts, "cartItems": cartItems}
    return render(request, "view_products.html", context)    
