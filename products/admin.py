from django.contrib import admin
from .models import (
    Product, Category, Review, Deals, NewsletterSubscription, Coupon
)
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'display_categories',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    display_categories.short_description = 'Categories'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):

    list_display = (
        'name', 'content', 'product', 'date_posted', 'approved', 'author')
    list_filter = ('approved', 'date_posted')
    search_fields = ['name', 'email', 'content']
    summernote_fields = ('content')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(approved=True)


@admin.register(Deals)
class DealsAdmin(admin.ModelAdmin):
    list_display = ('category', 'discount_percentage')


class CouponAdmin(admin.ModelAdmin):
    list_display = ['discount_code', 'user', 'used']
    list_filter = ['used']
    search_fields = ['discount_code', 'user__username']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(NewsletterSubscription)
admin.site.register(Coupon, CouponAdmin)
