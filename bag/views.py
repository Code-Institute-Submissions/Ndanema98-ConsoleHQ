from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser

from django.http import JsonResponse
from .utils import send_subscription_email, generate_coupon_code
from products.models import Product, NewsletterSubscription

# Create your views here.


def view_bag(request):
    if isinstance(request.user, AnonymousUser):
        newsletter_subscription = None
    else:
        newsletter_subscription = NewsletterSubscription.objects.filter(
            user=request.user).first()

    context = {
        'newsletter': newsletter_subscription
    }
    return render(request, 'bag/bag.html', context=context)


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(
            request, f'Updated {product.name} quantity for {bag[item_id]}')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag.')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the
    specified product to the specified amount """

    product = get_object_or_404(Product, pk=item_id)
    bag = request.session.get('bag', {})
    quantity = int(request.POST.get('quantity'))

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(
            request, f'Updated {product.name} quantity for {bag[item_id]}')
    else:
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag.')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def delete_item_bag(request, item_id):
    """ Remove the specified product from the shopping bag """
    try:
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})
        bag.pop(item_id, None)
        messages.success(request, f'Removed {product.name} from your bag.')
        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)


def subscribe_to_newsletter(request):
    if request.user.is_authenticated:

        object, created = NewsletterSubscription.objects.get_or_create(
            user=request.user)
        checkbox = request.GET.get("newsletter")
        email = request.GET.get("email")
        if checkbox:
            if not object.subscribed:
                object.subscribed = True
                message = "Subscribed to newsletter successfully!"
                send_subscription_email(object.user)
            else:
                object.subscribed = False
                message = "Unsubscribed from newsletter successfully!"
            object.save()
        else:
            message = "Invalid request. Newsletter checkbox not found."
        return JsonResponse({"message": message}, status=200)

    return JsonResponse({"message": "User Not Validated"})
