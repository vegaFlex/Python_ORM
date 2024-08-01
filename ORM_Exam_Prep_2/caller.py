import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Count, F, Q
from decimal import Decimal
from main_app.models import Profile, Product, Order


def get_profiles(search_string=None):
    if search_string is not None:
        profiles = Profile.objects.filter(
            Q(full_name__icontains=search_string) |
            Q(email__icontains=search_string) |
            Q(phone_number__icontains=search_string)
        ).annotate(num_of_orders=Count('order')).order_by('full_name')
    else:
        profiles = Profile.objects.annotate(num_of_orders=Count('order')).order_by('full_name')

    if not profiles:
        return ""

    profile_lines = [
        f"Profile: {profile.full_name}, email: {profile.email}, phone number: {profile.phone_number}, orders: {profile.num_of_orders}"
        for profile in profiles
    ]

    return "\n".join(profile_lines)


def get_loyal_profiles():
    loyal_profiles = Profile.objects.get_regular_customers()

    if not loyal_profiles:
        return ""

    profile_lines = [
        f"Profile: {profile.full_name}, orders: {profile.order_count}"
        for profile in loyal_profiles
    ]

    return "\n".join(profile_lines)


def get_last_sold_products():
    last_order = Order.objects.order_by('-creation_date').first()

    if not last_order:
        return ""

    products = last_order.products.order_by('name')
    if not products:
        return ""

    product_names = [product.name for product in products]

    return f"Last sold products: {', '.join(product_names)}"


def get_top_products():
    top_products = Product.objects.annotate(
        num_orders=Count('order')
    ).filter(
        num_orders__gt=0
    ).order_by(
        '-num_orders', 'name'
    )[:5]

    if not top_products:
        return ""

    product_lines = [
        f"{product.name}, sold {product.num_orders} times"
        for product in top_products]

    return "Top products:\n" + "\n".join(product_lines)


def apply_discounts():
    affected_orders = Order.objects.annotate(num_products=Count('products')).filter(
        num_products__gt=2,
        is_completed=False
    )

    num_of_updated_orders = affected_orders.update(
        total_price=F('total_price') * Decimal('0.90')
    )

    return f"Discount applied to {num_of_updated_orders} orders."


def complete_order():
    oldest_order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if not oldest_order:
        return ""

    for product in oldest_order.products.all():
        product.in_stock -= 1
        if product.in_stock == 0:
            product.is_available = False
        product.save()

    oldest_order.is_completed = True
    oldest_order.save()

    return "Order has been completed!"