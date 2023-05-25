from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Product, Category, Deals
from .forms import ProductForm, ReviewForm

# Create your views here.


def all_products(request):
    """A view to show and sort all products and search queries."""

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'categories' in request.GET:
            categories = request.GET['categories'].split(',')
            print(categories)
            products = products.filter(categories__name__in=categories)
            print(products)
            categories = Category.objects.filter(name__in=categories)
            print(categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You have not entered anything!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    discounted_prices = {}
    if categories:
        for category in categories:
            category_products = products.filter(categories=category)
            deals = Deals.objects.filter(category=category).first()
            if deals:
                discount_percentage = deals.discount_percentage
                discounted_prices[category] = [product.price - (product.price * discount_percentage) for product in category_products]
            else:
                discounted_prices[category] = [product.price for product in category_products]

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'discounted_prices': discounted_prices,
    }

    return render(request, 'products/products.html', context)


def products_by_category(request, category):
    """A view to show products filtered by category"""

    products = Product.objects.filter(categories__name=category)
    categories = Category.objects.all()

    context = {
        'products': products,
        'current_category': category,
        'categories': categories,
    }

    return render(request, 'products/products_by_category.html', context)


def product_detail(request, product_id):
    """A view to show the products details individually. """

    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()

    context = {
        'product': product,
        'reviews': reviews,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


def create_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviewform = ReviewForm()
    if request.method == 'POST':
        reviewform = ReviewForm(request.POST)
        if reviewform.is_valid():
            review = reviewform.save(commit=False)
            review.author = request.user
            review.post = product
            review.save()
            return redirect('products:product_detail', product_id=product_id)
    return render(
        request, 'review_form.html', {'reviewform': reviewform, 'product': product})