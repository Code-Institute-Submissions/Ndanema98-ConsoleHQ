from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product, Coupon
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser


def bag_contents(request):
    bag_items = []
    total = Decimal('0')
    product_count = 0
    bag = request.session.get('bag', {})
    free_delivery_threshold = settings.FREE_DELIVERY_THRESHOLD

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        if product.get_discounted_price():
            total += Decimal(product.get_discounted_price()) * Decimal(quantity)
        else:
            total += product.price * Decimal(quantity)
        product_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    coupon_obj = None
    discount_price = Decimal('0')

    coupon_id = request.session.get('applied_coupon')
    if coupon_id:
        coupon_obj = Coupon.objects.filter(
                Q(id=coupon_id) & Q(used=True) & Q(user=request.user)).first()
        print("Coupon Object:", coupon_obj)
        if coupon_obj:
            discount_price = grand_total * Decimal('0.20')
            grand_total -= discount_price
            if grand_total < Decimal('0'):
                grand_total = Decimal('0')

        print("Discounted Price (Coupon):", discount_price)

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': free_delivery_threshold,
        'grand_total': grand_total,
        'applied_coupon': coupon_obj,
        'discount_price': discount_price,
    }

    return context
