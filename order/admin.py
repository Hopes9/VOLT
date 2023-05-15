from coreapi.compat import force_text
from django.contrib import admin
from django.db.models import Q
from .func import send_my_email_pay
from .models import Order, Order_list, Status


@admin.register(Order_list)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_name', 'money', 'count')

    def product_name(self, obj):
        return obj.product.product_id.name


class Product_Admin_inline_order(admin.TabularInline):
    model = Order_list

    def product_name(self, obj):
        return obj.product.product_id.name

    def ml(self, obj):
        return obj.product.ml

    readonly_fields = ('product_name', 'ml')
    fields = ('order', 'product_name', 'ml', 'money', 'count')
    extra = 0


class CustomFilter(admin.SimpleListFilter):
    title = 'Фильтр заказов'
    parameter_name = 'custom_filter_parameter'
    default_value = 'status_not_finish'

    def lookups(self, request, model_admin):
        return (
            ('all', 'Все'),
            ('status_not_finish', 'Все кроме завершенных'),
            ('status_create', 'Созданные'),
            ('on_pay', 'Оплата'),
            ('delivery', 'В доставке'),
            ('status_finish', 'Завершенные'),

        )

    def choices(self, changelist):
        """
        Overwrite this method to prevent the default "All".
        """
        value = self.value() or self.default_value
        for lookup, title in self.lookup_choices:
            yield {
                'selected': value == force_text(lookup),
                'query_string': changelist.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        value = self.value() or self.default_value
        if value == 'status_create':
            return queryset.filter(status=Status.CREATED)
        elif value == 'status_finish':
            return queryset.filter(status=Status.Completed)
        elif value == 'status_not_finish':
            return queryset.filter(~Q(status=Status.Completed))
        elif value == 'on_pay':
            return queryset.filter(status=Status.ON_PAY)
        elif value == 'delivery':
            return queryset.filter(status=Status.Delivery)
        elif value == 'finish':
            return queryset.filter(status=Status.Completed)
        else:
            return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = (CustomFilter,)
    list_display = (
        'id', 'id_user', 'data_order', 'status', 'delivery', 'sum', 'count_product',
        'pay',
        'pay_online')
    list_editable = ['status', 'sum', 'count_product']
    list_per_page = 20
    ordering = ("-data_order",)
    inlines = [Product_Admin_inline_order]

    def save_model(self, request, obj, form, change):
        sd = Order.objects.get(id=obj.id)
        if sd.status != 1:
            if obj.status == 1:
                if sd.pay_online:
                    send_my_email_pay(lang='ru', order=obj)
        super(OrderAdmin, self).save_model(request, obj, form, change)
