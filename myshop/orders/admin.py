from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


def order_detail(obj):
    return mark_safe('<a href="{}">Открыть</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])))


order_detail.short_description = 'Детальнее'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'display_products', 'first_name',
                    'last_name', 'discount', 'get_total_cost',
                    'email', 'address', 'created', 'need_delivery',
                    'paid', 'status', order_detail]
    list_filter = ['paid', 'created', 'updated']
    list_per_page = 10
    inlines = [OrderItemInline]
