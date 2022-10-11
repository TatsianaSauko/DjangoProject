from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True).order_by(
        get_order_by_products(request))
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html',
                  {'category': category, 'products': products})


def get_order_by_products(request):
    order_by = ''
    if request.GET.__contains__('sort') and request.GET.__contains__('up'):
        sort = request.GET['sort']
        up = request.GET['up']
        if sort == 'price' or sort == 'name':
            if up == '0':
                order_by = '-'
            order_by += sort
    if not order_by:
        order_by = '-created'
    return order_by


def delivery(request):
    return render(
        request,
        'shop/delivery.html'
    )


def contacts(request):
    return render(
        request,
        'shop/contacts.html'
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


def handler404(request, exception):
    return render(request, '404.html', status=404)
