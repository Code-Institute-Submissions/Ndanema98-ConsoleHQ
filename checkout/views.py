from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51N9Qi6A0HdlJUre3QiFIKTGf8GZl11C3FLYgcBiByvMO9S05CLHjZyBBgHXsA7M1SeaPePZP4DOZ9wmufwa1bmoK00iK32zCvO',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)