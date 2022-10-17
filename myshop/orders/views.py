from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse

from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.need_delivery = True if form.cleaned_data[
                                              'delivery'] == 1 else False
            order.save()
            add_user(form.cleaned_data['first_name'],
                     form.cleaned_data['email'])
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


def add_user(name, email):
    if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
        return
    password = User.objects.make_random_password()
    user = User.objects.create_user(email, email, password)
    user.first_name = name
    group = Group.objects.get(name='Клиенты')
    user.groups.add(group)
    user.save()

    text = get_template('registration/registration_email.html')
    html = get_template('registration/registration_email.html')

    context = {'username': email, 'password': password}

    subject = 'Регистрация'
    from_email = 'from@booksite.by'
    text_content = text.render(context)
    html_content = html.render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@login_required
def orders(request):
    user_orders = Order.objects.filter(email__exact=request.user.email)
    return render(
        request,
        'orders/order/orders.html',
        context={'orders': user_orders}
    )


@login_required
def cancelorder(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.email == request.user.email and order.status == 'NEW':
        order.status = 'CNL'
        order.save()
    return HttpResponseRedirect(reverse('orders:orders'))
