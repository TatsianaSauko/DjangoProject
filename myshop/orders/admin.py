from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'display_products', 'first_name',
                    'last_name', 'get_total_cost',
                    'email', 'address', 'created', 'need_delivery',
                    'paid', 'status']
    list_filter = ['paid', 'created', 'updated']
    list_per_page = 10
    inlines = [OrderItemInline]
